<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">수주</div>
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
              :options="{ text: '수주복사', icon: 'copy', disabled: !vars.formData.id, onClick: methods.copyItem }"
            />
            <dx-item location="after" locate-in-menu="auto" widget="dxButton"
              :options="{ text: '주문서출력', icon: 'print', disabled: !vars.formData.id, onClick: methods.printDocument }"
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
                  ...generateItemButtonOption('search', methods.createFindPopupFn('order', '수주조회')),
                }"
              >
                <dx-label text="수주번호" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="order_date" editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  ...vars.formState,
                }"
              >
                <dx-label text="수주일자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="client_company"
                :editor-options="{
                  onEnterKey: methods.createFindPopupFn('client', '업체조회', {
                    name: vars.formData.client_company,
                  }),
                  ...generateItemButtonOption('search', methods.createFindPopupFn('client', '업체조회', { 
                    name: vars.formData.client_company 
                  })),
                  ...vars.formState,
                }"
              >
                <dx-label text="고객업체" :show-colon="false" />
                <dx-required-rule message="고객업체를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="client_manager" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'name',
                  displayExpr: methods.clientManagerExpr,
                  acceptCustomValue: true,
                  disabled: vars.disabled.clientManager,
                  dataSource: vars.dataSource.client_manager,
                  onEnterKey: methods.createFindPopupFn('client-manager', '업체담당자조회', {
                    name: vars.formData.client_manager,
                    fk_client_id: vars.filter.baseItem.clientId
                  }),
                  ...generateItemButtonOption('search', methods.createFindPopupFn('client-manager', '업체담당자조회', { 
                    name: vars.formData.client_manager,
                    fk_client_id: vars.filter.baseItem.clientId
                  })),
                  ...vars.formState,
                }"
              >
                <dx-label text="업체담당자" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="order_department" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'department_name',
                  displayExpr: 'department_name',
                  acceptCustomValue: true,
                  dataSource: vars.dataSource.department,
                  onValueChanged: methods.onDepartmentChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="수주부서" :show-colon="false" />
                <dx-required-rule message="수주부서를 선택하세요" />
              </dx-simple-item>
              <dx-simple-item data-field="order_manager" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'emp_name',
                  displayExpr: 'emp_name',
                  disabled: vars.disabled.manager,
                  dataSource: vars.dataSource.employee,
                  ...vars.formState,
                }"
              >
                <dx-label text="수주담당자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="order_type" editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  dataSource: vars.dataSource.order_type,
                  onValueChanged: methods.onOrderTypeChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="수주구분" :show-colon="false" />
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
              <dx-simple-item data-field="release_number"
                :editor-options="{
                  readOnly: true,
                  buttons: [
                    {
                      name: 'release_number',
                      location: 'after',
                      options: { icon: 'link', stylingMode: 'text', disabled: false, onClick: methods.redirectToRelease },
                    },
                  ],
                }"
              >
                <dx-label text="출고번호" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-group-item :col-count="2">
                <dx-simple-item data-field="confirmed" editor-type="dxCheckBox"
                :editor-options="{ onValueChanged: methods.onConfirmChanged }">
                  <dx-label text="수주확정" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item data-field="approve" editor-type="dxCheckBox"
                  :editor-options="{ onValueChanged: methods.onApproveChanged }">
                    <dx-label text="수주승인" :show-colon="false" />
                </dx-simple-item>
              </dx-group-item>
              
              <dx-simple-item data-field="etc" editor-type="dxTextArea"
                :editor-options="{
                  labelMode: 'hidden',
                  height: '130px',
                  placeholder: '비고',
                  ...generateItemButtonOption('rename', methods.createFindPopupFn('etc', '비고', vars.formData.etc)),
                  ...vars.formState,
                }"
              >
                <dx-label text="비고" :show-colon="false" :visible="false" />
              </dx-simple-item>
            </dx-group-item>
          </dx-group-item>
          <dx-group-item :col-count="5">
            <dx-group-item :col-span="1">
              <dx-simple-item data-field="client_manager_phone"
                :calculate-cell-value="methods.getClientManagerPhone"
                :editor-options="{ ...vars.formState }"
              >
                <dx-label text="담당연락처" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item :col-span="4">
              <dx-simple-item data-field="delivery_place" :editor-options="{ ...vars.formState }">
                <dx-label text="납품장소" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
          </dx-group-item>
        </dx-form>
      </div>

      <div class="dx-card responsive-paddings mt-1">
        <dx-tab-panel :animation-enabled="false" :swipe-enabled="false">
          <dx-item title="수주내역">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 516px)"
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
                  @data-error-occurred="methods.onDataError"
                  @cell-dbl-click="methods.itemPopupClick"
                  @focused-cell-changed="methods.onFocusedCellChanged"
                >
                  <dx-grid-toolbar>
                    <dx-item template="exportToRelease" location="before" :visible="vars.formData.confirmed" />
                    <dx-item template="addFromQuote" location="before" :visible="!vars.formState.readOnly" />
                    <dx-item template="addFromProject" location="before" :visible="!vars.formState.readOnly" />
                    <dx-item template="calcAvailStock" location="before" :visible="!vars.formState.readOnly" />
                    <dx-grid-item name="addRowButton" :options="{ onClick: methods.showAddPopup }" />
                    <dx-grid-item name="saveButton" :visible="!!vars.formData.id" />
                    <dx-grid-item name="revertButton" />
                    <dx-grid-item name="columnChooserButton" />
                  </dx-grid-toolbar>
                  <template #exportToRelease>
                    <dx-button text="출고로 보내기" icon="export" @click="methods.exportToRelease" />
                  </template>
                  <template #addFromQuote>
                    <dx-button text="견적에서 가져오기" icon="add" @click="methods.showAddQuotePopup" />
                  </template>
                  <template #addFromProject>
                    <dx-button text="프로젝트에서 가져오기" icon="add" @click="methods.showAddProjectPopup" />
                  </template>
                  <template #calcAvailStock>
                    <dx-button text="할당수량 재계산" icon="formula" @click="methods.calculateAssignQuantity" />
                  </template>

                  <dx-column caption="품목코드" data-field="item_code" width="180" :allow-editing="false" />
                  <dx-column caption="품명" data-field="item.item_name" :allow-editing="false" />
                  <dx-column caption="규격" data-field="item.item_standard" :allow-editing="false" />
                  <dx-column caption="수주수량" data-field="order_quantity" data-type="number" format="fixedPoint" :set-cell-value="methods.setQuantity" />
                  <dx-column caption="할당수량" data-field="assign_quantity" data-type="number" format="fixedPoint" :allow-editing="false" />
                  <dx-column caption="단가" data-field="unit_price" data-type="number" format="currency"  :set-cell-value="methods.setUnitPrice" />
                  <dx-column caption="단위" data-field="item.unit" :allow-editing="false" />
                  <dx-column caption="공급가" data-field="supply_price" data-type="number" format="currency" :allow-editing="false" />
                  <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
                  <dx-column caption="출고창고" data-field="warehouse.wh_name" :set-cell-value="methods.setWarehouse">
                    <dx-lookup value-expr="wh_name" display-expr="wh_name" :data-source="vars.dataSource.warehouse" />
                  </dx-column>
                  <dx-column caption="미출고" data-field="not_shipped" data-type="number" format="fixedPoint" :allow-editing="false" />
                  <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :allow-editing="false" :calculate-display-value="methods.availableStock" />
                  <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :allow-editing="false" :calculate-display-value="methods.currentStock" />
                  <dx-column caption="생산계획수량" data-field="produce_plan_quantity" data-type="number" format="fixedPoint" :allow-editing="true" :set-cell-value="methods.setPlanQuantity" />
                  <dx-column caption="생산계획 미처리" data-field="not_produce_plan_quantity" data-type="number" format="fixedPoint" :allow-editing="false" />
                  <dx-column caption="견적번호" data-field="quote_number" :allow-editing="false" />
                  <dx-column caption="고객사품번" data-field="client_item_number" />
                  <dx-column caption="품목설명" data-field="item.item_detail" :allow-editing="false" />
                  <dx-column caption="참고사항" data-field="note" />
                  <dx-column caption="종결" data-field="closing_yn" data-type="boolean" />
                  <dx-column caption="프로젝트번호" data-field="project_management.project_number"
                    :editor-options="{ ...generateItemButtonOption('search', methods.createFindPopupFn('project2', '프로젝트조회')) }"
                    :set-cell-value="methods.setProjectManagement"
                  />
                  <dx-column caption="수주아이디" data-field="fk_order_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
                  <dx-column caption="견적품목아이디" data-field="fk_quote_item_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
                  <dx-column caption="창고코드" data-field="warehouse_code" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />

                  <dx-summary :recalculate-while-editing="true" :calculate-custom-summary="methods.calculateCustomSummary">
                    <dx-total-item name="supply_price" summary-type="custom" />
                  </dx-summary>

                  <dx-scrolling mode="standard" />
                  <dx-column-chooser mode="select" :enabled="true" />
                  <dx-editing mode="batch"
                    :allow-adding="!vars.formState.readOnly"
                    :allow-updating="!vars.formState.readOnly && !vars.formData.confirmed"
                    :allow-deleting="!vars.formState.readOnly"
                  />
                </dx-data-grid>
              </div>
            </template>
          </dx-item>
        </dx-tab-panel>

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
      title="견적품목찾기"
      content-template="popup-content"
      v-model:visible="vars.dlg.addQuoteItem.show"
      :width="680"
      :height="500"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="(evt) => methods.onGridInitialized(evt, 'find-item-popup')"
    >
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ text: '선택된 항목 추가', icon: 'add', onClick: methods.addSelectedQuoteRows }"
      />

      <template #popup-content>
        <dx-data-grid
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="vars.dataSource.quoteItem"
          :on-initialized="(evt) => methods.onGridInitialized(evt, 'quoteItem')"
        >
          <dx-column caption="고객업체" data-field="quote.client_company" />
          <dx-column caption="견적번호" data-field="quote.quote_number" :sort-index="1" sort-order="desc" />
          <dx-column caption="견적일자" data-field="quote.quote_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="견적수량" data-field="quote_quantity" data-type="number" format="fixedPoint" />

          <dx-paging :page-size="20" />
          <dx-sorting mode="multiple"/>
          <dx-filter-row :visible="true" />
          <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick" />
        </dx-data-grid>
      </template>
    </dx-popup>

    <dx-popup
      title="프로젝트 품목찾기"
      content-template="popup-content"
      v-model:visible="vars.dlg.addProjectItem.show"
      :width="680"
      :height="500"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="(evt) => methods.onGridInitialized(evt, 'find-project-popup')"
    >
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ text: '선택된 항목 추가', icon: 'add', onClick: methods.addSelectedProjectRows }"
      />

      <template #popup-content>
        <dx-data-grid
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="vars.dataSource.projectItem"
          :on-initialized="(evt) => methods.onGridInitialized(evt, 'projectItem')"
        >
          <dx-column caption="프로젝트번호" data-field="project_management.project_number" />
          <dx-column caption="프로젝트명" data-field="project_management.project_name" />
          <dx-column caption="발주기관" data-field="project_management.order_company" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="수량" data-field="quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="미수주수량" data-field="not_ordered" data-type="number" format="fixedPoint" />

          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick" />
        </dx-data-grid>
      </template>
    </dx-popup>

    <dx-popup
      title="품목찾기"
      content-template="popup-content"
      v-model:visible="vars.dlg.addItem.show"
      width="70%"
      :height="500"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="(evt) => methods.onGridInitialized(evt, 'find-item2-popup')"
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
          :on-initialized="(evt) => methods.onGridInitialized(evt, 'baseItem')"
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
      :resize-enabled="true"
      :close-on-outside-click="true"
      :key="vars.dlg.finder.key"
      :title="vars.dlg.finder.title"
      @initialized="(evt) => methods.onGridInitialized(evt, 'multiuse-popup')"
    >
      <template #popup-content>
        <data-grid-client v-if="vars.dlg.finder.key === 'client'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-client v-else-if="vars.dlg.finder.key === 'enduser'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-client-manager v-else-if="vars.dlg.finder.key === 'client-manager'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-order v-else-if="vars.dlg.finder.key === 'order'" @change="methods.finderReturnHandler" />
        <data-grid-project v-else-if="vars.dlg.finder.key === 'project'" @change="methods.finderReturnHandler" />
        <data-grid-project v-else-if="vars.dlg.finder.key === 'project2'" @change="methods.finderReturnHandler" />
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

