<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">Purchase Order</div>
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
                data-field="order_number"
                :editor-options="{
                  placeholder: '(자동 or 직접입력)',
                  ...generateItemButtonOption('search', methods.createFindPopupFn('order', '발주조회')),
                }"
              >
                <dx-label text="P/O No" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="order_date" editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  ...vars.formState,
                }"
              >
                <dx-label text="OrderDate" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="supplier"
                :editor-options="{
                  onEnterKey: methods.createFindPopupFn('supplier', '업체조회', { name: vars.formData.supplier }),
                  ...generateItemButtonOption('search', methods.createFindPopupFn('supplier', '업체조회', { name: vars.formData.supplier })),
                  ...vars.formState,
                }"
              >
                <dx-label text="Supplier" :show-colon="false" />
                <dx-required-rule message="공급업체를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="supplier_contact"
                :editor-options="{
                  disabled: vars.disabled.clientManager,
                  acceptCustomValue: true,
                  ...vars.formState,
                }"
              >
                <dx-label text="SupplierContact" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="buyer" 
                :editor-options="{
                  onEnterKey: methods.createFindPopupFn('buyer', '업체조회', { name: vars.formData.buyer }),
                  ...generateItemButtonOption('search', methods.createFindPopupFn('buyer', '업체조회', { name: vars.formData.buyer })),
                  ...vars.formState,
                }"
              >
                <dx-label text="Buyer" :show-colon="false" />
              </dx-simple-item>
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
            </dx-group-item>

            <dx-group-item>
              <dx-simple-item data-field="owner_dept" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'department_name',
                  displayExpr: 'department_name',
                  dataSource: vars.dataSource.department,
                  onValueChanged: methods.onDepartmentChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="OwnerDept" :show-colon="false" />
                <dx-required-rule message="발주부서를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="member" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'emp_name',
                  displayExpr: 'emp_name',
                  disabled: vars.disabled.manager,
                  dataSource: vars.dataSource.employee,
                  ...vars.formState,
                }"
              >
                <dx-label text="Member" :show-colon="false" />
              </dx-simple-item>
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
              <dx-simple-item data-field="valid_period" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  dataSource: vars.dataSource.valid_period,
                  ...vars.formState,
                }"
              >
                <dx-label text="ValidPeriod" :show-colon="false" />
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
            </dx-group-item>

            <dx-group-item>
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
                  format: ',##0.00',
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

            <dx-group-item :col-span="2">
              <dx-simple-item data-field="remark" editor-type="dxTextArea" :editor-options="{
                  labelMode: 'hidden',
                  height: '200px',
                  placeholder: 'remark',
                  ...generateItemButtonOption('rename', methods.createFindPopupFn('remark', 'remark', vars.formData.remark)),
                  ...vars.formState,
                }"
              >
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
            :data-source="vars.dataSource.item1"
            :on-initialized="(evt) => methods.onGridInitialized(evt, 'item1')"
            @saving="methods.onSavingItem"
            @data-error-occurred="methods.onDataError"
            @cell-dbl-click="methods.itemPopupClick"
            @focused-cell-changed="methods.onFocusedCellChanged"
          >
            <dx-grid-toolbar>
              <dx-item template="addFromPlan" location="before" :visible="!vars.formState.readOnly" />
              <dx-grid-item name="addRowButton" :options="{ onClick: methods.showAddItemPopup }" />
              <dx-grid-item name="saveButton" :visible="!!vars.formData.id" />
              <dx-grid-item name="revertButton" />
              <dx-grid-item name="columnChooserButton" />
            </dx-grid-toolbar>
            <template #addFromPlan>
              <dx-button text="발주계획에서 가져오기" icon="add" @click="methods.showAddOrderPlanPopup" />
            </template>

            <dx-column caption="ItemCode" data-field="item_code" width="180" :allow-editing="false" />
            <dx-column caption="Name SubName" data-field="item.item_name" :allow-editing="false" />
            <dx-column caption="Qty" data-field="qty" data-type="number" format="fixedPoint" :set-cell-value="methods.setQuantity" />
            <dx-column caption="Unit" data-field="item.unit" data-type="number" :allow-editing="false" />
            <dx-column caption="ImportPrice" data-field="import_price" data-type="number" :format="',##0.00000'" :set-cell-value="methods.setUnitPrice" />
            <dx-column caption="Amount" data-field="amount" data-type="number" :format="methods.customFormat" />
            <dx-column caption="ReqDeliDate" data-field="req_date" data-type="date" format="yyyy-MM-dd" />
            <dx-column caption="ConDeliDate" data-field="con_date" data-type="date" format="yyyy-MM-dd" />
            <dx-column caption="NetPrice" data-field="net_price" data-type="number" :format="{ type: 'fixedPoint', precision: 4 }" />
            <dx-column caption="EndUser" data-field="end_user" />
            <dx-column caption="미LC" data-field="not_lc" data-type="number" format="fixedPoint" :allow-editing="false" />
            <dx-column caption="미선적" data-field="not_shipment" data-type="number" format="fixedPoint" :allow-editing="false" />
            <dx-summary :recalculate-while-editing="true" :calculate-custom-summary="methods.calculateCustomSummary">
              <dx-total-item name="supply_price" summary-type="custom" />
            </dx-summary>

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
              <th>합계금액:</th>
              <td>{{ vars.summary.total_price.value }}</td>
            </tr>
          </table>
        </div>
      </div>
    </div>

    <dx-popup
      title="발주품목찾기"
      content-template="popup-content"
      v-model:visible="vars.dlg.addItem.show"
      width="70%"
      :height="460"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="(evt) => methods.onGridInitialized(evt, 'find-item-popup')"
    >
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ text: '선택된 항목 추가', icon: 'add', onClick: methods.addSelectedRows }"
      />

      <template #popup-content>
        <dx-data-grid
          column-resizing-mode="widget"
          :show-borders="true"
          :remote-operations="true"
          :column-auto-width="true"
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
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :calculate-display-value="methods.availableStock" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :calculate-display-value="methods.currentStock" />

          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick" />
        </dx-data-grid>
      </template>
    </dx-popup>

    <dx-popup
      title="발주계획에서 가져오기"
      content-template="popup-content"
      v-model:visible="vars.dlg.addOrderPlanItem.show"
      width="70%"
      :height="460"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="(evt) => methods.onGridInitialized(evt, 'load-order-popup')"
    >
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ text: '선택된 항목 추가', icon: 'add', onClick: methods.addSelectedOrderPlanRows }"
      />

      <template #popup-content>
        <dx-data-grid
          column-resizing-mode="widget"
          :show-borders="true"
          :remote-operations="true"
          :column-auto-width="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="vars.dataSource.planItem"
          :on-initialized="(evt) => methods.onGridInitialized(evt, 'planItem')"
        >
          <dx-column caption="발주계획번호" data-field="order_plan.order_plan_number" :sort-index="1" sort-order="desc" />
          <dx-column caption="발주계획일자" data-field="order_plan.order_plan_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="발주계획수량" data-field="order_plan_quantity" />
          <dx-column caption="단가" data-field="unit_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="금액" data-field="supply_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
          <dx-column caption="요청납기" data-field="request_delivery_date" />
          <dx-column caption="미발주" data-field="unordered_quantity" />
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" />
          <dx-column caption="수주번호" data-field="order_number" />
          <dx-column caption="주공급업체" data-field="main_supplier" />
          <dx-column caption="고객사품번" data-field="client_item_number" />

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
      :resize-enabled="true"
      :close-on-outside-click="true"
      :key="vars.dlg.finder.key"
      :title="vars.dlg.finder.title"
      @initialized="(evt) => methods.onGridInitialized(evt, 'multiuse-popup')"
    >
      <template #popup-content>
        <data-grid-client  v-if="vars.dlg.finder.key === 'supplier'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-client  v-else-if="vars.dlg.finder.key === 'buyer'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-client  v-else-if="vars.dlg.finder.key === 'enduser'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-purchase-order v-else-if="vars.dlg.finder.key === 'order'" @change="methods.finderReturnHandler" />

        <div v-else-if="vars.dlg.finder.key === 'remark'">
          <div class="mb-2">
            <dx-text-area :height="190" :value="vars.dlg.finder.data" @update:value="methods.updateEtcValue" />
          </div>
          <dx-toolbar>
            <dx-item widget="dxButton" toolbar="top" location="after" :options="{ text: '닫기', icon: null, onClick: methods.finderReturnHandler }" />
          </dx-toolbar>
        </div>
      </template>
    </dx-popup>

    <popup-item-detail :item-id="vars.itemDetail.id" v-model:visible="vars.itemDetail.visible" />
  </div>
