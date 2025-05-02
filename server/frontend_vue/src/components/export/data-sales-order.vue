<template>
  <dx-data-grid
    date-serialization-format="yyyy-MM-ddTHH:mm:ss"
    column-resizing-mode="widget"
    :data-source="salesOrder"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="OrderNo" data-field="order_number" :sort-index="1" sort-order="desc" />
    <dx-column
      caption="OrderDate"
      data-field="order_date"
      data-type="date"
      format="yyyy-MM-dd"
      :sort-index="0"
      sort-order="desc"
    />
    <dx-column caption="Buyer" data-field="client_company" />
    <dx-column caption="BuyerContact" data-field="client_manager" />
    <dx-column caption="OwnerDept" data-field="order_department" />
    <dx-column caption="Member" data-field="order_manager" />
    <dx-column caption="PayTerms" data-field="payment_terms" />
    <dx-column caption="PriceTerms" data-field="vat_type" />
    <dx-column caption="Origin" data-field="origin" />
    <dx-column caption="ShipPort" data-field="ship_port" />
    <dx-column caption="Currency" data-field="currency" />
    <dx-column
      caption="ExRate"
      data-field="exrate"
      data-type="number"
      :format="{ type: 'fixedPoint', precision: 2 }"
    />
    <dx-column caption="OrderType" data-field="order_type" />
    <dx-column caption="Remark" data-field="etc" />
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
import { salesOrder } from '../../data-source/export';

export default {
  props: {
    multiple: {
      type: Boolean,
      default: false,
    },
    fixedFilter: {
      type: Object,
    },
  },
  components: { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow },
  setup(props, { emit }) {
    const onSelectionChanged = ({ selectedRowsData }) => {
      if (!props.multiple && selectedRowsData)
        selectedRowsData = selectedRowsData[0];
      emit('change', selectedRowsData);
    };

    if (props.fixedFilter) {
      !(() => (salesOrder.defaultFilters = props.fixedFilter))();
    }

    return {
      mode: props.multiple ? 'multiple' : 'single',
      salesOrder,
      onSelectionChanged,
    };
  },
};
</script>
