<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">발주</div>
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
              :options="{ text: '품의서', type: 'print', icon: 'print', onClick: methods.printDocumentApproval }"
            />
            <dx-item widget="dxButton" location="after" locate-in-menu="auto"
              :options="{ text: '출력', type: 'print', icon: 'print', onClick: methods.printDocument }"
            />
            <dx-item widget="dxButton" location="after" locate-in-menu="auto"
              :options="{ text: '메일발송', type: 'print', icon: 'doc', onClick: methods.saveDocumentToPDF }"
            />
          </dx-toolbar>
        </div>
        <dx-form :form-data="vars.formData">
          <dx-group-item :col-count="5">
            <dx-group-item>
              <dx-simple-item
                data-field="order_number"
                :editor-options="{
                  placeholder: '(자동 or 직접입력)',
                  ...generateItemButtonOption('search', methods.createFindPopupFn('order', '발주조회')),
                }"
              >
                <dx-label text="발주번호" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="order_date"
                editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  ...vars.formState,
                }"
              >
                <dx-label text="발주일자" :show-colon="false" />
              </dx-simple-item>

              <dx-simple-item
                data-field="client_company"
                :editor-options="{
                  ...generateItemButtonOption(
                    'search',
                    methods.createFindPopupFn('client', '고객조회', {
                      name: vars.formData.client_company,
                    })
                  ),
                  ...vars.formState,
                  onEnterKey: methods.createFindPopupFn('client', '고객조회', {
                    name: vars.formData.client_company,
                  }),
                }"
              >
                <dx-label text="공급업체" :show-colon="false" />
                <dx-required-rule message="고객업체를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item
                data-field="client_manager"
                editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.client_manager,
                  displayExpr: 'name',
                  valueExpr: 'name',
                  acceptCustomValue: true,
                  disabled: vars.disabled.clientManager,
                  onValueChanged: methods.onClientManagerChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="업체담당자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="client_manager_email"
                :editor-options="{ readOnly: true }"
              >
                <dx-label text="업체 이메일" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item
                data-field="order_department"
                editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.department,
                  displayExpr: 'department_name',
                  valueExpr: 'department_name',
                  acceptCustomValue: true,
                  onValueChanged: methods.onDepartmentChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="발주부서" :show-colon="false" />
                <dx-required-rule message="발주부서를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item
                data-field="order_manager"
                editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.employee,
                  displayExpr: 'emp_name',
                  valueExpr: 'emp_name',
                  disabled: vars.disabled.manager,
                  ...vars.formState,
                  onValueChanged: methods.onManagerChanged
                }"
              >
                <dx-label text="발주담당자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="order_manager_email"
                :editor-options="{ readOnly: true }"
              >
                <dx-label text="발주담당자 이메일" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="order_type"
                editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.order_type,
                  displayExpr: 'code_name',
                  valueExpr: 'code_name',
                  ...vars.formState,
                }"
              >
                <dx-label text="발주구분" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="vat_type"
                editor-type="dxSelectBox"
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
              <dx-simple-item
                data-field="payment_terms"
                editor-type="dxSelectBox"
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
              <dx-simple-item
                data-field="delivery_date"
                editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  ...vars.formState,
                }"
              >
                <dx-label text="납품기한" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="delivery_place"
                editor-type="dxSelectBox"
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
                data-field="ref_number"
                :editor-options="{ ...vars.formState }"
              >
                <dx-label text="무상수리기간" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item
                data-field="project_management.project_number"
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
              <dx-simple-item
                data-field="end_user"
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
              <dx-simple-item
                data-field="note"
                :editor-options="{ ...vars.formState }"
              >
                <dx-label text="참고사항" :show-colon="false" />
              </dx-simple-item>
              <dx-group-item :col-count="2">
                <dx-simple-item data-field="approve" editor-type="dxCheckBox"
                  :editor-options="{ onValueChanged: methods.onApproveChanged }">
                    <dx-label text="발주승인" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item
                    data-field="confirmed"
                    editor-type="dxCheckBox"
                    :editor-options="{ onValueChanged: methods.onConfirmChanged }"
                  >
                    <dx-label text="발주확인" :show-colon="false" />
                </dx-simple-item>
              </dx-group-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item
                data-field="etc"
                editor-type="dxTextArea"
                :editor-options="{
                  ...generateItemButtonOption(
                    'rename',
                    methods.createFindPopupFn('etc', '비고', vars.formData.etc)
                  ),
                  ...vars.formState,
                  height: '174px',
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
            @data-error-occurred="methods.onDataError"
            @cell-dbl-click="methods.itemPopupClick"
            @focused-cell-changed="methods.onFocusedCellChanged"
          >
            <dx-grid-toolbar>
              <dx-item template="addFromPlan" location="before" :visible="!vars.formState.readOnly" />
              <dx-grid-item name="addRowButton" :options="{ onClick: methods.showAddPopup }" />
              <dx-grid-item name="saveButton" :visible="!!vars.formData.id" />
              <dx-grid-item name="revertButton" />
              <dx-grid-item name="columnChooserButton" />
            </dx-grid-toolbar>
            <template #addFromPlan>
              <dx-button text="발주계획에서 가져오기" icon="add" @click="methods.showAddOrderPlanPopup" />
            </template>

            <dx-column caption="품목코드" data-field="item_code" width="180" :allow-editing="false" />
            <dx-column caption="품명" data-field="item.item_name" :allow-editing="false" />
            <dx-column caption="규격" data-field="item.item_standard" :allow-editing="false" />
            <dx-column caption="발주수량" data-field="order_quantity" data-type="number" format="fixedPoint" :set-cell-value="methods.setQuantity" />
            <dx-column caption="예정단가" data-field="expect_unit_price" data-type="number" format="₩,##0" :allow-editing="false" />
            <dx-column caption="단가" data-field="unit_price" data-type="number" format="₩,##0" :set-cell-value="methods.setUnitPrice" />
            <dx-column caption="단위" data-field="item.unit" data-type="number" :allow-editing="false" />
            <dx-column caption="공급가" data-field="supply_price" data-type="number" format="₩,##0" :allow-editing="false" />
            <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
            <dx-column caption="확정납기" data-field="fixed_delivery_date" data-type="date" format="yyyy-MM-dd" :visible="false" />
            <dx-column caption="미가입고수량" data-field="not_shipped" data-type="number" format="fixedPoint" :allow-editing="false" v-if="vars.control.not_use_prereceiving" />
            <dx-column caption="미입고수량" data-field="not_shipped" data-type="number" format="fixedPoint" :allow-editing="false" v-else />
            <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :allow-editing="false" />
            <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :allow-editing="false" />
            <dx-column caption="입고창고" data-field="warehouse.wh_name" :set-cell-value="methods.setWarehouse">
              <dx-lookup value-expr="wh_name" display-expr="wh_name" :data-source="vars.dataSource.warehouse" />
            </dx-column>
            <dx-column caption="발주계획번호" data-field="order_plan_number" :allow-editing="false" />
            <dx-column caption="프로젝트번호" data-field="project_management.project_number"
              :editor-options="{
                ...generateItemButtonOption( 'search', methods.createFindPopupFn('project-item', '프로젝트조회'))
              }"
              :set-cell-value="methods.setProjectManagement"
            />
            <dx-column caption="공급사품번" data-field="client_item_number" />
            <dx-column caption="품목설명" data-field="item.item_detail" :allow-editing="false" />
            <dx-column caption="참고사항" data-field="note" />
            <dx-column caption="종결" data-field="closing_yn" data-type="boolean" />
            <dx-column caption="발주아이디" data-field="fk_purchase_order_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
            <dx-column  caption="발주계획품목아이디" data-field="fk_order_plan_item_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
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
      title="발주품목찾기"  
      content-template="popup-content"
      v-model:visible="vars.dlg.addItem.show"
      width="70%"
      :height="460"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'find-item-popup')"
    >

      <template #popup-content>
        <dx-data-grid
          column-resizing-mode="widget"
          :show-borders="true"
          :remote-operations="true"
          :column-auto-width="true"
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
          <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick"/>
          <dx-editing mode="row" :use-icons="true" :allow-adding="true" :allow-updating="true" :allow-deleting="true" />
        </dx-data-grid>
      </template>
    </dx-popup>

    <dx-popup
      title="발주계획에서 가져오기"  
      content-template="popup-content"
      v-model:visible="vars.dlg.addOrderPlanItem.show"
      width="70%"
      :height="460"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'load-order-popup')"
    >
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ text: '선택된 항목 추가', icon: 'add', onClick: methods.addSelectedOrderPlanRows }"
      />

      <template #popup-content>
        <dx-data-grid
          column-resizing-mode="widget"
          :show-borders="true"
          :remote-operations="true"
          :column-auto-width="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="vars.dataSource.planItem"
          :on-initialized="evt => methods.onGridInitialized(evt, 'planItem')"
        >
          <dx-column caption="발주계획번호" data-field="order_plan.order_plan_number" :sort-index="1" sort-order="desc" />
          <dx-column caption="발주계획일자" data-field="order_plan.order_plan_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="발주계획수량" data-field="order_plan_quantity" />
          <dx-column caption="단가" data-field="unit_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="금액" data-field="supply_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
          <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column dcaption="미발주" ata-field="unordered_quantity" />
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="수주번호" data-field="order_number" />
          <dx-column caption="주공급업체" data-field="main_supplier" />
          <dx-column caption="고객사품번" data-field="client_item_number" />

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
      :key="vars.dlg.finder.key"
      :title="vars.dlg.finder.title"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'multiuse-popup')"
    >
      <template #popup-content>
        <data-grid-client v-if="vars.dlg.finder.key === 'client'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-client v-else-if="vars.dlg.finder.key === 'enduser'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-order v-else-if="vars.dlg.finder.key === 'order'" @change="methods.finderReturnHandler" />
        <data-grid-project v-else-if="vars.dlg.finder.key === 'project'" @change="methods.finderReturnHandler" />
        <data-grid-project v-else-if="vars.dlg.finder.key === 'project-item'" @change="methods.finderReturnHandler" />
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