</template>

<script>
import moment from 'moment';
import numeral from 'numeral';

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
import { DxDataGrid, DxColumn, DxPaging, DxLookup, DxEditing, DxSorting, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, 
  DxItem as DxGridItem, DxToolbar as DxGridToolbar, DxButton as DxGridButton } from 'devextreme-vue/data-grid';

import stateStore from '@/utils/state-store';
import { getPurchaseOrderPlanItem } from '../../data-source/purchase';
import { importPurchaseOrder, getImportPurchaseOrderItem } from '../../data-source/import';

import { baseItem, baseCodeLoader, baseClient, getBaseItem } from '../../data-source/base';
import { getStock } from '../../data-source/setup';
import DataGridClient from '../../components/base/data-client.vue';
import DataGridPurchaseOrder from '../../components/import/data-purchase-order.vue';
import DataGridProject from '../../components/project/data-project.vue';
import authService from '../../auth';
import { calcPriceSummary, generateItemButtonOption, currentDateTime } from '../../utils/util';
import { loadEmployee, loadWarehouse, loadDepartment, loadClientManager, loadBank } from '../../utils/data-loader';
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
    DxDataGrid, DxColumn, DxPaging, DxLookup, DxEditing, DxSorting, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, DxGridItem, DxGridToolbar, DxGridButton,
    DataGridPurchaseOrder, DataGridClient, DataGridProject,
    PopupItemDetail,
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
    vars.grid = { baseItem: null, planItem: null, item1: null };
    vars.dlg.addItem = reactive({ show: false });
    vars.dlg.addOrderPlanItem = reactive({ show: false });
    vars.dlg.finder = reactive({ title: '', show: false, key: null, data: null });
    vars.warehouse = {};
    vars.filter = {};
    vars.filter.baseItem = { clientId: 0 };
    vars.filter.planItem = { clientCompany: '' };
    vars.filter.item1 = [{ name: 'fk_import_order_id', op: 'eq', val: props.id || 0 }];
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
      destination: [],
      valid_period: [],
      delivery: [],
      price_terms: [],
      origin: [],
      ship_port: [],
      packing: [],
      adv_bank: [],
      currency: [],
      inspection: [],
      payment: [],
      pay_terms: [],
      order_type: [],
      vat_type: [],
      delivery_place: [],
      client_manager: [],
      department: [],
      employee: [],
      warehouse: [],
      bank: [],
      baseItem: null,
      planItem: null,
      item1: getImportPurchaseOrderItem(vars.filter.item1),
    });
    vars.focus = reactive({ item1: null });
    vars.formData = reactive({});

    vars.summary = {};
    vars.summary.supply_price = computed(() => '₩' + numeral(vars.formData.supply_price).format('0,0'));
    vars.summary.vat = computed(() => '₩' + numeral(vars.formData.vat).format('0,0'));
    vars.summary.total_price = computed(() => numeral(Math.floor(vars.formData.total_price * 100) / 100).format('0,0.00'));

    vars.itemDetail = reactive({ visible: false, id: 0 });

    onMounted(async () => {
      await loadDepartment(vars.dataSource);
      await loadBank(vars.dataSource);
      await methods.loadBaseCode();
      methods.initById(props.id);
      loadWarehouse(vars.dataSource);
    });

    // public methods
    const methods = {
      async initById(id) {
        await methods.gridItem1Refresh(id);
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

        let { data } = await importPurchaseOrder.byKey(id);
        Object.assign(vars.formData, data);

        methods.enableDelete();
        vars.disabled.edit = false;
        if (vars.formData.supplier && vars.formData.owner_dept) {
          methods.enableSave();
          vars.disabled.items = false;
        }
        methods.onSupplierChanged();
      },
      clearFormData() {
        vars.formData.id = null;
        vars.formData.created = null;
        vars.formData.order_number = '';
        vars.formData.order_date = '';
        vars.formData.supplier = '';
        vars.formData.supplier_contact = '';
        vars.formData.buyer = '';
        vars.formData.owner_dept = '';
        vars.formData.member = '';
        vars.formData.pay_terms = '';
        vars.formData.destination = '';
        vars.formData.valid_period = '';
        vars.formData.delivery = '';
        vars.formData.price_terms = '';
        vars.formData.origin = '';
        vars.formData.ship_port = '';
        vars.formData.packing = '';
        vars.formData.adv_bank = '';
        vars.formData.currency = '';
        vars.formData.ex_rate = 0;
        vars.formData.inspection = '';
        vars.formData.payment = '';
        vars.formData.remark = '';
        vars.formData.fk_company_id = authService.getCompanyId();
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
          // const basicStock = row.basic_stock ? { ...row.basic_stock } : { current_stock: 0, available_stock: 0 };

          let importPrice = row.purchase_price;
          const { data: item } = await baseItem.load({
            filter: [['item_code', '=', row.item_code]]
          });
          if (item.length > 0) {
            if (item[0].client_item && item[0].client_item.length > 0) {
              for (const clientItem of item[0].client_item) {
                if (clientItem.unit_price_type == '수입단가' && clientItem.client_id == vars.filter.baseItem.clientId) {
                  importPrice = clientItem.unit_price;
                  break;
                }
              }
            }
          }

          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code; // 품목코드
          data.qty = 0; // 발주수량
          data.import_price = importPrice; // 수입단가
          data.amount = 0; // 총금액
          data.req_date = null; // 요청 일자
          data.con_date = null; // 확인 일자
          data.net_price = 0; //
          data.end_user = '';
          data.not_lc = 0; // 미LC
          data.not_shipment = 0;// 미선적
          data.order_plan_number = null; // 발주계획번호
          data.fk_order_plan_item_id = null; // 발주계획품목 ID
          data.fk_import_order_id = vars.formData.id; // 발주 ID
          data.item = { ...row }; // 품목
          // data.basic_stock = { ...basicStock }; // 기초재고
          // data.warehouse = { ...vars.warehouse }; // 입고창고
          // data.warehouse_code = vars.warehouse.wh_code; // 창고코드
        }
        grid.refresh();
        vars.dlg.addItem.show = false;
      },
      async addSelectedOrderPlanRows() {
        const grid = vars.grid.item1;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }
        
        const rows = await vars.grid.planItem.getSelectedRowsData();
        for (let row of rows) {
          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code; // 품목코드
          data.qty = row.unordered_quantity; // 발주수량
          data.import_price = row.unit_price ? row.unit_price : 0; // 수입단가
          data.amount = data.qty * data.import_price; // 총금액
          data.req_date = null; // 요청 일자
          data.con_date = null; // 확인 일자
          data.net_price = 0; //
          data.end_user = row.end_user;
          data.not_lc = data.qty; // 미LC
          data.not_shipment = data.qty;// 미선적
          data.order_plan_number = row.order_plan.order_plan_number; // 발주계획번호
          data.fk_order_plan_item_id = row.id; // 발주계획품목 ID
          data.fk_import_order_id = vars.formData.id; // 발주 ID
          data.item = { ...row }; // 품목
          // data.basic_stock = { ...row.basic_stock }; // 기초재고
          // data.warehouse = { ...vars.warehouse }; // 입고창고
          // data.warehouse_code = vars.warehouse.wh_code; // 창고코드
        }
        grid.refresh();
        vars.dlg.addOrderPlanItem.show = false;
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
      showAddItemPopup() {
        methods.gridClear(vars.grid.baseItem);
        vars.dlg.addItem.show = true;
      },
      showAddOrderPlanPopup() {
        methods.gridClear(vars.grid.planItem);
        vars.dlg.addOrderPlanItem.show = true;
      },
      gridClear(grid) {
        if (grid) {
          grid.clearSelection();
          grid.refresh();
        }
      },
      async gridItem1Refresh(id) {
        if (!id) id = 0;
        vars.filter.item1[0].val = id;
        vars.dataSource.item1.defaultFilters = vars.filter.item1;
        if (vars.grid.item1) {
          vars.grid.item1.cancelEditData();
          vars.grid.item1.refresh();
        }
      },
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`import-purchase-order-${key}`, evt.component);
      },
      async newItem() {
        methods.gridItem1Refresh();
        if (vars.formData.id) {
          methods.clearFormData();
          methods.redirect();
          vars.formData.id = null;
        }
        setTimeout(() => {
          methods.clearFormData();
          vars.formData.created = null;
          vars.formData.order_date = currentDateTime();
          vars.formData.owner_dept = authService.getDepartmentName();
          vars.formData.member = authService.getUserName();
          vars.formData.pay_terms = methods.getFirstPaymentTerms();
          vars.formData.destination = methods.getFirstDestination();
          vars.formData.valid_period = methods.getFirstValidPeriod();
          vars.formData.delivery = methods.getFirstDelivery();
          vars.formData.price_terms = methods.getFirstPriceTerms();
          vars.formData.origin = methods.getFirstOrigin();
          vars.formData.ship_port = methods.getFirstShipPort();
          vars.formData.packing = methods.getFirstPacking();
          vars.formData.adv_bank = methods.getFirstAdvBank();
          vars.formData.currency = methods.getFirstCurrency();
          vars.formData.inspection = methods.getFirstInspection();
          vars.formData.payment = methods.getFirstPayment();
          vars.formData.fk_company_id = authService.getCompanyId();

          vars.formState.readOnly = false;
        }, 200);
      },
      async editItem() {
        if (!vars.formData.id) return;
        if (vars.formState.readOnly) {
          let isSelect = await confirm('수정하시겠습니까?', '수정');
          if (!isSelect) { return; }
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
            await importPurchaseOrder.remove(vars.formData.id);
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
            await importPurchaseOrder.update(vars.formData.id, vars.formData);
            if (vars.grid.item1) { await vars.grid.item1.saveEditData(); }

            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');

            methods.enableSave();
            methods.enableDelete();
          } else {
            // 채번이 없을 경우 자동 채번
            let { data } = await importPurchaseOrder.insert(vars.formData);
            vars.formData.id = data.id;

            const gridItem1 = vars.grid.item1;
            if (gridItem1 && gridItem1.hasEditData()) {
              await gridItem1.saveEditData();
            }

            methods.redirect(data.id);
            vars.formState.readOnly = true;
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
      finderReturnHandler(data) {
        switch (vars.dlg.finder.key) {
          case 'order': {
            methods.redirect(data.id);
            vars.formState.readOnly = true;
            break;
          }
          case 'supplier': {
            vars.formData.supplier = data.name;
            methods.onSupplierChanged();
            break;
          }
          case 'buyer': {
            vars.formData.buyer = data.name;
            break;
          }
          case 'enduser': {
            vars.formData.end_user = data.name;
            break;
          }
          case 'remark': {
            vars.formData.remark = vars.dlg.finder.data;
            break;
          }
        }

        vars.dlg.finder.title = '';
        vars.dlg.finder.key = null;
        vars.dlg.finder.data = null;
        vars.dlg.finder.show = false;
      },
      validateExistClient({ value }) {
        const client = vars.dataSource.supplier.find((client) => client.name === value);
        return !!client;
      },
      async onSupplierChanged() {
        const inputValue = vars.formData.supplier;
        const { data } = await baseClient.load({
          filter: [
            ['fk_company_id', '=', authService.getCompanyId()],
            ['name', '=', inputValue],
          ],
          take: 1,
          skip: 0,
        });
        const client = data.length > 0 ? data[0] : null;

        vars.filter.baseItem.clientId = client ? client.id : 0;
        methods.loadBaseItem();

        vars.filter.planItem.clientCompany = client ? client.name : '';
        methods.loadPlanItem();

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
              vars.formData.supplier_contact = null;
            } else {
              vars.formData.supplier = '';
              vars.disabled.tradeYn = true;
              vars.formData.supplier_contact = null;
            }
          }
        }
        methods.checkPossibleSave();
      },
      async onEndUserChanged(e) {
        if (vars.formState.readOnly) { return; }

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
      async onConfirmChanged(e) {
        if (!vars.formData.id) { return; }
        if (e.value) {
          vars.formState.readOnly = true;
          vars.disabled.edit = true;
          vars.disabled.delete = true;
          vars.disabled.items = true;
        } else {
          if (vars.formData.supplier && vars.formData.owner_dept) {
            methods.enableDelete();
            vars.disabled.edit = false;
            vars.disabled.items = false;
          }
        }
      },
      bankNameFormat(value){
        if(!value) return '';
        return value.bank_code +" / "+ value.bank_name;
      },
      updateEtcValue(v) {
        vars.dlg.finder.data = v;
      },
      onDepartmentChanged(e) {
        if (!e.value) {
          methods.enableSave();
          vars.disabled.items = true;
          vars.disabled.manager = true;
          vars.formData.member = null;
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
        methods.loadPlanItem();
      },
      onFocusedCellChanged(e) {
        vars.focus.item1 = e;
      },
      onDataError(e) {
        if (e.error.response.status == 605) {
          e.error.message = '연결된 데이터가 있어서 삭제가 안됩니다';
        } else if (e.error.response.status == 403) {
          e.error.message = '권한이 없습니다';
        }
      },
      availableStock(rowData) {
        if (!rowData.basic_stock) { return '0'; }
        return rowData.basic_stock.available_stock;
      },
      currentStock(rowData) {
        if (!rowData.basic_stock) { return '0'; }
        return rowData.basic_stock.current_stock;
      },
      onSavingItem(e) {
        e.changes.forEach((element) => {
          if (element.type != 'remove') {
            element.data.fk_import_order_id = vars.formData.id;
            delete element.data.item;
            delete element.data.order;
            delete element.data.order_plan_item;
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
        importPurchaseOrder.update(vars.formData.id, priceData);
      },
      async setWarehouse(newData, value, currentRowData) {
        const warehouseList = vars.dataSource.warehouse;
        for (let i = 0; i < warehouseList.length; i++) {
          if (warehouseList[i].wh_name == value) {
            newData.warehouse = { ...warehouseList[i] };
            newData.warehouse_code = warehouseList[i].wh_code;

            const { basicStock } = await getStock(currentRowData.item_code, newData.warehouse_code);
            newData.basic_stock = { ...basicStock };
            break;
          }
        }
      },
      setQuantity(newData, value, currentRowData) {
        newData.not_lc = currentRowData.not_lc + (value - currentRowData.qty);
        newData.not_shipment = currentRowData.not_shipment + (value - currentRowData.qty);
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
      customFormat(value){
        return numeral(Math.floor(value * 100) / 100).format('0,0.00');
      },
      loadBaseCode() {
        return baseCodeLoader([
          'Pay Terms',
          'destination',
          'ValidPeriod',
          'delivery',
          'Price Terms',
          'origin',
          'Ship Port',
          'packing',
          'AdvBank',
          'currency',
          'inspection',
          'payment'
        ])
          .then((response) => {
            vars.dataSource.pay_terms = response['Pay Terms'];
            vars.dataSource.destination = response['destination'];
            vars.dataSource.valid_period = response['ValidPeriod'];
            vars.dataSource.delivery = response['delivery'];
            vars.dataSource.price_terms = response['Price Terms'];
            vars.dataSource.origin = response['origin'];
            vars.dataSource.ship_port = response['Ship Port'];
            vars.dataSource.packing = response['packing'];
            vars.dataSource.adv_bank = response['AdvBank'];
            vars.dataSource.currency = response['currency'];
            vars.dataSource.inspection = response['inspection'];
            vars.dataSource.payment = response['payment'];
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
      loadPlanItem() {
        vars.dataSource.planItem = getPurchaseOrderPlanItem([
          {
            name: 'main_supplier',
            op: 'eq',
            val: vars.filter.planItem.clientCompany,
          },
          {
            name: 'unordered_quantity',
            op: 'gt',
            val: 0,
          },
        ]);
      },
      checkPossibleSave() {
        if (vars.formData.supplier && vars.formData.owner_dept) {
          methods.enableSave();
          vars.disabled.items = false;
        }
      },
      getFirstPaymentTerms() {
        return methods.getFirstItemName(vars.dataSource.pay_terms);
      },
      getFirstDestination() {
        return methods.getFirstItemName(vars.dataSource.destination);
      },
      getFirstValidPeriod() {
        return methods.getFirstItemName(vars.dataSource.valid_period);
      },
      getFirstDelivery() {
        return methods.getFirstItemName(vars.dataSource.delivery);
      },
      getFirstPriceTerms() {
        return methods.getFirstItemName(vars.dataSource.price_terms);
      },
      getFirstOrigin() {
        return methods.getFirstItemName(vars.dataSource.origin);
      },
      getFirstShipPort() {
        return methods.getFirstItemName(vars.dataSource.ship_port);
      },
      getFirstPacking() {
        return methods.getFirstItemName(vars.dataSource.packing);
      },
      getFirstAdvBank() {
        return methods.getFirstItemName(vars.dataSource.adv_bank);
      },
      getFirstCurrency() {
        return methods.getFirstItemName(vars.dataSource.currency);
      },
      getFirstInspection() {
        return methods.getFirstItemName(vars.dataSource.inspection);
      },
      getFirstPayment() {
        return methods.getFirstItemName(vars.dataSource.payment);
      },
      getFirstItemName(itemList) {
        if (!itemList || itemList.length <= 0) { return ''; }
        return itemList[0].code_name;
      },
      redirect(id) {
        if (id) { router.replace({ path: `/import/purchase-order/${id}` }); }
        else { router.replace({ path: `/import/purchase-order` }); }
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
        params.total_price = numeral(Math.floor(vars.formData.total_price * 100) / 100).format('0,0.00');
        params.order_date = moment(vars.formData.order_date).format('YYYY년 M월 D일');
        // params.delivery_date = moment(vars.formData.delivery_date).format('YYYY년 M월 D일');

        // const orderManager = vars.dataSource.employee.find((v) => v.emp_name === vars.formData.member);
        // if (orderManager) {
        //   params.order_manager = orderManager;
        //   const department = vars.dataSource.department.find((v) => v.id === orderManager.fk_department_id);
        //   if (department) {
        //     params.order_manager.department_name = department.department_name;
        //   }
        // } else {
        //   params.order_manager = { emp_name: vars.formData.order_manager };
        // }

        const { data: item1 } = await vars.dataSource.item1.load();

        params.items = [...item1];
        const { data : buyer_client } = await baseClient.load({
          filter: [
            ['name', '=', params.buyer]
          ]
        })
        const { data : supplier_client } = await baseClient.load({
          filter: [
            ['name', '=', params.supplier]
          ]
        })
        params.remark = typeof params.remark === 'string' ? params.remark.replace(/\n/g, '<br>') : '';
        params.supplier_contact = vars.formData.supplier_contact ? vars.formData.supplier_contact : "";
        params.supplier_ceo_name_en = supplier_client[0].ceo_name_en;
        params.buyer_address_en = buyer_client[0].address_en;
        params.buyer_name_en = buyer_client[0].name_en;
        // params.items.forEach((item) => {
        //   item.unit_price = numeral(item.unit_price).format('0,0');
        //   item.supply_price = numeral(item.supply_price).format('0,0');

        //   const { total_price } = calcPriceSummary(vars.formData.vat_type, item.supply_price);
        //   item.total_price = numeral(total_price).format('0,0');
        // });

        // const clientManager = vars.dataSource.client_manager.find((v) => v.name === vars.formData.client_manager);
        // if (clientManager) { params.client_manager = clientManager; }
        // else { params.client_manager = { name: vars.formData.client_manager }; }
        
        await printDocument('import-purchase-order', params);
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
