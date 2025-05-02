<script setup>
import {
  DxDataGrid,
  DxColumn,
  DxEditing,
  DxPaging
} from 'devextreme-vue/data-grid';
import DxButton from 'devextreme-vue/button';
import { DxSelectBox } from 'devextreme-vue/select-box'
import { setupProduceCost } from '@/data-source/setup'
import { ref, watch } from 'vue'

const currentYear = new Date().getFullYear()
const selectedYear = ref(String(currentYear))
const yearOptions = [String(currentYear - 2), String(currentYear - 1), String(currentYear)]
let grid = undefined

setupProduceCost.defaultFilters = [{name: 'year', op: 'eq', val: selectedYear.value}]

watch(
  selectedYear,
  () => {
    setupProduceCost.defaultFilters = [{name: 'year', op: 'eq', val: selectedYear.value}]
    grid.getDataSource().reload()
  }
)

function initialized (component) {
  grid = component
}
</script>

<template>
<div>
  <div class="search-status">
    <dx-select-box v-model="selectedYear" :items="yearOptions" />
  </div>
</div>
<dx-data-grid
  :data-source="setupProduceCost"
  :column-auto-width="true"
  :allow-column-reordering="true"
  :show-borders="true"
  :show-row-lines="true"
  @initialized="(evt) => initialized(evt.component)">
  <dx-paging :enabled="true" :page-size="1000" />
  <dx-column
    data-field="name"
    caption="제조구분"
    :allow-editing="true"
  />
  <dx-column
    data-field="subfix"
    caption="구분"
    :allow-editing="true"
  />
  <dx-column
    data-field="labor_cost"
    data-type="number"
    caption="노무비단가(원)"
    :allow-editing="true"
  />
  <dx-column
    data-field="produce_cost_rate"
    data-type="number"
    caption="제조경비(%)"
    :allow-editing="true"
  />
  <dx-column
    data-field="operating_cost_rate"
    data-type="number"
    caption="판관비(%)"
    :allow-editing="true"
  />
  <dx-editing
    mode="row"
    :allow-adding="false"
    :allow-updating="true"
    :allow-deleting="false"
    :use-icons="true"
  />
</dx-data-grid>
</template>

<style lang="scss" scoped>
.search-status {
  padding: 2px 10px 12px;
}
</style>