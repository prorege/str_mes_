<template>
  <div>
    <dx-data-grid
      :data-source="shipmentRelease"
      :show-borders="true"
      :column-auto-width="true"
    >
      <dx-column caption="출고번호" data-field="release.release_number" :filter-operations="['contains', '=']" />
      <dx-column caption="출고일자" data-field="release.release_date" data-type="date" format="yyyy-MM-dd" sort-order="desc" />
      <dx-column caption="출고수량" data-field="release_quantity" data-type="number" format="fixedPoint" />
      <dx-column caption="출고창고" data-field="warehouse.wh_name" />
      <dx-column caption="프로젝트번호" data-field="project_management.project_number" />

      <dx-paging :page-size="5" />
    </dx-data-grid>
  </div>
</template>
<script>
import { DxDataGrid, DxColumn, DxPaging } from 'devextreme-vue/data-grid';

import { getShipmentReleaseItem } from '../../data-source/shipment';

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
      shipmentRelease: this.getTasks(id),
    };
  },
  methods: {
    completedValue(rowData) {
      return rowData.Status === 'Completed';
    },
    getTasks(key) {
      return getShipmentReleaseItem([
        { name: 'fk_order_item_id', op: 'eq', val: key || 0 },
      ]);
    },
  },
};
</script>
