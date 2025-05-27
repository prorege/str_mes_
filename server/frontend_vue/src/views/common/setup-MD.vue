<script setup>
import {
  DxDataGrid,
  DxColumn,
  DxEditing,
  DxPaging
} from 'devextreme-vue/data-grid';
import DxButton from 'devextreme-vue/button';
import { DxSelectBox } from 'devextreme-vue/select-box'
import { setupMD } from '@/data-source/setup'
import { ref, watch } from 'vue'

let grid = undefined

function initialized (component) {
  grid = component
}
</script>

<template>
  
<dx-data-grid
  :data-source="setupMD"
  :column-auto-width="true"
  :allow-column-reordering="true"
  :show-borders="true"
  :show-row-lines="true"
  @initialized="(evt) => initialized(evt.component)">
  <dx-paging :enabled="true" :page-size="1000" />
  <dx-column
    data-field="name"
    caption="비용명"
    :allow-editing="true"
  />
  <dx-column
    data-field="md"
    caption="M/D"
    data-type="number"
    :allow-editing="true"
    alignment="left"
  />
  <dx-search-panel :visible="false" :width="240" placeholder="검색" />
  <dx-editing
    mode="batch"
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