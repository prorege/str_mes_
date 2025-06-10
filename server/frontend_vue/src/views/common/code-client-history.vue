<template>
  <dx-data-grid
    :column-auto-width="true"
    :allow-column-reordering="true"
    :show-borders="true"
    :data-source="vars.dataSource.item"
  >
    <dx-header-filter :visible="true" />

    <dx-column data-field="previous_code" caption="변경전 코드" />
    <dx-column data-field="after_code" caption="변경후 코드" />
    <dx-column data-field="name" caption="업체명" />
    <dx-column data-field="change_reason" caption="변경사유" />
    <dx-column
      data-field="created"
      caption="변경일자"
      data-type="date"
      format="yyyy-MM-dd"
    />
    <dx-column data-field="fk_user_id" caption="변경담당자" />

    <dx-export :enabled="true" :allow-export-selected-data="false" />
    <dx-paging :page-size="20" />
    <dx-filter-row :visible="true" />
  </dx-data-grid>
</template>

<script>
import {
  DxDataGrid,
  DxColumn,
  DxSearchPanel,
  DxHeaderFilter,
  DxExport,
  DxPaging,
  DxFilterRow,
} from 'devextreme-vue/data-grid';
import { getSetupCodeChangeHistory } from '../../data-source/setup';
import { generateItemButtonOption } from '../../utils/util';
import { reactive } from 'vue';

export default {
  components: {
    DxDataGrid,
    DxColumn,
    DxSearchPanel,
    DxHeaderFilter,
    DxExport,
    DxPaging,
    DxFilterRow,
  },
  setup() {
    const vars = { dlg: {} };
    vars.filter = {
      history: [{ name: 'change_type', op: 'eq', val: 2 }],
    };
    vars.dataSource = reactive({
      item: getSetupCodeChangeHistory(vars.filter.history),
    });

    const methods = {};

    return {
      vars,
      methods,
      generateItemButtonOption,
    };
  },
};
</script>

<style></style>
