<template>
  <dx-pie-chart type="doughnut"
    class="mes-pie-chart"
    :data-source="series"
    :inner-radius="0.5"
    :palette="[props.color, props.track]"
    :start-angle="90"
    center-template="centerTemplate">
    <dx-series argument-field="arg" value-field="val"></dx-series>
    <dx-legend :visible="false"/>
    <template #centerTemplate>
      <svg>
        <text :style="{fontSize: 70, fill: '#FFFFFF'}"
          text-anchor="middle" x="100" y="120">
          <tspan
            :style="{ fontWeight: 600 }"
            x="100" dy="20px">
            &nbsp;{{ props.value }}
            <tspan :style="{ fontSize: 20 }" dx="-10px">%</tspan>
          </tspan>
        </text>
      </svg>
    </template>
  </dx-pie-chart>
</template>

<script setup>
import DxPieChart, { DxSeries, DxLegend } from 'devextreme-vue/pie-chart'
import {defineProps, computed} from 'vue'

const props = defineProps({
  color: {type: String, default: '#000000'},
  track: {type: String, default: '#FFFFFF'},
  value: {type: Number, default: 0}
})

const series = computed(() => {
  return [
    { arg: 'progress', val: props.value },
    { arg: 'none', val: 100 - props.value}
  ]
})
</script>

<style lang="scss" scoped>
.mes-pie-chart {
  width: 100%;
  height: 100%;
}
</style>