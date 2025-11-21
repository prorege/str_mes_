<template>
    <div v-if="vars.init.value">
      <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
      <div class="content-block">
        <div class="dx-card responsive-paddings back-colored">
          <div class="content-header">
            <dx-toolbar class="back-colored">
              <dx-item location="before"
                ><div class="content-title">A/S처리</div></dx-item
              >
              <dx-item location="after">
                <div class="barobill-state" v-if="vars.dlg.invoice.state">{{ vars.dlg.invoice.state }}</div>
              </dx-item>
              <dx-item location="after" locate-in-menu="auto" widget="dxButton" :visible="true"
                :options="{ text: '전자세금계산서발행', type: 'copy', icon: 'paste', onClick: methods.exportInvoice }"
                />
              <dx-item
                location="after"
                locate-in-menu="auto"
                widget="dxButton"
                :options="{
                  text: '신규',
                  type: 'add',
                  icon: 'add',
                  onClick: methods.newItem,
                  visible: true
                }"
              />
              <dx-item
                location="after"
                locate-in-menu="auto"
                widget="dxButton"
                :options="{
                  text: '수정',
                  type: 'rename',
                  icon: 'rename',
                  disabled: vars.disabled.edit,
                  onClick: methods.editItem,
                }"
              />
              <dx-item
                location="after"
                locate-in-menu="auto"
                widget="dxButton"
                :options="{
                  text: '삭제',
                  type: 'remove',
                  icon: 'remove',
                  disabled: vars.disabled.delete,
                  onClick: methods.deleteItem,
                }"
              />
              <dx-item
                location="after"
                locate-in-menu="auto"
                widget="dxButton"
                :options="{
                  text: '저장',
                  type: 'save',
                  icon: 'save',
                  disabled: vars.disabled.save,
                  onClick: methods.saveItem,
                }"
              />
            </dx-toolbar>
          </div>
          <dx-form
          :form-data="vars.formData">
            <dx-group-item :col-count=5>
              <dx-group-item :col-span=2 :col-count=2>
                <dx-group-item :col-span=1 :col-count=1> 
                  <dx-simple-item
                    data-field="result_number"
                    :editor-options="{
                      onValueChanged: methods.onValueChanged,
                      placeholder: '(자동 or 직접입력)',
                      ...methods.generateItemButtonOption(
                        'search',
                        methods.createFindPopupFn('result_number', 'A/S처리조회')
                      ),
                    }"
                  >
                    <dx-label text="A/S처리번호" :show-colon="false" />
                  </dx-simple-item>
                  <dx-simple-item
                    data-field="as_receipt.receipt_number"
                    :editor-options="{
                      ...vars.formState,
                      ...methods.generateItemButtonOption(
                        'search',
                        methods.createFindPopupFn('receipt_number', 'A/S접수조회')
                      ),
                    }"
                  >
                    <dx-label text="A/S접수번호" :show-colon="false" />
                  </dx-simple-item>
                  <dx-simple-item
                    data-field="project_management.project_number"
                    :editor-options="{
                      readOnly: true,
                    }"
                  >
                    <dx-label text="프로젝트번호" :show-colon="false" />
                  </dx-simple-item>
                </dx-group-item>
                <dx-group-item :col-span=1 :col-count=1>
                  <dx-simple-item
                    data-field="as_receipt.receipt_date"
                    editor-type="dxDateBox"
                    :editor-options="{
                      readOnly: true,
                    }"
                  >
                    <dx-label text="접수일자" :show-colon="false" />
                  </dx-simple-item>
                  <dx-simple-item
                    data-field="as_receipt.department"
                    :editor-options="{
                      readOnly: true,
                    }"
                  >
                    <dx-label text="접수부서" :show-colon="false" />
                  </dx-simple-item>
                  <dx-simple-item
                    data-field="as_receipt.manager"
                    editor-type="dxTextBox"
                    :editor-options="{
                      readOnly: true,
                    }"
                  >
                    <dx-label text="접수 담당자" :show-colon="false" />
                  </dx-simple-item>
                </dx-group-item>
                <dx-group-item :col-span=2 :col-count=1>
                  <dx-simple-item
                    :col-span=2
                    data-field="as_receipt.project_name"
                    editor-type="dxTextBox"
                    :editor-options="{
                      readOnly: true,
                    }"
                  >
                    <dx-label text="프로젝트 명" :show-colon="false" />
                  </dx-simple-item>
              </dx-group-item>
              </dx-group-item>
              <dx-group-item :col-span=3 :col-count=3>
                <dx-group-item :col-span=3 :col-count=3>
                    <dx-simple-item
                        data-field="as_receipt.paid_type"
                        editor-type="dxTextBox"
                        :editor-options="{
                            readOnly: true,
                        }"
                        >
                        <dx-label text="유무상 구분" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item
                        data-field="result_price"
                        editor-type="dxNumberBox"
                        :editor-options="{
                            readOnly: true,
                            format: 'currency',
                        }"
                        >
                        <dx-label text="A/S 처리비용" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item
                        data-field="as_receipt.client_manager"
                        editor-type="dxTextBox"
                        :editor-options="{
                            readOnly: true,
                        }"
                        >
                        <dx-label text="고객사 담당자" :show-colon="false" />
                    </dx-simple-item>
                </dx-group-item>
                <dx-group-item :col-span=3 :col-count=3>
                    <dx-simple-item
                      data-field="result_date"
                      editor-type="dxDateBox"
                      :editor-options="{
                        dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                        showClearButton: true,
                        useMaskBehavior: true,
                        ...vars.formState,
                      }"
                      >
                      <dx-label text="처리일자" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item
                        data-field="result_manager"
                        editor-type="dxSelectBox"
                        :editor-options="{
                            onValueChanged: methods.onValueChanged,
                            dataSource: vars.dataSource.employee,
                            displayExpr: 'emp_name',
                            valueExpr: 'emp_name',
                            ...vars.formState,
                        }"
                        >
                        <dx-label text="처리담당자" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item
                        data-field="result_manager_check"
                        editor-type="dxTextBox"
                        :editor-options="{
                            ...vars.formState,
                        }"
                        >
                        <dx-label text="담당자 확인" :show-colon="false" />
                    </dx-simple-item>
                </dx-group-item>
                <dx-group-item :col-span=3 :col-count=3>
                  <dx-simple-item
                      data-field="result_department"
                      editor-type="dxSelectBox"
                      :editor-options="{
                          dataSource: vars.dataSource.department,
                          displayExpr: 'department_name',
                          valueExpr: 'department_name',
                          onValueChanged: methods.selectDepartment,
                          ...vars.formState,
                      }"
                      >
                      <dx-label text="처리부서" :show-colon="false" />
                  </dx-simple-item>
                  <dx-simple-item 
                        data-field="process_status" 
                        editor-type="dxSelectBox"
                        :editor-options="{
                            dataSource: vars.dataSource.process_status,
                            displayExpr: 'code_name',
                            valueExpr: 'code_name',
                        ...vars.formState,
                        }">
                        <dx-label text="처리현황" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item 
                        data-field="final_status" 
                        editor-type="dxSelectBox"
                        :editor-options="{
                            dataSource: vars.dataSource.process_status,
                            displayExpr: 'code_name',
                            valueExpr: 'code_name',
                        ...vars.formState,
                        }">
                        <dx-label text="최종현황" :show-colon="false" />
                    </dx-simple-item>
                </dx-group-item>
                <dx-group-item :col-span=3 :col-count=1>
                    <dx-simple-item 
                        data-field="as_receipt.receipt_detail" 
                        :editor-options="{
                        ...vars.formState,
                        }">
                        <dx-label text="접수내용" :show-colon="false" />
                    </dx-simple-item>
                </dx-group-item>
              </dx-group-item>
              <dx-group-item :col-span=5 :col-count=1>
                  <dx-simple-item 
                      data-field="result_detail" 
                      :editor-options="{
                      ...vars.formState,
                      }">
                      <dx-label text="처리내용" :show-colon="false" />
                  </dx-simple-item>
              </dx-group-item>              
            </dx-group-item>
          </dx-form>
        </div>
        <div class="dx-card responsive-paddings mt-1">
          <dx-tab-panel 
            :animation-enabled="false" 
            :swipe-enabled="false" 
            :defer-rendering="false" 
          >
            <dx-item title="사용자재">
              <template #default>
                <div class="pa-2">
                  <dx-data-grid
                    class="fixed-header-table"
                    height="calc(100vh - 516px)"
                    data-serialization-format="yyyy-MM-ddTHH:mm:ss"
                    column-resizing-mode="widget"
                    :show-borders="true"
                    :remote-operations="false"
                    :column-auto-width="true"
                    :focused-row-enabled="true"
                    :allow-column-resizing="true"
                    :allow-column-reordering="true"
                    :row-alternation-enabled="true"
                    :select-text-onedit-start="true"
                    :data-source="vars.dataSource.item"
                    :on-initialized="evt => methods.onGridInitialized(evt, 'item')"
                    @saving="methods.onSavingItem"
                    @data-error-occurred="methods.onDataError"
                    >
                    <dx-grid-toolbar>
                        <dx-grid-item template="addItemRowButton" location="after" :visible="!vars.formState.readOnly" />
                        <dx-grid-item template="itemSaveButton" location="after" :visible="false" />
                        <dx-grid-item name="revertButton" location="after" />
                    </dx-grid-toolbar>
                    <template #addItemRowButton>
                        <dx-button text="품목찾기" icon="add" @click="methods.showAddPopup" />
                    </template>
                    <template #itemSaveButton>
                        <dx-button text="저장" icon="save" @click="methods.itemSaveButton('item')" />
                    </template>
                    <dx-column type="buttons" :visible="!vars.formState.readOnly"/>
                    <dx-column caption="품목코드" data-field="item_code" />
                    <dx-column caption="품명" data-field="item.item_name" />
                    <dx-column caption="규격" data-field="item.item_standard" />
                    <dx-column caption="수량" data-field="item_quantity" data-type="number" format="fixedPoint" :set-cell-value="methods.setQuantity" />
                    <dx-column caption="단가" data-field="unit_price" data-type="number" format="currency" :set-cell-value="methods.setUnitPrice" />
                    <dx-column caption="공급가" data-field="supply_price" data-type="number" format="currency" :allow-editing="false" />
                    <dx-column caption="비고" data-field="etc" />
                    <dx-scrolling mode="standard" />
                    <dx-summary :recalculate-while-editing="true" :calculate-custom-summary="methods.calcSummaryItem">
                        <dx-total-item name="supply_price" summary-type="custom" />
                    </dx-summary>
                    <dx-editing mode="batch"
                      :use-icons="true"
                      :allow-adding="!vars.formState.readOnly"
                      :allow-updating="!vars.formState.readOnly"
                      :allow-deleting="!vars.formState.readOnly"
                      />
                  </dx-data-grid>
                </div>
              </template>
            </dx-item>
            <dx-item title="파일 업로드">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 516px)"
                  date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                  column-resizing-mode="widget"
                  :on-initialized="
                    evt => methods.onGridInitialized(evt, 'attachment')
                  "
                  :remote-operations="true"
                  :data-source="vars.dataSource.attachment"
                  :show-borders="true"
                  :allow-column-reordering="true"
                  :allow-column-resizing="true"
                  :column-auto-width="true"
                  :select-text-on-edit-start="true"
                  :row-alternation-enabled="true"
                  :focused-row-enabled="true"
                  @saving="methods.onSavingAttachment"
                  @row-removing="methods.onAttchmentRowRemoving"
                >
                  <dx-grid-toolbar>
                      <dx-grid-item template="addRowButtonAttachment" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item template="itemSaveButtonAttachment" location="after" :visible="false" />
                      <dx-grid-item name="revertButton" location="after" />
                  </dx-grid-toolbar>
                  <template #addRowButtonAttachment>
                      <dx-button text="첨부파일 추가" icon="add" @click="methods.addFile" />
                  </template>
                  <template #itemSaveButtonAttachment>
                      <dx-button text="저장" icon="save" @click="methods.itemSaveButton('attachment')" />
                  </template>
                  <dx-column type="buttons" :visible="!vars.formState.readOnly"/>
                  <dx-column caption="파일명" data-field="file_name" />
                  <dx-column caption="다운로드" data-field="file_path" cell-template="download" :allow-editing="false" />
                  <template #download="{data}">
                    <a style="cursor: pointer; text-decoration: underline;" @click="methods.downloadFile(data)">다운로드</a>
                  </template>
                  <dx-editing mode="batch"
                    :use-icons="true"
                    :allow-adding="!vars.formState.readOnly"
                    :allow-updating="!vars.formState.readOnly"
                    :allow-deleting="!vars.formState.readOnly"
                    />
                  <dx-scrolling mode="standard" />
             
                </dx-data-grid>
              </div>
            </template>
          </dx-item>
          <dx-item title="경비">
              <template #default>
                <div class="pa-2">
                  <dx-data-grid
                    class="fixed-header-table"
                    height="calc(100vh - 516px)"
                    data-serialization-format="yyyy-MM-ddTHH:mm:ss"
                    column-resizing-mode="widget"
                    :show-borders="true"
                    :remote-operations="false"
                    :column-auto-width="true"
                    :focused-row-enabled="true"
                    :allow-column-resizing="true"
                    :allow-column-reordering="true"
                    :row-alternation-enabled="true"
                    :select-text-onedit-start="true"
                    :data-source="vars.dataSource.expense"
                    :on-initialized="evt => methods.onGridInitialized(evt, 'expense')"
                    @saving="methods.onSavingItem"
                    @data-error-occurred="methods.onDataError"
                    @init-new-row="(e) => methods.initNewRow(e, 'expense')"
                    >
                    <dx-grid-toolbar>
                        <dx-grid-item template="addItemRowButtonExpense" location="after" :visible="!vars.formState.readOnly" />
                        <dx-grid-item template="itemSaveButton" location="after" :visible="false" />
                        <dx-grid-item name="revertButton" location="after" />
                    </dx-grid-toolbar>
                    <template #addItemRowButtonExpense>
                        <dx-button text="경비 추가" icon="add" @click="methods.addItemRowButton('expense')" />
                    </template>
                    <template #itemSaveButtonExpense>
                        <dx-button text="저장" icon="save" @click="methods.itemSaveButton('expense')" />
                    </template>
                    <dx-column type="buttons" :visible="!vars.formState.readOnly"/>
                    <dx-column caption="지출일자" data-field="expense_date" data-type="date" format="yyyy-MM-dd" />
                    <dx-column caption="경비항목" data-field="expense_description" />
                    <dx-column caption="등록자" data-field="register" :allow-editing="false" />
                    <dx-column caption="금액" data-field="expense_amount" data-type="number" format="currency" />
                    <dx-column caption="비고" data-field="etc" />
                    <dx-scrolling mode="standard" />
                    <dx-summary :recalculate-while-editing="true" :calculate-custom-summary="methods.calcSummaryItem">
                        <dx-total-item name="expense_amount" summary-type="custom" />
                    </dx-summary>
                    <dx-editing mode="batch"
                      :use-icons="true"
                      :allow-adding="!vars.formState.readOnly"
                      :allow-updating="!vars.formState.readOnly"
                      :allow-deleting="!vars.formState.readOnly"
                      />
                  </dx-data-grid>
                </div>
              </template>
            </dx-item>
          </dx-tab-panel>
        </div>
      </div>
      <dx-popup
        v-model:visible="vars.dlg.finder.show"
        content-template="popup-content"
        width="60%"
        height="60%"
        :title="vars.dlg.finder.title"
        :close-on-outside-click="true"
        :key="vars.dlg.finder.key"
        :resize-enabled="true"
        @initialized="evt => methods.onGridInitialized(evt, 'find-popup')"
      >
        <template #popup-content>
          <data-grid-as-receipt
            v-if="vars.dlg.finder.key === 'receipt_number'"
            @change="methods.finderReturnHandler" :filters="{ name: 'closing_yn', op: 'eq', val: false }"
          />
          <data-grid-as-result v-else-if="vars.dlg.finder.key === 'result_number'" @change="methods.finderReturnHandler" />
          <data-grid-project v-else-if="vars.dlg.finder.key === 'project'" @change="methods.finderReturnHandler" />
  
      
        </template>
      </dx-popup>
      <dx-popup
        v-model:visible="vars.dlg.addItem.show"
        content-template="popup-content"
        title="품목찾기"
        :close-on-outside-click="true"
        width="70%"
        :height="500"
        :resize-enabled="true"
        @hidden="methods.addItemHidden"
        @initialized="evt => methods.onGridInitialized(evt, 'add-popup')"
        >
            
        <template #popup-content>
            <popup-item
            :toggle="vars.dlg.addItem.show"
            @baseItemChange="methods.addSelectedRows"
            />
        </template>
     </dx-popup>
     <dx-popup
      v-model:visible="vars.dlg.invoice.show"
      content-template="popup-content"
      :show-title="false" :show-close-button="false"
      :close-on-outside-click="false"
      :width="780" :height="620"
      :resize-enabled="true"
      @initialized="(evt) => vars.dlg.invoice.component = evt.component"
      @hiding="methods.refreshBarobillState()"
    >
      <template #popup-content>
        <ShipmentBillForm 
          :show="vars.dlg.invoice.show"
          :number="vars.dlg.invoice.number"
          :form-data="vars.dlg.invoice.data"
          :items="vars.dlg.invoice.items" 
          @close="vars.dlg.invoice.component && vars.dlg.invoice.component.hide()"
        />
      </template>
    </dx-popup>
    </div>
