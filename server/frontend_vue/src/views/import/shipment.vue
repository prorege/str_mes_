<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">Shipment</div>
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
              <dx-simple-item data-field="shipment_number"
                :editor-options="{
                  placeholder: '(자동 or 직접입력)',
                  ...generateItemButtonOption('search', methods.createFindPopupFn('shipment', '선적조회')),
                }"
              >
                <dx-label text="OfferNo" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="shipment_date" editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  ...vars.formState,
                }"
              >
                <dx-label text="IssueDate" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="purchase_order.order_number"
                :editor-options="{
                  ...generateItemButtonOption('search', methods.createFindPopupFn('purchase-order', 'Purchase Order 조회')),
                  ...vars.formState,
                }"
              >
                <dx-label text="P/O No." :show-colon="false" />
                <dx-required-rule message="발주를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="supplier" :editor-options="{ readOnly: true }">
                <dx-label text="Supplier" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="buyer" :editor-options="{ readOnly: true }">
                <dx-label text="Buyer" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="validity" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  dataSource: vars.dataSource.validity,
                  ...vars.formState,
                }"
              >
                <dx-label text="Validity" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="pay_terms" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  dataSource: vars.dataSource.pay_terms,
                  ...vars.formState,
                }"
              >
                <dx-label text="Pay Terms" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="destination" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  dataSource: vars.dataSource.destination,
                  ...vars.formState,
                }"
              >
                <dx-label text="Destination" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="delivery" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  dataSource: vars.dataSource.delivery,
                  ...vars.formState,
                }"
              >
                <dx-label text="Delivery" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="price_terms" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  dataSource: vars.dataSource.price_terms,
                  ...vars.formState,
                }"
              >
                <dx-label text="Price Terms" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="origin" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  dataSource: vars.dataSource.origin,
                  ...vars.formState,
                }"
              >
                <dx-label text="Origin" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="ship_port" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  dataSource: vars.dataSource.ship_port,
                  ...vars.formState,
                }"
              >
                <dx-label text="ShipPort" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="packing" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  dataSource: vars.dataSource.packing,
                  ...vars.formState,
                }"
              >
                <dx-label text="Packing" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="adv_bank" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'bank_code',
                  displayExpr: methods.bankNameFormat,
                  acceptCustomValue: true,
                  dataSource: vars.dataSource.bank,
                  ...vars.formState,
                }"
              >
                <dx-label text="AdvBank" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="currency" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  dataSource: vars.dataSource.currency,
                  ...vars.formState,
                }"
              >
                <dx-label text="Currency" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="ex_rate" editor-type="dxNumberBox" 
                :editor-options="{ 
                  format: '#0.00',
                  ...vars.formState 
                }"
              >
                <dx-label text="ExRate" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="inspection" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  dataSource: vars.dataSource.inspection,
                  ...vars.formState,
                }"
              >
                <dx-label text="Inspection" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="payment" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_class_detail',
                  displayExpr: 'code_name',
                  dataSource: vars.dataSource.payment,
                  ...vars.formState,
                }"
              >
                <dx-label text="Payment" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="remark" :editor-options="{ ...vars.formState }">
                <dx-label text="Remark" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
          </dx-group-item>
        </dx-form>
      </div>

      <div class="dx-card responsive-paddings mt-1">
        <div class="mt-2">
          <dx-data-grid
            class="fixed-header-table"
            height="calc(100vh - 416px)"
            date-serialization-format="yyyy-MM-ddTHH:mm:ss"
            column-resizing-mode="widget"
            :show-borders="true"
            :column-auto-width="true"
            :remote-operations="false"
            :focused-row-enabled="true"
            :allow-column-resizing="true"
            :allow-column-reordering="true"
            :row-alternation-enabled="true"
            :select-text-on-edit-start="true"
            :disabled="vars.disabled.items"
            :data-source="vars.dataSource.shipmentItem"
            :on-initialized="(evt) => methods.onGridInitialized(evt, 'shipmentItem')"
            @saving="methods.onSavingItem"
            @cell-dbl-click="methods.itemPopupClick"
            @data-error-occurred="methods.onDataError"
            @focused-cell-changed="methods.onFocusedCellChanged"
          >
            <dx-grid-toolbar>
              <dx-grid-item name="saveButton" :visible="!!vars.formData.id" />
              <dx-grid-item name="revertButton" />
              <dx-grid-item name="columnChooserButton" />
            </dx-grid-toolbar>

            <dx-column caption="ItemCode" data-field="item_code" width="180" :allow-editing="false" />
            <dx-column caption="Name SubName" data-field="item.item_name" :allow-editing="false" />
            <dx-column caption="Qty" data-field="qty" data-type="number" format="fixedPoint" :set-cell-value="methods.setQuantity" />
            <dx-column caption="Unit" data-field="item.unit" :allow-editing="false" />
            <dx-column caption="ImportPrice" data-field="import_price" data-type="number" :format="',##0.00000'" :allow-editing="false" />
            <dx-column caption="Amount" data-field="amount" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :set-cell-value="methods.setUnitPrice" :allow-editing="false" />
            <dx-column caption="ReqDeliDate" data-field="req_date" data-type="date" format="yyyy-MM-dd" :allow-editing="false" />
            <dx-column caption="ConDeliDate" data-field="con_date" data-type="date" format="yyyy-MM-dd" :allow-editing="false" />
            <dx-column caption="EndUser" data-field="end_user" :allow-editing="false" />
            <dx-column caption="미오퍼" data-field="import_purchase_order_item.not_shipment" data-type="number" format="fixedPoint" :allow-editing="false" />
            <dx-column caption="미통관" data-field="not_clearance" data-type="number" format="fixedPoint" :allow-editing="false" />
            <dx-column caption="미발행" data-field="not_publish" data-type="number" format="fixedPoint" :allow-editing="false" />
            <dx-column caption="종결" data-field="closing_yn" data-type="boolean" />
            
            <dx-summary :recalculate-while-editing="true" :calculate-custom-summary="methods.calculateCustomSummary">
              <dx-total-item name="supply_price" summary-type="custom" />
            </dx-summary>

            <dx-scrolling mode="standard" />
            <dx-column-chooser mode="select" :enabled="true" />
            <dx-editing mode="batch"
              :allow-updating="!vars.formState.readOnly"
              :allow-deleting="!vars.formState.readOnly"
            />
          </dx-data-grid>
        </div>

        <div class="mt-2">
          <table class="summary-table">
            <tr>
              <th>합계금액:</th>
              <td>{{ vars.summary.total_price.value }}</td>
            </tr>
          </table>
        </div>
      </div>
    </div>

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
        <data-grid-client         v-if="vars.dlg.finder.key === 'enduser'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-shipment       v-else-if="vars.dlg.finder.key === 'shipment'" @change="methods.finderReturnHandler" />
        <data-grid-purchase-order v-else-if="vars.dlg.finder.key === 'purchase-order'" @change="methods.finderReturnHandler" />
      </template>
    </dx-popup>

    <popup-item-detail :item-id="vars.itemDetail.id" v-model:visible="vars.itemDetail.visible" />
  </div>
