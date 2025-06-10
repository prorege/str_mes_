<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">사급자재입고</div>
            </dx-item>
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{text: '신규', type: 'add', icon: 'add', disabled: vars.disabled.new, onClick: methods.newItem}"
            />
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{text: '수정', type: 'rename', icon: 'rename', disabled: vars.disabled.edit, onClick: methods.editItem}"
            />
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{text: '삭제', type: 'remove', icon: 'remove', disabled: vars.disabled.delete, onClick: methods.deleteItem}"
            />
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{text: '저장', type: 'save', icon: 'save', disabled: vars.disabled.save, onClick: methods.saveItem}"
            />
          </dx-toolbar>
        </div>
        <dx-form :form-data="vars.formData">
          <dx-group-item :col-count="4">
            <dx-group-item>
              <dx-simple-item data-field="number"
                :editor-options="{
                  placeholder: '(자동 or 직접입력)',
                  ...generateItemButtonOption('search', methods.createFindPopupFn('stock-correction', '사급자재조회'))
                }"
              >
                <dx-label text="입고번호" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="target_date" editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  ...vars.formState,
                }"
              >
                <dx-label text="입고일자" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="department" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'department_name',
                  displayExpr: 'department_name',
                  acceptCustomValue: true,
                  dataSource: vars.dataSource.department,
                  onValueChanged: methods.onDepartmentChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="담당부서" :show-colon="false" />
                <dx-required-rule message="담당부서를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="manager" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'emp_name',
                  displayExpr: 'emp_name',
                  disabled: vars.disabled.manager,
                  dataSource: vars.dataSource.employee,
                  ...vars.formState,
                }"
              >
                <dx-label text="담당자" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="note" :editor-options="{ ...vars.formState }">
                <dx-label text="참고사항" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="etc" editor-type="dxTextArea"
                :editor-options="{
                  height: '80px',
                  labelMode: 'hidden',
                  placeholder: '비고',
                  ...generateItemButtonOption('rename', methods.createFindPopupFn('etc', '비고', vars.formData.etc)),
                  ...vars.formState,
                }"
              >
                <dx-label text="비고" :show-colon="false" :visible="false" />
              </dx-simple-item>
            </dx-group-item>
          </dx-group-item>
        </dx-form>
      </div>

      <div class="dx-card responsive-paddings mt-1">
        <div class="mt-2">
          <dx-data-grid
            class="fixed-header-table"
            height="calc(100vh - 286px)"
            date-serialization-format="yyyy-MM-ddTHH:mm:ss"
            column-resizing-mode="widget"
            :show-borders="true"
            :column-auto-width="true"
            :remote-operations="true"
            :focused-row-enabled="true"
            :allow-column-resizing="true"
            :row-alternation-enabled="true"
            :allow-column-reordering="true"
            :select-text-on-edit-start="true"
            :disabled="vars.disabled.items"
            :data-source="vars.stockCorrectionItem"
            :on-initialized="evt => methods.onGridInitialized(evt, 'item1')"
            @saving="methods.onSavingItem"
            @data-error-occurred="methods.onDataError"
            @cell-dbl-click="methods.itemPopupClick"
            @focused-cell-changed="methods.onFocusedCellChanged"
          >
            <dx-grid-toolbar>
              <dx-item template="addFromCommInvoice" location="before" :visible="!vars.formState.readOnly" />
              <dx-grid-item name="addRowButton" :options="{ onClick: methods.showAddPopup }" />
              <dx-grid-item name="saveButton" :visible="!!vars.formData.id" />
              <dx-grid-item name="revertButton" />
              <dx-grid-item name="columnChooserButton" />
            </dx-grid-toolbar>
            <template #addFromCommInvoice>
              <dx-button text="사급자재 가져오기" icon="add" @click="methods.showAddCommInvoiceItemPopup" />
            </template>

            <dx-column caption="입고구분" data-field="type" >
              <dx-lookup alue-expr="code_name" display-expr="code_name" :data-source="vars.dataSource.type" />
            </dx-column>
            <dx-column caption="품목코드" data-field="item_code" width="180" :allow-editing="false" />
            <dx-column caption="품명" data-field="item.item_name" :allow-editing="false" />
            <dx-column caption="규격" data-field="item.item_standard" :allow-editing="false" />
            <dx-column caption="입고수량" data-field="quantity" data-type="number" format="fixedPoint" />
            <dx-column caption="Invoice 수량" data-field="export_comm_invoice_item.invoice_quantity" data-type="number" format="fixedPoint" :allow-editing="false" />
            <dx-column caption="미입고" data-field="export_comm_invoice_item.not_received" data-type="number" format="fixedPoint" :allow-editing="false" />
            <dx-column caption="단위" data-field="item.unit" :allow-editing="false" />
            <dx-column caption="단가" data-field="unit_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
            <dx-column caption="금액" data-field="supply_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :allow-editing="false" :calculate-cell-value="methods.calcSupplyPrice" />
            <dx-column data-field="warehouse_code" caption="입고창고">
              <dx-lookup value-expr="wh_code" display-expr="wh_name" :data-source="vars.dataSource.warehouse" />
            </dx-column>
            <dx-column caption="입고유형" data-field="correction_type">
              <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.dataSource.correctionType" />
            </dx-column>
            <dx-column caption="Invoice No" data-field="export_comm_invoice.invoice_number" width="180" :allow-editing="false" />
            <dx-column caption="프로젝트번호" data-field="project_management.project_number" :editor-options="{...generateItemButtonOption('search', methods.createFindPopupFn('project', '프로젝트조회'))}"
            :set-cell-value="methods.setProjectManagement" />
            <dx-column caption="참고" data-field="note" />
            <dx-column caption="자산구분" data-field="item.asset_type" />
            <dx-column caption="대분류" data-field="item.main_category" />
            <dx-column caption="중분류" data-field="item.middle_category" />
            <dx-column caption="소분류" data-field="item.sub_category" />
            <dx-column caption="재고보정 FK" data-field="fk_stock_correction_id" :visible="false" :show-in-column-chooser="false" />
            <dx-column caption="comm-invoice FK" data-field="fk_export_comm_invoice_id" :visible="false" :show-in-column-chooser="false" />
            <dx-column caption="comm-invoice-item FK" data-field="fk_export_comm_invoice_item_id" :visible="false" :show-in-column-chooser="false" />

            <dx-scrolling mode="standard" />
            <dx-column-chooser mode="select" :enabled="true" />
            <dx-editing mode="batch"
              :allow-adding="!vars.formState.readOnly"
              :allow-updating="!vars.formState.readOnly"
              :allow-deleting="!vars.formState.readOnly"
            />
          </dx-data-grid>
        </div>

        <div class="mt-2">
          <table class="summary-table">
            <tr>
              <th>공급가:</th>
              <td>{{ vars.summary.supply_price.value }}</td>
              <th>부가세:</th>
              <td>{{ vars.summary.vat.value }}</td>
              <th>합계금액:</th>
              <td>{{ vars.summary.total_price.value }}</td>
            </tr>
          </table>
        </div>
      </div>
    </div>

    <dx-popup
      title="사급자재찾기"
      content-template="popup-content"
      v-model:visible="vars.dlg.addCommInvoiceItem.show"
      width="70%"
      :height="500"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="(evt) => methods.onGridInitialized(evt, 'find-item-popup')"
    >
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ text: '선택된 항목 추가', icon: 'add', onClick: methods.addSelectedCommInvoiceRows }"
      />

      <template #popup-content>
        <dx-data-grid
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="vars.dataSource.commInvoiceItem"
          :on-initialized="(evt) => methods.onGridInitialized(evt, 'commInvoiceItem')"
        >
          <dx-column caption="Buyer" data-field="export_comm_invoice.client_company" />
          <dx-column caption="Invoice No" data-field="export_comm_invoice.invoice_number" :sort-index="1" sort-order="desc" />
          <dx-column caption="Invoice Date" data-field="export_comm_invoice.invoice_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="출고수량" data-field="invoice_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="미입고" data-field="not_received" data-type="number" format="fixedPoint" />

          <dx-paging :page-size="20" />
          <dx-sorting mode="multiple"/>
          <dx-filter-row :visible="true" />
          <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick" />
        </dx-data-grid>
      </template>
    </dx-popup>

    <dx-popup
      title="품목찾기"
      content-template="popup-content"
      v-model:visible="vars.dlg.addBaseItem.show"
      width="70%"
      :height="500"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'base-item-popup')"
    >
      <dx-toolbar-item  toolbar="top" location="after" widget="dxButton"
        :options="{text: '선택된 항목 추가', icon: 'add', onClick: methods.addSelectedRows}"
      />

      <template #popup-content>
        <dx-data-grid
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="vars.dataSource.baseItem"
          :on-initialized="evt => methods.onGridInitialized(evt, 'baseItem')"
        >
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item_name" />
          <dx-column caption="규격" data-field="item_standard" />
          <dx-column caption="고객사품번" data-field="client_item.client_item_code" />
          <dx-column caption="자산구분" data-field="asset_type" />
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" />

          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick" />
        </dx-data-grid>
      </template>
    </dx-popup>

    <dx-popup
      content-template="popup-content"
      v-model:visible="vars.dlg.finder.show"
      width="70%"
      :height="500"
      :key="vars.dlg.finder.key"
      :title="vars.dlg.finder.title"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'multiuse-popup')"
    >
      <template #popup-content>
        <data-stock-correction v-if="vars.dlg.finder.key === 'stock-correction'"
          @change="methods.finderReturnHandler"
        />
        <data-grid-project v-else-if="vars.dlg.finder.key === 'project'"
          @change="methods.finderReturnHandler"
        />
        <data-grid-client v-if="vars.dlg.finder.key === 'client'"
          @change="methods.finderReturnHandler"
        />
        <div v-else-if="vars.dlg.finder.key === 'etc'">
          <div class="mb-2">
            <dx-text-area :height="190" :value="vars.dlg.finder.data" @update:value="methods.updateEtcValue" />
          </div>
          <dx-toolbar>
            <dx-item toolbar="top" location="after" widget="dxButton" 
              :options="{text: '닫기', icon: null, onClick: methods.finderReturnHandler}" />
          </dx-toolbar>
        </div>
      </template>
    </dx-popup>

    <popup-item-detail v-model:visible="vars.itemDetail.visible" :item-id="vars.itemDetail.id" />
  </div>
