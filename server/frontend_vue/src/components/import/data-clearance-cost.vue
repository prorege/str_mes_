<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="importClearanceCost"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="비용번호" data-field="clearance_cost_number" :sort-index="1" sort-order="desc" />
    <dx-column caption="발행일" data-field="clearance_cost_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
    <dx-column caption="통관번호" data-field="clearance.clearance_number" />
    <dx-column caption="비용구분" data-field="cost_type" />
    <dx-column caption="Supplier" data-field="supplier" />
    <dx-column caption="담당부서" data-field="department" />
    <dx-column caption="담당자" data-field="member" />
    <dx-column caption="Amount" data-field="amount" />
    <dx-column caption="Currency" data-field="currency" />
    <dx-column caption="ExRate" data-field="ex_rate" />
    <dx-column caption="Won Amt" data-field="won_amount" />
    <dx-column caption="Remark" data-field="remark" />

    <dx-paging :page-size="20" />
    <dx-filter-row :visible="true" />
    <dx-selection :mode="mode" select-all-mode="page" show-check-boxes-mode="always" />
  </dx-data-grid>
</template>

<script>
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { importClearanceCost } from '../../data-source/import';

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
      !(() => (importClearanceCost.defaultFilters = props.fixedFilter))();
    }

    return {
      mode: props.multiple ? 'multiple' : 'single',
      importClearanceCost,
      onSelectionChanged,
    };
  },
};
</script>
