<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">결재(매입계산서)</div>
            </dx-item>
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{ text: '신규', type: 'add', icon: 'add', disabled: vars.disabled.new, onClick: methods.newItem }"
            />
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{ text: '수정', type: 'rename', icon: 'rename', disabled: vars.disabled.edit, onClick: methods.editItem }"
            />
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{ text: '삭제', type: 'remove', icon: 'remove', disabled: vars.disabled.delete, onClick: methods.deleteItem }"
            />
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{ text: '저장', type: 'save', icon: 'save', disabled: vars.disabled.save, onClick: methods.saveItem }"
            />
            <dx-item location="after" locate-in-menu="auto" widget="dxButton" :visible="false"
              :options="{ text: '출력', type: 'print', icon: 'print', onClick: methods.printDocument }"
            />
          </dx-toolbar>
        </div>

        <dx-form :form-data="vars.formData">
          <dx-group-item :col-count="5">
            <dx-group-item>
              <dx-simple-item
                data-field="payment_number"
                :editor-options="{
                  placeholder: '(자동 or 직접입력)',
                  ...generateItemButtonOption('search', methods.createFindPopupFn('payment', '결제조회')),
                }"
              >
                <dx-label text="결재번호" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="payment_date" editor-type="dxDateBox"
                :editor-options="{ dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss', ...vars.formState }"
              >
                <dx-label text="결재일자" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="client_company"
                :editor-options="{
                  ...generateItemButtonOption(
                    'search',
                    methods.createFindPopupFn('client', '업체조회', {name: vars.formData.client_company})
                  ),
                  ...vars.formState,
                  onEnterKey: methods.createFindPopupFn('client', '업체조회', {name: vars.formData.client_company}),
                }"
              >
                <dx-label text="공급업체" :show-colon="false" />
                <dx-required-rule message="공급업체를 선택하세요" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="payment_department" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.department,
                  displayExpr: 'department_name',
                  valueExpr: 'department_name',
                  acceptCustomValue: true,
                  onValueChanged: methods.onDepartmentChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="결재부서" :show-colon="false" />
                <dx-required-rule message="영업부서를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="payment_manager" editor-type="dxSelectBox"
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
              <dx-simple-item data-field="etc" editor-type="dxTextArea"
                :editor-options="{
                  ...generateItemButtonOption('rename', methods.createFindPopupFn('etc', '비고', vars.formData.etc)),
                  ...vars.formState,
                  height: '80px',
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
        <div class="mt-2">
          <dx-data-grid
            class="fixed-header-table"
            height="calc(100vh - 416px)"
            date-serialization-format="yyyy-MM-ddTHH:mm:ss"
             column-resizing-mode="widget"
            :on-initialized="evt => methods.onGridInitialized(evt, 'item1')"
            :data-source="vars.dataSource.item1"
            :show-borders="true"
            :remote-operations="false"
            :column-auto-width="true"
            :focused-row-enabled="true"
            :allow-column-resizing="true"
            :row-alternation-enabled="true"
            :allow-column-reordering="true"
            :select-text-on-edit-start="true"
            @saving="methods.onSavingItem"
            @cell-dbl-click="methods.itemPopupClick"
            @data-error-occurred="methods.onDataError"
          >
            <dx-grid-toolbar>
              <dx-item template="addFromStatement" location="before" :visible="vars.isAllowEdit.value" />
              <dx-grid-item name="addRowButton" />
              <dx-grid-item name="saveButton" :visible="!!vars.formData.id" />
              <dx-grid-item name="revertButton" />
              <dx-grid-item name="columnChooserButton" />
            </dx-grid-toolbar>
            <template #addFromStatement>
              <dx-button text="계산서에서 가져오기" icon="add" @click="methods.showAddPopup" />
            </template>

            <dx-column caption="계산서번호" data-field="statement.statement_number" width="180" :allow-editing="false" />
            <dx-column caption="금액" data-field="price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :allow-editing="true" :set-cell-value="methods.setPrice" />
            <dx-column caption="결제형태" data-field="payment_type">
              <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.dataSource.payment_type" />
            </dx-column>
            <dx-column caption="결제적요" data-field="etc" />
            <dx-column caption="미결제" data-field="statement.not_payment" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
            <dx-column caption="계산서아이디" data-field="fk_statement_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
            
             <dx-summary :recalculate-while-editing="true" :calculate-custom-summary="methods.calculateCustomSummary">
              <dx-total-item name="total_price" summary-type="custom" />
            </dx-summary>

            <dx-editing mode="batch" :use-icons="true"
              :allow-adding="vars.isAllowEdit.value"
              :allow-updating="!vars.formState.readOnly"
              :allow-deleting="!vars.formState.readOnly"
            />
            <dx-scrolling mode="standard" />
            <dx-column-chooser mode="select" :enabled="true" />
          </dx-data-grid>
        </div>

        <div class="mt-2">
          <table class="summary-table">
            <tr>
              <th>합계금액</th>
              <td>{{ vars.summary.total_price.value}}</td>
            </tr>
          </table>
        </div>

      </div>
    </div>

    <dx-popup
      title="계산서찾기"
      content-template="popup-content"
      v-model:visible="vars.dlg.addItem.show"
      width="70%"
      :height="460"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="
        (evt) => methods.onGridInitialized(evt, 'find-statement-popup')
      "
    >
      <dx-toolbar-item
        widget="dxButton"
        toolbar="top"
        location="after"
        :options="{
          text: '선택된 항목 추가',
          icon: 'add',
          onClick: methods.addSelectedRows,
        }"
      />

      <template #popup-content>
        <dx-data-grid
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="{
            filtering: true,
            grouping: true,
            groupPaging: true,
            paging: true,
            sorting: true,
            summary:false
          }"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="vars.dataSource.statement"
          :on-initialized="evt => methods.onGridInitialized(evt, 'statement')"
        >
          <dx-column caption="공급업체" data-field="client_company" />
          <dx-column caption="계산서번호" data-field="statement_number" :sort-index="1" sort-order="desc" />
          <dx-column caption="발행일자" data-field="statement_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
          <dx-column caption="매입부서" data-field="statement_department" />
          <dx-column caption="매입담당자" data-field="statement_manager" />
          <dx-column caption="부가세구분" data-field="vat_type" />
          <dx-column caption="계산서유형" data-field="statement_type" />
          <dx-column caption="결재유형" data-field="approval_type" />
          <dx-column caption="발행구분" data-field="publish_type" />
          <dx-column caption="본지점구분" data-field="office_type" />
          <dx-column caption="부가세" data-field="vat" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
          <dx-column caption="공급가" data-field="supply_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
          <dx-column caption="합계금액" data-field="total_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
          <dx-column caption="미결제" data-field="not_payment" data-type="number" :visible="true" :format="{ type: 'fixedPoint', precision: 2 }" />

          <dx-summary>
            <dx-total-item column="vat" summary-type="sum" value-format=",##0.00" display-format="부가세: {0}" />
            <dx-total-item column="supply_price" summary-type="sum" value-format=",##0.00" display-format="공급가: {0}" />
            <dx-total-item column="total_price" summary-type="sum" value-format=",##0.00" display-format="합계금액: {0}" />
            <dx-total-item column="not_payment" summary-type="sum" value-format=",##0.00" display-format="미결제: {0}" />
          </dx-summary>

          <dx-paging :page-size="20" />
          <dx-sorting mode="multiple" />
          <dx-filter-row :visible="true" />
          <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick" />
        </dx-data-grid>
      </template>
    </dx-popup>

    <dx-popup
      v-model:visible="vars.dlg.finder.show"
      content-template="popup-content"
      :title="vars.dlg.finder.title"
      :close-on-outside-click="true"
      width="70%"
      :height="500"
      :key="vars.dlg.finder.key"
      :resize-enabled="true"
      @initialized="evt => methods.onGridInitialized(evt, 'multiuse-popup')"
    >
      <template #popup-content>
        <data-grid-client v-if="vars.dlg.finder.key === 'client'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-client v-else-if="vars.dlg.finder.key === 'enduser'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-payment v-else-if="vars.dlg.finder.key === 'payment'" @change="methods.finderReturnHandler" />
        <data-grid-project v-else-if="vars.dlg.finder.key === 'project'" @change="methods.finderReturnHandler" />
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

  </div>
