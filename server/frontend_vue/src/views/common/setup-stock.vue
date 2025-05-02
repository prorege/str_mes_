<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="vars.stock.item"
    :selection="{ mode: 'single' }"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :focused-row-enabled="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @saving="methods.onStockSaving"
    @cell-click="methods.onStockCellClick"
    @init-new-row="methods.onStockInitNewRow"
    @editor-preparing="methods.onStockEditorPreparing"
    @initialized="(evt) => methods.initialized(evt, 'gridStock')"
  >
    <dx-grid-toolbar>
      <dx-item template="calculateStock" location="before" />
      <dx-item name="searchPanel" location="before" />
      <dx-item name="addRowButton" template="addStockButton" :visible="false" />
      <dx-item name="saveButton" :visible="false" />
      <dx-item name="revertButton" :visible="false" />
      <dx-item location="after" template="excelSampleDownloadButton" />
      <dx-item location="after" template="excelUploadButton" />
    </dx-grid-toolbar>
    <template #calculateStock>
      <dx-button text="현재고 재계산" icon="formula" @click="methods.calculateStock" />
    </template>
    <template #addStockButton>
      <dx-button icon="add" @click="methods.showAddItemPopup" />
    </template>
    <template #excelUploadButton>
      <dx-button icon="upload" @click="methods.excelUpload" />
    </template>
    <template #excelSampleDownloadButton>
      <dx-button icon="download" @click="methods.excelSampleDownload" />
    </template>

    <dx-column caption="창고구분" data-field="wh_code">
      <dx-lookup value-expr="wh_code" display-expr="wh_name" :data-source="vars.dataSource.warehouse" />
      <dx-required-rule message="창고를 선택하세요" />
      <dx-async-rule
        :validation-callback="methods.duplicateCheck"
        message="해당 창고에 동일한 품목이 존재합니다"
      />
      <dx-custom-rule
        :validation-callback="methods.duplicateCheckGrid"
        message="해당 창고에 동일한 품목이 존재합니다"
      />
    </dx-column>
    <dx-column caption="자산구분" data-field="item.asset_type" :allow-editing="false" />
    <dx-column caption="품목코드" data-field="item_code" :allow-editing="false" />
    <dx-column caption="품명" data-field="item.item_name" :allow-editing="false" />
    <dx-column caption="규격" data-field="item.item_standard" :allow-editing="false" />
    <dx-column caption="기초재고수량" data-field="basic_stock" data-type="number" format="fixedPoint" :set-cell-value="methods.setBasicStock" :allow-editing="vars.permission.value" >
      <dx-required-rule message="기초재고수량을 입력하세요" />
      <dx-range-rule :max="1000000000" message="1,000,000,000까지 입력 가능합니다" />
    </dx-column>
    <dx-column caption="현재고" data-field="current_stock" data-type="number" format="fixedPoint" :allow-editing="false">
      <dx-required-rule message="현재고수량을 입력하세요" />
      <dx-range-rule :max="1000000000" message="1,000,000,000까지 입력 가능합니다" />
    </dx-column>
    <dx-column caption="가용재고" data-field="available_stock" data-type="number" format="fixedPoint" :allow-editing="false">
      <dx-required-rule message="가용재고수량을 입력하세요" />
      <dx-range-rule :max="1000000000" message="1,000,000,000까지 입력 가능합니다" />
    </dx-column>
    <dx-column caption="단가" data-field="item_unit_price" data-type="number" :format="{ type: 'fixedPoint', precision: 4 }" :set-cell-value="methods.setUnitPrice" :allow-editing="false" >
      <dx-range-rule :max="1000000000" message="1,000,000,000까지 입력 가능합니다" />
    </dx-column>
    <dx-column caption="금액" data-field="item_price" data-type="number" :format="{ type: 'fixedPoint', precision: 4 }" :allow-editing="false" />
    <dx-column data-field="etc" caption="비고" :allow-editing="false" />

    <dx-paging :page-size="10" />
    <dx-filter-row :visible="true" />
    <dx-header-filter :visible="false" />
    <dx-export :enabled="true" :allow-export-selected-data="false" />
    <dx-search-panel placeholder="검색" :visible="false" :width="240" />
    <dx-editing mode="row"
      :use-icons="true"  
      :allow-adding="false"
      :allow-updating="vars.permission.value"
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
    <dx-popup
      title="품목찾기"  
      content-template="popup-content"
      v-model:visible="vars.addItem.visible"
      :width="680"
      :height="460"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="(evt) => methods.initialized(evt, 'popupItem')"
    >
      <dx-toolbar-item
        widget="dxButton"
        toolbar="top"
        location="after"
        :options="{ text: '선택된 항목 추가', icon: 'add', onClick: methods.addSelectedRows }"
      />

      <template #popup-content>
        <dx-data-grid
          :data-source="baseItem"  
          :on-initialized="(evt) => methods.initialized(evt, 'gridItem')"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
        >
          <dx-column caption="품목코드"  data-field="item_code" />
          <dx-column caption="품명" data-field="item_name" />
          <dx-column caption="규격" data-field="item_standard" />
          <dx-column caption="자산구분" data-field="asset_type">
            <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.dataSource.asset_type" />
          </dx-column>
          <dx-column caption="품목설명" data-field="item_detail" />

          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-selection
            mode="multiple"  
            select-all-mode="page"
            show-check-boxes-mode="onClick"
          />
        </dx-data-grid>
      </template>
    </dx-popup>

    <input hidden type="file" ref="excelRef" accept=".xlsx,.xls" @change="methods.excelFileChange" />
  </div>