</template>

<script>
import numeral from 'numeral';

import { useRouter } from 'vue-router';
import { onMounted, ref, reactive, computed, watch, nextTick } from 'vue';

import { DxButton } from 'devextreme-vue/button';
import DxTextArea from 'devextreme-vue/text-area';
import { confirm, alert } from 'devextreme/ui/dialog';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxRequiredRule } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxLookup, DxEditing, DxSorting, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, DxItem as DxGridItem, DxToolbar as DxGridToolbar } from 'devextreme-vue/data-grid';

import authService from '../../auth';
import stateStore from '@/utils/state-store';
import { notifyInfo, notifyError } from '../../utils/notify';
import { loadEmployee, loadWarehouse, loadDepartment } from '../../utils/data-loader';
import { sumSupplyPrice, calcPriceSummary, generateItemButtonOption, beforeExitConfirm, currentDateTime } from '../../utils/util';

import { getStock } from '../../data-source/setup';
import { shipmentOrderItem } from '../../data-source/shipment';
import { stockCorrection, getStockCorrectionItem } from '@/data-source/stock';
import { getCommInvoiceItem } from '../../data-source/export';
import { baseItem, baseClient, getBaseItem, baseCodeLoader } from '../../data-source/base';

import PopupItemDetail from '@/components/base/popup-item-detail';
import DataGridClient from '../../components/base/data-client.vue';
import DataGridProject from '../../components/project/data-project.vue';
import DataStockCorrection from '../../components/stock/data-stock-correction';

