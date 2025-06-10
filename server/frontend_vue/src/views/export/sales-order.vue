<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">Sales Order</div>
            </dx-item>

            <dx-item widget="dxButton" location="after" locate-in-menu="auto"
              :options="{ text: '신규', type: 'add', icon: 'add', disabled: vars.disabled.new, onClick: methods.newItem }"
            />
            <dx-item widget="dxButton" location="after" locate-in-menu="auto"
              :options="{ text: '수정', type: 'rename', icon: 'rename', disabled: vars.disabled.edit, onClick: methods.editItem }"
            />
            <dx-item widget="dxButton" location="after" locate-in-menu="auto"
              :options="{ text: '삭제', type: 'remove', icon: 'remove', disabled: vars.disabled.delete, onClick: methods.deleteItem }"
            />
            <dx-item widget="dxButton" location="after" locate-in-menu="auto"
              :options="{ text: '저장', type: 'save', icon: 'save', disabled: vars.disabled.save, onClick: methods.saveItem }"
            />
            <dx-item widget="dxButton" location="after" locate-in-menu="auto"
              :options="{ text: '수주복사', icon: 'copy', disabled: vars.disabled.edit, onClick: methods.copyItem }"
            />
          </dx-toolbar>
        </div>

        <dx-form :form-data="vars.formData">
          <dx-group-item :col-count="5">
            <dx-group-item>
              <dx-simple-item data-field="order_number"
                :editor-options="{
                  placeholder: '(자동 or 직접입력)',
                  ...generateItemButtonOption('search', methods.createFindPopupFn('order', '수출수주조회')),
                }"
              >
                <dx-label text="OrderNo" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="order_date" editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  ...vars.formState,
                }"
              >
                <dx-label text="OrderDate" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="client_company"
                :editor-options="{
                  onEnterKey: methods.createFindPopupFn('client', '업체조회', {
                    name: vars.formData.client_company,
                  }),
                  ...generateItemButtonOption('search', methods.createFindPopupFn('client', '업체조회', {
                      name: vars.formData.client_company,
                    })
                  ),
                  ...vars.formState,
                }"
              >
                <dx-label text="Buyer" :show-colon="false" />
                <dx-required-rule message="고객업체를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="client_manager" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'name',
                  acceptCustomValue: true,
                  disabled: vars.disabled.clientManager,
                  displayExpr: methods.clientManagerExpr,
                  dataSource: vars.dataSource.client_manager,
                  ...vars.formState,
                }"
              >
                <dx-label text="BuyerContact" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="payment_terms" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  acceptCustomValue: true,
                  dataSource: vars.dataSource.payment_terms,
                  ...vars.formState,
                }"
              >
                <dx-label text="Pay Terms" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="vat_type" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  acceptCustomValue: true,
                  dataSource: vars.dataSource.vat_type,
                  ...vars.formState,
                }"
              >
                <dx-label text="Price Terms" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="order_department" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'department_name',
                  displayExpr: 'department_name',
                  acceptCustomValue: true,
                  dataSource: vars.dataSource.department,
                  onValueChanged: methods.onDepartmentChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="OwnerDept" :show-colon="false" />
                <dx-required-rule message="수주부서를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="order_manager" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'emp_name',
                  displayExpr: 'emp_name',
                  disabled: vars.disabled.manager,
                  dataSource: vars.dataSource.employee,
                  ...vars.formState,
                }"
              >
                <dx-label text="member" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="origin" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  acceptCustomValue: true,
                  dataSource: vars.dataSource.origin,
                  ...vars.formState,
                }"
              >
                <dx-label text="Origin" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="ship_port" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  acceptCustomValue: true,
                  dataSource: vars.dataSource.ship_port,
                  ...vars.formState,
                }"
              >
                <dx-label text="Ship Port" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="currency" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  acceptCustomValue: true,
                  dataSource: vars.dataSource.currency,
                  ...vars.formState,
                }"
              >
                <dx-label text="Currency" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="exrate" editor-type="dxNumberBox" 
                :editor-options="{ format: '#0.00', ...vars.formState }"
              >
                <dx-label text="ExRate" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="order_type" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  dataSource: vars.dataSource.order_type,
                  ...vars.formState,
                }"
              >
                <dx-label text="수주구분" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="confirmed" editor-type="dxCheckBox"
                :editor-options="{ onValueChanged: methods.onConfirmChanged }"
              >
                <dx-label text="수주확정" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="etc" editor-type="dxTextArea"
                :editor-options="{
                  height: '170px',
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
        <dx-tab-panel :animation-enabled="false" :swipe-enabled="false">
          <dx-item title="수주내역">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 516px)"
                  date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                  column-resizing-mode="widget"
                  :show-borders="true"
                  :remote-operations="false"
                  :column-auto-width="true"
                  :focused-row-enabled="true"
                  :allow-column-resizing="true"
                  :row-alternation-enabled="true"
                  :allow-column-reordering="true"
                  :select-text-on-edit-start="true"
                  :data-source="vars.dataSource.item1"
                  :on-initialized="(evt) => methods.onGridInitialized(evt, 'item1')"
                  @cell-dbl-click="methods.itemPopupClick"
                  @data-error-occurred="methods.onDataError"
                  @focused-cell-changed="methods.onFocusedCellChanged"
                >
                  <dx-grid-toolbar>
                    <dx-item template="exportToRelease" location="before" :visible="vars.formData.confirmed" />
                    <dx-item template="calcAvailStock" location="before" :visible="!vars.formState.readOnly" />
                    <dx-item template="downloadSample" location="after" :visible="!vars.formState.readOnly" />
                    <dx-item template="importItem" location="after" :visible="!vars.formState.readOnly" />
                    <dx-grid-item name="addRowButton" :options="{ onClick: methods.showAddPopup }" />
                    <!-- <dx-grid-item name="saveButton" :visible="!!vars.formData.id" /> -->
                    <dx-grid-item name="revertButton" />
                    <dx-grid-item name="columnChooserButton" />
                  </dx-grid-toolbar>
                  <template #exportToRelease>
                    <dx-button text="출고로 보내기" icon="export" @click="methods.exportToRelease" />
                  </template>
                  <template #calcAvailStock>
                    <dx-button text="할당수량 재계산" icon="formula" @click="methods.calculateAssignQuantity" />
                  </template>
                  <template #downloadSample>
                    <dx-button text="엑셀샘플" icon="arrowdown" @click="methods.downloadSampleFile" />
                  </template>
                  <template #importItem>
                    <dx-button text="엑셀업로드" icon="xlsxfile" @click="methods.importExcelData" />
                  </template>

                  <dx-column caption="ItemCode" data-field="item_code" width="180" :allow-editing="false" />
                  <dx-column caption="ItemName" data-field="item.item_name" :allow-editing="false" />
                  <dx-column caption="SubName" data-field="item.item_standard" :allow-editing="false" />
                  <dx-column caption="Qty" data-field="order_quantity" data-type="number" format="fixedPoint" :set-cell-value="methods.setQuantity" />
                  <dx-column caption="Unit" data-field="item.unit" :allow-editing="false" />
                  <dx-column caption="ExportPrice" data-field="unit_price" data-type="number" :format="{ type: 'fixedPoint', precision: 4 }" :set-cell-value="methods.setUnitPrice" />
                  <dx-column caption="Amount" data-field="supply_price" data-type="number" :format="{ type: 'fixedPoint', precision: 4 }" :allow-editing="false" />
                  <dx-column caption="ReqDate" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
                  <dx-column caption="ConDate" data-field="contact_delivery_date" data-type="date" format="yyyy-MM-dd" />
                  <dx-column caption="LOT NO(생산주차)" data-field="lot" />
                  <dx-column caption="출고창고" data-field="warehouse.wh_name" :set-cell-value="methods.setWarehouse">
                    <dx-lookup value-expr="wh_name" display-expr="wh_name" :data-source="vars.dataSource.warehouse" />
                  </dx-column>
                  <dx-column caption="Description" data-field="item.item_detail" :allow-editing="false" />
                  <dx-column caption="할당수량" data-field="assign_quantity" data-type="number" format="fixedPoint" :allow-editing="false" />
                  <dx-column caption="미선적량" data-field="not_shipped" data-type="number" format="fixedPoint" :allow-editing="false" />
                  <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :allow-editing="false" :calculate-display-value="methods.availableStock" />
                  <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :allow-editing="false" :calculate-display-value="methods.currentStock" />
                  <dx-column caption="수주아이디" data-field="fk_export_sales_order_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
                  <dx-column caption="창고코드" data-field="warehouse_code" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
                  <dx-summary :recalculate-while-editing="true" :calculate-custom-summary="methods.calculateCustomSummary">
                    <dx-total-item name="supply_price" summary-type="custom" />
                  </dx-summary>

                  <dx-scrolling mode="standard" />
                  <dx-column-chooser mode="select" :enabled="true" />
                  <dx-editing mode="batch"
                    :allow-adding="!vars.formState.readOnly"
                    :allow-updating="!vars.formState.readOnly && !vars.formData.confirmed"
                    :allow-deleting="!vars.formState.readOnly"
                  />
                </dx-data-grid>
              </div>
            </template>
          </dx-item>
        </dx-tab-panel>

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
      title="품목찾기"
      content-template="popup-content"
      v-model:visible="vars.dlg.addItem.show"
      :width="680"
      :height="500"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="(evt) => methods.onGridInitialized(evt, 'find-item2-popup')"
    >
      <dx-toolbar-item
        widget="dxButton"
        toolbar="top"
        location="after"
        :options="{ text: '선택된 항목 추가', icon: 'add', onClick: methods.addSelectedRows }"
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
          :on-initialized="(evt) => methods.onGridInitialized(evt, 'baseItem')"
        >
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item_name" />
          <dx-column caption="규격" data-field="item_standard" />
          <dx-column caption="고객사품번" data-field="client_item.client_item_code" />
          <dx-column caption="자산구분" data-field="asset_type" />
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :allow-sorting="false" :calculate-display-value="methods.availableStock" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint"  :allow-sorting="false" :calculate-display-value="methods.currentStock"/>

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
      :resize-enabled="true"
      :close-on-outside-click="true"
      :key="vars.dlg.finder.key"
      :title="vars.dlg.finder.title"
      @initialized="(evt) => methods.onGridInitialized(evt, 'multiuse-popup')"
    >
      <template #popup-content>
        <data-grid-client v-if="vars.dlg.finder.key === 'client'"  :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-client v-else-if="vars.dlg.finder.key === 'enduser'"  :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-order v-else-if="vars.dlg.finder.key === 'order'" @change="methods.finderReturnHandler" />
        <div v-else-if="vars.dlg.finder.key === 'etc'">
          <div class="mb-2">
            <dx-text-area :height="190" :value="vars.dlg.finder.data" @update:value="methods.updateEtcValue" />
          </div>
          <dx-toolbar>
            <dx-item widget="dxButton" toolbar="top" location="after"
              :options="{ text: '닫기', icon: null, onClick: methods.finderReturnHandler }"
            />
          </dx-toolbar>
        </div>
      </template>
    </dx-popup>

    <popup-item-detail v-model:visible="vars.itemDetail.visible" :item-id="vars.itemDetail.id" />

    <input hidden
      type="file"
      ref="excelRef"
      accept=".xlsx,.xls"
      @change="methods.excelFileChange"
    />
  </div>
