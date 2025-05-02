<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">Clearance</div>
            </dx-item>
            <dx-item widget="dxButton" location="after" locate-in-menu="auto"
              :options="{ text: '수입원가마감', type: 'calculate', icon: 'money', onClick: methods.calculateCostPrice }"
            />
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
          <dx-group-item :col-count="4">
            <dx-group-item>
              <dx-simple-item data-field="clearance_number"
                :editor-options="{
                  placeholder: '(자동 or 직접입력)',
                  ...generateItemButtonOption('search', methods.createFindPopupFn('clearance', '발주조회'))
                }"
              >
                <dx-label text="통관번호" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="clearance_date" editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  ...vars.formState,
                }"
              >
                <dx-label text="통관일자" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
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
              <dx-simple-item data-field="buyer" 
                :editor-options="{
                  onEnterKey: methods.createFindPopupFn('buyer', '업체조회', { name: vars.formData.buyer }),
                  ...generateItemButtonOption('search', methods.createFindPopupFn('buyer', '업체조회', { name: vars.formData.buyer })),
                  ...vars.formState,
                }"
              >
                <dx-label text="Buyer" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="clearance_department" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'department_name',
                  displayExpr: 'department_name',
                  dataSource: vars.dataSource.department,
                  onValueChanged: methods.onDepartmentChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="부서" :show-colon="false" />
                <dx-required-rule message="부서를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="member" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'emp_name',
                  displayExpr: 'emp_name',
                  dataSource: vars.dataSource.employee,
                  acceptCustomValue: true,
                  ...vars.formState,
                }"
              >
                <dx-label text="담당자" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
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
                  onValueChanged: methods.onExRateChanged,
                  ...vars.formState 
                }"
              >
                <dx-label text="ExRate" :show-colon="false" />
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
            :data-source="vars.dataSource.clearanceItem"
            :on-initialized="(evt) => methods.onGridInitialized(evt, 'clearanceItem')"
            @saving="methods.onSavingItem"
            @cell-dbl-click="methods.itemPopupClick"
            @data-error-occurred="methods.onDataError"
            @focused-cell-changed="methods.onFocusedCellChanged"
          >
            <dx-grid-toolbar>
              <dx-grid-item name="addRowButton" :options="{ onClick: methods.showAddPopup }" />
              <dx-grid-item name="saveButton" :visible="!!vars.formData.id" />
              <dx-grid-item name="revertButton" />
              <dx-grid-item name="columnChooserButton" />
            </dx-grid-toolbar>

            <dx-column caption="ItemCode" data-field="item_code" width="180" :allow-editing="false" />
            <dx-column caption="Name" data-field="item.item_name" :allow-editing="false" />
            <dx-column caption="Qty" data-field="qty" data-type="number" format="fixedPoint" :set-cell-value="methods.setQuantity" />
            <dx-column caption="Unit" data-field="item.unit" :allow-editing="false" />
            <dx-column caption="ImportPrice" data-field="import_price" data-type="number" :format="',##0.00000'" :allow-editing="false" :set-cell-value="methods.setImportPrice" />
            <dx-column caption="Amount" data-field="amount" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :allow-editing="false" />
            <dx-column caption="WonPrice" data-field="won_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :allow-editing="false" />
            <dx-column caption="WonAmount" data-field="won_amount" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :allow-editing="false" />
            <dx-column caption="CostPrice" data-field="cost_price" data-type="number" :format="{ type: 'fixedPoint', precision: 4 }" />
            <dx-column caption="CostRate" data-field="cost_rate" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
            <dx-column caption="선적번호" data-field="import_shipment_number" :allow-editing="false" />
            <dx-column caption="입고창고" data-field="warehouse.wh_name" :set-cell-value="methods.setWarehouse">
              <dx-lookup value-expr="wh_name" display-expr="wh_name" :data-source="vars.dataSource.warehouse" />
            </dx-column>
            
            <dx-summary :recalculate-while-editing="true" :calculate-custom-summary="methods.calculateCustomSummary">
              <dx-total-item name="supply_price" summary-type="custom" />
              <dx-total-item name="total_price_cost" summary-type="custom" />
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
              <th>amount 합계</th>
              <td>{{ vars.summary.total_price_import.value }}</td>
              <th>won amount 합계</th>
              <td>{{ vars.summary.total_price_cost.value }}</td>
            </tr>
          </table>
        </div>
      </div>
    </div>

    <dx-popup
      title="선적에서 가져오기"
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
          :data-source="vars.dataSource.shipmentItem"
          :on-initialized="(evt) => methods.onGridInitialized(evt, 'shipmentItem')"
        >
          <dx-column caption="OfferNo" data-field="shipment.shipment_number" :sort-index="1" sort-order="desc" />
          <dx-column caption="OfferDate" data-field="shipment.shipment_date" :sort-index="0" sort-order="desc" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="Unit" data-field="item.item_standard" />
          <dx-column caption="Qty" data-field="qty" data-type="number" format="fixedPoint" />
          <dx-column caption="ImportPrice" data-field="import_price" :format="{ type: 'currency', precision: 4 }" />
          <dx-column caption="Amount" data-field="amount" :format="{ type: 'fixedPoint', precision: 2 }" />
          <dx-column caption="ReqDeliDate" data-field="req_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="ConDeliDate" data-field="con_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="EndUser" data-field="end_user" />
          <dx-column caption="미오퍼" data-field="not_offer" data-type="number" format="fixedPoint" />
          <dx-column caption="미통관" data-field="not_clearance" data-type="number" format="fixedPoint" />
          <dx-column caption="미발행" data-field="not_publish" data-type="number" format="fixedPoint" />

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
        <data-grid-client    v-if="vars.dlg.finder.key === 'supplier'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-client    v-else-if="vars.dlg.finder.key === 'buyer'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-client    v-else-if="vars.dlg.finder.key === 'enduser'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-clearance v-else-if="vars.dlg.finder.key === 'clearance'" @change="methods.finderReturnHandler" />
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

