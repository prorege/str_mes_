<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">출고</div>
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
              <dx-simple-item data-field="release_number"
                :editor-options="{
                  placeholder: '(자동 or 직접입력)',
                  ...generateItemButtonOption('search', methods.createFindPopupFn('release', '출고조회')),
                }"
              >
                <dx-label text="출고번호" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="release_date" editor-type="dxDateBox"
                :editor-options="{ dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss', ...vars.formState }"
              >
                <dx-label text="출고일자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="client_company"
                :editor-options="{
                  onEnterKey: methods.createFindPopupFn('client', '고객조회', { name: vars.formData.client_company}),
                  ...generateItemButtonOption('search', methods.createFindPopupFn('client', '고객조회', { name: vars.formData.client_company })),
                  ...vars.formState,
                }"
              >
                <dx-label text="고객업체" :show-colon="false" />
                <dx-required-rule message="고객업체를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="client_manager" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.client_manager,
                  displayExpr: methods.clientManagerExpr,
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
              <dx-simple-item data-field="release_department" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.department,
                  displayExpr: 'department_name',
                  valueExpr: 'department_name',
                  acceptCustomValue: true,
                  onValueChanged: methods.onDepartmentChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="출고부서" :show-colon="false" />
                <dx-required-rule message="출고부서를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="release_manager" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.employee,
                  displayExpr: 'emp_name',
                  valueExpr: 'emp_name',
                  disabled: vars.disabled.manager,
                  ...vars.formState,
                }"
              >
                <dx-label text="출고담당자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="release_type" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.release_type,
                  displayExpr: 'code_name',
                  valueExpr: 'code_name',
                  ...vars.formState,
                }"
              >
                <dx-label text="출고구분" :show-colon="false" />
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
              <dx-simple-item data-field="payment_terms" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.payment_terms,
                  displayExpr: 'code_name',
                  valueExpr: 'code_name',
                  acceptCustomValue: true,
                  ...vars.formState,
                }"
              >
                <dx-label text="결재조건" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="delivery_date" editor-type="dxDateBox"
                :editor-options="{ dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss', ...vars.formState }"
              >
                <dx-label text="납품기한" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="client_order_number" :editor-options="{ ...vars.formState }">
                <dx-label text="고객발주번호" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="project_management.project_number"
                :editor-options="{
                  ...generateItemButtonOption('search', methods.createFindPopupFn('project', '프로젝트조회')),
                  ...vars.formState,
                }"
              >
                <dx-label text="프로젝트번호" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="end_user"
                :editor-options="{
                  ...generateItemButtonOption('search', methods.createFindPopupFn('enduser', '고객조회')),
                  ...vars.formState,
                }"
              >
                <dx-label text="EndUser" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="transport" :editor-options="{ ...vars.formState }">
                <dx-label text="운송구분" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="sales_number"
                :editor-options="{
                  readOnly: true,
                  buttons: [
                    {
                      name: 'sales_number',
                      location: 'after',
                      options: {
                        stylingMode: 'text',
                        icon: 'link',
                        disabled: false,
                        onClick: methods.redirectToSales,
                      },
                    },
                  ],
                }"
              >
                <dx-label text="계산서번호" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="confirmed" editor-type="dxCheckBox"
                :editor-options="{ onValueChanged: methods.onConfirmChanged }"
              >
                <dx-label text="출고확정" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="etc" editor-type="dxTextArea"
                :editor-options="{
                  placeholder: '비고',
                  height: '130px',
                  ...generateItemButtonOption('rename', methods.createFindPopupFn('etc', '비고', vars.formData.etc)),
                  ...vars.formState,
                }"
              >
                <dx-label text="비고" :show-colon="false" :visible="false" />
              </dx-simple-item>
            </dx-group-item>
          </dx-group-item>
          <dx-group-item :col-count="5">
            <dx-simple-item data-field="client_manager_phone"
              :calculate-cell-value="methods.getClientManagerPhone"
              :editor-options="{ ...vars.formState }"
            >
              <dx-label text="담당연락처" :show-colon="false" />
            </dx-simple-item>
            <dx-simple-item data-field="delivery_place"
              :col-span="4"
              :editor-options="{ ...vars.formState }"
            >
              <dx-label text="납품장소" :show-colon="false" />
            </dx-simple-item>
          </dx-group-item>
        </dx-form>
      </div>

      <div class="dx-card responsive-paddings mt-1">
        <div class="mt-2">
          <dx-data-grid
            class="fixed-header-table"
            height="calc(100vh - 466px)"
            date-serialization-format="yyyy-MM-ddTHH:mm:ss"
            column-resizing-mode="widget"
            :show-borders="true"
            :remote-operations="false"
            :column-auto-width="true"
            :focused-row-enabled="true"
            :allow-column-resizing="true"
            :row-alternation-enabled="true"
            :allow-column-reordering="true"
            :select-text-on-edit-start="true"
            :data-source="vars.dataSource.item1"
            :on-initialized="(evt) => methods.onGridInitialized(evt, 'item1')"
            @saving="methods.onSavingItem"
            @cell-dbl-click="methods.itemPopupClick"
            @data-error-occurred="methods.onDataError"
          >
            <dx-grid-toolbar>
              <dx-item template="exportToSales" location="before" :visible="vars.formData.confirmed" />
              <dx-item template="importFromOrder" location="before" :visible="!vars.formState.readOnly" />
              <dx-grid-item name="addRowButton" :options="{ onClick: methods.showAddItemPopup }" />
              <dx-grid-item name="saveButton" :visible="!!vars.formData.id" />
              <dx-grid-item name="revertButton" />
              <dx-grid-item name="columnChooserButton" />
            </dx-grid-toolbar>
            <template #exportToSales>
              <dx-button text="계산서로 보내기" icon="export" @click="methods.exportToSales" />
            </template>
            <template #importFromOrder>
              <dx-button text="수주품목찾기" icon="download" @click="methods.showAddPopup" />
            </template>

            <dx-column caption="품목코드" data-field="item_code" width="180" :allow-editing="false" />
            <dx-column caption="품명" data-field="item.item_name" :allow-editing="false" />
            <dx-column caption="규격" data-field="item.item_standard" :allow-editing="false" />
            <dx-column caption="수주수량" data-field="order_item.order_quantity" data-type="number" format="fixedPoint" :allow-editing="false" />
            <dx-column caption="출고수량" data-field="release_quantity" data-type="number" format="fixedPoint" :set-cell-value="methods.setQuantity" />
            <dx-column caption="미출고수량" data-field="order_item.not_shipped" data-type="number" format="fixedPoint" :allow-editing="false" />
            <dx-column caption="단가" data-field="unit_price" data-type="number" format="currency" :set-cell-value="methods.setUnitPrice" />
            <dx-column caption="단위" data-field="item.unit" :allow-editing="false" />
            <dx-column caption="공급가" data-type="number" format="currency" :allow-editing="false" :calculate-display-value="methods.calcSupplyPrice" />
            <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
            <dx-column caption="미계산서" data-field="non_invoice" data-type="number" format="fixedPoint" :allow-editing="false" />
            <dx-column caption="출고창고" data-field="warehouse.wh_name" :set-cell-value="methods.setWarehouse">
              <dx-lookup value-expr="wh_name" display-expr="wh_name" :data-source="vars.dataSource.warehouse" />
            </dx-column>
            <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :allow-editing="false" />
            <dx-column caption="수주번호" data-field="order_number" :allow-editing="false" />
            <dx-column caption="출고 LOT번호" data-field="lot_number" />
            <dx-column caption="고객사품번" data-field="client_item_number" />
            <dx-column caption="품목설명" data-field="item.item_detail" :allow-editing="false" />
            <dx-column caption="참고사항" data-field="note" />
            <dx-column caption="프로젝트번호" data-field="project_management.project_number" />
            <dx-column caption="출고아이디" data-field="fk_release_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
            <dx-column caption="수주 품목 아이디" data-field="fk_order_item_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
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
      title="품목찾기"  
      content-template="popup-item-content"
      v-model:visible="vars.dlg.addBaseItem.show"
      width="70%"
      :height="500"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="(evt) => methods.onGridInitialized(evt, 'find-item-popup')"
    >
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ text: '선택된 항목 추가', icon: 'add', onClick: methods.addSelectedBaseItemRows }"
      />

      <template #popup-item-content>
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
          <dx-column caption="단위" data-field="unit" />
          <dx-column caption="자산구분" data-field="asset_type" />
          <dx-column caption="대분류" data-field="main_category" />
          <dx-column caption="중분류" data-field="middle_category" />
          <dx-column caption="소분류" data-field="sub_category" />

          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick" />
        </dx-data-grid>
      </template>
    </dx-popup>

    <dx-popup
      title="수주품목찾기"  
      content-template="popup-content"
      v-model:visible="vars.dlg.addItem.show"
      width="70%"
      :height="460"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="(evt) => methods.onGridInitialized(evt, 'find-release-popup')"
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
          :data-source="vars.dataSource.orderItem"
          :on-initialized="(evt) => methods.onGridInitialized(evt, 'orderItem')"
        >
          <dx-column caption="고객업체" data-field="order.client_company" />
          <dx-column caption="수주번호" data-field="order.order_number" :sort-index="1" sort-order="desc" />
          <dx-column caption="수주일자" data-field="order.order_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="수주수량" data-field="order_quantity" />
          <dx-column caption="할당수량" data-field="assign_quantity" />
          <dx-column caption="미출고수량" data-field="not_shipped" />

          <dx-paging :page-size="20" />
          <dx-sorting mode="multiple" />
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
      @initialized="(evt) => methods.onGridInitialized(evt, 'multiuse-popup')"
    >
      <template #popup-content>
        <data-grid-client v-if="vars.dlg.finder.key === 'client'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-client v-else-if="vars.dlg.finder.key === 'enduser'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-release v-else-if="vars.dlg.finder.key === 'release'" @change="methods.finderReturnHandler" />
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
import { DxDataGrid, DxColumn, DxLookup, DxPaging, DxEditing, DxSorting, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, 
  DxItem as DxGridItem, DxToolbar as DxGridToolbar, DxButton as DxGridButton } from 'devextreme-vue/data-grid';