</template>

<script>
import moment from 'moment';
import numeral from 'numeral';

import { onMounted, ref, reactive, computed, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';

import { DxButton } from 'devextreme-vue/button';
import DxTextArea from 'devextreme-vue/text-area';
import { confirm, alert } from 'devextreme/ui/dialog';
import { DxTabPanel } from 'devextreme-vue/tab-panel';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxCustomRule, DxRequiredRule } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxLookup, DxEditing, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser,
  DxItem as DxGridItem, DxToolbar as DxGridToolbar, DxButton as DxGridButton } from 'devextreme-vue/data-grid';

import { getStock } from '../../data-source/setup';
import { baseClient, getBaseItem, baseCodeLoader } from '../../data-source/base';

import PopupItemDetail from '@/components/base/popup-item-detail';
import DataGridClient from '../../components/base/data-client.vue';
import { getSalesOrderItem, salesOrder, salesOrderItem } from '../../data-source/export';
import DataGridOrder from '../../components/export/data-sales-order.vue';

import authService from '../../auth';
import stateStore from '@/utils/state-store';
import ApiService from '../../utils/api-service';
import { notifyInfo, notifyError } from '../../utils/notify';
import { loadEmployee, loadWarehouse, loadDepartment, loadClientManager } from '../../utils/data-loader';
import { calcPriceSummary, generateItemButtonOption, beforeExitConfirm, currentDateTime } from '../../utils/util';

