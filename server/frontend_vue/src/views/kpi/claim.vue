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
  DxValueAxis
} from 'devextreme-vue/chart'
import { alert } from 'devextreme/ui/dialog'
import { ref } from 'vue'
import { chain } from 'lodash'
import moment from 'moment'

const ds = {}, loading = ref(false)
ds.series1 = ref([])
ds.visible = ref(false);

const search = ref({
  start: new Date(2024, 0, 1),
  end: moment().toDate()
})

async function submit () {
  loading.value = true
  const chartData = [
    {'key' : '1월', 'value' : 14},
    {'key' : '2월', 'value' : 12},
    {'key' : '3월', 'value' : 15},
    {'key' : '4월', 'value' : 11},
    {'key' : '5월', 'value' : 13},
  ]
  if (chartData) {
    ds.series1.value = chartData;
    ds.visible.value = true;
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
            <div class="content-title">Claim 건 수</div>
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
            :editor-options="{
              displayFormat: 'yyyy-MM-dd',
              min: new Date(2024,0,1)
            }">
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
        <label>Claim 건 수</label>
        <dx-chart :data-source="ds.series1.value" class="graph-wrap" >
          <dx-common-series-settings type="bar" :bar-width="40" argument-field="key" :show-in-legend="false">
            <dx-label :visible="true" />
          </dx-common-series-settings>
          <dx-series value-field="value" />
          <dx-legend vertical-alignment="bottom" horizontal-alignment="center" />
          <dx-value-axis :max-value-margin="0.01"/>
        </dx-chart>
        <label>월별</label>
        <div class="avg_box" v-if="ds.visible.value">평균 13건</div>
      </div>
    </div>
      
  </div>
</template>

<style lang="scss" scoped>
.graph-container {
  height: calc(100vh - 195px);
  width: calc(100vw - 250px);
  margin-top: 10px;
  overflow: auto;
}
.graph-item:not(:first-child) {
  // margin-top: 30px;
}
.graph-item{
  height: 95%;
}
.graph-wrap {
  height: 95%;
}
.avg_box{
  text-align: center; 
  font-size: 20px;
}
</style>