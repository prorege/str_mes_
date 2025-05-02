<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="importApproval"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="결재번호" data-field="approval_number" :sort-index="1" sort-order="desc" />
    <dx-column caption="결재일" data-field="approval_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
    <dx-column caption="공급업체" data-field="supplier" />
    <dx-column caption="담당부서" data-field="department" />
    <dx-column caption="담당자" data-field="member" />
    <dx-column caption="결재유형" data-field="approval_type" />
    <dx-column caption="환종" data-field="currency" />
    <dx-column caption="비고" data-field="remark" />

    <dx-paging :page-size="20" />
    <dx-filter-row :visible="true" />
    <dx-selection :mode="mode" select-all-mode="page" show-check-boxes-mode="always" />
  </dx-data-grid>
</template>

<script>
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { importApproval } from '../../data-source/import';

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
      !(() => (importApproval.defaultFilters = props.fixedFilter))();
    }

    return {
      mode: props.multiple ? 'multiple' : 'single',
      importApproval,
      onSelectionChanged,
    };
  },
};
</script>
