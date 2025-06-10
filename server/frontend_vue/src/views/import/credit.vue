<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">Import Credit</div>
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
              <dx-simple-item data-field="credit_number"
                :editor-options="{
                  placeholder: '(자동 or 직접입력)',
                  ...generateItemButtonOption('search', methods.createFindPopupFn('credit', '발주조회')),
                }"
              >
                <dx-label text="Credit No." :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="work_day" editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  ...vars.formState,
                }"
              >
                <dx-label text="Work Day" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="supplier"
                :editor-options="{
                  onEnterKey: methods.createFindPopupFn('supplier', '업체조회', { name: vars.formData.supplier }),
                  ...generateItemButtonOption('search', methods.createFindPopupFn('supplier', '업체조회', { name: vars.formData.supplier })),
                  ...vars.formState,
                }"
              >
                <dx-label text="Supplier" :show-colon="false" />
                <dx-required-rule message="업체를 선택하세요" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="department" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'department_name',
                  displayExpr: 'department_name',
                  dataSource: vars.dataSource.department,
                  onValueChanged: methods.onDepartmentChanged,
                  acceptCustomValue: true,
                  ...vars.formState,
                }"
              >
                <dx-label text="Depart" :show-colon="false" />
                <dx-required-rule message="부서를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="employee" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'emp_name',
                  displayExpr: 'emp_name',
                  dataSource: vars.dataSource.employee,
                  disabled: vars.disabled.manager,
                  ...vars.formState,
                }"
              >
                <dx-label text="Employee" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="due_date" editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  ...vars.formState,
                }"
              >
                <dx-label text="Due Day" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="credit_type" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  dataSource: vars.dataSource.credit_type,
                  ...vars.formState,
                }"
              >
                <dx-label text="Credit Type" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="tax" editor-type="dxNumberBox" 
                :editor-options="{ 
                  format: '#0\'%\'',
                  ...vars.formState 
                }"
              >
                <dx-label text="Tax" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="excute_day" editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  ...vars.formState,
                }"
              >
                <dx-label text="Excute Day" :show-colon="false" />
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
            :data-source="vars.dataSource.creditItem"
            :on-initialized="(evt) => methods.onGridInitialized(evt, 'creditItem')"
            @saving="methods.onSavingItem"
            @data-error-occurred="methods.onDataError"
            @focused-cell-changed="methods.onFocusedCellChanged"
          >
            <dx-grid-toolbar>
              <dx-grid-item name="addRowButton" :options="{ onClick: methods.showAddPopup }" />
              <dx-grid-item name="saveButton" :visible="!!vars.formData.id" />
              <dx-grid-item name="revertButton" />
              <dx-grid-item name="columnChooserButton" />
            </dx-grid-toolbar>

            <dx-column caption="Invoice No" data-field="shipment.shipment_number" width="180" :allow-editing="false" />
            <dx-column caption="ShipDate" data-field="shipment.shipment_date" data-type="date" format="yyyy-MM-dd" :allow-editing="false" />
            <dx-column caption="Amount" data-field="amount" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :allow-editing="false" :set-cell-value="methods.setAmount" />
            
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
      title="선적 찾기"
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
          :data-source="vars.dataSource.shipment"
          :on-initialized="(evt) => methods.onGridInitialized(evt, 'shipment')"
        >
          <dx-column caption="Offer No" data-field="shipment_number" :sort-index="1" sort-order="desc" />
          <dx-column caption="IssueDate" data-field="purchase_order.order_number" :sort-index="0" sort-order="desc" />
          <dx-column caption="P/O No" data-field="item_name" />
          <dx-column caption="Supplier" data-field="supplier" />
          <dx-column caption="buyer" data-field="buyer" />
          <dx-column caption="validity" data-field="validity" />
          <dx-column caption="PayTerms" data-field="pay_terms" />
          <dx-column caption="Destination" data-field="destination" />
          <dx-column caption="Delivery" data-field="delivery" />
          <dx-column caption="Price Terms" data-field="price_terms" />
          <dx-column caption="Origin" data-field="origin" />
          <dx-column caption="ShipPort" data-field="ship_port" />
          <dx-column caption="Packing" data-field="packing" />
          <dx-column caption="AdvBank" data-field="adv_bank" />
          <dx-column caption="Currency" data-field="currency" />
          <dx-column caption="ExRate" data-field="ex_rate" />
          <dx-column caption="Inspection" data-field="inspection" />
          <dx-column caption="Payment" data-field="payment" />
          <dx-column caption="Remark" data-field="remark" />

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
        <data-grid-client v-if="vars.dlg.finder.key === 'supplier'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-credit v-else-if="vars.dlg.finder.key === 'credit'" @change="methods.finderReturnHandler" />
      </template>
    </dx-popup>
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

