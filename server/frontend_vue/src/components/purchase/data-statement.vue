<template>
    <dx-data-grid
      column-resizing-mode="widget"
      :data-source="purchaseStatement"
      :show-borders="true"
      :column-auto-width="true"
      :remote-operations="true"
      :allow-column-resizing="true"
      :allow-column-reordering="true"
      @selection-changed="onSelectionChanged"
    >
      <dx-column caption="계산서번호" data-field="statement_number" :sort-index="1" sort-order="desc" />
      <dx-column caption="발행일자" data-field="statement_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
      <dx-column caption="고객업체" data-field="client_company" />
      <dx-column caption="업체담당자" data-field="client_manager" />
      <dx-column caption="매출부서" data-field="statement_department" />
      <dx-column caption="매출담당자" data-field="statement_manager" />
      <dx-column caption="부가세구분" data-field="vat_type" />
      <dx-column caption="계산서유형" data-field="statement_type" />
      <dx-column caption="결재유형" data-field="approval_type" />
      <dx-column caption="발행구분" data-field="publish_type" />
      <dx-column caption="본지점구분" data-field="office_type" />
      <dx-column caption="비고" data-field="etc" />
      <dx-column caption="공급가" data-field="supply_price"  data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
      <dx-column caption="부가세" data-field="vat" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
      <dx-column caption="합계금액" data-field="total_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
  
      <dx-paging :page-size="20" />
      <dx-filter-row :visible="true" />
      <dx-selection :mode="mode" select-all-mode="page" show-check-boxes-mode="always" />
    </dx-data-grid>
</template>

<script>
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { purchaseStatement } from '../../data-source/purchase';

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
    purchaseStatement,
    onSelectionChanged,
    };
},
};
</script>
  