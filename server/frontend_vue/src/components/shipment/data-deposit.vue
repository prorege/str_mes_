<template>
  <dx-data-grid
     column-resizing-mode="widget"
    :data-source="shipmentDeposit"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="입금번호" data-field="deposit_number" :sort-index="1" sort-order="desc" />
    <dx-column caption="입금일자" data-field="deposit_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc"  />
    <dx-column caption="고객업체" data-field="client_company" />
    <dx-column caption="영업부서" data-field="deposit_department" />
    <dx-column caption="영업담당자" data-field="deposit_manager" />
    <dx-column caption="비고" data-field="etc" />

    <dx-paging :page-size="20" />
    <dx-filter-row :visible="true" />
    <dx-selection :mode="mode" select-all-mode="page" show-check-boxes-mode="always" />
  </dx-data-grid>
</template>

<script>
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { shipmentDeposit } from '../../data-source/shipment';

export default {
  props: {
    multiple: {
      type: Boolean,
      default: false,
    },
  },
  components: { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow },
  setup(props, { emit }) {
    const onSelectionChanged = ({ selectedRowsData }) => {
      if (!props.multiple && selectedRowsData)
        selectedRowsData = selectedRowsData[0];
      emit('change', selectedRowsData);
    };

    return {
      mode: props.multiple ? 'multiple' : 'single',
      shipmentDeposit,
      onSelectionChanged,
    };
  },
};
</script>
