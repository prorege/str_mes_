<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">작업지시</div>
            </dx-item>
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{text: '신규', type: 'add', icon: 'add', disabled: vars.disabled.new, onClick: methods.newItem}"
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
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{ text: '출력', type: 'print', icon: 'print', onClick: methods.printDocument }"
            />
          </dx-toolbar>
        </div>
        <dx-form :form-data="vars.formData">
          <dx-group-item :col-count="4">
            <dx-group-item>
              <dx-simple-item
                data-field="number"
                :editor-options="{
                  placeholder: '(자동 or 직접입력)',
                  ...generateItemButtonOption('search', methods.createFindPopupFn('work-order', '작업지시조회')),
                }"
              >
                <dx-label text="작업지시번호" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="target_date"
                editor-type="dxDateBox"
                :editor-options="{dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss', ...vars.formState}"
              >
                <dx-label text="작업지시일자" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item
                data-field="department"
                editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'department_name',
                  displayExpr: 'department_name',
                  acceptCustomValue: true,
                  dataSource: vars.dataSource.department,
                  onValueChanged: methods.onDepartmentChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="담당부서" :show-colon="false" />
                <dx-required-rule message="담당부서를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item
                data-field="manager"
                editor-type="dxSelectBox"
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
              <dx-simple-item data-field="note" :editor-options="{ ...vars.formState }">
                <dx-label text="참고사항" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="stock_move_request_number"
                :editor-options="{
                  readOnly: true,
                  buttons: [
                    {
                      name: 'move_request_number',
                      location: 'after',
                      options: {stylingMode: 'text', icon: 'link', disabled: false, onClick: methods.redirectStockMoveRequest},
                    },
                  ],
                }"
              >
                <dx-label text="이동요청번호" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item
                data-field="etc"
                editor-type="dxTextArea"
                :editor-options="{
                  ...generateItemButtonOption('rename', methods.createFindPopupFn('etc', '비고', vars.formData.etc)),
                  height: '80px',
                  labelMode: 'hidden',
                  placeholder: '비고',
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
        <dx-tab-panel
          v-model:selected-index="vars.tab.index"
          :swipe-enabled="false"
          :animation-enabled="false"
        >
          <dx-item title="작업지시">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 416px)"
                  date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                  column-resizing-mode="widget"
                  :show-borders="true"
                  :remote-operations="true"
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
                    <dx-item template="addFromPlan" location="before" :visible="!vars.formData.closing_yn && !vars.formState.readOnly" />
                    <dx-item template="addItem" name="addRowButton" :visible="!vars.formData.closing_yn && !vars.formState.readOnly" />
                    <dx-item name="saveButton" :visible="!!vars.formData.id" />
                    <dx-item name="revertButton" />
                    <dx-item name="columnChooserButton" />
                  </dx-grid-toolbar>
                  <template #addFromPlan>
                    <dx-button icon="add" text="생산계획에서 가져오기" @click="methods.showPlanItem" />
                  </template>
                  <template #addItem>
                    <dx-button icon="add" @click="methods.showBaseItem" />
                  </template>

                  <dx-column caption="품목코드" data-field="item_code" width="180" :allow-editing="false" />
                  <dx-column caption="품명" data-field="item.item_name" :allow-editing="false" />
                  <dx-column caption="규격" data-field="item.item_standard" :allow-editing="false" />
                  <dx-column caption="작업지시수량" data-field="required_quantity" data-type="number" format="fixedPoint" :allow-editing="!vars.formData.closing_yn" :set-cell-value="methods.setQuantity" />
                  <dx-column caption="BOM여부" data-field="item.bom_yn" data-type="boolean" :allow-editing="false" />
                  <dx-column caption="단위" data-field="item.unit" :allow-editing="false" />
                  <dx-column caption="생산계획번호" data-field="production_plan_number" :allow-editing="false" />
                  <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" :allow-editing="!vars.formData.closing_yn" />
                  <dx-column caption="미생산수량" data-field="unproduced_quantity" data-type="number" format="fixedPoint" :allow-editing="false" />
                  <dx-column caption="가용재고"  data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :allow-editing="false" />
                  <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :allow-editing="false" />
                  <dx-column  caption="입고창고" data-field="warehouse.wh_name" :allow-editing="!vars.formData.closing_yn" :set-cell-value="methods.setWarehouse">
                    <dx-lookup  value-expr="wh_name" display-expr="wh_name" :data-source="vars.dataSource.warehouse" />
                  </dx-column>
                  <dx-column caption="수주번호" data-field="order_number" :allow-editing="false" />
                  <dx-column caption="고객업체" data-field="client_company" :allow-editing="!vars.formData.closing_yn" :editor-options="{...generateItemButtonOption('search', methods.createFindPopupFn('client', '고객업체조회'))}" />
                  <dx-column caption="고객사품번" data-field="client_item_number" :allow-editing="false" />
                  <dx-column caption="실수요자" data-field="end_user" :allow-editing="false" />
                  <dx-column caption="프로젝트번호" data-field="project_management.project_number" :allow-editing="!vars.formData.closing_yn" :editor-options="{...generateItemButtonOption('search', methods.createFindPopupFn('project', '프로젝트조회'))}"
                  :set-cell-value="methods.setProjectManagement" />
                  <dx-column caption="종료" data-field="end_yn" data-type="boolean" />
                  <dx-column caption="입고창고" data-field="warehouse_code" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
                  <dx-column caption="작업지시 아이디" data-field="fk_work_order_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
                  <dx-column caption="생산계획품목 아이디" data-field="fk_plan_item_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />

                  <dx-scrolling mode="standard" />
                  <dx-column-chooser mode="select" :enabled="true" />
                  <dx-editing mode="batch"
                    :allow-adding="!vars.formData.closing_yn && !vars.formState.readOnly"
                    :allow-updating="!vars.formState.readOnly"
                    :allow-deleting="!vars.formData.closing_yn && !vars.formState.readOnly"
                  />
                </dx-data-grid>
              </div>
            </template>
          </dx-item>

          <dx-item title="필요자재">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 416px)"
                  date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                  column-resizing-mode="widget"
                  :show-borders="true"
                  :column-auto-width="true"
                  :remote-operations="true"
                  :allow-column-resizing="true"
                  :allow-column-reordering="true"
                  :select-text-on-edit-start="true"
                  :disabled="vars.disabled.items"
                  :data-source="vars.dataSource.item2"
                  :on-initialized="evt => methods.onGridInitialized(evt, 'item2')"
                  @init-new-row="methods.onItem2Insert"
                  @cell-dbl-click="methods.itemPopupClick"
                  @saving="methods.onSavingItem"
                >
                  <dx-grid-toolbar>
                    <dx-item template="calculate" location="before" :visible="!vars.formData.closing_yn" />
                    <dx-item template="exportOrder" location="before" :visible="!vars.formData.closing_yn" />
                    <dx-item name="saveButton" />
                    <dx-item name="revertButton" />
                    <dx-item name="columnChooserButton" />
                  </dx-grid-toolbar>
                  <template #calculate>
                    <dx-button text="실행계획 품목 가져오기" icon="formula" @click="methods.calculateItem" />
                  </template>
                  <template #exportOrder>
                    <dx-button text="필요자재 출고요청" icon="export" @click="methods.requestExport" />
                  </template>

                  <dx-column caption="투입품목코드" data-field="item_code" width="180" :allow-editing="false" />
                  <dx-column caption="품명" data-field="item.item_name" :allow-editing="false" />
                  <dx-column caption="규격" data-field="item.item_standard" :allow-editing="false" />
                  <dx-column caption="주공급업체" data-field="client_company" :allow-editing="false" />
                  <dx-column caption="필요수량" data-field="required_quantity" data-type="number" format="fixedPoint" :allow-editing="false" />
                  <dx-column caption="출고요청수량" data-field="delivery_request_quantity" data-type="number" format="fixedPoint" />
                  <dx-column caption="자산구분" data-field="item.asset_type" :allow-editing="false" >
                    <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.dataSource.asset_type" />
                  </dx-column>
                  <dx-column caption="단위" data-field="item.unit" :allow-editing="false" />
                  <dx-column caption="출고창고" data-field="warehouse.wh_name" :set-cell-value="methods.setWarehouse">
                    <dx-lookup value-expr="wh_name" display-expr="wh_name" :data-source="vars.dataSource.warehouse" />
                  </dx-column>
                  <dx-column caption="입고창고" data-field="in_warehouse.wh_name" :set-cell-value="methods.setWarehouse2">
                    <dx-lookup value-expr="wh_name" display-expr="wh_name" :data-source="vars.dataSource.warehouse" />
                  </dx-column>
                  <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
                  <dx-column caption="미출고수량" data-field="uninput_quantity" data-type="number" format="fixedPoint" :allow-editing="false" />
                  <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :allow-editing="false" />
                  <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :allow-editing="false" />
                  <dx-column caption="출고창고" data-field="warehouse_code" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
                  <dx-column caption="입고창고" data-field="in_warehouse_code" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
                  <dx-column caption="작업지시 아이디" data-field="fk_work_order_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
                  <dx-column caption="생산계획품목 아이디" data-field="fk_plan_item_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />

                  <dx-scrolling mode="standard" />
                  <dx-column-chooser mode="select" :enabled="true" />
                  <dx-editing mode="batch"
                    :allow-adding="!vars.formData.closing_yn"
                    :allow-updating="!vars.formData.closing_yn && !vars.formState.readOnly"
                    :allow-deleting="!vars.formData.closing_yn"
                  />
                </dx-data-grid>
              </div>
            </template>
          </dx-item>
        </dx-tab-panel>
      </div>
    </div>

    <dx-popup
      content-template="popup-content"
      title="생산계획품목찾기"
      v-model:visible="vars.dlg.addplanItem.show"
      width="70%"
      :height="500"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'find-plan-popup')"
    >
      <dx-toolbar-item toolbar="top" location="after"  widget="dxButton"
        :options="{text: '선택된 항목 추가', icon: 'add', onClick: methods.addOrderPlanRows}"
      />

      <template #popup-content>
        <dx-data-grid
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="vars.dataSource.planItem"
          :on-initialized="evt => methods.onGridInitialized(evt, 'planItem')"
        >
          <dx-column caption="생산계획번호" data-field="production_plan.number" :sort-index="0" sort-order="desc" />
          <dx-column caption="고객사" data-field="client_company" />
          <dx-column caption="수주일자" data-field="order_date" data-type="date" format="yyyy-MM-dd" :sort-index="1" sort-order="desc" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="자산구분" data-field="item.asset_type" />
          <dx-column caption="계획수량" data-field="production_plan_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="미작지수량" data-field="unordered_quantity" data-type="number" format="fixedPoint" />
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
      v-model:visible="vars.dlg.addBaseItem.show"
      width="70%"
      :height="500"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'base-item-popup')"
    >

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
          <dx-grid-toolbar>
            <dx-item template="addItemButton" location="after" />
            <dx-grid-item name="addRowButton" location="after" />
          </dx-grid-toolbar>
          <template #addItemButton>
            <dx-button text="선택된 항목 추가" icon="add" @click="methods.addSelectedRows" />
          </template>
          <dx-column caption="품목코드" data-field="item_code">
            <dx-grid-required-rule />
          </dx-column>
          <dx-column caption="품명" data-field="item_name">
            <dx-grid-required-rule />
          </dx-column>
          <dx-column caption="생성일자" data-field="created" ata-type="date" format="yyyy-MM-dd" :visible="false" sort-order="desc" />
          <dx-column caption="규격" data-field="item_standard" />
          <dx-column caption="자산구분" data-field="asset_type">
            <dx-lookup
              :data-source="vars.dataSource.asset_type"
              value-expr="code_name"
              display-expr="code_name" />
          </dx-column>
          <dx-column caption="품목그룹" data-field="item_group">
            <dx-lookup
              :data-source="vars.dataSource.item_group"
              value-expr="code_name"
              display-expr="code_name" />
          </dx-column>
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :calculate-display-value="methods.availableStock" :allow-sorting="false" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :calculate-display-value="methods.currentStock" :allow-sorting="false" />

          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick" />
          <dx-editing mode="row" :use-icons="true" :allow-adding="true" :allow-updating="true" :allow-deleting="true" />
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
      @initialized="evt => methods.onGridInitialized(evt, 'multiuse-popup')"
    >
      <template #popup-content>
        <data-grid-work-order v-if="vars.dlg.finder.key === 'work-order'"
          @change="methods.finderReturnHandler"
        />
        <data-grid-client v-else-if="vars.dlg.finder.key === 'client'"
          @change="methods.finderReturnHandler"
        />
        <data-grid-project v-else-if="vars.dlg.finder.key === 'project'"
          @change="methods.finderReturnHandler"
        />
        <div v-else-if="vars.dlg.finder.key === 'etc'">
          <div class="mb-2">
            <dx-text-area :height="190" :value="vars.dlg.finder.data" @update:value="methods.updateEtcValue" />
          </div>
          <dx-toolbar>
            <dx-item toolbar="top" location="after" widget="dxButton"
              :options="{text: '닫기', icon: null, onClick: methods.finderReturnHandler}"
            />
          </dx-toolbar>
        </div>
      </template>
    </dx-popup>

    <popup-item-detail v-model:visible="vars.itemDetail.visible" :item-id="vars.itemDetail.id" />
  </div>
