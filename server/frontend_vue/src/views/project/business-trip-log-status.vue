<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before"
              ><div class="content-title">외근-출장관리현황</div></dx-item
            >
          </dx-toolbar>
        </div>
        <div class="search-status search-line">
          <span class="search-title">등록일자</span>
          <dx-date-box v-model:value="vars.formData.startDate" />
          
          <span class="search-bar">~</span>
          <dx-date-box v-model:value="vars.formData.endDate" />
          
          <span class="search-tab"></span>
          <SearchButtonGroup @change="({startDate, endDate}) => { vars.formData.startDate = startDate; vars.formData.endDate = endDate; }" />
          
        </div>

        <div class="search-status">
          <span class="search-title">담당자</span>
          <dx-lookup 
            value-expr="emp_name"
            display-expr="emp_name"
            v-model:value="vars.formData.employee"
            :data-source="vars.dataSource.employee"
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
          :on-initialized="evt => methods.onGridInitialized(evt, 'trip-log-status')"
          @exporting="methods.onExporting"
        >
          <dx-column caption="담당자" data-field="manager" />
          <dx-column caption="등록일자" data-field="created" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="구분" data-field="trip_type" />
          <dx-column caption="시작날짜" data-field="trip_start_date" data-type="datetime" format="yyyy-MM-dd HH:mm" />
          <dx-column caption="종료날짜" data-field="trip_end_date" data-type="datetime" format="yyyy-MM-dd HH:mm" />
          <dx-column caption="프로젝트명" data-field="project_name"  />
          <dx-column caption="당사담당자" data-field="note" />
          <dx-column caption="업무 내용" data-field="business_progress" />
          <dx-column caption="경유지" data-field="stopover" />
          <dx-column caption="운행차량" data-field="vehicle" />
         
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
import { projectBusinessTripLog } from '../../data-source/project';
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
    });
    vars.dataSource = reactive({
      employee: null,
    })
    const dataSource = new ArrayStore({ key: 'grid_id', data: [] })
    // vars.formData.startDate.setDate(vars.formData.startDate.getDate() - 7);
    onMounted(async () => {
      await loadEmployee(vars.dataSource);
    })
    const methods = {
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`project-business-${key}`, evt.component);


        // methods.searchDateRange();
      },

      getParams () {
        const startDate = moment(vars.formData.startDate).startOf('day').format('YYYY-MM-DD 00:00:00');
        const endDate = moment(vars.formData.endDate).endOf('day').format('YYYY-MM-DD 23:59:59');

        const params = {
            filter: [
                ['trip_start_date', '>=', startDate],
                'and',
                ['trip_end_date', '<=', endDate],
            ],
            sort: [{ selector: 'created', desc: true }],
            skip: 0,
            take: 10000,
        };

        if (vars.formData.employee) params.filter.push('and', ['manager', '=', vars.formData.employee]);

        return params;
      },

      async searchDateRange() {
        if (vars.formData.startDate > vars.formData.endDate) {
          await alert('조회 일자가 잘못 되었습니다', '조회');
          return;
        }

        try{
          dataSource.clear()
          vars.grid['trip-log-status'].beginCustomLoading('데이터를 집계중입니다')
          const params = methods.getParams(); 

          const { data } = await projectBusinessTripLog.load(params);
          let i = 1;
          data.forEach((v) => {
            v.grid_id = i++
            dataSource.insert(v);
          });
        }catch(ex){
          console.error(ex)
        }finally{
          vars.grid['trip-log-status'].endCustomLoading()
        }
        vars.grid['trip-log-status'].refresh() 
      },
      onExporting(evt) {
        projectBusinessTripLog.exportData(evt.component, '외근-출장관리현황', `외근-출장관리현황_${Date.now()}.xlsx`);
        evt.cancel = true;
      },
      searchReset(){
        vars.formData.employee = null;
      }
    };

    return { vars, methods, dataSource };
  },
};
</script>
<style scoped>
.search-title{
  width: 70px;
}
</style>