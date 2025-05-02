<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">매출계산서</div>
            </dx-item>
            <dx-item location="after">
              <div class="barobill-state" v-if="vars.dlg.invoice.state">{{ vars.dlg.invoice.state }}</div>
            </dx-item>
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{ text: '전자세금계산서발행', type: 'copy', icon: 'paste', onClick: methods.exportInvoice }"
            />
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
                data-field="sales_number"
                :editor-options="{
                  placeholder: '(자동 or 직접입력)',
                  ...generateItemButtonOption('search', methods.createFindPopupFn('sales', '계산서조회')),
                }"
              >
                <dx-label text="계산서번호" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="sales_date" editor-type="dxDateBox"
                :editor-options="{ dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss', ...vars.formState }"
              >
                <dx-label text="발행일자" :show-colon="false" />
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
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="sales_department" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.department,
                  displayExpr: 'department_name',
                  valueExpr: 'department_name',
                  acceptCustomValue: true,
                  onValueChanged: methods.onDepartmentChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="매출부서" :show-colon="false" />
                <dx-required-rule message="매출부서를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="sales_manager" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.employee,
                  displayExpr: 'emp_name',
                  valueExpr: 'emp_name',
                  disabled: vars.disabled.manager,
                  ...vars.formState,
                }"
              >
                <dx-label text="매출담당자" :show-colon="false" />
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
              <dx-simple-item data-field="vat_adjustment" editor-type="dxNumberBox" 
                :editor-options="{ 
                  format: '₩,##0',
                  onValueChanged: methods.onVatAdjustmentChanged,
                  ...vars.formState 
                }"
              >
                <dx-label text="부가세보정" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="sales_type" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.sales_type,
                  displayExpr: 'code_name',
                  valueExpr: 'code_name',
                  ...vars.formState,
                }"
              >
                <dx-label text="계산서유형" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="approval_type" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.approval_type,
                  displayExpr: 'code_name',
                  valueExpr: 'code_name',
                  onValueChanged: methods.onVatTypeChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="결재유형" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="publish_type" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.publish_type,
                  displayExpr: 'code_name',
                  valueExpr: 'code_name',
                  acceptCustomValue: true,
                  ...vars.formState,
                }"
              >
                <dx-label text="발행구분" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="office_type" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.office_type,
                  displayExpr: 'code_name',
                  valueExpr: 'code_name',
                  acceptCustomValue: true,
                  ...vars.formState,
                }"
              >
                <dx-label text="본지점구분" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="etc" editor-type="dxTextArea"
                :editor-options="{
                  ...generateItemButtonOption('rename', methods.createFindPopupFn('etc', '비고', vars.formData.etc)),
                  ...vars.formState,
                  height: '130px',
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
              <dx-item template="addFromProject" location="before" :visible="vars.isAllowEdit.value" />
              <dx-item template="addFromRelease" location="before" :visible="vars.isAllowEdit.value" />
              <dx-item template="addFromReleaseReturn" location="before" :visible="vars.isAllowEdit.value" />
              <dx-grid-item name="addRowButton" :options="{ onClick: methods.showAddPopup }" />
              <dx-grid-item name="saveButton" :visible="false" />
              <dx-grid-item name="revertButton" />
              <dx-grid-item name="columnChooserButton" />
            </dx-grid-toolbar>
            <template #addFromProject>
              <dx-button text="프로젝트에서 가져오기" icon="add" @click="methods.showAddProjectPopup" />
            </template>
            <template #addFromRelease>
              <dx-button text="출고에서 가져오기" icon="add" @click="methods.showAddReleasePopup" />
            </template>
            <template #addFromReleaseReturn>
              <dx-button text="출고반품에서 가져오기" icon="add" @click="methods.showAddReleaseReturnPopup" />
            </template>
            <dx-column caption="프로젝트번호" data-field="project_management.project_number" :allow-editing="false" />
            <dx-column caption="계산서품목" data-field="statement_item" width="180" :allow-editing="true" />
            <dx-column caption="품목코드" data-field="item_code" width="180" :allow-editing="false" />
            <dx-column caption="품명" data-field="item.item_name" :allow-editing="false" />
            <dx-column caption="규격" data-field="item.item_standard" :allow-editing="false" />
            <dx-column caption="수량" data-field="quantity" data-type="number" format="fixedPoint" :set-cell-value="methods.setQuantity" />
            <dx-column caption="단가" data-field="unit_price" data-type="number" format="currency" :set-cell-value="methods.setUnitPrice" />
            <dx-column caption="부가세" data-field="vat" data-type="number" format="currency" :allow-editing="false" />
            <dx-column caption="공급가" data-field="supply_price" data-type="number" format="currency" :allow-editing="false" />
            <dx-column caption="금액" data-field="total_price" data-type="number" format="currency" :allow-editing="false" />
            <dx-column caption="단위" data-field="item.unit" :allow-editing="false" />
            <dx-column caption="추가설명" data-field="note" />
            <dx-column caption="출고번호" data-field="release_number" width="180" :allow-editing="false" />
            <dx-column caption="출고반품번호" data-field="release_return_number" width="180" :allow-editing="false" />
            <dx-column caption="출고품목아이디" data-field="fk_release_item_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
            <dx-column caption="출고반품품목아이디" data-field="fk_release_return_item_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
            <dx-column caption="프로젝트아이디" data-field="fk_project_management_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />

            <dx-summary :recalculate-while-editing="true" :calculate-custom-summary="methods.calculateCustomSummary">
              <dx-total-item name="supply_price" summary-type="custom" />
            </dx-summary>

            <dx-scrolling mode="standard" />
            <dx-column-chooser mode="select" :enabled="true" />
            <dx-editing mode="batch"
              :allow-adding="vars.isAllowEdit.value"
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

          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick" />
        </dx-data-grid>
      </template>
    </dx-popup>

    <dx-popup
      title="프로젝트찾기"  
      content-template="popup-content"
      v-model:visible="vars.dlg.addProjectItem.show"
      width="70%"
      :height="460"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'find-project-popup')"
    >
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ text: '선택된 항목 추가', icon: 'add', onClick: methods.addSelectedProjectRows }"
      />

      <template #popup-content>
        <dx-scroll-view width="100%" height="100%">
          <dx-data-grid
            column-resizing-mode="widget"
            :show-borders="true"
            :column-auto-width="true"
            :remote-operations="true"
            :filter-sync-enabled="true"
            :allow-column-resizing="true"
            :allow-column-reordering="true"
            :data-source="vars.dataSource.projectItem"
            :on-initialized="evt => methods.onGridInitialized(evt, 'projectItem')"
            @selection-changed="methods.onSelectionChangeProject"
          >
            <dx-column caption="프로젝트번호" data-field="project_number" data-type="string" :sort-index="1" sort-order="desc" />
            <dx-column caption="프로젝트명" data-field="project_name" data-type="string" />
            <dx-column caption="계약일자" data-field="contract_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" :width="150" />
            <dx-column caption="고객업체" data-field="order_company" data-type="string" />
            <dx-column caption="계약금액" data-field="company_amount" data-type="number" :format="{ type: 'fixedPoint' }" />
            <dx-column caption="미계산서금액" data-field="non_invoice" data-type="number" format="fixedPoint" />
            <dx-paging :page-size="20" />
            <dx-sorting mode="multiple" />
            <dx-filter-row :visible="true" />
            <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick" />
          </dx-data-grid>

          <div class="mt-2">
            <table class="summary-table">
              <tr>
                <th>선택한 프로젝트 합계금액:</th>
                <td>{{ vars.dlg.addProjectItem.selection_price }}</td>
                <th>총 프로젝트 합계금액:</th>
                <td>{{ vars.dlg.addProjectItem.total_price }}</td>
              </tr>
            </table>
          </div>
        </dx-scroll-view>
      </template>
    </dx-popup>

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
        <dx-scroll-view width="100%" height="100%">
          <dx-data-grid
            column-resizing-mode="widget"
            :show-borders="true"
            :column-auto-width="true"
            :remote-operations="true"
            :filter-sync-enabled="true"
            :allow-column-resizing="true"
            :allow-column-reordering="true"
            :data-source="vars.dataSource.releaseItem"
            :on-initialized="evt => methods.onGridInitialized(evt, 'releaseItem')"
            @selection-changed="methods.onSelectionChangeRelease"
          >
            <dx-column caption="고객업체" data-field="release.client_company" data-type="string" />
            <dx-column caption="출고번호" data-field="release.release_number" data-type="string" :sort-index="1" sort-order="desc" />
            <dx-column caption="출고일자" data-field="release.release_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" :width="150" />
            <dx-column caption="품목코드" data-field="item_code" data-type="string" />
            <dx-column caption="품명" data-field="item.item_name" data-type="string" />
            <dx-column caption="규격" data-field="item.item_standard" data-type="string" />
            <dx-column caption="출고수량" data-field="release_quantity" data-type="number" format="fixedPoint" />
            <dx-column caption="단가" data-field="unit_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
            <dx-column caption="미계산서수량" data-field="non_invoice" data-type="number" format="fixedPoint" />
            <dx-column caption="합계금액" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :calculate-cell-value="(row) => row.release_quantity * row.unit_price" />
            <dx-column caption="참고" data-field="note" data-type="string" />

            <dx-paging :page-size="20" />
            <dx-sorting mode="multiple" />
            <dx-filter-row :visible="true" />
            <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick" />
          </dx-data-grid>

          <div class="mt-2">
            <table class="summary-table">
              <tr>
                <th>선택한 출고품목 합계금액:</th>
                <td>{{ vars.dlg.addReleaseItem.selection_price }}</td>
                <th>총 출고품목 합계금액:</th>
                <td>{{ vars.dlg.addReleaseItem.total_price }}</td>
              </tr>
            </table>
          </div>
        </dx-scroll-view>
      </template>
    </dx-popup>

    <dx-popup
      title="출고반품품목찾기"  
      content-template="popup-content"
      v-model:visible="vars.dlg.addReleaseReturnItem.show"
      width="70%"
      :height="460"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'find-release-return-popup')"
    >
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ text: '선택된 항목 추가', icon: 'add', onClick: methods.addSelectedReleaseReturnRows }"
      />

      <template #popup-content>
        <dx-scroll-view width="100%" height="100%">
          <dx-data-grid
             column-resizing-mode="widget"
            :show-borders="true"
            :column-auto-width="true"
            :remote-operations="true"
            :filter-sync-enabled="true"
            :allow-column-resizing="true"
            :allow-column-reordering="true"
            :data-source="vars.dataSource.releaseReturnItem"
            :on-initialized="evt => methods.onGridInitialized(evt, 'releaseReturnItem')"
            @selection-changed="methods.onSelectionChangeReleaseReturn"
          >
            <dx-column caption="고객업체" data-field="release_return.client_company" data-type="string" />
            <dx-column caption="반품번호" data-field="release_return.return_number" data-type="string" :sort-index="1" sort-order="desc" />
            <dx-column caption="반품일자" data-field="release_return.return_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" :width="150" :selected-filter-operation="'between'" :filter-value="vars.filterRow.date" />
            <dx-column caption="품목코드" data-field="item_code" data-type="string" />
            <dx-column caption="품명" data-field="item.item_name" data-type="string" />
            <dx-column caption="규격" data-field="item.item_standard" data-type="string" />
            <dx-column caption="반품수량" data-field="return_quantity" data-type="number" format="fixedPoint" />
            <dx-column caption="단가" data-field="unit_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
            <dx-column caption="미계산서수량" data-field="non_invoice" data-type="number" format="fixedPoint" />
            <dx-column caption="합계금액" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :calculate-cell-value="(row) => row.return_quantity * row.unit_price" />
            <dx-column caption="반품사유" data-field="return_reason" data-type="string" />

            <dx-paging :page-size="20" />
            <dx-sorting mode="multiple" />
            <dx-filter-row :visible="true" />
            <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick" />
          </dx-data-grid>

          <div class="mt-2">
            <table class="summary-table">
              <tr>
                <th>선택한 출고반품품목 합계금액:</th>
                <td>{{ vars.dlg.addReleaseReturnItem.selection_price }}</td>
                <th>총 출고반품품목 합계금액:</th>
                <td>{{ vars.dlg.addReleaseReturnItem.total_price }}</td>
              </tr>
            </table>
          </div>
        </dx-scroll-view>
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
        <data-grid-client v-if="vars.dlg.finder.key === 'client'" @change="methods.finderReturnHandler" />
        <data-grid-client v-else-if="vars.dlg.finder.key === 'enduser'" @change="methods.finderReturnHandler" />
        <data-grid-sales v-else-if="vars.dlg.finder.key === 'sales'" @change="methods.finderReturnHandler" />
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
import numeral from 'numeral';

