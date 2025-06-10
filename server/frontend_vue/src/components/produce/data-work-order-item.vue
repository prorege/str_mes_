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
    <dx-column caption="작업지시번호" data-field="work_order.number" :filter-operations="['contains', '=']" />
    <dx-column caption="일자" data-field="work_order.target_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
    <dx-column caption="고객업체" data-field="client_company" />
    <dx-column caption="수주번호" data-field="order_number" />
    <dx-column caption="수주일자" data-field="order.order_date" />
    <dx-column caption="담당자" data-field="work_order.manager" />
    <dx-column caption="품목코드" data-field="item_code" />
    <dx-column caption="품명" data-field="item.item_name" />
    <dx-column caption="규격" data-field="item.item_standard" />
    <dx-column caption="작업지시수량" data-field="required_quantity" />
    <dx-column caption="단가" data-field="unit_price" :format="{ type: 'fixedPoint', precision: 2 }" />
    <dx-column caption="단위" data-field="unit" />
    <dx-column caption="공급가" data-field="supply_price" :format="{ type: 'fixedPoint', precision: 2 }" />
    <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
    <dx-column caption="미입고수량" data-field="unproduced_quantity" />
    <dx-column caption="가용재고" data-field="available_stock" />
    <dx-column caption="현재고" data-field="current_stock" />
    <dx-column caption="품목대분류" data-field="item.main_category" />
    <dx-column caption="품목중분류" data-field="item.middle_category" />
    <dx-column caption="품목소분류" data-field="item.sub_category" />
    <dx-column caption="자산구분" data-field="item.asset_type" />
    <dx-column caption="안전재고" data-field="item.safety_stock" />
    <dx-column caption="종료" data-field="end_yn" data-type="boolean" />

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
