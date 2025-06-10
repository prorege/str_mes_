<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="shipmentQuote"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="영업건명" data-field="business_name" />
    <dx-column caption="견적번호" data-field="quote_number" :sort-index="1" sort-order="desc" />
    <dx-column caption="견적일자" data-field="quote_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
    <dx-column caption="고객업체" data-field="client_company" />
    <dx-column caption="업체담당" data-field="client_manager" />
    <dx-column caption="견적부서" data-field="quote_department" />
    <dx-column caption="견적담당" data-field="quote_manager" />
    <dx-column caption="견적구분" data-field="quote_type" />
    <dx-column caption="이전견적" data-field="previous_quote.quote_number" />
    <dx-column caption="비고" data-field="etc" />
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
import { shipmentQuote } from '../../data-source/shipment';

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
      shipmentQuote,
      onSelectionChanged,
    };
  },
};
</script>
