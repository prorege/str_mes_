<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">

        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">견적(수기)</div>
            </dx-item>
            <!-- 상단 메뉴 -->
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{ text: '신규', type: 'add', icon: 'add', onClick: methods.newItem }"
            />
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{ text: '수정', type: 'rename', icon: 'rename', onClick: methods.editItem, disabled: vars.disabled.edit }"
            />
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{ text: '삭제', type: 'remove', icon: 'remove', onClick: methods.deleteItem, disabled: vars.disabled.delete }"
            />
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{ text: '저장', type: 'save', icon: 'save', onClick: methods.saveItem, disabled: vars.disabled.save }"
            />
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{ text: '복사', type: 'copy', icon: 'copy', onClick: methods.copyItem, disabled: vars.disabled.copy }"
            />
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{ text: '출력', type: 'print', icon: 'print', onClick: methods.printDocument }"
            />
          </dx-toolbar>
        </div>

        <dx-form :form-data="vars.formData" @field-data-changed="methods.checkPossibleSave">
          <dx-group-item :col-count="5">
            <dx-group-item>
              <dx-simple-item data-field="quote_number"
                :editor-options="{
                  placeholder: '(자동 or 직접입력)',
                  ...generateItemButtonOption('search', methods.createFindPopupFn('quote', '견적조회'))
                }"
              >
                <dx-label text="견적번호" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="quote_date" editor-type="dxDateBox"
                :editor-options="{ dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss', ...vars.formState }"
              >
                <dx-label text="견적일자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="client_company"
                :editor-options="{...vars.formState}"
              >
                <dx-label text="고객업체" :show-colon="false" />
                <dx-required-rule message="고객업체를 입력하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="client_manager"
                :editor-options="{...vars.formState}"
              >
                <dx-label text="업체담당자" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="quote_department" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'department_name',
                  displayExpr: 'department_name',
                  acceptCustomValue: true,
                  dataSource: vars.dataSource.department,
                  onValueChanged: methods.onDepartmentChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="견적부서" :show-colon="false" />
                <dx-required-rule message="견적부서를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="quote_manager" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'emp_name',
                  displayExpr: 'emp_name',
                  dataSource: vars.dataSource.employee,
                  disabled: vars.disabled.manager,
                  ...vars.formState,
                }"
              >
                <dx-label text="견적담당자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="quote_type" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  dataSource: vars.dataSource.quote_type,
                  ...vars.formState,
                }"
              >
                <dx-label text="견적구분" :show-colon="false" />
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
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="payment_terms"
                :editor-options="vars.formState"
              >
                <dx-label text="결재조건" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="delivery_date" editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  ...vars.formState,
                }"
              >
                <dx-label text="납품기한" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="delivery_place" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.delivery_place,
                  displayExpr: 'code_name',
                  valueExpr: 'code_name',
                  acceptCustomValue: true,
                  ...vars.formState,
                }"
              >
                <dx-label text="납품장소" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="previous_quote_number"
                :editor-options="{ ...vars.formState }"
              >
                <dx-label text="이전견적번호" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="project_number"
                :editor-options="{
                  ...generateItemButtonOption(
                    'search',
                    methods.createFindPopupFn('project', '프로젝트조회')
                  ),
                  ...vars.formState,
                }"
              >
                <dx-label text="프로젝트번호" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="end_user"
                :editor-options="{
                  ...generateItemButtonOption(
                    'search',
                    methods.createFindPopupFn('enduser', '고객조회')
                  ),
                  ...vars.formState,
                }"
              >
                <dx-label text="EndUser" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="note" :editor-options="{ ...vars.formState }">
                <dx-label text="참고사항" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="order_number">
                <dx-label text="수주번호" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item
                data-field="confirmed"
                editor-type="dxCheckBox"
                :visible="true"
                :editor-options="{ onValueChanged: methods.onConfirmChanged }"
              >
                <dx-label text="견적확정" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="etc" editor-type="dxTextArea"
                :editor-options="{
                  ...generateItemButtonOption('rename', methods.createFindPopupFn('etc', '비고', vars.formData.etc)),
                  ...vars.formState,
                  height: '130px',
                  labelMode: 'hidden',
                  placeholder: '비고',
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
          <dx-item title="견적품목입력">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 470px)"
                  date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                  :show-borders="true"
                  :column-auto-width="true"
                  :remote-operations="false"
                  :focused-row-enabled="true"
                  :allow-column-resizing="true"
                  :allow-column-reordering="true"
                  :select-text-on-edit-start="true"
                  :disabled="vars.disabled.items"
                  :data-source="vars.dataSource.item1"
                  :on-initialized="evt => methods.onGridInitialized(evt, 'item1')"
                  @saving="methods.onSavingItem"
                  @init-new-row="methods.onItem2Insert"
                  @focused-cell-changed="methods.onFocusedCellChanged2"
                >
                  <dx-column caption="품목코드" data-field="item_code" width="180" />
                  <dx-column data-field="item_name" caption="품명" />
                  <dx-column data-field="item_standard" caption="규격" />
                  <dx-column caption="견적수량" data-field="quote_quantity" data-type="number" format="fixedPoint" :set-cell-value="methods.setQuantity" />
                  <dx-column caption="단가" data-field="unit_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :set-cell-value="methods.setUnitPrice" />
                  <dx-column data-field="unit" caption="단위" />
                  <dx-column caption="공급가" data-field="supply_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :allow-editing="false" :calculate-cell-value="methods.calcSupplyPrice" />
                  <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
                  <dx-column caption="출고창고" data-field="warehouse.wh_name" :set-cell-value="methods.setWarehouse">
                    <dx-lookup value-expr="wh_name" display-expr="wh_name" :data-source="vars.dataSource.warehouse" />
                  </dx-column>
                  <dx-column caption="고객사품번" data-field="client_item_number" />
                  <dx-column caption="품목설명" data-field="item_detail" />
                  <dx-column caption="참고사항" data-field="note" />
                  <dx-column caption="프로젝트번호" data-field="project_number"
                    :editor-options="{ ...generateItemButtonOption('search', methods.createFindPopupFn('project3', '프로젝트조회')) }"
                  />
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
      title="견적품목찾기"
      content-template="popup-content"
      v-model:visible="vars.dlg.addItem.show"
      :width="680"
      :height="460"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'item-popup')"
    >
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ text: '선택된 항목 추가', icon: 'add', onClick: methods.addSelectedRows }"
      />

      <template #popup-content>
        <dx-data-grid
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
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :calculate-display-value="methods.availableStock" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :calculate-display-value="methods.currentStock" />

          <dx-paging :page-size="20" />
          <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick" />
          <dx-filter-row :visible="true" />
        </dx-data-grid>
      </template>
    </dx-popup>

    <dx-popup
      content-template="popup-content"  
      v-model:visible="vars.dlg.finder.show"
      :width="680"
      :height="500"
      :key="vars.dlg.finder.key"
      :title="vars.dlg.finder.title"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'find-popup')"
    >
      <template #popup-content>
        <data-grid-client v-if="vars.dlg.finder.key === 'client'" @change="methods.finderReturnHandler" />
        <data-grid-client v-else-if="vars.dlg.finder.key === 'enduser'" @change="methods.finderReturnHandler" />
        <data-grid-quote v-else-if="vars.dlg.finder.key === 'quote'" @change="methods.finderReturnHandler" />
        <data-grid-project v-else-if="vars.dlg.finder.key === 'project'" @change="methods.finderReturnHandler" />
        <data-grid-project v-else-if="vars.dlg.finder.key === 'project2'" @change="methods.finderReturnHandler" />
        <data-grid-project v-else-if="vars.dlg.finder.key === 'project3'" @change="methods.finderReturnHandler" />
        <div v-else-if="vars.dlg.finder.key === 'etc'">
          <div class="mb-2">
            <dx-text-area
              :height="440"
              :value="vars.dlg.finder.data"
              @update:value="methods.updateEtcValue"
            />
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
  </div>
