<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="shipmentReleaseReturn"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="반품번호" data-field="return_number" :sort-index="1" sort-order="desc" />
    <dx-column caption="반품일자" data-field="return_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
    <dx-column caption="고객업체" data-field="client_company" />
    <dx-column caption="업체담당자" data-field="client_manager" />
    <dx-column caption="반품부서" data-field="return_department" />
    <dx-column caption="반품담당자" data-field="return_manager" />
    <dx-column caption="반품구분" data-field="return_type" />
    <dx-column caption="부가세구분" data-field="vat_type" />
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
import { shipmentReleaseReturn } from '../../data-source/shipment';

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
      shipmentReleaseReturn,
      onSelectionChanged,
    };
  },
};
</script>