import { saveAs } from 'file-saver';

export default {
  components: {
    DxButton,
    DxTextArea,
    DxTabPanel,
    DxLoadPanel,
    DxToolbar, DxItem,
    DxPopup, DxToolbarItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxCustomRule, DxRequiredRule,
    DxDataGrid, DxColumn, DxPaging, DxLookup, DxEditing, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser,
    DxGridItem, DxGridToolbar, DxGridButton,
    DataGridOrder, DataGridClient, PopupItemDetail,
  },
  props: {
    id: [String, Number],
  },
  setup(props) {
    // variable 설정
    const router = useRouter();
    const vars = {};
    vars.init = ref(false);
    vars.loading = ref(false);
    vars.formData = reactive({});
    vars.formState = reactive({ readOnly: true });
    vars.grid = {};
    vars.dlg = {};
    vars.dlg.addItem = reactive({ show: false });

    const excelRef = ref()

    vars.dlg.finder = reactive({
      title: '',
      key: null,
      data: null,
      show: false,
    });
    vars.api = {};
    vars.api.updateAssignQuantity = new ApiService('/api/mes/v1/export-update-assign-quantity');
    vars.api.exportToRelease = new ApiService('/api/mes/v1/shipment/order/export/release');
    vars.warehouse = {};
    vars.focus = {};
    vars.focus.item1 = null;
    vars.filter = {};
    vars.filter.baseItem = { clientId: null };
    vars.filter.item1 = [{ name: 'fk_export_sales_order_id', op: 'eq', val: props.id || 0 }];
    vars.disabled = reactive({
      new: false,
      edit: true,
      save: true,
      delete: true,
      manager: true,
      tradeYn: false,
      clientManager: true,
    });
    vars.dataSource = reactive({
      employee: [],
      department: [],
      order_type: [],
      payment_terms: [],
      vat_type: [],
      origin: [],
      ship_port: [],
      currency: [],
      client_manager: [],
      baseItem: null,
      item1: getSalesOrderItem(vars.filter.item1),
    });
    vars.itemDetail = reactive({ visible: false, id: 0 });

    vars.summary = {};
    vars.summary.supply_price = computed(() => numeral(vars.formData.supply_price).format('0,0'));
    vars.summary.vat = computed(() => numeral(vars.formData.vat).format('0,0'));
    vars.summary.total_price = computed(() => numeral(vars.formData.total_price).format('0,0'));

    onMounted(async () => {
      await loadDepartment(vars.dataSource);
      await methods.loadBaseCode();
      methods.initById(props.id);
      loadWarehouse(vars.dataSource);
    });

    // public methods
    const methods = {
      async initById(id) {
        beforeExitConfirm.check(() => !vars.disabled.save);
        methods.gridItem1Refresh(id);
        if (!id) {
          methods.clearFormData();
          methods.disableAllAction();
          return;
        }

        await methods.loadOrderData(id);

        methods.syncStatusDelete();
        vars.disabled.edit = false;
        if (methods.isFilledFormRequiredData()) {
          methods.syncStatusSave();
        }
        if (methods.isOrderConfirmed()) {
          methods.disableAllAction();
        }
        methods.onClientChanged();
      },
      async loadOrderData(id) {
        let { data } = await salesOrder.byKey(id);
        Object.assign(vars.formData, data);
      },
      clearFormData() {
        vars.formData.id = null;
        vars.formData.created = null;
        vars.formData.order_number = '';
        vars.formData.order_date = '';
        vars.formData.client_company = ''; // buyer
        vars.formData.client_manager = ''; // buyer_conteact
        vars.formData.order_department = ''; // owner_dept
        vars.formData.order_manager = ''; // member
        vars.formData.order_type = '';
        vars.formData.payment_terms = ''; // pay_terms
        vars.formData.vat_type = ''; // price_terms
        vars.formData.origin = '';
        vars.formData.ship_port = '';
        vars.formData.currency = '';
        vars.formData.exrate = 0;
        // vars.formData.delivery_date = ''; //
        vars.formData.etc = ''; // remark
        vars.formData.supply_price = 0; // amount
        vars.formData.vat = 0;
        vars.formData.total_price = 0;
        vars.formData.confirmed = false;
        vars.formData.fk_company_id = authService.getCompanyId();
      },
      async addSelectedRows() {
        const grid = vars.grid.item1;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        const rows = await vars.grid.baseItem.getSelectedRowsData().reverse();
        for (let row of rows) {
          const basicStock = row.basic_stock
            ? { ...row.basic_stock }
            : { current_stock: 0, available_stock: 0 };

          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code; // 품목코드
          data.item = { ...row }; // 품목
          data.supply_price = 0; // 공급가
          data.order_quantity = 0; // 수주수량
          data.assign_quantity = 0; // 할당수량
          data.not_shipped = 0; // 미출고
          data.unit_price = row.purchase_price; // 단가
          data.request_delivery_date = null; // 요청납기
          data.contact_delivery_date = null; // 요청납기
          data.basic_stock = { ...basicStock }; // 기초재고
          data.warehouse = { ...vars.warehouse }; // 출고창고
          data.warehouse_code = vars.warehouse.wh_code; // 창고코드
          data.fk_export_sales_order_id = vars.formData.id; // 수주 아이디
        }
        grid.refresh();
        vars.dlg.addItem.show = false;
      },
      createFindPopupFn(key, title, data = null) {
        const _key = key, _title = title, _data = data;
        return () => {
          vars.dlg.finder.key = _key;
          vars.dlg.finder.data = _data;
          vars.dlg.finder.title = _title;
          vars.dlg.finder.show = true;
        };
      },
      gridClearAndRefresh(grid) {
        if (grid) {
          grid.clearSelection();
          grid.clearFilter();
          grid.refresh();
        }
      },
      showAddPopup() {
        methods.gridClearAndRefresh(vars.grid.baseItem);
        vars.dlg.addItem.show = true;
      },
      async postUpdateAssignQuantity(orderItemId, itemCode, warehouseCode) {
        /// 여기 부터
        const params = {
          order_item_id: orderItemId,
          item_code: itemCode,
          warehouse: warehouseCode,
        };
        await vars.api.updateAssignQuantity.post('', params);
      },
      async calculateAssignQuantity() {
        const rows = vars.grid.item1.getVisibleRows();
        for (const row of rows) {
          if (row.data.id) {
            await methods.postUpdateAssignQuantity(
              row.data.id,
              row.data.item_code,
              row.data.warehouse_code
            );
          }
        }
        vars.grid.item1.refresh();
      },
      async gridItem1Refresh(id) {
        vars.dataSource.item1.defaultFilters = methods.setIdToGridFilter(
          vars.filter.item1,
          id
        );
        methods.gridRefresh(vars.grid.item1);
      },
      setIdToGridFilter(filter, id) {
        if (!id) {
          id = 0;
        }
        filter[0].val = id;
        return filter;
      },
      gridRefresh(grid) {
        if (grid) {
          grid.cancelEditData();
          grid.refresh();
        }
      },
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`export-sales-order-${key}`, evt.component);
      },
      async newItem() {
        methods.gridItem1Refresh();
        if (vars.formData.id) {
          methods.clearFormData();
          methods.redirect();
        }
        setTimeout(() => {
          methods.clearFormData();
          vars.formData.order_date = currentDateTime();
          vars.formData.order_department = authService.getDepartmentName();
          vars.formData.order_manager = authService.getUserName();
          vars.formData.order_type = methods.getFirstOrderType();
          vars.formData.payment_terms = methods.getFirstPaymentTerms();
          vars.formData.vat_type = methods.getFirstVatType();
          vars.formData.origin = methods.getFirstOrigin();
          vars.formData.ship_port = methods.getFirstShipPort();
          vars.formData.currency = methods.getFirstCuurrency();
          vars.formData.fk_company_id = authService.getCompanyId();
          vars.formState.readOnly = false;
        }, 200);
      },
      async editItem() {
        if (!vars.formData.id) {
          return;
        }
        if (methods.isFormReadOnly() && methods.isOrderConfirmed()) {
          return;
        }
        if (methods.isFormReadOnly()) {
          let isSelect = await confirm('수정하시겠습니까?', '수정');
          if (!isSelect) {
            return;
          }
        }

        const saveFormData = Object.assign({}, vars.formData);
        vars.formState.readOnly = !vars.formState.readOnly;

        methods.syncStatusDelete();
        methods.syncStatusSave();

        await nextTick();
        Object.assign(vars.formData, saveFormData);
      },
      async deleteItem() {
        const result = await confirm('이 항목을 삭제하시겠습니까?', '삭제 확인');
        if (result) {
          try {
            await salesOrder.remove(vars.formData.id);
            beforeExitConfirm.clear()
            await alert('삭제되었습니다', '삭제 확인');
            methods.redirect();
            vars.formState.readOnly = true;
          } catch (ex) {
            if (ex.response.status != 403) {
              await alert('연결된 데이터가 있어서 삭제가 안됩니다', '삭제 확인');
            }
          }
        }
      },
      async saveItem() {
        methods.showLoading();
        try {
          if (vars.formData.id) {
            // 기존 정보 업데이트
            const updateDate = Object.assign({}, vars.formData);
            delete updateDate.created;
            delete updateDate.order_number;
            const { data } = await salesOrder.update(
              vars.formData.id,
              updateDate
            );
            vars.formData.order_number = data.order_number;
            await methods.saveItem1();

            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');

            methods.syncStatusSave();
            methods.syncStatusDelete();
          } else {
            // 채번이 없을 경우 자동 채번
            if (vars.formData.created) vars.formData.created = null;
            let { data } = await salesOrder.insert(vars.formData);
            vars.formData.id = data.id;

            await methods.saveItem1();

            beforeExitConfirm.clear()
            methods.redirect(data.id);
            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');
          }
        } catch (ex) {
          console.log("ex : ", ex.response.status)
          if (ex.response.status == 602) {
            notifyError('이미 존재하는 번호 입니다');
          } else if(ex.response.status == 400){
            notifyError('연결된 데이터가 있어서 삭제가 안됩니다')
          }else{
            console.error(ex);
            notifyError('저장 할 내용이 없습니다');
          }
        } finally {
          methods.hideLoading();
        }
      },
      async saveItem1() {
        await methods.saveGrid(vars.grid.item1);
      },
      async saveGrid(grid) {

        if (grid && grid.hasEditData()) {
      
          const data = [...grid.option("editing.changes")].reverse();
   

          for (let item of data){
            if(item.type == 'insert'){
              item.data.fk_export_sales_order_id = vars.formData.id;
              delete item.data.item;
              delete item.data.warehouse;
              delete item.data.basic_stock;
              await salesOrderItem.insert(item.data)

            }else if(item.type  == 'update'){
              await salesOrderItem.update(item.key, item.data)

            }else if(item.type == 'remove'){
              await salesOrderItem.remove(item.key)
      
            }
            
          }
          methods.saveSummary();
          grid.refresh();
        }
        
      },
      finderReturnHandler(data) {
        switch (vars.dlg.finder.key) {
          case 'order': {
            methods.redirect(data.id);
            vars.formState.readOnly = true;
            break;
          }
          case 'client': {
            vars.formData.client_company = data.name;
            methods.onClientChanged();
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
      async onClientChanged() {
        const inputValue = vars.formData.client_company;
        const { data } = await baseClient.load({
          filter: [
            ['fk_company_id', '=', authService.getCompanyId()],
            ['name', '=', inputValue],
          ],
          take: 1,
          skip: 0,
        });
        const client = data.length > 0 ? data[0] : null;

        vars.filter.baseItem.clientId = client ? client.id : null;
        methods.loadBaseItem();
        if (!client) {
          vars.disabled.edit = true;
          vars.disabled.delete = true;
          vars.disabled.save = true;
          vars.disabled.tradeYn = false;
          vars.disabled.clientManager = true;
          vars.formData.client_manager = null;
          vars.dataSource.client_manager = [];
        } else {
          if (methods.isFormReadOnly() || vars.disabled.tradeYn) {
            loadClientManager(vars.dataSource, client.name);
            vars.disabled.tradeYn = false;
            vars.disabled.clientManager = false;
          } else {
            let isSelect = true;
            if (client.trade_yn) {
              isSelect = await confirm('거래중지 업체입니다. 계속 진행하시겠습니까?', '고객업체');
            }
            if (isSelect) {
              loadClientManager(vars.dataSource, client.name);
              vars.disabled.clientManager = false;
              vars.formData.client_manager = null;
            } else {
              vars.formData.client_company = '';
              vars.disabled.tradeYn = true;
              vars.formData.client_manager = null;
            }
          }
        }
        methods.checkPossibleSave();
      },
      async onEndUserChanged(e) {
        if (methods.isFormReadOnly()) {
          return;
        }
        const client = e.component.option('selectedItem');
        if (client) {
          if (client.trade_yn && !vars.disabled.tradeYn) {
            const result = await confirm('거래중지 업체입니다. 계속 진행하시겠습니까?', 'EndUser');
            if (!result) {
              vars.disabled.tradeYn = true;
              return;
            }
          }
        }
        vars.disabled.tradeYn = false;
      },
      async onConfirmChanged(e) {
        if (!vars.formData.id) {
          vars.formData.confirmed = 0;
          return;
        }
        let param = { confirmed: 1 };
        if (e.value) {
          param.confirmed = 1;
          vars.formState.readOnly = true;
          vars.disabled.edit = true;
          vars.disabled.delete = true;
        } else {
          param.confirmed = 0;
          if (methods.isFilledFormRequiredData()) {
            vars.disabled.edit = false;
            methods.syncStatusSave();
            methods.syncStatusDelete();
          }
        }
        await salesOrder.update(vars.formData.id, param);
      },
      updateEtcValue(v) {
        vars.dlg.finder.data = v;
      },
      onDepartmentChanged(e) {
        if (!e.value) {
          vars.disabled.save = true;
          vars.disabled.manager = true;
          vars.formData.order_manager = null;
          vars.dataSource.employee = [];
        } else {
          const selectItem = e.component.option('selectedItem');
          if (selectItem) {
            loadEmployee(vars.dataSource, selectItem.id);
            vars.disabled.manager = false;
          }
        }
        methods.checkPossibleSave();

        const selectedItem = e.component.option('selectedItem');
        if (selectedItem) {
          vars.warehouse = { ...selectedItem.warehouse };
        } else {
          vars.warehouse = {};
        }
        methods.loadBaseItem();
      },

      onSavingItem(e) {
        e.changes.forEach((element) => {
          if (element.type != 'remove') {
            element.data.fk_export_sales_order_id = vars.formData.id;
            delete element.data.item;
            delete element.data.warehouse;
            delete element.data.basic_stock;
          }
        });
        methods.saveSummary();
      },
      saveSummary() {
        const priceData = {
          supply_price: vars.formData.supply_price,
          vat: vars.formData.vat,
          total_price: vars.formData.total_price,
        };
        salesOrder.update(vars.formData.id, priceData);
      },
      onDataError(e) {
        if (e.error.response.status == 605) {
          e.error.message = '연결된 데이터가 있어서 삭제가 안됩니다';
        } else if (e.error.response.status == 606) {
          e.error.message = '출고수량이 현재고를 초과했습니다';
        } else if (e.error.response.status == 607) {
          e.error.message = '기초재고가 등록되지 않은 품목입니다';
        } else if (e.error.response.status == 403) {
          e.error.message = '권한이 없습니다';
        }
      },
      onFocusedCellChanged(e) {
        vars.focus.item1 = e;
      },
      availableStock(rowData) {
        if (!rowData.basic_stock) {
          return '0';
        }
        return rowData.basic_stock.available_stock;
      },
      currentStock(rowData) {
        if (!rowData.basic_stock) {
          return '0';
        }
        return rowData.basic_stock.current_stock;
      },
      setQuantity(newData, value, currentRowData) {
        const { not_shipped, order_quantity, unit_price, basic_stock } =
          currentRowData;

        newData.not_shipped = not_shipped + (value - order_quantity);
        newData.order_quantity = value;
        newData.unit_price = unit_price;
        if (!basic_stock) {
          newData.assign_quantity = 0;
        } else {
          if (basic_stock.available_stock >= newData.not_shipped) {
            newData.assign_quantity = newData.not_shipped;
          } else {
            newData.assign_quantity = basic_stock.available_stock;
          }
        }
        newData.supply_price = newData.order_quantity * newData.unit_price;
      },
      setUnitPrice(newData, value, currentRowData) {
        newData.order_quantity = currentRowData.order_quantity;
        newData.unit_price = value;
        newData.supply_price = newData.order_quantity * newData.unit_price;
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

            if (!basicStock) {
              newData.assign_quantity = 0;
            } else {
              if (basicStock.available_stock >= currentRowData.not_shipped) {
                newData.assign_quantity = currentRowData.not_shipped;
              } else {
                newData.assign_quantity = basicStock.available_stock;
              }
            }
            break;
          }
        }
      },
      loadBaseCode() {
        return baseCodeLoader([
          'Origin',
          'Ship Port',
          'Currency',
          '부가세구분',
          '수주구분',
          '결재조건',
        ])
          .then((response) => {
            vars.dataSource.payment_terms = response['결재조건'];
            vars.dataSource.order_type = response['수주구분'];
            vars.dataSource.vat_type = response['부가세구분'];
            vars.dataSource.origin = response['Origin'];
            vars.dataSource.ship_port = response['Ship Port'];
            vars.dataSource.currency = response['Currency'];
          })
          .then(() => (vars.init.value = true));
      },
      loadBaseItem() {
        vars.dataSource.baseItem = getBaseItem(
          null,
          vars.filter.baseItem.clientId,
          vars.warehouse.wh_code
        );
      },

      checkPossibleSave() {
        if (methods.isFilledFormRequiredData() && !methods.isOrderConfirmed()) {
          methods.syncStatusSave();
        }
      },
      getFirstOrderType() {
        return methods.getFirstItemName(vars.dataSource.order_type);
      },
      getFirstVatType() {
        return methods.getFirstItemName(vars.dataSource.vat_type);
      },
      getFirstPaymentTerms() {
        return methods.getFirstItemName(vars.dataSource.payment_terms);
      },
      getFirstOrigin() {
        return methods.getFirstItemName(vars.dataSource.origin);
      },
      getFirstShipPort() {
        return methods.getFirstItemName(vars.dataSource.ship_port);
      },
      getFirstCuurrency() {
        return methods.getFirstItemName(vars.dataSource.currency);
      },
      getFirstItemName(itemList) {
        if (!itemList || itemList.length <= 0) {
          return '';
        } else {
          return itemList[0].code_name;
        }
      },
      redirect(id) {
        if (id) {
          router.replace({ path: `/export/sales-order/${id}` });
        } else {
          router.replace({ path: `/export/sales-order` });
        }
      },
      itemPopupClick({ column, data }) {
        if (column.name === 'item_code') {
          vars.itemDetail.id = data.item.id;
          vars.itemDetail.visible = true;
        }
      },
      syncStatusDelete() {
        if (methods.isFormReadOnly()) {
          vars.disabled.delete = true;
        } else {
          vars.disabled.delete = false;
        }
      },
      syncStatusSave() {
        if (methods.isFormReadOnly()) {
          vars.disabled.save = true;
        } else {
          vars.disabled.save = false;
        }
      },
      disableAllAction() {
        vars.disabled.edit = true;
        vars.disabled.delete = true;
        vars.disabled.save = true;
        vars.disabled.manager = true;
        vars.disabled.clientManager = true;
      },
      async exportToRelease() {
        if (!vars.formData.id) {
          return;
        }
        const params = { order_id: vars.formData.id };
        try {
          await vars.api.exportToRelease.post('', params);
          await alert('출고로 보내기가 완료되었습니다', '출고로 보내기');

          methods.loadOrderData(vars.formData.id);
          methods.gridItem1Refresh(vars.formData.id);
        } catch (ex) {
          if (ex.response.status == 608) {
            await alert('미출고 수량이 없습니다', '출고로 보내기');
          } else {
            await alert('출고로 보내기가 실패했습니다', '출고로 보내기');
          }
        }
      },
      clientManagerExpr(item) {
        if (!item) return '';
        if (item.mobile) {
          vars.formData.client_manager_phone = item.mobile;
        }
        return item.name;
      },
      async copyItem() {
        methods.showLoading();

        const params = Object.assign(vars.formData);

        delete params.id;
        delete params.created;
        delete params.order_number;
        let { data } = await salesOrder.insert(params);
        const gridItem1 = vars.grid.item1;
        if (gridItem1 && gridItem1.hasEditData()) {
          await gridItem1.saveEditData();
        }
        const ds = getSalesOrderItem();
        const rows = gridItem1.getVisibleRows();
        for (const row of rows) {
          const newItem = {
            fk_export_sales_order_id: data.id,
            item_code: row.data.item_code,
            order_quantity: row.data.order_quantity,
            unit_price: row.data.unit_price,
            supply_price: row.data.supply_price,
            request_delivery_date: row.data.request_delivery_date,
            contact_delivery_date: row.data.contact_delivery_date,
            assign_quantity: row.data.assign_quantity,
            not_shipped: row.data.not_shipped,
            warehouse_code: row.data.warehouse_code,
          };
          await ds.insert(newItem);
        }

        methods.redirect(data.id);
        vars.formState.readOnly = true;
        notifyInfo('복사되었습니다');
        methods.hideLoading();
      },
      showLoading() {
        vars.loading.value = true;
      },
      hideLoading() {
        vars.loading.value = false;
      },
      isFormReadOnly() {
        return vars.formState.readOnly;
      },
      isOrderConfirmed() {
        return vars.formData.confirmed;
      },
      calculateCustomSummary(options) {
        if (options.name === 'supply_price') {
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          } else if (options.summaryProcess === 'calculate') {
            options.totalValue += options.value.order_quantity * options.value.unit_price;
          } else if (options.summaryProcess === 'finalize') {
            const response = calcPriceSummary(vars.formData.vat_type, options.totalValue);
            vars.formData.supply_price = response.supply_price;
            vars.formData.vat = response.vat;
            vars.formData.total_price = response.total_price;
          }
        }
      },
      isFilledFormRequiredData() {
        if (vars.formData.client_company && vars.formData.order_department) {
          return true;
        }
        return false;
      },
      downloadSampleFile () {
        saveAs('/api/mes/v1/excel/export/sales_order', 'sample.xlsx');
      },
      importExcelData () {
        excelRef.value.click()
      },
      async excelFileChange ({ target }) {
        if (!target.files.length) return;

        vars.grid['item1'].beginCustomLoading('엑셀 데이터를 읽고 있습니다');

        const api = new ApiService('/api/mes/v1/excel/export/sales_order')
        const fd = new FormData();
        fd.append('file', target.files[0]);
        const exceptedItems = []

        try {
          const {data: excelResp} = await api.post('', fd);
          const baseItem = getBaseItem()
          const excelRespReverse = excelResp.objects.reverse();
          for (const item of excelRespReverse) {
            const {data: items} = await baseItem.load({filter: ['item_code', '=', item.item_code]})
            if (!items.length) {
              exceptedItems.push(item.item_code)
              continue
            }
            const basicStock = items[0].basic_stock
              ? { ...items[0].basic_stock[0] }
              : { current_stock: 0, available_stock: 0 };

            await vars.grid.item1.addRow();
            const data = await vars.grid.item1.byKey(vars.grid.item1.getKeyByRowIndex(0));
            data.item_code = items[0].item_code; // 품목코드
            data.item = { ...items[0] }; // 품목
            data.supply_price = item.unit_price * item.order_quantity; // 공급가
            data.order_quantity = item.order_quantity; // 수주수량
            data.assign_quantity = basicStock.available_stock > item.order_quantity
              ? item.order_quantity
              : basicStock.available_stock; // 할당수량
            data.not_shipped = item.order_quantity; // 미출고
            data.unit_price = item.unit_price; // 단가
            data.request_delivery_date = null; // 요청납기
            data.contact_delivery_date = null; // 요청납기
            data.basic_stock = { ...basicStock }; // 기초재고
            data.warehouse = { ...vars.warehouse }; // 출고창고
            data.warehouse_code = '본사창고'; // 창고코드
            data.fk_export_sales_order_id = vars.formData.id; // 수주 아이디
            data.lot = item.lot
          }
          vars.grid.item1.refresh();
        } catch (ex) {
          if (ex.response && ex.response.data) {
            notifyError(ex.response.data);
          }
          else {
            console.error(ex)
          }
        } finally {
          vars.grid.item1.endCustomLoading();
          target.value = null;
        }

        if (exceptedItems.length) {
          notifyError(`[${exceptedItems.join(', ')}] 품목을 찾을수 없어 제외했습니다`);
        }
      }
    };

    watch(
      () => props.id,
      () => methods.initById(props.id)
    );

    return {
      vars,
      methods,
      excelRef,
      generateItemButtonOption,
    };
  },
};
</script>
<style>
.popup-message {
  text-align: center;
}
.currency_item_box > label > span {
  max-width: 50px;
}
.currency_item_box {
  padding-right: 0px !important;
}
</style>
