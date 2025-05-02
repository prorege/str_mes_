<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="vars.workOrder"
    :show-borders="true"
    :allow-column-reordering="true"
    :allow-column-resizing="true"
    :column-auto-width="true"
    :remote-operations="true"
    @selection-changed="methods.onSelectionChanged"
  >
    <dx-column caption="작업지시번호" data-field="number" :sort-index="1" sort-order="desc" />
    <dx-column caption="작업지시일자" data-field="target_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
    <dx-column caption="담당부서" data-field="department" />
    <dx-column caption="담당자" data-field="manager" />
    <dx-column caption="참고사항" data-field="note" />
    <dx-column caption="비고" data-field="etc" />

    <dx-paging :page-size="20" />
    <dx-filter-row :visible="true" />
    <dx-selection :mode="vars.mode" select-all-mode="page" show-check-boxes-mode="always" />
  </dx-data-grid>
</template>

<script>
import { onMounted, reactive } from 'vue';

import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';

import { getProduceWorkOrder } from '../../data-source/produce';
import authService from '../../auth';

export default {
  props: {
    multiple: {
      type: Boolean,
      default: false,
    },
  },
  components: { DxDataGrid, DxColumn, DxSelection, DxPaging, DxFilterRow },
  setup(props, { emit }) {
    onMounted(() => {
      methods.refresh();
    });

    const vars = reactive({
      mode: props.multiple ? 'multiple' : 'single',
      workOrder: null,
      planFilter: [
        {
          name: 'fk_company_id',
          op: 'eq',
          val: authService._user.fk_company_id || 0,
        },
      ],
    });

    const methods = {
      refresh: async () => {
        vars.workOrder = getProduceWorkOrder(vars.planFilter);
      },
      onSelectionChanged: ({ selectedRowsData }) => {
        if (!props.multiple && selectedRowsData)
          selectedRowsData = selectedRowsData[0];
        emit('change', selectedRowsData);
      },
    };

    return {
      vars,
      methods,
    };
  },
};
</script>