import { useRouter } from 'vue-router';
import { ref, reactive, computed, watch, nextTick, onMounted } from 'vue';

import { DxButton } from 'devextreme-vue/button';
import DxTextArea from 'devextreme-vue/text-area';
import { confirm, alert } from 'devextreme/ui/dialog';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import { DxScrollView } from 'devextreme-vue/scroll-view';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxCustomRule, DxRequiredRule } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxLookup, DxPaging, DxEditing, DxSorting, DxSummary, DxTotalItem, DxSelection, DxFilterRow,
  DxScrolling, DxColumnChooser, DxItem as DxGridItem, DxToolbar as DxGridToolbar, DxButton as DxGridButton } from 'devextreme-vue/data-grid';

import { getStock } from '../../data-source/setup';
import { baseItem, baseClient, baseCodeLoader, getBaseItem } from '../../data-source/base';
import { getShipmentReleaseItem, getShipmentReleaseReturnItem, getShipmentSalesStatementItem, shipmentSalesStatement } from '../../data-source/shipment';
import { getProjectRegistration } from '../../data-source/project';

import DataGridClient from '../../components/base/data-client.vue';
import DataGridSales from '../../components/shipment/data-sales.vue';
import DataGridProject from '../../components/project/data-project.vue';

import authService from '../../auth';
import stateStore from '@/utils/state-store';
import { calcPriceSummary, generateItemButtonOption, beforeExitConfirm } from '../../utils/util';
import { loadEmployee, loadDepartment, loadClientManager } from '../../utils/data-loader';
import { notifyInfo, notifyError } from '../../utils/notify';
import PopupItemDetail from '@/components/base/popup-item-detail';
import ShipmentBillForm from '@/components/shipment/bill.vue'
import ApiService from '@/utils/api-service'

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
    DxButton,
    DxTextArea,
    DxLoadPanel,
    DxScrollView,
    DxToolbar, DxItem,
    DxPopup, DxToolbarItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxCustomRule, DxRequiredRule,
    DxDataGrid, DxColumn, DxLookup, DxPaging, DxEditing, DxSorting, DxSummary, DxTotalItem, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, 
    DxGridItem, DxGridToolbar, DxGridButton,
    DataGridClient, DataGridSales, DataGridProject,
    PopupItemDetail,
    ShipmentBillForm,
  },
  props: {
    id: [String, Number],
  },
  setup(props) {
    // variable 설정
    const router = useRouter();
    const barobillService = new ApiService('/api/mes/v1/barobill')
    const vars = { dlg: {} };
    vars.init = ref(false);
    vars.loading = ref(false);
    vars.formState = reactive({ readOnly: true });
    vars.grid = { releaseItem: null, releaseReturnItem: null, item1: null, projectItem: null };
    vars.dlg.addItem = reactive({ show: false });
    vars.dlg.addReleaseItem = reactive({ show: false, total_price: '0', selection_price: '0' });
    vars.dlg.addReleaseReturnItem = reactive({ show: false, total_price: '0', selection_price: '0' });
    vars.dlg.addProjectItem = reactive({ show: false, total_price: '0', selection_price: '0' });
    vars.dlg.finder = reactive({
      show: false,
      title: '',
      key: null,
      data: null,
    });
    vars.dlg.invoice = reactive({ component: null, show: false, data: null, number: null, items: null, state: null });
    vars.filter = {
      baseItem: {
        clientId: null,
      },
      releaseItem: {
        clientCompany: null,
      },
      releaseReturnItem: {
        clientCompany: null,
      },
      projectItem: {
        clientCompany: null,
      },
      item1: [{ name: 'fk_sales_id', op: 'eq', val: props.id || 0 }],
    };
    vars.filterRow = reactive({
      date: []
    });
    vars.disabled = reactive({
      edit: true,
      delete: true,
      new: false,
      save: true,
      items: true,
      manger: true,
    });
    vars.dataSource = reactive({
      payment_terms: [],
      release_type: [],
      vat_type: [],
      delivery_place: [],
      client_manager: [],
      department: [],
      employee: [],
      publish_type: [],
      sales_type: [],
      approval_type: [],
      office_type: [],
      baseItem: null,
      releaseItem: null,
      releaseReturnItem: null,
      projectItem: null,
      item1: getShipmentSalesStatementItem(vars.filter.item1),
    });
    vars.formData = reactive({});

    vars.summary = {};
    vars.summary.supply_price = computed(() => '₩' + numeral(vars.formData.supply_price).format('0,0'));
    vars.summary.vat = computed(() => '₩' + numeral(vars.formData.vat).format('0,0'));
    vars.summary.total_price = computed(() => '₩' + numeral(vars.formData.total_price).format('0,0'));
    
    vars.itemDetail = reactive({ visible: false, id: 0 });

    vars.isAllowEdit = computed(() => {
      return !vars.formState.readOnly && !!vars.formData.client_company
    })

    onMounted(async () => {
      await loadDepartment(vars.dataSource);
      await methods.loadBaseCode();
      methods.loadBaseItem();
      methods.initById(props.id);

      const date = new Date();
      const y = date.getFullYear();
      const m = date.getMonth();
      const firstDay = new Date(y, m, 1);
      const lastDay = new Date(y, m + 1, 0);
      vars.filterRow.date.push(firstDay, lastDay);
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
          return;
        }

        let { data } = await shipmentSalesStatement.byKey(id);
        Object.assign(vars.formData, data);

        methods.enableDelete();
        vars.disabled.edit = false;
        if (vars.formData.client_company && vars.formData.sales_department) {
          methods.enableSave();
          vars.disabled.items = false;
        }
        methods.onClientChanged();

        console.info('세금계산서 상태 업데이트 (부모 페이지)')
        const {data: state} = await barobillService.get(`state/${vars.formData.sales_number}`)
        
        vars.dlg.invoice.state = BAROBILL_STATE[state.data.BarobillState]
        console.log(`세금계산서 상태: ${state.data.BarobillState} [${BAROBILL_STATE[state.data.BarobillState]}]`)
      },
      clearFormData() {
        vars.dlg.invoice.state = ''
        vars.formData.id = null;
        vars.formData.created = null;
        vars.formData.sales_number = '';
        vars.formData.sales_date = '';
        vars.formData.client_company = '';
        vars.formData.client_manager = '';
        vars.formData.sales_department = '';
        vars.formData.sales_manager = '';
        vars.formData.vat_type = '';
        vars.formData.etc = '';
        vars.formData.supply_price = 0;
        vars.formData.vat = 0;
        vars.formData.vat_adjustment = 0;
        vars.formData.total_price = 0;
        vars.formData.not_deposit = 0;
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
          await grid.addRow();
          grid.cellValue(0, 'statement_item', row.item_name); // 계산서품목
          grid.cellValue(0, 'item_code', row.item_code); // 품목코드
          grid.cellValue(0, 'item.item_name', row.item_name); // 품명
          grid.cellValue(0, 'item.item_standard', row.item_standard); // 규격
          grid.cellValue(0, 'quantity', 0); // 수량
          grid.cellValue(0, 'unit_price', row.sales_price); // 단가
          grid.cellValue(0, 'item.unit', row.unit); // 단위
          grid.cellValue(0, 'vat', 0); // 부가세
          grid.cellValue(0, 'supply_price', 0); // 공급가
          grid.cellValue(0, 'total_price', 0); // 금액
          grid.cellValue(0, 'not_deposit', 0); // 미입금
          grid.cellValue(0, 'note', ''); // 추가설명
          grid.cellValue(0, 'release_number', null); // 출고번호
          grid.cellValue(0, 'fk_project_management_id', null); // 프로젝트 아이디
          grid.cellValue(0, 'fk_sales_id', vars.formData.id); // 계산서 아이디
          grid.cellValue(0, 'fk_release_item_id', null); // 출고 품목 아이디
          grid.cellValue(0, 'fk_release_return_item_id', null); // 출고반품 품목 아이디
        }
        grid.refresh();
        vars.dlg.addItem.show = false;
      },
      async addSelectedProjectRows() {
        const grid = vars.grid.item1;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }
        const rows = await vars.grid.projectItem.getSelectedRowsData();
        for (let row of rows) {
          console.log("row : ", row)
          const response = calcPriceSummary(vars.formData.vat_type, row.non_invoice);
          await grid.addRow();
          grid.cellValue(0, 'statement_item', row.project_name); // 계산서품목
          grid.cellValue(0, 'item_code', '-'); // 품목코드
          grid.cellValue(0, 'quantity', 1)
          grid.cellValue(0, 'unit_price', row.non_invoice)
          grid.cellValue(0, 'vat', response.vat)
          grid.cellValue(0, 'supply_price', response.supply_price)
          grid.cellValue(0, 'total_price', response.total_price)
          grid.cellValue(0, 'not_deposit', response.total_price)
          grid.cellValue(0, 'note', row.note)
          grid.cellValue(0, 'release_number', null)
          grid.cellValue(0, 'fk_project_management_id', row.id)
          grid.cellValue(0, 'project_management.project_number', row.project_number)
          grid.cellValue(0, 'fk_sales_id', vars.formData.id)
          grid.cellValue(0, 'fk_release_item_id', null)
          grid.cellValue(0, 'fk_release_return_item_id', null)
        }
        grid.refresh();
        vars.dlg.addProjectItem.show = false;
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
          const response = calcPriceSummary(vars.formData.vat_type, row.non_invoice * row.unit_price);

          await grid.addRow();
          grid.cellValue(0, 'statement_item', row.item_name); // 계산서품목
          grid.cellValue(0, 'item_code', row.item_code); // 품목코드
          grid.cellValue(0, 'item.item_name', row.item.item_name); // 품명
          grid.cellValue(0, 'item.item_standard', row.item.item_standard); // 규격
          grid.cellValue(0, 'quantity', row.non_invoice); // 수량
          grid.cellValue(0, 'unit_price', row.unit_price); // 단가
          grid.cellValue(0, 'item.unit', row.item.unit); // 단위
          grid.cellValue(0, 'vat', response.vat); // 부가세
          grid.cellValue(0, 'supply_price', response.supply_price); // 공급가
          grid.cellValue(0, 'total_price', response.total_price); // 금액
          grid.cellValue(0, 'not_deposit', response.total_price); // 미입금
          grid.cellValue(0, 'note', row.note); // 추가설명
          grid.cellValue(0, 'release_number', row.release.release_number); // 출고번호
          grid.cellValue(0, 'fk_project_management_id', row.fk_project_management_id); // 프로젝트번호
          grid.cellValue(0, 'project_management.project_number', row.project_management ? row.project_management : null); // 프로젝트번호
          grid.cellValue(0, 'fk_sales_id', vars.formData.id); // 계산서 아이디
          grid.cellValue(0, 'fk_release_item_id', row.id); // 출고 품목 아이디
          grid.cellValue(0, 'fk_release_return_item_id', null); // 출고반품 품목 아이디
        }
        grid.refresh();
        vars.dlg.addReleaseItem.show = false;
      },
      async addSelectedReleaseReturnRows() {
        const grid = vars.grid.item1;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        const rows = await vars.grid.releaseReturnItem.getSelectedRowsData();
        for (let row of rows) {
          const response = calcPriceSummary(vars.formData.vat_type, row.non_invoice * row.unit_price);

          await grid.addRow();
          grid.cellValue(0, 'statement_item', row.item_name); // 계산서품목
          grid.cellValue(0, 'item_code', row.item_code); // 품목코드
          grid.cellValue(0, 'item.item_name', row.item.item_name); // 품명
          grid.cellValue(0, 'item.item_standard', row.item.item_standard); // 규격
          grid.cellValue(0, 'quantity', row.non_invoice); // 수량
          grid.cellValue(0, 'unit_price', row.unit_price); // 단가
          grid.cellValue(0, 'item.unit', row.item.unit); // 단위
          grid.cellValue(0, 'vat', -response.vat); // 부가세
          grid.cellValue(0, 'supply_price', -response.supply_price); // 공급가
          grid.cellValue(0, 'total_price', -response.total_price); // 금액
          grid.cellValue(0, 'not_deposit', -response.total_price); // 미입금
          grid.cellValue(0, 'note', ''); // 추가설명
          grid.cellValue(0, 'release_number', row.release ? row.release.release_number : null); // 출고번호
          grid.cellValue(0, 'release_return_number', row.release_return ? row.release_return.return_number : null); // 출고반품번호
          grid.cellValue(0, 'fk_project_management_id', null); // 프로젝트번호
          grid.cellValue(0, 'fk_sales_id', vars.formData.id); // 계산서 아이디
          grid.cellValue(0, 'fk_release_item_id', null); // 출고 품목 아이디
          grid.cellValue(0, 'fk_release_return_item_id', row.id); // 출고반품 품목 아이디
        }
        grid.refresh();
        vars.dlg.addReleaseReturnItem.show = false;
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
          vars.grid.baseItem.refresh();
        }
        vars.dlg.addItem.show = true;
      },
      showAddProjectPopup() {
        const notContains = [];
        for (const item of vars.grid.item1.getVisibleRows()) {
          if (!item.id) {
            if (item.data.fk_project_management_id) {
              notContains.push(['id', '<>', item.data.fk_project_management_id], 'and');
            }
          }
        }
        notContains.pop()
        
        if (vars.grid.projectItem) {
          vars.grid.projectItem.filter(notContains);
          vars.grid.projectItem.clearSelection();
          vars.grid.projectItem.refresh();
        }
        vars.dlg.addProjectItem.show = true;
      },
      showAddReleasePopup() {
        const notContains = [];
        for (const item of vars.grid.item1.getVisibleRows()) {
          if (!item.id) {
            if (item.data.fk_release_item_id) {
              notContains.push(['id', '<>', item.data.fk_release_item_id], 'and');
            }
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
      showAddReleaseReturnPopup() {
        const notContains = [];
        for (const item of vars.grid.item1.getVisibleRows()) {
          if (!item.id) {
            if (item.data.fk_release_return_item_id) {
              notContains.push(['id', '<>', item.data.fk_release_return_item_id], 'and');
            }
          }
        }
        notContains.pop()

        if (vars.grid.releaseReturnItem) {
          vars.grid.releaseReturnItem.filter(notContains);
          vars.grid.releaseReturnItem.clearSelection();
          vars.grid.releaseReturnItem.refresh();
        }
        vars.dlg.addReleaseReturnItem.show = true;
      },
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`shipment-sales-${key}`, evt.component);
      },
      async newItem() {
        methods.gridItem1Refresh();
        if (vars.formData.id) {
          methods.clearFormData();
          methods.redirect();
        }
        setTimeout(() => {
          methods.clearFormData();
          vars.formData.sales_date = new Date();
          vars.formData.sales_department = authService.getDepartmentName();
          vars.formData.sales_manager = authService.getUserName();
          vars.formData.vat_type = methods.getFirstVatType();
          vars.formData.sales_type = methods.getFirstSalesType();
          vars.formData.approval_type = methods.getFirstApprovalType();
          vars.formData.publish_type = methods.getFirstPublishType();
          vars.formData.office_type = methods.getFirstOfficeType();
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
            await shipmentSalesStatement.remove(vars.formData.id);
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
            const { data } = await shipmentSalesStatement.update(vars.formData.id, updateDate);
            vars.formData.sales_number = data.sales_number;
            if (vars.grid.item1) await vars.grid.item1.saveEditData();

            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');

            methods.enableSave();
            methods.enableDelete();
          } else {
            // 채번이 없을 경우 자동 채번
            if (vars.formData.created) vars.formData.created = null;
            let { data } = await shipmentSalesStatement.insert(vars.formData);
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
            notifyError('이미 존재하는 계산서번호 입니다');
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
          case 'sales': {
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
            if (data.order_company && data.order_company != vars.formData.client_company) {
              vars.formData.client_company = data.order_company;
              if (vars.formData.client_company) { methods.onClientChanged(); }
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

        vars.filter.baseItem.clientId = client ? client.id : null;
        methods.loadBaseItem();

        vars.filter.releaseItem.clientCompany = vars.formData.client_company;
        methods.loadReleaseItem();

        vars.filter.releaseReturnItem.clientCompany = vars.formData.client_company;
        methods.loadReleaseReturnItem();

        vars.filter.projectItem.clientCompany = vars.formData.client_company;
        methods.loadProjectItem();

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
          vars.formData.sales_manager = null;
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
            element.data.fk_sales_id = vars.formData.id;
            delete element.data.item;
            delete element.data.basic_stock;
            delete element.data.release_item;
            delete element.data.current_stock;
            delete element.data.available_stock;
            delete element.data.project_management;
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
        shipmentSalesStatement.update(vars.formData.id, priceData);
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
      setQuantity(newData, value, currentRowData) {
        newData.quantity = value;
        newData.unit_price = currentRowData.unit_price;
        const response = calcPriceSummary(vars.formData.vat_type, newData.quantity * newData.unit_price);
        newData.supply_price = response.supply_price;
        newData.vat = response.vat;
        newData.total_price = response.total_price;
        newData.not_deposit = response.total_price;
        if (currentRowData.fk_release_return_item_id) {
          newData.supply_price = -newData.supply_price;
          newData.vat = -newData.vat;
          newData.total_price = -newData.total_price;
          newData.not_deposit = -newData.not_deposit;
        }
      },
      setUnitPrice(newData, value, currentRowData) {
        newData.quantity = currentRowData.quantity;
        newData.unit_price = value;
        const response = calcPriceSummary(vars.formData.vat_type, newData.quantity * newData.unit_price);
        newData.supply_price = response.supply_price;
        newData.vat = response.vat;
        newData.total_price = response.total_price;
        newData.not_deposit = response.total_price;
        if (currentRowData.fk_release_return_item_id) {
          newData.supply_price = -newData.supply_price;
          newData.vat = -newData.vat;
          newData.total_price = -newData.total_price;
          newData.not_deposit = -newData.not_deposit;
        }
      },
      setProjectManagement(newData, value, currentRowData){
        if(!value) return;
        newData.fk_project_management_id = value.id;
        newData.project_management = value;
      },
      loadBaseCode() {
        return baseCodeLoader([
          '부가세구분', '수주구분', '결재조건', '납품장소',
          '발행구분', '계산서유형', '결재유형', '본지점구분'
        ])
          .then(response => {
            vars.dataSource.payment_terms = response['결재조건'];
            vars.dataSource.release_type = response['수주구분'];
            vars.dataSource.vat_type = response['부가세구분'];
            vars.dataSource.delivery_place = response['납품장소'];
            vars.dataSource.publish_type = response['발행구분'];
            vars.dataSource.sales_type = response['계산서유형'];
            vars.dataSource.approval_type = response['결재유형'];
            vars.dataSource.office_type = response['본지점구분'];
          })
          .then(() => (vars.init.value = true));
      },
      loadBaseItem() {
        vars.dataSource.baseItem = getBaseItem(
          null,
          vars.filter.baseItem.clientId,
          null
        );
      },
      loadProjectItem() {
        const defaultFilter = [
          {
            name: 'order_company',
            op: 'eq',
            val: vars.filter.projectItem.clientCompany,
          },
          { name: 'non_invoice', op: 'gt', val: 0 }
        ];
        vars.dataSource.projectItem = getProjectRegistration(defaultFilter);
        vars.dataSource.projectItem.on('loaded', ({data}) => {
          const dataSourceForTotalPrice = getProjectRegistration(defaultFilter);
          dataSourceForTotalPrice.load({
            filter: vars.grid.projectItem.getCombinedFilter(),
            take: 1000000
          }).then(response => {
            const price = response.data.reduce((t, i) => t += i.non_invoice, 0);
            if (!price) {
              vars.dlg.addProjectItem.total_price = '0';
            }
            vars.dlg.addProjectItem.total_price = numeral(price).format('0,0');
          });
        });
      },
      loadReleaseItem() {
        const defaultFilter = [
          {
            name: 'release',
            op: 'has',
            val: {
              name: 'client_company',
              op: 'eq',
              val: vars.filter.releaseItem.clientCompany,
            },
          },
          { name: 'non_invoice', op: 'gt', val: 0 }
        ];
        vars.dataSource.releaseItem = getShipmentReleaseItem(defaultFilter);

        vars.dataSource.releaseItem.on('loaded', ({data}) => {
          //const price = data.reduce((t, i) => t += i.release_quantity * i.unit_price, 0)
          //if (!price) vars.dlg.addReleaseItem.total_price = '0'
          //vars.dlg.addReleaseItem.total_price = numeral(price).format('0,0')

          const dataSourceForTotalPrice = getShipmentReleaseItem(defaultFilter);
          dataSourceForTotalPrice.load({
            filter: vars.grid.releaseItem.getCombinedFilter(),
            take: 1000000
          }).then(response => {
            const price = response.data.reduce((t, i) => t += i.release_quantity * i.unit_price, 0);
            if (!price) {
              vars.dlg.addReleaseItem.total_price = '0';
            }
            vars.dlg.addReleaseItem.total_price = numeral(price).format('0,0');
          });
        })
      },
      loadReleaseReturnItem() {
        const defaultFilter = [
          {
            name: 'release_return',
            op: 'has',
            val: {
              name: 'client_company',
              op: 'eq',
              val: vars.filter.releaseReturnItem.clientCompany,
            },
          },
          { name: 'non_invoice', op: 'gt', val: 0 }
        ];
        vars.dataSource.releaseReturnItem = getShipmentReleaseReturnItem(defaultFilter);

        vars.dataSource.releaseReturnItem.on('loaded', ({data}) => {
          //const price = data.reduce((t, i) => t += i.release_quantity * i.unit_price, 0)
          //if (!price) vars.dlg.addReleaseItem.total_price = '0'
          //vars.dlg.addReleaseItem.total_price = numeral(price).format('0,0')

          const dataSourceForTotalPrice = getShipmentReleaseReturnItem(defaultFilter);
          dataSourceForTotalPrice.load({
            filter: vars.grid.releaseReturnItem.getCombinedFilter(),
            take: 1000000
          }).then(response => {
            const price = response.data.reduce((t, i) => t += i.return_quantity * i.unit_price, 0);
            if (!price) {
              vars.dlg.addReleaseReturnItem.total_price = '0';
            }
            vars.dlg.addReleaseReturnItem.total_price = numeral(price).format('0,0');
          });
        })
      },
      checkPossibleSave() {
        if (vars.formData.client_company && vars.formData.sales_department) {
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
      getFirstVatType() {
        return methods.getFirstItemName(vars.dataSource.vat_type);
      },
      getFirstSalesType() {
        return methods.getFirstItemName(vars.dataSource.sales_type);
      },
      getFirstApprovalType() {
        return methods.getFirstItemName(vars.dataSource.approval_type);
      },
      getFirstPublishType() {
        return methods.getFirstItemName(vars.dataSource.publish_type);
      },
      getFirstOfficeType() {
        return methods.getFirstItemName(vars.dataSource.office_type);
      },
      getFirstItemName(itemList) {
        if (!itemList || itemList.length <= 0) { return ''; }
        else { return itemList[0].code_name; }
      },
      redirect(id) {
        if (id) { router.replace({ path: `/shipment/sales-statement/${id}` }); }
        else { router.replace({ path: `/shipment/sales-statement` }); }
      },
      onVatTypeChanged(e) {
        vars.grid.item1.refresh();
      },
      onVatAdjustmentChanged(e) {
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
      calculateCustomSummary(options) {
        if (options.name === 'supply_price') {
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          } else if (options.summaryProcess === 'calculate') {
            if (options.value.fk_release_return_item_id) {
              options.totalValue -= options.value.quantity * options.value.unit_price;
            } else {
              options.totalValue += options.value.quantity * options.value.unit_price;
            }
            
          } else if (options.summaryProcess === 'finalize') {
            const response = calcPriceSummary(vars.formData.vat_type, options.totalValue);
            vars.formData.supply_price = response.supply_price;
            vars.formData.vat = response.vat - vars.formData.vat_adjustment;
            vars.formData.total_price = response.total_price;
            vars.formData.not_deposit = response.total_price;
          }
        }
      },
      async exportInvoice () {
        if (!vars.formData.id) return
        const {data: item1} = await vars.dataSource.item1.load()
        vars.dlg.invoice.data = {...vars.formData}
        vars.dlg.invoice.items = item1
        vars.dlg.invoice.number = vars.formData.sales_number
        vars.dlg.invoice.show = true
      },
      async refreshBarobillState () {
        if (!vars.formData.sales_number) return
        console.info('세금계산서 상태 업데이트 (부모 페이지)')
        const {data: state} = await barobillService.get(`state/${vars.formData.sales_number}`)

        vars.dlg.invoice.state = BAROBILL_STATE[state.data.BarobillState]
        console.log(`세금계산서 상태: ${state.data.BarobillState} [${BAROBILL_STATE[state.data.BarobillState]}]`)
      },
      onSelectionChangeProject ({selectedRowsData}) {
        const price = selectedRowsData.reduce((t, i) => t += i.non_invoice, 0);
        if (!price) vars.dlg.addProjectItem.selection_price = '0';
        vars.dlg.addProjectItem.selection_price = numeral(price).format('0,0');
      },
      onSelectionChangeRelease ({selectedRowsData}) { 
        const price = selectedRowsData.reduce((t, i) => t += i.release_quantity * i.unit_price, 0)
        if (!price) vars.dlg.addReleaseItem.selection_price = '0'
        vars.dlg.addReleaseItem.selection_price = numeral(price).format('0,0')
      },
      onSelectionChangeReleaseReturn ({selectedRowsData}) {
        const price = selectedRowsData.reduce((t, i) => t += i.return_quantity * i.unit_price, 0)
        if (!price) vars.dlg.addReleaseReturnItem.selection_price = '0'
        vars.dlg.addReleaseReturnItem.selection_price = numeral(price).format('0,0')
      }
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