import { useRouter } from 'vue-router';
import { onMounted, ref, reactive, computed, watch, nextTick } from 'vue';

import { DxButton } from 'devextreme-vue/button';
import DxTextArea from 'devextreme-vue/text-area';
import { confirm, alert } from 'devextreme/ui/dialog';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxCustomRule, DxRequiredRule } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxLookup, DxPaging, DxEditing, DxSorting, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, 
  DxItem as DxGridItem, DxToolbar as DxGridToolbar, DxButton as DxGridButton,  DxRequiredRule as DxGridRequiredRule } from 'devextreme-vue/data-grid';

import PopupItemDetail from '@/components/base/popup-item-detail';
import DataGridClient from '../../components/base/data-client.vue';
import DataGridOrder from '../../components/purchase/data-order.vue';
import DataGridProject from '../../components/project/data-project.vue';

import authService from '../../auth';
import stateStore from '@/utils/state-store';
import ApiService from '@/utils/api-service';
import { notifyInfo, notifyError } from '../../utils/notify';
import {printDocument, saveDocumentToBlob, saveDocumentToPdfBlob} from '@/utils/print-document';
import { loadEmployee, loadWarehouse, loadDepartment, loadClientManager, } from '../../utils/data-loader';
import { calcPriceSummary, currentDateTime, beforeExitConfirm, generateItemButtonOption, } from '../../utils/util';

