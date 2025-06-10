<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="shipmentLend"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="가출고번호" data-field="lend_number" :sort-index="1" sort-order="desc" />
    <dx-column caption="가출고일자" data-field="lend_date"  data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
    <dx-column caption="관련업체" data-field="client_company" />
    <dx-column caption="가출고담당자" data-field="lend_manager" />
    <dx-column caption="품목코드" data-field="item_code" />
    <dx-column caption="품명" data-field="item.item_name" />
    <dx-column caption="규격" data-field="item.item_standard" />
    <dx-column caption="가출고수량" data-field="quantity" />
    <dx-column caption="미회수수량" data-field="not_retrieved_quantity" />
    <dx-column caption="참고사항" data-field="note" />
    <dx-column caption="비고" data-field="etc" />

    <dx-paging :page-size="20" />
    <dx-filter-row :visible="true" />
    <dx-selection :mode="mode" select-all-mode="page" show-check-boxes-mode="always" />
  </dx-data-grid>
</template>

<script>
import { DxDataGrid, DxColumn, DxPaging, DxSelection,  DxFilterRow } from 'devextreme-vue/data-grid';
import { shipmentLend } from '../../data-source/shipment';

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
      shipmentLend,
      onSelectionChanged,
    };
  },
};
</script>