</template>

<script>
import moment from 'moment';
import numeral from 'numeral';

import { useRouter } from 'vue-router';
import { ref, reactive, computed, watch, nextTick, onMounted } from 'vue';

import { DxButton } from 'devextreme-vue/button';
import DxTextArea from 'devextreme-vue/text-area';
import { DxTabPanel } from 'devextreme-vue/tab-panel';
import { confirm, alert } from 'devextreme/ui/dialog';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxCustomRule, DxRequiredRule } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxLookup, DxEditing, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, 
  DxToolbar as DxGridToolbar, DxItem as DxGridItem, DxButton as DxGridButton } from 'devextreme-vue/data-grid';

import { getStock } from '../../data-source/setup';
import { baseClient, getBaseItem, baseCodeLoader } from '../../data-source/base';
import { shipmentQuoteManual, getShipmentQuoteManualItem } from '../../data-source/shipment';

import DataGridClient from '../../components/base/data-client.vue';
import DataGridQuote from '../../components/shipment/data-quote-manual.vue';
import DataGridProject from '../../components/project/data-project.vue';

import authService from '../../auth';
import ApiService from '../../utils/api-service';
import stateStore from '@/utils/state-store';
import printDocument from '@/utils/print-document';
import { notifyInfo, notifyError } from '../../utils/notify';
import { humanize, calcPriceSummary, generateItemButtonOption, beforeExitConfirm, currentDateTime } from '../../utils/util';
import { loadEmployee, loadWarehouse, loadDepartment, loadClientManager } from '../../utils/data-loader';