import { onMounted, ref, reactive, computed, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';


import { DxButton } from 'devextreme-vue/button';
import DxTextArea from 'devextreme-vue/text-area';
import { DxTabPanel } from 'devextreme-vue/tab-panel';
import { confirm, alert } from 'devextreme/ui/dialog';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxCustomRule, DxRequiredRule } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxLookup, DxEditing, DxSorting, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, 
  DxItem as DxGridItem, DxToolbar as DxGridToolbar, DxButton as DxGridButton, DxSummary, DxTotalItem, DxRequiredRule as DxGridRequiredRule } from 'devextreme-vue/data-grid';

import { getStock } from '../../data-source/setup';
import { getProjectItem } from '../../data-source/project';
import { baseClient, baseCodeLoader, getBaseItem } from '../../data-source/base';
import { shipmentOrder, shipmentRelease, shipmentQuoteItem, getShipmentQuoteItem, getShipmentOrderItem } from '../../data-source/shipment';

import PopupItemDetail from '@/components/base/popup-item-detail';
import DataGridClient from '@/components/base/data-client.vue';
import DataGridClientManager from '@/components/base/data-client-manager.vue';
import DataGridOrder from '../../components/shipment/data-order.vue';
import DataGridProject from '../../components/project/data-project.vue';

import authService from '../../auth';
import stateStore from '@/utils/state-store';
import ApiService from '../../utils/api-service';
import printDocument from '../../utils/print-document'
import { notifyInfo, notifyError } from '../../utils/notify';
import { loadEmployee, loadWarehouse, loadDepartment, loadClientManager } from '../../utils/data-loader';
import { calcPriceSummary, currentDateTime, beforeExitConfirm, generateItemButtonOption } from '../../utils/util';