</template>

<script>
import moment from 'moment';
import numeral from 'numeral';
import { groupBy } from 'lodash'

import { useRouter } from 'vue-router';
import { onMounted, ref, reactive, computed, watch, nextTick } from 'vue';

import { DxButton } from 'devextreme-vue/button';
import DxTextArea from 'devextreme-vue/text-area';
import { confirm, alert } from 'devextreme/ui/dialog';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { notifyInfo, notifyError } from '../../utils/notify';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxCustomRule, DxRequiredRule } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxLookup, DxEditing, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, 
  DxItem as DxGridItem, DxToolbar as DxGridToolbar, DxButton as DxGridButton } from 'devextreme-vue/data-grid';

import stateStore from '@/utils/state-store';
import { baseCodeLoader, baseClient } from '../../data-source/base';
import { importShipment, getImportShipmentItem, getImportPurchaseOrderItem } from '../../data-source/import';

import DataGridClient from '../../components/base/data-client.vue';
import DataGridShipment from '../../components/import/data-shipment.vue';
import DataGridPurchaseOrder from '../../components/import/data-purchase-order.vue';
import authService from '../../auth';
import { calcPriceSummary, generateItemButtonOption, getFirstCodeNameInBaseCodeList, currentDateTime } from '../../utils/util';
import { loadBank } from '../../utils/data-loader';
import PopupItemDetail from '@/components/base/popup-item-detail';
import printDocument from '@/utils/print-document';

