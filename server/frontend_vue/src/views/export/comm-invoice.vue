<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">Comm Invoice</div>
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
              :options="{ text: '출력', type: 'print', icon: 'print', onClick: methods.printDocument }"
            />
          </dx-toolbar>
        </div>

        <dx-form :form-data="vars.formData">
          <dx-group-item :col-count="5">
            <dx-group-item>
              <dx-simple-item
                data-field="invoice_number"
                :editor-options="{
                  placeholder: '(자동 or 직접입력)',
                  ...generateItemButtonOption('search', methods.createFindPopupFn('invoice', '출고조회')),
                }"
              >
                <dx-label text="Invoice No" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="invoice_date" editor-type="dxDateBox"
                :editor-options="{ dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss', ...vars.formState }"
              >
                <dx-label text="Invoice Date" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="ship_date" editor-type="dxDateBox"
                :editor-options="{ dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss', ...vars.formState }"
              >
                <dx-label text="Ship Date" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="sale_date" editor-type="dxDateBox"
                :editor-options="{ dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss', ...vars.formState }"
              >
                <dx-label text="Sale Date" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="client_company"
                :editor-options="{
                  onEnterKey: methods.createFindPopupFn('client', '고객조회', { name: vars.formData.client_company }),
                  ...generateItemButtonOption('search', methods.createFindPopupFn('client', '고객조회', {
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
                  dataSource: vars.dataSource.client_manager,
                  displayExpr: methods.clientManagerExpr,
                  valueExpr: 'name',
                  acceptCustomValue: true,
                  disabled: vars.disabled.clientManager,
                  ...vars.formState,
                }"
              >
                <dx-label text="Buyer Contact" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="invoice_department" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.department,
                  displayExpr: 'department_name',
                  valueExpr: 'department_name',
                  acceptCustomValue: true,
                  onValueChanged: methods.onDepartmentChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="Owner Dept" :show-colon="false" />
                <dx-required-rule message="출고부서를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="invoice_manager" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.employee,
                  displayExpr: 'emp_name',
                  valueExpr: 'emp_name',
                  disabled: vars.disabled.manager,
                  ...vars.formState,
                }"
              >
                <dx-label text="Member" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
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
              <dx-simple-item data-field="vat_type" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.vat_type,
                  displayExpr: 'code_name',
                  valueExpr: 'code_name',
                  onValueChanged: methods.onVatTypeChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="부가세구분" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="confirmed" editor-type="dxCheckBox"
                :editor-options="{ onValueChanged: methods.onConfirmChanged }"
              >
                <dx-label text="출고확정" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="etc" editor-type="dxTextArea"
                :editor-options="{
                  height: '170px',
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
            height="calc(100vh - 466px)"
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
            @saving="methods.onSavingItem"
            @cell-dbl-click="methods.itemPopupClick"
            @data-error-occurred="methods.onDataError"
          >
            <dx-grid-toolbar>
              <dx-grid-item name="addRowButton" :options="{ onClick: methods.showAddPopup }" />
              <dx-grid-item name="saveButton" :visible="!!vars.formData.id" />
              <dx-grid-item name="revertButton" />
              <dx-grid-item name="columnChooserButton" />
            </dx-grid-toolbar>

            <dx-column caption="Item Code" data-field="item_code" width="180" :allow-editing="false" />
            <dx-column caption="Itme Name" data-field="item.item_name" :allow-editing="false" />
            <dx-column caption="Sub Name" data-field="item.item_standard" :allow-editing="false" />
            <dx-column caption="Qty" data-field="export_sales_order_item.order_quantity" data-type="number" format="fixedPoint" :allow-editing="false" />
            <dx-column caption="출고수량" data-field="invoice_quantity" data-type="number" format="fixedPoint" :set-cell-value="methods.setQuantity" />
            <dx-column caption="미입고" data-field="not_received" data-type="number" format="fixedPoint" />
            <dx-column caption="Export Price" data-field="unit_price" data-type="number" :format="{ type: 'fixedPoint', precision: 4 }" :set-cell-value="methods.setUnitPrice" />
            <dx-column caption="단위" data-field="item.unit" :allow-editing="false" />
            <dx-column caption="Amount" data-field="supply_price" data-type="number" :format="{ type: 'fixedPoint', precision: 4 }" :allow-editing="false" />
            <dx-column caption="Req Date" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
            <dx-column caption="Con Date" data-field="contact_delivery_date" data-type="date" format="yyyy-MM-dd" />
            <dx-column caption="LOT NO(생산주차)" data-field="lot" />
            <dx-column caption="출고창고" data-field="warehouse.wh_name" :set-cell-value="methods.setWarehouse" >
              <dx-lookup value-expr="wh_name" display-expr="wh_name" :data-source="vars.dataSource.warehouse" />
            </dx-column>
            <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :allow-editing="false" />
            <dx-column caption="Order No" data-field="order_number" :allow-editing="false" />
            <dx-column caption="Description" data-field="item.item_detail" :allow-editing="false" />
            <dx-column caption="출고아이디" data-field="fk_export_comm_invoice_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
            <dx-column caption="수주 품목 아이디" data-field="fk_export_sales_order_item_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
            <dx-column caption="창고코드" data-field="warehouse_code" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />

            <dx-summary :recalculate-while-editing="true" :calculate-custom-summary="methods.calculateCustomSummary">
              <dx-total-item name="supply_price" summary-type="custom" />
            </dx-summary>

            <dx-scrolling mode="standard" />
            <dx-column-chooser mode="select" :enabled="true" />
            <dx-editing
              mode="batch"
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
      title="수주품목찾기"
      content-template="popup-content"
      v-model:visible="vars.dlg.addItem.show"
      width="70%"
      :height="460"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="(evt) => methods.onGridInitialized(evt, 'find-release-popup')"
    >
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
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
          :data-source="vars.dataSource.orderItem"
          :on-initialized="(evt) => methods.onGridInitialized(evt, 'orderItem')"
        >
          <dx-column caption="고객업체" data-field="export_order.client_company" />
          <dx-column caption="수주번호" data-field="export_order.order_number" :sort-index="1" sort-order="desc" />
          <dx-column caption="수주일자" data-field="export_order.order_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="수주수량" data-field="order_quantity" />
          <dx-column caption="할당수량" data-field="assign_quantity" />
          <dx-column caption="미출고수량" data-field="not_shipped" />

          <dx-paging :page-size="20" />
          <dx-sorting mode="multiple"/>
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
      @initialized="(evt) => methods.onGridInitialized(evt, 'multiuse-popup')"
    >
      <template #popup-content>
        <data-grid-client v-if="vars.dlg.finder.key === 'client'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-client v-else-if="vars.dlg.finder.key === 'enduser'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-invoice v-else-if="vars.dlg.finder.key === 'invoice'" @change="methods.finderReturnHandler" />
        <data-grid-project v-else-if="vars.dlg.finder.key === 'project'" @change="methods.finderReturnHandler" />
        <div v-else-if="vars.dlg.finder.key === 'etc'">
          <div class="mb-2">
            <dx-text-area :height="190" :value="vars.dlg.finder.data" @update:value="methods.updateEtcValue" />
          </div>
          <dx-toolbar>
            <dx-item widget="dxButton" toolbar="top" location="after"
              :options="{ text: '닫기', icon: null, onClick: methods.finderReturnHandler, }"
            />
          </dx-toolbar>
        </div>
      </template>
    </dx-popup>

    <popup-item-detail v-model:visible="vars.itemDetail.visible" :item-id="vars.itemDetail.id" />
  </div>
</template>

<script>
import moment from 'moment';
import numeral from 'numeral';
import { chunk } from 'lodash'

import { useRouter } from 'vue-router';
import { ref, reactive, computed, watch, nextTick, onMounted } from 'vue';

import { DxButton } from 'devextreme-vue/button';
import DxTextArea from 'devextreme-vue/text-area';
import { confirm, alert } from 'devextreme/ui/dialog';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxCustomRule, DxRequiredRule } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxLookup, DxPaging, DxEditing, DxSorting, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, 
  DxItem as DxGridItem, DxButton as DxGridButton, DxToolbar as DxGridToolbar } from 'devextreme-vue/data-grid';