export default {
  components: {
    DxButton,
    DxTextArea,
    DxTabPanel,
    DxLoadPanel,
    DxToolbar, DxItem,
    DxPopup, DxToolbarItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem, DxCustomRule, DxRequiredRule,
    DxDataGrid, DxColumn, DxPaging, DxLookup, DxEditing, DxSorting, DxSelection, DxFilterRow, DxScrolling, DxColumnChooser, DxGridItem, DxGridToolbar, DxGridButton, DxSummary, DxTotalItem,
    DataGridOrder, DataGridClient, DataGridProject, PopupItemDetail, DataGridClientManager, DxGridRequiredRule
  },
  props: {
    id: [String, Number],
  },
  setup(props) {
    // variable 설정
    const router = useRouter();
    const vars = {};
    vars.init = ref(false);
    vars.loading = ref(false);
    vars.formData = reactive({});
    vars.formState = reactive({ readOnly: true });
    vars.grid = {};
    vars.dlg = {};
    vars.dlg.addItem = reactive({ show: false });
    vars.dlg.addQuoteItem = reactive({ show: false });
    vars.dlg.addProjectItem = reactive({ show: false });
    vars.dlg.finder = reactive({ title: '', key: null, data: null, show: false });
    vars.api = {};
    vars.api.updateAssignQuantity = new ApiService('/api/mes/v1/update-assign-quantity');
    vars.api.exportToRelease = new ApiService('/api/mes/v1/shipment/order/export/release');
    vars.api.updateItemStock = new ApiService('/api/mes/v1/setup/update/item/stock');
    vars.warehouse = {};
    vars.focus = {};
    vars.focus.item1 = null;
    vars.filter = {};
    vars.filter.baseItem = { clientId: null };
    vars.filter.quoteItem = { clientCompany: null };
    vars.filter.item1 = [{ name: 'fk_order_id', op: 'eq', val: props.id || 0 }];
    vars.disabled = reactive({
      new: false,
      edit: true,
      save: true,
      delete: true,
      manager: true,
      tradeYn: false,
      clientManager: true,
    });
    vars.dataSource = reactive({
      vat_type: [],
      employee: [],
      warehouse: [],
      department: [],
      order_type: [],
      payment_terms: [],
      delivery_place: [],
      client_manager: [],
      item_group: [],
      asset_type: [],
      baseItem: null,
      quoteItem: null,
      item1: getShipmentOrderItem(vars.filter.item1),
    });
    vars.itemDetail = reactive({ visible: false, id: 0 });

    vars.summary = {};
    vars.summary.supply_price = computed(() => '₩' + numeral(vars.formData.supply_price).format('0,0'));
    vars.summary.vat = computed(() => '₩' + numeral(vars.formData.vat).format('0,0'));
    vars.summary.total_price = computed(() => '₩' + numeral(vars.formData.total_price).format('0,0'));

    onMounted(async () => {
      await loadDepartment(vars.dataSource);
      await methods.loadBaseCode();
      methods.initById(props.id);
      methods.loadProjectItem();
      loadWarehouse(vars.dataSource);
    });

    // public methods
    const methods = {
      async initById(id) {
        beforeExitConfirm.check(() => !vars.disabled.save);
        methods.gridItem1Refresh(id);
        if (!id) {
          methods.clearFormData();
          methods.disableAllAction();
          return;
        }

        await methods.loadOrderData(id);

        methods.syncStatusDelete();
        vars.disabled.edit = false;
        if (methods.isFilledFormRequiredData()) {
          methods.syncStatusSave();
        }
        if (methods.isOrderConfirmed()) {
          methods.disableAllAction();
        }
        methods.onClientChanged();
      },
      async loadOrderData(id) {
        let { data } = await shipmentOrder.byKey(id);
        Object.assign(vars.formData, data);
      },
      clearFormData() {
        vars.formData.id = null;
        vars.formData.created = null;
        vars.formData.order_number = '';
        vars.formData.order_date = '';
        vars.formData.client_company = '';
        vars.formData.client_manager = '';
        vars.formData.client_manager_phone = '';
        vars.formData.order_department = '';
        vars.formData.order_manager = '';
        vars.formData.order_type = '';
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
        vars.formData.release_number = null;
        vars.formData.confirmed = false;
        vars.formData.approve = false;
        vars.formData.fk_project_management_id = null;
        vars.formData.project_management = null;
        vars.formData.fk_company_id = authService.getCompanyId();
      },
      async addSelectedRows() {
        const grid = vars.grid.item1;
        const rows = await vars.grid.baseItem.getSelectedRowsData();
        for (let row of rows) {
          const clientItemNumber = row.client_item ? row.client_item.client_item_code : null;
          const basicStock = row.basic_stock ? { ...row.basic_stock } : { current_stock: 0, available_stock: 0 };

          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code; // 품목코드
          data.item = { ...row }; // 품목
          data.order_quantity = 0; // 수주수량
          data.assign_quantity = 0; // 할당수량
          data.not_shipped = 0; // 미출고
          data.unit_price = row.sales_price; // 단가
          data.supply_price = 0; // 공급가
          data.request_delivery_date = null; // 요청납기
          data.basic_stock = { ...basicStock }; // 기초재고
          data.produce_plan_quantity = 0; // 생산계획수량
          data.not_produce_plan_quantity = 0; // 생산계획미처리
          data.client_item_number = clientItemNumber; // 공급사품번
          data.quote_number = null; // 견적번호
          data.note = ''; // 참고사항
          data.closing_yn = false; // 종결
          data.warehouse = { ...vars.warehouse }; // 출고창고
          data.warehouse_code = vars.warehouse.wh_code; // 창고코드
          // data.fk_project_management_id = vars.formData.fk_project_management_id; // 프로젝트번호
          data.fk_quote_item_id = null; // 견적품목 아이디
          data.fk_order_id = vars.formData.id; // 수주 아이디
          data.fk_project_item_id = null; // 프로젝트 품목 아이디
        }
        grid.refresh();
        vars.dlg.addItem.show = false;
      },
      async addSelectedQuoteRows() {
        const grid = vars.grid.item1;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        const rows = await vars.grid.quoteItem.getSelectedRowsData();
        for (let row of rows) {
          const basicStock = row.basic_stock ? { ...row.basic_stock } : { current_stock: 0, available_stock: 0 };

          let assignQuantity = row.quote_quantity;
          if (basicStock.available_stock < row.quote_quantity) {
            assignQuantity = basicStock.available_stock;
          }

          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code; // 품목코드
          data.item = { ...row.item }; // 품목
          data.order_quantity = row.quote_quantity; // 수주수량
          if (methods.isNotAssignQuantity()) {
            data.assign_quantity = 0; // 할당수량
          } else {
            data.assign_quantity = assignQuantity; // 할당수량
          }
          data.not_shipped = row.quote_quantity; // 미출고
          data.unit_price = row.unit_price; // 단가
          data.supply_price = data.order_quantity * data.unit_price; // 공급가
          data.request_delivery_date = null; // 요청납기
          data.basic_stock = { ...basicStock }; // 기초재고
          // data.produce_plan_quantity = row.quote_quantity - assignQuantity; // 생산계획수량
          // data.not_produce_plan_quantity = row.quote_quantity - assignQuantity;  // 생산계획미처리
          data.produce_plan_quantity = 0; // 생산계획수량
          data.not_produce_plan_quantity = 0;  // 생산계획미처리
          data.client_item_number = row.client_item_number; // 공급사품번
          data.quote_number = row.quote.quote_number; // 견적번호
          data.note = row.note; // 참고사항
          data.closing_yn = false; // 종결
          data.warehouse = { ...row.warehouse }; // 출고창고
          data.warehouse_code = row.warehouse.wh_code; // 창고코드
          // data.fk_project_management_id = row.fk_project_management_id; // 프로젝트번호
          data.fk_quote_item_id = row.id; // 견적품목 아이디
          data.fk_order_id = vars.formData.id; // 수주 아이디
          data.fk_project_item_id = null; // 프로젝트 품목 아이디
        }
        grid.refresh();
        vars.dlg.addQuoteItem.show = false;
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
          const clientItemNumber = row.item.client_item ? row.item.client_item.client_item_code : null;
          const basicStock = row.basic_stock ? { ...row.basic_stock } : { current_stock: 0, available_stock: 0 };

          let assignQuantity = row.not_ordered;
          if (basicStock.available_stock < row.not_ordered) {
            assignQuantity = basicStock.available_stock;
          }

          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code; // 품목코드
          data.item = { ...row.item }; // 품목
          data.order_quantity = row.not_ordered; // 수주수량
          if (methods.isNotAssignQuantity()) {
            data.assign_quantity = 0; // 할당수량
          } else {
            data.assign_quantity = assignQuantity; // 할당수량
          }
          data.not_shipped = row.not_ordered; // 미출고
          data.unit_price = row.item.sales_price; // 단가
          data.supply_price = data.order_quantity * data.unit_price; // 공급가
          data.request_delivery_date = null; // 요청납기
          data.basic_stock = { ...basicStock }; // 기초재고
          data.produce_plan_quantity = 0; // 생산계획수량
          data.not_produce_plan_quantity = 0; // 생산계획미처리
          data.client_item_number = clientItemNumber; // 공급사품번
          data.quote_number = null; // 견적번호
          data.note = ''; // 참고사항
          data.closing_yn = false; // 종결
          data.warehouse = { ...vars.warehouse }; // 출고창고
          data.warehouse_code = vars.warehouse.wh_code; // 창고코드
          data.fk_project_management_id = row.project_management.id; // 프로젝트번호
          data.project_management = row.project_management;
          data.fk_quote_item_id = null; // 견적품목 아이디
          data.fk_order_id = vars.formData.id; // 수주 아이디
          data.fk_project_item_id = row.id; // 프로젝트 품목 아이디
        }
        grid.refresh();
        vars.dlg.addProjectItem.show = false;
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
      gridClearAndRefresh(grid) {
        if (grid) {
          grid.clearSelection();
          grid.clearFilter();
          grid.refresh();
        }
      },
      showAddPopup() {
        methods.gridClearAndRefresh(vars.grid.baseItem);
        vars.dlg.addItem.show = true;
      },
      showAddQuotePopup() {
        const notContains = [];
        for (const item of vars.grid.item1.getVisibleRows()) {
          if (!item.id) {
            notContains.push(['id', '<>', item.data.fk_quote_item_id], 'and');
          }
        }
        notContains.pop()

        if (vars.grid.quoteItem) {
          vars.grid.quoteItem.filter(notContains);
          vars.grid.quoteItem.clearSelection();
          vars.grid.quoteItem.refresh();
        }
        vars.dlg.addQuoteItem.show = true;
      },
      showAddProjectPopup() {
        methods.loadProjectItem();
        
        const notContains = [];
        for (const item of vars.grid.item1.getVisibleRows()) {
          if (!item.id) {
            notContains.push(['id', '<>', item.data.fk_project_item_id], 'and');
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
      async postUpdateAssignQuantity(orderItemId, itemCode, warehouseCode) {
        const params = {
          order_item_id: orderItemId,
          item_code: itemCode,
          warehouse: warehouseCode,
        };
        await vars.api.updateAssignQuantity.post('', params);
      },
      async calculateAssignQuantity() {
        const rows = vars.grid.item1.getVisibleRows();
        for (const row of rows) {
          if (row.data.id) {
            await methods.postUpdateAssignQuantity(
              row.data.id,
              row.data.item_code,
              row.data.warehouse_code
            );
          }
        }
        vars.grid.item1.refresh();
      },
      async gridItem1Refresh(id) {
        vars.dataSource.item1.defaultFilters = methods.setIdToGridFilter(
          vars.filter.item1,
          id
        );
        methods.gridRefresh(vars.grid.item1);
      },
      setIdToGridFilter(filter, id) {
        if (!id) { id = 0; }
        filter[0].val = id;
        return filter;
      },
      gridRefresh(grid) {
        if (grid) {
          grid.cancelEditData();
          grid.refresh();
        }
      },
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`shipment-order-${key}`, evt.component);
      },
      async newItem() {
        methods.gridItem1Refresh();
        if (vars.formData.id) {
          methods.clearFormData();
          methods.redirect();
        }
        setTimeout(() => {
          methods.clearFormData();

          vars.formData.order_date = currentDateTime();
          vars.formData.order_department = authService.getDepartmentName();
          vars.formData.order_manager = authService.getUserName();
          vars.formData.order_type = methods.getFirstOrderType();
          vars.formData.vat_type = methods.getFirstVatType();
          vars.formData.payment_terms = methods.getFirstPaymentTerms();
          // vars.formData.delivery_place = methods.getFirstDeliveryPlace();
          vars.formData.fk_company_id = authService.getCompanyId();
          vars.formState.readOnly = false;
        }, 200);
      },
      async editItem() {
        if (!vars.formData.id) {
          return;
        }
        if (methods.isFormReadOnly() && methods.isOrderConfirmed()) {
          return;
        }
        if (methods.isFormReadOnly()) {
          let isSelect = await confirm('수정하시겠습니까?', '수정');
          if (!isSelect) {
            return;
          }
        }

        const saveFormData = Object.assign({}, vars.formData);
        vars.formState.readOnly = !vars.formState.readOnly;

        methods.syncStatusDelete();
        methods.syncStatusSave();

        await nextTick();
        Object.assign(vars.formData, saveFormData);
      },
      async deleteItem() {
        const result = await confirm('이 항목을 삭제하시겠습니까?', '삭제 확인');
        if (result) {
          try {
            await shipmentOrder.remove(vars.formData.id);
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
        methods.showLoading();
        try {
          if (vars.formData.id) {
            // 기존 정보 업데이트
            const updateDate = Object.assign({}, vars.formData);
            delete updateDate.created;
            delete updateDate.order_number;
            const { data } = await shipmentOrder.update(
              vars.formData.id,
              updateDate
            );
            vars.formData.order_number = data.order_number;
            await methods.saveItem1();

            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');

            methods.syncStatusSave();
            methods.syncStatusDelete();
          } else {
            // 채번이 없을 경우 자동 채번
            if (vars.formData.created) vars.formData.created = null;
            let { data } = await shipmentOrder.insert(vars.formData);
            vars.formData.id = data.id;

            await methods.saveItem1();

            beforeExitConfirm.clear()
            methods.redirect(data.id);
            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');
          }
        } catch (ex) {
          if (ex.response.status === 602) {
            notifyError('이미 존재하는 수주번호 입니다');
          } else {
            console.error(ex);
            notifyError('저장 할 내용이 없습니다');
          }
        } finally {
          methods.hideLoading();
        }
      },
      async saveItem1() {
        await methods.saveGrid(vars.grid.item1);
      },
      async saveGrid(grid) {
        if (grid && grid.hasEditData()) {
          await grid.saveEditData();
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
          case 'client-manager': {
            loadClientManager(vars.dataSource, vars.formData.client_company).then(() => {
              vars.formData.client_manager = data.name;
            })
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
          case 'project2': {
            vars.focus.item1.component.cellValue(
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

        vars.filter.quoteItem.clientCompany = client ? client.name : null;
        methods.loadQuoteItem();

        if (!client) {
          vars.disabled.edit = true;
          vars.disabled.delete = true;
          vars.disabled.save = true;
          vars.disabled.tradeYn = false;
          vars.disabled.clientManager = true;
          vars.formData.client_manager = null;
          vars.dataSource.client_manager = [];
        } else {
          if (!vars.formData.delivery_place) {
            vars.formData.delivery_place = `${client.address} ${client.address_detail}`;
          }
          else {
            console.log(vars.formData.delivery_place)
          }

          if (methods.isFormReadOnly() || vars.disabled.tradeYn) {
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
              vars.formData.vat_type = client.zero_tax_rate_yn ? '영세' : methods.getFirstVatType();
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
        if (methods.isFormReadOnly()) {
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
          if (methods.isFilledFormRequiredData()) {
            vars.disabled.edit = false;
            methods.syncStatusSave();
            methods.syncStatusDelete();
          }
        }
        await shipmentOrder.update(vars.formData.id, param);
      },
      async onApproveChanged(e){
        if (!vars.formData.id) {
          vars.formData.approve = 0;
          return;
        }
        let param = { approve: 1 };
        if (e.value) {
          param.approve = 1;
        }else{
          param.approve = 0;
        }
        await shipmentOrder.update(vars.formData.id, param);
      },
      updateEtcValue(v) {
        vars.dlg.finder.data = v;
      },
      onOrderTypeChanged(e) {
        if (e.value) {
          const rows = vars.grid.item1.getVisibleRows();
          for (const row of rows) {
            let assignQuantity = 0;
            if (row.data.closing_yn || !row.data.basic_stock || methods.isNotAssignQuantity()) {
              assignQuantity = 0;
            } else {
              if (row.data.basic_stock.available_stock >= row.data.not_shipped) {
                assignQuantity = row.data.not_shipped;
              } else {
                assignQuantity = row.data.basic_stock.available_stock;
              }
            }
            row.data.assign_quantity = assignQuantity;

            const columnIndex = vars.grid.item1.getVisibleColumnIndex('할당수량')
            vars.grid.item1.cellValue(row.rowIndex, columnIndex, assignQuantity);
          }
          vars.grid.item1.refresh();
        }
      },
      onDepartmentChanged(e) {
        if (!e.value) {
          vars.disabled.save = true;
          vars.disabled.manager = true;
          vars.formData.order_manager = null;
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
      },
      onSavingItem(e) {
        e.changes.forEach((element) => {
          if (element.type != 'remove') {
            element.data.fk_order_id = vars.formData.id;
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
        shipmentOrder.update(vars.formData.id, priceData);
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
      onFocusedCellChanged(e) {
        vars.focus.item1 = e;
      },
      availableStock(rowData) {
        if (!rowData.basic_stock) {
          return '0';
        }
        return rowData.basic_stock.available_stock;
      },
      currentStock(rowData) {
        if (!rowData.basic_stock) {
          return '0';
        }
        return rowData.basic_stock.current_stock;
      },
      setPlanQuantity(newData, value, currentRowData) {
        newData.not_produce_plan_quantity = currentRowData.not_produce_plan_quantity + (value - currentRowData.produce_plan_quantity);
        newData.produce_plan_quantity = value;
      },
      setQuantity(newData, value, currentRowData) {
        const {
          not_shipped,
          order_quantity,
          unit_price,
          basic_stock,
          closing_yn,
        } = currentRowData;

        newData.not_shipped = not_shipped + (value - order_quantity);
        newData.order_quantity = value;
        newData.unit_price = unit_price;
        if (closing_yn || !basic_stock || methods.isNotAssignQuantity()) {
          newData.assign_quantity = 0;
        } else {
          if (basic_stock.available_stock >= newData.not_shipped) {
            newData.assign_quantity = newData.not_shipped;
          } else {
            newData.assign_quantity = basic_stock.available_stock;
          }
        }
        newData.supply_price = newData.order_quantity * newData.unit_price;
      },
      setUnitPrice(newData, value, currentRowData) {
        newData.order_quantity = currentRowData.order_quantity;
        newData.unit_price = value;
        newData.supply_price = newData.order_quantity * newData.unit_price;
      },
      setProjectManagement(newData, value, currentRowData){
        if(!value) return;
        newData.project_management = value;
        newData.fk_project_management_id = value.id;
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

            if (currentRowData.closing_yn || !basicStock || methods.isNotAssignQuantity()) {
              newData.assign_quantity = 0;
            } else {
              if (basicStock.available_stock >= currentRowData.not_shipped) {
                newData.assign_quantity = currentRowData.not_shipped;
              } else {
                newData.assign_quantity = basicStock.available_stock;
              }
            }
            break;
          }
        }
      },
      loadBaseCode() {
        return baseCodeLoader([
          '부가세구분',
          '수주구분',
          '결재조건',
          '납품장소',
          '자산구분', 
          '품목그룹',
        ])
          .then((response) => {
            vars.dataSource.payment_terms = response['결재조건'];
            vars.dataSource.order_type = response['수주구분'];
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
          vars.filter.baseItem.clientId,
          vars.warehouse.wh_code
        );
      },
      loadQuoteItem() {
        vars.dataSource.quoteItem = getShipmentQuoteItem([
          {
            name: 'quote',
            op: 'has',
            val: {
              name: 'client_company',
              op: 'eq',
              val: vars.filter.quoteItem.clientCompany,
            },
          },
        ]);
      },
      loadProjectItem() {
        vars.dataSource.projectItem = getProjectItem([
          {
            name: 'project_management',
            op: 'has',
            val: {
              name: 'id',
              op: 'eq',
              val: vars.formData.fk_project_management_id,
            },
          },
          { name: 'not_ordered', op: 'gt', val: 0 },
        ]);
      },
      checkPossibleSave() {
        if (methods.isFilledFormRequiredData() && !methods.isOrderConfirmed()) {
          methods.syncStatusSave();
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
        if (!itemList || itemList.length <= 0) {
          return '';
        } else {
          return itemList[0].code_name;
        }
      },
      redirect(id) {
        if (id) {
          router.replace({ path: `/shipment/order/${id}` });
        } else {
          router.replace({ path: `/shipment/order` });
        }
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
      syncStatusDelete() {
        if (methods.isFormReadOnly()) {
          vars.disabled.delete = true;
        } else {
          vars.disabled.delete = false;
        }
      },
      syncStatusSave() {
        if (methods.isFormReadOnly()) {
          vars.disabled.save = true;
        } else {
          vars.disabled.save = false;
        }
      },
      disableAllAction() {
        vars.disabled.edit = true;
        vars.disabled.delete = true;
        vars.disabled.save = true;
        vars.disabled.manager = true;
        vars.disabled.clientManager = true;
      },
      async exportToRelease() {
        if (!vars.formData.id) {
          return;
        }
        const params = { order_id: vars.formData.id };
        try {
          await vars.api.exportToRelease.post('', params);
          await alert('출고로 보내기가 완료되었습니다', '출고로 보내기');

          methods.loadOrderData(vars.formData.id);
          methods.gridItem1Refresh(vars.formData.id);
        } catch (ex) {
          if (ex.response.status == 608) {
            await alert('미출고 수량이 없습니다', '출고로 보내기');
          } else {
            await alert('출고로 보내기가 실패했습니다', '출고로 보내기');
          }
        }
      },
      async redirectToRelease() {
        if (!vars.formData.release_number) {
          await alert('출고번호가 존재하지 않습니다', '출고로 이동');
          return;
        }
        const response = await shipmentRelease.load({
          filter: [
            ['release_number', '=', vars.formData.release_number],
            ['fk_company_id', '=', authService.getCompanyId()],
          ],
        });
        if (response.data.length > 0) {
          router.replace({ path: `/shipment/release/${response.data[0].id}` });
        } else {
          await alert('출고번호가 존재하지 않습니다', '출고로 이동');
        }
      },
      clientManagerExpr(item) {
        if (!item) return '';
        if (item.mobile) {
          vars.formData.client_manager_phone = item.mobile;
        }
        return item.name;
      },
      async copyItem() {
        methods.showLoading();

        const params = Object.assign(vars.formData);
        // UTC to KST (UTC + 9시간)
        const curr = new Date();
        const utc = curr.getTime();
        const KR_TIME_DIFF = 9 * 60 * 60 * 1000;
        params.order_date = new Date(utc + (KR_TIME_DIFF));
        params.confirmed = false
        params.approve = false
        delete params.id;
        delete params.created;
        delete params.order_number;
        delete params.release_number;

        let { data } = await shipmentOrder.insert(params);
        const gridItem1 = vars.grid.item1;
        if (gridItem1 && gridItem1.hasEditData()) {
          await gridItem1.saveEditData();
        }
        const ds = getShipmentOrderItem();
        const rows = gridItem1.getVisibleRows();
        for (const row of rows) {
          let assignQuantity = row.data.order_quantity;
          if (row.data.basic_stock.available_stock < row.data.order_quantity) {
            assignQuantity = row.data.basic_stock.available_stock;
          }
          if (methods.isNotAssignQuantity()) {
            assignQuantity = 0;
          }

          const newItem = {
            fk_order_id: data.id,
            assign_quantity: assignQuantity,
            produce_plan_quantity: row.data.order_quantity - assignQuantity,
            not_produce_plan_quantity: row.data.order_quantity - assignQuantity,
            not_shipped: row.data.order_quantity,
            client_item_number: row.data.client_item_number,
            closing_yn: false,
            fk_project_item_id: row.data.fk_project_item_id,
            fk_quote_item_id: row.data.fk_quote_item_id,
            item_code: row.data.item_code,
            note: row.data.note,
            order_quantity: row.data.order_quantity,
            fk_project_management_id: row.data.fk_project_management_id,
            quote_item: row.data.quote_item,
            quote_number: row.data.quote_number,
            request_delivery_date: row.data.request_delivery_date,
            supply_price: row.data.supply_price,
            unit_price: row.data.unit_price,
            warehouse_code: row.data.warehouse_code,
          };
          await ds.insert(newItem);

          await vars.api.updateItemStock.post('', {
            item_code: row.data.item_code,
            warehouse_code: row.data.warehouse_code
          });
        }

        methods.redirect(data.id);
        vars.formState.readOnly = true;
        notifyInfo('복사되었습니다');
        methods.hideLoading();
      },
      showLoading() {
        vars.loading.value = true;
      },
      hideLoading() {
        vars.loading.value = false;
      },
      isFormReadOnly() {
        return vars.formState.readOnly;
      },
      isOrderConfirmed() {
        return vars.formData.confirmed;
      },
      isFilledFormRequiredData() {
        if (vars.formData.client_company && vars.formData.order_department) {
          return true;
        }
        return false;
      },
      isNotAssignQuantity() {
        if (!vars.formData.order_type) {
          return false;
        }
        if (vars.formData.order_type.indexOf('반품') >= 0) {
          return true;
        }
        if (vars.formData.order_type == 'STOCK') {
          return true;
        }
        return false;
      },
      calculateCustomSummary(options) {
        if (options.name === 'supply_price') {
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          } else if (options.summaryProcess === 'calculate') {
            options.totalValue += options.value.order_quantity * options.value.unit_price;
          } else if (options.summaryProcess === 'finalize') {
            const response = calcPriceSummary(vars.formData.vat_type, options.totalValue);
            vars.formData.supply_price = response.supply_price;
            vars.formData.vat = response.vat;
            vars.formData.total_price = response.total_price;
          }
        }
      },
      async printDocument () {
        const params = {...vars.formData}
        params.procDateShort = moment().format('YYMMDD')
        const { data: item1 } = await vars.dataSource.item1.load()
        const items = item1.map((item, idx) =>{
          item.index = idx + 1;
          return item;
        })
        params.pages = chunk(items, 11)
        params.pages[params.pages.length -1]['total_supply_price'] = numeral(vars.formData.supply_price).format('0,0');
        const api = new ApiService('/api/mes/v1/shipment/summary-sales-balance')
        const { data: response } = await api.get(encodeURIComponent(params.client_company))
        params.balance = response
        params.balance.current_balance = (response.receivable_balance + response.release_balance) - response.deposit_balance
        params.etc = typeof params.etc === 'string' ? params.etc.replace(/\n/g, '<br>') : '';
        printDocument('shipment-order', params)
      }
    };

    watch(
      () => props.id,
      () => methods.initById(props.id)
    );

    return {
      vars,
      methods,
      shipmentQuoteItem,
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
