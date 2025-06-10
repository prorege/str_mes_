<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="stockEtcItem"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="기타입출고 번호" data-field="stock_etc.number" />
    <dx-column caption="입출고 일자" data-field="stock_etc.target_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
    <dx-column caption="품목번호" data-field="item.item_code" />
    <dx-column caption="품목이름" data-field="item.item_name" />
    <dx-column caption="규격" data-field="item.item_standard" />
    <dx-column caption="담당부서" data-field="stock_etc.department" />
    <dx-column caption="담당자" data-field="stock_etc.manager" />
    <dx-column caption="참고사항" data-field="stock_etc.note" />
    <dx-column caption="비고" data-field="stock_etc.etc" />

    <dx-paging :page-size="20" />
    <dx-filter-row :visible="true" />
    <dx-selection :mode="mode" select-all-mode="page" show-check-boxes-mode="always" />
  </dx-data-grid>
</template>

<script>
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { stockEtcItem } from '../../data-source/stock';

export default {
  props: {
    multiple: {
      type: Boolean,
      default: false,
    },
    filter: {
      type: Array
    }
  },
  components: { DxDataGrid, DxColumn, DxSelection, DxPaging, DxFilterRow },
  setup(props, { emit }) {
    if (props.filter) {
      stockEtcItem.defaultFilters = [...props.filter]
    }

    const onSelectionChanged = ({ selectedRowsData }) => {
      if (!props.multiple && selectedRowsData)
        selectedRowsData = selectedRowsData[0];
      emit('change', selectedRowsData);
    };

    return {
      mode: props.multiple ? 'multiple' : 'single',
      stockEtcItem,
      onSelectionChanged,
    };
  },
};
</script>
