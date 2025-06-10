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
import { alert } from 'devextreme/ui/dialog'
import {performanceItem1} from '@/data-source/produce'
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

  performanceItem1.defaultFilters = [
    {name: 'performance_registration', op: 'has', val: {name: 'fk_company_id', op: 'eq', val: authService.getCompanyId()}},
    {name: 'performance_registration', op: 'has', val: {name: 'target_date', op: 'gte', val: moment(search.value.start).format('YYYY-MM-DD 00:00:00')}},
    {name: 'performance_registration', op: 'has', val: {name: 'target_date', op: 'lte', val: moment(search.value.end).format('YYYY-MM-DD 23:59:59')}},
  ]

  const {data, totalCount} = await performanceItem1.load()
  if (totalCount) {
    console.log(data)
    ds.series1.value = chain(data)
      .groupBy(item => item.client_company || '없음')
      .transform((result, value, key) => {
        result.push({ key, value: value.reduce((r, item) => r + item.production_receiving_quantity, 0) })
      }, [])
      .value()

    ds.series2.value = chain(data)
      .groupBy(item => item.performance_registration.department)
      .transform((result, value, key) => {
        result.push({ key, value: value.reduce((r, item) => r + item.production_receiving_quantity, 0) })
      }, [])
      .value()

    ds.series3.value = chain(data)
      .groupBy(item => item.item.item_name)
      .transform((result, value, key) => {
        result.push({ key, value: value.reduce((r, item) => r + item.production_receiving_quantity, 0) })
      }, [])
      .value()
  }
  else {
    await alert('검색 결과가 없습니다', '조회결과')
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
            <div class="content-title">생산실적</div>
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
        <label>업체별</label>
        <dx-chart :data-source="ds.series1.value" class="graph-wrap">
          <dx-common-series-settings type="bar" :bar-width="12" argument-field="key" :show-in-legend="false">
            <dx-label :visible="true" />
          </dx-common-series-settings>
          <dx-series value-field="value" />
          <dx-legend vertical-alignment="bottom" horizontal-alignment="center" />
        </dx-chart>
      </div>
      <div class="graph-item">
        <label>부서별</label>
        <dx-chart :data-source="ds.series2.value" class="graph-wrap">
          <dx-common-series-settings type="bar" :bar-width="12" argument-field="key" :show-in-legend="false">
            <dx-label :visible="true" />
          </dx-common-series-settings>
          <dx-series value-field="value" />
          <dx-legend vertical-alignment="bottom" horizontal-alignment="center" />
        </dx-chart>
      </div>
      <div class="graph-item">
        <label>품목별</label>
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