</template>

<script>
import { remove } from 'lodash'
import numeral from 'numeral';
import { useRouter } from 'vue-router';
import { ref, reactive, computed, watch, nextTick, onMounted } from 'vue';

import { DxButton } from 'devextreme-vue/button';
import DxTextArea from 'devextreme-vue/text-area';
import { confirm, alert } from 'devextreme/ui/dialog';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxCustomRule, DxRequiredRule } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxLookup, DxPaging, DxEditing, DxSorting, DxSelection, DxFilterRow,
  DxScrolling, DxColumnChooser, DxItem as DxGridItem, DxToolbar as DxGridToolbar, DxSummary, DxTotalItem } from 'devextreme-vue/data-grid';

import { getStock } from '../../data-source/setup';
import { baseItem, baseClient, baseCodeLoader } from '../../data-source/base';

import DataGridClient from '../../components/base/data-client.vue';
import DataGridPayment from '../../components/purchase/data-payment.vue';
import DataGridProject from '../../components/project/data-project.vue';

import authService from '../../auth';
import stateStore from '@/utils/state-store';
import { generateItemButtonOption, beforeExitConfirm, currentDateTime } from '../../utils/util';
import { loadEmployee, loadDepartment, loadClientManager } from '../../utils/data-loader';
import { notifyInfo, notifyError } from '../../utils/notify';
import { getPurchasePaymentItem, getPurchaseStatement, purchasePayment } from '../../data-source/purchase';

