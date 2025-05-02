<template>
  <div>
    <dx-data-grid
      :data-source="shipmentSales"
      :show-borders="true"
      :column-auto-width="true"
    >
      <dx-column caption="계산서번호" data-field="sales.sales_number" :filter-operations="['contains', '=']" />
      <dx-column caption="발행일자" data-field="sales.sales_date" data-type="date" format="yyyy-MM-dd" sort-order="desc" />
      <dx-column caption="수량" data-field="quantity" data-type="number" format="fixedPoint" />
      <dx-column caption="단가" data-field="unit_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
      <dx-column caption="공급가" data-field="supply_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
      <dx-column caption="부가세" data-field="vat" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
      <dx-column caption="합계금액" data-field="total_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
      <dx-column caption="프로젝트번호" data-field="project_management.project_number" />

      <dx-paging :page-size="5" />
    </dx-data-grid>
  </div>
</template>
<script>
import { DxDataGrid, DxColumn, DxPaging } from 'devextreme-vue/data-grid';

import { getShipmentSalesStatementItem } from '../../data-source/shipment';

export default {
  components: { DxDataGrid, DxColumn, DxPaging },
  props: {
    templateData: {
      type: Object,
      default: () => {},
    },
  },
  data() {
    const { id } = this.templateData.data;
    return {
      shipmentSales: this.getTasks(id),
    };
  },
  methods: {
    completedValue(rowData) {
      return rowData.Status === 'Completed';
    },
    getTasks(key) {
      return getShipmentSalesStatementItem([
        { name: 'fk_release_item_id', op: 'eq', val: key || 0 },
      ]);
    },
  },
};
</script>
