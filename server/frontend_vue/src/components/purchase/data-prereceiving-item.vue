<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="purchasePreReceivingItem"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="가입고번호" data-field="prereceiving.prereceiving_number" :filter-operations="['contains', '=']" :sort-index="1" sort-order="desc" />
    <dx-column caption="가입고일자" data-field="prereceiving.prereceiving_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
    <dx-column caption="공급업체" data-field="prereceiving.client_company" />
    <dx-column caption="입고부서" data-field="prereceiving.receiving_department" />
    <dx-column caption="입고담당자" data-field="prereceiving.receiving_manager" />
    <dx-column caption="입고구분" data-field="prereceiving.receiving_type" />
    <dx-column caption="품목코드" data-field="item_code" />
    <dx-column caption="품명" data-field="item.item_name" />
    <dx-column caption="규격" data-field="item.item_standard" />
    <dx-column caption="발주수량" data-field="order_quantity" data-type="number" format="fixedPoint" />
    <dx-column caption="가입고수량" data-field="prereceiving_quantity" data-type="number" format="fixedPoint" />
    <dx-column caption="단가" data-field="unit_price" :format="{ type: 'fixedPoint', precision: 2 }" />
    <dx-column caption="단위" data-field="item.unit" />
    <dx-column caption="공급가" data-field="supply_price" :format="{ type: 'fixedPoint', precision: 2 }" />
    <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
    <dx-column caption="품목대분류" data-field="item.main_category" />
    <dx-column caption="품목중분류" data-field="item.middle_category" />
    <dx-column caption="품목소분류" data-field="item.sub_category" />
    <dx-column caption="발주번호" data-field="order_number" />
    <dx-column caption="공급사품번" data-field="client_item_number" />
    <dx-column caption="품목설명" data-field="item.item_detail" />
    <dx-column caption="LOT번호" data-field="lot_number" />
    <dx-column caption="검사완료" data-field="check_yn" />

    <dx-paging :page-size="20" />
    <dx-sorting mode="multiple" />
    <dx-filter-row :visible="true" />
    <dx-selection :mode="mode" select-all-mode="page" show-check-boxes-mode="always" />
  </dx-data-grid>
</template>

<script setup>
import { DxDataGrid, DxColumn, DxPaging, DxSorting, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { purchasePreReceivingItem } from '../../data-source/purchase';
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
  !(() => (purchasePreReceivingItem.defaultFilters = props.fixedFilter))();
}

function onSelectionChanged({ selectedRowsData }) {
  if (!props.multiple && selectedRowsData)
    selectedRowsData = selectedRowsData[0];
  emit('change', selectedRowsData);
}
</script>