export default {
  components: {
    DxButton,
    DxTextArea,
    DxLoadPanel,
    DxToolbar, DxItem,
    DxPopup, DxToolbarItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxCustomRule, DxRequiredRule,
    DxDataGrid, DxColumn, DxLookup, DxPaging, DxEditing, DxSorting, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, DxGridItem, DxGridToolbar, DxSummary, DxTotalItem,
    DataGridClient, DataGridPayment, DataGridProject,
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
    vars.grid = { statement: null, item1: null };
    vars.dlg.addItem = reactive({ show: false });
    vars.dlg.finder = reactive({
      show: false,
      title: '',
      key: null,
      data: null,
    });
    vars.filter = {
      statement: {
        clientCompany: null,
      },
      item1: [{ name: 'fk_payment_id', op: 'eq', val: props.id || 0 }],
    };
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
      payment_type: [],
      client_manager: [],
      department: [],
      employee: [],
      statement: null,
      item1: getPurchasePaymentItem(vars.filter.item1),
    });
    vars.formData = reactive({});

    vars.summary = {};
    vars.summary.total_price = computed( () => '₩' + numeral(vars.formData.total_price).format('0,0'))

    vars.isAllowEdit = computed(() => {
      return !vars.formState.readOnly && !!vars.formData.client_company
    });

    onMounted(async () => {
      await loadDepartment(vars.dataSource);
      await methods.loadBaseCode();
      methods.initById(props.id);
    });

    // public methods
    const methods = {
      async initById(id) {
        beforeExitConfirm.check(() => !vars.disabled.save)
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

        let { data } = await purchasePayment.byKey(id);
        Object.assign(vars.formData, data);

        methods.enableDelete();
        vars.disabled.edit = false;
        if (vars.formData.client_company && vars.formData.payment_department) {
          methods.enableSave();
          vars.disabled.items = false;
        }
        methods.onClientChanged();
      },
      clearFormData() {
        vars.formData.id = null;
        vars.formData.created = null;
        vars.formData.payment_number = '';
        vars.formData.payment_date = '';
        vars.formData.client_company = '';
        vars.formData.client_manager = '';
        vars.formData.payment_department = '';
        vars.formData.payment_manager = '';
        vars.formData.fk_company_id = authService.getCompanyId();
      },
      async addSelectedRows() {
        const grid = vars.grid.item1;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        const rows = await vars.grid.statement.getSelectedRowsData();
        
        for (let row of rows) {
          grid.on("initNewRow", (e) => {
            e.data.statement = row;
            e.data.price = Number(row.not_payment);
            e.data.payment_type = '';
            e.data.fk_statement_id = row.id;
          })
          grid.addRow();
          grid.off("initNewRow");
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
        if (!id) { id = 0; }
        vars.filter.item1[0].val = id;
        vars.dataSource.item1.defaultFilters = vars.filter.item1;
        if (vars.grid.item1) {
          vars.grid.item1.cancelEditData();
          vars.grid.item1.refresh();
        }
      },
      showAddPopup() {
        const notContains = [];
        for (const item of vars.grid.item1.getVisibleRows()) {
          if (!item.id) {
            notContains.push(['id', '<>', item.data.fk_statement_id], 'and');
          }
        }
        notContains.pop()

        if (vars.grid.statement) {
          vars.grid.statement.filter(notContains);
          vars.grid.statement.clearSelection();
          vars.grid.statement.refresh();
        }
        vars.dlg.addItem.show = true;
      },
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`purchase-${key}`, evt.component);
      },
      async newItem() {
        methods.gridItem1Refresh();
        if (vars.formData.id) {
          methods.clearFormData();
          methods.redirect();
        }
        setTimeout(() => {
          methods.clearFormData();

          vars.formData.payment_date = currentDateTime();
          vars.formData.payment_department = authService.getDepartmentName();
          vars.formData.payment_manager = authService.getUserName();
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
            await purchasePayment.remove(vars.formData.id);
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
            delete updateDate.payment_number;
            const { data } = await purchasePayment.update(vars.formData.id, updateDate);
            vars.formData.payment_number = data.payment_number;
            if (vars.grid.item1) await vars.grid.item1.saveEditData();

            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');

            methods.enableSave();
            methods.enableDelete();
          } else {
            // 채번이 없을 경우 자동 채번
            if (vars.formData.created) vars.formData.created = null;
            let { data } = await purchasePayment.insert(vars.formData);
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
            notifyError('이미 존재하는 입금번호 입니다');
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
          case 'payment': {
            methods.redirect(data.id);
            vars.formState.readOnly = true;
            break;
          }
          case 'client': {
            vars.formData.client_company = data.name;
            methods.onClientChanged();
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
              if (vars.formData.client_company) {
                methods.onClientChanged();
              }
            }
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

        vars.filter.statement.clientCompany = client ? client.name : null;
        methods.loadStatement();

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
              isSelect = await confirm('거래중지 업체입니다. 계속 진행하시겠습니까?', '공급업체');
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
              vars.formData.end_user = e.previousValue;
              vars.disabled.tradeYn = true;
              return;
            }
          }
        }
        vars.disabled.tradeYn = false;
      },
      async onConfirmChanged(e) {
        if (!vars.formData.id) {
          return;
        }
        if (e.value) {
          vars.formState.readOnly = true;
          vars.disabled.edit = true;
          vars.disabled.delete = true;
          vars.disabled.items = true;
        } else {
          if (vars.formData.client_company && vars.formData.payment_department) {
            methods.enableDelete();
            vars.disabled.edit = false;
            vars.disabled.items = false;
          }
        }
      },
      updateEtcValue(v) {
        vars.dlg.finder.data = v;
      },
      onDepartmentChanged(e) {
        if (!e.value) {
          vars.disabled.save = true;
          vars.disabled.items = true;
          vars.disabled.manager = true;
          vars.formData.payment_manager = null;
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
        remove(e.changes, (element) => {
          return ['insert', 'update'].includes(element.type) && isNaN(element.data.price)
        })
        e.changes.forEach(element => {
          if (element.type != 'remove') {
            element.data.fk_payment_id = vars.formData.id;
            delete element.data.statement;
          }
        });
        methods.saveSummary();
      },
      saveSummary(){
        const piceDate = {
          total_price : vars.formData.total_price
        }
        purchasePayment.update(vars.formData.id, piceDate)

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
      setPrice(newData, value, currentRowData) {
        if (currentRowData.statement && currentRowData.statement.not_payment) {
          if (value > currentRowData.statement.total_price) {
            newData.price = currentRowData.statement.total_price;
          } else {
            newData.price = value;
          }
        } else {
          newData.price = value;
        }
      },
      calculateCustomSummary(options){
        if (options.name === 'total_price'){
          if(options.summaryProcess === 'start'){
            options.totalValue = 0;
          }else if(options.summaryProcess === 'calculate'){
            options.totalValue += options.value.price;
          }else if(options.summaryProcess === 'finalize'){
            vars.formData.total_price = options.totalValue
          }
        }
      },
      loadBaseCode() {
        return baseCodeLoader(['입금형태']).then(response => {
          vars.dataSource.payment_type = response['입금형태'];
        }).then(() => (vars.init.value = true));
      },
      loadStatement() {
        vars.dataSource.statement = getPurchaseStatement([
          {
            name: 'client_company',
            op: 'eq',
            val: vars.filter.statement.clientCompany,
          },
          {
            name: 'not_payment',
            op: 'neq',
            val: 0,
          },
        ]);
      },
      checkPossibleSave() {
        if (vars.formData.client_company && vars.formData.payment_department) {
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
      redirect(id) {
        if (id) { router.replace({ path: `/purchase/payment/${id}` }); }
        else { router.replace({ path: `/purchase/payment` }); }
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
