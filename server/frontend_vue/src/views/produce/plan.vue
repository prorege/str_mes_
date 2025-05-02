<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">생산계획</div>
            </dx-item>

            <dx-item widget="dxButton" location="after" locate-in-menu="auto"
              :options="{ text: '신규', type: 'add', icon: 'add', disabled: vars.disabled.new, onClick: methods.newItem, }"
            />
            <dx-item widget="dxButton" location="after" locate-in-menu="auto"
              :options="{ text: '수정', type: 'rename', icon: 'rename', disabled: vars.disabled.edit, onClick: methods.editItem, }"
            />
            <dx-item widget="dxButton" location="after" locate-in-menu="auto"
              :options="{ text: '삭제', type: 'remove', icon: 'remove', disabled: vars.disabled.delete, onClick: methods.deleteItem, }"
            />
            <dx-item widget="dxButton" location="after" locate-in-menu="auto"
              :options="{ text: '저장', type: 'save', icon: 'save', disabled: vars.disabled.save, onClick: methods.saveItem, }"
            />
          </dx-toolbar>
        </div>

        <dx-form :form-data="vars.formData">
          <dx-group-item :col-count="4">
            <dx-group-item>
              <dx-simple-item data-field="number"
                :editor-options="{
                  placeholder: '(자동 or 직접입력)',
                  ...generateItemButtonOption('search', methods.createFindPopupFn('plan', '생산계획조회')),
                }"
              >
                <dx-label text="생산계획번호" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="target_date" editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  ...vars.formState,
                }"
              >
                <dx-label text="계획일자" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="department" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.department,
                  displayExpr: 'department_name',
                  valueExpr: 'department_name',
                  acceptCustomValue: true,
                  onValueChanged: methods.onDepartmentChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="담당부서" :show-colon="false" />
                <dx-required-rule message="담당부서를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="manager" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.employee,
                  displayExpr: 'emp_name',
                  valueExpr: 'emp_name',
                  disabled: vars.disabled.manager,
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
            height="calc(100vh - 324px)"
            date-serialization-format="yyyy-MM-ddTHH:mm:ss"
            column-resizing-mode="widget"
            :show-borders="true"
            :remote-operations="false"
            :column-auto-width="true"
            :focused-row-enabled="true"
            :allow-column-resizing="true"
            :allow-column-reordering="true"
            :row-alternation-enabled="true"
            :select-text-on-edit-start="true"
            :disabled="vars.disabled.items"
            :data-source="vars.dataSource.item1"
            :on-initialized="evt => methods.onGridInitialized(evt, 'item1')"
            @saving="methods.onSavingItem"
            @cell-dbl-click="methods.itemPopupClick"
            @data-error-occurred="methods.onDataError"
            @focused-cell-changed="methods.onFocusedCellChanged"
          >
            <dx-grid-toolbar>
              <dx-item template="addFromShipmentOrder" location="before" :visible="!vars.formState.readOnly" />
              <dx-item template="addFromPurchaseOrderPlan" location="before" :visible="!vars.formState.readOnly" />
              <dx-grid-item name="addRowButton" :options="{ onClick: methods.showAddBaseItem }" />
              <dx-grid-item name="saveButton" :visible="!!vars.formData.id" />
              <dx-grid-item name="revertButton" />
              <dx-grid-item name="columnChooserButton" />
            </dx-grid-toolbar>
            <template #addFromShipmentOrder>
              <dx-button text="수주에서 가져오기" icon="add" @click="methods.showAddShipmentOrderItem" />
            </template>
            <template #addFromPurchaseOrderPlan>
              <dx-button text="발주계획에서 가져오기" icon="add" @click="methods.showAddPurchaseOrderPlanItem" />
            </template>

            <dx-column caption="품목코드" data-field="item_code" width="180" :allow-editing="false" />
            <dx-column caption="품명" data-field="item.item_name" :allow-editing="false" />
            <dx-column caption="규격" data-field="item.item_standard" :allow-editing="false" />
            <dx-column caption="생산계획수량" data-field="production_plan_quantity" data-type="number" format="fixedPoint" :set-cell-value="methods.setQuantity" />
            <dx-column caption="단가" data-field="unit_price" data-type="number" format="₩,##0" :set-cell-value="methods.setUnitPrice" />
            <dx-column caption="단위" data-field="item.unit" :allow-editing="false" />
            <dx-column caption="공급가" data-field="supply_price" data-type="number" format="₩,##0" :allow-editing="false" />
            <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
            <dx-column caption="미작지수량" data-field="unordered_quantity" data-type="number" format="fixedPoint" :allow-editing="false" />
            <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :allow-editing="false" :calculate-display-value="methods.availableStock" />
            <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :allow-editing="false" :calculate-display-value="methods.currentStock" />
            <dx-column caption="입고창고" data-field="warehouse.wh_name" :set-cell-value="methods.setWarehouse" >
              <dx-lookup value-expr="wh_name" display-expr="wh_name" :data-source="vars.dataSource.warehouse" />
            </dx-column>
            <dx-column caption="발주계획번호" data-field="purchase_order_plan_number" :allow-editing="false" />
            <dx-column caption="수주번호" data-field="order_number" :allow-editing="false" />
            <dx-column caption="수주일자" data-field="order_date" :allow-editing="false" :visible="false" />
            <dx-column caption="프로젝트번호" data-field="project_management.project_number"
              :editor-options="{ ...generateItemButtonOption('search', methods.createFindPopupFn('project', '프로젝트조회')), }"
              :set-cell-value="methods.setProjectManagement"
            />
            <dx-column caption="고객업체" data-field="client_company"
              :editor-options="{ ...generateItemButtonOption('search', methods.createFindPopupFn('client', '고객업체조회')), }"
            />
            <dx-column caption="고객사품번" data-field="client_item_number" />
            <dx-column caption="실수요자" data-field="end_user" :allow-editing="false" />
            <dx-column caption="품목설명" data-field="item.item_detail" :allow-editing="false" />
            <dx-column caption="수주품목" data-field="fk_order_item_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
            <dx-column caption="생산계획" data-field="fk_production_plan_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
            <dx-column caption="창고코드" data-field="warehouse_code" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
            <dx-column caption="미소요량계산수량" data-field="not_measure_requirement" data-type="number" format="fixedPoint" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
            
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
      v-model:visible="vars.dlg.orderItem.show"
      width="70%"
      :height="500"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'order-item-popup')"
    >
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ text: '선택된 항목 추가', icon: 'add', onClick: methods.addOrderItem, }"
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
          :on-initialized="evt => methods.onGridInitialized(evt, 'orderItem')"
        >
          <dx-column caption="수주번호" data-field="order.order_number" :sort-index="0" sort-order="desc" />
          <dx-column caption="고객사" data-field="order.client_company" />
          <dx-column caption="수주일자" data-field="order.order_date" data-type="date" format="yyyy-MM-dd" :sort-index="1" sort-order="desc" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="자산구분" data-field="item.asset_type" />
          <dx-column caption="수주수량" data-field="order_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="생산계획수량" data-field="produce_plan_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="생산계획 미처리" data-field="not_produce_plan_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="미출고수량" data-field="not_shipped" data-type="number" format="fixedPoint" />
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" />

          <dx-paging :page-size="20" />
          <dx-sorting mode="multiple"/>
          <dx-filter-row :visible="true" />
          <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick" />
        </dx-data-grid>
      </template>
    </dx-popup>

    <dx-popup
      title="발주계획품목찾기"  
      content-template="popup-content"
      v-model:visible="vars.dlg.purchaseOrderPlanItem.show"
      width="70%"
      :height="500"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'purchase-order-plan-item-popup')"
    >
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ text: '선택된 항목 추가', icon: 'add', onClick: methods.addPurchaseOrderPlanItem, }"
      />

      <template #popup-content>
        <dx-data-grid
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="vars.dataSource.purchaseOrderPlanItem"
          :on-initialized="evt => methods.onGridInitialized(evt, 'purchaseOrderPlanItem')"
        >
          <dx-column caption="발주계획번호" data-field="order_plan.order_plan_number" :sort-index="0" sort-order="desc" />
          <dx-column caption="발주계획일자" data-field="order_plan.order_plan_date" data-type="date" format="yyyy-MM-dd" :sort-index="1" sort-order="desc" />
          <dx-column caption="발주구분" data-field="order_plan.order_type" />
          <dx-column caption="주공급업체" data-field="main_supplier" />
          <dx-column caption="실수요자" data-field="end_user" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="자산구분" data-field="item.asset_type" />
          <dx-column caption="발주계획수량" data-field="order_plan_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="미발주수량" data-field="unordered_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="미생산계획수량" data-field="not_produce_plan_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" />

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
      v-model:visible="vars.dlg.baseItem.show"
      width="70%"
      :height="500"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'base-item-popup')"
    >
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ text: '선택된 항목 추가', icon: 'add', onClick: methods.addBaseItem, }"
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
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :calculate-display-value="methods.availableStock" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :calculate-display-value="methods.currentStock" />
          
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
      @showing="vars.dlg.finder.onShowing"
      @initialized="evt => methods.onGridInitialized(evt, 'multiuse-popup')"
    >
      <template #popup-content>
        <data-grid-plan v-if="vars.dlg.finder.key === 'plan'" @change="methods.finderReturnHandler" ref="popupSearchPlan" />
        <data-grid-project v-else-if="vars.dlg.finder.key === 'project'" @change="methods.finderReturnHandler" />
        <data-grid-client v-else-if="vars.dlg.finder.key === 'client'" @change="methods.finderReturnHandler" />
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

