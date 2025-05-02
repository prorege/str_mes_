<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="vars.item"
    :show-borders="true"
    :allow-column-reordering="true"
    :allow-column-resizing="true"
    :column-auto-width="true"
    :remote-operations="true"
    @selection-changed="methods.onSelectionChanged"
  >
    <dx-column caption="품목코드" data-field="item_code" />
    <dx-column caption="품명" data-field="item_name" />
    <dx-column caption="규격" data-field="item_standard" />
    <dx-column caption="자산구분" data-field="asset_type" />
    <dx-column caption="대분류" data-field="main_category" />
    <dx-column caption="중분류" data-field="middle_category" />
    <dx-column caption="소분류" data-field="sub_category" />

    <dx-paging :page-size="20" />
    <dx-selection
      select-all-mode="page"
      show-check-boxes-mode="always"
      :mode="vars.mode"
    />
    <dx-filter-row :visible="true" />
  </dx-data-grid>
</template>

<script>
import { onMounted, reactive } from 'vue';

import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';

import { getBaseItem } from '../../data-source/base';
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
      item: null,
      itemFilter: [
        {
          name: 'fk_company_id',
          op: 'eq',
          val: authService._user.fk_company_id || 0,
        },
      ],
    });

    const methods = {
      refresh: async () => {
        vars.item = getBaseItem(vars.itemFilter);
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
