<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">출고반품</div>
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
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{ text: '출력', type: 'print', icon: 'print', onClick: methods.printDocument }"
            />
          </dx-toolbar>
        </div>

        <dx-form :form-data="vars.formData">
          <dx-group-item :col-count="5">
            <dx-group-item>
              <dx-simple-item
                data-field="return_number"
                :editor-options="{
                  placeholder: '(자동 or 직접입력)',
                  ...generateItemButtonOption('search', methods.createFindPopupFn('return', '반품조회')),
                }"
              >
                <dx-label text="반품번호" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="return_date" editor-type="dxDateBox" :editor-options="{ dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss', ...vars.formState }">
                <dx-label text="반품일자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="client_company"
                :editor-options="{
                  ...generateItemButtonOption(
                    'search',
                    methods.createFindPopupFn('client', '고객조회', {name: vars.formData.client_company})
                  ),
                  ...vars.formState,
                  onEnterKey: methods.createFindPopupFn('client', '고객조회', {name: vars.formData.client_company}),
                }"
              >
                <dx-label text="고객업체" :show-colon="false" />
                <dx-required-rule message="고객업체를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="client_manager" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.client_manager,
                  displayExpr: 'name',
                  valueExpr: 'name',
                  acceptCustomValue: true,
                  disabled: vars.disabled.clientManager,
                  ...vars.formState,
                }"
              >
                <dx-label text="업체담당자" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="return_department" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.department,
                  displayExpr: 'department_name',
                  valueExpr: 'department_name',
                  acceptCustomValue: true,
                  onValueChanged: methods.onDepartmentChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="반품부서" :show-colon="false" />
                <dx-required-rule message="반품부서 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="return_manager" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.employee,
                  displayExpr: 'emp_name',
                  valueExpr: 'emp_name',
                  disabled: vars.disabled.manager,
                  ...vars.formState,
                }"
              >
                <dx-label text="반품담당자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="return_type" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.return_type,
                  displayExpr: 'code_name',
                  valueExpr: 'code_name',
                  ...vars.formState,
                }"
              >
                <dx-label text="반품구분" :show-colon="false" />
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
              <dx-simple-item data-field="etc" editor-type="dxTextArea"
                :editor-options="{
                  ...generateItemButtonOption('rename', methods.createFindPopupFn('etc', '비고', vars.formData.etc)),
                  ...vars.formState,
                  height: '174px',
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
              <dx-item template="addFromRelease" location="after" :visible="!vars.formState.readOnly" />
              <dx-grid-item name="addRowButton" :options="{ onClick: methods.showAddPopup }" />
              <dx-grid-item name="saveButton" :visible="!!vars.formData.id" />
              <dx-grid-item name="revertButton" />
              <dx-grid-item name="columnChooserButton" />
            </dx-grid-toolbar>
            <template #addFromRelease>
              <dx-button text="출고에서 가져오기" icon="add" @click="methods.showAddReleasePopup" />
            </template>

            <dx-column caption="품목코드" data-field="item_code" width="180" :allow-editing="false" />
            <dx-column caption="품명" data-field="item.item_name" :allow-editing="false" />
            <dx-column caption="규격" data-field="item.item_standard" :allow-editing="false" />
            <dx-column caption="출고수량" data-field="release_quantity" data-type="number" format="fixedPoint" :allow-editing="true" />
            <dx-column caption="반품수량" data-field="return_quantity" data-type="number" format="fixedPoint" :set-cell-value="methods.setQuantity" />
            <dx-column caption="미계산서" data-field="non_invoice" data-type="number" format="fixedPoint" :allow-editing="false" />
            <dx-column caption="단가" data-field="unit_price" data-type="number" format="currency" :allow-editing="true" />
            <dx-column caption="반품원가" data-field="cost_price" data-type="number" format="currency" :allow-editing="true" />
            <dx-column caption="단위" data-field="item.unit" :allow-editing="false" />
            <dx-column caption="공급가" data-field="supply_price" data-type="number" format="currency" :allow-editing="false" />
            <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
            <dx-column caption="미반품수량" data-type="number" format="fixedPoint" :allow-editing="false" :calculate-display-value="methods.calcNotReturnedQuantity" />
            <dx-column caption="입고창고" data-field="warehouse.wh_name" :set-cell-value="methods.setWarehouse">
              <dx-lookup value-expr="wh_name" display-expr="wh_name" :data-source="vars.dataSource.warehouse" />
            </dx-column>
            <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :allow-editing="false" />
            <dx-column caption="출고번호" data-field="release.release_number" :allow-editing="false" />
            <dx-column caption="출고일" data-field="release.release_date" :allow-editing="false" />
            <dx-column caption="반품사유" data-field="return_reason" />
            <dx-column caption="출고아이디" data-field="fk_release_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
            <dx-column caption="출고 품목 아이디" data-field="fk_release_item_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
            <dx-column caption="반품아이디" data-field="fk_release_return_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
            <dx-column caption="창고코드" data-field="warehouse_code" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
            
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
      title="출고품목찾기"
      content-template="popup-content"
      v-model:visible="vars.dlg.addReleaseItem.show"
      width="70%"
      :height="460"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'find-release-popup')"
    >
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ text: '선택된 항목 추가', icon: 'add', onClick: methods.addSelectedReleaseRows }"
      />

      <template #popup-content>
        <dx-data-grid
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="vars.dataSource.releaseItem"
          :on-initialized="evt => methods.onGridInitialized(evt, 'releaseItem')"
        >
          <dx-column caption="고객업체" data-field="release.client_company" />
          <dx-column caption="출고번호" data-field="release.release_number" :sort-index="1" sort-order="desc" />
          <dx-column caption="출고일자" data-field="release.release_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="출고수량" data-field="release_quantity" />
          <dx-column caption="미계산서수량" data-field="non_invoice" />

          <dx-paging :page-size="20" />
          <dx-sorting mode="multiple" />
          <dx-filter-row :visible="true" />
          <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick" />
        </dx-data-grid>
      </template>
    </dx-popup>

    <dx-popup
      title="품목찾기"
      content-template="popup-content"
      v-model:visible="vars.dlg.addItem.show"
      :width="680"
      :height="500"
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
          :column-auto-width="true"
          :remote-operations="true"
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
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :calculate-display-value="methods.availableStock" :allow-sorting="false" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :calculate-display-value="methods.currentStock" :allow-sorting="false" />

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
      :resize-enabled="true"
      :close-on-outside-click="true"
      :key="vars.dlg.finder.key"
      :title="vars.dlg.finder.title"
      @initialized="evt => methods.onGridInitialized(evt, 'multiuse-popup')"
    >
      <template #popup-content>
        <data-grid-client v-if="vars.dlg.finder.key === 'client'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-release-return v-else-if="vars.dlg.finder.key === 'return'" @change="methods.finderReturnHandler" />
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
import { DxDataGrid, DxColumn, DxLookup, DxPaging, DxEditing, DxSorting, DxSummary, DxTotalItem, DxSelection, DxFilterRow,
  DxScrolling, DxColumnChooser, DxItem as DxGridItem, DxToolbar as DxGridToolbar, DxButton as DxGridButton } from 'devextreme-vue/data-grid';

