<template>
  <dx-data-grid
    date-serialization-format="yyyy-MM-ddTHH:mm:ss"
    column-resizing-mode="widget"
    :data-source="commInvoice"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="출고번호" data-field="invoice_number" :sort-index="1" sort-order="desc" />
    <dx-column
      caption="Invoice Date"
      data-field="invoice_date"
      data-type="date"
      format="yyyy-MM-dd"
      :sort-index="0"
      sort-order="desc"
    />
    <dx-column
      caption="Ship Date"
      data-field="ship_date"
      data-type="date"
      format="yyyy-MM-dd"
      :sort-index="0"
      sort-order="desc"
    />
    <dx-column
      caption="Sale Date"
      data-field="sale_date"
      data-type="date"
      format="yyyy-MM-dd"
      :sort-index="0"
      sort-order="desc"
    />
    <dx-column caption="Buyer" data-field="client_company" />
    <dx-column caption="Buyer Contact" data-field="client_manager" />
    <dx-column caption="Owner Dept" data-field="invoice_department" />
    <dx-column caption="Member" data-field="invoice_manager" />
    <dx-column caption="Currency" data-field="Currency" />
    <dx-column
      caption="ExRate"
      data-field="exrate"
      data-type="number"
      :format="{ type: 'fixedPoint', precision: 2 }"
    />
    <dx-column caption="부가세구분" data-field="vat_type" />
    <dx-column
      caption="공급가"
      data-field="supply_price"
      data-type="number"
      :format="{ type: 'fixedPoint', precision: 2 }"
    />
    <dx-column
      caption="부가세"
      data-field="vat"
      data-type="number"
      :format="{ type: 'fixedPoint', precision: 2 }"
    />
    <dx-column
      caption="합계금액"
      data-field="total_price"
      data-type="number"
      :format="{ type: 'fixedPoint', precision: 2 }"
    />
    <dx-column caption="비고" data-field="etc" />
    <dx-paging :page-size="20" />
    <dx-selection
      select-all-mode="page"
      show-check-boxes-mode="always"
      :mode="mode"
    />
    <dx-filter-row :visible="true" />
  </dx-data-grid>
</template>

<script>
import {
  DxDataGrid,
  DxColumn,
  DxPaging,
  DxSelection,
  DxFilterRow,
} from 'devextreme-vue/data-grid';
import { commInvoice } from '../../data-source/export';

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
      commInvoice,
      onSelectionChanged,
    };
  },
};
</script>
