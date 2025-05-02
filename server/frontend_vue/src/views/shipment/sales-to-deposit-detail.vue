<template>
  <div>
    <dx-data-grid
      :show-borders="true"
      :column-auto-width="true"
      :data-source="shipmentDeposit"
    >
      <dx-column caption="입금번호" data-field="deposit.deposit_number" :filter-operations="['contains', '=']" />
      <dx-column caption="발행일자" data-field="deposit.deposit_date" data-type="date" format="yyyy-MM-dd" sort-order="desc" />
      <dx-column caption="금액" data-field="price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
      <dx-column caption="입금형태" data-field="deposit_type" />
      <dx-column caption="프로젝트번호" data-field="project_management.project_number" />
      <dx-column caption="입금적요" data-field="etc" />

      <dx-paging :page-size="5" />
    </dx-data-grid>
  </div>
</template>
<script>
import { DxDataGrid, DxColumn, DxPaging } from 'devextreme-vue/data-grid';

import { getShipmentDepositItem } from '../../data-source/shipment';

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
      shipmentDeposit: this.getTasks(id),
    };
  },
  methods: {
    completedValue(rowData) {
      return rowData.Status === 'Completed';
    },
    getTasks(key) {
      return getShipmentDepositItem([
        { name: 'fk_sales_id', op: 'eq', val: key || 0 },
      ]);
    },
  },
};
</script>
