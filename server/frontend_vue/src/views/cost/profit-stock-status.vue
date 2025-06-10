<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">품목별매출이익현황</div>
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
          <dx-column caption="품목분류" data-field="main_category" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item_name" />
          <dx-column caption="규격" data-field="item_standard" />
          <dx-column caption="매출수량" data-field="total_quantity" data-type="number" format="fixedPoint"/>
          <dx-column caption="매출원가" data-field="cost_price" :calculate-display-value="calcTotalCostPrice" data-type="number" :format="{ type: 'fixedPoint', precision: 0 }"/>
          <dx-column caption="매출액" data-field="total_price" data-type="number" :format="{ type: 'fixedPoint', precision: 0 }" />
          <dx-column caption="매출이익" data-field="" :calculate-display-value="calcTotalProfitMargin" data-type="number" :format="{ type: 'fixedPoint', precision: 0 }" />
          <dx-column caption="이익율" data-field="" :calculate-display-value="calcProfitMarginRate" />
        
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
  stateStore.bind(`profit-stock-status-${key}`, evt.component);

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

function calcTotalCostPrice(rowData){
  let totalCostPirce = 0;
  if (rowData.cost_price != null && rowData.total_quantity != null){
    totalCostPirce = rowData.cost_price * rowData.total_quantity;
  }
  return totalCostPirce;
}

function calcTotalProfitMargin(rowData){
  let totalProfitMargin = 0;
  if (rowData.total_price != null && rowData.cost_price != null && rowData.total_quantity != null){
    let total_price = rowData.total_price
    let total_cost_price = rowData.cost_price * rowData.total_quantity
    totalProfitMargin = total_price - total_cost_price
  }
  return totalProfitMargin
}

function calcProfitMarginRate(rowData){
  let totalProfitMargin = 0
  if (rowData.total_price != null &&  rowData.cost_price != null && rowData.total_quantity != null){
    if(Number(rowData.total_quantity) > 0 && Number(rowData.total_price) === 0){
       totalProfitMargin = -1
    }else{
      let total_price = rowData.total_price
      let total_cost_price = rowData.cost_price * rowData.total_quantity
      totalProfitMargin = (total_price - total_cost_price) / total_price
    }
    
  }
  return totalProfitMargin === 0 || totalProfitMargin === -Infinity ? `0%` : `${Math.floor(totalProfitMargin * 10000) / 100 }%`;
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
  const api = new ApiService('/api/mes/v1/cost/profit-stock-status')
  const {data} = await api.get('', {params});
  console.log("data : ", data)
  vars.grid['status'].endCustomLoading()
  dataSource.value = data.objects

}

async function onExporting(evt) {
  shipmentReleaseItem.exportData(evt.component, '품목별매출이익현황', `품목별매출이익현황${Date.now()}.xlsx`);
  evt.cancel = true;
}
</script>