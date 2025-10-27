<template>
    <div>
      <div class="content-block">
        <div class="dx-card responsive-paddings back-colored">
  
          <div class="content-header">
            <dx-toolbar class="back-colored">
              <dx-item location="before">
                <div class="content-title">A/S접수·처리 현황</div>
              </dx-item>
            </dx-toolbar>
          </div>
  
          <div>
            <div class="search-status search-line">
              <span class="search-title">등록일자</span>
              <dx-date-box v-model:value="vars.formData.startDate" />
              
              <span class="search-bar">~</span>
              <dx-date-box v-model:value="vars.formData.endDate" />
              
              <span class="search-tab"></span>
              <SearchButtonGroup @change="({startDate, endDate}) => { vars.formData.startDate = startDate; vars.formData.endDate = endDate; }" />
              
            </div>
            <div class="search-status" style="display: flex; align-items: center;">
              <span class="search-title">접수 담당자</span>
              <dx-lookup
                value-expr="emp_name"
                display-expr="emp_name"
                v-model:value="vars.formData.receipt_manager"
                :data-source="vars.dataSource.employee"
                />
              <span class="search-tab"></span>
              <span class="search-title">처리 담당자</span>
              <dx-lookup 
                value-expr="emp_name"
                display-expr="emp_name"
                v-model:value="vars.formData.result_manager"
                :data-source="vars.dataSource.employee"
                />
              <span class="search-tab"></span>
              <span>
                <dx-radio-group v-model:value="vars.formData.closing_yn" :items="vars.dataSource.closing_yn" valueExpr="value" displayExpr="text" layout="horizontal"/>
              </span>
              <span class="search-tab"></span>
              <dx-button text="검색" icon="search" @click="methods.searchDateRange()" />
              <span class="search-tab"></span>
              <dx-button text="초기화" icon="" @click="methods.searchReset()" />
            </div>
          </div>
  
        </div>
  
        <div class="dx-card responsive-paddings mt-1">
          <dx-data-grid
            height="calc(100vh - 230px)"
            column-resizing-mode="widget"
            :show-borders="true"
            :column-auto-width="true"
            :remote-operations="true"
            :focused-row-enabled="true"
            :allow-column-resizing="true"
            :allow-column-reordering="true"
            :row-alternation-enabled="true"
            :data-source="vars.dataSource.receipt_result_status"
            :on-initialized="evt => methods.onGridInitialized(evt, 'status')"
            @exporting="methods.onExporting"
            @row-dbl-click="methods.goReceiptDetail"
          >
            <dx-column caption="A/S접수번호" data-field="receipt_number" :sort-index="1" sort-order="desc" />
            <dx-column caption="A/S처리번호" data-field="result_number" />
            <dx-column caption="처리일자" data-field="result_date" data-type="date" format="yyyy-MM-dd" alignment="center" />
            <dx-column caption="접수일자" data-field="receipt_date" sort-order="desc" data-type="date" format="yyyy-MM-dd" alignment="center" />
            <dx-column caption="프로젝트명" data-field="project_name" />
            <dx-column caption="프로젝트번호" data-field="project_number" />
            <dx-column caption="수요기관" data-field="contract_company" />
            <dx-column caption="접수 담당자" data-field="receipt_manager" alignment="center" />
            <dx-column caption="처리 담당자" data-field="result_manager" alignment="center" />
            <dx-column caption="접수내용" data-field="receipt_detail" />
            <dx-column caption="처리내용" data-field="result_detail" />
            <dx-column caption="처리현황" data-field="process_status" />
            <dx-column caption="최종현황" data-field="final_status" />
            <dx-column caption="완료여부" data-field="closing_yn" />
            <dx-column caption="유무상 구분" data-field="paid_type" alignment="center" />
            <dx-column caption="A/S처리비용" data-field="result_price" data-type="number" format="currency"/>
            <dx-sorting mode="single" />
            <dx-export :enabled="true" />
            <dx-paging :page-size="20" />
            <dx-filter-row :visible="true" />
            <dx-column-chooser mode="select" :enabled="true" />
          </dx-data-grid>
        </div>
      </div>
    </div>
