<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="shipmentRelease"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="출고번호" data-field="release_number" :sort-index="1" sort-order="desc" />
    <dx-column caption="출고일자" data-field="release_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
    <dx-column caption="고객업체" data-field="client_company" />
    <dx-column caption="업체담당자" data-field="client_manager" />
    <dx-column caption="출고부서" data-field="release_department" />
    <dx-column caption="출고담당자" data-field="release_manager" />
    <dx-column caption="출고구분" data-field="release_type" />
    <dx-column caption="부가세구분" data-field="vat_type" />
    <dx-column caption="결재조건" data-field="payment_terms" />
    <dx-column caption="납품기한" data-field="delivery_date" data-type="date" format="yyyy-MM-dd" />
    <dx-column caption="납품장소" data-field="delivery_place"/>
    <dx-column caption="고객발주번호" data-field="client_order_number" />
    <dx-column caption="프로젝트번호" data-field="project_management.project_number" />
    <dx-column caption="EndUser" data-field="end_user" />
    <dx-column caption="참고사항" data-field="note" />
    <dx-column caption="비고" data-field="etc" />
    <dx-column caption="공급가" data-field="supply_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
    <dx-column caption="부가세" data-field="vat" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
    <dx-column caption="합계금액" data-field="total_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />

    <dx-paging :page-size="20" />
    <dx-filter-row :visible="true" />
    <dx-selection :mode="mode" select-all-mode="page" show-check-boxes-mode="always" />
  </dx-data-grid>
</template>

<script>
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { shipmentRelease } from '../../data-source/shipment';

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
      shipmentRelease,
      onSelectionChanged,
    };
  },
};
</script>
