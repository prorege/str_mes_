<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :height="props.height"
    :data-source="produceWorkOrderItem1"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @initialized="onInitialized"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="Work Order Number" data-field="work_order.number" :filter-operations="['contains', '=']" />
    <dx-column caption="Work Order Date" data-field="work_order.target_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
    <dx-column caption="Client Company" data-field="client_company" :visible="false"/>
    <dx-column caption="Order Number" data-field="order_number" :visible="false"/>
    <dx-column caption="Order Date" data-field="order.order_date" :visible="false"/>
    <dx-column caption="Manager" data-field="work_order.manager" />
    <dx-column caption="Item Code" data-field="item_code" />
    <dx-column caption="Item Name" data-field="item.item_name" />
    <dx-column caption="Item Standard" data-field="item.item_standard" />
    <dx-column caption="Required Quantity" data-field="required_quantity" />
    <dx-column caption="Unit Pirce" data-field="unit_price" :format="{ type: 'fixedPoint', precision: 2 }" :visible="false"/>
    <dx-column caption="Unit" data-field="item.unit" />
    <dx-column caption="Supply Pirce" data-field="supply_price" :format="{ type: 'fixedPoint', precision: 2 }" :visible="false"/>
    <dx-column caption="Request Delivery Date" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
    <dx-column caption="Unproduced Quantity" data-field="unproduced_quantity" />
    <dx-column caption="Available Stock" data-field="basic_stock.available_stock" />
    <dx-column caption="Current Stock" data-field="basic_stock.current_stock" />
    <dx-column caption="Main Category" data-field="item.main_category" />
    <dx-column caption="Middle Category" data-field="item.middle_category" :visible="false"/>
    <dx-column caption="Sub Category" data-field="item.sub_category" :visible="false"/>
    <dx-column caption="Asset Type" data-field="item.asset_type" />
    <dx-column caption="Safety Stock" data-field="item.safety_stock" :visible="false"/>
    <dx-column caption="End" data-field="end_yn" data-type="boolean" :visible="false"/>

    <dx-paging :page-size="20" />
    <dx-filter-row :visible="true" />
    <dx-selection :mode="mode" select-all-mode="page" show-check-boxes-mode="always" />
  </dx-data-grid>
</template>

<script setup>
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { produceWorkOrderItem1 } from '../../data-source/produce';
import { ref, watch, defineProps, defineEmits } from 'vue';

const props = defineProps({
  multiple: {
    type: Boolean,
    default: false,
  },
  height: {
    type: [String, Number]
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