import { useRouter } from 'vue-router';
import { onMounted, ref, reactive, computed, watch, nextTick } from 'vue';

import { DxButton } from 'devextreme-vue/button';
import DxTextArea from 'devextreme-vue/text-area';
import { confirm, alert } from 'devextreme/ui/dialog';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxRequiredRule } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxLookup, DxEditing, DxSorting, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, 
  DxItem as DxGridItem, DxToolbar as DxGridToolbar, DxButton as DxGridButton } from 'devextreme-vue/data-grid';

import PopupItemDetail from '@/components/base/popup-item-detail';
import DataGridPlan from '../../components/produce/data-plan.vue';
import DataGridClient from '../../components/base/data-client.vue';
import DataGridProject from '../../components/project/data-project.vue';

import { getStock } from '../../data-source/setup';
import { getShipmentOrderItem } from '../../data-source/shipment';
import { baseCodeLoader, getBaseItem } from '../../data-source/base';
import { producePlan, producePlanItem, getProducePlanItem } from '../../data-source/produce';
import { getPurchaseOrderPlanItem } from '../../data-source/purchase'

import authService from '../../auth';
import stateStore from '@/utils/state-store';
import { notifyInfo, notifyError } from '../../utils/notify';
import { loadEmployee, loadWarehouse, loadDepartment } from '../../utils/data-loader';
import { sumSupplyPrice, currentDateTime, calcPriceSummary, beforeExitConfirm, generateItemButtonOption } from '../../utils/util';