</template>

<script>
import { onMounted, ref, reactive, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import numeral from 'numeral';
import moment from 'moment';
import { orderBy } from 'lodash';

import { DxButton } from 'devextreme-vue/button';
import DxTextArea from 'devextreme-vue/text-area';
import { DxTabPanel } from 'devextreme-vue/tab-panel';
import { confirm, alert } from 'devextreme/ui/dialog';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxRequiredRule } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxLookup, DxEditing, DxSorting, DxFilterRow, DxScrolling, DxSelection, DxColumnChooser, DxToolbar as DxGridToolbar, DxItem as DxGridItem, DxRequiredRule as DxGridRequiredRule, } from 'devextreme-vue/data-grid';


import { getStock } from '../../data-source/setup';
import { stockMoveRequest } from '../../data-source/stock';
import { baseCodeLoader, getBaseItem, baseDepartment } from '../../data-source/base';
import { produceWorkOrder, getProducePlanItem, getProduceWorkOrderItem1, getProduceWorkOrderItem2 } from '../../data-source/produce';

import DataGridClient from '../../components/base/data-client.vue';
import DataGridProject from '../../components/project/data-project.vue';
import DataGridWorkOrder from '../../components/produce/data-work-order.vue';
import DataGridOrderPlan from '../../components/purchase/data-order-plan.vue';
import PopupItemDetail from '@/components/base/popup-item-detail';

