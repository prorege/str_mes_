<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="importClearance"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="통관번호" data-field="clearance_number" :sort-index="1" sort-order="desc" />
    <dx-column caption="통관일자" data-field="clearance_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
    <dx-column caption="Supplier" data-field="supplier" />
    <dx-column caption="Buyer" data-field="buyer" />
    <dx-column caption="부서" data-field="clearance_department" />
    <dx-column caption="담당자" data-field="member" />
    <dx-column caption="Currency" data-field="currency" />
    <dx-column caption="ExRate" data-field="ex_rate" />
    <dx-column caption="Remark" data-field="remark" />

    <dx-paging :page-size="20" />
    <dx-filter-row :visible="true" />
    <dx-selection :mode="mode" select-all-mode="page" show-check-boxes-mode="always" />
  </dx-data-grid>
</template>

<script>
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { importClearance } from '../../data-source/import';

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
      !(() => (importClearance.defaultFilters = props.fixedFilter))();
    }

    return {
      mode: props.multiple ? 'multiple' : 'single',
      importClearance,
      onSelectionChanged,
    };
  },
};
</script>
