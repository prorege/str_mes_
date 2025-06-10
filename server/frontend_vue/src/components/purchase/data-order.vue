<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="purchaseOrder"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="발주번호" data-field="order_number" :sort-index="1" sort-order="desc" />
    <dx-column caption="발주일자" data-field="order_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
    <dx-column caption="고객업체" data-field="client_company" />
    <dx-column caption="업체담당자" data-field="client_manager" />
    <dx-column caption="발주부서" data-field="order_department" />
    <dx-column caption="발주담당자" data-field="order_manager" />
    <dx-column caption="납품기한" data-field="delivery_date" data-type="date" format="yyyy-MM-dd" />
    <!-- <dx-column caption="프로젝트번호" data-field="project_management.project_number" /> -->
    <dx-column caption="프로젝트명" data-field="project_management.project_name" />
    <dx-column caption="EndUser" data-field="end_user" />
    <dx-column caption="참고사항" data-field="note" />
    <dx-column caption="공급가" data-field="supply_price" data-type="number" format="currency" />
    <dx-column caption="부가세" data-field="vat" data-type="number" format="currency" />
    <dx-column caption="합계금액" data-field="total_price" data-type="number" format="currency" />

    <dx-paging :page-size="20" />
    <dx-filter-row :visible="true" />
    <dx-selection :mode="mode" select-all-mode="page" show-check-boxes-mode="always" />
  </dx-data-grid>
</template>

<script>
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { purchaseOrder } from '../../data-source/purchase';

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
      purchaseOrder,
      onSelectionChanged,
    };
  },
};
</script>
