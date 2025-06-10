<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">

        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">입고</div>
            </dx-item>
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{text: '신규',  type: 'add', icon: 'add', disabled: vars.disabled.new, onClick: methods.newItem}"
            />
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{text: '수정', type: 'rename', icon: 'rename', disabled: vars.disabled.edit, onClick: methods.editItem}"
            />
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{text: '삭제', type: 'remove', icon: 'remove', disabled: vars.disabled.delete, onClick: methods.deleteItem}"
            />
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{text: '저장', type: 'save', icon: 'save', disabled: vars.disabled.save, onClick: methods.saveItem}"
            />
          </dx-toolbar>
        </div>

        <dx-form :form-data="vars.formData">
          <dx-group-item :col-count="5">
            <dx-group-item>
              <dx-simple-item data-field="receiving_number"
                :editor-options="{
                  placeholder: '(자동 or 직접입력)',
                  ...generateItemButtonOption('search', methods.createFindPopupFn('receiving', '입고조회')),
                }"
              >
                <dx-label text="입고번호" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="receiving_date" editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  ...vars.formState,
                }"
              >
                <dx-label text="수불일자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="receiving_date2" editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  ...vars.formState,
                }"
              >
                <dx-label text="입고일자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="client_company"
                :editor-options="{
                  onFocusOut: methods.onClientChanged,
                  onValueChanged: methods.onClientChanged,
                  onEnterKey: methods.createFindPopupFn('client', '업체조회', { name: vars.formData.client_company }),
                  ...generateItemButtonOption('search', methods.createFindPopupFn('client', '업체조회', { name: vars.formData.client_company })),
                  ...vars.formState,
                }"
              >
                <dx-label text="공급업체" :show-colon="false" />
                <dx-required-rule message="공급업체를 선택하세요" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="receiving_department" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'department_name',
                  displayExpr: 'department_name',
                  acceptCustomValue: true,
                  dataSource: vars.dataSource.department,
                  onValueChanged: methods.onDepartmentChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="입고부서" :show-colon="false" />
                <dx-required-rule message="입고부서를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="receiving_manager" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'emp_name',
                  displayExpr: 'emp_name',
                  disabled: vars.disabled.manager,
                  dataSource: vars.dataSource.employee,
                  ...vars.formState,
                }"
              >
                <dx-label text="입고담당자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="receiving_type" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  dataSource: vars.dataSource.receiving_type,
                  ...vars.formState,
                }"
              >
                <dx-label text="입고구분" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="vat_type" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  dataSource: vars.dataSource.vat_type,
                  onValueChanged: methods.onVatTypeChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="부가세구분" :show-colon="false" />
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
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  acceptCustomValue: true,
                  dataSource: vars.dataSource.delivery_place,
                  ...vars.formState,
                }"
              >
                <dx-label text="납품장소" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="ref_number" :editor-options="{ ...vars.formState }">
                <dx-label text="참고번호" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="project_number"
                :editor-options="{
                  ...generateItemButtonOption('search', methods.createFindPopupFn('project', '프로젝트조회')),
                  ...vars.formState,
                }"
              >
                <dx-label text="프로젝트번호" :show-colon="false" :allow-editing="false" />
              </dx-simple-item>
              <dx-simple-item data-field="client_manager" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'name',
                  displayExpr: 'name',
                  acceptCustomValue: true,
                  disabled: vars.disabled.clientManager,
                  dataSource: vars.dataSource.client_manager,
                  ...vars.formState,
                }"
              >
                <dx-label text="업체담당자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="end_user"
                :editor-options="{
                  ...generateItemButtonOption('search', methods.createFindPopupFn('enduser', '고객조회')),
                  ...vars.formState,
                }"
              >
                <dx-label text="EndUser" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="note" :editor-options="{ ...vars.formState }">
                <dx-label text="참고사항" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="confirmed" editor-type="dxCheckBox"
                :visible="false"
                :editor-options="{ onValueChanged: methods.onConfirmChanged }"
              >
                <dx-label text="입고확정" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="etc" editor-type="dxTextArea"
                :editor-options="{
                  height: '174px',
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
            :on-initialized="evt => methods.onGridInitialized(evt, 'item1')"
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

            <dx-column caption="품목코드" data-field="item_code" width="180" :allow-editing="false" />
            <dx-column caption="품명" data-field="item.item_name" :allow-editing="false" />
            <dx-column caption="규격" data-field="item.item_standard" :allow-editing="false" />
            <dx-column caption="발주번호" data-field="order_number" :allow-editing="false" />
            <dx-column caption="발주수량" data-field="order_quantity" data-type="number" format="fixedPoint" :allow-editing="false" />
            <dx-column caption="입고수량" data-field="receiving_quantity" data-type="number" format="fixedPoint" :set-cell-value="methods.setQuantity" />
            <dx-column caption="단가" data-field="unit_price" data-type="number" format="₩,##0.00" :set-cell-value="methods.setUnitPrice" />
            <dx-column caption="단위" data-field="item.unit" :allow-editing="false" />
            <dx-column caption="공급가" data-field="supply_price" data-type="number" format="₩,##0" :allow-editing="false" />
            <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
            <dx-column caption="입고창고" data-field="warehouse.wh_name" :allow-editing="false" />
            <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :allow-editing="false" />
            <dx-column caption="가입고번호" data-field="prereceiving.prereceiving_number" />
            <dx-column caption="LOT번호" data-field="lot_number" :allow-editing="false" />
            <dx-column caption="공급처 LOT번호" data-field="supplier_lot_number" data-type="text" :allow-editing="true" />
            <dx-column caption="프로젝트 번호" data-field="project_number" :editor-options="{...generateItemButtonOption('search', methods.createFindPopupFn('project-item', '프로젝트조회'))}" />
            <dx-column caption="품목설명" data-field="item.item_detail" :allow-editing="false" />
            <dx-column caption="참고사항" data-field="note" />
            <dx-column caption="고객사품번" data-field="client_item_number" />
            <dx-column caption="종결" data-field="closing_yn" data-type="boolean" />
            <dx-column caption="입고아이디" data-field="fk_receiving_id" :visible="false" :show-in-column-chooser="false" />
            <dx-column caption="발주 품목 아이디" data-field="fk_order_item_id" :visible="false" :show-in-column-chooser="false" />
            <dx-column caption="가입고 아이디" data-field="fk_prereceiving_id" :visible="false" :show-in-column-chooser="false" />
            <dx-column caption="가입고 품목 아이디" data-field="fk_prereceiving_item_id" :visible="false" :show-in-column-chooser="false" />
            <dx-column caption="창고코드" data-field="warehouse_code" :visible="false" :show-in-column-chooser="false" />
            
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
      title="가입고에서 가져오기"  
      content-template="popup-content"
      v-model:visible="vars.dlg.addItem.show"
      width="70%"
      :height="460"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'load-order-popup')"
    >
      <dx-toolbar-item toolbar="top" location="after" widget="dxButton"
        :options="{icon: 'add', text: '선택된 항목 추가', onClick: methods.addSelectedRows}"
      />

      <template #popup-content>
        <dx-data-grid
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="vars.dataSource.prereceivingItem"
          :on-initialized="evt => methods.onGridInitialized(evt, 'prereceivingItem')"
        >
          <dx-column caption="공급업체" data-field="prereceiving.client_company" />
          <dx-column caption="가입고번호" data-field="prereceiving.prereceiving_number" :sort-index="1" sort-order="desc" />
          <dx-column caption="가입고일자" data-field="prereceiving.prereceiving_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
          <dx-column caption="품목코드" data-field="item.item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="발주수량" data-field="order_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="가입고수량" data-field="prereceiving_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="검수수량" data-field="check_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="불량수량" data-field="bad_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="양품수량" data-field="good_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="미입고수량" data-field="not_shipped" data-type="number" format="fixedPoint" />
          <dx-column caption="LOT번호" data-field="lot_number" />
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" />

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
      width="70%"
      :height="500"
      :key="vars.dlg.finder.key"
      :title="vars.dlg.finder.title"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'multiuse-popup')"
    >
      <template #popup-content>
        <data-grid-client v-if="vars.dlg.finder.key === 'client'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-client v-else-if="vars.dlg.finder.key === 'enduser'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-receiving v-else-if="vars.dlg.finder.key === 'receiving'" @change="methods.finderReturnHandler" />
        <data-grid-project v-else-if="vars.dlg.finder.key === 'project'" @change="methods.finderReturnHandler" />
        <data-grid-project v-else-if="vars.dlg.finder.key === 'project-item'" @change="methods.finderReturnHandler" />
        <div v-else-if="vars.dlg.finder.key === 'etc'">
          <div class="mb-2">
            <dx-text-area :height="190" :value="vars.dlg.finder.data" @update:value="methods.updateEtcValue" />
          </div>
          <dx-toolbar>
            <dx-item toolbar="top" location="after" widget="dxButton"
              :options="{icon: null, text: '닫기', onClick: methods.finderReturnHandler}"
            />
          </dx-toolbar>
        </div>
      </template>
    </dx-popup>

    <popup-item-detail v-model:visible="vars.itemDetail.visible" :item-id="vars.itemDetail.id" />
  </div>
