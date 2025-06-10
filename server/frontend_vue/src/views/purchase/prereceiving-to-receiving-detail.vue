<template>
  <div>
    <dx-data-grid
      :show-borders="true"
      :column-auto-width="true"
      :data-source="purchaseReceiving"
    >
      <dx-column caption="입고번호" data-field="receiving.receiving_number" :filter-operations="['contains', '=']" />
      <dx-column caption="입고일자" data-field="receiving.receiving_date" data-type="date" format="yyyy-MM-dd" sort-order="desc" />
      <dx-column caption="입고수량" data-field="receiving_quantity" data-type="number" format="fixedPoint" />
      <dx-column caption="입고창고" data-field="warehouse.wh_name" />
      <dx-column caption="프로젝트번호" data-field="project_management.project_number" />

      <dx-paging :page-size="5" />
    </dx-data-grid>
  </div>
</template>
<script>
import { DxDataGrid, DxColumn, DxPaging } from 'devextreme-vue/data-grid';

import { getPurchaseReceivingItem } from '../../data-source/purchase';

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
      purchaseReceiving: this.getTasks(id),
    };
  },
  methods: {
    completedValue(rowData) {
      return rowData.Status === 'Completed';
    },
    getTasks(key) {
      return getPurchaseReceivingItem([
        { name: 'fk_prereceiving_item_id', op: 'eq', val: key || 0 },
      ]);
    },
  },
};
</script>
