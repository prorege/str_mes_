<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">

        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">프로젝트현황</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div>
          <div class="search-status search-line">
            <span class="search-title">계약일자</span>
            <dx-date-box v-model:value="vars.formData.startDate" />
            
            <span class="search-bar">~</span>
            <dx-date-box v-model:value="vars.formData.endDate" />
            
            <span class="search-tab"></span>
            <SearchButtonGroup @change="({startDate, endDate}) => { vars.formData.startDate = startDate; vars.formData.endDate = endDate; }" />
            
          </div>
          <div class="search-status">
            <span class="search-title">등록자</span>
            <dx-lookup
              value-expr="emp_name"
              display-expr="emp_name"
              v-model:value="vars.formData.employee"
              :data-source="vars.dataSource.employee"
              />
            <span class="search-tab"></span>
            <span class="search-title">진행단계</span>
            <dx-lookup 
              value-expr="code_name"
              display-expr="code_name"
              v-model:value="vars.formData.progress_status"
              :data-source="vars.dataSource.progress_status"
              />
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
          :data-source="dataSource"
          :on-initialized="evt => methods.onGridInitialized(evt, 'status')"
          @exporting="methods.onExporting"
          @row-dbl-click="methods.goProjectDetail"
        >
          <dx-column 
            caption="실행계획"
            data-field="excution_yn"
            data-type="boolean"
            true-text="등록"
            false-text="미등록"
          />
          <dx-column caption="프로젝트번호" data-field="project_number" :sort-index="1" sort-order="desc" />
          <dx-column caption="프로젝트명" data-field="project_name" />
          <dx-column caption="등록일자" data-field="project_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
          <dx-column caption="원발주처" data-field="order_company" />
          <dx-column caption="원청업체" data-field="contract_company" />
          <dx-column caption="등록부서" data-field="project_department" />
          <dx-column caption="등록담당자" data-field="project_manager" />
          <dx-column caption="계약일자" data-field="contract_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="하자만기" data-field="defect_end_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="착공일자" data-field="commencement_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="준공일자" data-field="completion_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="하자기간" data-field="defect_period" />
          <dx-column caption="자사금액" data-field="company_amount" data-type="number" format="currency"/>

          <dx-column caption="진행단계" data-field="progress_status" />
          <dx-column caption="연결영업 번호" data-field="business.business_number" />
          <dx-column caption="중요" data-field="project_important" />
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
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxColumnChooser } from 'devextreme-vue/data-grid';
import DxLookup from 'devextreme-vue/select-box';
import stateStore from '@/utils/state-store';
import ArrayStore from 'devextreme/data/array_store';
import { projectRegistration } from '../../data-source/project';
import SearchButtonGroup from '../../components/search-button-group.vue';
import { loadEmployee } from '../../utils/data-loader';
import { baseCodeLoader } from '../../data-source/base';
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
  },
  setup() {
    const router = useRouter();
    const vars = {};
    vars.grid = {};
    vars.formData = reactive({
      startDate: new Date(),
      endDate: new Date(),
      employee: null,
      progress_status: null,
    });

    vars.dataSource = reactive({
      employee: null,
      progress_status: null,
    });

    const dataSource = new ArrayStore({ key: 'grid_id', data: [] })

    onMounted(async () => {
      await loadEmployee(vars.dataSource);
      await methods.loadBaseCode();
    })
    const methods = {
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`project-status-${key}`, evt.component);

        // methods.initSorting();
        // methods.searchDateRange();
      },
      initSorting() {
        const columns = vars.grid['status'].getVisibleColumns();
        const col = columns.filter(item => item.sortOrder);
        if (col.length == 0) {
          const defaultName = 'contract_date';
          const defaultSort = columns.filter(item => item.name == defaultName);
          if (defaultSort.length > 0) {
            vars.grid['status'].columnOption(defaultSort[0].index, 'sortOrder', 'desc');
          }
        }
      },
      calcSupplyPrice(rowData) {
        let supply_price = 0;
        if (rowData.quote_quantity && rowData.unit_price) {
          supply_price = rowData.quote_quantity * rowData.unit_price;
        }
        rowData.supply_price = supply_price;
        return supply_price;
      },
      availableStock(rowData) {
        if (!rowData.basic_stock) return '0';
        return rowData.basic_stock.available_stock;
      },
      currentStock(rowData) {
        if (!rowData.basic_stock) return '0';
        return rowData.basic_stock.current_stock;
      },
      goProjectDetail({ data }) {
        router.push({ path: `/project/registration/${data.id}` });
      },
      getParams () {
        const startDate = moment(vars.formData.startDate).startOf('day').format('YYYY-MM-DD 00:00:00');
        const endDate = moment(vars.formData.endDate).endOf('day').format('YYYY-MM-DD 23:59:59');

        const params = {
            filter: [
                ['contract_date', '>=', startDate],
                'and',
                ['contract_date', '<=', endDate],
            ],
            sort: [{ selector: 'contract_date', desc: true }],
            skip: 0,
            take: 10000,
        };

        if (vars.formData.employee) params.filter.push('and', ['project_manager', '=', vars.formData.employee]);
        if (vars.formData.progress_status) params.filter.push('and', ['progress_status', '=', vars.formData.progress_status]);

        return params;
      },
      async searchDateRange() {
        if (vars.formData.startDate > vars.formData.endDate) {
          await alert('조회 일자가 잘못 되었습니다', '조회');
          return;
        }

        try{
          dataSource.clear();
          vars.grid['status'].beginCustomLoading('데이터를 집계중입니다');
          const params = methods.getParams();

          const { data } = await projectRegistration.load(params);
          
          let i = 1;
          data.forEach((v) =>{
            v.grid_id = i++;
            dataSource.insert(v);
          });
        }catch(ex){
          console.log(ex);
        }finally{
          vars.grid['status'].endCustomLoading();
        }
        vars.grid['status'].refresh();

      },
      loadBaseCode(){
        return baseCodeLoader(['진행단계']).then(response =>{
          vars.dataSource.progress_status = response['진행단계'];
        })
      },
      onExporting (evt) {
        projectRegistration.exportData(evt.component, '프로젝트현황', `프로젝트현황_${Date.now()}.xlsx`)
        evt.cancel = true
      },
      searchReset(){
        vars.formData.employee = null;
        vars.formData.progress_status = null;
      },
    };

    return { vars, methods, dataSource };
  },
};
</script>
<style scoped>
.search-title{
  width: 60px;
}
</style>
