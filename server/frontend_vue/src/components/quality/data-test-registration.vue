<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="qualityTestRegistration"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="검사번호" data-field="qa_number" :sort-index="1" sort-order="desc" />
    <dx-column caption="검사일자" data-field="qa_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
    <dx-column caption="설비" data-field="equipment" />
    <dx-column caption="품목코드" data-field="item_code" />
    <dx-column caption="품명" data-field="item_name" />
    <dx-column caption="규격" data-field="standard" />
    <dx-column caption="검사자" data-field="qa_manager" />
    <dx-column caption="검사횟수" data-field="qa_count" />
    <dx-column caption="공정명" data-field="process_name" />
    <dx-column caption="작업자" data-field="worker" />
    <dx-column caption="LOT No." data-field="lot_no" />
    <dx-column caption="공정수량" data-field="process_quantity" />
    <dx-column caption="불량수량" data-field="bad_quantity" />
    <dx-column caption="양품수량" data-field="good_quantity" />

    <dx-paging :page-size="20" />
    <dx-filter-row :visible="true" />
    <dx-selection :mode="mode" select-all-mode="page" show-check-boxes-mode="always" />
  </dx-data-grid>
</template>

<script>
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { qualityTestRegistration } from '../../data-source/quality';

export default {
  props: {
    multiple: {
      type: Boolean,
      default: false,
    },
  },
  components: { DxDataGrid, DxColumn, DxSelection, DxPaging, DxFilterRow },
  setup(props, { emit }) {
    const onSelectionChanged = ({ selectedRowsData }) => {
      if (!props.multiple && selectedRowsData)
        selectedRowsData = selectedRowsData[0];
      emit('change', selectedRowsData);
    };

    return {
      mode: props.multiple ? 'multiple' : 'single',
      qualityTestRegistration,
      onSelectionChanged,
    };
  },
};
</script>