</template>

<script>
import {
  DxDataGrid,
  DxColumn,
  DxSearchPanel,
  DxHeaderFilter,
  DxFilterRow,
  DxEditing,
  DxExport,
  DxLookup,
  DxPager,
  DxPaging,
  DxToolbar as DxGridToolbar,
  DxItem,
  DxSelection,
  DxScrolling,
  DxColumnChooser,
  DxRequiredRule,
  DxRangeRule,
  DxAsyncRule,
  DxCustomRule,
} from 'devextreme-vue/data-grid';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxButton } from 'devextreme-vue/button';
import { reactive, onMounted, ref } from 'vue';
import { setupBasicStock, getSetupBasicStock } from '../../data-source/setup';
import { baseItem, baseCodeLoader } from '../../data-source/base';
import ApiService from '../../utils/api-service';
import { saveAs } from 'file-saver';
import authService from '../../auth';
import stateStore from '@/utils/state-store';
import { loadWarehouse } from '../../utils/data-loader';
import { confirm, alert } from 'devextreme/ui/dialog';

export default {
  components: {
    DxDataGrid,
    DxColumn,
    DxSearchPanel,
    DxHeaderFilter,
    DxFilterRow,
    DxEditing,
    DxExport,
    DxLookup,
    DxPopup,
    DxToolbarItem,
    DxPager,
    DxPaging,
    DxGridToolbar,
    DxItem,
    DxButton,
    DxSelection,
    DxScrolling,
    DxColumnChooser,
    DxRequiredRule,
    DxAsyncRule,
    DxCustomRule,
    DxRangeRule,
  },
  setup() {
    const excelRef = ref(null);
    const apiService = new ApiService('/api/mes/v1/excel/setup/basic_stock');
    const apiCalcStock = new ApiService('/api/mes/v1/setup/calcstock');
    const vars = {};
    vars.permission = ref(false);
    vars.permission.value = authService.user?.user_type == 1;
  
    vars.component = {};
    vars.stock = reactive({
      grid: null,
      selectedCell: null,
      item: null,
      filter: [
        {
          name: 'fk_company_id',
          op: 'eq',
          val: authService._user.fk_company_id || 0,
        },
      ],
    });
    vars.dataSource = reactive({
      warehouse: [],
      asset_type: [],
    });
    vars.addItem = reactive({
      visible: false,
    });

    const methods = {
      initialized(evt, key) {
        vars.component[key] = evt.component;
        stateStore.bind(key, evt.component);
      },
      async refreshBasicStock() {
        vars.stock.item = getSetupBasicStock(vars.stock.filter);
      },
      isArrayEmpty(array) {
        if ((array && array.length) < 1) {
          return true;
        }
        return false;
      },
      showAddItemPopup() {
        if (vars.component.gridItem) {
          vars.component.gridItem.deselectAll();
          vars.component.gridItem.refresh().then(function () {
            vars.addItem.visible = true;
          });
        } else {
          vars.addItem.visible = true;
        }
      },
      hideAddItemPopup() {
        vars.addItem.visible = false;
      },
      async addSelectedRows() {
        const grid = vars.component.gridStock;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        const rows = await vars.component.gridItem.getSelectedRowsData();
        for (let row of rows) {
          await grid.addRow();
          grid.cellValue(0, 'item_code', row.item_code); // 품목코드
          grid.cellValue(0, 'item.item_name', row.item_name); // 품명
          grid.cellValue(0, 'item.asset_type', row.asset_type); // 자산구분
          grid.cellValue(0, 'item.item_standard', row.item_standard); // 규격
          grid.cellValue(0, 'basic_stock', 0); // 기초재고수량
          grid.cellValue(0, 'current_stock', 0); // 현재고
          grid.cellValue(0, 'available_stock', 0); // 가용재고
          grid.cellValue(0, 'item_unit_price', 0); // 단가
          grid.cellValue(0, 'etc', ''); // 비고
          if (vars.dataSource.warehouse.length > 0) {
            grid.cellValue(0, 'wh_code', vars.dataSource.warehouse[0].wh_code); // 창고구분
          }
        }
        methods.hideAddItemPopup();
      },
      onStockCellClick(e) {
        vars.stock.selectedCell = e;
        vars.stock.grid = e.component;
      },
      onStockInitNewRow(e) {
        e.data.fk_company_id = authService._user.fk_company_id;
      },
      onStockToolbarPreparing(e) {
        let toolbarItems = e.toolbarOptions.items;
        toolbarItems.forEach(function (item) {
          if (item.name === 'searchPanel') {
            item.location = 'before';
          }
        });
      },
      onStockSaving(e) {
        e.changes.forEach((item) => {
          if (item.type != 'remove') {
            delete item.data.item;
            item.data.available_stock = item.data.current_stock;
            item.data.fk_company_id = authService.getCompanyId();
          }
        });
      },
      onStockEditorPreparing(e) {
        if (e.dataField == 'item_code' && e.parentType === 'filterRow') {
          e.editorOptions.buttons = [];
        }
      },
      excelUpload() {
        excelRef.value.click();
      },
      async excelFileChange({ target }) {
        if (!target.files.length) return;

        vars.component.gridStock.beginCustomLoading(
          '엑셀 데이터를 읽고 있습니다'
        );
        const fd = new FormData();
        fd.append('file', target.files[0]);

        try {
          await apiService.post('', fd);
          vars.component.gridStock.refresh();
        } catch (ex) {
          console.error(ex);
          console.log(ex.response);
        } finally {
          vars.component.gridStock.endCustomLoading();
          target.value = null;
        }
      },
      excelSampleDownload() {
        saveAs('/api/mes/v1/excel/setup/basic_stock', '기초재고입력양식.xlsx');
      },
      calcSupplyPrice(rowData) {
        let item_price = 0;
        if (rowData.current_stock && rowData.item_unit_price) {
          item_price = rowData.current_stock * rowData.item_unit_price;
        }
        rowData.item_price = item_price;
        return item_price;
      },
      duplicateCheck(params) {
        return setupBasicStock
          .load({
            filter: [
              ['wh_code', '=', params.data.wh_code],
              ['item_code', '=', params.data.item_code],
            ],
          })
          .then(({ data }) => {
            if (data.length > 0) {
              if (params.data.id && params.data.id == data[0].id) {
                return true;
              }
              return false;
            }
            return true;
          });
      },
      duplicateCheckGrid(e) {
        let count = 0;
        const rows = vars.component.gridStock.getVisibleRows();
        for (let i = 0; i < rows.length; i++) {
          const rowData = rows[i].data;
          if (
            rowData.item_code == e.data.item_code &&
            rowData.wh_code == e.data.wh_code
          ) {
            count += 1;
          }
        }
        if (count > 1) {
          return false;
        }
        return true;
      },
      setBasicStock(newData, value, currentRowData) {  
        // newData.current_stock = value + currentRowData.current_stock - currentRowData.basic_stock;
        // newData.available_stock = value + currentRowData.available_stock - currentRowData.basic_stock;
        newData.basic_stock = value;
        newData.item_price = value * currentRowData.item_unit_price;
      },
      setUnitPrice(newData, value, currentRowData) {
        newData.item_unit_price = value;
        newData.item_price = value * currentRowData.basic_stock;
      },
      async calculateStock() {
        try {
          vars.component.gridStock.beginCustomLoading('계산중입니다');
          vars.component.gridStock.refresh();
          await apiCalcStock.post('');
        } catch (ex) {
          console.error(ex);
        } finally {
          vars.component.gridStock.endCustomLoading();
          await alert('계산이 완료되었습니다', '현재고 재계산');
          vars.component.gridStock.refresh();
        }
      },
    };

    onMounted(() => {
      methods.refreshBasicStock();
      loadWarehouse(vars.dataSource);
      baseCodeLoader(['자산구분'], authService.getCompanyId()).then(
        (response) => {
          vars.dataSource.asset_type = response['자산구분'];
        }
      );
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