</template>

<script>
import moment from 'moment';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import DxTextArea from 'devextreme-vue/text-area';
import {
    DxForm,
    DxLabel,
    DxGroupItem,
    DxSimpleItem,
    DxEmptyItem,
    DxRequiredRule,
} from 'devextreme-vue/form';
import {
    DxSorting,
    DxDataGrid,
    DxColumn,
    DxEditing,
    DxSelection,
    DxFilterRow,
    DxPaging,
    DxLookup,
    DxScrolling,
    DxColumnChooser,
    DxToolbar as DxGridToolbar,
    DxItem as DxGridItem,
    DxButton as DxGridButton,
    DxSummary,
    DxTotalItem,
} from 'devextreme-vue/data-grid';

import PopupItem from '../../components/base/popup-item.vue';
import { DxTabPanel } from 'devextreme-vue/tab-panel';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxTextBox, DxButton as DxTextBoxButton } from 'devextreme-vue/text-box';
import { DxButton } from 'devextreme-vue/button';
import { DxFileUploader } from 'devextreme-vue/file-uploader';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import { confirm, alert } from 'devextreme/ui/dialog';
import { onMounted, ref, reactive, computed, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import stateStore from '@/utils/state-store';
import {
    baseEmployee,
    baseCodeLoader,
} from '../../data-source/base';
import DataGridAsReceipt from '../../components/as/data-as-receipt.vue';
import authService from '../../auth';
import { notifyInfo, notifyError } from '../../utils/notify';
import { currentDateTime } from '../../utils/util';
import { loadDepartment } from '../../utils/data-loader';
import { DxNumberBox } from 'devextreme-vue/number-box';
import { asResult, getAsResultItem, getAsResultAttachment, getAsResultExpense } from '../../data-source/as';
import DataGridProject from '../../components/project/data-project.vue';
import DataGridAsResult from '../../components/as/data-as-result.vue';
import ApiService from '../../utils/api-service';
import ShipmentBillForm from '../../components/shipment/bill.vue';

const BAROBILL_STATE = {
    1000 : '임시저장',
    2010 : '발급예정 승인대기',
    2011 : '발급예정 승인완료',
    2020 : '역발행요청 발급대기',
    3011 : '발급예정 발급완료',
    3021 : '역발행요청 발급완료',
    3014 : '발급완료',
    4012 : '발급예정 거부',
    4022 : '역발행요청 거부',
    5013 : '발급예정 승인 전 공급자에 의한 취소',
    5023 : '역발행요청 승인 전 공급받는자에 의한 취소',
    5031 : '발급예정 승인 후, 또는 발급완료 후 공급자에 의한 취소'
}
export default {
components: {
    DxToolbar,
    DxItem,
    DxTextArea,
    DxLoadPanel,
    DxForm,
    DxSelection,
    DxFilterRow,
    DxLabel,
    DxTextBox,
    DxTextBoxButton,
    DxButton,
    DxFileUploader,
    DxGroupItem,
    DxSimpleItem,
    DxEmptyItem,
    DxTabPanel,
    DxDataGrid,
    DxEditing,
    DxColumn,
    DxLookup,
    DxPopup,
    DxSorting,
    DxToolbarItem,
    DxScrolling,
    DxColumnChooser,
    DxPaging,
    DataGridAsReceipt,
    DxRequiredRule,
    DxGridToolbar,
    DxGridItem,
    PopupItem,
    DxNumberBox,
    DxGridButton,
    DataGridProject,
    DataGridAsResult,
    DxSummary,
    DxTotalItem,
    ShipmentBillForm,
},
props: {
    id: [String, Number],
},
setup(props) {

    const router = useRouter();
    const barobillService = new ApiService('/api/mes/v1/barobill');
    const vars = { dlg: {} };
    vars.init = ref(true);
    vars.loading = ref(false);
    vars.formState = reactive({ readOnly: true });
    vars.summary = reactive({
        item: {
            supply_price: 0,
            expense_amount: 0,
        },
    });
    vars.grid = {
        fk_project_management_id : null,
    };
    vars.dlg.finder = reactive({
        show: false,
        title: '',
        key: null,
        data: null,
    });
    vars.dlg.addItem = reactive({ show: false });
    vars.dlg.invoice = reactive({ component: null, show: false, data: null, number: null, items: null, state: null });
    vars.formData = reactive({
      id: null,
      created: null,
      result_number: '',
      result_date: '',
      result_department: '',
      result_manager: '',
      result_manager_check: '',
      result_detail: '',
      process_status: '',
      final_status: '',
      result_price: 0,
      fk_project_management_id: null,
      fk_as_receipt_id: null,
      fk_company_id: authService.getCompanyId(),
      project_management: null,
      as_receipt: null,
    });
    vars.filter = {};
    vars.filter.item = [{ name: 'fk_as_result_id', op: 'eq', val: props.id || 0 }];
    vars.dataSource = reactive({
      item: getAsResultItem(vars.filter.item),
      attachment: getAsResultAttachment(vars.filter.item),
      expense: getAsResultExpense(vars.filter.item),
      employee: [],
      process_status: [],
    });

    vars.attchFiles = reactive({})
    vars.disabled = reactive({
        edit: true,
        delete: true,
        save: true,
    });

    
    onMounted(async () => {
        await loadDepartment(vars.dataSource);
        await methods.loadBaseCode();
        methods.initById(props.id);
    
    });

    const methods = {
        async initById(id) {
          methods.gridItemRefresh(id);
          methods.gridAttachmentRefresh(id);
          methods.gridExpenseRefresh(id);
          if (!id) {
              methods.clearFormData();
              vars.disabled.edit = true;
              vars.disabled.delete = true;
              vars.disabled.save = true;
              return;
          }

          let { data } = await asResult.byKey(id);

          Object.assign(vars.formData, data);
          vars.formState.readOnly = true;
          vars.disabled.edit = false;
          methods.enableDelete();
          methods.enableSave();

          const {data: state} = await barobillService.get(`state/${vars.formData.result_number}`)

        
          vars.dlg.invoice.state = BAROBILL_STATE[state.data.BarobillState]
          console.log(`세금계산서 상태: ${state.data.BarobillState} [${BAROBILL_STATE[state.data.BarobillState]}]`)
        },
        async loadBaseCode() {
          await baseCodeLoader(['처리현황']).then(response => {
            vars.dataSource.process_status = response['처리현황'];

          });
        },
        gridItemRefresh(id) {
          vars.dataSource.item.defaultFilters = methods.setIdToGridFilter(vars.filter.item, id);
          if (vars.grid.item) {
            vars.grid.item.cancelEditData();
            vars.grid.item.refresh();
          }
        },
        gridAttachmentRefresh(id) {
          vars.dataSource.attachment.defaultFilters = methods.setIdToGridFilter(vars.filter.item, id);
          if (vars.grid.attachment) {
            vars.grid.attachment.cancelEditData();
            vars.grid.attachment.refresh();
          }
        },
        gridExpenseRefresh(id) {
          vars.dataSource.expense.defaultFilters = methods.setIdToGridFilter(vars.filter.item, id);
          if (vars.grid.expense) {
            vars.grid.expense.cancelEditData();
            vars.grid.expense.refresh();
          }
        },
        setIdToGridFilter(filter, id) {
          if (!id) { id = 0; }
          filter[0].val = id;
          return filter;
        },
        clearFormData() {
            vars.formData.id = null;
            vars.formData.created = null;
            vars.formData.result_number = '';
            vars.formData.result_date = '';
            vars.formData.result_department = '';
            vars.formData.result_manager = '';
            vars.formData.result_manager_check = '';
            vars.formData.result_detail = '';
            vars.formData.process_status = '';
            vars.formData.final_status = '';
            vars.formData.result_price = 0;
            vars.formData.fk_as_receipt_id = null;
            vars.formData.fk_project_management_id = null;
            vars.formData.fk_company_id = authService.getCompanyId();
            vars.formData.project_management = null;
            vars.formData.as_receipt = null;
            vars.formData.project_management = null;
            vars.formData.fk_company_id = authService.getCompanyId();
        },
        generateItemButtonOption(
            icon,
            callback,
            location = 'after',
            options = {}
        ) {
            let buttonOptions = { stylingMode: 'text', icon, onClick: callback };
            return {
                ...options,
                buttons: [{ name: icon, location, options: buttonOptions }],
            };
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
        onGridInitialized(evt, key) {
            vars.grid[key] = evt.component;
            stateStore.bind(`as-result-${key}`, evt.component);
        },
        async newItem() { 
          methods.gridItemRefresh();
          methods.gridAttachmentRefresh();
          methods.gridExpenseRefresh();
          if (vars.formData.id) {
              methods.clearFormData();
              methods.redirect();
          }
          setTimeout(() => {
              methods.clearFormData();
              methods.setFormData();
          }, 200);
        },

        setFormData(){
            vars.formData.result_department = authService.getDepartmentName();
            vars.formData.result_manager = authService.getUserName();
            vars.formData.result_date = currentDateTime();
            vars.formData.fk_company_id = authService.getCompanyId();
            vars.formState.readOnly = false;
        },
        async editItem() {
            if (!vars.formData.id) return;

            const saveFormData = Object.assign({}, vars.formData);
            vars.formState.readOnly = !vars.formState.readOnly;

            methods.enableSave();
            methods.enableDelete();

            await nextTick();
            Object.assign(vars.formData, saveFormData);
        },
        showAddPopup() {
            vars.dlg.addItem.show = true;
        },
        async addSelectedRows(rows) {
            const grid = vars.grid.item;
            await grid.pageIndex(0);
            const firstRowKey = grid.getKeyByRowIndex(0);
            if (firstRowKey) {
            await grid.navigateToRow(firstRowKey);
            }

            for (let row of rows) {
                await grid.addRow();
                const data = await grid.byKey(grid.getKeyByRowIndex(0));
                data.item_quantity = 0; // 수량
                data.unit_price = Number(row.purchase_price); // 단가
                data.supply_price = 0,
                data.item_code = row.item_code; // 품목코드
                data.item = { ...row }; // 품목
            }
            vars.dlg.addItem.show = false;
        },
        finderReturnHandler(data) {
            switch (vars.dlg.finder.key) {
              case 'project': {
                  vars.formData.project_management = data;
                  vars.formData.fk_project_management_id = data.id;
                  break;
              }
              case 'receipt_number': {
                  vars.formData.fk_as_receipt_id = data.id;
                  vars.formData.as_receipt = data;
                  vars.formData.fk_project_management_id = data.project_management?.id || null;
                  vars.formData.project_management = data.project_management || null;
                  break;
              }
              case 'result_number': {
                  methods.redirect(data.id);
                  break;
              }
            }

            vars.dlg.finder.show = false;
            vars.dlg.finder.title = '';
            vars.dlg.finder.key = null;
            vars.dlg.finder.data = null;
        },
        async saveItem() {
            let isSelect = await confirm('저장하시겠습니까?', '저장');
            if (!isSelect) {
              return;
            }
            vars.loading.value = true;
            try {
            
            if (vars.formData.id) {       
                const updateDate = Object.assign({}, vars.formData);
                delete updateDate.id;
                delete updateDate.created;
                delete updateDate.result_number;
                delete updateDate.project_management;
                delete updateDate.as_receipt;
              console.log("updateDate : ", updateDate)
                const { data } = await asResult.update(
                  vars.formData.id,
                  updateDate
                );
                                            
                vars.formData.result_number = data.result_number;
                vars.formData.as_receipt = data.as_receipt;
                vars.formData.project_management = data.project_management;

                if (vars.grid.item && vars.grid.item.hasEditData()) {
                  await vars.grid.item.saveEditData();
                }
                if (vars.grid.attachment && vars.grid.attachment.hasEditData()) {
                  await vars.grid.attachment.saveEditData();
                }
                if (vars.grid.expense && vars.grid.expense.hasEditData()) {
                  await vars.grid.expense.saveEditData();
                }

                vars.formState.readOnly = true;

                notifyInfo('저장되었습니다');
                methods.enableSave();
                methods.enableDelete();

            } else {
                delete vars.formData.created;
                delete vars.formData.id;
                delete vars.formData.project_management;
                delete vars.formData.as_receipt;
                let { data } = await asResult.insert(vars.formData);
                vars.formData.id = data.id;
                vars.formData.as_receipt = data.as_receipt;
                vars.formData.project_management = data.project_management;

                                
                if (vars.grid.item && vars.grid.item.hasEditData()) {
                  await vars.grid.item.saveEditData();
                }
                if (vars.grid.attachment && vars.grid.attachment.hasEditData()) {
                  await vars.grid.attachment.saveEditData();
                }
                if (vars.grid.expense && vars.grid.expense.hasEditData()) {
                  await vars.grid.expense.saveEditData();
                }
                notifyInfo('저장되었습니다');
                methods.redirect(data.id);
                vars.formState.readOnly = true;
            }
            } catch (ex) {
              console.error(ex);
              notifyError('저장 할 내용이 없습니다');
    
            } finally {
            vars.loading.value = false;
            }

        },
        selectDepartment(e) {
            const selectItem = e.component.option('selectedItem');
            if (selectItem) {
              baseEmployee
                  .load({
                    filter: [
                        ['fk_company_id', '=', authService._user.fk_company_id],
                        ['fk_department_id', '=', selectItem.id],
                    ],
                    skip: 0,
                    take: 1000,
                  })
                  .then(({ data }) => {
                    vars.dataSource.employee = data;
                  });
            }else{
              vars.dataSource.employee = [];
            }
        },
        async deleteItem() {
            if (!vars.formData.id) {
            return;
            }

            const result = await confirm(
            '이 항목을 삭제하시겠습니까?',
            '삭제 확인'
            );
            try{
            if (result) {
                await asResult.remove(vars.formData.id);
                await alert('삭제되었습니다', '삭제 확인');
                methods.redirect();
                methods.gridItemRefresh();
                methods.gridAttachmentRefresh();
                methods.gridExpenseRefresh();
                vars.formState.readOnly = true;
            }
            }
            catch(ex){
            console.error(ex);
            notifyError('연결된 데이터가 있어서 삭제가 안됩니다');
            }
        
        },
        redirect(id) {
            if (id) router.replace({ path: `/as/result/${id}` });
            else router.replace({ path: `/as/result` });
        },
        onValueChanged(e) {
            if (!e.value) {
                vars.disabled.save = true;
            } else {
                if(methods.isFilledFormRequiredData()){
                    methods.enableSave();
                }
            }
        },
        calcSummaryItem(options) {
            if (options.name === 'supply_price') {
                if (options.summaryProcess === 'start') {
                    options.totalValue = 0;
                } else if (options.summaryProcess === 'calculate') {
                    options.totalValue += Number(options.value.supply_price);
                } else if (options.summaryProcess === 'finalize') {
                    vars.summary.item.supply_price = options.totalValue;
                    vars.formData.result_price = vars.summary.item.supply_price + vars.summary.item.expense_amount;
                }
            }
            if (options.name === 'expense_amount') {
                if (options.summaryProcess === 'start') {
                    options.totalValue = 0;
                } else if (options.summaryProcess === 'calculate') {
                    options.totalValue += Number(options.value.expense_amount);
                } else if (options.summaryProcess === 'finalize') {
                    vars.summary.item.expense_amount = options.totalValue;
                    vars.formData.result_price = vars.summary.item.supply_price + vars.summary.item.expense_amount;
                }
            }
        },
        isFilledFormRequiredData(){
            if(vars.formData.result_department && vars.formData.result_manager){
            return true;
            }
            return false;
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
        onDataError(e) {
            console.log("e : ", e)
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
        async refreshBarobillState () {
          if (!vars.formData.result_number) return
          console.info('세금계산서 상태 업데이트 (부모 페이지)')
          const {data: state} = await barobillService.get(`state/${vars.formData.result_number}`)

          vars.dlg.invoice.state = BAROBILL_STATE[state.data.BarobillState]
          console.log(`세금계산서 상태: ${state.data.BarobillState} [${BAROBILL_STATE[state.data.BarobillState]}]`)
        },
        onSavingItem(e) {
          e.changes.forEach((element) => {
            if (element.type != 'remove') {
                element.data.fk_as_result_id = vars.formData.id;
                delete element.data.item;
            }
            });
        },
        async onAttchmentRowRemoving(e) {
            const apiService = new ApiService('/api/server/v1/as-result-attachment');
            return await apiService.post(`remove/${e.data.id}`) 
        },
        onSavingAttachment(e) {
          e.promise = methods.onSavingAttachmentImpl(e);
        },
        async onSavingAttachmentImpl(e) {
            for(const element of e.changes){
                if(element.type != 'remove'){
                    element.data.fk_as_result_id = vars.formData.id;
                    await methods.updateUploadAttachment(element);
                }
            }
        },
        async updateUploadAttachment(element) {
            const uploadService = new ApiService('/api/mes/v1/file-manager')
            for(const key in element.data){
                if(vars.attchFiles[element.data[key]]){
                    const fd = new FormData();
                    fd.append('file', vars.attchFiles[element.data[key]], vars.attchFiles[element.data[key]].name);
                    fd.append('path', 'as-result-attachment')
                    const {data: filename} = await uploadService.post('upload', fd);
                    element.data['file_path'] = `as-result-attachment/${filename}`;
                    delete vars.attchFiles[element.data[key]];
                }
            }
        },
        setQuantity(newData, value, currentRowData) {
            newData.item_quantity = value;
            newData.supply_price = value * currentRowData.unit_price;
        },
        setUnitPrice(newData, value, currentRowData) {
            newData.unit_price = value;
            newData.supply_price = value * currentRowData.item_quantity;
        },
        async addItemRowButton(item){
            const grid = vars.grid[item];
            if(grid){
            await grid.addRow();
            }
        },
        async itemSaveButton(item){
            if(!vars.formData.id) return;
            const grid = vars.grid[item];
            if(grid && grid.hasEditData()){
            await grid.saveEditData();
            }
        },
        addFile(){
            const f = document.createElement('input');
            f.type = 'file';
            f.style.position = 'absolute';
            f.style.left = '-9999px';
            f.style.opacity = '0';
            f.style.width = '0';
            f.style.height = '0';
            f.style.overflow = 'hidden';
                    
            f.onchange = async () => {
                if(f.files[0]){
                    vars.attchFiles[f.files[0].name] = f.files[0];
                    vars.grid.attachment.addRow();
                    const data = await vars.grid.attachment.byKey(vars.grid.attachment.getKeyByRowIndex(0));
                    data.file_name = f.files[0].name;
                }
                f.onchange = undefined;
                f.remove();
            }
            document.body.appendChild(f);
            f.click();
        },
        downloadFile(data){
            if (data.data['file_path'] && data.data['file_name']) {
                const file_path = data.data['file_path'];
                const file_name = data.data['file_name'];
                location.href = `/api/mes/v1/file-manager/download/${file_path}/${file_name}`;
            }else {
                notifyError('첨부파일이 아직 저장되지 않았습니다');
            }
        },
        initNewRow(e, item){
            if(item === 'expense'){
                e.data.expense_date = currentDateTime();
                e.data.register = authService.getUserName();
                e.data.expense_amount = 0;
            }
        },

        async exportInvoice () {
            if (!vars.formData.id) return
            const {data: item} = await vars.dataSource.item.load();
            for (let ele of item) {
              ele.statement_item = ele.item_name;
            }
            const {data: expense } = await vars.dataSource.expense.load();
            for (let ele of expense) {
              ele.statement_item = ele.expense_description;
              ele.supply_price = ele.expense_amount;
            }
            const formData = {...vars.formData};
            formData.vat_type = '별도';
            formData.approval_type = '청구';
            formData.sales_number = formData.result_number;
            formData.sales_date = formData.result_date;
            formData.client_company = formData.as_receipt.order_company;
            vars.dlg.invoice.data = formData;
            vars.dlg.invoice.items = [...item, ...expense];
            vars.dlg.invoice.number = formData.result_number;
            vars.dlg.invoice.show = true;
        },

      };
  
      watch(
        () => props.id,
        () => methods.initById(props.id)
      );
  
      return {
        vars,
        methods,
      };
    },
  };
  </script>
  
  <style lang="scss" >
  .vat-data-box{
    // border: 1px dashed #ddd;
    // border-radius: 15px;
    // padding: 3px;
    // margin-top: 3px;
  
  }
  .dx-fileuploader-wrapper {
    padding: 0px;
    margin: 0px;
  }
  .dx-fileuploader-input-wrapper {
    padding: 0px;
    margin: 0px;
  }
  .company_name{
    color:rgb(156, 50, 32); 
    
  }
  .company_name:hover{
    color: red;
    text-decoration: underline;
    cursor: pointer;
  }
    
  </style>
  
<style lang="scss" scoped>
.barobill-state {
  padding: 6px 20px;
  border-radius: 4px;
  border: 1px solid #d7d7d7;
  box-shadow: inset 0px 1px 3px 0px #38530d6b;
  background-color: #e3ffb8;
  color: #5c8816;
}
</style>