<template>
  <dx-data-grid
    height="340px"
    column-resizing-mode="widget"
    :data-source="processPerformanceRegistration"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @initialized="onInitialized"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="Performance Number" data-field="number" />
    <dx-column caption="생성시간" data-field="created" width="0px" />
    <dx-column caption="Production Process" data-field="process.process_name" />
    <dx-column caption="Work Order Number" data-field="order_number" />
    <dx-column caption="Completed Quantity" data-field="process_quantity" />
    <dx-column caption="Item Code" data-field="item_code" />
    <dx-column caption="Item Name" data-field="item.item_name" />
    <dx-column caption="Required Quantity" data-field="work_order_item.required_quantity" data-type="number" />

    <dx-paging :page-size="20" />
    <dx-filter-row :visible="true" />
    <dx-selection :mode="mode" select-all-mode="page" show-check-boxes-mode="always" />
  </dx-data-grid>
</template>

<script setup>
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { processPerformanceRegistration } from '../../data-source/produce';
import { ref, watch, defineProps, defineEmits } from 'vue';

const props = defineProps({
  multiple: {
    type: Boolean,
    default: false,
  },
  filters: {
    type: Object
  }
});
const emit = defineEmits(['change']);
const mode = ref(props.multiple ? 'multiple' : 'single');
let component = undefined

function onInitialized (e) {
  component = e.component
  setFilter()
}

function setFilter () {
  if (!component) return
  const columns = component.getVisibleColumns();
  const defaultSort = columns.filter((item) => item.name == 'created');
  if (defaultSort.length > 0) {
    component.columnOption(defaultSort[0].index, 'sortOrder', 'desc');
  }
  if (!props.filters || !props.filters.length) {
    component.clearFilter()
    return
  }
  component.filter(props.filters)
}

function onSelectionChanged({ selectedRowsData }) {
  if (!props.multiple && selectedRowsData)
    selectedRowsData = selectedRowsData[0];
  emit('change', selectedRowsData);
}

watch(
  () => props.filters,
  () => setFilter()
);
</script>