import authService from '../../auth';
import stateStore from '@/utils/state-store';
import ApiService from '../../utils/api-service';
import { generateItemButtonOption, beforeExitConfirm, currentDateTime } from '../../utils/util';
import { notifyInfo, notifyError } from '../../utils/notify';
import { loadEmployee, loadWarehouse, loadDepartment } from '../../utils/data-loader';
import printDocument from '@/utils/print-document'

export default {
  components: {
    DxButton,
    DxTextArea,
    DxTabPanel,
    DxLoadPanel,
    DxToolbar, DxItem,
    DxPopup, DxToolbarItem, DxGridItem, DxGridRequiredRule,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxRequiredRule,
    DxDataGrid, DxColumn, DxPaging, DxLookup, DxEditing, DxSorting, DxFilterRow, DxScrolling, DxSelection, DxColumnChooser, DxGridToolbar,
    PopupItemDetail, DataGridClient, DataGridProject, DataGridOrderPlan, DataGridWorkOrder,
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
    vars.tab = reactive({
      index: 0,
    });
    vars.formState = reactive({ readOnly: true });
    vars.grid = {
      item1: null,
      item2: null,
      baseItem: null,
      planItem: null,
    };
    vars.dlg.addBaseItem = reactive({ show: false });
    vars.dlg.addplanItem = reactive({ show: false });
    vars.dlg.finder = reactive({
      show: false,
      title: '',
      key: null,
      data: null,
    });
    vars.warehouse = {};
    vars.filter = reactive({
      item1: [{ name: 'fk_work_order_id', op: 'eq', val: props.id || 0 }],
      item2: [{ name: 'fk_work_order_id', op: 'eq', val: props.id || 0 }],
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
      payment_terms: [],
      order_type: [],
      vat_type: [],
      delivery_place: [],
      client_company: [],
      client_manager: [],
      department: [],
      employee: [],
      warehouse: [],
      item_group: [],
      asset_type: [],
      baseItem: null,
      planItem: null,
      item1: getProduceWorkOrderItem1(vars.filter.item1),
      item2: getProduceWorkOrderItem2(vars.filter.item2),
    });
    vars.dataSource.item2.transform = (list) => {
      list.forEach(v => {
        if (!v.basic_stock) v.basic_stock = {
          available_stock: 0,
          current_stock: 0
        }
      })
    }
    vars.focus = reactive({
      item1: null,
      item2: null,
    });
    vars.formData = reactive({});

    vars.itemDetail = reactive({ visible: false, id: 0 });

    onMounted(async () => {
      await loadDepartment(vars.dataSource);
      await methods.loadBaseCode();
      methods.initById(props.id);
      loadWarehouse(vars.dataSource);
      beforeExitConfirm.check(() => !vars.disabled.save)
    });

    // public methods
    const methods = {
      async initById(id) {
        await methods.gridItem1Refresh(id);
        await methods.gridItem2Refresh(id);
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

        let { data } = await produceWorkOrder.byKey(id);
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
        vars.formData.closing_yn = false;
        vars.formData.stock_move_request_number = null;
        vars.formData.fk_company_id = authService.getCompanyId();
      },
      async addOrderPlanRows() {
        const grid = vars.grid.item1;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        const rows = await vars.grid.planItem.getSelectedRowsData();
        for (let row of rows) {
          const basicStock = row.basic_stock
            ? { ...row.basic_stock }
            : {
                current_stock: 0,
                available_stock: 0,
              };

          // 작업지시
          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code; // 품목코드
          data.item = { ...row.item }; // 품목
          data.required_quantity = row.unordered_quantity; // 작업지시수량
          data.bom_yn = row.item.bom_yn; // BOM여부
          data.production_plan_number = row.production_plan.number; // 생산계획번호
          data.request_delivery_date = row.request_delivery_date; // 요청납기
          data.unproduced_quantity = row.unordered_quantity; // 미생산수량
          data.basic_stock = { ...basicStock }; // 기초재고
          data.warehouse = { ...row.warehouse }; // 입고창고
          data.warehouse_code = row.warehouse.wh_code; // 창고코드
          data.order_number = row.order_number; // 수주번호
          data.client_company = row.client_company; // 고객업체
          data.client_item_number = row.client_item_number; // 고객사품번
          data.end_user = row.end_user; // 실수요자
          data.end_yn = false; // 종료
          data.fk_project_management_id = row.fk_project_management_id; // 프로젝트번호
          data.fk_plan_item_id = row.id; // 생산계획품목 아이디
          data.fk_work_order_id = vars.formData.id; // 작업지시 아이디
          data.project_management = row.project_management ? row.project_management : null;
        }
        vars.dlg.addBaseItem.show = false;
        vars.dlg.addplanItem.show = false;
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
          data.required_quantity = 0; // 작업지시수량
          data.bom_yn = row.bom_yn; // BOM여부
          data.production_plan_number = null; // 생산계획번호
          data.request_delivery_date = null; // 요청납기
          data.unproduced_quantity = 0; // 미생산수량
          data.basic_stock = { ...basicStock }; // 기초재고
          data.warehouse = { ...vars.warehouse }; // 입고창고
          data.warehouse_code = vars.warehouse.wh_code; // 창고코드
          data.order_number = null; // 수주번호
          data.client_company = null; // 고객업체
          data.client_item_number = clientItemNumber; // 고객사품번
          data.end_user = null; // 실수요자
          data.fk_project_management_id = null; // 프로젝트번호
          data.end_yn = false; // 종료
          data.fk_plan_item_id = null; // 생산계획품목 아이디
          data.fk_work_order_id = vars.formData.id; // 작업지시 아이디
        }
        vars.dlg.addBaseItem.show = false;
        vars.dlg.addplanItem.show = false;
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
      showBaseItem() {
        methods.gridClear(vars.grid.baseItem);
        vars.dlg.addBaseItem.show = true;
      },
      showPlanItem() {
        const notContains = [];
        for (const item of vars.grid.item1.getVisibleRows()) {
          if (!item.id && item.data.fk_plan_item_id) {
            notContains.push(['id', '<>', item.data.fk_plan_item_id], 'and');
          }
        }
        notContains.pop()

        if (vars.grid.planItem) {
          vars.grid.planItem.filter(notContains);
          methods.gridClear(vars.grid.planItem);
        }
        vars.dlg.addplanItem.show = true;
      },
      gridClear(grid) {
        if (grid) {
          grid.clearSelection();
          grid.refresh();
        }
      },
      async calculateItem() {
        const rows = vars.grid.item1.getVisibleRows();
        const excutionPlanList = [];
        for (let row of rows) {
          if (!row.data.project_management || !row.data.project_management.fk_excution_plan_id) {
            await alert('실행계획이 연결되지 않은 품목이 있습니다.', '실행계획 확인');
            
          }else{
            excutionPlanList.push(row.data.project_management.fk_excution_plan_id);
          }
        }
        const result = await confirm(
          '실행계획 품목 가져오기 시 기존에 작성된 내용이 모두 삭제됩니다.<br/>계속하시겠습니까?',
          '투입자재 재계산'
        );
        if (result) {
          const params = {
            work_order_id: vars.formData.id,
            warehouse_code: vars.warehouse.wh_code,
            excution_plan_ids : excutionPlanList
          };
          const apiService = new ApiService('/api/mes/v1/update-excution-to-work-order');
          await apiService.post('', params);
          await alert('실행계획 품목 가져오기가 완료되었습니다', '실행계획 품목 가져오기');
          vars.grid.item2.refresh();
        }
      },
      async requestExport() {
        const result = await confirm(
          '필요자재 출고요청 후 품목 변경이 불가능합니다.<br/>계속하시겠습니까?',
          '필요자재 출고요청'
        );
        if (result) {
          const params = {
            work_order_id: vars.formData.id,
          };
          const apiService = new ApiService('/api/mes/v1/export-work-order');
          await apiService.post('', params);
          await alert('필요자재 출고요청 완료되었습니다', '필요자재 출고요청');
          router.go();
        }
      },
      async newItem() {
        methods.gridItem1Refresh();
        methods.gridItem2Refresh();
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
        const result = await confirm(
          '이 항목을 삭제하시겠습니까?',
          '삭제 확인'
        );
        if (result) {
          try {
            await produceWorkOrder.remove(vars.formData.id);
            beforeExitConfirm.clear()
            await alert('삭제되었습니다', '삭제 확인');
            methods.redirect();
            vars.formState.readOnly = true;
          } catch (ex) {
            if (ex.response.status != 403) {
              await alert(
                '연결된 데이터가 있어서 삭제가 안됩니다',
                '삭제 확인'
              );
            }
          }
        }
      },
      async saveItem() {
        vars.loading.value = true;
        try {
          if (vars.formData.id) {
            // 기존 정보 업데이트
            await produceWorkOrder.update(vars.formData.id, vars.formData);
            if (vars.grid.item1) {
              await vars.grid.item1.saveEditData();
            }
            if (vars.grid.item2) {
              await vars.grid.item2.saveEditData();
            }

            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');

            methods.enableSave();
            methods.enableDelete();
          } else {
            // 채번이 없을 경우 자동 채번
            let { data } = await produceWorkOrder.insert(vars.formData);
            vars.formData.id = data.id;

            const item1 = vars.grid.item1;
            if (item1 && item1.hasEditData()) {
              await item1.saveEditData();
            }
            const item2 = vars.grid.item2;
            if (item2 && item2.hasEditData()) {
              await item2.saveEditData();
            }
            beforeExitConfirm.clear()
            methods.redirect(data.id);
            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');
          }
        } catch (ex) {
          if (ex.response.status === 602) {
            notifyError('이미 존재하는 작업지시번호 입니다');
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
          case 'work-order': {
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
      onFocusedCellChanged(e) {
        vars.focus.item1 = e;
      },
      updateEtcValue(v) {
        vars.dlg.finder.data = v;
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
      async gridItem2Refresh(id) {
        if (!id) id = 0;
        vars.filter.item2[0].val = id;
        vars.dataSource.item2.defaultFilters = vars.filter.item2;
        if (vars.grid.item2) {
          vars.grid.item2.cancelEditData();
          vars.grid.item2.refresh();
        }
      },
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`produce-work-order-${key}`, evt.component);
      },
      onDepartmentChanged(e) {
        if (!e.value) {
          vars.disabled.save = true;
          vars.disabled.items = true;
          vars.disabled.manager = true;
          vars.formData.manager = null;
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
      onDataError(e) {
        if (e.error.response.status == 605) {
          e.error.message = '연결된 데이터가 있어서 삭제가 안됩니다';
        } else if (e.error.response.status == 403) {
          e.error.message = '권한이 없습니다';
        }
      },
      availableStock(rowData) {
        if (!rowData.basic_stock) return '0';
        return rowData.basic_stock.available_stock;
      },
      currentStock(rowData) {
        if (!rowData.basic_stock) return '0';
        return rowData.basic_stock.current_stock;
      },
      onSavingItem(e) {
        e.changes.forEach(element => {
          if (element.type != 'remove') {
            console.log('work-order-onSavingItem', element.data);
            element.data.fk_work_order_id = vars.formData.id;
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
        produceWorkOrder.update(vars.formData.id, priceData);
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
      async setWarehouse2(newData, value, currentRowData) {
        const warehouseList = vars.dataSource.warehouse;
        for (let i = 0; i < warehouseList.length; i++) {
          if (warehouseList[i].wh_name == value) {
            newData.in_warehouse = { ...warehouseList[i] };
            newData.in_warehouse_code = warehouseList[i].wh_code;
            break;
          }
        }
      },
      setQuantity(newData, value, currentRowData) {
        const unproduced_quantity = currentRowData.unproduced_quantity - (currentRowData.required_quantity - value);
        if (unproduced_quantity >= 0) {
          newData.required_quantity = value;
          newData.unproduced_quantity = unproduced_quantity;
        }
      },
      setProjectManagement(newData, value, currentRowData){
        if(!value) return;
        newData.project_management = value;
        newData.fk_project_management_id = value.id;
      },
      loadBaseCode() {
        return baseCodeLoader(['부가세구분', '결재조건', '납품장소', '자산구분', '품목그룹'])
          .then(response => {
            vars.dataSource.payment_terms = response['결재조건'];
            vars.dataSource.vat_type = response['부가세구분'];
            vars.dataSource.delivery_place = response['납품장소'];
            vars.dataSource.asset_type = response['자산구분'];
            vars.dataSource.item_group = response['품목그룹'];
          })
          .then(() => (vars.init.value = true));
      },
      loadBaseItem() {
        vars.dataSource.baseItem = getBaseItem(
          null,
          null,
          vars.warehouse.wh_code
        );
      },
      loadPlanItem() {
        vars.dataSource.planItem = getProducePlanItem([{ name: 'unordered_quantity', op: 'gt', val: 0 }]);
      },
      checkPossibleSave() {
        if (vars.formData.department) {
          methods.enableSave();
          vars.disabled.items = false;
        }
      },
      redirect(id) {
        if (id) {
          router.replace({ path: `/produce/work-order/${id}` });
        } else {
          router.replace({ path: `/produce/work-order` });
        }
      },
      async redirectStockMoveRequest() {
        if (!vars.formData.stock_move_request_number) {
          await alert(
            '이동요청번호가 존재하지 않습니다',
            '재고이동요청으로 이동'
          );
          return;
        }
        const response = await stockMoveRequest.load({
          filter: [
            ['number', '=', vars.formData.stock_move_request_number],
            ['fk_company_id', '=', authService.getCompanyId()],
          ],
        });
        if (response.data.length > 0) {
          router.replace({ path: `/stock/move-request/${response.data[0].id}` });
        } else {
          await alert('이동요청번호가 존재하지 않습니다', '재고이동요청으로 이동');
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
      async printDocument () {
        if (!vars.formData.id) return

        const { data: item1 } = await vars.dataSource.item1.load()
        const { data: item2 } = await vars.dataSource.item2.load()

        const params = {}
        params.client_company = ''
        params.income_warehouse = ''

        if (item1.length) {
          params.client_company = item1[0].client_company
        }

        if (item2.length) {
          params.income_warehouse = item2[0].in_warehouse_code
          params.outcome_warehouse = item2[0].warehouse_code
        }
        
        params.etc = vars.formData.etc
        params.target_date = moment(vars.formData.target_date).format('YYYY년 M월 D일')
        params.number = vars.formData.number
        params.item1 = item1.map(itemTransform)
        params.item2 = orderBy(item2.map(itemTransform), ['item.item_code'], ['asc'])

        function itemTransform (item) {
          if (!item.required_quantity) item.required_quantity = 0
          if (!item.basic_stock) item.basic_stock = { current_stock: 0 }
          // else item.basic_stock.current_stock = numeral(item.basic_stock.current_stock).format('0,0');
          return item
        }

        await printDocument('workorder', params)
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
