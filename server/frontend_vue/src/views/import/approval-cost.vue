<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">수입결재비용</div>
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
          <dx-group-item :col-count="4">
            <dx-group-item>
              <dx-simple-item data-field="approval_cost_number"
                :editor-options="{
                  placeholder: '(자동 or 직접입력)',
                  ...generateItemButtonOption('search', methods.createFindPopupFn('approval-cost', '수입결재비용 조회')),
                }"
              >
                <dx-label text="비용번호" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="approval_cost_date" editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  ...vars.formState,
                }"
              >
                <dx-label text="발행일" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="shipment.shipment_number"
                :editor-options="{
                  ...generateItemButtonOption('search', methods.createFindPopupFn('shipment', '입고 조회')),
                  ...vars.formState,
                }"
              >
                <dx-label text="InvoiceNO" :show-colon="false" />
                <dx-required-rule message="입고를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="cost_type" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  dataSource: vars.dataSource.cost_type,
                  ...vars.formState,
                }"
              >
                <dx-label text="비용구분" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="supplier"
                :editor-options="{
                  onEnterKey: methods.createFindPopupFn('supplier', '고객조회', { name: vars.formData.supplier }),
                  ...generateItemButtonOption('search', methods.createFindPopupFn('supplier', '고객조회', { name: vars.formData.supplier })),
                  ...vars.formState,
                }"
              >
                <dx-label text="공급업체" :show-colon="false" />
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
                  ...vars.formState,
                }"
              >
                <dx-label text="담당부서" :show-colon="false" />
                <dx-required-rule message="부서를 선택하세요" />
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
                <dx-label text="담당자" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="amount" editor-type="dxNumberBox" 
                :editor-options="{
                    format: ',##0.##',
                    onValueChanged: methods.onValueChangedAmount,
                    ...vars.formState 
                }"
              >
                <dx-label text="Amount" :show-colon="false" />
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
                  onValueChanged: methods.onValueChangedExRate,
                  ...vars.formState 
                }"
              >
                <dx-label text="ExRate" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="won_amount" editor-type="dxNumberBox" 
                :editor-options="{
                  format: 'fixedPoint',
                  ...vars.formState 
                }"
              >
                <dx-label text="Won Amt" :show-colon="false" />
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
            :data-source="vars.dataSource.approvalCostItem"
            :on-initialized="(evt) => methods.onGridInitialized(evt, 'approvalCostItem')"
            @saving="methods.onSavingItem"
            @init-new-row="methods.onInitNewRow"
            @data-error-occurred="methods.onDataError"
            @focused-cell-changed="methods.onFocusedCellChanged"
          >
            <dx-grid-toolbar>
              <dx-grid-item name="addRowButton" />
              <dx-grid-item name="saveButton" :visible="!!vars.formData.id" />
              <dx-grid-item name="revertButton" />
              <dx-grid-item name="columnChooserButton" />
            </dx-grid-toolbar>

            <dx-column caption="계정과목" data-field="account_type" width="180" >
              <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.dataSource.account_type" />
            </dx-column>
            <dx-column caption="적요" data-field="briefs">
              <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.dataSource.briefs" />
            </dx-column>
            <dx-column caption="공급업체" data-field="supplier" :allow-editing="false" />
            <dx-column caption="금액" data-field="amount" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :set-cell-value="methods.setAmount" />
            <dx-column caption="지불방법" data-field="payment_method">
              <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.dataSource.payment_method" />
            </dx-column>
            <dx-column caption="비고" data-field="remark" />
            
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
        <data-grid-client        v-if="vars.dlg.finder.key === 'supplier'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-shipment      v-else-if="vars.dlg.finder.key === 'shipment'" @change="methods.finderReturnHandler" />
        <data-grid-approval-cost v-else-if="vars.dlg.finder.key === 'approval-cost'" @change="methods.finderReturnHandler" />
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
import { DxDataGrid, DxColumn, DxPaging, DxLookup, DxEditing, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, 
  DxItem as DxGridItem, DxToolbar as DxGridToolbar, DxButton as DxGridButton } from 'devextreme-vue/data-grid';

import DataGridClient from '../../components/base/data-client.vue';
import DataGridShipment from '../../components/import/data-shipment.vue';
import DataGridApprovalCost from '../../components/import/data-approval-cost.vue';

import { baseClient, baseCodeLoader } from '../../data-source/base';
import { importApprovalCost, getImportApprovalCostItem } from '../../data-source/import';

import authService from '../../auth';

