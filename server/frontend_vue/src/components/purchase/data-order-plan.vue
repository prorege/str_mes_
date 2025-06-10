<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="purchaseOrderPlan"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="발주계획번호" data-field="order_plan_number" :sort-index="0" sort-order="desc" />
    <dx-column caption="발주계획일자" data-field="order_plan_date" data-type="date" format="yyyy-MM-dd" :sort-index="1" sort-order="desc" />
    <dx-column caption="발주계획부서" data-field="order_plan_department" />
    <dx-column caption="발주계획담당자" data-field="order_plan_manager" />
    <dx-column caption="발주구분" data-field="order_type" />
    <dx-column caption="참고사항" data-field="note" />
    <dx-column caption="비고" data-field="etc" />
    <dx-column caption="공급가" data-field="supply_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
    <dx-column caption="부가세" data-field="vat" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
    <dx-column caption="합계금액" data-field="total_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />

    <dx-paging :page-size="20" />
    <dx-filter-row :visible="true" />
    <dx-selection :mode="mode" select-all-mode="page" show-check-boxes-mode="always" />
  </dx-data-grid>
</template>

<script>
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { purchaseOrderPlan } from '../../data-source/purchase';

export default {
  props: {
    multiple: {
      type: Boolean,
      default: false,
    },
  },
  components: { DxDataGrid, DxColumn, DxSelection, DxPaging, DxFilterRow },
  setup(props, { emit }) {
    const onSelectionChanged = ({ selectedRowsData }) => {
      if (!props.multiple && selectedRowsData)
        selectedRowsData = selectedRowsData[0];
      emit('change', selectedRowsData);
    };

    return {
      mode: props.multiple ? 'multiple' : 'single',
      purchaseOrderPlan,
      onSelectionChanged,
    };
  },
};
</script>