import { getStock } from '../../data-source/setup';
import { baseItem, baseClient, getBaseItem, baseCodeLoader, baseClientManager } from '../../data-source/base';
import { purchaseOrder, purchaseOrderPlanItem, getPurchaseOrderItem, getPurchaseOrderPlanItem, } from '../../data-source/purchase';
import { baseEmployee } from '../../data-source/base';
export default {
  components: {
    DxButton,
    DxTextArea,
    DxLoadPanel,
    DxToolbar, DxItem,
    DxPopup, DxToolbarItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxCustomRule, DxRequiredRule,
    DxDataGrid, DxColumn, DxLookup, DxPaging, DxEditing, DxSorting, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, 
    DxGridItem, DxGridToolbar, DxGridButton, DxGridRequiredRule,
    PopupItemDetail, DataGridClient, DataGridOrder, DataGridProject,
  },
  props: {
    id: [String, Number],
  },
  setup(props) {
    // variable 설정
    const router = useRouter();
    const vars = { dlg: {} };
    const uploadService = new ApiService('/api/mes/v1/mail-attachment');

    vars.init = ref(false);
    vars.loading = ref(false);
    vars.formState = reactive({ readOnly: true });
    vars.grid = { baseItem: null, planItem: null, item1: null };
    vars.dlg.addItem = reactive({ show: false });
    vars.dlg.addOrderPlanItem = reactive({ show: false });
    vars.dlg.finder = reactive({
      show: false,
      title: '',
      key: null,
      data: null,
    });
    vars.warehouse = {};
    vars.control = reactive({
      not_use_prereceiving: false,
    });
    vars.filter = {
      baseItem: {
        clientId: 0,
      },
      planItem: {
        clientCompany: '',
      },
      item1: [{ name: 'fk_purchase_order_id', op: 'eq', val: props.id || 0 }],
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
      order_type: [],
      vat_type: [],
      delivery_place: [],
      client_manager: [],
      department: [],
      employee: [],
      warehouse: [],
      item_group: [],
      asset_type: [],
      baseItem: null,
      planItem: null,
      item1: getPurchaseOrderItem(vars.filter.item1),
    });
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
      beforeExitConfirm.check(() => !vars.disabled.save)
    });
    // public methods
    const methods = {
      async initById(id) {
        await methods.gridItem1Refresh(id);
        if (!id) {
          vars.formData.id = null;
          vars.formData.created = null;
          vars.formData.order_number = ''; // 발주번호
          vars.formData.order_date = ''; // 발주일자
          vars.formData.client_company = ''; // 공급업체
          vars.formData.client_manager = ''; // 업체담당자
          vars.formData.client_manager_email = ''; // 업체담당자 이메일
          vars.formData.order_department = ''; // 발주부서
          vars.formData.order_manager = ''; // 발주담당자
          vars.formData.order_manager_email = ''; // 발주담당자 이메일
          vars.formData.order_type = ''; // 발주구분
          vars.formData.vat_type = ''; // 부가세구분
          vars.formData.payment_terms = ''; // 결재조건
          vars.formData.delivery_date = ''; // 납품기한
          vars.formData.delivery_place = ''; // 납품장소
          vars.formData.ref_number = ''; // 무상수리기간
          vars.formData.end_user = ''; // 실사용자
          vars.formData.note = ''; // 참고사항
          vars.formData.etc = ''; // 비고
          vars.formData.confirmed = 0;
          vars.formData.confirmed_date = null;
          vars.formData.confirmed_manager = null; // 발주확정
          vars.formData.approve = 0;
          vars.formData.approve_date = null;
          vars.formData.approve_manager = null; // 발주승인
          vars.formData.supply_price = 0; // 공급가
          vars.formData.vat = 0; // 부가세
          vars.formData.total_price = 0; // 합계금액
          vars.formData.fk_project_management_id = null; // 프로젝트번호
          vars.formData.project_management = null; // 프로젝트
          vars.formData.fk_company_id = authService.getCompanyId();

          vars.disabled.edit = true;
          vars.disabled.delete = true;
          vars.disabled.save = true;
          vars.disabled.items = true;
          vars.disabled.manager = true;
          vars.disabled.clientManager = true;
          return;
        }

        let { data } = await purchaseOrder.byKey(id);
        Object.assign(vars.formData, data);

        methods.enableDelete();
        vars.disabled.edit = false;
        if (vars.formData.client_company && vars.formData.order_department) {
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

        const rows = await vars.grid.baseItem.getSelectedRowsData();
        for (let row of rows) {
          let checkYn = false;
          if (row.import_check == 0) {
            checkYn = true;
          }
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
          data.order_quantity = 0; // 발주수량
          data.unit_price = row.purchase_price ? row.purchase_price : 0; // 단가
          data.request_delivery_date = null; // 요청납기
          data.fixed_delivery_date = null; // 확정납기
          data.not_shipped = 0; // 미입고수량
          data.basic_stock = { ...basicStock }; // 기초재고
          data.warehouse = { ...vars.warehouse }; // 입고창고
          data.warehouse_code = vars.warehouse.wh_code; // 창고코드
          data.order_plan_number = null; // 발주계획번호
          data.client_item_number = clientItemNumber; // 공급사품번
          data.note = ''; // 참고사항
          data.closing_yn = false; // 종결
          data.fk_order_plan_item_id = null; // 발주계획품목 ID
          data.fk_purchase_order_id = vars.formData.id; // 발주 ID
          data.fk_project_management_id = vars.formData.fk_project_management_id; // 프로젝트번호
          data.check_yn = checkYn; // 검수완료
        }
        grid.refresh();
        vars.dlg.addItem.show = false;
      },
      async addSelectedOrderPlanRows() {
        const grid = vars.grid.item1;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        const rows = await vars.grid.planItem.getSelectedRowsData();
        for (let row of rows) {
          let checkYn = false;
          if (row.item.import_check == 0) {
            checkYn = true;
          }

          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code; // 품목코드
          data.item = { ...row.item }; // 품목
          data.order_quantity = row.order_plan_quantity; // 발주수량
          data.unit_price = row.unit_price ? row.unit_price : 0; // 단가
          data.supply_price = data.order_quantity * data.unit_price; // 공급가
          data.request_delivery_date = row.request_delivery_date; // 요청납기
          data.fixed_delivery_date = null; // 확정납기
          data.not_shipped = row.order_plan_quantity; // 미입고수량
          data.basic_stock = { ...row.basic_stock }; // 기초재고
          data.warehouse = { ...row.warehouse }; // 입고창고
          data.warehouse_code = row.warehouse_code; // 창고코드
          data.order_plan_number = row.order_plan.order_plan_number; // 발주계획번호
          data.fk_project_management_id = row.fk_project_management_id; // 프로젝트번호
          data.client_item_number = row.client_item_number; // 공급사품번
          data.note = ''; // 참고사항
          data.closing_yn = false; // 종결
          data.fk_order_plan_item_id = row.id; // 발주계획품목 ID
          data.fk_purchase_order_id = vars.formData.id; // 발주 ID
          data.check_yn = checkYn; // 검수완료
        }
        grid.refresh();
        vars.dlg.addOrderPlanItem.show = false;
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
        methods.gridClear(vars.grid.baseItem);
        vars.dlg.addItem.show = true;
      },
      showAddOrderPlanPopup() {
        const notContains = [];
        for (const item of vars.grid.item1.getVisibleRows()) {
          if (!item.id && item.data.fk_order_plan_item_id) {
            notContains.push(['id', '<>', item.data.fk_order_plan_item_id], 'and');
          }
        }
        notContains.pop()

        if (vars.grid.planItem) {
          vars.grid.planItem.filter(notContains);
          methods.gridClear(vars.grid.planItem);
        }
        vars.dlg.addOrderPlanItem.show = true;
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
        stateStore.bind(`purchase-order-${key}`, evt.component);
      },
      async newItem() {
        
        methods.gridItem1Refresh();
        if (vars.formData.id) {
          methods.redirect();
          vars.formData.id = null;
        }
        setTimeout(() => {
          vars.formData.created = null;
          vars.formData.order_date = currentDateTime();
          vars.formData.order_department = authService.getDepartmentName();
          vars.formData.order_manager = authService.getUserName();
          vars.formData.order_type = methods.getFirstOrderType();
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
        const result = await confirm(
          '이 항목을 삭제하시겠습니까?',
          '삭제 확인'
        );
        if (result) {
          try {
            await purchaseOrder.remove(vars.formData.id);
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
            await purchaseOrder.update(vars.formData.id, vars.formData);
            if (vars.grid.item1) await vars.grid.item1.saveEditData();

            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');

            methods.enableSave();
            methods.enableDelete();
          } else {
            // 채번이 없을 경우 자동 채번
            let { data } = await purchaseOrder.insert(vars.formData);
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
            notifyError('이미 존재하는 발주번호 입니다');
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
          case 'order': {
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
            break;
          }
          case 'project-item': {
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

        vars.filter.baseItem.clientId = client ? client.id : 0;
        methods.loadBaseItem();

        vars.filter.planItem.clientCompany = client ? client.name : '';
        methods.loadPlanItem();
        if (!client) {
          vars.disabled.edit = true;
          vars.disabled.delete = true;
          vars.disabled.save = true;
          vars.disabled.items = true;
          vars.disabled.tradeYn = false;
          vars.disabled.clientManager = true;
          vars.formData.client_manager = null;
          vars.formData.client_manager_email = null; // 업체담당자 이메일
          vars.dataSource.client_manager = [];

          if (inputValue) {
            vars.disabled.edit = false;
            vars.disabled.delete = false;
          }
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
              vars.disabled.clientManager = false;
              vars.formData.client_manager = null;
              vars.formData.client_manager_email = null; 

              baseClient.load({
                filter: [['name', '=', client.name]]
              }).then(({ data }) => {
                if (data.length > 0) {
                  baseClientManager.load({
                    filter: [['fk_client_id', '=', data[0].id]],
                    sort: [{selector: 'id', desc: true}],
                    take: 10000000,
                    skip: 0,
                  }).then(({ data }) => {
                    vars.dataSource.client_manager = data;
                    if (data.length > 0) {
                      vars.formData.client_manager = vars.dataSource.client_manager[0].name;
                      vars.formData.client_manager_email = vars.dataSource.client_manager[0].email;
                    }
                  });
                }
              });
            } else {
              vars.formData.client_company = '';
              vars.disabled.tradeYn = true;
              vars.formData.client_manager = null;
              vars.formData.client_manager_email = null; 
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
            const result = await confirm(
              '거래중지 업체입니다. 계속 진행하시겠습니까?',
              'EndUser'
            );
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
        if(!e.event && e.value){
          vars.formState.readOnly = true;
          vars.disabled.edit = true;
          vars.disabled.delete = true;
          vars.disabled.items = true;
        }
        if(!e.event) return;
        if (!vars.formData.id) {
          vars.formData.confirmed = 0;
          return;
        }
        let param = {};
        const getUserName = authService.getUserName();
        if (e.value) {
           param.confirmed = 1;
           if(getUserName == '김영순'){
            param.confirmed_manager = getUserName;
            param.confirmed_date = moment().format('YYYY-MM-DD HH:mm:ss');
           }
          vars.formState.readOnly = true;
          vars.disabled.edit = true;
          vars.disabled.delete = true;
          vars.disabled.items = true;
        } else {
          param.confirmed = 0;
          if(getUserName == '김영순'){
            param.confirmed_manager = null;
            param.confirmed_date = null;
          }
          if (vars.formData.client_company && vars.formData.order_department) {
            methods.enableDelete();
            vars.disabled.edit = false;
            vars.disabled.items = false;
          }
        }

        const { data } = await purchaseOrder.update(vars.formData.id, param);
        vars.formData.confirmed = data.confirmed;
        vars.formData.confirmed_manager = data.confirmed_manager;
        vars.formData.confirmed_date = data.confirmed_date;
      },
      async onApproveChanged(e){
        if(!e.event) return;
        if (!vars.formData.id) {
          vars.formData.approve = 0;
          return;
        }
        let param = {};
        const getUserName = authService.getUserName();
        if (e.value) {
          param.approve = 1;
          if(getUserName == '홍석준'){
            param.approve_manager = getUserName;
            param.approve_date = moment().format('YYYY-MM-DD HH:mm:ss');
          }
        }else{
          param.approve = 0;
          if(getUserName == '홍석준'){
            param.approve_manager = null;
            param.approve_date = null;
          }

        }
        const { data } = await purchaseOrder.update(vars.formData.id, param);
        vars.formData.approve = data.approve;
        vars.formData.approve_manager = data.approve_manager;
        vars.formData.approve_date = data.approve_date;
      },
      updateEtcValue(v) {
        vars.dlg.finder.data = v;
      },
      onDepartmentChanged(e) {
        if (!e.value) {
          methods.enableSave();
          vars.disabled.items = true;
          vars.disabled.manager = true;
          vars.formData.order_manager = null;
          // vars.formData.order_manager_email = null;
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
      async onManagerChanged(e){
        // const { data  } = await baseEmployee.load({
        //   filter: [['emp_name', '=', e.value]]
        // })
        // if(data.length > 0){
        //   vars.formData.order_manager_email = data[0].emp_email;
        // }else{
        //   vars.formData.order_manager_email = null;
        // }
      },
      onFocusedCellChanged(e) {
        vars.focus.item1 = e;
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
            element.data.fk_purchase_order_id = vars.formData.id;
            delete element.data.item;
            delete element.data.order;
            delete element.data.order_plan_item;
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
        purchaseOrder.update(vars.formData.id, priceData);
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
        newData.not_shipped =
          currentRowData.not_shipped + (value - currentRowData.order_quantity);
        newData.order_quantity = value;
        newData.unit_price = currentRowData.unit_price;
        newData.supply_price = methods.calculateTotalPriceWithDecimal(newData.unit_price, newData.order_quantity);
      },
      setUnitPrice(newData, value, currentRowData) {
        newData.order_quantity = currentRowData.order_quantity;
        newData.unit_price = value;
        newData.supply_price = methods.calculateTotalPriceWithDecimal(newData.unit_price, newData.order_quantity);
        if(currentRowData.excution_plan_item){
          newData.excution_plan_item = {...currentRowData.excution_plan_item};
          newData.excution_plan_item.purchase_unit_price = value;
        }
        if(currentRowData.excution_plan_subcontract){
          newData.excution_plan_subcontract = {...currentRowData.excution_plan_subcontract};
          newData.excution_plan_subcontract.purchase_unit_price = value;
        }
      },
      setProjectManagement(newData, value, currentRowData){
        if(!value) return;
        newData.project_management = value;
        newData.fk_project_management_id = value.id;
      },
      onClientManagerChanged(e){
        // console.log("업체담당자 : ",e.value)
      },
      loadBaseCode() {
        return baseCodeLoader([
          '부가세구분',
          '발주구분',
          '결재조건',
          '납품장소',
          '자산구분', 
          '품목그룹',
        ])
          .then(response => {
            vars.dataSource.vat_type = response['부가세구분'];
            vars.dataSource.order_type = response['발주구분'];
            vars.dataSource.payment_terms = response['결재조건'];
            vars.dataSource.delivery_place = response['납품장소'];
            vars.dataSource.asset_type = response['자산구분'];
            vars.dataSource.item_group = response['품목그룹'];
          })
          .then(() => (vars.init.value = true));
      },
      async loadControl() {
        vars.control.not_use_prereceiving = authService.getMenu().find((v)=> v.name == "가입고") ? true : false;
        console.log(vars.control.not_use_prereceiving)   
      },
      loadBaseItem() {
        vars.dataSource.baseItem = getBaseItem(
          null,
          vars.filter.baseItem.clientId,
          vars.warehouse.wh_code
        );
      },
      loadPlanItem() {
        vars.dataSource.planItem = getPurchaseOrderPlanItem([
          {
            name: 'main_supplier',
            op: 'eq',
            val: vars.filter.planItem.clientCompany,
          },
          {
            name: 'unordered_quantity',
            op: 'gt',
            val: 0,
          },
        ]);
      },
      checkPossibleSave() {
        if (vars.formData.client_company && vars.formData.order_department) {
          methods.enableSave();
          vars.disabled.items = false;
        }
      },
      getFirstOrderType() {
        return methods.getFirstItemName(vars.dataSource.order_type);
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
        if (id) {
          router.replace({ path: `/purchase/order/${id}` });
        } else {
          router.replace({ path: `/purchase/order` });
        }
      },
      itemPopupClick({ column, data }) {
        if (column.name === 'item_code') {
          vars.itemDetail.id = data.item.id;
          vars.itemDetail.visible = true;
        }
      },
      async createExportParams () {
        if (!vars.formData.id) return;
        const params = { ...vars.formData };
        params.supply_price = numeral(vars.formData.supply_price).format('0,0.00');
        params.total_price = numeral(vars.formData.total_price).format('0,0.00');
        params.tax_price = numeral(
          vars.formData.total_price - vars.formData.supply_price
        ).format('0,0.00');
        params.order_date = vars.formData.order_date
          ? moment(vars.formData.order_date).format('YYYY년 M월 D일')
          : ''
        params.delivery_date = vars.formData.delivery_date
          ? moment(vars.formData.delivery_date).format('YYYY년 M월 D일')
          : ''

        const orderManager = vars.dataSource.employee.find(
          v => v.emp_name === vars.formData.order_manager
        );
        if (orderManager) {
          params.order_manager = orderManager;
          const department = vars.dataSource.department.find(
            v => v.id === orderManager.fk_department_id
          );
          if (department)
            params.order_manager.department_name = department.department_name;
        } else params.order_manager = { emp_name: vars.formData.order_manager };

        const { data: item1 } = await vars.dataSource.item1.load();
        params.items = [...item1];
        let delivery_price = 0;
        let note = '';
        params.items.forEach(item => {
          if (
            item.excution_plan_item &&
            typeof item.excution_plan_item.delivery_price === 'number' &&
            item.excution_plan_item.delivery_price !== null
          ) {
            delivery_price += item.excution_plan_item.delivery_price;
          }
          if(item.excution_plan_item && item.excution_plan_item.note){
            note += item.excution_plan_item.note + '<br/>';
          }
          item.order_quantity = numeral(item.order_quantity).format('0,0');
          item.unit_price = numeral(item.unit_price).format('0,0.00');
          item.supply_price = numeral(item.supply_price).format('0,0.00');

          const { total_price } = calcPriceSummary(
            vars.formData.vat_type,
            item.supply_price
          );
          item.total_price = numeral(total_price).format('0,0.00');

          item.request_delivery_date = item.request_delivery_date
            ? moment(item.request_delivery_date).format('YYYY.M.D')
            : ''
        });
        params.delivery_price = delivery_price;
        params._note = note;
        const clientManager = vars.dataSource.client_manager.find(
          v => v.name === vars.formData.client_manager
        );
  
        if (clientManager) {
          params.client_manager = clientManager;
          params.client_manager.ceo_name = clientManager.client.ceo_name;
          params.client_manager.fax = clientManager.client.fax;
        } 
        else if(vars.formData.client_manager) {
          params.client_manager = { name: vars.formData.client_manager };
          params.client_manager.ceo_name = vars.dataSource.client_manager[0].client.ceo_name;
          params.client_manager.fax = vars.dataSource.client_manager[0].client.fax;
          params.client_manager.email = vars.dataSource.client_manager[0].client.email;
          params.client_manager.mobile = vars.dataSource.client_manager[0].client.phone;
        } 


        if (params.project_management) {
          const { data: projectManager } = await baseEmployee.load({
            filter: [['emp_name', '=', params.project_management.project_manager]]
          });
          if (projectManager.length > 0) {
            params.project_management.project_manager_position = projectManager[0].emp_position;
            params.project_management.project_manager_email = projectManager[0].emp_email;
            params.project_management.project_manager_mobile = projectManager[0].emp_mobile;
          }
        }
        return params
      },
      async saveDocumentToPDF() {
        if (!vars.formData.id) return;
        vars.loading.value = true;
        const params = await methods.createExportParams();
        const blob = await saveDocumentToPdfBlob('order', params);
        try {
          const fd = new FormData()
          fd.append('file', blob, `${vars.formData.order_number}.pdf`)
    
          const {data: filename} = await uploadService.post('', fd)
          const body = `발주서 다운로드: ${location.origin}/api/mes/v1/mail-attachment/${filename}`
          const mailto = `mailto:?subject=${encodeURIComponent('발주서')}&body=${encodeURIComponent(body)}`

          location.href = mailto
        }
        catch (ex) {
          console.error(ex)
        }
        vars.loading.value = false;
      },
      async printDocument() {
        if (!vars.formData.id) return;
        const params = await methods.createExportParams();

        params['items'].forEach( (item) => {
          item.request_delivery_date = moment(item.request_delivery_date, "YYYY.MM.DD").format('YYYY-MM-DD')
        })
        console.log("params : ", params)
        await printDocument('order', params);
      },
      async printDocumentApproval() {
        if (!vars.formData.id) return;
        const params = await methods.createExportParams();
        params.order_date_short = vars.formData.order_date
          ? moment(vars.formData.order_date).format('YYMMDD')
          : '';
        console.log(params)
        await printDocument('approval', params);
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
            options.totalValue += methods.calculateTotalPriceWithDecimal(options.value.unit_price, options.value.order_quantity);
          } else if (options.summaryProcess === 'finalize') {
            const response = calcPriceSummary(vars.formData.vat_type, options.totalValue);
            vars.formData.supply_price = response.supply_price;
            vars.formData.vat = response.vat;
            vars.formData.total_price = response.total_price;
          }
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
      purchaseOrderPlanItem,
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
