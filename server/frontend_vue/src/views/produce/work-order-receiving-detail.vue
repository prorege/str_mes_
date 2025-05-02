<template>
  <div>
    <dx-data-grid
      :show-borders="true"
      :remote-operations="true"
      :column-auto-width="true"
      :data-source="performanceItem1"
    >
      <dx-column caption="입고번호" data-field="performance_registration.number" :allow-sorting="false" :filter-operations="['contains', '=']" />
      <dx-column caption="입고일자" data-field="performance_registration.target_date" data-type="date" format="yyyy-MM-dd" sort-order="desc" />
      <dx-column caption="입고수량" data-field="production_receiving_quantity" data-type="number" format="fixedPoint" />
      <dx-column caption="입고창고" data-field="warehouse.wh_name" :allow-sorting="false" />
      <dx-column caption="프로젝트번호" data-field="project_management.project_number" />

      <dx-paging :page-size="5" />
    </dx-data-grid>
  </div>
</template>
<script>
import { DxDataGrid, DxColumn, DxPaging } from 'devextreme-vue/data-grid';

import { getPerformanceItem1 } from '../../data-source/produce';

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
      performanceItem1: this.getTasks(id),
    };
  },
  methods: {
    completedValue(rowData) {
      return rowData.Status === 'Completed';
    },
    getTasks(key) {
      return getPerformanceItem1([
        { name: 'fk_work_order_item', op: 'eq', val: key || 0 },
      ]);
    },
  },
};
</script>
