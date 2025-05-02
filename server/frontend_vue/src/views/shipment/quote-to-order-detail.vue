<template>
  <div>
    <dx-data-grid
      :data-source="shipmentOrder"
      :show-borders="true"
      :column-auto-width="true"
    >
      <dx-column caption="수주번호" data-field="order.order_number" :filter-operations="['contains', '=']" />
      <dx-column caption="수주일자" data-field="order.order_date" data-type="date" format="yyyy-MM-dd" sort-order="desc" />
      <dx-column caption="수주수량" data-field="order_quantity" data-type="number" format="fixedPoint" />
      <dx-column caption="수주창고" data-field="warehouse.wh_name" />
      <dx-column caption="프로젝트번호" data-field="project_management.project_number" />

      <dx-paging :page-size="5" />
    </dx-data-grid>
  </div>
</template>
<script>
import { DxDataGrid, DxColumn, DxPaging } from 'devextreme-vue/data-grid';

import { getShipmentOrderItem } from '../../data-source/shipment';

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
      shipmentOrder: this.getTasks(id),
    };
  },
  methods: {
    completedValue(rowData) {
      return rowData.Status === 'Completed';
    },
    getTasks(key) {
      return getShipmentOrderItem([
        { name: 'fk_quote_item_id', op: 'eq', val: key || 0 },
      ]);
    },
  },
};
</script>