export default {
  components: {
    DxButton,
    DxTextArea,
    DxLoadPanel,
    DxToolbar, DxItem,
    DxPopup, DxToolbarItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxRequiredRule,
    DxDataGrid, DxColumn, DxPaging, DxLookup, DxEditing, DxSorting, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, DxGridItem, DxGridToolbar,
    PopupItemDetail, DataGridClient, DataGridProject, DataStockCorrection,
  },
  props: {
    id: [String, Number],
  },
  setup(props) {
    // variable 설정
    const router = useRouter();
    const vars = { dlg: {} };
    vars.init = ref(false);
    vars.loading = ref(false);
    vars.formState = reactive({ readOnly: true });
    vars.grid = { baseItem: null, item1: null };
    vars.dlg.addBaseItem = reactive({ show: false });
    vars.dlg.addCommInvoiceItem = reactive({ show: false });
    vars.dlg.finder = reactive({ show: false, title: '', key: null, data: null });
    vars.warehouseName = '';
    vars.filter = {};
    vars.filter.baseItem = { clientId: null, warehouseCode: null }
    vars.filter.commInvoiceItem = [{ name: 'not_received', op: 'gt', val: 0 }];
    vars.filter.item1 = [{ name: 'fk_stock_correction_id', op: 'eq', val: props.id || 0 }];
    vars.disabled = reactive({
      edit: true,
      new: false,
      delete: true,
      save: true,
      items: true,
      manager: true,
      clientManager: true,
      tradeYn: false,
    });
    vars.dataSource = reactive({
      payment_terms: [],
      type: [],
      correctionType: [],
      vat_type: [],
      department: [],
      employee: [],
      warehouse: [],
      baseItem: null,
      commInvoiceItem: getCommInvoiceItem(vars.filter.commInvoiceItem),
    });

    vars.focus = reactive({ item1: null });
    vars.formData = reactive({});
    vars.summary = {};
    vars.summary.supply_price = computed(() => '₩' + numeral(vars.formData.supply_price).format('0,0'));
    vars.summary.vat = computed(() => '₩' + numeral(vars.formData.vat).format('0,0'));
    vars.summary.total_price = computed(() => '₩' + numeral(vars.formData.total_price).format('0,0'));
    vars.stockCorrectionItem = getStockCorrectionItem(vars.filter.item1);
    vars.itemDetail = reactive({ visible: false, id: 0 });

    onMounted(async () => {
      await methods.loadBaseCode();
      await loadDepartment(vars.dataSource);
      await loadWarehouse(vars.dataSource);
      methods.initById(props.id);
    });

    // public methods
    const methods = {
      async initById(id) {
        if (id) {
          vars.filter.item1[0].val = id;
        } else {
          vars.filter.item1[0].val = 0;
        }
        vars.stockCorrectionItem.defaultFilters = vars.filter.item1;
        if (vars.grid.item1) vars.grid.item1.refresh();

        beforeExitConfirm.check(() => !vars.disabled.save)
        if (!id) {
          vars.formData.id = null;
          vars.formData.number = '';
          vars.formData.target_date = '';
          vars.formData.department = '';
          vars.formData.manager = '';
          vars.formData.note = '';
          vars.formData.etc = '';
          vars.formData.fk_company_id = authService.getCompanyId();

          vars.disabled.edit = true;
          vars.disabled.delete = true;
          vars.disabled.save = true;
          vars.disabled.items = true;
          vars.disabled.manager = true;
          vars.disabled.clientManager = true;
          return;
        }

        let { data } = await stockCorrection.byKey(id);
        Object.assign(vars.formData, data);

        methods.enableDelete();
        vars.disabled.edit = false;
        if (vars.formData.department) {
          methods.enableSave();
          vars.disabled.items = false;
        }
      },
      async addSelectedRows() {
        const grid = vars.grid.item1;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        const rows = await vars.grid.baseItem.getSelectedRowsData();
        for (let row of rows) {
          const basicStock = row.basic_stock ? { ...row.basic_stock } : { current_stock: 0, available_stock: 0 };

          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));

          data.item_code = row.item_code; // 품목코드
          data.item = { ...row }; // 품목
          data.quantity = 0; // 수량
          data.unit_price = row.purchase_price; // 단가
          data.basic_stock = { ...basicStock }; // 기초재고
          data.warehouse_code = vars.filter.baseItem.warehouseCode; // 창고코드
          data.type = methods.getFirstType(); // 입고구분
          data.correction_type = methods.getFirstCorrectionType(); // 입고유형
          data.export_comm_invoice = null;
          data.export_comm_invoice_item = null;
          data.fk_export_comm_invoice_id = null; // comm-invoice id
          data.fk_export_comm_invoice_item_id = null; // comm-invoice-item id
        }
        grid.refresh();
        vars.dlg.addBaseItem.show = false;
      },
      async addSelectedCommInvoiceRows() {
        const grid = vars.grid.item1;
        const rows = await vars.grid.commInvoiceItem.getSelectedRowsData();
        for (let row of rows) {
          const basicStock = row.basic_stock ? { ...row.basic_stock } : { current_stock: 0, available_stock: 0 };

          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));

          data.item_code = row.item_code; // 품목코드
          data.item = { ...row.item }; // 품목
          data.quantity = row.not_received; // 수량
          data.unit_price = row.unit_price; // 단가
          data.basic_stock = { ...basicStock }; // 기초재고
          data.warehouse_code = vars.filter.baseItem.warehouseCode; // 창고코드
          data.type = methods.getFirstType(); // 입고구분
          data.correction_type = methods.getFirstCorrectionType(); // 입고유형
          data.export_comm_invoice = { ...row.export_comm_invoice };
          data.export_comm_invoice_item = { ...row };
          data.fk_export_comm_invoice_id = row.export_comm_invoice.id; // comm-invoice id
          data.fk_export_comm_invoice_item_id = row.id; // comm-invoice-item id
        }
        grid.refresh();
        vars.dlg.addCommInvoiceItem.show = false;
      },
      getFirstType() {
        return methods.getFirstItemName(vars.dataSource.type);
      },
      getFirstCorrectionType() {
        return methods.getFirstItemName(vars.dataSource.correctionType);
      },
      getFirstItemName(itemList) {
        if (!itemList || itemList.length <= 0) {
          return '';
        } else {
          return itemList[0].code_name;
        }
      },
      generateItemSelectOption(items = [], value = '', searchEnabled = false) {
        return { value, searchEnabled, items };
      },
      createFindPopupFn(key, title, data = null) {
        const _key = key,
          _title = title,
          _data = data;
        return () => {
          vars.dlg.finder.key = _key;
          vars.dlg.finder.data = _data;
          vars.dlg.finder.title = _title;
          vars.dlg.finder.show = true;
        };
      },
      showAddPopup() {
        if (vars.grid.baseItem) {
          vars.grid.baseItem.clearSelection();
          vars.grid.baseItem.clearFilter();
          vars.grid.baseItem.refresh();
        }
        vars.dlg.addBaseItem.show = true;
      },
      showAddCommInvoiceItemPopup() {
        const notContains = [];
        for (const item of vars.grid.item1.getVisibleRows()) {
          if (!item.id && item.data.fk_export_comm_invoice_item_id) {
            notContains.push(['id', '<>', item.data.fk_export_comm_invoice_item_id], 'and');
          }
        }
        notContains.pop();

        if (vars.grid.commInvoiceItem) {
          vars.grid.commInvoiceItem.filter(notContains);
          vars.grid.commInvoiceItem.clearSelection();
          vars.grid.commInvoiceItem.refresh();
        }
        vars.dlg.addCommInvoiceItem.show = true;
      },
      setProjectManagement(newData, value, currentRowData){
        if(!value) return;
        newData.project_management = value;
        newData.fk_project_management_id = value.id;
      },
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(key, evt.component);
      },
      async newItem() {
        if (vars.grid.item1) {
          vars.filter.item1[0].val = 0;
          vars.stockCorrectionItem.defaultFilters = vars.filter.item1;
          vars.grid.item1.refresh();
        }
        if (vars.formData.id) {
          router.replace('/stock/stock-correction');
          vars.formData.id = null;
        }
        setTimeout(() => {
          vars.formData.target_date = currentDateTime();
          vars.formData.department = authService.getDepartmentName();
          vars.formData.manager = authService.getUserName();
          vars.formData.fk_company_id = authService.getCompanyId();

          vars.formState.readOnly = false;
        }, 200);
      },
      async editItem() {
        if (!vars.formData.id) return;
        if (vars.formState.readOnly) {
          let isSelect = await confirm('수정하시겠습니까?', '수정');
          if (!isSelect) {
            return;
          }
        }

        const saveFormData = Object.assign({}, vars.formData);
        vars.formState.readOnly = !vars.formState.readOnly;

        methods.enableSave();
        methods.enableDelete();

        await nextTick();
        Object.assign(vars.formData, saveFormData);
      },
      async deleteItem() {
        const result = await confirm(
          '이 항목을 삭제하시겠습니까?',
          '삭제 확인'
        );
        if (result) {
          try {
            await stockCorrection.remove(vars.formData.id);
            beforeExitConfirm.clear()
            await alert('삭제되었습니다', '삭제 확인');
            router.replace({ path: '/stock/stock-correction' });
            vars.formState.readOnly = true;
          } catch (ex) {
            if (ex.response.status != 403) {
              await alert(
                '연결된 데이터가 있어서 삭제가 안됩니다',
                '삭제 확인'
              );
            }
          }
        }
      },
      async saveItem() {
        vars.loading.value = true;
        try {
          if (vars.formData.id) {
            // 기존 정보 업데이트
            const updateValues = Object.assign({}, vars.formData);
            delete updateValues.id;
            delete updateValues.total_price;
            delete updateValues.supply_price;
            delete updateValues.vat;

            await stockCorrection.update(vars.formData.id, updateValues);
            if (vars.grid.item1) await vars.grid.item1.saveEditData();

            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');

            methods.enableSave();
            methods.enableDelete();
          } else {
            // 채번이 없을 경우 자동 채번
            const updateValues = Object.assign({}, vars.formData);
            delete updateValues.id;
            delete updateValues.total_price;
            delete updateValues.supply_price;
            delete updateValues.vat;

            let { data } = await stockCorrection.insert(updateValues);
            vars.formData.id = data.id;

            const gridItem1 = vars.grid.item1;
            if (gridItem1 && gridItem1.hasEditData()) {
              await gridItem1.saveEditData();
            }
            beforeExitConfirm.clear()
            router.replace({ path: `/stock/stock-correction/${data.id}` });
            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');
          }
        } catch (ex) {
          if (ex.response.status === 602) {
            notifyError('이미 존재하는 재고보정번호 입니다');
          } else {
            console.error(ex);
            notifyError('저장 할 내용이 없습니다');
          }
        } finally {
          vars.loading.value = false;
        }
      },
      finderReturnHandler(data) {
        switch (vars.dlg.finder.key) {
          case 'stock-correction': {
            router.replace({ path: `/stock/stock-correction/${data.id}` });
            vars.formState.readOnly = true;
            break;
          }
          case 'project': {
            vars.grid.item1.cellValue(
              vars.focus.item1.rowIndex,
              vars.focus.item1.columnIndex,
              data
            );
            break;
          }
          case 'etc': {
            vars.formData.etc = vars.dlg.finder.data;
            break;
          }
        }

        vars.dlg.finder.show = false;
        vars.dlg.finder.title = '';
        vars.dlg.finder.key = null;
        vars.dlg.finder.data = null;
      },
      updateEtcValue(v) {
        vars.dlg.finder.data = v;
      },
      onDepartmentChanged(e) {
        if (!e.value) {
          vars.disabled.save = true;
          vars.disabled.items = true;
          vars.disabled.manager = true;
          vars.formData.manager = null;
          vars.dataSource.employee = [];
        } else {
          const selectItem = e.component.option('selectedItem');
          if (selectItem) {
            loadEmployee(vars.dataSource, selectItem.id);
            vars.disabled.manager = false;
          }
        }
        methods.checkPossibleSave();

        const selectItem = e.component.option('selectedItem');
        vars.warehouseName = selectItem ? selectItem.warehouse.wh_name : '';
        vars.filter.baseItem.warehouseCode = selectItem
          ? selectItem.wh_code
          : null;
        methods.loadBaseItem();
      },
      onFocusedCellChanged(e) {
        vars.focus.item1 = e;
      },
      onSavingItem(e) {
        e.changes.forEach(element => {
          if (element.type != 'remove') {
            element.data.fk_stock_correction_id = vars.formData.id;
            delete element.data.item;
            delete element.data.basic_stock;
            delete element.data.warehouse;
            delete element.data.export_comm_invoice;
            delete element.data.export_comm_invoice_item;
          }
        });
      },
      onDataError(e) {
        if (e.error.response.status == 403) {
          e.error.message = '권한이 없습니다';
        } else if (e.error.response.status == 605) {
          e.error.message = '연결된 데이터가 있어서 삭제가 안됩니다';
        } else if (e.error.response.status == 606) {
          e.error.message = '현재고가 부족합니다';
        }
      },
      async setWarehouse(newData, value, currentRowData) {
        const warehouseList = vars.dataSource.warehouse;
        for (let i = 0; i < warehouseList.length; i++) {
          if (warehouseList[i].wh_name == value) {
            newData.warehouse = {};
            Object.assign(newData.warehouse, warehouseList[i]);
            newData.warehouse_code = warehouseList[i].wh_code;

            const { basicStock } = await getStock(
              currentRowData.item_code,
              newData.warehouse_code
            );
            newData.basic_stock = {
              current_stock: basicStock.current_stock,
              available_stock: basicStock.available_stock,
            };
            break;
          }
        }
      },
      setQuantity(newData, value, currentRowData) {
        newData.quantity = value;
        newData.unit_price = currentRowData.unit_price;
      },
      setUnitPrice(newData, value, currentRowData) {
        newData.quantity = currentRowData.quantity;
        newData.unit_price = value;
      },
      calcSupplyPrice(rowData) {
        let supply_price = 0;
        if (rowData.quantity && rowData.unit_price) {
          supply_price = rowData.quantity * rowData.unit_price;
        }
        rowData.supply_price = supply_price;
        methods.calcSummary();
        return supply_price;
      },
      calcSummary() {
        let total = sumSupplyPrice(vars.grid.item1, 'quantity', 'unit_price');

        const response = calcPriceSummary(vars.formData.vat_type, total);
        vars.formData.supply_price = response.supply_price;
        vars.formData.vat = response.vat;
        vars.formData.total_price = response.total_price;
      },
      loadBaseCode() {
        return baseCodeLoader([
          '부가세구분',
          '입고구분',
          '입고유형',
          '결재조건',
        ])
          .then(response => {
            vars.dataSource.payment_terms = response['결재조건'];
            vars.dataSource.type = response['입고구분'];
            vars.dataSource.correctionType = response['입고유형'];
            vars.dataSource.vat_type = response['부가세구분'];
          })
          .then(() => (vars.init.value = true));
      },
      loadBaseItem() {
        vars.dataSource.baseItem = getBaseItem(
          null,
          vars.filter.baseItem.clientId,
          vars.filter.baseItem.warehouseCode
        );
      },
      checkPossibleSave() {
        if (vars.formData.department) {
          methods.enableSave();
          vars.disabled.items = false;
        }
      },
      itemPopupClick({ column, data }) {
        if (column.name === 'item_code') {
          vars.itemDetail.id = data.item.id;
          vars.itemDetail.visible = true;
        }
      },
      enableDelete() {
        if (vars.formState.readOnly) {
          vars.disabled.delete = true;
        } else {
          vars.disabled.delete = false;
        }
      },
      enableSave() {
        if (vars.formState.readOnly) {
          vars.disabled.save = true;
        } else {
          vars.disabled.save = false;
        }
      },
    };

    watch(
      () => props.id,
      () => methods.initById(props.id)
    );

    return {
      vars,
      methods,
      baseItem,
      baseClient,
      shipmentOrderItem,
      generateItemButtonOption,
    };
  },
};
</script>