import PopupItemDetail from '@/components/base/popup-item-detail';

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
    DxGridToolbar, DxGridItem, DxGridButton,
    DataGridClient, DataGridQuote, DataGridProject,
    PopupItemDetail,
  },
  props: {
    id: [String, Number],
  },
  setup(props) {
    // variable 설정
    const router = useRouter();
    const apiExportToOrder = new ApiService('/api/mes/v1/shipment/quote/export/order');
    const vars = {};
    vars.init = ref(false);
    vars.loading = ref(false);
    vars.formState = reactive({ readOnly: true });
    vars.grid = { baseItem: null, item1: null, item2: null };
    vars.dlg = {};
    vars.dlg.addItem = reactive({ show: false });
    vars.dlg.finder = reactive({ show: false, title: '', key: null, data: null });
    vars.dlg.print = reactive({ show: false });
    vars.warehouse = {};
    vars.filter = {};
    vars.filter.baseItem = { clientId: null };
    vars.filter.item1 = [{ name: 'fk_quote_id', op: 'eq', val: props.id || 0 }]
    vars.disabled = reactive({
      copy: true,
      edit: true,
      delete: true,
      save: true,
      manger: true,
      clientManager: true,
      tradeYn: false,
    });
    vars.dataSource = reactive({
      payment_terms: [],
      quote_type: [],
      vat_type: [],
      delivery_place: [],
      client_manager: [],
      department: [],
      employee: [],
      warehouse: [],
      baseItem: null,
      item1: getShipmentQuoteManualItem(vars.filter.item1),
    });
    vars.formData = reactive({});
    vars.summary = {};
    vars.summary.supply_price = computed(() => '₩' + numeral(vars.formData.supply_price).format('0,0'));
    vars.summary.vat = computed(() => '₩' + numeral(vars.formData.vat).format('0,0'));
    vars.summary.total_price = computed(() => '₩' + numeral(vars.formData.total_price).format('0,0'));
    vars.itemDetail = reactive({ visible: false, id: 0 });
    vars.focus = { item1: null, item2: null };

    onMounted(async () => {
      await loadDepartment(vars.dataSource);
      await methods.loadBaseCode();
      methods.initById(props.id);
      loadWarehouse(vars.dataSource);
    });

    // public methods
    const methods = {
      async initById(id) {
        beforeExitConfirm.check(() => { return !vars.disabled.save })
        methods.gridItem1Refresh(id);
        if (!id) {
          methods.clearFormData();

          vars.disabled.copy = true;
          vars.disabled.edit = true;
          vars.disabled.delete = true;
          vars.disabled.save = true;
          vars.disabled.manager = true;
          vars.disabled.clientManager = true;
          return;
        }

        let { data } = await shipmentQuoteManual.byKey(id);
        Object.assign(vars.formData, data);

        methods.enableDelete();
        vars.disabled.copy = false;
        vars.disabled.edit = false;
        if (vars.formData.client_company && vars.formData.quote_department) {
          methods.enableSave();
        }
        
        if (vars.formData.confirmed) {
          vars.disabled.edit = true;
          vars.disabled.delete = true;
          vars.disabled.save = true;
          vars.disabled.manager = true;
          vars.disabled.clientManager = true;
        }
      },
      clearFormData() {
        vars.formData.id = null;
        vars.formData.created = null;
        vars.formData.quote_number = '';
        vars.formData.quote_date = '';
        vars.formData.client_company = '';
        vars.formData.client_manager = '';
        vars.formData.quote_department = '';
        vars.formData.quote_manager = '';
        vars.formData.quote_type = '';
        vars.formData.vat_type = '';
        vars.formData.payment_terms = '';
        vars.formData.delivery_date = '';
        vars.formData.delivery_place = '';
        vars.formData.previous_quote_number = '';
        vars.formData.project_number = '';
        vars.formData.end_user = '';
        vars.formData.note = '';
        vars.formData.etc = '';
        vars.formData.supply_price = 0;
        vars.formData.vat = 0;
        vars.formData.total_price = 0;
        vars.formData.order_number = null;
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

        const rows = await vars.grid.baseItem.getSelectedRowsData();
        for (let row of rows) {
          // 거래처 품목코드(공급사품번)
          const clientItemNumber = row.client_item ? row.client_item.client_item_code : null;
          // 거래처 단가(영업단가)
          let salesUnitPrice = row.client_item ? row.client_item.unit_price : null;
          if (!salesUnitPrice) { salesUnitPrice = row.sales_price; }
          // 기초재고
          const basicStock = row.basic_stock ? { ...row.basic_stock } : { current_stock: 0, available_stock: 0 };
          
          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code; // 품목코드
          data.item = { ...row }; // 품목
          data.quote_quantity = 0; // 견적수량
          data.unit_price = row.sales_price; // 견적단가
          data.sales_unit_price = salesUnitPrice; // 영업단가
          data.supply_price = 0; // 견적공급가
          data.sales_supply_price = 0; // 영업공급가
          data.dc_rate = 0; // DC Rate
          data.request_delivery_date = null; // 요청납기
          data.basic_stock = { ...basicStock }; // 기초재고
          data.client_item_number = clientItemNumber; // 공급사품번
          data.note = ''; // 참고사항
          data.warehouse = { ...vars.warehouse }; // 출고창고
          data.warehouse_code = vars.warehouse.wh_code; // 창고코드
          data.project_number = vars.formData.project_number; // 프로젝트번호
          data.not_ordered = 0; // 미수주수량
        }
        grid.refresh();
        vars.dlg.addItem.show = false;
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
      showAddPopup() {
        if (vars.grid.baseItem) {
          vars.grid.baseItem.clearSelection();
          vars.grid.baseItem.clearFilter();
          vars.grid.baseItem.refresh();
        }
        vars.dlg.addItem.show = true;
      },
      async gridItem1Refresh(id) {
        methods.gridRefresh(id, vars.grid.item1, vars.filter.item1, vars.dataSource.item1);
      },
      async gridRefresh(id, grid, filter, dataSource) {
        if (!id) { id = 0; }
        filter[0].val = id;
        dataSource.defaultFilters = filter;
        if (grid) {
          grid.cancelEditData();
          grid.refresh();
        }
      },
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`shipment-quote-${key}`, evt.component);
      },
      onItem2Insert(evt) {
        evt.data.fk_quote_id = vars.formData.id;
      },
      newItem() {
        methods.gridItem1Refresh();
        if (vars.formData.id) {
          methods.clearFormData();
          methods.redirect();
        }
        setTimeout(() => {
          methods.clearFormData();
          vars.formData.quote_date = currentDateTime();
          vars.formData.quote_department = authService.getDepartmentName();
          vars.formData.quote_manager = authService.getUserName();
          vars.formData.quote_type = methods.getFirstQuoteType();
          vars.formData.vat_type = methods.getFirstVatType();
          vars.formData.payment_terms = methods.getFirstPaymentTerms();
          vars.formData.delivery_place = methods.getFirstDeliveryPlace();
          vars.formData.fk_company_id = authService.getCompanyId();

          vars.formState.readOnly = false;
        }, 200);
      },
      async copyItem() {
        const result = await confirm('견적을 복사하시겠습니까?', '복사 확인');
        if (result) {
          let params = Object.assign({}, vars.formData);
          delete params.created;
          params.id = null;
          params.quote_number = '';
          params.quote_date = currentDateTime();
          params.quote_type = '재견적';
          params.previous_quote_number = vars.formData.quote_number;

          let { data } = await shipmentQuoteManual.insert(params);

          await alert('복사가 완료되었습니다', '복사 확인');
          methods.redirect(data.id);
          vars.formState.readOnly = false;
        }
      },
      async deleteItem() {
        const result = await confirm('이 항목을 삭제하시겠습니까?', '삭제 확인');
        if (result) {
          try {
            await shipmentQuoteManual.remove(vars.formData.id);
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
      async editItem() {
        if (!vars.formData.id) { return; }
        if (vars.formState.readOnly && vars.formData.confirmed) { return; }
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
      async saveItem() {
        vars.loading.value = true;
        try {
          if (vars.formData.id) {
            // 기존 정보 업데이트
            const updateDate = Object.assign({}, vars.formData);
            delete updateDate.created;
            delete updateDate.quote_number;
            const { data } = await shipmentQuoteManual.update(
              vars.formData.id,
              updateDate
            );
            vars.formData.quote_number = data.quote_number;

            const gridItem1 = vars.grid.item1;
            if (gridItem1) await gridItem1.saveEditData();
            const gridItem2 = vars.grid.item2;
            if (gridItem2) await gridItem2.saveEditData();

            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');

            methods.enableSave();
            methods.enableDelete();
          } else {
            // 채번이 없을 경우 자동 채번
            if (vars.formData.created) vars.formData.created = null;
            let { data } = await shipmentQuoteManual.insert(vars.formData);
            vars.formData.id = data.id;

            const gridItem1 = vars.grid.item1;
            if (gridItem1 && gridItem1.hasEditData()) {
              await gridItem1.saveEditData();
            }
            const gridItem2 = vars.grid.item2;
            if (gridItem2 && gridItem2.hasEditData()) {
              await gridItem2.saveEditData();
            }
            beforeExitConfirm.clear()
            methods.redirect(data.id);
            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');
          }
        } catch (ex) {
          if (ex.response.status === 602) {
            notifyError('이미 존재하는 견적번호 입니다');
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
          case 'quote': {
            // Object.assign(vars.formData, data)
            methods.redirect(data.id);
            vars.formState.readOnly = true;
            break;
          }
          case 'client': {
            vars.formData.client_company = data.name;
            break;
          }
          case 'enduser': {
            vars.formData.end_user = data.name;
            break;
          }
          case 'project': {
            vars.formData.project_number = data.project_number;
            if (
              data.order_company &&
              data.order_company != vars.formData.client_company
            ) {
              vars.formData.client_company = data.order_company;
            }
            break;
          }
          case 'project2': {
            vars.focus.item1.component.cellValue(
              vars.focus.item1.rowIndex,
              vars.focus.item1.columnIndex,
              data.project_number
            );
            break;
          }
          case 'project3': {
            vars.focus.item2.component.cellValue(
              vars.focus.item2.rowIndex,
              vars.focus.item2.columnIndex,
              data.project_number
            );
            break;
          }
          case 'etc': {
            console.log(vars.dlg.finder.data);
            vars.formData.etc = vars.dlg.finder.data;
            break;
          }
        }

        vars.dlg.finder.show = false;
        vars.dlg.finder.title = '';
        vars.dlg.finder.key = null;
        vars.dlg.finder.data = null;
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
              vars.formData.end_user = e.previousValue;
              vars.disabled.tradeYn = true;
              return;
            }
          }
        }
        vars.disabled.tradeYn = false;
      },
      updateEtcValue(v) {
        vars.dlg.finder.data = v;
      },
      onDepartmentChanged(e) {
        if (!e.value) {
          vars.disabled.save = true;
          vars.disabled.manager = true;
          vars.formData.quote_manager = null;
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
      onDataError(e) {
        if (e.error.response.status == 605) {
          e.error.message = '연결된 데이터가 있어서 삭제가 안됩니다';
        } else if (e.error.response.status == 403) {
          e.error.message = '권한이 없습니다';
        }
      },
      onFocusedCellChanged(e) {
        vars.focus.item1 = e;
      },
      onFocusedCellChanged2(e) {
        vars.focus.item2 = e;
      },
      onSavingItem(e) {
        e.changes.forEach(element => {
          if (element.type != 'remove') {
            element.data.fk_quote_id = vars.formData.id;
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
        shipmentQuoteManual.update(vars.formData.id, priceData);
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
      availableStock(rowData) {
        if (!rowData.basic_stock) { return '0'; }
        return rowData.basic_stock.available_stock;
      },
      currentStock(rowData) {
        if (!rowData.basic_stock) { return '0'; }
        return rowData.basic_stock.current_stock;
      },
      setQuantity(newData, value, currentRowData) {
        newData.quote_quantity = value;
        newData.not_ordered = currentRowData.not_ordered + (value - currentRowData.quote_quantity);
        // 견적공급가 계산
        newData.unit_price = currentRowData.unit_price;
        newData.supply_price = newData.quote_quantity * newData.unit_price;
        // 영업공급가 계산
        newData.sales_unit_price = currentRowData.sales_unit_price;
        newData.sales_supply_price = newData.quote_quantity * currentRowData.sales_unit_price;
      },
      setUnitPrice(newData, value, currentRowData) {
        newData.unit_price = value;
        if (currentRowData.sales_unit_price == 0) {
          newData.dc_rate = 0;
        } else {
          newData.dc_rate = parseInt(((currentRowData.sales_unit_price - newData.unit_price) / currentRowData.sales_unit_price) * 100);
        }
        newData.quote_quantity = currentRowData.quote_quantity;
        newData.supply_price = newData.quote_quantity * newData.unit_price;
      },
      setDCRate(newData, value, currentRowData) {
        newData.dc_rate = value;
        newData.unit_price = parseInt(currentRowData.sales_unit_price - (currentRowData.sales_unit_price * (newData.dc_rate / 100)));
        newData.quote_quantity = currentRowData.quote_quantity;
        newData.supply_price = newData.quote_quantity * newData.unit_price;
      },
      loadBaseCode() {
        return baseCodeLoader(
          ['부가세구분', '견적구분', '결재조건', '납품장소'],
          authService.getCompanyId()
        ).then(response => {
          vars.dataSource.payment_terms = response['결재조건'];
          vars.dataSource.quote_type = response['견적구분'];
          vars.dataSource.vat_type = response['부가세구분'];
          vars.dataSource.delivery_place = response['납품장소'];
        }).then(() => (vars.init.value = true));
      },
      loadBaseItem() {
        vars.dataSource.baseItem = getBaseItem(
          null,
          vars.filter.baseItem.clientId,
          vars.warehouse.wh_code
        );
      },
      checkPossibleSave() {
        if (vars.formData.client_company && vars.formData.quote_department && !vars.formData.confirmed) {
          methods.enableSave();
        }
      },
      getFirstQuoteType() {
        return methods.getFirstItemName(vars.dataSource.quote_type);
      },
      getFirstVatType() {
        return methods.getFirstItemName(vars.dataSource.vat_type);
      },
      getFirstPaymentTerms() {
        return methods.getFirstItemName(vars.dataSource.payment_terms);
      },
      getFirstDeliveryPlace() {
        return methods.getFirstItemName(vars.dataSource.delivery_place);
      },
      getFirstItemName(itemList) {
        if (!itemList || itemList.length <= 0) { return ''; }
        else { return itemList[0].code_name; }
      },
      redirect(id) {
        if (id) { router.replace({ path: `/shipment/quote-manual/${id}` }); }
        else { router.replace({ path: `/shipment/quote-manual` }); }
      },
      itemPopupClick({ column, data }) {
        if (column.name === 'item_code') {
          vars.itemDetail.id = data.item.id;
          vars.itemDetail.visible = true;
        }
      },
      async printDocument() {
        if (!vars.formData.id) { return; }
        const params = { ...vars.formData };
        params.supply_price = numeral(vars.formData.supply_price).format('0,0');
        params.supply_price_humanize = humanize(vars.formData.supply_price);
        params.quote_date = moment(vars.formData.quote_date).format('YYYY년 M월 D일');

        const quoteManager = vars.dataSource.employee.find(
          v => v.emp_name === vars.formData.quote_manager
        );
        if (quoteManager) { params.quote_manager = quoteManager; }
        else { params.quote_manager = { emp_name: vars.formData.quote_manager }; }

        const { data: item1 } = await vars.dataSource.item1.load();
        const { data: item2 } = await vars.dataSource.item2.load();
        params.items = [...item1, ...item2];
        params.items.forEach(item => {
          item.unit_price = numeral(item.unit_price).format('0,0');
          item.supply_price = numeral(item.supply_price).format('0,0');
        });

        const clientManager = vars.dataSource.client_manager.find(
          v => v.name === vars.formData.client_manager
        );
        if (clientManager) { params.client_manager = clientManager; }
        else { params.client_manager = { name: vars.formData.client_manager }; }

        await printDocument('quote', params);
      },
      onVatTypeChanged(e) {
        vars.grid.item1.refresh();
      },
      enableDelete() {
        if (vars.formState.readOnly) { vars.disabled.delete = true; }
        else { vars.disabled.delete = false; }
      },
      enableSave() {
        if (vars.formState.readOnly) { vars.disabled.save = true; } 
        else { vars.disabled.save = false; }
      },
      async exportToOrder() {
        if (!vars.formData.id) { return; }
        const params = { quote_id: vars.formData.id };
        try {
          await apiExportToOrder.post('', params);
          await alert('수주로 보내기가 완료되었습니다', '수주로 보내기');

          let { data } = await shipmentQuoteManual.byKey(vars.formData.id);
          Object.assign(vars.formData, data);

          methods.gridItem1Refresh(vars.formData.id);
        } catch (ex) {
          if (ex.response.status == 608) {
            await alert('미수주 수량이 없습니다', '수주로 보내기');
          } else {
            await alert('수주로 보내기가 실패했습니다', '수주로 보내기');
          }
        }
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
          if (vars.formData.client_company && vars.formData.quote_department) {
            vars.disabled.edit = false;
            methods.enableSave();
            methods.enableDelete();
          }
        }
        await shipmentQuoteManual.update(vars.formData.id, param);
      },
      calculateCustomSummary(options) {
        if (options.name === 'supply_price') {
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          } else if (options.summaryProcess === 'calculate') {
            options.totalValue += options.value.quote_quantity * options.value.unit_price;
          } else if (options.summaryProcess === 'finalize') {
            const response = calcPriceSummary(vars.formData.vat_type, options.totalValue);
            vars.formData.supply_price = response.supply_price;
            vars.formData.vat = response.vat;
            vars.formData.total_price = response.total_price;
          }
        }
      },
      customManagerCreating(data) {
        if (!data.text) {
          data.customItem = null;
          return;
        }

        const id = vars.dataSource.client_manager[vars.dataSource.client_manager.length - 1].id + 1;
        vars.dataSource.client_manager = [...vars.dataSource.client_manager, {
          'id': id,
          'name': data.text
        }];
        data.customItem = vars.dataSource.client_manager[vars.dataSource.client_manager.length - 1];
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
