<script setup>
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar'
import { DxLoadPanel } from 'devextreme-vue/load-panel'
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxButtonItem } from 'devextreme-vue/form'
import {
  DxChart,
  DxSeries,
  DxCommonSeriesSettings,
  DxLabel as DxChartLabel,
  DxLegend,
} from 'devextreme-vue/chart'
import { shipmentReleaseItem } from '@/data-source/shipment'
import { performanceItem1 } from '@/data-source/produce'
import { purchaseReceivingItem } from '@/data-source/purchase'
import authService from '@/auth'
import { ref } from 'vue'
import { chain } from 'lodash'
import moment from 'moment'

const ds = {}, loading = ref(false)
ds.series1 = ref([])
ds.series2 = ref([])
ds.series3 = ref([])
ds.series4 = ref([])
ds.series5 = ref([])

const search = ref({
  start: moment().startOf('month').toDate(), 
  end: moment().toDate()
})

async function submit () {
  loading.value = true

  shipmentReleaseItem.defaultFilters = [
    {name: 'release', op: 'has', val: {name: 'fk_company_id', op: 'eq', val: authService.getCompanyId()}},
    {name: 'release', op: 'has', val: {name: 'release_date', op: 'gte', val: moment(search.value.start).format('YYYY-MM-DD 00:00:00')}},
    {name: 'release', op: 'has', val: {name: 'release_date', op: 'lte', val: moment(search.value.end).format('YYYY-MM-DD 23:59:59')}},
  ]
  const {data: shipData, totalCount: shipTotal} = await shipmentReleaseItem.load()
  if (shipTotal) {
    ds.series1.value = chain(shipData)
      .groupBy(item => item.fk_project_management_id || '지정안됨')
      .transform((result, value, key) => {
        result.push({ key, value: value.reduce((r, item) => r + item.supply_price, 0) })
      }, [])
      .value()
  }

  purchaseReceivingItem.defaultFilters = [
    {name: 'receiving', op: 'has', val: {name: 'fk_company_id', op: 'eq', val: authService.getCompanyId()}},
    {name: 'receiving', op: 'has', val: {name: 'receiving_date', op: 'gte', val: moment(search.value.start).format('YYYY-MM-DD 00:00:00')}},
    {name: 'receiving', op: 'has', val: {name: 'receiving_date', op: 'lte', val: moment(search.value.end).format('YYYY-MM-DD 23:59:59')}},
  ]
  const {data: recvData, totalCount: recvTotal} = await purchaseReceivingItem.load()
  if (recvTotal) {
    ds.series2.value = chain(recvData)
      .groupBy(item => item.fk_project_management_id || '지정안됨')
      .transform((result, value, key) => {
        result.push({ key, value: value.reduce((r, item) => r + item.supply_price, 0) })
      }, [])
      .value()
  }

  performanceItem1.defaultFilters = [
    {name: 'performance_registration', op: 'has', val: {name: 'fk_company_id', op: 'eq', val: authService.getCompanyId()}},
    {name: 'performance_registration', op: 'has', val: {name: 'target_date', op: 'gte', val: moment(search.value.start).format('YYYY-MM-DD 00:00:00')}},
    {name: 'performance_registration', op: 'has', val: {name: 'target_date', op: 'lte', val: moment(search.value.end).format('YYYY-MM-DD 23:59:59')}},
  ]
  const {data: prodData, totalCount: prodTotal} = await performanceItem1.load()
  if (prodTotal) {
    ds.series3.value = chain(prodData)
      .groupBy(item => item.fk_project_management_id || '지정안됨')
      .transform((result, value, key) => {
        result.push({ key, value: value.reduce((r, item) => r + item.production_receiving_quantity, 0) })
      }, [])
      .value()
  }

  loading.value = false
}
</script>

<template>
  <div class="content-block">
    <dx-load-panel v-model:visible="loading" :show-pane="true" />
    <div class="dx-card responsive-paddings">
      <div class="content-header">
        <dx-toolbar>
          <dx-item location="before">
            <div class="content-title">프로젝트실적</div>
          </dx-item>
        </dx-toolbar>
      </div>

      <dx-form
        label-mode="static"
        :form-data="search">
        <dx-group-item :col-count="4">
          <dx-simple-item 
            data-field="start"
            editor-type="dxDateBox"
            :editor-options="{displayFormat: 'yyyy-MM-dd'}">
            <dx-chart-label text="검색연도" />
          </dx-simple-item>
          <dx-simple-item 
            data-field="end"
            editor-type="dxDateBox"
            :editor-options="{displayFormat: 'yyyy-MM-dd'}">
            <dx-chart-label text="검색월" />
          </dx-simple-item>
          <dx-button-item
            :button-options="{
              text: '검색',
              type: 'success',
              useSubmitBehavior: true,
              onClick: submit
            }"
            horizontal-alignment="left"
          />
        </dx-group-item>
      </dx-form>
    </div>

    <div class="graph-container dx-card responsive-paddings">
      <div class="graph-item">
        <label>매출실적</label>
        <dx-chart :data-source="ds.series1.value" class="graph-wrap">
          <dx-common-series-settings type="bar" :bar-width="12" argument-field="key" :show-in-legend="false">
            <dx-label :visible="true" />
          </dx-common-series-settings>
          <dx-series value-field="value" />
          <dx-legend vertical-alignment="bottom" horizontal-alignment="center" />
        </dx-chart>
      </div>
      <div class="graph-item">
        <label>구매실적</label>
        <dx-chart :data-source="ds.series2.value" class="graph-wrap">
          <dx-common-series-settings type="bar" :bar-width="12" argument-field="key" :show-in-legend="false">
            <dx-label :visible="true" />
          </dx-common-series-settings>
          <dx-series value-field="value" />
          <dx-legend vertical-alignment="bottom" horizontal-alignment="center" />
        </dx-chart>
      </div>
      <div class="graph-item">
        <label>생산실적</label>
        <dx-chart :data-source="ds.series3.value" class="graph-wrap">
          <dx-common-series-settings type="bar" :bar-width="12" argument-field="key" :show-in-legend="false">
            <dx-label :visible="true" />
          </dx-common-series-settings>
          <dx-series value-field="value" />
          <dx-legend vertical-alignment="bottom" horizontal-alignment="center" />
        </dx-chart>
      </div>
    </div>
      
  </div>
</template>

<style lang="scss" scoped>
.graph-container {
  height: calc(100vh - 195px);
  display: flex;
  flex-direction: column;

  margin-top: 10px;
  overflow: auto;
}
.graph-item:not(:first-child) {
  margin-top: 30px;
}
// .graph-wrap {}
</style>