import printDocument from '@/utils/print-document';
import stateStore from '@/utils/state-store';
import { calcPriceSummary, generateItemButtonOption, getFirstCodeNameInBaseCodeList, currentDateTime } from '../../utils/util';
import { loadEmployee, loadWarehouse, loadDepartment } from '../../utils/data-loader';

export default {
  components: {
    DxButton,
    DxTextArea,
    DxLoadPanel,
    DxToolbar, DxItem,
    DxPopup, DxToolbarItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxCustomRule, DxRequiredRule,
    DxDataGrid, DxColumn, DxPaging, DxLookup, DxEditing, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, DxGridItem, DxGridToolbar, DxGridButton,
    DataGridClient, DataGridShipment, DataGridApprovalCost,
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
    vars.grid = { approvalCostItem: null };
    vars.dlg.addItem = reactive({ show: false });
    vars.dlg.addOrderPlanItem = reactive({ show: false });
    vars.dlg.finder = reactive({title: '', key: null, data: null, show: false });
    vars.warehouse = {};
    vars.filter = {};
    vars.filter.approvalCostItem = [{ name: 'fk_import_approval_cost_id', op: 'eq', val: props.id || 0 }];
    vars.dataSource = reactive({
      briefs: [],
      currency: [],
      cost_type: [],
      account_type: [],
      payment_method: [],
      employee: [],
      warehouse: [],
      department: [],
      approvalCostItem: getImportApprovalCostItem(vars.filter.approvalCostItem),
    });
    vars.disabled = reactive({
      new: false,
      edit: true,
      save: true,
      delete: true,
      items: true,
      manager: true,
      tradeYn: false,
    });
    vars.focus = reactive({ approvalCostItem: null });
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
        await methods.refreshGridApprovalCostItem(id);
        if (!id) {
          methods.clearFormData();

          methods.disableEdit(true);
          methods.disableSave(true);
          methods.disableItems(true);
          methods.disableDelete(true);
          methods.disableManager(true);
          return;
        }

        methods.loadFormData(id);

        methods.decideDisableDelete();
        methods.disableEdit(false);
        if (methods.isRequiredDataFilledInFormData()) {
          methods.decideDisableSave();
          methods.disableItems(false);
        }
        methods.onSupplierChanged();
      },
      clearFormData() {
        vars.formData.id = null;
        vars.formData.created = null;
        vars.formData.shipment = null;
        vars.formData.approval_cost_number = ''; // 결재비용번호
        vars.formData.approval_cost_date = ''; // 발행일
        vars.formData.cost_type = ''; // 비용구분
        vars.formData.supplier = ''; // Supplier
        vars.formData.department = ''; // 담당부서
        vars.formData.member = ''; // 담당자
        vars.formData.amount = ''; // Amount
        vars.formData.currency = ''; // Currency
        vars.formData.ex_rate = ''; // ExRate
        vars.formData.won_amount = ''; // Won Amount
        vars.formData.remark = ''; // 비고
        vars.formData.fk_import_shipment_id = null;
        vars.formData.fk_company_id = authService.getCompanyId();
      },
      async loadFormData(id) {
        let { data } = await importApprovalCost.byKey(id);
        Object.assign(vars.formData, data);
      },
      async insertFormData(insertData) {
        return await importApprovalCost.insert(insertData);
      },
      async updateFormData(id, updateData) {
        await importApprovalCost.update(id, updateData);
      },
      async removeFormData(id) {
        await importApprovalCost.remove(id);
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
      clearGrid(grid) {
        if (grid) {
          grid.cancelEditData();
          grid.clearSelection();
          grid.refresh();
        }
      },
      async refreshGridApprovalCostItem(id) {
        if (!id) { id = 0; }
        vars.filter.approvalCostItem[0].val = id;
        vars.dataSource.approvalCostItem.defaultFilters = vars.filter.approvalCostItem;
        methods.clearGrid(vars.grid.approvalCostItem);
      },
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`import-approval-cost-${key}`, evt.component);
      },
      async newItem() {
        methods.refreshGridApprovalCostItem();
        if (methods.isFormDataLoaded()) {
          methods.redirect();
          vars.formData.id = null;
        }
        setTimeout(() => {
          vars.formData.created = null;
          vars.formData.approval_cost_date = currentDateTime();
          vars.formData.department = authService.getDepartmentName();
          vars.formData.member = authService.getUserName();
          vars.formData.currency = methods.getFirstCurrency();
          vars.formData.cost_type = methods.getFirstCostType();
          vars.formData.fk_company_id = authService.getCompanyId();

          methods.setReadOnly(false);
        }, 200);
      },
      async editItem() {
        if (!methods.isFormDataLoaded()) { return; }
        if (methods.isReadOnly()) {
          let isSelect = await confirm('수정하시겠습니까?', '수정');
          if (!isSelect) { return; }
        }

        const saveFormData = Object.assign({}, vars.formData);

        methods.toggleReadOnly();
        methods.decideDisableSave();
        methods.decideDisableDelete();

        await nextTick();
        Object.assign(vars.formData, saveFormData);
      },
      async deleteItem() {
        const result = await confirm('이 항목을 삭제하시겠습니까?', '삭제 확인');
        if (result) {
          try {
            await methods.removeFormData(vars.formData.id);
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
          if (methods.isFormDataLoaded()) {
            // 기존 정보 업데이트
            const updateData = { ...vars.formData };
            delete updateData.shipment;

            await methods.updateFormData(vars.formData.id, updateData);
            await methods.saveGridApprovalCostItem();

            methods.setReadOnly(true);
            notifyInfo('저장되었습니다');

            methods.decideDisableSave();
            methods.decideDisableDelete();
          } else {
            // 채번이 없을 경우 자동 채번
            const updateData = { ...vars.formData };
            delete updateData.shipment;

            let { data } = await methods.insertFormData(updateData);
            vars.formData.id = data.id;

            await methods.saveGridApprovalCostItem();

            methods.redirect(vars.formData.id);
            methods.setReadOnly(true);
            notifyInfo('저장되었습니다');
          }
        } catch (ex) {
          if (ex.response.status === 602) {
            notifyError('이미 존재하는 수입결재비용번호 입니다');
          } else {
            console.error(ex);
            notifyError('저장 할 내용이 없습니다');
          }
        } finally {
          vars.loading.value = false;
        }
      },
      async saveGridApprovalCostItem() {
        await methods.saveGridItem(vars.grid.approvalCostItem);
      },
      async saveGridItem(grid) {
        if (grid && grid.hasEditData()) { await grid.saveEditData(); }
      },
      finderReturnHandler(data) {
        switch (vars.dlg.finder.key) {
          case 'approval-cost': {
            methods.redirect(data.id);
            methods.setReadOnly(true);
            break;
          }
          case 'supplier': {
            vars.formData.supplier = data.name;
            methods.onSupplierChanged();
            break;
          }
          case 'shipment': {
            methods.setFormDataFromShipment(data);
            break;
          }
        }

        vars.dlg.finder.title = '';
        vars.dlg.finder.key = null;
        vars.dlg.finder.data = null;
        vars.dlg.finder.show = false;
      },
      async setFormDataFromShipment(data) {
        vars.formData.supplier = data.supplier;
        vars.formData.amount = data.total_price;
        vars.formData.currency = data.currency;
        vars.formData.ex_rate = data.ex_rate;
        vars.formData.won_amount = data.won_amount;
        vars.formData.fk_import_shipment_id = data.id;
        vars.formData.shipment = { ...data };

        methods.refreshGridApprovalCostItem();

        methods.disableEdit(false);
        methods.disableDelete(false);
        methods.disableSave(false);
        methods.disableItems(false);
      },
      onValueChangedAmount(e) {
        methods.setWonAmount();
      },
      onValueChangedExRate(e) {
        methods.setWonAmount();
      },
      setWonAmount() {
        vars.formData.won_amount = vars.formData.amount * vars.formData.ex_rate
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
        if (!client) {
          methods.disableEdit(true);
          methods.disableDelete(true);
          methods.disableSave(true);
          methods.disableItems(true);
          vars.disabled.tradeYn = false;
        } else {
          if (methods.isReadOnly() || vars.disabled.tradeYn) {
            vars.disabled.tradeYn = false;
          } else {
            let isSelect = true;
            if (client.trade_yn) {
              isSelect = await confirm('거래중지 업체입니다. 계속 진행하시겠습니까?', '고객업체');
            }
            if (!isSelect) {
              vars.formData.supplier = '';
              vars.disabled.tradeYn = true;
            }
          }
        }
        methods.checkPossibleSave();
      },
      onDepartmentChanged(e) {
        if (!e.value) {
          methods.decideDisableSave();
          methods.disableItems(true);
          methods.disableManager(true);
          vars.formData.member = null;
          vars.dataSource.employee = [];
        } else {
          const selectItem = e.component.option('selectedItem');
          if (selectItem) {
            loadEmployee(vars.dataSource, selectItem.id);
            methods.disableManager(false);
          }
        }
        methods.checkPossibleSave();

        const selectedItem = e.component.option('selectedItem');
        if (selectedItem) {
          vars.warehouse = { ...selectedItem.warehouse };
        } else {
          vars.warehouse = {};
        }
      },
      onFocusedCellChanged(e) {
        vars.focus.approvalCostItem = e;
      },
      onDataError(e) {
        if (e.error.response.status == 605) {
          e.error.message = '연결된 데이터가 있어서 삭제가 안됩니다';
        } else if (e.error.response.status == 403) {
          e.error.message = '권한이 없습니다';
        }
      },
      onInitNewRow(e) {
        e.data['amount'] = 0;
        e.data['remark'] = '';
        e.data['supplier'] = vars.formData.supplier;
        e.data['briefs'] = methods.getFirstBriefs();
        e.data['account_type'] = methods.getFirstAccountType();
        e.data['payment_method'] = methods.getFirstPaymentMethod();
      },
      onSavingItem(e) {
        e.changes.forEach((element) => {
          if (element.type != 'remove') {
            element.data.fk_import_approval_cost_id = vars.formData.id;
            delete element.data.shipment;
            delete element.data.approval_cost;
          }
        });
        methods.saveSummary();
      },
      saveSummary() {
        const priceData = {
          total_price: vars.formData.total_price
        };
        importApprovalCost.update(vars.formData.id, priceData);
      },
      setAmount(newData, value, currentRowData) {
        newData.amount = value;
      },
      calculateCustomSummary(options) {
        if (options.name === 'supply_price') {
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          } else if (options.summaryProcess === 'calculate') {
            options.totalValue += Number(options.value.amount);
          } else if (options.summaryProcess === 'finalize') {
            vars.formData.total_price = options.totalValue;
          }
        }
      },
      loadBaseCode() {
        return baseCodeLoader([
          'currency',
          '비용구분',
          '적요',
          '계정과목',
          '지불방법',
        ]).then((response) => {
          vars.dataSource.currency = response['currency'];
          vars.dataSource.cost_type = response['비용구분'];
          vars.dataSource.briefs = response['적요'];
          vars.dataSource.account_type = response['계정과목'];
          vars.dataSource.payment_method = response['지불방법'];
        }).then(() => (vars.init.value = true));
      },
      checkPossibleSave() {
        if (methods.isRequiredDataFilledInFormData()) {
          methods.decideDisableSave();
          methods.disableItems(false);
        }
      },
      getFirstCurrency() {
        return getFirstCodeNameInBaseCodeList(vars.dataSource.currency);
      },
      getFirstCostType() {
        return getFirstCodeNameInBaseCodeList(vars.dataSource.cost_type);
      },
      getFirstBriefs() {
        return getFirstCodeNameInBaseCodeList(vars.dataSource.briefs);
      },
      getFirstAccountType() {
        return getFirstCodeNameInBaseCodeList(vars.dataSource.account_type);
      },
      getFirstPaymentMethod() {
        return getFirstCodeNameInBaseCodeList(vars.dataSource.payment_method);
      },
      redirect(id) {
        let path = '/import/approval-cost';
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

        const orderManager = vars.dataSource.employee.find((v) => v.emp_name === vars.formData.order_manager);
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

        const clientManager = vars.dataSource.client_manager.find((v) => v.name === vars.formData.client_manager);
        
        if (clientManager) params.client_manager = clientManager;
        else params.client_manager = { name: vars.formData.client_manager };

        await printDocument('order', params);
      },
      isFormDataLoaded() {
        return vars.formData.id ? true : false;
      },
      decideDisableDelete() {
        if (methods.isReadOnly()) { methods.disableDelete(true); }
        else { methods.disableDelete(false); }
      },
      decideDisableSave() {
        if (methods.isReadOnly()) { methods.disableSave(true); }
        else { methods.disableSave(false); }
      },
      isRequiredDataFilledInFormData() {
        if (vars.formData.supplier && vars.formData.department) {
          return true;
        }
        return false;
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
      disableEdit(isDisable) {
        vars.disabled.edit = isDisable;
      },
      disableItems(isDisable) {
        vars.disabled.items = isDisable;
      },
      disableManager(isDisable) {
        vars.disabled.manager = isDisable;
      },
      disableSave(isDisable) {
        vars.disabled.save = isDisable;
      },
      disableDelete(isDisable) {
        vars.disabled.delete = isDisable;
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
