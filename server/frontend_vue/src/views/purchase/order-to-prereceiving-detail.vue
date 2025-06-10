<template>
  <div>
    <dx-data-grid
      :show-borders="true"
      :column-auto-width="true"
      :data-source="purchasePrereceiving"
    >
      <dx-column caption="가입고번호" data-field="prereceiving.prereceiving_number" :filter-operations="['contains', '=']" />
      <dx-column caption="가입고일자" data-field="prereceiving.prereceiving_date" data-type="date" format="yyyy-MM-dd" sort-order="desc" />
      <dx-column caption="가입고수량" data-field="prereceiving_quantity" data-type="number" format="fixedPoint" />
      <dx-column caption="미입고수량" data-field="not_shipped" data-type="number" format="fixedPoint" />
      <dx-column caption="검수수량" data-field="check_quantity" data-type="number" format="fixedPoint" />
      <dx-column caption="불량수량" data-field="bad_quantity" data-type="number" format="fixedPoint" />
      <dx-column caption="양품수량" data-field="good_quantity" data-type="number" format="fixedPoint" />
      <dx-column caption="입고창고" data-field="warehouse.wh_name" />
      <dx-column caption="프로젝트번호" data-field="project_management.project_number" />
      <dx-column caption="검수완료" data-field="check_yn" data-type="boolean" />

      <dx-paging :page-size="5" />
    </dx-data-grid>
  </div>
</template>
<script>
import { DxDataGrid, DxColumn, DxPaging } from 'devextreme-vue/data-grid';

import { getPurchasePreReceivingItem } from '../../data-source/purchase';

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
      purchasePrereceiving: this.getTasks(id),
    };
  },
  methods: {
    completedValue(rowData) {
      return rowData.Status === 'Completed';
    },
    getTasks(key) {
      return getPurchasePreReceivingItem([
        { name: 'fk_order_item_id', op: 'eq', val: key || 0 },
      ]);
    },
  },
};
</script>