</template>

<script>
import numeral from 'numeral';

import { useRouter } from 'vue-router';
import { onMounted, ref, reactive, computed, watch, nextTick } from 'vue';

import { DxButton } from 'devextreme-vue/button';
import DxTextArea from 'devextreme-vue/text-area';
import { confirm, alert } from 'devextreme/ui/dialog';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxCustomRule, DxRequiredRule } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxEditing, DxSorting, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, 
  DxItem as DxGridItem, DxToolbar as DxGridToolbar, DxButton as DxGridButton } from 'devextreme-vue/data-grid';

import { setupControl } from '../../data-source/setup';
import { baseClient, baseCodeLoader } from '../../data-source/base';
import { purchaseReceiving, getPurchasePreReceivingItem, getPurchaseReceivingItem } from '../../data-source/purchase';

import authService from '../../auth';
import stateStore from '@/utils/state-store';
import { notifyInfo, notifyError } from '../../utils/notify';
import { calcPriceSummary, generateItemButtonOption, beforeExitConfirm, currentDateTime } from '../../utils/util';
import { loadEmployee, loadWarehouse, loadDepartment, loadClientManager } from '../../utils/data-loader';

import PopupItemDetail from '@/components/base/popup-item-detail';
import DataGridClient from '../../components/base/data-client.vue';
import DataGridProject from '../../components/project/data-project.vue';
import DataGridReceiving from '../../components/purchase/data-receiving.vue';

