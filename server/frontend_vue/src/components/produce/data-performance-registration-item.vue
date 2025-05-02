<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="performanceItem1"
    :show-borders="true"
    :remote-operations="true"
    :column-auto-width="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="생산입고번호" data-field="performance_registration.number" :sort-index="1" sort-order="desc" />
    <dx-column caption="작업지시번호" data-field="work_order.number" />
    <dx-column caption="품목코드" data-field="item_code" />
    <dx-column caption="품명" data-field="item.item_name" />
    <dx-column caption="규격" data-field="item.item_standard" />
    <dx-column caption="작지수량" data-field="work_order_item.required_quantity" data-type="number" format="fixedPoint" />
    <dx-column caption="검수수량" data-field="work_order_item.check_quantity" data-type="number" format="fixedPoint" :calculate-display-value="checkQuantity" />
    <dx-column caption="생산입고수량" data-field="production_receiving_quantity" data-type="number" format="fixedPoint" />
    <dx-column caption="단위" data-field="item.unit" />
    <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
    <dx-column caption="미생산수량" data-field="unproduced_quantity" data-type="number" format="fixedPoint" />
    <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" />
    <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" />
    <dx-column caption="수주번호" data-field="order_number" />
    <dx-column caption="고객업체" data-field="client_company" />
    <dx-column caption="고객사품번" data-field="client_item_number" />
    <dx-column caption="실수요자" data-field="end_user" />
    <dx-column caption="입고창고" data-field="warehouse.wh_name" />
    <dx-column caption="생산입고 아이디" data-field="fk_performance_registration_id" :visible="false" />
    <dx-column caption="작업지시품목 아이디" data-field="fk_work_order_item" :visible="false" />
    <dx-column caption="창고코드" data-field="warehouse_code" :visible="false" />
    <dx-column caption="일자" data-field="work_order.target_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />

    <dx-paging :page-size="20" />
    <dx-sorting mode="multiple" />
    <dx-filter-row :visible="true" />
    <dx-selection :mode="mode" select-all-mode="page" show-check-boxes-mode="always" />
  </dx-data-grid>
</template>

<script setup>
import {DxDataGrid, DxColumn, DxPaging, DxSorting, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { performanceItem1 } from '../../data-source/produce';
import { ref, defineProps, defineEmits } from 'vue';

const props = defineProps({
  multiple: {
    type: Boolean,
    default: false,
  },
  fixedFilter: {
    type: Object,
  },
});
const emit = defineEmits(['change']);
const mode = ref(props.multiple ? 'multiple' : 'single');
if (props.fixedFilter) {
  !(() => (performanceItem1.defaultFilters = props.fixedFilter))();
}

function onSelectionChanged({ selectedRowsData }) {
  if (!props.multiple && selectedRowsData)
    selectedRowsData = selectedRowsData[0];
  emit('change', selectedRowsData);
}

function checkQuantity(rowData) {
  if (!rowData.check_quantity) { return '0'; }
  return rowData.check_quantity;
}
</script>
