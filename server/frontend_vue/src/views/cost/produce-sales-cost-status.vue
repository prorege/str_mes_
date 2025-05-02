<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">생산매출원가분석현황</div>
            </dx-item>
          </dx-toolbar>
        </div>
        <div>
          <div class="search-status">
            <span class="search-title">조회일자</span>
            <dx-date-box v-model:value="vars.formData.startDate" />
            <span class="search-bar">~</span>
            <dx-date-box v-model:value="vars.formData.endDate" />
            <span class="search-tab"></span>
            <SearchButtonGroup @change="({startDate, endDate}) => { vars.formData.startDate = startDate; vars.formData.endDate = endDate; }" />
            <span class="search-tab"></span>
            <span class="search-tab"></span>
            <dx-button text="검색" icon="search" @click="searchDateRange()" />
          </div>
        </div>
      </div>
      <div class="dx-card responsive-paddings mt-1">
        <dx-data-grid
          height="calc(100vh - 230px)"
          date-serialization-format="yyyy-MM-ddTHH:mm:ss"
          key-expr="id"
          column-resizing-mode="widget"
          :on-initialized="evt => onGridInitialized(evt, 'status')"
          :data-source="dataSource"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-reordering="true"
          :allow-column-resizing="true"
          :row-alternation-enabled="true"
          :focused-row-enabled="true"
          @exporting="onExporting"
        >
        <dx-column caption="매출년월" data-field="date" data-type="date" format="yyyy.MM" />
        <dx-column caption="품목분류" data-field="main_category" />
        <dx-column caption="품목코드" data-field="item_code" />
        <dx-column caption="품명" data-field="item_name" />
        <dx-column caption="판매수량" data-field="total_quantity" data-type="number" format="fixedPoint"/>
        <dx-column caption="판매단가" data-field="sales_price" data-type="number" :format="{ type: 'fixedPoint', precision: 0 }" />
        <dx-column caption="매출액" data-field="total_price" data-type="number" :format="{ type: 'fixedPoint', precision: 0 }" />
        <dx-column caption="공수(분)" data-field="ct" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
        <dx-column caption="노무비" data-field="labor_cost" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :calculate-display-value="calcLaborCost" />
        <dx-column caption="마감자재비" data-field="part_cost" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
      
        <dx-export :enabled="true" />
        <dx-paging :page-size="20" />
        <dx-sorting mode="single" />
        <dx-filter-row :visible="true" />
        <dx-column-chooser mode="select" :enabled="true" />
        </dx-data-grid>
      </div>
    </div>
  </div>
</template>
<script setup>
import moment from 'moment';
import {ref} from 'vue'
import {groupBy} from 'lodash'
import { useRouter } from 'vue-router';
import { reactive } from 'vue';

import { alert } from 'devextreme/ui/dialog';
import DxButton from 'devextreme-vue/button';
import DxCheckBox from 'devextreme-vue/check-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxExport, DxPaging, DxSorting, DxFilterRow, DxColumnChooser } from 'devextreme-vue/data-grid';

import stateStore from '@/utils/state-store';
import { shipmentReleaseItem } from '../../data-source/shipment';
import { baseBom, baseBomLink } from '@/data-source/base'
import SearchButtonGroup from '../../components/search-button-group.vue';
import { baseItem } from '../../data-source/base';
import ApiService from '../../utils/api-service';

const router = useRouter();
const vars = {};
vars.grid = {};
vars.formData = reactive({
startDate: new Date(),
endDate: new Date(),
});
// vars.formData.startDate.setDate(vars.formData.startDate.getDate() - 7);
const dataSource = ref([])
function onGridInitialized(evt, key) {
  vars.grid[key] = evt.component;
  stateStore.bind(`produce-sales-cost-status-${key}`, evt.component);

  // methods.initSorting();
  // searchDateRange();
}
function initSorting() {
  const columns = vars.grid['status'].getVisibleColumns();
  const col = columns.filter(item => item.sortOrder);
  if (col.length == 0) {
    const defaultName = 'release.release_date';
    const defaultSort = columns.filter(item => item.name == defaultName);
    if (defaultSort.length > 0) {
      vars.grid['status'].columnOption(defaultSort[0].index, 'sortOrder', 'desc');
    }
  }
}

async function searchDateRange() {
  if (vars.formData.startDate > vars.formData.endDate) {
    await alert('조회 일자가 잘못 되었습니다', '조회');
    return;
  }
  vars.grid['status'].beginCustomLoading('데이터를 집계중입니다')
  const params = {
    start: moment(vars.formData.startDate).startOf('day').format('YYYY-MM-DD HH:mm:ss'),
    end: moment(vars.formData.endDate).endOf('day').format('YYYY-MM-DD HH:mm:ss')
  }
  const api = new ApiService('/api/mes/v1/cost/produce-sales-cost-status')

  const {data} = await api.get('', {params});

  vars.grid['status'].endCustomLoading()
  dataSource.value = data.objects;
}

function calcLaborCost(rowData){
  let calcLaborCost = 0;
  if(rowData.total_quantity != null && rowData.labor_cost != null){
    calcLaborCost = rowData.total_quantity * rowData.labor_cost;
  }
  return calcLaborCost;
}

async function onExporting(evt) {
  shipmentReleaseItem.exportData(evt.component, '생산매출원가분석현황', `생산매출원가분석현황${Date.now()}.xlsx`);
  evt.cancel = true;
}
</script>