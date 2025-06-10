<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :focused-row-enabled="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    :data-source="vars.balance.item"
    :selection="{ mode: 'single' }"
    @saving="methods.onSavingBalance"
    @initialized="methods.initialized($event, 'setup-balance')"
  >
    <dx-grid-toolbar>
      <dx-item name="searchPanel" location="before" />
      <dx-item name="addRowButton" :visible="false" />
      <dx-item name="saveButton" :visible="false" />
      <dx-item name="revertButton" :visible="false" />
    </dx-grid-toolbar>

    <dx-column caption="업체명" data-field="base_client.name" :allow-editing="false" />
    <dx-column caption="업체약칭" data-field="base_client.alias" :allow-editing="false" />
    <dx-column caption="사업자번호" data-field="base_client.business_number" :allow-editing="false" />
    <dx-column caption="매출잔액" data-field="sales_balance" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :allow-editing="false" />
    <dx-column caption="매입잔액" data-field="purchase_balance" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :allow-editing="false" />

    <dx-paging :page-size="10" />
    <dx-filter-row :visible="true" />
    <dx-header-filter :visible="false" />
    <dx-export :enabled="true" :allow-export-selected-data="false" />
    <dx-search-panel :visible="false" :width="240" placeholder="검색" />
    <dx-editing
      mode="batch"
      :use-icons="true"
      :allow-adding="false"
      :allow-updating="false"
      :allow-deleting="false"
    />
    <dx-pager
      :visible="true"
      :show-info="false"
      :show-page-size-selector="false"
      :show-navigation-buttons="false"
    />
  </dx-data-grid>

  <div id="app-container">
    <input
      hidden
      type="file"
      ref="excelRef"
      accept=".xlsx,.xls"
      @change="methods.excelFileChange"
    />
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';

import { DxButton } from 'devextreme-vue/button';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxDataGrid, DxItem, DxPager, DxPaging, DxColumn, DxExport, DxLookup, DxEditing, DxSelection, DxScrolling, DxFilterRow, DxSearchPanel, DxHeaderFilter, DxColumnChooser, DxToolbar as DxGridToolbar } from 'devextreme-vue/data-grid';

import { baseItem } from '../../data-source/base';
import { setupBasicBalance, getSetupBasicBalance } from '../../data-source/setup';

import authService from '../../auth';

import stateStore from '@/utils/state-store';

export default {
  components: {
    DxButton,
    DxPopup, DxToolbarItem,
    DxDataGrid, DxItem, DxPager, DxPaging, DxColumn, DxExport, DxLookup, DxEditing, DxSelection, DxScrolling, DxFilterRow, DxSearchPanel, DxHeaderFilter, DxColumnChooser, DxGridToolbar,
  },
  setup() {
    const excelRef = ref(null);
    const vars = {};
    vars.component = {};
    vars.balance = reactive({
      item: null,
      grid: null,
      filter: [{ name: 'fk_company_id', op: 'eq', val: authService.getCompanyId() || 0 }],
    });

    const methods = {
      initialized(evt, key) {
        vars.component[key] = evt.component;
        stateStore.bind(key, evt.component);
      },
      async refreshBasicBalance() {
        vars.balance.item = getSetupBasicBalance(vars.balance.filter);
      },
      isArrayEmpty(array) {
        if ((array && array.length) < 1) {
          return true;
        }
        return false;
      },
      onSavingBalance(e) {
        e.changes.forEach(item => {
          if (item.type != 'remove') {
            delete item.data.base_client;
            item.data.fk_company_id = authService.getCompanyId();
          }
        });
      },
    };

    onMounted(() => {
      methods.refreshBasicBalance();
    });

    return {
      vars,
      excelRef,
      methods,
      baseItem,
    };
  },
};
</script>

<style></style>
