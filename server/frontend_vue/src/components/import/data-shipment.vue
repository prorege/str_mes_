<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="importShipment"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="Offder No" data-field="shipment_number" :sort-index="1" sort-order="desc" />
    <dx-column caption="Issue Date" data-field="shipment_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
    <dx-column caption="P/O No" data-field="purchase_order.order_number" />
    <dx-column caption="Supplier" data-field="supplier" />
    <dx-column caption="Buyer" data-field="buyer" />
    <dx-column caption="Validity" data-field="validity" />
    <dx-column caption="Pay Terms" data-field="pay_terms" />
    <dx-column caption="Destination" data-field="destination" />
    <dx-column caption="Delivery" data-field="delivery" />
    <dx-column caption="Price Terms" data-field="price_terms" />
    <dx-column caption="Origin" data-field="origin" />
    <dx-column caption="Ship Port" data-field="ship_port" />
    <dx-column caption="Packing" data-field="packing" />
    <dx-column caption="Adv Bank" data-field="advbank" />
    <dx-column caption="Currency" data-field="currency" />
    <dx-column caption="Ex Rate" data-field="ex_rate" />
    <dx-column caption="Inspection" data-field="inspection" />
    <dx-column caption="Payment" data-field="payment" />

    <dx-paging :page-size="20" />
    <dx-filter-row :visible="true" />
    <dx-selection :mode="mode" select-all-mode="page" show-check-boxes-mode="always" />
  </dx-data-grid>
</template>

<script>
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { importShipment } from '../../data-source/import';

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
      !(() => (importShipment.defaultFilters = props.fixedFilter))();
    }

    return {
      mode: props.multiple ? 'multiple' : 'single',
      importShipment,
      onSelectionChanged,
    };
  },
};
</script>
