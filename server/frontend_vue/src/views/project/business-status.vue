<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before"
              ><div class="content-title">영업현황</div></dx-item
            >
          </dx-toolbar>
        </div>
        <div class="search-status search-line">
          <span class="search-title">영업일자</span>
          <dx-date-box v-model:value="vars.formData.startDate" />
          
          <span class="search-bar">~</span>
          <dx-date-box v-model:value="vars.formData.endDate" />
          
          <span class="search-tab"></span>
          <SearchButtonGroup @change="({startDate, endDate}) => { vars.formData.startDate = startDate; vars.formData.endDate = endDate; }" />
          
        </div>

        <div class="search-status">
          <span class="search-title">당사담당자</span>
          <dx-lookup 
            value-expr="emp_name"
            display-expr="emp_name"
            v-model:value="vars.formData.employee"
            :data-source="vars.dataSource.employee"
            />
          <span class="search-tab"></span>
          <span class="search-title">현재단계</span>
          <dx-lookup 
            value-expr="code_name"
            display-expr="code_name"
            v-model:value="vars.formData.business_status"
            :data-source="vars.dataSource.business_status"
            />
          <span class="search-tab"></span>
          <span class="search-title">진행현황</span>
          <dx-lookup 
            value-expr="code_name"
            display-expr="code_name"
            v-model:value="vars.formData.business_progress"
            :data-source="vars.dataSource.business_progress"
            />
          <span class="search-tab"></span>
          <dx-button text="검색" icon="search" @click="methods.searchDateRange()" />
          <span class="search-tab"></span>
          <dx-button text="초기화" icon="" @click="methods.searchReset()" />
        </div>
    </div>

      <div class="dx-card responsive-paddings mt-1">
        <dx-data-grid
          height="calc(100vh - 230px)"
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="{
            filtering: true,
            grouping: true,
            groupPaging: true,
            paging: true,
            sorting: true,
            summary:false
          }"
          :focused-row-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :data-source="dataSource"
          :filter-sync-enabled="true"
          :on-initialized="evt => methods.onGridInitialized(evt, 'status')"
          @exporting="methods.onExporting"
          @row-dbl-click="methods.goOrderDetail"
        >
          <dx-column caption="영업번호" data-field="business_number" />
          <dx-column caption="영업건명" data-field="business_name" />
          <dx-column caption="고객업체" data-field="client_company" />
          <dx-column caption="업체담당자" data-field="client_manager" />
          <dx-column caption="담당부서" data-field="business_department"  />
          <dx-column caption="당사담당자" data-field="business_manager" />
          <dx-column caption="진행현황" data-field="business_progress" />
          <dx-column caption="현재단계" data-field="business_status" />
          <dx-column caption="영업금액" data-field="business_amount" format="₩,##0" />
          <dx-column caption="영업일자" data-field="business_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="중요" data-field="business_important" />
          <dx-column caption="프로젝트" data-field="project.project_number" />
          <dx-column caption="수정자" data-field="modify_manager" />
          <dx-column caption="수정일자" data-field="modify_date" data-type="date" format="yyyy-MM-dd" />
         
          <dx-summary>
            <dx-total-item column="business_amount" summary-type="sum" value-format="fixedPoint" display-format="영업금액: {0}" />
          </dx-summary>
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
import DxLookup from 'devextreme-vue/select-box';
import { alert } from 'devextreme/ui/dialog';
import DxButton from 'devextreme-vue/button';
import DxCheckBox from 'devextreme-vue/check-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxColumnChooser, DxSummary, DxTotalItem } from 'devextreme-vue/data-grid';

import SearchButtonGroup from '../../components/search-button-group.vue';
import ArrayStore from 'devextreme/data/array_store';
import stateStore from '@/utils/state-store';
import { projectBusiness } from '../../data-source/project';
import { loadEmployee } from '../../utils/data-loader';
import { baseCodeLoader } from '../../data-source/base';

export default {
  components: {
    DxButton,
    DxCheckBox,
    DxDateBox,
    DxToolbar, DxItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem,
    DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxColumnChooser, DxSummary, DxTotalItem,
    SearchButtonGroup,
    DxLookup
  },
  setup() {
    const router = useRouter();
    const vars = {};
    vars.grid = {};
    vars.formData = reactive({
      startDate: new Date(),
      endDate: new Date(),
      employee: null,
      business_status: null,
      business_progress: null,
    });
    vars.dataSource = reactive({
      employee: null,
      business_status: null,
      business_progress: null,
    })
    const dataSource = new ArrayStore({ key: 'grid_id', data: [] })
    // vars.formData.startDate.setDate(vars.formData.startDate.getDate() - 7);
    onMounted(async () => {
      await loadEmployee(vars.dataSource);
      await methods.loadBaseCode();
    })
    const methods = {
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`project-business-${key}`, evt.component);


        // methods.searchDateRange();
      },

      goOrderDetail({ data }) {
        router.push({ path: `/project/business/${data.id}` });
      },
      calculateTotalPriceWithDecimal(unitPrice, quantity) {
        const decimalPlaces = (unitPrice.toString().split('.')[1] || '').length;
        const conversionUnit = Math.pow(10, decimalPlaces);
        const roundedUnitPrice = Math.round(unitPrice * conversionUnit);
        const total = Math.floor(roundedUnitPrice * quantity / conversionUnit);

        return total;
      },
      getParams () {
        const startDate = moment(vars.formData.startDate).startOf('day').format('YYYY-MM-DD 00:00:00');
        const endDate = moment(vars.formData.endDate).endOf('day').format('YYYY-MM-DD 23:59:59');

        const params = {
            filter: [
                ['business_date', '>=', startDate],
                'and',
                ['business_date', '<=', endDate],
            ],
            sort: [{ selector: 'business_date', desc: true }],
            skip: 0,
            take: 10000,
        };

        if (vars.formData.employee) params.filter.push('and', ['business_manager', '=', vars.formData.employee]);
        if (vars.formData.business_status) params.filter.push('and', ['business_status', '=', vars.formData.business_status]);
        if (vars.formData.business_progress) params.filter.push('and', ['business_progress', '=', vars.formData.business_progress]);

        return params;
      },

      async searchDateRange() {
        if (vars.formData.startDate > vars.formData.endDate) {
          await alert('조회 일자가 잘못 되었습니다', '조회');
          return;
        }

        try{
          dataSource.clear()
          vars.grid['status'].beginCustomLoading('데이터를 집계중입니다')
          const params = methods.getParams(); 

          const { data } = await projectBusiness.load(params);
          console.log("data : ", data)
          let i = 1;
          data.forEach((v) => {
            v.grid_id = i++
            dataSource.insert(v);
          });
        }catch(ex){
          console.error(ex)
        }finally{
          vars.grid['status'].endCustomLoading()
        }
        vars.grid['status'].refresh() 
      },
      loadBaseCode(){
        return baseCodeLoader(['현재단계', '진행현황']).then(response =>{
          vars.dataSource.business_status = response['현재단계'];
          vars.dataSource.business_progress = response['진행현황'];
        })
      },
      onExporting(evt) {
        projectBusiness.exportData(evt.component, '영업현황', `영업현황_${Date.now()}.xlsx`);
        evt.cancel = true;
      },
      searchReset(){
        vars.formData.employee = null;
        vars.formData.business_status = null;
        vars.formData.business_progress = null;
      }
    };

    return { vars, methods, projectBusiness, dataSource };
  },
};
</script>
<style scoped>
.search-title{
  width: 70px;
}
</style>