export default {
  components: {
    DxButton,
    DxTextArea,
    DxLoadPanel,
    DxToolbar, DxItem,
    DxPopup, DxToolbarItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxRequiredRule,
    DxDataGrid, DxColumn, DxPaging, DxLookup, DxEditing, DxSorting, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, 
    DxGridItem, DxGridToolbar, DxGridButton,
    DataGridPlan, DataGridClient, DataGridProject, PopupItemDetail,
  },
  props: {
    id: [String, Number],
  },
  setup(props) {
    // variable 설정
    const router = useRouter();
    const vars = { dlg: {} };
    const popupSearchPlan = ref(null);
    vars.init = ref(false);
    vars.loading = ref(false);
    vars.formState = reactive({ readOnly: true });
    vars.grid = { baseItem: null, orderItem: null, item1: null };
    vars.dlg.baseItem = reactive({ show: false });
    vars.dlg.orderItem = reactive({ show: false });
    vars.dlg.purchaseOrderPlanItem = reactive({ show: false })
    vars.dlg.finder = reactive({ show: false, title: '', key: null, data: null });
    vars.warehouse = {};
    vars.filter = reactive({
      baseItem: {
        clientId: null,
      },
      orderItem: {
        clientCompany: null,
      },
      purchaseOrderPlanItem: {
        clientCompany: null,
      },
      item1: [{ name: 'fk_production_plan_id', op: 'eq', val: props.id || 0 }],
    });
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
      department: [],
      employee: [],
      warehouse: [],
      baseItem: null,
      orderItem: null,
      purchaseOrderPlanItem: null,
      item1: getProducePlanItem(vars.filter.item1),
    });
    vars.focus = reactive({ item1: null });
    vars.formData = reactive({});
    vars.summary = {};
    vars.summary.supply_price = computed(() => '₩' + numeral(vars.formData.supply_price).format('0,0'));
    vars.summary.vat = computed(() => '₩' + numeral(vars.formData.vat).format('0,0'));
    vars.summary.total_price = computed(() => '₩' + numeral(vars.formData.total_price).format('0,0'));

    vars.itemDetail = reactive({ visible: false, id: 0 });

    onMounted(async () => {
      await loadDepartment(vars.dataSource);
      await methods.loadBaseCode();
      methods.initById(props.id);
      loadWarehouse(vars.dataSource);
    });

    // public methods
    const methods = {
      async initById(id) {
        beforeExitConfirm.check(() => !vars.disabled.save)
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

        let { data } = await producePlan.byKey(id);
        Object.assign(vars.formData, data);

        methods.enableDelete();
        vars.disabled.edit = false;
        if (vars.formData.department) {
          methods.enableSave();
          vars.disabled.items = false;
        }
      },
      clearFormData() {
        vars.formData.id = null;
        vars.formData.created = null;
        vars.formData.number = '';
        vars.formData.target_date = '';
        vars.formData.department = '';
        vars.formData.manager = '';
        vars.formData.note = '';
        vars.formData.etc = '';
        vars.formData.supply_price = 0;
        vars.formData.vat = 0;
        vars.formData.total_price = 0;
        vars.formData.fk_company_id = authService.getCompanyId();
      },
      async addOrderItem() {
        const grid = vars.grid.item1;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        const rows = await vars.grid.orderItem.getSelectedRowsData();
        for (let row of rows) {
          let orderNumber = null;
          let orderDate = null;
          let clientCompany = null;
          let endUser = null;
          if (row.order) {
            orderNumber = row.order.order_number;
            orderDate = row.order.order_date;
            clientCompany = row.order.client_company;
            endUser = row.order.end_user;
          }
          if (!row.basic_stock) {
            row.basic_stock = {
              available_stock: 0,
              current_stock: 0,
            };
          }

          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code; // 품목코드
          data.item = { ...row.item }; // 품목
          data.production_plan_quantity = row.not_produce_plan_quantity; // 생산계획수량
          data.unit_price = row.unit_price; // 단가
          data.supply_price = data.production_plan_quantity * data.unit_price; // 공급가
          data.request_delivery_date = row.request_delivery_date; // 요청납기
          data.unordered_quantity = data.production_plan_quantity; // 미작지수량
          data.not_measure_requirement = data.production_plan_quantity; // 미소요량계산수량
          data.basic_stock = { ...row.basic_stock }; // 기초재고
          data.warehouse = { ...row.warehouse }; // 입고창고
          data.warehouse_code = row.warehouse.wh_code; // 창고코드
          data.order_number = orderNumber; // 수주번호
          data.order_date = orderDate; // 수주일자
          data.client_company = clientCompany; // 고객업체
          data.client_item_number = row.client_item_number; // 고객사품번
          data.end_user = endUser; // 실수요자
          data.fk_project_management_id = row.fk_project_management_id; // 프로젝트번호
          data.fk_order_item_id = row.id; // 수요품목 아이디
          data.fk_production_plan_id = vars.formData.id; // 생산계획 아이디
          data.project_management = row.project_management ? row.project_management : null;
        }
        vars.dlg.baseItem.show = false;
        vars.dlg.orderItem.show = false;
        vars.dlg.purchaseOrderPlanItem.show = false;
        grid.refresh();
      },
      async addPurchaseOrderPlanItem() {
        const grid = vars.grid.item1;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        const rows = await vars.grid.purchaseOrderPlanItem.getSelectedRowsData();
        for (let row of rows) {
          if (!row.basic_stock) {
            row.basic_stock = {
              available_stock: 0,
              current_stock: 0,
            };
          }

          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code; // 품목코드
          data.item = { ...row.item }; // 품목
          data.production_plan_quantity = row.not_produce_plan_quantity; // 생산계획수량
          data.unit_price = row.unit_price; // 단가
          data.supply_price = data.production_plan_quantity * data.unit_price; // 공급가
          data.request_delivery_date = row.request_delivery_date; // 요청납기
          data.unordered_quantity = data.production_plan_quantity; // 미작지수량
          data.not_measure_requirement = data.production_plan_quantity; // 미소요량계산수량
          data.basic_stock = { ...row.basic_stock }; // 기초재고
          data.warehouse = { ...row.warehouse }; // 입고창고
          data.warehouse_code = row.warehouse.wh_code; // 창고코드
          data.order_number = row.order_number; // 수주번호
          data.order_date = row.order_date; // 수주일자
          data.client_company = row.end_user; // 고객업체
          data.client_item_number = row.client_item_number; // 고객사품번
          data.end_user = row.end_user; // 실수요자
          data.purchase_order_plan_number = row.order_plan.order_plan_number; // 발주계획번호
          data.fk_project_management_id = row.fk_project_management_id; // 프로젝트번호
          data.fk_order_item_id = row.fk_shipment_order_item_id; // 수요품목 아이디
          data.fk_purchase_order_plan_id = row.order_plan.id; // 발주계획 아이디
          data.fk_purchase_order_plan_item_id = row.id; // 발주계획품목 아이디
          data.fk_production_plan_id = vars.formData.id; // 생산계획 아이디
          data.project_management = row.project_management ? row.project_management : null;
        }
        vars.dlg.baseItem.show = false;
        vars.dlg.orderItem.show = false;
        vars.dlg.purchaseOrderPlanItem.show = false;
        grid.refresh();
      },
      async addBaseItem() {
        const grid = vars.grid.item1;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        const rows = await vars.grid.baseItem.getSelectedRowsData();
        for (let row of rows) {
          const clientItemNumber = row.client_item
            ? row.client_item.client_item_code
            : null;
          const basicStock = row.basic_stock
            ? { ...row.basic_stock }
            : {
                current_stock: 0,
                available_stock: 0,
              };

          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code; // 품목코드
          data.item = { ...row }; // 품목
          data.supply_price = 0; // 공급가
          data.production_plan_quantity = 0; // 생산계획수량
          data.unit_price = row.sales_price ? row.sales_price : 0; // 단가
          data.request_delivery_date = null; // 요청납기
          data.unordered_quantity = 0; // 미작지수량
          data.not_measure_requirement = 0; // 미소요량계산수량
          data.basic_stock = { ...basicStock }; // 기초재고
          data.warehouse = { ...vars.warehouse }; // 입고창고
          data.warehouse_code = vars.warehouse.wh_code; // 창고코드
          data.order_number = null; // 수주번호
          data.order_date = null; // 수주일자
          data.client_company = null; // 고객업체
          data.client_item_number = clientItemNumber; // 고객사품번
          data.end_user = null; // 실수요자
          data.fk_project_management_id = null; // 프로젝트번호
          data.fk_order_item_id = null; // 수요품목 아이디
          data.fk_production_plan_id = vars.formData.id; // 생산계획 아이디
        }
        vars.dlg.baseItem.show = false;
        vars.dlg.orderItem.show = false;
        vars.dlg.purchaseOrderPlanItem.show = false;
        grid.refresh();
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
          vars.dlg.finder.onShowing = () => {
            if (vars.dlg.finder.key === 'plan') {
              popupSearchPlan.value.methods.refresh();
            }
          };
        };
      },
      showAddBaseItem() {
        methods.gridClear(vars.grid.baseItem);
        vars.dlg.baseItem.show = true;
      },
      showAddShipmentOrderItem() {
        const notContains = [];
        for (const item of vars.grid.item1.getVisibleRows()) {
          if (!item.id && item.data.fk_order_item_id) {
            notContains.push(['id', '<>', item.data.fk_order_item_id], 'and');
          }
        }
        notContains.pop()

        if (vars.grid.orderItem) {
          vars.grid.orderItem.filter(notContains);
          methods.gridClear(vars.grid.orderItem);
        }
        vars.dlg.orderItem.show = true;
      },
      showAddPurchaseOrderPlanItem() {
        const notContains = [];
        for (const item of vars.grid.item1.getVisibleRows()) {
          if (!item.id && item.data.fk_purchase_order_plan_item_id) {
            notContains.push(['id', '<>', item.data.fk_purchase_order_plan_item_id], 'and');
          }
        }
        notContains.pop()
        
        if (vars.grid.purchaseOrderPlanItem) {
          vars.grid.purchaseOrderPlanItem.filter(notContains);
          methods.gridClear(vars.grid.purchaseOrderPlanItem);
        }

        vars.dlg.purchaseOrderPlanItem.show = true;
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
        stateStore.bind(`produce-plan-${key}`, evt.component);
      },
      async newItem() {
        methods.gridItem1Refresh();
        if (vars.formData.id) {
          methods.clearFormData();
          methods.redirect();
        }
        setTimeout(() => {
          methods.clearFormData();
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
        const result = await confirm('이 항목을 삭제하시겠습니까?', '삭제 확인');
        if (result) {
          try {
            await producePlan.remove(vars.formData.id);
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
            await producePlan.update(vars.formData.id, vars.formData);
            if (vars.grid.item1) await vars.grid.item1.saveEditData();

            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');

            methods.enableSave();
            methods.enableDelete();
          } else {
            // 채번이 없을 경우 자동 채번
            let { data } = await producePlan.insert(vars.formData);
            vars.formData.id = data.id;

            const item1 = vars.grid.item1;
            if (item1 && item1.hasEditData()) {
              await item1.saveEditData();
            }
            beforeExitConfirm.clear()
            methods.redirect(data.id);
            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');
          }
        } catch (ex) {
          if (ex.response.status === 602) {
            notifyError('이미 존재하는 생산계획번호 입니다');
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
          case 'plan': {
            methods.redirect(data.id);
            vars.formState.readOnly = true;
            break;
          }
          case 'client': {
            vars.grid.item1.cellValue(
              vars.focus.item1.rowIndex,
              vars.focus.item1.columnIndex,
              data.name
            );
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
          const selectedItem = e.component.option('selectedItem');
          if (selectedItem) {
            loadEmployee(vars.dataSource, selectedItem.id);
            vars.disabled.manager = false;
          }
        }
        methods.checkPossibleSave();

        const selectedItem = e.component.option('selectedItem');
        if (selectedItem) vars.warehouse = { ...selectedItem.warehouse };
        else vars.warehouse = {};
        methods.loadBaseItem();
        methods.loadOrderItem();
        methods.loadPurchaseOrderPlanItem();
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
      onSavingItem(e) {
        e.changes.forEach(element => {
          if (element.type != 'remove') {
            console.log('produce-plan-onSavingItem', element.data);
            element.data.fk_production_plan_id = vars.formData.id;
            delete element.data.item;
            delete element.data.warehouse;
            delete element.data.order_item;
            delete element.data.basic_stock;
            delete element.data.production_plan;
            delete element.data.purchase_order_plan;
            delete element.data.purchase_order_plan_item;
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
        producePlan.update(vars.formData.id, priceData);
      },
      async setWarehouse(newData, value, currentRowData) {
        const warehouseList = vars.dataSource.warehouse;
        for (let i = 0; i < warehouseList.length; i++) {
          if (warehouseList[i].wh_name == value) {
            newData.warehouse = { ...warehouseList[i] };
            newData.warehouse_code = warehouseList[i].wh_code;

            const { basicStock } = await getStock(
              currentRowData.item_code,
              newData.warehouse_code
            );
            newData.basic_stock = { ...basicStock };
            break;
          }
        }
      },
      loadBaseCode() {
        vars.init.value = true;
      },
      availableStock(rowData) {
        if (!rowData.basic_stock) return '0';
        return rowData.basic_stock.available_stock;
      },
      currentStock(rowData) {
        if (!rowData.basic_stock) return '0';
        return rowData.basic_stock.current_stock;
      },
      setQuantity(newData, value, currentRowData) {
        newData.unordered_quantity =
          currentRowData.unordered_quantity +
          (value - currentRowData.production_plan_quantity);
        newData.not_measure_requirement =
          currentRowData.not_measure_requirement +
          (value - currentRowData.production_plan_quantity);
        newData.production_plan_quantity = value;
        newData.unit_price = currentRowData.unit_price;
        newData.supply_price = value * newData.unit_price;
      },
      setUnitPrice(newData, value, currentRowData) {
        newData.production_plan_quantity =
          currentRowData.production_plan_quantity;
        newData.unit_price = value;
        newData.supply_price = newData.production_plan_quantity * value;
      },
      setProjectManagement(newData, value, currentRowData){
        if(!value) return;
        newData.project_management = value;
        newData.fk_project_management_id = value.id;
      },
      calculateCustomSummary(options) {
        if (options.name === 'supply_price') {
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          } else if (options.summaryProcess === 'calculate') {
            options.totalValue += options.value.production_plan_quantity * options.value.unit_price;
          } else if (options.summaryProcess === 'finalize') {
            const response = calcPriceSummary(vars.formData.vat_type, options.totalValue);
            vars.formData.supply_price = response.supply_price;
            vars.formData.vat = response.vat;
            vars.formData.total_price = response.total_price;
          }
        }
      },
      loadBaseItem() {
        vars.dataSource.baseItem = getBaseItem(null, null, vars.warehouse.wh_code);
      },
      loadOrderItem() {
        vars.dataSource.orderItem = getShipmentOrderItem([
          { name: 'not_shipped', op: 'gt', val: 0 },
          { name: 'produce_plan_quantity', op: 'gt', val: 0 },
          { name: 'not_produce_plan_quantity', op: 'gt', val: 0 },
          { name: 'closing_yn', op: 'eq', val: 0 },
        ]);
      },
      loadPurchaseOrderPlanItem() {
        vars.dataSource.purchaseOrderPlanItem = getPurchaseOrderPlanItem([
          { name: 'not_produce_plan_quantity', op: 'gt', val: 0 },
        ]);
      },
      checkPossibleSave() {
        if (vars.formData.department) {
          methods.enableSave();
          vars.disabled.items = false;
        }
      },
      redirect(id) {
        if (id) {
          router.replace({ path: `/produce/plan/${id}` });
        } else {
          router.replace({ path: `/produce/plan` });
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
      popupSearchPlan,
      generateItemButtonOption,
    };
  },
};
</script>