import { getStock } from '../../data-source/setup';
import { baseItem, baseClient, baseCodeLoader, getBaseItem } from '../../data-source/base';
import { shipmentRelease, shipmentOrderItem, getShipmentOrderItem, getShipmentReleaseItem, shipmentSalesStatement } from '../../data-source/shipment';

import PopupItemDetail from '@/components/base/popup-item-detail';
import DataGridClient from '@/components/base/data-client.vue';
import DataGridProject from '../../components/project/data-project.vue';
import DataGridRelease from '../../components/shipment/data-release.vue';

import authService from '../../auth';
import stateStore from '@/utils/state-store';
import ApiService from '../../utils/api-service';
import printDocument from '@/utils/print-document';
import { notifyInfo, notifyError } from '../../utils/notify';
import { loadEmployee, loadWarehouse, loadDepartment, loadClientManager } from '../../utils/data-loader';
import { calcPriceSummary, currentDateTime, beforeExitConfirm, generateItemButtonOption } from '../../utils/util';

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
    PopupItemDetail, DataGridClient, DataGridRelease, DataGridProject,
  },
  props: {
    id: [String, Number],
  },
  setup(props) {
    moment.locale('ko')

    // variable 설정
    const router = useRouter();
    const apiExportToSales = new ApiService('/api/mes/v1/shipment/release/export/sales');
    const vars = {};
    vars.init = ref(false);
    vars.loading = ref(false);
    vars.formState = reactive({ readOnly: true });
    vars.grid = {};
    vars.grid.orderItem = null;
    vars.grid.item1 = null;
    vars.grid.baseItem = null;
    vars.dlg = {};
    vars.dlg.addItem = reactive({ show: false });
    vars.dlg.addBaseItem = reactive({ show: false });
    vars.dlg.finder = reactive({ show: false, title: '', key: null, data: null });
    
    vars.filter = {};
    vars.filter.orderItem = { clientCompany: null };
    vars.filter.item1 = [{ name: 'fk_release_id', op: 'eq', val: props.id || 0 }];
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
      payment_terms: [],
      release_type: [],
      vat_type: [],
      delivery_place: [],
      warehouse: [],
      client_manager: [],
      department: [],
      employee: [],
      orderItem: null,
      baseItem: getBaseItem(null, null, null),
      item1: getShipmentReleaseItem(vars.filter.item1),
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
      beforeExitConfirm.check(() => !vars.disabled.save);
    });

    // public methods
    const methods = {
      async initById(id) {
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

        let { data } = await shipmentRelease.byKey(id);
        Object.assign(vars.formData, data);

        methods.enableDelete();
        vars.disabled.edit = false;
        if (vars.formData.client_company && vars.formData.release_department) {
          methods.enableSave();
          vars.disabled.items = false;
        }
        methods.onClientChanged();
      },
      clearFormData() {
        vars.formData.id = null;
        vars.formData.created = null;
        vars.formData.release_number = '';
        vars.formData.release_date = '';
        vars.formData.client_company = '';
        vars.formData.client_manager = '';
        vars.formData.client_manager_phone = '';
        vars.formData.release_department = '';
        vars.formData.release_manager = '';
        vars.formData.release_type = '';
        vars.formData.vat_type = '';
        vars.formData.payment_terms = '';
        vars.formData.delivery_date = '';
        vars.formData.delivery_place = '';
        vars.formData.client_order_number = '';
        vars.formData.end_user = '';
        vars.formData.note = '';
        vars.formData.etc = '';
        vars.formData.supply_price = 0;
        vars.formData.vat = 0;
        vars.formData.total_price = 0;
        vars.formData.confirmed = false;
        vars.formData.sales_number = null;
        vars.formData.fk_project_management_id = null;
        vars.formData.fk_company_id = authService.getCompanyId();
        vars.formData.project_management = null;
      },
      async addSelectedRows() {
        const grid = vars.grid.item1;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }
        
        const rows = await vars.grid.orderItem.getSelectedRowsData();
        for (let row of rows) {
          const basicStock = row.basic_stock ? { ...row.basic_stock } : { current_stock: 0, available_stock: 0 };

          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code; // 품목코드
          data.item = { ...row.item }; // 품목
          data.order_item = { ...row }; // 수주 품목
          data.release_quantity = row.assign_quantity; // 출고수량
          data.unit_price = row.unit_price; // 단가
          data.request_delivery_date = row.request_delivery_date; // 요청납기
          data.non_invoice = row.assign_quantity; // 미계산서
          data.warehouse = { ...row.warehouse }; // 출고창고
          data.warehouse_code = row.warehouse.wh_code; // 창고코드
          data.basic_stock = { ...basicStock }; // 기초재고
          data.order_number = row.order.order_number; // 수주번호
          data.client_item_number = row.client_item_number; // 고객사품번
          data.note = row.note; // 참고사항
          data.closing_yn = false; // 출하검사
          data.fk_project_management_id = row.fk_project_management_id; // 프로젝트번호
          data.fk_release_id = vars.formData.id; // 출고번호
          data.fk_order_item_id = row.id; // 수주품목번호
          data.project_management = row.project_management ? row.project_management : null;
        }
        grid.refresh();
        vars.dlg.addItem.show = false;
      },
      async addSelectedBaseItemRows() {
        const grid = vars.grid.item1;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) await grid.navigateToRow(firstRowKey);

        const rows = await vars.grid.baseItem.getSelectedRowsData();
        for (let row of rows) {
          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code;
          data.item = { item_name: row.item_name, item_standard: row.item_standard, unit: row.unit, item_detail: row.item_detail };
          data.order_item = { order_quantity: 0, not_shipped: 0 };
          data.release_quantity = 0;
          data.unit_price = row.purchase_price || 0;
          data.non_invoice = 0;
          data.closing_yn = false;
          data.fk_release_id = vars.formData.id;
          data.fk_order_item_id = null;
        }
        grid.refresh();
        vars.dlg.addBaseItem.show = false;
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
          if (!item.id) {
            notContains.push(['id', '<>', item.data.fk_order_item_id], 'and');
          }
        }
        notContains.pop()

        if (vars.grid.orderItem) {
          vars.grid.orderItem.filter(notContains);
          vars.grid.orderItem.clearSelection();
          vars.grid.orderItem.refresh();
        }
        vars.dlg.addItem.show = true;
      },
      showAddItemPopup() {
        if (vars.grid.baseItem) {
          vars.grid.baseItem.clearSelection();
          vars.grid.baseItem.clearFilter();
          vars.grid.baseItem.refresh();
        }
        vars.dlg.addBaseItem.show = true;
      },
      async gridItem1Refresh(id) {
        if (!id) {
          id = 0;
        }
        vars.filter.item1[0].val = id;
        vars.dataSource.item1.defaultFilters = vars.filter.item1;
        if (vars.grid.item1) {
          vars.grid.item1.cancelEditData();
          vars.grid.item1.refresh();
        }
      },
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`shipment-release-${key}`, evt.component);
      },
      async newItem() {
        methods.gridItem1Refresh();
        if (vars.formData.id) {
          methods.clearFormData();
          methods.redirect();
        }
        setTimeout(() => {
          methods.clearFormData();
          vars.formData.release_date = currentDateTime();
          vars.formData.release_department = authService.getDepartmentName();
          vars.formData.release_manager = authService.getUserName();
          vars.formData.release_type = methods.getFirstReleaseType();
          vars.formData.vat_type = methods.getFirstVatType();
          vars.formData.payment_terms = methods.getFirstPaymentTerms();
          vars.formData.delivery_place = methods.getFirstDeliveryPlace();
          vars.formData.confirmed = false;
          vars.formData.fk_company_id = authService.getCompanyId();
          vars.formState.readOnly = false;
        }, 200);
      },
      async editItem() {
        if (!vars.formData.id) { return; }
        if (vars.formState.readOnly && vars.formData.confirmed) {
          return;
        }
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
            await shipmentRelease.remove(vars.formData.id);
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
            delete updateDate.release_number;
            const { data } = await shipmentRelease.update(
              vars.formData.id,
              updateDate
            );
            vars.formData.release_number = data.release_number;
            if (vars.grid.item1) await vars.grid.item1.saveEditData();

            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');

            methods.enableSave();
            methods.enableDelete();
          } else {
            // 채번이 없을 경우 자동 채번
            if (vars.formData.created) {
              vars.formData.created = null;
            }
            let { data } = await shipmentRelease.insert(vars.formData);
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
            notifyError('이미 존재하는 출고번호 입니다');
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
          case 'release': {
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
            vars.formData.fk_project_management_id = data.id;
            vars.formData.project_management = data;
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

        vars.filter.orderItem.clientCompany = client ? client.name : null;
        methods.loadOrderItem();

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
          if (
            vars.formData.client_company &&
            vars.formData.release_department
          ) {
            vars.disabled.edit = false;
            methods.enableSave();
            methods.enableDelete();
          }
        }
        await shipmentRelease.update(vars.formData.id, param);
      },
      updateEtcValue(v) {
        vars.dlg.finder.data = v;
      },
      onDepartmentChanged(e) {
        if (!e.value) {
          vars.disabled.save = true;
          vars.disabled.items = true;
          vars.disabled.manager = true;
          vars.formData.release_manager = null;
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
        e.changes.forEach((element) => {
          if (element.type != 'remove') {
            element.data.fk_release_id = vars.formData.id;
            delete element.data.item;
            delete element.data.warehouse;
            delete element.data.basic_stock;
            delete element.data.order_item;
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
        shipmentRelease.update(vars.formData.id, priceData);
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
      numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      },
      setQuantity(newData, value, currentRowData) {
        if (currentRowData.id) {
          const rows = vars.grid.item1.getVisibleRows();
          for (const row of rows) {
            if (row.data.id == currentRowData.id) {
              if (row.oldData) {
                const limitQuantity = row.oldData.release_quantity + currentRowData.order_item.not_shipped;
                if (value > limitQuantity) {
                  alert(`설정 가능한 최대 출고 수량은 ${methods.numberWithCommas(limitQuantity)}입니다`, '출고수량')
                  return;
                }
              } else {
                const limitQuantity = currentRowData.release_quantity + currentRowData.order_item.not_shipped;
                if (value > limitQuantity) {
                  alert(`설정 가능한 최대 출고 수량은 ${methods.numberWithCommas(limitQuantity)}입니다`, '출고수량')
                  return;
                }
              }
              break;
            }
          }
        } else {
          const limitQuantity = currentRowData.order_item.not_shipped;
          if (value > limitQuantity) {
            alert(`설정 가능한 최대 출고 수량은 ${methods.numberWithCommas(limitQuantity)}입니다`, '출고수량')
            return;
          }
        }
        newData.release_quantity = value;
        newData.non_invoice = currentRowData.non_invoice + (value - currentRowData.release_quantity);
        newData.unit_price = currentRowData.unit_price;
      },
      setUnitPrice(newData, value, currentRowData) {
        newData.release_quantity = currentRowData.release_quantity;
        newData.non_invoice = currentRowData.non_invoice;
        newData.unit_price = value;
      },
      calcSupplyPrice(rowData) {
        if (rowData.release_quantity && rowData.unit_price) {
          return rowData.release_quantity * rowData.unit_price;
        }
        return 0;
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
        return baseCodeLoader([
          '부가세구분',
          '출고구분',
          '결재조건',
          '납품장소',
        ])
          .then((response) => {
            vars.dataSource.payment_terms = response['결재조건'];
            vars.dataSource.release_type = response['출고구분'];
            vars.dataSource.vat_type = response['부가세구분'];
            vars.dataSource.delivery_place = response['납품장소'];
          })
          .then(() => (vars.init.value = true));
      },
      loadOrderItem() {
        vars.dataSource.orderItem = getShipmentOrderItem([
          {
            name: 'order',
            op: 'has',
            val: {
              name: 'client_company',
              op: 'eq',
              val: vars.filter.orderItem.clientCompany,
            },
          },
          { name: 'not_shipped', op: 'gt', val: 0 },
          { name: 'closing_yn', op: 'eq', val: 0 },
        ]);
      },
      checkPossibleSave() {
        if (vars.formData.client_company && vars.formData.release_department) {
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
      getFirstReleaseType() {
        return methods.getFirstItemName(vars.dataSource.release_type);
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
        if (!itemList || itemList.length <= 0) {
          return '';
        } else return itemList[0].code_name;
      },
      redirect(id) {
        if (id) router.replace({ path: `/shipment/release/${id}` });
        else router.replace({ path: `/shipment/release` });
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
      async exportToSales() {
        if (!vars.formData.id) {
          return;
        }

        const params = { release_id: vars.formData.id };
        try {
          await apiExportToSales.post('', params);
          await alert('계산서로 보내기가 완료되었습니다', '계산서로 보내기');

          let { data } = await shipmentRelease.byKey(vars.formData.id);
          Object.assign(vars.formData, data);

          methods.gridItem1Refresh(vars.formData.id);
        } catch (ex) {
          if (ex.response.status == 608) {
            await alert('미계산서 수량이 없습니다', '계산서로 보내기');
          } else {
            await alert('계산서로 보내기가 실패했습니다', '계산서로 보내기');
          }
        }
      },
      async redirectToSales() {
        if (!vars.formData.sales_number) {
          await alert('계산서번호가 존재하지 않습니다', '계산서로 이동');
          return;
        }
        const response = await shipmentSalesStatement.load({
          filter: [
            ['sales_number', '=', vars.formData.sales_number],
            ['fk_company_id', '=', authService.getCompanyId()],
          ],
        });
        if (response.data.length > 0) {
          router.replace({
            path: `/shipment/sales-statement/${response.data[0].id}`,
          });
        } else {
          await alert('계산서번호가 존재하지 않습니다', '계산서로 이동');
        }
      },
      calculateCustomSummary(options) {
        if (options.name === 'supply_price') {
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          } else if (options.summaryProcess === 'calculate') {
            options.totalValue += options.value.release_quantity * options.value.unit_price;
          } else if (options.summaryProcess === 'finalize') {
            const response = vars.formData.client_company == '에스케이쉴더스 주식회사' ? methods.individuallyCalcPriceSummary(vars.formData.vat_type, options.totalValue) : calcPriceSummary(vars.formData.vat_type, options.totalValue);
            vars.formData.supply_price = response.supply_price;
            vars.formData.vat = response.vat;
            vars.formData.total_price = response.total_price;
          }
        }
      },
      individuallyCalcPriceSummary(vat_type, total){
        let supply_price = 0;
        let vat = 0;
        let total_price = 0;

        switch (vat_type) {
          case '별도': {
            supply_price = total;
            vat = Math.round(total * 0.1);
            total_price = total + vat;
            break;
          }
          case '포함': {
            total_price = total;
            supply_price = Math.round((total * 10) / 11);
            vat = total_price - supply_price;
            break;
          }
          case '영세': {
            total_price = total;
            vat = 0;
            supply_price = total;
            break;
          }
          default: {
            total_price = total;
            vat = 0;
            supply_price = total;
          }
        }
        return { supply_price, vat, total_price };
      },
      clientManagerExpr(item) {
        if (!item) return '';
        if (item.mobile) {
          vars.formData.client_manager_phone = item.mobile;
        }
        return item.name;
      },
      async printDocument() {
        if (!vars.formData.id) return;

        // console.log(vars.formData)
        const params = {};
        params.client_company = vars.formData.client_company;

        const {data: clientResponse} = await baseClient.load({filter: ['name', '=', params.client_company]})

        if (clientResponse.length) params.caps = clientResponse[0].alias.includes('캡스');
        else params.caps = params.client_company.includes('캡스');

        params.manager = {
          emp_ext_phone: '',
          emp_name: '',
          emp_position: '',
          emp_mobile: '',
          emp_email: '',
        };
        params.supply_price = numeral(vars.formData.supply_price).format('0,0');
        params.vat = numeral(vars.formData.vat).format('0,0');
        params.total_price = numeral(vars.formData.total_price).format('0,0');

        params.vat_type = 0;
        params.etc = vars.formData.etc;
        params.release_number = vars.formData.release_number;
        params.release_date = moment(vars.formData.release_date).format(
          'YYYY년 M월 D일 dddd'
        );
        params.release_manager = vars.formData.release_manager;

        const { data: item1 } = await vars.dataSource.item1.load();

        const items = item1.map((item, idx) => {
          item.index = idx + 1
          item.supply_price = 0
          if (item.release_quantity && item.unit_price) {
            item.supply_price = item.release_quantity * item.unit_price;
          }

          item.unit_price = numeral(item.unit_price).format('0,0');
          item.supply_price = numeral(item.supply_price).format('0,0');
          return item;
        });

        params.pages = chunk(items, 12)
        params.title = vars.formData.release_type === 'SAMPLE출고'
          ? '샘 플 출 고 명 세 서'
          : '거 래 명 세 서'
        const path = vars.formData.release_type ==='인수증' ? 'release-certificate' : 'release'
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
      shipmentOrderItem,
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