import DataGridClient from '../../components/base/data-client.vue';
import DataGridCredit from '../../components/import/data-credit.vue';

import authService from '../../auth';

import { baseClient, baseCodeLoader } from '../../data-source/base';
import { importCredit, getImportCreditItem, getImportShipment } from '../../data-source/import';

import stateStore from '@/utils/state-store';
import printDocument from '@/utils/print-document';
import { loadEmployee, loadWarehouse, loadDepartment } from '../../utils/data-loader';
import { calcPriceSummary, generateItemButtonOption, getFirstCodeNameInBaseCodeList, currentDateTime } from '../../utils/util';

export default {
  components: {
    DxButton,
    DxTextArea,
    DxLoadPanel,
    DxToolbar, DxItem,
    DxPopup, DxToolbarItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxCustomRule, DxRequiredRule,
    DxDataGrid, DxColumn, DxPaging, DxLookup, DxEditing, DxSorting, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser,  DxGridItem, DxGridToolbar, DxGridButton,
    DataGridClient, DataGridCredit,
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
    vars.formData = reactive({});
    vars.formState = reactive({ readOnly: true });
    vars.grid = { shipment: null, creditItem: null };
    vars.dlg.addItem = reactive({ show: false });
    vars.dlg.finder = reactive({ title: '', key: null, data: null, show: false });
    vars.warehouse = {};
    vars.filter = {};
    vars.filter.shipment = { supplier: '' };
    vars.filter.creditItem = [{ name: 'fk_import_credit_id', op: 'eq', val: props.id || 0 }];
    vars.dataSource = reactive({
      currency: [],
      credit_type: [],
      employee: [],
      warehouse: [],
      department: [],
      shipment: getImportShipment([{ name: 'supplier', op: 'eq', val: vars.filter.shipment.supplier}]),
      creditItem: getImportCreditItem(vars.filter.creditItem),
    });
    vars.disabled = reactive({
      new: false,
      edit: true,
      save: true,
      delete: true,
      items: true,
      manager: true,
      transaction: false,
    });
    vars.focus = reactive({ creditItem: null });

    vars.summary = {};
    vars.summary.total_price = computed(() => '₩' + numeral(vars.formData.total_price).format('0,0.00'));
    
    onMounted(async () => {
      await loadDepartment(vars.dataSource);
      await methods.loadBaseCode();
      methods.initById(props.id);
      loadWarehouse(vars.dataSource);
    });

    // public methods
    const methods = {
      async initById(id) {
        await methods.refreshGridCreditItem(id);
        if (!id) {
          methods.clearFormData();

          methods.disableEdit();
          methods.disableSave();
          methods.disableDelete();
          methods.disableManager();
          methods.disableItems();
          return;
        }

        await methods.loadFormDataById(id);

        methods.decideEnableDelete();
        methods.enableEdit();
        if (methods.isRequiredDataFilledInFormData()) {
          methods.decideEnableSave();
          methods.enableItems();
        }
        methods.onSupplierChanged();
      },
      clearFormData() {
        vars.formData.id = null;
        vars.formData.created = null;
        vars.formData.credit_number = ''; // 번호
        vars.formData.work_day = ''; // 
        vars.formData.supplier = ''; // 공급업체
        vars.formData.department = ''; // 부서
        vars.formData.employee = ''; // 담당자
        vars.formData.due_day = ''; // 
        vars.formData.credit_type = ''; // 
        vars.formData.tax = 0; // 
        vars.formData.excute_day = ''; // 
        vars.formData.currency = ''; // 환종
        vars.formData.remark = ''; // 참고사항
        vars.formData.total_price = 0;
        vars.formData.fk_company_id = authService.getCompanyId();
      },
      async loadFormDataById(id) {
        let { data } = await importCredit.byKey(id);
        Object.assign(vars.formData, data);
      },
      async addSelectedRows() {
        const grid = vars.grid.creditItem;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        const rows = await vars.grid.shipment.getSelectedRowsData();
        for (let row of rows) {
          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.amount = row.total_price; // 총 금액
          data.fk_import_shipment_id = row.id; // 선적 ID
          data.fk_import_credit_id = vars.formData.id; // 계산서 ID
          data.shipment = { ...row };
        }
        grid.refresh();
        methods.hideAddPopup();
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
        methods.clearGrid(vars.grid.shipment);
        vars.dlg.addItem.show = true;
      },
      hideAddPopup() {
        vars.dlg.addItem.show = false;
      },
      clearGrid(grid) {
        if (grid) {
          grid.cancelEditData();
          grid.clearSelection();
          grid.refresh();
        }
      },
      async refreshGridCreditItem(id) {
        if (!id) { id = 0; }
        vars.filter.creditItem[0].val = id;
        vars.dataSource.creditItem.defaultFilters = vars.filter.creditItem;
        if (vars.grid.creditItem) {
          methods.clearGrid(vars.grid.creditItem);
        }
      },
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`import-credit-${key}`, evt.component);
      },
      async newItem() {
        methods.refreshGridCreditItem();
        if (vars.formData.id) {
          methods.redirect();
          vars.formData.id = null;
        }
        setTimeout(() => {
          vars.formData.created = null;
          vars.formData.work_day = currentDateTime();
          vars.formData.currency = methods.getFirstCurrency();
          vars.formData.credit_type = methods.getFirstCreditType();
          vars.formData.department = authService.getDepartmentName();
          vars.formData.employee = authService.getUserName();
          vars.formData.fk_company_id = authService.getCompanyId();

          methods.setReadOnly(false);
        }, 200);
      },
      async editItem() {
        if (!vars.formData.id) { return; }
        if (methods.isReadOnly()) {
          let isSelect = await confirm('수정하시겠습니까?', '수정');
          if (!isSelect) {
            return;
          }
        }

        const saveFormData = Object.assign({}, vars.formData);

        methods.toggleReadOnly();
        methods.decideEnableSave();
        methods.decideEnableDelete();

        await nextTick();
        Object.assign(vars.formData, saveFormData);
      },
      async deleteItem() {
        const result = await confirm('이 항목을 삭제하시겠습니까?', '삭제 확인');
        if (result) {
          try {
            await importCredit.remove(vars.formData.id);
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
            await importCredit.update(vars.formData.id, vars.formData);
            await methods.saveGridCreditItem();

            methods.setReadOnly(true);
            notifyInfo('저장되었습니다');

            methods.decideEnableSave();
            methods.decideEnableDelete();
          } else {
            // 채번이 없을 경우 자동 채번
            let { data } = await importCredit.insert(vars.formData);
            vars.formData.id = data.id;

            await methods.saveGridCreditItem();

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
      async saveGridCreditItem() {
        await methods.saveGridItem(vars.grid.creditItem);
      },
      async saveGridItem(grid) {
        if (grid && grid.hasEditData()) { await grid.saveEditData(); }
      },
      finderReturnHandler(data) {
        switch (vars.dlg.finder.key) {
          case 'credit': {
            methods.redirect(data.id);
            methods.setReadOnly(true);
            break;
          }
          case 'supplier': {
            vars.formData.supplier = data.name;
            methods.onSupplierChanged();
            break;
          }
        }

        vars.dlg.finder.title = '';
        vars.dlg.finder.key = null;
        vars.dlg.finder.data = null;
        vars.dlg.finder.show = false;
      },
      async loadBaseClient(clientName) {
        const { data } = await baseClient.load({
          filter: [
            ['fk_company_id', '=', authService.getCompanyId()],
            ['name', '=', clientName],
          ],
          take: 1,
          skip: 0,
        });
        const client = data.length > 0 ? data[0] : null;
        return client;
      },
      async onSupplierChanged() {
        const clientName = vars.formData.supplier;
        const client = await methods.loadBaseClient(clientName);
        if (!client) {
          methods.disableEdit();
          methods.disableSave();
          methods.disableDelete();
          methods.disableItems();
          methods.disableTransaction();
        } else {
          if (methods.isReadOnly() || methods.isTransaction()) {
            methods.enableTransaction();
          } else {
            let isSelect = true;
            if (client.trade_yn) {
              isSelect = await confirm('거래중지 업체입니다. 계속 진행하시겠습니까?', '고객업체');
            }
            if (!isSelect) {
              vars.formData.supplier = '';
              methods.disableTransaction();
            }
          }
        }
        methods.setShipmentFilter(vars.formData.supplier);
        methods.loadShipment();
        methods.checkIsPossibleToSave();
      },
      onDepartmentChanged(e) {
        if (!e.value) {
          methods.decideEnableSave();
          methods.disableItems();
          methods.disableManager();
          vars.formData.employee = null;
          vars.dataSource.employee = [];
        } else {
          const selectItem = e.component.option('selectedItem');
          if (selectItem) {
            loadEmployee(vars.dataSource, selectItem.id);
            methods.enableManager();
          }
        }
        methods.checkIsPossibleToSave();

        const selectedItem = e.component.option('selectedItem');
        if (selectedItem) {
          vars.warehouse = { ...selectedItem.warehouse };
        } else {
          vars.warehouse = {};
        }
        methods.loadShipment();
      },
      onFocusedCellChanged(e) {
        vars.focus.creditItem = e;
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
            element.data.fk_import_credit_id = vars.formData.id;
            delete element.data.credit;
            delete element.data.shipment;
            delete element.data.warehouse;
            delete element.data.basic_stock;
          }
        });
        methods.saveSummary();
      },
      saveSummary() {
        const priceData = {
          total_price: vars.formData.total_price
        };
        importCredit.update(vars.formData.id, priceData);
      },
      setAmount(newData, value, currentRowData) {
        newData.amount = value;
      },
      calculateCustomSummary(options) {
        if (options.name === 'supply_price') {
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          } else if (options.summaryProcess === 'calculate') {
            options.totalValue += options.value.amount;
          } else if (options.summaryProcess === 'finalize') {
            vars.formData.total_price = options.totalValue
          }
        }
      },
      loadBaseCode() {
        return baseCodeLoader([
          'currency',
          'Credit Type',
        ]).then((response) => {
          vars.dataSource.currency = response['currency'];
          vars.dataSource.credit_type = response['Credit Type'];
        }).then(() => (vars.init.value = true));
      },
      loadShipment() {
        vars.dataSource.shipment = getImportShipment([
          {
            name: 'supplier',
            op: 'eq',
            val: vars.filter.shipment.supplier,
          },
        ]);
      },
      setShipmentFilter(clientName) {
        vars.filter.shipment.supplier = clientName;
      },
      checkIsPossibleToSave() {
        if (methods.isRequiredDataFilledInFormData()) {
          methods.decideEnableSave();
          methods.enableItems();
        }
      },
      isRequiredDataFilledInFormData() {
        if (vars.formData.supplier && vars.formData.department) {
          return true;
        }
        return false;
      },
      getFirstCurrency() {
        return getFirstCodeNameInBaseCodeList(vars.dataSource.currency);
      },
      getFirstCreditType() {
        return getFirstCodeNameInBaseCodeList(vars.dataSource.credit_type);
      },
      redirect(id) {
        let path = '/import/credit';
        if (id) { path = `${path}/${id}` }
        router.replace({ path: path });
      },
      async printDocument() {
        if (!vars.formData.id) return;
        const params = { ...vars.formData };
        params.supply_price = numeral(vars.formData.supply_price).format('0,0');
        params.total_price = numeral(vars.formData.total_price).format('0,0');
        params.tax_price = numeral(vars.formData.total_price - vars.formData.supply_price).format('0,0');
        params.order_date = moment(vars.formData.order_date).format('YYYY년 M월 D일');
        params.delivery_date = moment(vars.formData.delivery_date).format('YYYY년 M월 D일');

        const orderManager = vars.dataSource.employee.find((v) => v.emp_name === vars.formData.employee);
        if (orderManager) {
          params.order_manager = orderManager;
          const department = vars.dataSource.department.find((v) => v.id === orderManager.fk_department_id);
          if (department)
            params.order_manager.department_name = department.department_name;
        } else params.order_manager = { emp_name: vars.formData.order_manager };

        const { data: item1 } = await vars.dataSource.item1.load();
        params.items = [...item1];
        params.items.forEach((item) => {
          item.unit_price = numeral(item.unit_price).format('0,0');
          item.supply_price = numeral(item.supply_price).format('0,0');

          const { total_price } = calcPriceSummary(
            vars.formData.vat_type,
            item.supply_price
          );
          item.total_price = numeral(total_price).format('0,0');
        });
        await printDocument('order', params);
      },
      decideEnableDelete() {
        if (methods.isReadOnly()) { methods.disableDelete(); }
        else { methods.enableDelete(); }
      },
      decideEnableSave() {
        if (methods.isReadOnly()) { methods.disableSave(); }
        else { methods.enableSave(); }
      },
      isReadOnly() {
        return vars.formState.readOnly;
      },
      setReadOnly(isReadOnly) {
        vars.formState.readOnly = isReadOnly;
      },
      toggleReadOnly() {
        vars.formState.readOnly = !vars.formState.readOnly;
      },
      enableEdit() {
        vars.disabled.edit = false;
      },
      disableEdit() {
        vars.disabled.edit = true;
      },
      enableItems() {
        vars.disabled.items = false;
      },
      disableItems() {
        vars.disabled.items = true;
      },
      enableManager() {
        vars.disabled.manager = false;
      },
      disableManager() {
        vars.disabled.manager = true;
      },
      enableSave() {
        vars.disabled.save = false;
      },
      disableSave() {
        vars.disabled.save = true;
      },
      enableDelete() {
        vars.disabled.delete = false;
      },
      disableDelete() {
        vars.disabled.delete = true;
      },
      enableTransaction() {
        vars.disabled.transaction = false;
      },
      disableTransaction() {
        vars.disabled.transaction = true;
      },
      isTransaction() {
        return vars.disabled.transaction;
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