</template>
  
<script>
import moment from 'moment';

import { reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';

import { alert } from 'devextreme/ui/dialog';
import DxButton from 'devextreme-vue/button';
import DxCheckBox from 'devextreme-vue/check-box';
import { DxRadioGroup } from 'devextreme-vue/radio-group';

import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxColumnChooser } from 'devextreme-vue/data-grid';
import DxLookup from 'devextreme-vue/select-box';
import stateStore from '@/utils/state-store';
import ArrayStore from 'devextreme/data/array_store';
import SearchButtonGroup from '../../components/search-button-group.vue';
import { loadEmployee } from '../../utils/data-loader';
import { baseCodeLoader } from '../../data-source/base';
import { getAsReceiptResultStatus, asReceiptResultStatus } from '../../data-source/as';
export default {
    components: {
      DxButton,
      DxCheckBox,
      DxDateBox,
      DxToolbar, DxItem,
      DxForm, DxLabel, DxGroupItem, DxSimpleItem,
      DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxColumnChooser,
      SearchButtonGroup,
      DxLookup,
      DxRadioGroup
    },
    setup() {
      const router = useRouter();
      const vars = {};
      vars.grid = {};
      vars.now = new Date();
      vars.formData = reactive({
        startDate: new Date(vars.now.getFullYear(), vars.now.getMonth(), vars.now.getDate() - 7),
        endDate: new Date(vars.now.getFullYear(), vars.now.getMonth(), vars.now.getDate(), 23, 59, 59),
        receipt_manager: null,
        result_manager: null,
        closing_yn: 'ALL',
      });
  
      vars.dataSource = reactive({
        employee: null,
        receipt_result_status: getAsReceiptResultStatus(),
        closing_yn: [
            { value: 'true', text: '완료' },
            { value: 'false', text: '미처리' },
            { value: 'ALL', text: '전체' },
        ]
      });
  
      onMounted(async () => {
        await loadEmployee(vars.dataSource);
      })
      const methods = {
        onGridInitialized(evt, key) {
          vars.grid[key] = evt.component;
          stateStore.bind(`as-receipt-result-status-${key}`, evt.component);
          methods.searchDateRange();
      
        },

        goReceiptDetail({ data }) {
          router.push({ path: `/as/receipt/${data.receipt_id}` });
        },

        async searchDateRange() {
          if (vars.formData.startDate > vars.formData.endDate) {
            await alert('조회 일자가 잘못 되었습니다', '조회');
            return;
          }
  
          try{
            vars.grid['status'].beginCustomLoading('데이터를 집계중입니다');
            const filters = [];
            vars.grid['status'].clearFilter();
  
            if (vars.formData.startDate) {
              filters.push(['receipt_date', '>=', moment(vars.formData.startDate).format('YYYY-MM-DD HH:mm:ss')]);
            }
            if (vars.formData.endDate) {
              filters.push(['receipt_date', '<=', moment(vars.formData.endDate).format('YYYY-MM-DD HH:mm:ss')]);
            }
            if (vars.formData.receipt_manager) {
              filters.push(['receipt_manager', '=', vars.formData.receipt_manager]);
            }
            if (vars.formData.result_manager) {
              filters.push(['result_manager', '=', vars.formData.result_manager]);
            }
            console.log(vars.formData.closing_yn);
            if (vars.formData.closing_yn !== 'ALL') {
              filters.push(['closing_yn', '=', vars.formData.closing_yn === 'true' ? true : false]);
            }
            vars.grid['status'].filter(filters);
          }catch(ex){
            console.log(ex);
          }finally{
            vars.grid['status'].endCustomLoading();
          }
          vars.grid['status'].refresh();
  
        },
        onExporting (evt) {
          asReceiptResultStatus.exportData(evt.component, 'A/S접수·처리 현황', `A/S접수·처리 현황_${Date.now()}.xlsx`)
          evt.cancel = true
        },
        searchReset(){
          vars.formData.receipt_manager = null;
          vars.formData.result_manager = null;
          vars.formData.closing_yn = 'ALL';
        }
      };
  
      return { vars, methods };
    },
};
</script>