import PopupItemDetail from '@/components/base/popup-item-detail';
import DataGridClient from '../../components/base/data-client.vue';
import DataGridClearance from '../../components/import/data-clearance.vue';

import authService from '../../auth';

import { getStock } from '../../data-source/setup';
import { baseClient, baseCodeLoader } from '../../data-source/base';
import { importClearance, getImportShipmentItem, getImportClearanceItem, getImportApprovalCost, getImportClearanceCost } from '../../data-source/import';

import stateStore from '@/utils/state-store';
import printDocument from '@/utils/print-document';
import { loadEmployee, loadWarehouse, loadDepartment } from '../../utils/data-loader';
import { calcPriceSummary, generateItemButtonOption, getFirstCodeNameInBaseCodeList, currentDateTime } from '../../utils/util';
import ApiService from '../../utils/api-service';

export default {
  components: {
    DxButton,
    DxTextArea,
    DxLoadPanel,
    DxToolbar, DxItem,
    DxPopup, DxToolbarItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxCustomRule, DxRequiredRule,
    DxDataGrid, DxColumn, DxPaging, DxLookup, DxEditing, DxSorting, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, DxGridItem, DxGridToolbar, DxGridButton,
    DataGridClient, DataGridClearance,
    PopupItemDetail,
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
    vars.grid = { shipmentItem: null, clearanceItem: null };
    vars.dlg = {};
    vars.dlg.addItem = reactive({ show: false });
    vars.dlg.finder = reactive({ title: '', key: null, data: null, show: false });
    vars.warehouse = {};
    vars.filter = {};
    vars.filter.shipmentItem = { supplier: null };
    vars.filter.clearanceItem = [{ name: 'fk_import_clearance_id', op: 'eq', val: props.id || 0 }];
    vars.dataSource = reactive({
      currency: [],
      employee: [],
      warehouse: [],
      department: [],
      shipmentItem: null,
      clearanceItem: getImportClearanceItem(vars.filter.clearanceItem),
    });
    vars.disabled = reactive({
      new: false,
      edit: true,
      save: true,
      items: true,
      delete: true,
      manager: true,
      tradeYn: false,
    });
    vars.focus = reactive({ clearanceItem: null });
    vars.itemDetail = reactive({ visible: false, id: 0 });

    vars.summary = {};
    vars.summary.total_price_import = computed(() => numeral(vars.formData.total_price_import).format('0,0.00'));
    vars.summary.total_price_cost = computed(() => '₩' + numeral(vars.formData.total_price_cost).format('0,0'));

    onMounted(async () => {
      await loadDepartment(vars.dataSource);
      await methods.loadBaseCode();
      methods.initById(props.id);
      loadWarehouse(vars.dataSource);
    });

    // public methods
    const methods = {
      async initById(id) {
        await methods.gridClearanceItemRefresh(id);
        if (!id) {
          methods.clearFormData();

          vars.disabled.edit = true;
          vars.disabled.delete = true;
          vars.disabled.save = true;
          vars.disabled.items = true;
          vars.disabled.manager = true;
          return;
        }

        let { data } = await importClearance.byKey(id);
        Object.assign(vars.formData, data);

        methods.enableDelete();
        vars.disabled.edit = false;
        if (vars.formData.supplier && vars.formData.clearance_department) {
          methods.enableSave();
          vars.disabled.items = false;
        }
        methods.onSupplierChanged();
      },
      clearFormData() {
        vars.formData.id = null;
        vars.formData.created = null;
        vars.formData.clearance_number = ''; // 통관번호
        vars.formData.clearance_date = ''; // 통관일자
        vars.formData.clearance_department = ''; // 부서
        vars.formData.member = ''; // 담당자
        vars.formData.supplier = ''; // 공급업체
        vars.formData.buyer = ''; // 고객업체
        vars.formData.currency = ''; // 통화
        vars.formData.ex_rate = 0; // 환율
        vars.formData.remark = ''; // 참고사항
        vars.formData.fk_company_id = authService.getCompanyId();
      },
      async addSelectedRows() {
        const grid = vars.grid.clearanceItem;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        const rows = await vars.grid.shipmentItem.getSelectedRowsData();
        for (let row of rows) {
          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code; // 품목코드
          data.item = { ...row.item }; // 품목
          data.qty = row.qty; // 수량
          data.import_price = row.import_price; // 수입단가
          data.amount = data.qty * data.import_price; // 총금액
          data.won_price = data.import_price * vars.formData.ex_rate; // 단가(원)
          data.won_amount = data.amount * vars.formData.ex_rate; // 총금액(원)
          data.cost_price = 0; // 
          data.cost_rate = 0; // 
          data.import_shipment_number = row.shipment.shipment_number; // 선적번호
          data.warehouse = { ...vars.warehouse }; // 입고창고
          data.warehouse_code = vars.warehouse.wh_code; // 창고코드
          data.fk_import_shipment_item_id = row.id; // 선적품목 ID
          data.fk_import_clearance_id = vars.formData.id; // 통관 ID
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
        methods.gridClear(vars.grid.shipmentItem);
        vars.dlg.addItem.show = true;
      },
      gridClear(grid) {
        if (grid) {
          grid.clearSelection();
          grid.refresh();
        }
      },
      async gridClearanceItemRefresh(id) {
        if (!id) id = 0;
        vars.filter.clearanceItem[0].val = id;
        vars.dataSource.clearanceItem.defaultFilters = vars.filter.clearanceItem;
        if (vars.grid.clearanceItem) {
          vars.grid.clearanceItem.cancelEditData();
          vars.grid.clearanceItem.refresh();
        }
      },
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`import-clearance-${key}`, evt.component);
      },
      async newItem() {
        methods.gridClearanceItemRefresh();
        if (vars.formData.id) {
          methods.redirect();
          vars.formData.id = null;
        }
        setTimeout(() => {
          vars.formData.created = null;
          vars.formData.clearance_date = currentDateTime();
          vars.formData.clearance_department = authService.getDepartmentName();
          vars.formData.member = authService.getUserName();
          vars.formData.currency = methods.getFirstCurrency();
          vars.formData.fk_company_id = authService.getCompanyId();

          vars.formState.readOnly = false;
        }, 200);
      },
      async editItem() {
        if (!vars.formData.id) { return; }
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
            await importClearance.remove(vars.formData.id);
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
            await importClearance.update(vars.formData.id, vars.formData);
            if (vars.grid.clearanceItem) { await vars.grid.clearanceItem.saveEditData(); }

            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');

            methods.enableSave();
            methods.enableDelete();
          } else {
            // 채번이 없을 경우 자동 채번
            console.log(vars.formData);
            let { data } = await importClearance.insert(vars.formData);
            vars.formData.id = data.id;

            const grid = vars.grid.clearanceItem;
            if (grid && grid.hasEditData()) {
              await grid.saveEditData();
            }

            methods.redirect(data.id);
            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');
          }
        } catch (ex) {
          if (ex.response.status === 602) {
            notifyError('이미 존재하는 통관번호 입니다');
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
          case 'clearance': {
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

        vars.filter.shipmentItem.supplier = client ? client.name : '';
        methods.loadShipmentItem();

        if (!client) {
          vars.disabled.edit = true;
          vars.disabled.delete = true;
          vars.disabled.save = true;
          vars.disabled.items = true;
          vars.disabled.tradeYn = false;
          vars.formData.member = null;
        } else {
          if (vars.formState.readOnly || vars.disabled.tradeYn) {
            vars.disabled.tradeYn = false;
          } else {
            let isSelect = true;
            if (client.trade_yn) {
              isSelect = await confirm('거래중지 업체입니다. 계속 진행하시겠습니까?', '고객업체');
            }
            if (isSelect) {
              vars.formData.member = null;
            } else {
              vars.formData.supplier = '';
              vars.disabled.tradeYn = true;
              vars.formData.member = null;
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
      onExRateChanged(e) {
        const rows = vars.grid.clearanceItem.getVisibleRows();
        for (const row of rows) {
          row.data.won_price = row.data.import_price * vars.formData.ex_rate;
          row.data.won_amount = row.data.won_price * row.data.qty;
          vars.grid.clearanceItem.cellValue(row.rowIndex, "won_price", row.data.import_price * vars.formData.ex_rate);
          vars.grid.clearanceItem.cellValue(row.rowIndex, "won_amount", row.data.won_price * row.data.qty);
        }
        vars.grid.clearanceItem.refresh();
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
        methods.loadShipmentItem();
      },
      onFocusedCellChanged(e) {
        vars.focus.clearanceItem = e;
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
            element.data.fk_import_clearance_id = vars.formData.id;
            delete element.data.item;
            delete element.data.clearance;
            delete element.data.warehouse;
            delete element.data.basic_stock;
          }
        });
        methods.saveSummary();
      },
      saveSummary() {
        const priceData = {
          total_price_import: vars.formData.total_price_import,
          total_price_won: vars.formData.total_price_won,
          total_price_cost: Math.round(vars.formData.total_price_cost),
        };
        importClearance.update(vars.formData.id, priceData);
      },
      async setWarehouse(newData, value, currentRowData) {
        const warehouseList = vars.dataSource.warehouse;
        for (let i = 0; i < warehouseList.length; i++) {
          if (warehouseList[i].wh_name == value) {
            newData.warehouse = { ...warehouseList[i] };
            newData.warehouse_code = warehouseList[i].wh_code;
            break;
          }
        }
      },
      setQuantity(newData, value, currentRowData) {
        newData.qty = value;
        newData.import_price = currentRowData.import_price;
        newData.amount = newData.qty * newData.import_price;
        newData.won_price = newData.import_price * vars.formData.ex_rate;
        newData.won_amount = newData.qty * newData.won_price;
      },
      setImportPrice(newData, value, currentRowData) {
        newData.qty = currentRowData.qty;
        newData.import_price = value;
        newData.amount = newData.qty * newData.import_price;
        newData.won_price = newData.import_price * vars.formData.ex_rate;
        newData.won_amount = newData.qty * newData.won_price
      },
      calculateCustomSummary(options) {
        if (options.name === 'supply_price') {
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          } else if (options.summaryProcess === 'calculate') {
            options.totalValue += options.value.qty * options.value.import_price;
          } else if (options.summaryProcess === 'finalize') {
            vars.formData.total_price_import = options.totalValue;
            vars.formData.total_price_won = vars.formData.total_price_import * vars.formData.ex_rate;
            // vars.formData.total_price = vars.formData.total_price_import + vars.formData.total_price_won;
          }
        }else if(options.name === 'total_price_cost'){
          if(options.summaryProcess === 'start'){
            options.totalValue = 0;
          }else if(options.summaryProcess === 'calculate'){
            options.totalValue += options.value.qty * options.value.cost_price;
          }else if(options.summaryProcess === 'finalize'){
            vars.formData.total_price_cost = options.totalValue;
          }
        }
      },
      loadBaseCode() {
        return baseCodeLoader([
          'currency',
        ]).then((response) => {
          vars.dataSource.currency = response['currency'];
        }).then(() => (vars.init.value = true));
      },
      loadShipmentItem() {
        vars.dataSource.shipmentItem = getImportShipmentItem([
          {
            name: 'shipment',
            op: 'has',
            val: {
              name: 'supplier',
              op: 'eq',
              val: vars.filter.shipmentItem.supplier,
            },
          },
          {
            name: 'not_clearance',
            op: 'gt',
            val: 0,
          },
        ]);
      },
      checkPossibleSave() {
        if (vars.formData.supplier && vars.formData.clearance_department) {
          methods.enableSave();
          vars.disabled.items = false;
        }
      },
      getFirstCurrency() {
        return getFirstCodeNameInBaseCodeList(vars.dataSource.currency);
      },
      redirect(id) {
        if (id) { router.replace({ path: `/import/clearance/${id}` }); }
        else { router.replace({ path: `/import/clearance` }); }
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
        const { data: clearanceItem } = await vars.dataSource.clearanceItem.load();
        params.list = [...clearanceItem];
        await printDocument('import-clearance', params);
      },
      enableDelete() {
        if (vars.formState.readOnly) { vars.disabled.delete = true; }
        else { vars.disabled.delete = false; }
      },
      enableSave() {
        if (vars.formState.readOnly) { vars.disabled.save = true; }
        else { vars.disabled.save = false; }
      },
      async calculateCostPrice() {
        if (!vars.formData.id) return;

        // 수입결재비용, 수입통관비용 확인
        const { data: clearanceItems } = await vars.dataSource.clearanceItem.load();
        for (const item of clearanceItems) {
          const { data: approvalCostItems } = await getImportApprovalCost([
            {
              name: 'shipment',
              op: 'has',
              val: {
                name: 'shipment_number',
                op: 'eq',
                val: item.import_shipment_number,
              },
            }
          ]).load();
          if (!approvalCostItems || approvalCostItems.length <= 0) {
            await alert('선적번호로 등록된 수입결재비용이 없습니다', '수입원가마감');
            return; 
          }

          const { data: clearanceCostItems }  = await getImportClearanceCost([
            {
              name: 'fk_import_clearance_id',
              op: 'eq',
              val: item.fk_import_clearance_id,
            }
          ]).load();
          if (!clearanceCostItems || clearanceCostItems.length <= 0) {
            await alert('통관번호로 등록된 수입통관비용이 없습니다', '수입원가마감');
            return; 
          }
        }

        vars.loading.value = true;
        const api = new ApiService('/api/mes/v1/import_cost');
        const params = { 
          clearance_id: vars.formData.id
        };
        try {
          const response = await api.post('', params);
          methods.gridClearanceItemRefresh(vars.formData.id);
          console.log(response);            
        } catch (ex) {
          console.log(ex);
        } finally {
          vars.loading.value = false;
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
