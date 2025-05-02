<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="importCredit"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="Credit No." data-field="credit_number" :sort-index="1" sort-order="desc" />
    <dx-column caption="Work Day" data-field="work_day" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
    <dx-column caption="Supplier" data-field="supplier" />
    <dx-column caption="Depart" data-field="department" />
    <dx-column caption="Employee" data-field="employee" />
    <dx-column caption="Due Day" data-field="due_day" data-type="date" format="yyyy-MM-dd" />
    <dx-column caption="Credit Type" data-field="credit_type" />
    <dx-column caption="Tax" data-field="tax" />
    <dx-column caption="Excute Day" data-field="excute_day" data-type="date" format="yyyy-MM-dd" />
    <dx-column caption="Currency" data-field="currency" />
    <dx-column caption="Remark" data-field="remark" />

    <dx-paging :page-size="20" />
    <dx-filter-row :visible="true" />
    <dx-selection :mode="mode" select-all-mode="page" show-check-boxes-mode="always" />
  </dx-data-grid>
</template>

<script>
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { importCredit } from '../../data-source/import';

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
      !(() => (importCredit.defaultFilters = props.fixedFilter))();
    }

    return {
      mode: props.multiple ? 'multiple' : 'single',
      importCredit,
      onSelectionChanged,
    };
  },
};
</script>