export default {
  components: {
    DxButton,
    DxTextArea,
    DxLoadPanel,
    DxToolbar, DxItem,
    DxPopup, DxToolbarItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxCustomRule, DxRequiredRule,
    DxDataGrid, DxColumn, DxPaging, DxLookup, DxEditing, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, DxGridItem, DxGridToolbar, DxGridButton,
    DataGridClient, DataGridShipment, DataGridPurchaseOrder,
    PopupItemDetail,
  },
  props: {
    id: [String, Number],
  },
  setup(props) {
    // variable 설정
    const router = useRouter();
    const vars = {};
    vars.dlg = {};
    vars.dlg.finder = reactive({ title: '', key: null, data: null, show: false });
    vars.init = ref(false);
    vars.loading = ref(false);
    vars.formData = reactive({});
    vars.formState = reactive({ readOnly: true });
    vars.focus = reactive({ shipmentItem: null });
    vars.grid = { baseItem: null, shipmentItem: null };
    vars.disabled = reactive({
      new: false,
      edit: true,
      save: true,
      items: true,
      delete: true,
      tradeYn: false,
    });
    vars.filter = {};
    vars.filter.baseItem = { clientId: 0 };
    vars.filter.shipmentItem = [{ name: 'fk_import_shipment_id', op: 'eq', val: props.id || 0 }];
    vars.dataSource = reactive({
      origin: [],
      packing: [],
      payment: [],
      delivery: [],
      validity: [],
      adv_bank: [],
      currency: [],
      pay_terms: [],
      ship_port: [],
      inspection: [],
      destination: [],
      price_terms: [],
      employee: [],
      bank: [],
      baseItem: null,
      shipmentItem: getImportShipmentItem(vars.filter.shipmentItem),
    });

    vars.summary = {};
    vars.summary.total_price = computed(() => numeral(vars.formData.total_price).format('0,0.00'));

    vars.itemDetail = reactive({ visible: false, id: 0 });

    moment.locale('ko')

    onMounted(async () => {
      await loadBank(vars.dataSource);
      await methods.loadBaseCode();
      methods.initById(props.id);
    });

    // public methods
    const methods = {
      async initById(id) {
        await methods.refreshGridShipmentItem(id);
        if (!id) {
          methods.clearFormData();

          vars.disabled.edit = true;
          vars.disabled.delete = true;
          vars.disabled.save = true;
          vars.disabled.items = true;
          return;
        }

        let { data } = await importShipment.byKey(id);
        Object.assign(vars.formData, data);

        methods.enableDelete();
        vars.disabled.edit = false;
        if (vars.formData.supplier) {
          methods.enableSave();
          vars.disabled.items = false;
        }
      },
      clearFormData() {
        vars.formData.id = null;
        vars.formData.created = null;
        vars.formData.purchase_order = null;
        vars.formData.shipment_number = ''; // 선적번호
        vars.formData.shipment_date = ''; // 선적일자
        vars.formData.supplier = ''; // 공급업체
        vars.formData.buyer = ''; // 고객업체
        vars.formData.validity = ''; // 유효기간
        vars.formData.pay_terms = ''; // 결재조건
        vars.formData.destination = ''; // 도착지
        vars.formData.delivery = ''; // 
        vars.formData.price_terms = ''; // 가격조건
        vars.formData.origin = ''; // 원산지
        vars.formData.ship_port = ''; // 배송지
        vars.formData.packing = ''; // 포장
        vars.formData.adv_bank = ''; // 
        vars.formData.currency = ''; // 환종
        vars.formData.ex_rate = 0; // 환율
        vars.formData.inspection = ''; // 
        vars.formData.payment = ''; // 
        vars.formData.remark = ''; // 참고사항
        vars.formData.total_price = 0; // 합계금액
        vars.formData.fk_purchase_order_id = null; // 발주 ID
        vars.formData.fk_company_id = authService.getCompanyId();
        vars.formData.purchase_order = null;
      },
      createFindPopupFn(key, title, data = null) {
        const _key = key;
        const _title = title;
        const _data = data;
        return () => {
          vars.dlg.finder.key = _key;
          vars.dlg.finder.data = _data;
          vars.dlg.finder.title = _title;
          vars.dlg.finder.show = true;
        };
      },
      gridClear(grid) {
        if (grid) {
          grid.clearSelection();
          grid.refresh();
        }
      },
      async refreshGridShipmentItem(id) {
        if (!id) { id = 0; }
        vars.filter.shipmentItem[0].val = id;
        vars.dataSource.shipmentItem.defaultFilters = vars.filter.shipmentItem;
        if (vars.grid.shipmentItem) {
          vars.grid.shipmentItem.cancelEditData();
          vars.grid.shipmentItem.refresh();
        }
      },
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`import-shipment-${key}`, evt.component);
      },
      async newItem() {
        methods.refreshGridShipmentItem();
        if (vars.formData.id) {
          methods.redirect();
          vars.formData.id = null;
        }
        setTimeout(() => {
          vars.formData.created = null;
          vars.formData.shipment_date = currentDateTime();
          vars.formData.origin = methods.getFirstOrigin();
          vars.formData.packing = methods.getFirstPacking();
          vars.formData.payment = methods.getFirstPayment();
          vars.formData.adv_bank = methods.getFirstAdvBank();
          vars.formData.validity = methods.getFirstValidity();
          vars.formData.delivery = methods.getFirstDelivery();
          vars.formData.currency = methods.getFirstCurrency();
          vars.formData.pay_terms = methods.getFirstPayTerms();
          vars.formData.ship_port = methods.getFirstShipPort();
          vars.formData.inspection = methods.getFirstInspection();
          vars.formData.price_terms = methods.getFirstPriceTerms();
          vars.formData.destination = methods.getFirstDestination();
          vars.formData.fk_company_id = authService.getCompanyId();

          methods.setReadOnly(false);
        }, 200);
      },
      async editItem() {
        if (!vars.formData.id) { return; }
        const isReadOnly = methods.isReadOnly();
        if (isReadOnly) {
          let isSelect = await confirm('수정하시겠습니까?', '수정');
          if (!isSelect) { return; }
        }

        const saveFormData = Object.assign({}, vars.formData);
        methods.toggleReadOnly();
        methods.enableSave();
        methods.enableDelete();

        await nextTick();
        Object.assign(vars.formData, saveFormData);
      },
      async deleteItem() {
        const result = await confirm('이 항목을 삭제하시겠습니까?', '삭제 확인');
        if (result) {
          try {
            await importShipment.remove(vars.formData.id);
            await alert('삭제되었습니다', '삭제 확인');
            methods.redirect();
            methods.setReadOnly(true);
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
            const updateData = { ...vars.formData };
            delete updateData.purchase_order;

            await importShipment.update(vars.formData.id, updateData);
            await methods.saveGridShipmentItem();

            methods.setReadOnly(true);
            notifyInfo('저장되었습니다');

            methods.enableSave();
            methods.enableDelete();
          } else {
            // 채번이 없을 경우 자동 채번
            const insertData = { ...vars.formData };
            delete insertData.purchase_order;

            let { data } = await importShipment.insert(insertData);
            vars.formData.id = data.id;

            await methods.saveGridShipmentItem();

            methods.redirect(data.id);
            methods.setReadOnly(true);
            notifyInfo('저장되었습니다');
          }
        } catch (ex) {
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
      async saveGridShipmentItem() {
        if (vars.grid.shipmentItem) { 
          await vars.grid.shipmentItem.saveEditData(); 
        }
      },
      finderReturnHandler(data) {
        switch (vars.dlg.finder.key) {
          case 'shipment': {
            methods.redirect(data.id);
            methods.setReadOnly(true);
            break;
          }
          case 'purchase-order': {
            methods.setFormDataFromPurchaseOrder(data);
            break;
          }
          case 'enduser': {
            vars.formData.end_user = data.name;
            break;
          }
        }

        vars.dlg.finder.show = false;
        vars.dlg.finder.title = '';
        vars.dlg.finder.key = null;
        vars.dlg.finder.data = null;
      },
      async setFormDataFromPurchaseOrder(data) {
        vars.formData.supplier = data.supplier;
        vars.formData.buyer = data.buyer;
        vars.formData.validity = data.valid_period;
        vars.formData.pay_terms = data.pay_terms;
        vars.formData.destination = data.destination;
        vars.formData.delivery = data.delivery;
        vars.formData.price_terms = data.price_terms;
        vars.formData.origin = data.origin;
        vars.formData.ship_port = data.ship_port;
        vars.formData.packing = data.packing;
        vars.formData.adv_bank = data.adv_bank;
        vars.formData.currency = data.currency;
        vars.formData.ex_rate = data.ex_rate;
        vars.formData.inspection = data.inspection;
        vars.formData.payment = data.payment;
        vars.formData.remark = data.remark;
        vars.formData.fk_purchase_order_id = data.id;
        vars.formData.purchase_order = { ...data };

        methods.refreshGridShipmentItem();
        methods.insertShipmentItems(data.id);

        vars.disabled.edit = false;
        vars.disabled.delete = false;
        vars.disabled.save = false;
        vars.disabled.items = false;
      },
      async insertShipmentItems(importPurchaseOrderId) {
        const purchaseOrderItems = await methods.loadImportPurchaseOrderItems(importPurchaseOrderId)
        const grid = vars.grid.shipmentItem;
        for (const item of purchaseOrderItems) {
          if (item.not_shipment <= 0) { continue; }

          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = item.item_code; // 품목코드
          data.item = { ...item.item }; // 품목
          data.qty = item.not_shipment; // 수량
          data.import_price = item.import_price; // 수입단가
          data.amount = data.qty * data.import_price; // 총금액
          data.req_date = item.req_date; // 
          data.con_date = item.con_date; // 
          data.end_user = null; // 
          data.not_clearance = item.not_shipment; // 미통관
          data.not_publish = item.not_shipment; // 미발행
          data.closing_yn = false; // 종결
          data.fk_import_shipment_id = vars.formData.id; // 입고 ID
          data.fk_import_purchase_order_item_id = item.id; // 발주 ID
          data.import_purchase_order_item = { ...item }; // 발주 품목
        }
        grid.refresh();
      },
      async loadImportPurchaseOrderItems(importPurchaseOrderId) {
        const dsPurchaseOrderItem = getImportPurchaseOrderItem([{ name: 'fk_import_order_id', op: 'eq', val: importPurchaseOrderId }]);
        const { data: purchaseOrderItems } = await dsPurchaseOrderItem.load();
        return purchaseOrderItems;
      },
      async onEndUserChanged(e) {
        if (methods.isReadOnly()) { return; }
        const client = e.component.option('selectedItem');
        if (client) {
          if (client.trade_yn && !vars.disabled.tradeYn) {
            const result = await confirm('거래중지 업체입니다. 계속 진행하시겠습니까?', 'EndUser');
            if (!result) {
              vars.formData.end_user = e.previousValue;
              vars.disabled.tradeYn = true;
              return;
            }
          }
        }
        vars.disabled.tradeYn = false;
      },
      onFocusedCellChanged(e) {
        vars.focus.shipmentItem = e;
      },
      onDataError(e) {
        if (e.error.response.status == 605) {
          e.error.message = '연결된 데이터가 있어서 삭제가 안됩니다';
        } else if (e.error.response.status == 403) {
          e.error.message = '권한이 없습니다';
        }
      },
      onSavingItem(e) {
        e.changes.forEach((element) => {
          if (element.type != 'remove') {
            element.data.fk_import_shipment_id = vars.formData.id;
            delete element.data.item;
            delete element.data.import_purchase_order_item;
          }
        });
        methods.saveSummary();
      },
      saveSummary() {
        const priceData = { total_price: vars.formData.total_price };
        importShipment.update(vars.formData.id, priceData);
      },
      setQuantity(newData, value, currentRowData) {
        newData.not_clearance = currentRowData.not_clearance + (value - currentRowData.qty);
        newData.not_publish = currentRowData.not_publish + (value - currentRowData.qty);
        newData.qty = value;
        newData.import_price = currentRowData.import_price;
        newData.amount = newData.qty * newData.import_price;
      },
      setUnitPrice(newData, value, currentRowData) {
        newData.qty = currentRowData.qty;
        newData.import_price = value;
        newData.amount = newData.qty * newData.import_price;
      },
      calculateCustomSummary(options) {
        if (options.name === 'supply_price') {
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          } else if (options.summaryProcess === 'calculate') {
            options.totalValue += options.value.qty * options.value.import_price;
          } else if (options.summaryProcess === 'finalize') {
            vars.formData.total_price = options.totalValue;
          }
        }
      },
      bankNameFormat(value){
        if(!value) return '';
        return value.bank_code +" / "+ value.bank_name;
      },
      loadBaseCode() {
        return baseCodeLoader([
          'origin',
          'packing',
          'payment',
          'Validity',
          'delivery',
          'AdvBank',
          'currency',
          'Pay Terms',
          'Ship Port',
          'inspection',
          'destination',
          'Price Terms',
        ]).then((response) => {
          vars.dataSource.origin = response['origin'];
          vars.dataSource.packing = response['packing'];
          vars.dataSource.payment = response['payment'];
          vars.dataSource.adv_bank = response['AdvBank'];
          vars.dataSource.validity = response['Validity'];
          vars.dataSource.delivery = response['delivery'];
          vars.dataSource.currency = response['currency'];
          vars.dataSource.pay_terms = response['Pay Terms'];
          vars.dataSource.ship_port = response['Ship Port'];
          vars.dataSource.inspection = response['inspection'];
          vars.dataSource.price_terms = response['Price Terms'];
          vars.dataSource.destination = response['destination'];
        }).then(() => (vars.init.value = true));
      },
      checkPossibleSave() {
        if (vars.formData.supplier) {
          methods.enableSave();
          vars.disabled.items = false;
        }
      },
      getFirstOrigin() {
        return getFirstCodeNameInBaseCodeList(vars.dataSource.origin);
      },
      getFirstPacking() {
        return getFirstCodeNameInBaseCodeList(vars.dataSource.packing);
      },
      getFirstPayment() {
        return getFirstCodeNameInBaseCodeList(vars.dataSource.payment);
      },
      getFirstAdvBank() {
        return getFirstCodeNameInBaseCodeList(vars.dataSource.adv_bank);
      },
      getFirstValidity() {
        return getFirstCodeNameInBaseCodeList(vars.dataSource.validity);
      },
      getFirstDelivery() {
        return getFirstCodeNameInBaseCodeList(vars.dataSource.delivery);
      },
      getFirstCurrency() {
        return getFirstCodeNameInBaseCodeList(vars.dataSource.currency);
      },
      getFirstPayTerms() {
        return getFirstCodeNameInBaseCodeList(vars.dataSource.pay_terms);
      },
      getFirstShipPort() {
        return getFirstCodeNameInBaseCodeList(vars.dataSource.ship_port);
      },
      getFirstInspection() {
        return getFirstCodeNameInBaseCodeList(vars.dataSource.inspection);
      },
      getFirstPriceTerms() {
        return getFirstCodeNameInBaseCodeList(vars.dataSource.price_terms);
      },
      getFirstDestination() {
        return getFirstCodeNameInBaseCodeList(vars.dataSource.destination);
      },
      redirect(id) {
        if (id) { router.replace({ path: `/import/shipment/${id}` }); }
        else { router.replace({ path: `/import/shipment` }); }
      },
      itemPopupClick({ column, data }) {
        if (column.name === 'item_code') {
          vars.itemDetail.id = data.item.id;
          vars.itemDetail.visible = true;
        }
      },
      async printDocument() {
        if (!vars.formData.id) return;
        const params = { ...vars.formData };
        params.supply_price = numeral(vars.formData.supply_price).format('0,0');
        params.total_price = numeral(vars.formData.total_price).format('0,0');
        params.tax_price = numeral(vars.formData.total_price - vars.formData.supply_price).format('0,0');
        params.order_date = moment(vars.formData.order_date).format('YYYY년 M월 D일');
        params.delivery_date = moment(vars.formData.delivery_date).format('YYYY년 M월 D일');
        params.shipment_date = moment(vars.formData.shipment_date).format('YYYY년 M월 D일 dddd');

        params.adv_bank_info = {}
        const bank = vars.dataSource.bank.find(v => v.bank_code === vars.formData.adv_bank)
        if (bank) params.adv_bank_info = bank
        
        if (params.buyer) {
          const {data: buyerData} = await baseClient.load({filter: ['name', '=', params.buyer]})
          if (buyerData.length) params.buyer = buyerData[0]
          else params.buyer = { name: params.buyer, name_en: params.buyer, address_en: '' }
        }
        else params.buyer = {}

        if (params.supplier) {
          const {data: supplierData} = await baseClient.load({filter: ['name', '=', params.supplier]})
          if (supplierData.length) params.supplier = supplierData[0]
          else params.supplier = { name: params.supplier, name_en: params.supplier, address_en: '' }
        }
        else params.supplier = {}

        const orderManager = vars.dataSource.employee.find(
          (v) => v.emp_name === vars.formData.order_manager
        );
        if (orderManager) {
          params.order_manager = orderManager;
          const department = vars.dataSource.department.find((v) => v.id === orderManager.fk_department_id);
          if (department) {
            params.order_manager.department_name = department.department_name;
          }
        } else params.order_manager = { emp_name: vars.formData.order_manager };

        const { data: shipmentItem } = await vars.dataSource.shipmentItem.load();
        params.items = [...shipmentItem];
        params.items.forEach((item) => {
          item.qty_str = numeral(item.qty).format('0,0');
          item.import_price_str = numeral(item.import_price).format('0,0.00000');
          item.amount_str = numeral(item.amount).format('0,0.00');

          const { total_price } = calcPriceSummary(
            vars.formData.vat_type,
            item.amount
          );
          item.total_price = total_price
          item.total_price_str = numeral(total_price).format('0,0.00');
        });
        params.grouped = groupBy(params.items, 'item.hs_code')
        
        for(let key in params.grouped){
            params.grouped[key] = groupBy(params.grouped[key], 'item.item_group');
        }
        params.total_price = shipmentItem.reduce((t, a) => {
          t += a.amount
          return t
        }, 0)
        params.total_price_str = numeral(params.total_price).format('0,0.00')

        params.total_qty = shipmentItem.reduce((t, a) => {
          t += a.qty
          return t
        }, 0)
        params.total_qty_str = numeral(params.total_qty).format('0,0')
        
        params.unit = shipmentItem[0] ? shipmentItem[0].item.unit : ''
        await printDocument('importshipment', params);
      },
      enableDelete() {
        const isReadOnly = methods.isReadOnly();
        if (isReadOnly) { vars.disabled.delete = true; }
        else { vars.disabled.delete = false; }
      },
      enableSave() {
        const isReadOnly = methods.isReadOnly();
        if (isReadOnly) { vars.disabled.save = true; }
        else { vars.disabled.save = false; }
      },
      isReadOnly() {
        return vars.formState.readOnly;
      },
      setReadOnly(isReadOnly) {
        vars.formState.readOnly = isReadOnly;
      },
      toggleReadOnly() {
        vars.formState.readOnly = !vars.formState.readOnly;
      }
    };

    watch(
      () => props.id,
      () => methods.initById(props.id)
    );

    return {
      vars,
      methods,
      generateItemButtonOption,
    };
  },
};
</script>
<style>
.popup-message {
  text-align: center;
}
</style>