import { getStock } from '../../data-source/setup';
import { baseItem, baseClient, baseCodeLoader } from '../../data-source/base';
import { commInvoice, getCommInvoiceItem, getSalesOrderItem } from '../../data-source/export';

import PopupItemDetail from '@/components/base/popup-item-detail';
import DataGridClient from '../../components/base/data-client.vue';
import DataGridInvoice from '../../components/export/data-comm-invoice.vue';
import DataGridProject from '../../components/project/data-project.vue';

import authService from '../../auth';
import stateStore from '@/utils/state-store';
import printDocument from '@/utils/print-document';
import { notifyInfo, notifyError } from '../../utils/notify';
import { loadEmployee, loadWarehouse, loadDepartment, loadClientManager } from '../../utils/data-loader';
import { currentDateTime, calcPriceSummary, beforeExitConfirm, generateItemButtonOption } from '../../utils/util';

export default {
  components: {
    DxButton,
    DxTextArea,
    DxLoadPanel,
    DxToolbar, DxItem,
    DxPopup, DxToolbarItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxCustomRule, DxRequiredRule,
    DxDataGrid, DxColumn, DxLookup, DxPaging, DxEditing, DxSorting, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser,
    DxGridItem, DxGridToolbar, DxGridButton,
    DataGridClient, DataGridInvoice, DataGridProject, PopupItemDetail,
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
    vars.grid = { orderItem: null, item1: null };
    vars.dlg.addItem = reactive({ show: false });
    vars.dlg.finder = reactive({ show: false, title: '', key: null, data: null });
    vars.filter = {};
    vars.filter.orderItem = { clientCompany: null };
    vars.filter.item1 = [{ name: 'fk_export_comm_invoice_id', op: 'eq', val: props.id || 0 }];
    vars.disabled = reactive({
      edit: true,
      delete: true,
      new: false,
      save: true,
      items: true,
      manger: true,
      clientManager: true,
      tradeYn: false,
    });
    vars.dataSource = reactive({
      employee: [],
      department: [],
      currency: [],
      client_manager: [],
      vat_type: [],
      warehouse: [],
      orderItem: null,
      item1: getCommInvoiceItem(vars.filter.item1),
    });
    vars.formData = reactive({});

    vars.summary = {};
    vars.summary.supply_price = computed(() => numeral(vars.formData.supply_price).format('0,0'));
    vars.summary.vat = computed(() => numeral(vars.formData.vat).format('0,0'));
    vars.summary.total_price = computed(() => numeral(vars.formData.total_price).format('0,0'));
    
    vars.itemDetail = reactive({ visible: false, id: 0 });

    onMounted(async () => {
      loadWarehouse(vars.dataSource);
      await loadDepartment(vars.dataSource);
      await methods.loadBaseCode();
      methods.initById(props.id);
    });

    // public methods
    const methods = {
      async initById(id) {
        beforeExitConfirm.check(() => !vars.disabled.save);
        methods.gridItem1Refresh(id);
        if (!id) {
          methods.clearFormData();

          vars.disabled.edit = true;
          vars.disabled.delete = true;
          vars.disabled.save = true;
          vars.disabled.items = true;
          vars.disabled.manager = true;
          vars.disabled.clientManager = true;
          return;
        }

        let { data } = await commInvoice.byKey(id);
        Object.assign(vars.formData, data);

        methods.enableDelete();
        vars.disabled.edit = false;
        if (vars.formData.client_company && vars.formData.invoice_department) {
          methods.enableSave();
          vars.disabled.items = false;
        }
        methods.onClientChanged();
      },
      clearFormData() {
        vars.formData.id = null;
        vars.formData.created = null;
        vars.formData.invoice_number = '';
        vars.formData.invoice_date = '';
        vars.formData.ship_date = '';
        vars.formData.sale_date = '';
        vars.formData.client_company = '';
        vars.formData.client_manager = '';
        vars.formData.invoice_department = '';
        vars.formData.invoice_manager = '';
        vars.formData.currency = '';
        vars.formData.exrate = 0;
        vars.formData.vat_type = '';
        vars.formData.etc = '';
        vars.formData.supply_price = 0;
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

        const rows = await vars.grid.orderItem.getSelectedRowsData();
        for (let row of rows) {
          let currentStock = 0;
          if (row.basic_stock) {
            currentStock = row.basic_stock.current_stock;
          }
          await grid.addRow();
          grid.cellValue(0, 'item_code', row.item_code); // 품목코드
          grid.cellValue(0, 'item.item_name', row.item.item_name); // 품명
          grid.cellValue(0, 'item.item_standard', row.item.item_standard); // 규격
          grid.cellValue(0, 'export_sales_order_item.order_quantity', row.order_quantity); // 수주수량
          grid.cellValue(0, 'invoice_quantity', row.order_quantity); // 출고수량
          grid.cellValue(0, 'unit_price', row.unit_price); // 단가
          grid.cellValue(0, 'item.unit', row.item.unit); // 단위
          grid.cellValue(0, 'supply_price', row.supply_price); // 공급가
          grid.cellValue(0, 'request_delivery_date', row.request_delivery_date); // 요청납기
          grid.cellValue(0, 'contact_delivery_date', row.contact_delivery_date); // 요청납기
          grid.cellValue(0, 'non_invoice', row.order_quantity); // 미계산서
          grid.cellValue(0, 'not_received', row.order_quantity); // 미입고
          grid.cellValue(0, 'lot', row.lot); // 생산주차
          grid.cellValue(0, 'warehouse.wh_name', row.warehouse.wh_name); // 출고창고
          grid.cellValue(0, 'basic_stock.current_stock', currentStock); // 현재고
          grid.cellValue(0, 'order_number', row.export_order.order_number); // 수주번호
          grid.cellValue(0, 'client_item_number', row.client_item_number); // 고객사품번
          grid.cellValue(0, 'item.item_detail', row.item.item_detail); // 품목설명
          grid.cellValue(0, 'closing_yn', false); // 출하검사
          grid.cellValue(0, 'warehouse_code', row.warehouse.wh_code); // 출고창고
          grid.cellValue(0, 'fk_export_comm_invoice_id', vars.formData.id);
          grid.cellValue(0, 'fk_export_sales_order_item_id', row.id);
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
      async gridItem1Refresh(id) {
        if (!id) {
          id = 0;
        }
        vars.filter.item1[0].val = id;
        vars.dataSource.item1.defaultFilters = vars.filter.item1;
        if (vars.grid.item1) {
          vars.grid.item1.cancelEditData();
          vars.grid.item1.refresh();
        }
      },
      showAddPopup() {
        if (vars.grid.orderItem) {
          vars.grid.orderItem.clearSelection();
          vars.grid.orderItem.refresh();
        }
        vars.dlg.addItem.show = true;
      },
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`shipment-release-${key}`, evt.component);
      },
      async newItem() {
        methods.gridItem1Refresh();
        if (vars.formData.id) {
          methods.clearFormData();
          methods.redirect();
        }
        setTimeout(() => {
          methods.clearFormData();
          vars.formData.invoice_date = currentDateTime();
          vars.formData.ship_date = currentDateTime();
          vars.formData.sale_date = currentDateTime();
          vars.formData.invoice_department = authService.getDepartmentName();
          vars.formData.invoice_manager = authService.getUserName();
          vars.formData.vat_type = methods.getFirstVatType();
          vars.formData.currency = methods.getFirstCurrency();
          vars.formData.confirmed = false;
          vars.formData.fk_company_id = authService.getCompanyId();
          vars.formState.readOnly = false;
        }, 200);
      },
      async editItem() {
        if (!vars.formData.id) {
          return;
        }
        if (vars.formState.readOnly && vars.formData.confirmed) {
          return;
        }
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
        const result = await confirm('이 항목을 삭제하시겠습니까?', '삭제 확인');
        if (result) {
          try {
            await commInvoice.remove(vars.formData.id);
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
        vars.loading.value = true;
        try {
          if (vars.formData.id) {
            // 기존 정보 업데이트
            const updateDate = Object.assign({}, vars.formData);
            delete updateDate.created;
            delete updateDate.invoice_number;
            const { data } = await commInvoice.update(
              vars.formData.id,
              updateDate
            );
            vars.formData.invoice_number = data.invoice_number;

            if (vars.grid.item1) await vars.grid.item1.saveEditData();

            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');

            methods.enableSave();
            methods.enableDelete();
          } else {
            // 채번이 없을 경우 자동 채번
            if (vars.formData.created) {
              vars.formData.created = null;
            }
            let { data } = await commInvoice.insert(vars.formData);
            vars.formData.id = data.id;

            const gridItem1 = vars.grid.item1;
            if (gridItem1 && gridItem1.hasEditData()) {
              await gridItem1.saveEditData();
            }

            beforeExitConfirm.clear()
            methods.redirect(data.id);
            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');
          }
        } catch (ex) {
          console.error(ex);
          if (ex.response.status === 602) {
            notifyError('이미 존재하는 번호 입니다');
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
          case 'invoice': {
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

        vars.filter.orderItem.clientCompany = client ? client.name : null;
        methods.loadOrderItem();

        if (!client) {
          vars.disabled.edit = true;
          vars.disabled.delete = true;
          vars.disabled.save = true;
          vars.disabled.items = true;
          vars.disabled.tradeYn = false;
          vars.disabled.clientManager = true;
          vars.formData.client_manager = null;
          vars.dataSource.client_manager = [];
        } else {
          if (vars.formState.readOnly || vars.disabled.tradeYn) {
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
        if (vars.formState.readOnly) {
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
          if (
            vars.formData.client_company &&
            vars.formData.invoice_department
          ) {
            vars.disabled.edit = false;
            methods.enableSave();
            methods.enableDelete();
          }
        }
        await commInvoice.update(vars.formData.id, param);
      },
      updateEtcValue(v) {
        vars.dlg.finder.data = v;
      },
      onDepartmentChanged(e) {
        if (!e.value) {
          vars.disabled.save = true;
          vars.disabled.items = true;
          vars.disabled.manager = true;
          vars.formData.invoice_manager = null;
          vars.dataSource.employee = [];
        } else {
          const selectItem = e.component.option('selectedItem');
          if (selectItem) {
            loadEmployee(vars.dataSource, selectItem.id);
            vars.disabled.manager = false;
          }
        }
        methods.checkPossibleSave();
      },
      onSavingItem(e) {
        e.changes.forEach((element) => {
          if (element.type != 'remove') {
            element.data.fk_export_comm_invoice_id = vars.formData.id;
            delete element.data.item;
            delete element.data.warehouse;
            delete element.data.basic_stock;
            delete element.data.export_sales_order_item;
            delete element.data.current_stock;
            delete element.data.available_stock;
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
        commInvoice.update(vars.formData.id, priceData);
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
      setQuantity(newData, value, currentRowData) {
        newData.invoice_quantity = value;
        newData.unit_price = currentRowData.unit_price;
        newData.supply_price = newData.invoice_quantity * newData.unit_price;
        newData.not_received = currentRowData.not_received + (value - currentRowData.invoice_quantity);
      },
      setUnitPrice(newData, value, currentRowData) {
        newData.invoice_quantity = currentRowData.invoice_quantity;
        newData.unit_price = value;
        newData.supply_price = newData.invoice_quantity * newData.unit_price;
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
      loadBaseCode() {
        return baseCodeLoader(['부가세구분', 'currency'])
          .then((response) => {
            vars.dataSource.vat_type = response['부가세구분'];
            vars.dataSource.currency = response['currency'];
          })
          .then(() => (vars.init.value = true));
      },
      loadOrderItem() {
        vars.dataSource.orderItem = getSalesOrderItem([
          {
            name: 'export_order',
            op: 'has',
            val: {
              name: 'client_company',
              op: 'eq',
              val: vars.filter.orderItem.clientCompany,
            },
          },
          { name: 'not_shipped', op: 'gt', val: 0 },
        ]);
      },
      checkPossibleSave() {
        if (vars.formData.client_company && vars.formData.invoice_department) {
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
      getFirstVatType() {
        return methods.getFirstItemName(vars.dataSource.vat_type);
      },
      getFirstCurrency() {
        return methods.getFirstItemName(vars.dataSource.currency);
      },
      getFirstItemName(itemList) {
        if (!itemList || itemList.length <= 0) {
          return '';
        } else return itemList[0].code_name;
      },
      redirect(id) {
        if (id) router.replace({ path: `/export/comm-invoice/${id}` });
        else router.replace({ path: `/export/comm-invoice` });
      },
      onVatTypeChanged(e) {
        vars.grid.item1.refresh();
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
      clientManagerExpr(item) {
        if (!item) return '';
        if (item.mobile) {
          vars.formData.client_manager_phone = item.mobile;
        }
        return item.name;
      },
      calculateCustomSummary(options) {
        if (options.name === 'supply_price') {
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          } else if (options.summaryProcess === 'calculate') {
            options.totalValue += options.value.invoice_quantity * options.value.unit_price;
          } else if (options.summaryProcess === 'finalize') {
            const response = calcPriceSummary(vars.formData.vat_type, options.totalValue);
            vars.formData.supply_price = response.supply_price;
            vars.formData.vat = response.vat;
            vars.formData.total_price = response.total_price;
          }
        }
      },
      async printDocument() {
        if (!vars.formData.id) return;
        const params = {};
        params.title = ''
        params.release_number = ''
        params.client_company = vars.formData.client_company;
        params.caps = params.client_company.includes('캡스');

        params.manager = {
          emp_ext_phone: '',
          emp_name: '',
          emp_position: '',
          emp_mobile: '',
          emp_email: '',
        };
        params.supply_price = numeral(vars.formData.supply_price).format('0,0');
        params.vat = numeral(vars.formData.vat).format('0,0');
        params.total_price = numeral(vars.formData.total_price).format('0,0');

        params.vat_type = 0;
        params.etc = '';
        params.invoice_number = vars.formData.invoice_number;
        params.invoice_date = moment(vars.formData.invoice_date).format('YYYY년 M월 D일');
        params.ship_date = moment(vars.formData.ship_date).format('YYYY년 M월 D일');
        params.sale_date = moment(vars.formData.sale_date).format('YYYY년 M월 D일');
        params.invoice_manager = vars.formData.invoice_manager;

        const { data: item1 } = await vars.dataSource.item1.load();
        const items = item1.map((item, idx) => {
          item.index = idx + 1
          item.unit_price = numeral(item.unit_price).format('0,0');
          item.supply_price = numeral(item.supply_price).format('0,0');
          return item;
        });
        params.pages = chunk(items, 17)

        await printDocument('release', params);
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