import { getStock } from '../../data-source/setup';
import { baseItem, baseClient, baseCodeLoader, getBaseItem } from '../../data-source/base';
import { shipmentReleaseItem, getShipmentReleaseItem, shipmentReleaseReturn, getShipmentReleaseReturnItem } from '../../data-source/shipment';

import DataGridClient from '../../components/base/data-client.vue';
import DataGridReleaseReturn from '../../components/shipment/data-release-return.vue';
import DataGridProject from '../../components/project/data-project.vue';

import printDocument from '@/utils/print-document';
import authService from '../../auth';
import stateStore from '@/utils/state-store';
import { calcPriceSummary, generateItemButtonOption, beforeExitConfirm, currentDateTime } from '../../utils/util';
import { loadEmployee, loadWarehouse, loadDepartment, loadClientManager } from '../../utils/data-loader';
import { notifyInfo, notifyError } from '../../utils/notify';

import PopupItemDetail from '@/components/base/popup-item-detail';

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
    DataGridClient, DataGridReleaseReturn, DataGridProject,
    PopupItemDetail,
  },
  props: {
    id: [String, Number],
  },
  setup(props) {
    moment.locale('ko')
    // variable 설정
    const router = useRouter();
    const vars = {};
    vars.init = ref(false);
    vars.loading = ref(false);
    vars.formState = reactive({ readOnly: true });
    vars.grid = {};
    vars.grid.releaseItem = null;
    vars.grid.baseItem = null;
    vars.grid.item1 = null;
    vars.dlg = {};
    vars.dlg.addItem = reactive({ show: false });
    vars.dlg.addReleaseItem = reactive({ show: false });
    vars.dlg.finder = reactive({ show: false, title: '', key: null, data: null });
    vars.filter = {};
    vars.filter.releaseItem = { clientCompany: null };
    vars.filter.item1 = [{ name: 'fk_release_return_id', op: 'eq', val: props.id || 0 }];
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
      return_type: [],
      vat_type: [],
      warehouse: [],
      client_manager: [],
      department: [],
      employee: [],
      baseItem: getBaseItem(null, null, null),
      releaseItem: null,
      item1: getShipmentReleaseReturnItem(vars.filter.item1),
    });
    vars.formData = reactive({});
    vars.summary = {};
    vars.summary.supply_price = computed(() => '₩' + numeral(vars.formData.supply_price).format('0,0'));
    vars.summary.vat = computed(() => '₩' + numeral(vars.formData.vat).format('0,0'));
    vars.summary.total_price = computed(() => '₩' + numeral(vars.formData.total_price).format('0,0'));
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

        let { data } = await shipmentReleaseReturn.byKey(id);
        Object.assign(vars.formData, data);

        methods.enableDelete();
        vars.disabled.edit = false;
        if (vars.formData.client_company && vars.formData.return_department) {
          methods.enableSave();
          vars.disabled.items = false;
        }
        methods.onClientChanged();
      },
      clearFormData() {
        vars.formData.id = null;
        vars.formData.created = null;
        vars.formData.return_number = '';
        vars.formData.return_date = '';
        vars.formData.client_company = '';
        vars.formData.client_manager = '';
        vars.formData.return_department = '';
        vars.formData.return_manager = '';
        vars.formData.return_type = '';
        vars.formData.vat_type = '';
        vars.formData.etc = '';
        vars.formData.supply_price = 0;
        vars.formData.vat = 0;
        vars.formData.total_price = 0;
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
          let currentStock = 0;
          if (row.basic_stock) {
            currentStock = row.basic_stock.current_stock;
          }

          await grid.addRow();
          grid.cellValue(0, 'item_code', row.item_code); // 품목코드
          grid.cellValue(0, 'item.item_name', row.item_name); // 품명
          grid.cellValue(0, 'item.item_standard', row.item_standard); // 규격
          grid.cellValue(0, 'release_quantity', 0); // 출고수량
          grid.cellValue(0, 'return_quantity', 0); // 반품수량
          grid.cellValue(0, 'non_invoice', 0); // 미계산서수량
          grid.cellValue(0, 'unit_price', 0); // 단가
          grid.cellValue(0, 'item.unit', row.unit); // 단위
          grid.cellValue(0, 'supply_price', 0); // 공급가
          grid.cellValue(0, 'request_delivery_date', null); // 요청납기
          grid.cellValue(0, 'warehouse.wh_name', null); // 출고창고
          grid.cellValue(0, 'basic_stock.current_stock', currentStock); // 현재고
          grid.cellValue(0, 'release.release_number', null); // 출고번호
          grid.cellValue(0, 'release.release_date', null); // 출고일
          grid.cellValue(0, 'return_reason', ''); // 반품사유
          grid.cellValue(0, 'warehouse_code', null); // 입고창고
          grid.cellValue(0, 'cost_price', 0.0); // 반품원가
          grid.cellValue(0, 'fk_release_id', null);
          grid.cellValue(0, 'fk_release_item_id', null);
          grid.cellValue(0, 'fk_release_return_id', vars.formData.id);
        }
        grid.refresh();
        vars.dlg.addItem.show = false;
      },
      async addSelectedReleaseRows() {
        const grid = vars.grid.item1;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        const rows = await vars.grid.releaseItem.getSelectedRowsData();
        for (let row of rows) {
          let currentStock = 0;
          if (row.basic_stock) {
            currentStock = row.basic_stock.current_stock;
          }

          await grid.addRow();
          grid.cellValue(0, 'item_code', row.item_code); // 품목코드
          grid.cellValue(0, 'item.item_name', row.item.item_name); // 품명
          grid.cellValue(0, 'item.item_standard', row.item.item_standard); // 규격
          grid.cellValue(0, 'release_quantity', row.release_quantity); // 출고수량
          grid.cellValue(0, 'return_quantity', 0); // 반품수량
          grid.cellValue(0, 'non_invoice', 0); // 미계산서수량
          grid.cellValue(0, 'unit_price', row.unit_price); // 단가
          grid.cellValue(0, 'item.unit', row.item.unit); // 단위
          grid.cellValue(0, 'supply_price', row.supply_price); // 공급가
          grid.cellValue(0, 'request_delivery_date', row.request_delivery_date); // 요청납기
          grid.cellValue(0, 'warehouse.wh_name', row.warehouse.wh_name); // 출고창고
          grid.cellValue(0, 'basic_stock.current_stock', currentStock); // 현재고
          grid.cellValue(0, 'release.release_number', row.release.release_number); // 출고번호
          grid.cellValue(0, 'release.release_date', row.release.release_date); // 출고일
          grid.cellValue(0, 'return_reason', ''); // 반품사유
          grid.cellValue(0, 'warehouse_code', row.warehouse.wh_code); // 출고창고
          grid.cellValue(0, 'cost_price', row.cost_price); // 반품원가
          grid.cellValue(0, 'fk_release_id', row.release.id);
          grid.cellValue(0, 'fk_release_item_id', row.id);
          grid.cellValue(0, 'fk_release_return_id', vars.formData.id);
        }
        grid.refresh();
        vars.dlg.addReleaseItem.show = false;
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
        if (vars.grid.baseItem) {
          vars.grid.baseItem.clearSelection();
          vars.grid.baseItem.clearFilter();
          vars.grid.baseItem.refresh();
        }
        vars.dlg.addItem.show = true;
      },
      showAddReleasePopup() {
        const notContains = [];
        for (const item of vars.grid.item1.getVisibleRows()) {
          if (!item.id) {
            notContains.push(['id', '<>', item.data.fk_release_item_id], 'and');
          }
        }
        notContains.pop()

        if (vars.grid.releaseItem) {
          vars.grid.releaseItem.filter(notContains);
          vars.grid.releaseItem.clearSelection();
          vars.grid.releaseItem.refresh();
        }
        vars.dlg.addReleaseItem.show = true;
      },
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`shipment-release-return-${key}`, evt.component);
      },
      async newItem() {
        methods.gridItem1Refresh();
        if (vars.formData.id) {
          methods.clearFormData();
          methods.redirect();
        }
        setTimeout(() => {
          methods.clearFormData();
          vars.formData.return_date = currentDateTime();
          vars.formData.return_department = authService.getDepartmentName();
          vars.formData.return_manager = authService.getUserName();
          vars.formData.return_type = methods.getFirstReturnType();
          vars.formData.vat_type = methods.getFirstVatType();
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
            await shipmentReleaseReturn.remove(vars.formData.id);
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
            delete updateDate.return_number;
            delete updateDate.created;

            const { data } = await shipmentReleaseReturn.update(vars.formData.id, updateDate);
            vars.formData.return_number = data.return_number;
            if (vars.grid.item1) await vars.grid.item1.saveEditData();

            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');

            methods.enableSave();
            methods.enableDelete();
          } else {
            // 채번이 없을 경우 자동 채번
            if (vars.formData.created) { vars.formData.created = null; }
            let { data } = await shipmentReleaseReturn.insert(vars.formData);
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
            notifyError('이미 존재하는 반품번호 입니다');
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
          case 'return': {
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

        vars.filter.releaseItem.clientCompany = client ? client.name : null;
        methods.loadReleaseItem();

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
      updateEtcValue(v) {
        vars.dlg.finder.data = v;
      },
      onDepartmentChanged(e) {
        if (!e.value) {
          vars.disabled.save = true;
          vars.disabled.items = true;
          vars.disabled.manager = true;
          vars.formData.return_manager = null;
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
        e.changes.forEach(element => {
          if (element.type != 'remove') {
            element.data.fk_release_return_id = vars.formData.id;
            delete element.data.item;
            delete element.data.warehouse;
            delete element.data.basic_stock;
            delete element.data.release;
            delete element.data.release_item;
            delete element.data.release_return;
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
        shipmentReleaseReturn.update(vars.formData.id, priceData);
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
      calcNotReturnedQuantity(rowData) {
        if (!rowData.fk_release_item_id) {
          return 0;
        }

        let releaseQuantity = 0;
        if (rowData.release_quantity) { 
          releaseQuantity = rowData.release_quantity; 
        }
        let returnQuantity = 0;
        if (rowData.return_quantity) { 
          returnQuantity = rowData.return_quantity; 
        }
        return releaseQuantity - returnQuantity;
      },
      setQuantity(newData, value, currentRowData) {
        let returnQuantity = value;
        if (!returnQuantity) { returnQuantity = 0; }

        if (returnQuantity > currentRowData.release_quantity) {
          returnQuantity = currentRowData.release_quantity;
        }
        newData.non_invoice = returnQuantity;
        newData.return_quantity = returnQuantity;
        if (currentRowData.unit_price) {
          newData.supply_price = returnQuantity * currentRowData.unit_price;
        } else {
          newData.supply_price = 0;
        }
      },
      setUnitPrice(newData, value, currentRowData) {
        let unitPrice = value;
        if (!unitPrice) { unitPrice = 0; }
        newData.unit_price = unitPrice;
        if (currentRowData.return_quantity) {
          newData.supply_price = unitPrice * currentRowData.return_quantity;
        } else {
          newData.supply_price = 0;
        }
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
        return baseCodeLoader(['반품구분', '부가세구분']
        ).then(response => {
          vars.dataSource.return_type = response['반품구분'];
          vars.dataSource.vat_type = response['부가세구분'];
        }).then(() => (vars.init.value = true));
      },
      loadReleaseItem() {
        vars.dataSource.releaseItem = getShipmentReleaseItem([
          {
            name: 'release',
            op: 'has',
            val: {
              name: 'client_company',
              op: 'eq',
              val: vars.filter.releaseItem.clientCompany,
            },
          },
        ]);
      },
      checkPossibleSave() {
        if (vars.formData.client_company && vars.formData.return_department) {
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
      getFirstReturnType() {
        return methods.getFirstItemName(vars.dataSource.return_type);
      },
      getFirstVatType() {
        return methods.getFirstItemName(vars.dataSource.vat_type);
      },
      getFirstItemName(itemList) {
        if (!itemList || itemList.length <= 0) { return ''; }
        else return itemList[0].code_name;
      },
      redirect(id) {
        if (id) router.replace({ path: `/shipment/release-return/${id}` });
        else router.replace({ path: `/shipment/release-return` });
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
      calculateCustomSummary(options) {
        if (options.name === 'supply_price') {
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          } else if (options.summaryProcess === 'calculate') {
            options.totalValue += options.value.return_quantity * options.value.unit_price;
          } else if (options.summaryProcess === 'finalize') {
            const response = calcPriceSummary(vars.formData.vat_type, options.totalValue);
            vars.formData.supply_price = response.supply_price;
            vars.formData.vat = response.vat;
            vars.formData.total_price = response.total_price;
          }
        }
      },
      async printDocument(){
        if (!vars.formData.id) return;

        const params = {};
        params.client_company = vars.formData.client_company;
      const {data : clientResponse } = await baseClient.load({filter: ['name', '=', params.client_company]}) 

      if(clientResponse.length){
        params.caps = clientResponse[0].alias.includes('캡스');
      }else{
        params.caps = params.client_company.includes('캡스');
      }

        params.supply_price = numeral(-vars.formData.supply_price).format('0,0');
        params.vat = numeral(-vars.formData.vat).format('0,0');
        params.total_price = numeral(-vars.formData.total_price).format('0,0');

        params.etc = vars.formData.etc;
        params.return_number = vars.formData.return_number;
        params.return_date = moment(vars.formData.return_date).format(
          'YYYY년 M월 D일 dddd'
        );
        params.return_manager = vars.formData.return_manager;

        const { data : item1 } = await vars.dataSource.item1.load();

        const items = item1.map((item, idx) => {
          item.index = idx + 1;
          item.unit_price = numeral(item.unit_price).format('0,0');
          item.supply_price = numeral(-item.supply_price).format('0,0');
          return item;
        });
        params.pages = chunk(items, 12);
        params.title = '반 품 거 래 명 세 서';
        const path = 'release-return';
        
        await printDocument(path, params);
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
      shipmentReleaseItem,
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