export default {
  components: {
    DxButton,
    DxTextArea,
    DxLoadPanel,
    DxToolbar, DxItem,
    DxPopup, DxToolbarItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxCustomRule, DxRequiredRule,
    DxDataGrid, DxColumn, DxPaging, DxEditing, DxSorting, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, 
    DxGridItem, DxGridToolbar, DxGridButton,
    PopupItemDetail, DataGridClient, DataGridProject, DataGridReceiving,
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
    vars.grid = { prereceivingItem: null, item1: null };
    vars.dlg.addItem = reactive({ show: false });
    vars.dlg.finder = reactive({
      show: false,
      title: '',
      key: null,
      data: null,
    });
    vars.warehouse = {};
    vars.warehouseName = '';
    vars.filter = {
      prereceivingItem: { clientCompany: null },
      item1: [{ name: 'fk_receiving_id', op: 'eq', val: props.id || 0 }],
    };
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
      payment_terms: [],
      receiving_type: [],
      vat_type: [],
      delivery_place: [],
      client_manager: [],
      department: [],
      employee: [],
      warehouse: [],
      prereceivingItem: null,
      item1: getPurchaseReceivingItem(vars.filter.item1),
    });
    vars.control = {
      not_use_prereceiving: false,
    };
    vars.focus = reactive({
      item1: null,
    });
    vars.formData = reactive({});

    vars.summary = {};
    vars.summary.supply_price = computed(() => '₩' + numeral(vars.formData.supply_price).format('0,0'));
    vars.summary.vat = computed(() => '₩' + numeral(vars.formData.vat).format('0,0'));
    vars.summary.total_price = computed(() => '₩' + numeral(vars.formData.total_price).format('0,0'));

    vars.itemDetail = reactive({ visible: false, id: 0 });

    onMounted(async () => {
      await methods.loadControl();
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
          vars.formData.id = null;
          vars.formData.created = null;
          vars.formData.receiving_number = '';
          vars.formData.receiving_date = '';
          vars.formData.client_company = '';
          vars.formData.client_manager = '';
          vars.formData.receiving_department = '';
          vars.formData.receiving_manager = '';
          vars.formData.receiving_type = '';
          vars.formData.vat_type = '';
          vars.formData.payment_terms = '';
          vars.formData.delivery_date = '';
          vars.formData.delivery_place = '';
          vars.formData.ref_number = '';
          vars.formData.project_number = '';
          vars.formData.end_user = '';
          vars.formData.note = '';
          vars.formData.etc = '';
          vars.formData.supply_price = 0;
          vars.formData.vat = 0;
          vars.formData.total_price = 0;
          vars.formData.confirmed = 0;
          vars.formData.fk_company_id = authService.getCompanyId();

          vars.disabled.edit = true;
          vars.disabled.delete = true;
          vars.disabled.save = true;
          vars.disabled.items = true;
          vars.disabled.manager = true;
          vars.disabled.clientManager = true;
          return;
        }

        let { data } = await purchaseReceiving.byKey(id);
        Object.assign(vars.formData, data);

        methods.enableDelete();
        vars.disabled.edit = false;
        if (
          vars.formData.client_company &&
          vars.formData.receiving_department
        ) {
          methods.enableSave();
          vars.disabled.items = false;
        }
        methods.onClientChanged();
      },
      async addSelectedRows() {
        const grid = vars.grid.item1;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }
        
        const rows = await vars.grid.prereceivingItem.getSelectedRowsData();

        if (rows.length) {
          console.info(`입고구분을 ${rows[0].prereceiving.receiving_type}로 변경`)
          vars.formData.receiving_type = rows[0].prereceiving.receiving_type
        }

        for (let row of rows) {
          const projectNumber = row.project_number ? row.project_number : vars.formData.project_number;

          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code; // 품목코드
          data.item = { ...row.item }; // 품목
          data.order_number = row.order_number; // 발주번호
          data.order_quantity = row.order_quantity; // 발주수량
          data.receiving_quantity = row.not_shipped; // 입고수량
          data.unit_price = row.unit_price; // 단가
          data.supply_price = methods.calculateTotalPriceWithDecimal(data.unit_price, data.receiving_quantity); // 공급가
          data.request_delivery_date = row.request_delivery_date; // 요청납기
          data.basic_stock = { ...row.basic_stock }; // 기초재고
          data.warehouse = { ...row.warehouse }; // 입고창고
          data.warehouse_code = row.warehouse_code; // 창고코드
          data.prereceiving = row.prereceiving; // 가입고
          data.lot_number = row.lot_number; // LOT번호
          data.note = row.note
          data.project_number = projectNumber; // 프로젝트번호
          data.client_item_number = row.client_item_number; // 고객사품번
          data.closing_yn = false; // 종결
          data.fk_order_item_id = row.fk_order_item_id; // 발주품목 아이디
          data.fk_prereceiving_id = row.fk_prereceiving_id; // 가입고 아이디
          data.fk_prereceiving_item_id = row.id; // 가입고품목 아이디
          data.fk_receiving_id = vars.formData.id; // 입고 아이디
        }
        grid.refresh();
        vars.dlg.addItem.show = false;
      },
      createFindPopupFn(key, title, data = null) {
        const _key = key,
          _title = title,
          _data = data;
        return () => {
          vars.dlg.finder.key = _key;
          vars.dlg.finder.data = _data;
          vars.dlg.finder.title = _title;
          vars.dlg.finder.show = true;
        };
      },
      showAddPopup() {
        const notContains = [];
        for (const item of vars.grid.item1.getVisibleRows()) {
          if (!item.id && item.data.fk_prereceiving_item_id) {
            notContains.push(['id', '<>', item.data.fk_prereceiving_item_id], 'and');
          }
        }
        notContains.pop()

        if (vars.grid.prereceivingItem) {
          vars.grid.prereceivingItem.filter(notContains);
          vars.grid.prereceivingItem.clearSelection();
          vars.grid.prereceivingItem.refresh();
        }
        vars.dlg.addItem.show = true;
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
        stateStore.bind(`purchase-receiving-${key}`, evt.component);
      },
      async newItem() {
        methods.gridItem1Refresh();
        if (vars.formData.id) {
          methods.redirect();
          vars.formData.id = null;
        }
        setTimeout(() => {
          vars.formData.created = null;
          vars.formData.receiving_date = vars.formData.receiving_date2 = currentDateTime();
          vars.formData.receiving_department = authService.getDepartmentName();
          vars.formData.receiving_manager = authService.getUserName();
          vars.formData.receiving_type = methods.getFirstReceivingType();
          vars.formData.vat_type = methods.getFirstVatType();
          vars.formData.payment_terms = methods.getFirstPaymentTerms();
          vars.formData.delivery_place = methods.getFirstDeliveryPlace();
          vars.formData.fk_company_id = authService.getCompanyId();

          vars.formState.readOnly = false;
        }, 200);
      },
      async editItem() {
        if (!vars.formData.id) return;
        if (vars.formState.readOnly && vars.formData.confirmed) return;
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
            await purchaseReceiving.remove(vars.formData.id);
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
            await purchaseReceiving.update(vars.formData.id, vars.formData);
            if (vars.grid.item1) await vars.grid.item1.saveEditData();

            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');

            methods.enableSave();
            methods.enableDelete();
          } else {
            // 채번이 없을 경우 자동 채번
            let { data } = await purchaseReceiving.insert(vars.formData);
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
          if (ex.response.status === 602) {
            notifyError('이미 존재하는 입고번호 입니다');
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
          case 'receiving': {
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
            break;
          }
          case 'project-item': {
            vars.grid.item1.cellValue(
              vars.focus.item1.rowIndex,
              vars.focus.item1.columnIndex,
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
      validateExistClient({ value }) {
        const client = vars.dataSource.client_company.find(
          client => client.name === value
        );
        return !!client;
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

        vars.filter.prereceivingItem.clientCompany = client ? client.name : null;
        methods.loadPrereceivingItem();

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
          if (
            vars.formData.client_company &&
            vars.formData.receiving_department
          ) {
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
          vars.formData.receiving_manager = null;
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
        methods.loadPrereceivingItem();
      },
      onFocusedCellChanged(e) {
        vars.focus.item1 = e;
      },
      onSavingItem(e) {
        e.changes.forEach(element => {
          if (element.type != 'remove') {
            element.data.fk_receiving_id = vars.formData.id;
            delete element.data.item;
            delete element.data.receiving;
            delete element.data.basic_stock;
            delete element.data.warehouse;
            delete element.data.prereceiving;
            delete element.data.prereceiving_item;
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
        purchaseReceiving.update(vars.formData.id, priceData);
      },
      onDataError(e) {
        if (e.error.response.status == 605) {
          e.error.message = '연결된 데이터가 있어서 삭제가 안됩니다';
        } else if (e.error.response.status == 403) {
          e.error.message = '권한이 없습니다';
        }
      },
      calculateDisplayValue(rowData) {
        let unit_price = rowData.unit_price;
        if (!unit_price || unit_price === '') {
          return unit_price;
        }
  
        if (typeof unit_price !== 'string') {
          unit_price = unit_price.toString();
        }
        
        const [integerPart, decimalPart] = unit_price.split('.');
        const formattedIntegerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        const displayValue = formattedIntegerPart + (decimalPart ? `.${decimalPart.slice(0, 2)}` : '');

        return displayValue;
      },
      calculateTotalPriceWithDecimal(unitPrice, quantity) {
        const decimalPlaces = (unitPrice.toString().split('.')[1] || '').length;
        const conversionUnit = Math.pow(10, decimalPlaces);
        const roundedUnitPrice = Math.round(unitPrice * conversionUnit);
        const total = Math.floor(roundedUnitPrice * quantity / conversionUnit);

        return total;
      },
      setQuantity(newData, value, currentRowData) {
        newData.receiving_quantity = value;
        newData.unit_price = currentRowData.unit_price;
        newData.supply_price = methods.calculateTotalPriceWithDecimal(newData.unit_price, newData.receiving_quantity);
      },
      setUnitPrice(newData, value, currentRowData) {
        newData.receiving_quantity = currentRowData.receiving_quantity;
        newData.unit_price = value;
        newData.supply_price = methods.calculateTotalPriceWithDecimal(newData.unit_price, newData.receiving_quantity);
      },
      calculateCustomSummary(options) {
        if (options.name === 'supply_price') {
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          } else if (options.summaryProcess === 'calculate') {
            options.totalValue += methods.calculateTotalPriceWithDecimal(options.value.unit_price, options.value.receiving_quantity);
          } else if (options.summaryProcess === 'finalize') {
            const response = calcPriceSummary(vars.formData.vat_type, options.totalValue);
            vars.formData.supply_price = response.supply_price;
            vars.formData.vat = response.vat;
            vars.formData.total_price = response.total_price;
          }
        }
      },
      loadBaseCode() {
        return baseCodeLoader(
            ['부가세구분', '입고구분', '결재조건', '납품장소']
          ).then(response => {
            vars.dataSource.payment_terms = response['결재조건'];
            vars.dataSource.receiving_type = response['입고구분'];
            vars.dataSource.vat_type = response['부가세구분'];
            vars.dataSource.delivery_place = response['납품장소'];
          }).then(() => (vars.init.value = true));
      },
      loadControl() {
        setupControl.load({
            filter: [['fk_company_id', '=', authService.getCompanyId()]],
            take: 1,
            skip: 0,
          }).then(response => {
            if (response.data.length > 0) {
              vars.control.not_use_prereceiving = response.data[0].not_use_prereceiving;
            }
          });
      },
      loadPrereceivingItem() {
        const filters = [
          {
            name: 'prereceiving',
            op: 'has',
            val: { name: 'client_company', op: 'eq', val: vars.filter.prereceivingItem.clientCompany }
          },
          { name: 'not_shipped', op: 'gt', val: 0},
          { name: 'check_yn', op: 'eq', val: true }
        ];
        vars.dataSource.prereceivingItem = getPurchasePreReceivingItem(filters);
      },
      checkPossibleSave() {
        if (vars.formData.client_company && vars.formData.receiving_department) {
          methods.enableSave();
          vars.disabled.items = false;
        }
      },
      getFirstReceivingType() {
        return methods.getFirstItemName(vars.dataSource.receiving_type);
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
        return itemList[0].code_name;
      },
      redirect(id) {
        if (id) { router.replace({ path: `/purchase/receiving/${id}` }); }
        else { router.replace({ path: `/purchase/receiving` }); }
      },
      itemPopupClick({ column, data }) {
        if (column.name === 'item_code') {
          vars.itemDetail.id = data.item.id;
          vars.itemDetail.visible = true;
        }
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
