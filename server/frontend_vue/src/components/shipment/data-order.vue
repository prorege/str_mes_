<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="shipmentOrder"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @selection-changed="onSelectionChanged"
  >
    <dx-column caption="수주번호" data-field="order_number" :sort-index="1" sort-order="desc"  width="140" />
    <dx-column caption="수주일자" data-field="order_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
    <dx-column caption="고객업체" data-field="client_company" />
    <dx-column caption="업체담당자" data-field="client_manager" />
    <dx-column caption="수주부서" data-field="order_department" />
    <dx-column caption="수주담당자" data-field="order_manager" />
    <dx-column caption="수주구분" data-field="order_type" />
    <dx-column caption="부가세구분" data-field="vat_type" />
    <dx-column caption="결재조건" data-field="payment_terms" />
    <dx-column caption="납품기한" data-field="delivery_date" data-type="date" format="yyyy-MM-dd" />
    <dx-column caption="납품장소" data-field="delivery_place" />
    <dx-column caption="고객발주번호" data-field="previous_order_number" />
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
import { shipmentOrder } from '../../data-source/shipment';

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
      console.log('selectedRowsData : ', selectedRowsData);
      if (!props.multiple && selectedRowsData)
        selectedRowsData = selectedRowsData[0];
      emit('change', selectedRowsData);
    };

    if (props.fixedFilter) {
      !(() => (shipmentOrder.defaultFilters = props.fixedFilter))();
    }

    return {
      mode: props.multiple ? 'multiple' : 'single',
      shipmentOrder,
      onSelectionChanged,
    };
  },
};
</script>
