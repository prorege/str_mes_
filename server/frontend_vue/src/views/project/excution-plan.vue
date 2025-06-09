<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before"
              ><div class="content-title">실행계획등록</div></dx-item
            >
            <dx-item location="after">
              <div class="approval-status" v-if="vars.formData.approval_status">{{ vars.formData.approval_status }}</div>
            </dx-item>
            <dx-item
              location="after"
              locate-in-menu="auto"
              widget="dxButton"
              :options="{
                text: '신규',
                type: 'add',
                icon: 'add',
                disabled: vars.disabled.new,
                onClick: methods.newItem,
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
        <dx-form :form-data="vars.formData">
          <dx-group-item :col-count="5">
            <dx-group-item>
              <dx-simple-item
                data-field="excution_plan_number"
                :editorOptions="{
                  placeholder: '(자동 or 직접입력)',
                  ...generateItemButtonOption(
                    'search',
                    methods.createFindPopupFn('excution-plan', '실행계획조회')
                  ),
                }">
                <dx-label text="실행계획번호" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="project_management.project_number"
                :editor-options="{
                  onValueChanged: methods.onValueChanged,
                  ...generateItemButtonOption(
                    'search',
                    methods.createFindPopupFn('project', '프로젝트조회'),
                  ),
                  ...vars.formState,
                }"
              >
                <dx-label text="프로젝트번호" :show-colon="false" />
                <dx-required-rule message="프로젝트번호를 입력하세요" />
              </dx-simple-item>
              <dx-simple-item
                data-field="project_management.project_name"
                :editor-options="{
                  readOnly: true
                }"
              >
                <dx-label text="프로젝트명" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>

            <dx-group-item>
              <dx-simple-item
                data-field="excution_plan_date"
                editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  ...vars.formState
                }"
              >
                <dx-label text="등록일자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="excution_plan_department"
                editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.department,
                  displayExpr: 'department_name',
                  valueExpr: 'department_name',
                  onValueChanged: methods.selectDepartment,
                  ...vars.formState,
                }"
              >
                <dx-label text="등록부서" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="excution_plan_manager"
                editor-type="dxSelectBox"
                :editor-options="{
                  onValueChanged: methods.onValueChanged,
                  dataSource: vars.dataSource.employee,
                  displayExpr: 'emp_name',
                  valueExpr: 'emp_name',
                  disabled: vars.disabled.employee,
                  ...vars.formState,
                }"
              >
                <dx-label text="등록담당자" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>

            <dx-group-item>
              <dx-simple-item data-field="approval_status" editor-type="dxSelectBox" :editor-options="{
                  dataSource: vars.dataSource.approval_status,
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  ...vars.formState,
                }">
                  <dx-label text="결재상태" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="reject_reason"
                :editor-options="{
                  ...vars.formState,
                }"
              >
                <dx-label text="반려사유" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="business_completion_amount"
                editor-type="dxNumberBox"
                :editor-options="{
                  format: 'currency',
                  readOnly: true,
                  ...vars.formState,
                }"
                :set-cell-value="methods.setBusinessCompletionAmount"

              >
                <dx-label text="사업완료금액" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
              
            <dx-group-item>
              <dx-simple-item
                data-field="contract_amount"
                editor-type="dxNumberBox"
                :editor-options="{
                  format: 'currency',
                  ...vars.formState,
                }"
                
              >
                <dx-label text="계약금액" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="expect_amount"
                editor-type="dxNumberBox"
                :editor-options="{
                  format: 'currency',
                  readOnly: true,
                }"
              >
                <dx-label text="예정금액" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="excution_amount"
                editor-type="dxNumberBox"
                :editor-options="{
                  format: 'currency',
                  ...vars.formState,
                }"
              >
                <dx-label text="실행금액" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item
                data-field="contract_to_expect_rate"
                editor-type="dxNumberBox"
                :editor-options="{
                  format: '#0.0\'%\'',
                  ...vars.formState.readOnly,
                }">
                <dx-label text="계약대비예정률" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="expect_to_excution_rate"
                editor-type="dxNumberBox"
                :editor-options="{
                  format: '#0.0\'%\'',
                  ...vars.formState.readOnly
                }">
                <dx-label text="예정대비실행률" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="contract_to_excution_rate"
                editor-type="dxNumberBox"
                :editor-options="{
                  format: '#0.0\'%\'',
                  ...vars.formState.readOnly
                }">
                <dx-label text="계약대비실행률" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
          </dx-group-item>
        </dx-form>
      </div>

      <div class="dx-card responsive-paddings mt-1">
        <dx-tab-panel :animation-enabled="false" :swipe-enabled="false" :defer-rendering="false" >
          <dx-item title="주요자재">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 416px)"
                  column-resizing-mode="widget"
                  :on-initialized="
                    evt => methods.onGridInitialized(evt, 'projectExcutionPlanItem')
                  "
                  :remote-operations="false"
                  :data-source="vars.dataSource.projectExcutionPlanItem"
                  :show-borders="true"
                  :allow-column-reordering="true"
                  :allow-column-resizing="true"
                  :column-auto-width="true"
                  :select-text-on-edit-start="true"
                  :row-alternation-enabled="true"
                  :focused-row-enabled="true"
                  @data-error-occurred="methods.onDataError"
                  @saving="methods.onSavingItem"
                  @editing-start="methods.onEditingStartItem"
                  @focused-cell-changed="evt => methods.onFocusedCellChanged(evt, 'projectExcutionPlanItem')"
                  @cell-click="evt => methods.cellClick(evt, 'projectExcutionPlanItem')"
                >
                  <dx-grid-toolbar>
                    <dx-item template="addFromProject" location="before" :visible="!vars.formState.readOnly" />
                    <dx-item template="addFromExcutionPlan" location="before" :visible="!vars.formState.readOnly" />
                    <dx-item template="exportToPurchaseOrder" location="before" :visible="vars.formState.readOnly && vars.formData.id && vars.formData.approval_status == '승인완료'" />
                    <dx-grid-item template="itemAddRowButtonPlanItem" :visible="!vars.formState.readOnly"/>
                    <dx-grid-item template="itemSaveButtonPlanItem" location="after" :visible="false" />
                    <dx-grid-item name="revertButton" />
                    <dx-grid-item name="columnChooserButton" />
                  </dx-grid-toolbar>
                  <template #addFromProject>
                    <dx-button text="프로젝트에서 가져오기" icon="add" @click="methods.showAddProjectPopup" />
                  </template>
                  <template #addFromExcutionPlan>
                    <dx-button text="실행계획 복사" icon="add" @click="methods.showAddExcutionPlanPopup" />
                  </template>
                  <template #exportToPurchaseOrder>
                    <dx-button text="발주로 내보내기" icon="export" @click="methods.exportToPurchaseOrder('projectExcutionPlanItem')" />
                  </template>
                  <template #itemAddRowButtonPlanItem>
                    <dx-button text="품목찾기" icon="add" @click="methods.showAddPopup"/>
                  </template>
                  <template #itemSaveButtonPlanItem>
                      <dx-button text="저장" icon="save" @click="methods.itemSaveButton('projectExcutionPlanItem')" />
                  </template>
                  <dx-column type="buttons" :visible="!vars.formState.readOnly"/>
                  <dx-column 
                    caption="발주여부" 
                    data-field="closing_yn" 
                    data-type="boolean"
                    :allow-editing="false"
                  />
                  <dx-column 
                    caption="발주확정" 
                    data-field="confirmed" 
                    data-type="boolean"
                    :allow-editing="false"
                    :calculate-cell-value="methods.calcConfirmed"
                  />
                  <dx-column
                    data-field="item_code"
                    caption="품목코드"
                    :allow-editing="false"
                    :visible="true"
                  />
                  <dx-column
                    data-field="item.item_name"
                    caption="제품명"
                    :allow-editing="false"
                    :visible="true"
                  />
                  <dx-column
                    data-field="item.item_standard"
                    caption="규격"
                    :allow-editing="false"
                    :visible="true"
                  />
                  <dx-column
                    data-field="main_supplier"
                    caption="구매처"
                    :allow-editing="true"
                    :editor-options="{ ...generateItemButtonOption('search', methods.createFindPopupFn('main_supplier', '구매처 조회')) }"
                  >
                  </dx-column>
                  <dx-column
                    data-field="assign_quantity"
                    caption="할당수량"
                    data-type="number"
                    format="fixedPoint"
                    :allow-editing="false"  
                  />
                  <dx-column 
                    caption="가용재고" 
                    data-field="basic_stock.available_stock" 
                    data-type="number" 
                    format="fixedPoint" 
                    :allow-editing="false" 
                    :calculate-display-value="methods.availableStock" 
                  />
                  <dx-column 
                    caption="현재고" 
                    data-field="basic_stock.current_stock" 
                    data-type="number" 
                    format="fixedPoint" 
                    :allow-editing="false" 
                    :calculate-display-value="methods.currentStock" 
                  />
                  <dx-column 
                    caption="입고창고" 
                    data-field="warehouse.wh_name" 
                    :set-cell-value="methods.setWarehouse">
                    <dx-lookup 
                      value-expr="wh_name" 
                      display-expr="wh_name" 
                      :data-source="vars.dataSource.warehouse" />
                  </dx-column>
                  <dx-column
                    data-field="excution_plan_quantity"
                    caption="발주수량"
                    data-type="number"
                    :allow-editing="true"
                    :set-cell-value="methods.setExcutionPlanQuantity"
                  />
                  <dx-column
                    data-field="not_excution_plan_quantity"
                    caption="미발주수량"
                    data-type="number"
                    :allow-editing="false" 
                  />
                  <dx-column
                    data-field="unit_price"
                    caption="예정단가"
                    data-type="number"
                    format="currency"
                    :set-cell-value="methods.setUnitPrice"
                  />
                  <dx-column
                    data-field="purchase_unit_price"
                    caption="발주단가"
                    data-type="number"
                    format="currency"
                    :set-cell-value="methods.setItemPurchaseUnitPrice"
                  />
                  <dx-column
                    data-field="supply_price"
                    caption="예정금액"
                    data-type="number"
                    format="currency"
                    :allow-editing="false"
                  />
                  <dx-column
                    data-field="purchase_supply_price"
                    caption="발주금액"
                    data-type="number"
                    format="currency"
                    :allow-editing="false"
                  />
                  <dx-column
                    data-field="delivery_price"
                    caption="배송비"
                    data-type="number"
                    format="currency"
                  />
                  <dx-column data-field="vat_type" caption="VAT" :set-cell-value="methods.setVatType">
                    <dx-lookup 
                      :data-source="vars.dataSource.vat_type"
                      value-expr="code_name"
                      display-expr="code_name"
                    />
                  </dx-column>
                  <dx-column
                    data-field="vat"
                    caption="부가세"
                    data-type="number"
                    format="currency"
                    :allow-editing="false"  
                  />
                  <dx-column
                    data-field="delivery_require"
                    caption="납기소요"
                  />
                  <dx-column caption="납기일자" 
                    data-field="delivery_date" 
                    data-type="date" 
                    format="yyyy-MM-dd" 
                  />
                  <dx-column caption="발주일자"
                    data-field="order_date"
                    data-type="date"
                    format="yyyy-MM-dd"
                  />
                  <dx-column caption="변경납기일자"
                    data-field="order_date_modify"
                    data-type="date"
                    format="yyyy-MM-dd"
                    :set-cell-value="methods.setOrderDateModify"
                  />
                  <dx-column 
                    caption="비고" 
                    data-field="note" 
                  />
                  <dx-column 
                    caption="등록자" 
                    data-field="register"
                    :allow-editing="false"  
                  />
                  <dx-column caption="등록일자" 
                    data-field="created" 
                    data-type="date" 
                    format="yyyy-MM-dd" 
                    :allow-editing="false" 
                  />
                  <dx-column 
                    caption="수정자" 
                    data-field="modify_register" 
                    :allow-editing="false" 
                  />
                  <dx-column caption="수정일자" 
                    data-field="modify_date" 
                    data-type="date" 
                    format="yyyy-MM-dd" 
                    :allow-editing="false" 
                  />
                  <dx-summary :recalculate-while-editing="true" :calculate-custom-summary="methods.calcSummaryPlanItem">
                    <dx-total-item name="purchase_supply_price" summary-type="custom" />
                    <dx-total-item name="supply_price" summary-type="custom" />
                    <dx-total-item name="vat" summary-type="custom" />
                    <dx-total-item name="completion_price" summary-type="custom" />
                  </dx-summary>

                  <dx-editing
                    :allow-adding="!vars.formState.readOnly"
                    :allow-updating="!vars.formState.readOnly"
                    :allow-deleting="!vars.formState.readOnly"
                    mode="batch"
                  />
                  <dx-paging :enabled="false" />
                  <dx-scrolling mode="standard" />
                  <dx-column-chooser mode="select" :enabled="true" />
                </dx-data-grid>
              </div>
              <div class="mb-2 ml-2">
                <table class="summary-table">
                  <tr>
                    <th>예정 공급가:</th>
                    <td>{{ '₩' + numeral(vars.summary.planItem.supply_price).format('0,0') }}</td>
                    <th>예정 부가세:</th>
                    <td>{{ '₩' + numeral(vars.summary.planItem.vat).format('0,0') }}</td>
                    <th>예정 합계금액:</th>
                    <td>{{ '₩' + numeral(vars.summary.planItem.total_price).format('0,0') }}</td>
                    <th>실행금액:</th>
                    <td>{{ '₩' + numeral(vars.summary.planItem.completion_price).format('0,0') }}</td>
                  </tr>
                </table>
              </div>
            </template>
            
          </dx-item>
          <dx-item title="외주공사">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 416px)"
                  date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                  column-resizing-mode="widget"
                  :on-initialized="
                    evt => methods.onGridInitialized(evt, 'projectExcutionPlanSubcontract')
                  "
                  :remote-operations="false"
                  :data-source="vars.dataSource.projectExcutionPlanSubcontract"
                  :show-borders="true"
                  :allow-column-reordering="true"
                  :allow-column-resizing="true"
                  :column-auto-width="true"
                  :select-text-on-edit-start="true"
                  :row-alternation-enabled="true"
                  :focused-row-enabled="true"
                  @saving="methods.onSavingItem"
                  @focused-cell-changed="evt => methods.onFocusedCellChanged(evt, 'projectExcutionPlanSubcontract')"
                  @cell-click="evt => methods.cellClick(evt, 'projectExcutionPlanSubcontract')"
                >
                  <dx-grid-toolbar>
                      <dx-grid-item template="addRowButtonSubcontract" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item template="itemSaveButtonSubcontract" location="after" :visible="false" />
                      <dx-grid-item name="revertButton" location="after" />
                      <dx-item template="_exportToPurchaseOrder" location="before" :visible="vars.formState.readOnly && vars.formData.id && vars.formData.approval_status == '승인완료'" />
                  </dx-grid-toolbar>
                  <template #addRowButtonSubcontract>
                      <dx-button text="외주공사 추가" icon="add" @click="methods.showAddPopup2" />
                  </template>
                  <template #itemSaveButtonSubcontract>
                      <dx-button text="저장" icon="save" @click="methods.itemSaveButton('projectExcutionPlanSubcontract')" />
                  </template>
                  <template #_exportToPurchaseOrder>
                    <dx-button text="발주로 내보내기" icon="export" @click="methods.exportToPurchaseOrder('projectExcutionPlanSubcontract')" />
                  </template>
                  <dx-column type="buttons" :visible="!vars.formState.readOnly"/>
                  <dx-column data-field="closing_yn" caption="발주여부" data-type="boolean" :width="80" :allow-editing="false" />
                  <dx-column data-field="subcontract_name" caption="공사명" />
                  <dx-column data-field="subcontract_company" caption="공사업체" :editor-options="{ 
                    ...generateItemButtonOption('search', methods.createFindPopupFn('subcontract_company', '업체 조회')) }" />
                  <dx-column data-field="expect_amount" caption="예정가격" data-type="number" format="currency" :set-cell-value="methods.setSubcontractExpectAmount"/>
                  <dx-column data-field="purchase_unit_price" caption="발주단가" data-type="number" format="currency" :set-cell-value="methods.setPurchaseUnitPrice" />
                  <dx-column data-field="vat_type" caption="VAT" :set-cell-value="methods.setSubcontractVatType">
                    <dx-lookup 
                      :data-source="vars.dataSource.vat_type"
                      value-expr="code_name"
                      display-expr="code_name"
                    />
                  </dx-column>
                  <dx-column data-field="vat" caption="부가세" data-type="number" format="currency" :allow-editing="false" />
                  <dx-column data-field="estimate_document" caption="견적서" cell-template="downloadEstimateDocument" edit-cell-template="uploadEstimateDocument" />
                  <dx-column data-field="contract_document" caption="계약서" cell-template="downloadContractDocument" edit-cell-template="uploadContractDocument" />
                  <dx-column data-field="contract_performance_bond" caption="계약이행증권" cell-template="downloadContractPerformanceBond" edit-cell-template="uploadContractPerformanceBond" />
                  <dx-column data-field="defect_liability_bond" caption="하자이행증권" cell-template="downloadDefectLiabilityBond" edit-cell-template="uploadDefectLiabilityBond" />
                  <dx-column data-field="start_date" caption="시작일자" data-type="date" format="yyyy-MM-dd" />
                  <dx-column data-field="end_date" caption="종료일자" data-type="date" format="yyyy-MM-dd" />
                  <dx-column data-field="register" caption="등록자" :allow-editing="false"  />
                  <dx-column data-field="created" caption="등록일자" data-type="date" format="yyyy-MM-dd" :allow-editing="false" />
                  <!-- 견적서 등록 -->
                  <template #downloadEstimateDocument="{data}">
                    <a :href="`/api/mes/v1/${data.data['estimate_document_path']}/${data.data['estimate_document']}`" download>{{data.data[data.column.dataField]}}</a>
                  </template>
                  <template #uploadEstimateDocument="{data}">
                    <dx-text-box :value="data.data[data.column.dataField]">
                      <dx-text-box-button location="after" name="upload"
                        :options="{
                          hint: '업로드', icon: 'upload',
                          onClick: methods.addFile(data)
                        }"
                      />
                    </dx-text-box>
                  </template>
                  <!-- 계약서 -->
                  <template #downloadContractDocument="{data}">
                    <a :href="`/api/mes/v1/${data.data['contract_document_path']}/${data.data['contract_document']}`" download>{{data.data[data.column.dataField]}}</a>
                  </template>
                  <template #uploadContractDocument="{data}">
                    <dx-text-box :value="data.data[data.column.dataField]">
                      <dx-text-box-button location="after" name="upload"
                        :options="{
                          hint: '업로드', icon: 'upload',
                          onClick: methods.addFile(data)
                        }"
                      />
                    </dx-text-box>
                  </template>
                  <template #downloadContractPerformanceBond="{data}">
                    <a :href="`/api/mes/v1/${data.data['contract_performance_bond_path']}/${data.data['contract_performance_bond']}`" download>{{data.data[data.column.dataField]}}</a>
                  </template>
                  <template #uploadContractPerformanceBond="{data}">
                    <dx-text-box :value="data.data[data.column.dataField]">
                      <dx-text-box-button location="after" name="upload"
                        :options="{
                          hint: '업로드', icon: 'upload',
                          onClick: methods.addFile(data)
                        }"
                      />
                    </dx-text-box>
                  </template>
                  <template #downloadDefectLiabilityBond="{data}">
                    <a :href="`/api/mes/v1/${data.data['defect_liability_bond_path']}/${data.data['defect_liability_bond']}`" download>{{data.data[data.column.dataField]}}</a>
                  </template>
                  <template #uploadDefectLiabilityBond="{data}">
                    <dx-text-box :value="data.data[data.column.dataField]">
                      <dx-text-box-button location="after" name="upload"
                        :options="{
                          hint: '업로드', icon: 'upload',
                          onClick: methods.addFile(data)
                        }"
                      />
                    </dx-text-box>
                  </template>
                  <dx-summary :recalculate-while-editing="true" :calculate-custom-summary="methods.calcSummarySubcontract">
                    <dx-total-item name="expect_amount" summary-type="custom" />
                    <dx-total-item name="purchase_unit_price" summary-type="custom" />
                    <dx-total-item name="vat" summary-type="custom" />
                    <dx-total-item name="completion_price" summary-type="custom" />

                  </dx-summary>


                  <dx-editing
                    :allow-adding="!vars.formState.readOnly"
                    :allow-updating="!vars.formState.readOnly"
                    :allow-deleting="!vars.formState.readOnly"
                    mode="batch"
                  />
                  <dx-paging :enabled="false" />
                  <dx-scrolling mode="standard" />
                </dx-data-grid>
              </div>
              <div class="mb-2 ml-2">
                <table class="summary-table">
                  <tr>
                    <th>예정 공급가:</th>
                    <td>{{ '₩' + numeral(vars.summary.planSubcontract.supply_price).format('0,0') }}</td>
                    <th>예정 부가세:</th>
                    <td>{{ '₩' + numeral(vars.summary.planSubcontract.vat).format('0,0') }}</td>
                    <th>예정 합계금액:</th>
                    <td>{{ '₩' + numeral(vars.summary.planSubcontract.total_price).format('0,0') }}</td>
                    <th>실행금액:</th>
                    <td>{{ '₩' + numeral(vars.summary.planSubcontract.completion_price).format('0,0') }}</td>                    
                  </tr>
                </table>
              </div>
            </template>
          </dx-item>
          <dx-item title="경비">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 416px)"
                  date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                  column-resizing-mode="widget"
                  :on-initialized="
                    evt => methods.onGridInitialized(evt, 'projectExcutionPlanExpense')
                  "
                  :remote-operations="false"
                  :data-source="vars.dataSource.projectExcutionPlanExpense"
                  :show-borders="true"
                  :allow-column-reordering="true"
                  :allow-column-resizing="true"
                  :column-auto-width="true"
                  :select-text-on-edit-start="true"
                  :row-alternation-enabled="true"
                  :focused-row-enabled="true"
                  @saving="methods.onSavingItem"
                  @init-new-row="evt => methods.initNewRow(evt, 'projectExcutionPlanExpense')"
                >
                  <dx-grid-toolbar>
                      <dx-grid-item template="addRowButtonExpense" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item template="itemSaveButtonExpense" location="after" :visible="false" />
                      <dx-grid-item name="revertButton" location="after" />
                  </dx-grid-toolbar>
                  <template #addRowButtonExpense>
                      <dx-button text="경비 추가" icon="add" @click="methods.addItemRowButton('projectExcutionPlanExpense')" />
                  </template>
                  <template #itemSaveButtonExpense>
                      <dx-button text="저장" icon="save" @click="methods.itemSaveButton('projectExcutionPlanExpense')" />
                  </template>
                  <dx-column type="buttons" :visible="!vars.formState.readOnly"/>
                  <dx-column data-field="expense_description" caption="경비내역">
                    <dx-lookup 
                      :data-source="vars.dataSource.expense_description"
                      value-expr="code_name"
                      display-expr="code_name"
                    />
                  </dx-column>
                  <dx-column data-field="expense_amount" caption="예정소요경비" data-type="number" format="currency" :set-cell-value="methods.setExpenseAmount" />
                  <dx-column data-field="excution_amount" caption="소요경비" data-type="number" format="currency" />
                  <dx-column data-field="day_amount" caption="일수" data-type="number" :editor-options="{readOnly: true}" :format="{ type: 'fixedPoint', precision: 1 }"/>
                  <dx-column data-field="time_amount" caption="시간" data-type="number" format="currency" :set-cell-value="methods.setExpenseTimeAmount"/>
                  <dx-column data-field="plan_amount" caption="계획소요경비" data-type="number" format="currency" :editor-options="{readOnly: true}"/>
                  <dx-column data-field="vat_type" caption="VAT" :set-cell-value="methods.setExpenseVatType">
                    <dx-lookup 
                      :data-source="vars.dataSource.vat_type"
                      value-expr="code_name"
                      display-expr="code_name"
                    />
                  </dx-column>
                  <dx-column data-field="vat" caption="부가세" data-type="number" format="currency" :allow-editing="false" />
                  <dx-column data-field="expense_source" caption="지출처" />
                  <dx-column data-field="expense_date" caption="지출일자" data-type="date" format="yyyy-MM-dd" />
                  <dx-column data-field="register" caption="등록자" :allow-editing="false"  />
                  <dx-column data-field="created" caption="등록일자" data-type="date" format="yyyy-MM-dd" :allow-editing="false" />
                  <dx-summary :recalculate-while-editing="true" :calculate-custom-summary="methods.calcSummaryExpense">
                    <dx-total-item name="expense_amount" summary-type="custom" />
                    <dx-total-item name="excution_amount" summary-type="custom" />
                    <dx-total-item name="vat" summary-type="custom" />
                    <dx-total-item name="completion_price" summary-type="custom" />

                  </dx-summary>

                  <dx-editing mode="batch"
                    :allow-adding="!vars.formState.readOnly"
                    :allow-updating="!vars.formState.readOnly"
                    :allow-deleting="!vars.formState.readOnly"
                  />
                  <dx-paging :enabled="false" />
                  <dx-scrolling mode="standard" />
                </dx-data-grid>
              </div>
              <div class="mb-2 ml-2">
                <table class="summary-table">
                  <tr>
                    <th>예정 공급가:</th>
                    <td>{{ '₩' + numeral(vars.summary.planExpense.supply_price).format('0,0') }}</td>
                    <th>예정 부가세:</th>
                    <td>{{ '₩' + numeral(vars.summary.planExpense.vat).format('0,0') }}</td>
                    <th>예정 합계금액:</th>
                    <td>{{ '₩' + numeral(vars.summary.planExpense.total_price).format('0,0') }}</td>
                    <th>실행 금액:</th>
                    <td>{{ '₩' + numeral(vars.summary.planExpense.completion_price).format('0,0') }}</td>
                  </tr>
                </table>
              </div>
            </template>
          </dx-item>
        </dx-tab-panel>
      </div>
    </div>

    <dx-popup
      v-model:visible="vars.dlg.addItem.show"
      content-template="popup-content"
      title="품목찾기"
      :close-on-outside-click="true"
      width="70%"
      :height="500"
      :resize-enabled="true"
      @hidden="methods.addItemHidden"
      @initialized="evt => methods.onGridInitialized(evt, 'add-base-item-popup')"
    >
      <template #popup-content>
        <popup-item
          :filters="vars.filter.baseItem"
          :toggle="vars.dlg.addItem.show"
          @baseItemChange="methods.addSelectedRows"
        />
      </template>
    </dx-popup>

    <dx-popup
      v-model:visible="vars.dlg.addItem2.show"
      content-template="popup-content"
      title="외주공사찾기"
      :close-on-outside-click="true"
      width="70%"
      :height="500"
      :resize-enabled="true"
      @hidden="methods.addItemHidden"
      @initialized="evt => methods.onGridInitialized(evt, 'add-base-item-popup')"
    >
      <template #popup-content>
        <popup-item
          :filters="vars.filter.baseItem"
          :toggle="vars.dlg.addItem2.show"
          @baseItemChange="methods.addSelectedRows2"
        />
      </template>
    </dx-popup>

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
        <data-grid-client
          v-if="vars.dlg.finder.key === 'subcontract_company'"
          :filters="vars.dlg.finder.data"
          @change="methods.finderReturnHandler"
        />
        <data-grid-client
          v-else-if="vars.dlg.finder.key === 'main_supplier'"
          :filters="vars.dlg.finder.data"
          @change="methods.finderReturnHandler"
        />
        <data-grid-project
          v-else-if="vars.dlg.finder.key === 'project'"
          @change="methods.finderReturnHandler"
        />
        <data-grid-excution-plan v-else-if="vars.dlg.finder.key === 'excution-plan'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <div v-else-if="vars.dlg.finder.key === 'etc'">
          <div class="mb-2">
            <dx-text-area
              :height="440"
              :value="vars.dlg.finder.data"
              @update:value="methods.updateEtcValue"
            />
          </div>
          <dx-toolbar>
            <dx-item
              widget="dxButton"
              toolbar="top"
              location="after"
              :options="{
                icon: null,
                text: '닫기',
                onClick: methods.finderReturnHandler,
              }"
            />
          </dx-toolbar>
        </div>
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
      @initialized="(evt) => methods.onGridInitialized(evt, 'find-project-item-popup')"
    >
      <template #popup-content>
        <dx-data-grid
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="vars.dataSource.projectItem"
          :on-initialized="(evt) => methods.onGridInitialized(evt, 'projectItem')"
        >
          <dx-grid-toolbar>
            <dx-item template="addItemButton" location="before" />
          </dx-grid-toolbar>
          <template #addItemButton>
            <dx-button text="선택된 항목 추가" icon="add" @click="methods.addSelectedProjectRows" />
          </template>
          <dx-column caption="프로젝트번호" data-field="project_management.project_number" />
          <dx-column caption="프로젝트명" data-field="project_management.project_name" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="수량" data-field="quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="미수주수량" data-field="not_ordered" data-type="number" format="fixedPoint" />

          <dx-paging :page-size="20" />
          <dx-sorting mode="multiple"/>
          <dx-filter-row :visible="true" />
          <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick" />
        </dx-data-grid>
      </template>
    </dx-popup>

    <dx-popup
      title="실행계획 찾기"
      content-template="popup-content"
      v-model:visible="vars.dlg.addExcutionPlan.show"
      :width="680"
      :height="500"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="(evt) => methods.onGridInitialized(evt, 'find-excution-plan-popup')"
    >
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ text: '선택된 항목 추가', icon: 'add', onClick: methods.addSelectedExcutionPlan }"
      />

      <template #popup-content>
        <dx-data-grid
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="vars.dataSource.excutionPlan"
          :on-initialized="(evt) => methods.onGridInitialized(evt, 'excutionPlan')"
        >
          <dx-column caption="실행계획번호" data-field="excution_plan_number" />
          <dx-column caption="프로젝트번호" data-field="project_management.project_number" />
          <dx-column caption="프로젝트명" data-field="project_management.project_name" />
          <dx-column caption="등록일자" data-field="excution_plan_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="담당부서" data-field="excution_plan_department" />
          <dx-column caption="등록자" data-field="excution_plan_manager" />

          <dx-paging :page-size="20" />
          <dx-sorting mode="multiple"/>
          <dx-filter-row :visible="true" />
          <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick" />
        </dx-data-grid>
      </template>
    </dx-popup>
  </div>
</template>

<script>
import moment from 'moment';
import numeral from 'numeral';
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
  DxSummary,
  DxTotalItem,
  DxRequiredRule as DxGridRequiredRule,
} from 'devextreme-vue/data-grid';
import { DxTabPanel } from 'devextreme-vue/tab-panel';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxTextBox, DxButton as DxTextBoxButton } from 'devextreme-vue/text-box';
import { DxButton } from 'devextreme-vue/button';
import { DxFileUploader } from 'devextreme-vue/file-uploader';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import { confirm, alert } from 'devextreme/ui/dialog';
import { onMounted, ref, reactive, computed, watch, nextTick} from 'vue';
import { useRouter } from 'vue-router';
import stateStore from '@/utils/state-store';
import ArrayStore from 'devextreme/data/array_store';
import {
  projectExcutionPlan,
  getProjectExcutionPlan,
  projectExcutionPlanItem,
  getProjectExcutionPlanItem,
  projectExcutionPlanSubcontract,
  getProjectExcutionPlanSubcontract,
  projectExcutionPlanExpense,
  getProjectExcutionPlanExpense,
  getProjectItem,
  projectItem,
  projectRegistration,
} from '../../data-source/project';
import {
  shipmentQuoteItem,
} from '../../data-source/shipment';
import {
  baseCodeLoader,
  baseClient,
  baseItem,
  baseDepartment,
  baseEmployee,
  baseBom,
  baseBomLink,
} from '../../data-source/base';
import { approvalManagement } from '../../data-source/approval';
import { baseClientItem } from '../../data-source/base';
import DataGridClient from '../../components/base/data-client.vue';
import DataGridProject from '../../components/project/data-project.vue';
import DataGridExcutionPlan from '@/components/project/data-excution-plan.vue';
import PopupItem from '../../components/base/popup-item.vue';
import authService from '../../auth';
import ApiService from '../../utils/api-service';
import { notifyInfo, notifyError } from '../../utils/notify';
import { beforeExitConfirm, generateItemButtonOption, currentDateTime, calcPriceSummary} from '../../utils/util';
import { loadEmployee, loadWarehouse, loadDepartment, loadClientManager } from '../../utils/data-loader';
import { getStock, setupBasicStock } from '../../data-source/setup';

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
    DxToolbarItem,
    DxScrolling,
    DxColumnChooser,
    DxPaging,
    DataGridClient,
    DataGridProject,
    DxRequiredRule,
    DxGridRequiredRule,
    DxGridToolbar,
    DxGridItem,
    DataGridExcutionPlan,
    DxSorting,
    DxSummary,
    DxTotalItem,
    PopupItem,
  },
  props: {
    id: [String, Number],
    project_id: [String, Number],
  },
  setup(props) {
    
    // variable 설정
    const uploadService = new ApiService('/api/mes/v1/project-excution-plan-subcontract/upload');
    const router = useRouter();
    const vars = { dlg: {} };
    vars.init = ref(false);
    vars.loading = ref(false);
    vars.formState = reactive({ readOnly: true });
    vars.focus = reactive({ projectExcutionPlanSubcontract: null,});
    vars.warehouse = {};
    vars.grid = {
      projectExcutionPlanItem: null,
      projectExcutionPlanSubcontract: null,
      projectExcutionPlanExpense: null,
    };
    vars.dlg.addItem = reactive({ show: false });
    vars.dlg.addItem2 = reactive({ show: false });
    vars.dlg.addProjectItem = reactive({ show: false });
    vars.dlg.addExcutionPlan = reactive({ show: false });
    vars.dlg.finder = reactive({
      show: false,
      title: '',
      key: null,
      data: null,
    });
    vars.formData = reactive({
      project_management: null,
      id: null,
      created: null, // 생성시간
      excution_plan_number: '', 
      excution_plan_date: null, 
      excution_plan_department: '', 
      excution_plan_manager: '', 
      approval_status: '',
      reject_reason: '',
      contract_amount: 0,
      expect_amount: 0,
      excution_amount: 0,
      business_completion_amount: 0,
      contract_to_expect_rate: 0,
      expect_to_excution_rate: 0,
      contract_to_excution_rate: 0,
      modify_manager: '',
      modify_date: null,
      fk_project_management_id: null,
      fk_company_id: authService._user.fk_company_id,
    });
    
    vars.filter = reactive({
      projectItem: [
        {
          name: 'project_management',
          op: 'has',
          val: {
            name: 'id',
            op: 'eq',
            val: 0
          },
        },
      ],
      projectExcutionPlanItem: [
        {
          name: 'fk_project_excution_plan_id',
          op: 'eq',
          val: props.id || 0,
        },
      ],
      projectExcutionPlanSubcontract: [
        {
          name: 'fk_project_excution_plan_id',
          op: 'eq',
          val: props.id || 0,
        },
      ],
      projectExcutionPlanExpense: [
        {
          name: 'fk_project_excution_plan_id',
          op: 'eq',
          val: props.id || 0,
        },
      ],
      baseItem: null,
    });
    vars.dataSource = reactive({
      projectItem: null,
      excutionPlan: null,
      projectExcutionPlanItem: null,
      projectExcutionPlanSubcontract: null,
      projectExcutionPlanExpense: null,
      department: null,
      employee: null,
      approval_status: null,
      vat_type: null,
      expense_description: null,
      warehouse: null,
      setup_md: null,
    });
    vars.dataSource.projectExcutionPlanItem = getProjectExcutionPlanItem(vars.filter.projectExcutionPlanItem);

    vars.dataSource.projectExcutionPlanSubcontract = getProjectExcutionPlanSubcontract(vars.filter.projectParticipant);

    vars.dataSource.projectExcutionPlanExpense = getProjectExcutionPlanExpense(vars.filter.projectCompany);

    vars.dataSource.excutionPlan = getProjectExcutionPlan();

    vars.disabled = reactive({
      edit: true,
      delete: true,
      save: true,
      employee: null,
    });

    vars.summary = reactive({
      planItem: {},
      planSubcontract: {},
      planExpense: {},
    })
    vars.attchFiles = reactive({})

    onMounted(async () => {
      const api = new ApiService('/api/mes/v1/setup/md');
      const response = await api.get(); // ← 반드시 await!
      vars.dataSource.setup_md = response.data; // 배열로 할당
      console.log('불러온 setup_md:', vars.dataSource.setup_md); // ✅ 여기에 추가

      await loadDepartment(vars.dataSource);
      await methods.loadBaseCode();
      methods.initById(props.id);
      loadWarehouse(vars.dataSource);
      if(props.project_id){
        await methods.initByProject(props.project_id);
      }
      console.log("저장 직전 데이터", vars.formData);

    });

    // public methods
    const methods = {
      async initById(id) {  
        methods.gridRefresh(id, 'projectExcutionPlanItem');
        methods.gridRefresh(id, 'projectExcutionPlanSubcontract');
        methods.gridRefresh(id, 'projectExcutionPlanExpense');
        if (!id) {
          methods.clearFormData();
          methods.disableAllAction();
          return;
        }
        try{
          let { data } = await projectExcutionPlan.byKey(id);
          Object.assign(vars.formData, data);
        }
        catch(e){
          if(e.response.status === 404) {
            return methods.redirect();
          }
        }
        methods.setBusinessCompletionAmount(vars.formData);
      },
      clearFormData() {
        vars.formData.project_management = null;
        vars.formData.id = null;
        vars.formData.created = null;
        vars.formData.excution_plan_number = '';
        vars.formData.excution_plan_date = null, 
        vars.formData.excution_plan_department = '', 
        vars.formData.excution_plan_manager = '',
        vars.formData.approval_status = '',
        vars.formData.reject_reason = '',
        vars.formData.contract_amount = 0,
        vars.formData.expect_amount = 0,
        vars.formData.excution_amount = 0,
        vars.formData.contract_to_expect_rate = 0,
        vars.formData.expect_to_excution_rate = 0,
        vars.formData.contract_to_excution_rate = 0,
        vars.formData.modify_manager = '',
        vars.formData.modify_date = null,
        vars.formData.fk_project_management_id = null;
        vars.formData.fk_company_id = authService.getCompanyId();
      },
      disableAllAction(){
        vars.disabled.new = false;
        vars.disabled.edit = true;
        vars.disabled.delete = true;
        vars.disabled.save = true;
        vars.disabled.printDocument = true;
        vars.disabled.employee = true;
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
        stateStore.bind(key, evt.component);
      },
      loadBaseCode(){
        return baseCodeLoader(['결재상태', '부가세구분', '경비내역']).then(response =>{
        vars.dataSource.approval_status = response['결재상태']
        vars.dataSource.vat_type = response['부가세구분']
        vars.dataSource.expense_description = response['경비내역']
        })
        .then(() => (vars.init.value = true));
      },
      async newItem() {
        if (vars.formData.id || vars.formData.fk_project_management_id) {
          methods.clearFormData();
          methods.redirect();
        }
        setTimeout(() => {
          methods.clearFormData();
          methods.setFormData();
        }, 200);
      },
      async initByProject(project_id){
        const { data : project } = await projectRegistration.load({
          filter: [
            ['id', '=', project_id]
          ]
        });
        const { data : items} = await projectItem.load({
          filter: [
            ['fk_project_management_id', '=', project_id]
          ]
        });
        methods.addSelectedProjectRows(items);
        vars.formData.project_management = project[0];
        vars.formData.fk_project_management_id = project_id;
        vars.formData.contract_amount = project[0].company_amount;
        methods.setFormData()
      },
      setExpenseTimeAmount(newData, value) {
        parseFloat(value);
        newData.time_amount = value;
        newData.day_amount = Math.round((value / 8) * 10) / 10;

        const mdList = vars.dataSource.setup_md?.objects;
        const mdRow = Array.isArray(mdList)
          ? mdList.find(row => row.name === 'M/D')
          : null;

        if (mdRow) {
          newData.plan_amount = (newData.day_amount * mdRow.md);
        } else {
          console.warn('M/D 단가를 찾을 수 없습니다');
          newData.plan_amount = 0;
        }

        // if (!isNaN(value) && mdRow && mdRow.md) {
        //   newData.plan_amount = value * mdRow.md;
        // } else {
        //   newData.plan_amount = 0;
        // }
      },
      setFormData(){
        vars.formData.excution_plan_department = authService.getDepartmentName();
        vars.formData.excution_plan_manager = authService.getUserName();
        vars.formData.excution_plan_date = currentDateTime();
        vars.formData.fk_company_id = authService.getCompanyId();
        vars.formData.approval_status = methods.getFirstItemName(vars.dataSource.approval_status);

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
      async gridRefresh(id, item) {
        if (!id) id = 0;
        vars.filter[item][0].val = id;
        vars.dataSource[item].defaultFilters = vars.filter[item];
        if (vars.grid[item]) {
          vars.grid[item].cancelEditData();
          vars.grid[item].refresh();
        }
      },
      finderReturnHandler(data) {
        switch (vars.dlg.finder.key) {
          case 'excution-plan': {
            methods.redirect(data.id);
            vars.formState.readOnly = true;
            break
          }
          case 'project': {
            vars.formData.fk_project_management_id = data.id;
            vars.formData.project_management = data;
            vars.formData.contract_amount = data.company_amount;
            break;
          }
          case 'subcontract_company': {
            const focus = vars.focus.projectExcutionPlanSubcontract;
            const grid = vars.grid.projectExcutionPlanSubcontract;
            if(focus){
              grid.cellValue(focus.rowIndex, focus.columnIndex, data.name);
            }else{
              grid.cellValue(0, 0, data.name);
            }
            break;
          }
          case 'main_supplier': {
            const focus = vars.focus.projectExcutionPlanItem;
            const grid = vars.grid.projectExcutionPlanItem;
            if(focus){
              grid.cellValue(focus.rowIndex, focus.columnIndex, data.name);
            }else{
              grid.cellValue(0, 0, data.name);
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
      updateEtcValue(v) {
        vars.dlg.finder.data = v;
      },
      // async saveItem() {
      //   let isSelect = await confirm('저장하시겠습니까?', '저장');
      //   if (!isSelect) return;

      //   vars.loading.value = true;

      //   try {
      //     const planItem = vars.grid.projectExcutionPlanItem;
      //     const planSubcontract = vars.grid.projectExcutionPlanSubcontract;
      //     const planExpense = vars.grid.projectExcutionPlanExpense;

      //     if (vars.formData.id) {
      //       // 기존 정보 업데이트
      //       vars.formData.modify_manager = authService.getUserName();
      //       vars.formData.modify_date = moment().format('YYYY-MM-DD HH:mm:ss');

      //       const updateDate = Object.assign({}, vars.formData);

      //       // ✅ 저장에 불필요한 필드 제거
      //       delete updateDate.created;
      //       delete updateDate.excution_plan_number;
      //       delete updateDate.project_management;

      //       // ✅ NaN 값 방지
      //       ['excution_amount', 'time_amount', 'day_amount', 'plan_amount'].forEach(field => {
      //         if (isNaN(updateDate[field])) {
      //           updateDate[field] = 0;
      //         }
      //       });

      //       // ✅ 콘솔 디버깅용 (최종 데이터 확인)
      //       console.log("🔍 저장 대상 필드 목록:", Object.keys(updateDate));
      //       console.log("📝 저장 데이터:", updateDate);

      //       // PATCH 요청
      //       const { data } = await projectExcutionPlan.update(vars.formData.id, updateDate);
      //       vars.formData.excution_plan_number = data.excution_plan_number;

      //       if (planItem) await planItem.saveEditData();
      //       if (planSubcontract) await planSubcontract.saveEditData();
      //       if (planExpense) await planExpense.saveEditData();

      //       await methods.approvalRequest();

      //       vars.formState.readOnly = true;
      //       methods.enableSave();
      //       methods.enableEdit();
      //       methods.enableDelete();
      //       notifyInfo('저장되었습니다');

      //     } else {
      //       // 신규 등록 시
      //       delete vars.formData.created;
      //       delete vars.formData.id;

      //       let { data } = await projectExcutionPlan.insert(vars.formData);
      //       vars.formData.id = data.id;

      //       if (planItem && planItem.hasEditData()) await planItem.saveEditData();
      //       if (planSubcontract && planSubcontract.hasEditData()) await planSubcontract.saveEditData();
      //       if (planExpense && planExpense.hasEditData()) await planExpense.saveEditData();

      //       await methods.approvalRequest();
      //       methods.redirect(data.id);
      //       vars.formState.readOnly = true;
      //       notifyInfo('저장되었습니다');
      //     }

      //   } catch (ex) {
      //     console.log("❌ 저장 중 오류:", ex);
      //     if (ex.response?.status === 602) {
      //       notifyError('이미 존재하는 프로젝트번호 입니다');
      //     } else {
      //       notifyError('저장 할 내용이 없습니다');
      //     }

      //   } finally {
      //     vars.loading.value = false;
      //   }
      // },
      async saveItem() {
        const isSelect = await confirm('저장하시겠습니까?', '저장');
        if (!isSelect) return;

        vars.loading.value = true;

        try {
          const planItem = vars.grid.projectExcutionPlanItem;
          const planSubcontract = vars.grid.projectExcutionPlanSubcontract;
          const planExpense = vars.grid.projectExcutionPlanExpense;

          // 숫자 필드 NaN 방지
          // const sanitizeNumbers = (obj) => {
          //   ['excution_amount', 'expect_amount', 'time_amount', 'day_amount', 'plan_amount'].forEach((field) => {
          //     if (isNaN(obj[field])) {
          //       obj[field] = 0;
          //     }
          //   });
          // };

          if (vars.formData.id) {
            // 기존 정보 업데이트 (PATCH)
            vars.formData.modify_manager = authService.getUserName();
            vars.formData.modify_date = moment().format('YYYY-MM-DD HH:mm:ss');

            const updateData = { ...vars.formData };
            delete updateData.created;
            delete updateData.excution_plan_number;
            delete updateData.project_management;

            // sanitizeNumbers(updateData);

            console.log('🔧 PATCH 데이터:', updateData);

            const { data } = await projectExcutionPlan.update(vars.formData.id, updateData);
            vars.formData.excution_plan_number = data.excution_plan_number;

            if (planItem) await planItem.saveEditData();
            if (planSubcontract) await planSubcontract.saveEditData();
            if (planExpense) await planExpense.saveEditData();

            await methods.approvalRequest();

            vars.formState.readOnly = true;
            methods.enableSave();
            methods.enableEdit();
            methods.enableDelete();
            notifyInfo('저장되었습니다');

          } else {
            // 신규 등록 (POST)
            const insertData = { ...vars.formData };
            delete insertData.created;
            delete insertData.id;
            delete insertData.project_management;

            // sanitizeNumbers(insertData);

            // 필수값 보완
            if (!insertData.excution_plan_department) {
              insertData.excution_plan_department = authService.getDepartmentName();
            }
            if (!insertData.excution_plan_manager) {
              insertData.excution_plan_manager = authService.getUserName();
            }
            if (!insertData.excution_plan_date) {
              insertData.excution_plan_date = currentDateTime();
            }

            console.log('🆕 POST 데이터:', insertData);

            const { data } = await projectExcutionPlan.insert(insertData);
            vars.formData.id = data.id;
            vars.formData.excution_plan_number = data.excution_plan_number;

            if (planItem && planItem.hasEditData()) await planItem.saveEditData();
            if (planSubcontract && planSubcontract.hasEditData()) await planSubcontract.saveEditData();
            if (planExpense && planExpense.hasEditData()) await planExpense.saveEditData();

            await methods.approvalRequest();
            methods.redirect(data.id);
            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');
          }

        } catch (ex) {
          console.error('❌ 저장 중 오류:', ex);
          if (ex.response?.status === 602) {
            notifyError('이미 존재하는 프로젝트번호 입니다');
          } else if (ex.response?.status === 400) {
            notifyError('유효하지 않은 입력값이 포함되어 있습니다');
          } else {
            notifyError('저장 중 오류가 발생했습니다');
          }

        } finally {
          vars.loading.value = false;
        }
      },


      async approvalRequest(){
        if(!vars.formData.id) return;
        if(vars.formData.approval_status == '승인요청'){
          let isSelect = await confirm('전자결재 요청을 하시겠습니까?', '전자결재');
          if (isSelect) {
                try{
                  const leader = vars.dataSource.department.find(item => item.department_name === vars.formData.excution_plan_department);
                  const params = {
                    request_date: currentDateTime(),
                    request_number: vars.formData.excution_plan_number,
                    request_path: 'project_excution_plan',
                    request_path_id: vars.formData.id,
                    request_name: vars.formData.excution_plan_manager,
                    approval_leader: leader ? leader.depart_head_name : '',
                    approval_status: '요청완료'
                }
                  await approvalManagement.insert(params);
                  vars.formData.approval_status = '요청완료';
                  await projectExcutionPlan.update(vars.formData.id, {approval_status: '요청완료'});
                  alert('전자결재 요청이 완료되었습니다');
                }catch(ex){
                  console.error(ex);
                  alert('전자결재 요청 중 오류가 발생했습니다');
                }
              }
        }
      },
      selectDepartment(e) {
        if(!e.value){
          vars.disabled.save = true;
          vars.formData.excution_plan_department = null;
          vars.disabled.employee = false;
          vars.dataSource.employee = [];
        } else{
          const selectItem = e.component.option('selectedItem');
          if (selectItem) {
            loadEmployee(vars.dataSource, selectItem.id);
            vars.disabled.employee = false;
            vars.warehouse = { ...selectItem.warehouse };
            vars.filter.baseItem = vars.warehouse.wh_code;
          }else{
            vars.warehouse = {};
          }
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
        if (result) {
          const rows = vars.grid.projectExcutionPlanSubcontract.getVisibleRows();
          for (let row of rows){
            await projectExcutionPlanSubcontract.remove(row.data.id);
          }
          await projectExcutionPlan.remove(vars.formData.id);
          await alert('삭제되었습니다', '삭제 확인');
          methods.redirect();
          vars.formState.readOnly = true;

          methods.gridRefresh(null, 'projectExcutionPlanItem');
          methods.gridRefresh(null, 'projectExcutionPlanSubcontract');
          methods.gridRefresh(null, 'projectExcutionPlanExpense');
        }
      },
      redirect(id) {
        if (id) router.replace({ path: `/project/excution-plan/${id}` });
        else router.replace({ path: `/project/excution-plan` });
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
      isFilledFormRequiredData(){
        if(vars.formData.fk_project_management_id && vars.formData.excution_plan_manager){
          return true;
        }
        return false;
      },
      addItemHidden(){
        const grid = vars.grid.projectExcutionPlanItem;
        const grid2 = vars.grid.projectExcutionPlanSubcontract;
        if(grid) {
          grid.refresh();
        }
        if(grid2){
          grid2.refresh();
        }
        
      },
      async addSelectedRows(rows) {
        const grid = vars.grid.projectExcutionPlanItem;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        for (let row of rows) {
          await grid.addRow();
          const basicStock = row.basic_stock ? { ...row.basic_stock } : { current_stock: 0, available_stock: 0 };
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code;
          data.main_supplier = row.client_company ? row.client_company : null; 
          data.excution_plan_quantity = 0;
          data.not_excution_plan_quantity = 0; 
          data.assign_quantity = 0; 
          data.purchase_unit_price = 0; 
          data.unit_price = 0;
          data.supply_price = 0; 
          data.delivery_price = 0; 
          data.vat_type = methods.getFirstItemName(vars.dataSource.vat_type); 
          data.vat = 0; 
          data.closing_yn = 0;
          data.confirm_yn = 0;
          data.delivery_require = 0; 
          data.delivery_date = null; 
          data.order_date = null;
          data.note = '';
          data.warehouse_code = vars.warehouse.wh_code;
          data.warehouse = { ...vars.warehouse}
          data.basic_stock = { ...basicStock };
          data.register = authService.getUserName(); 
          data.created = currentDateTime(); 
          data.item = { ...row }; 
        }
        grid.refresh();
        vars.dlg.addItem.show = false;
      },
      async addSelectedRows2(rows){
        const grid = vars.grid.projectExcutionPlanSubcontract;
        
        const userName = authService.getUserName();
        const vat_type = methods.getFirstItemName(vars.dataSource.vat_type);
        for(let row of rows){
          grid.on("initNewRow", (e) => {
            e.data.subcontract_name = row.item_code;
            e.data.register = userName;
            e.data.created = currentDateTime();
            e.data.vat_type = vat_type;
            e.data.expect_amount = 0;
            e.data.purchase_unit_price = 0;
            e.data.vat = 0;
          })
          grid.addRow();
          grid.off("initNewRow");
        }
        
        vars.dlg.addItem2.show = false;
      },
      async addSelectedProjectRows(data){
        let rows = null;
        if(Array.isArray(data)){
          rows = data;
        }else{
          rows = vars.grid.projectItem.getSelectedRowsData();
        }
        const grid = vars.grid.projectExcutionPlanItem;
        
        for (let row of rows) {
          let main_supplier = '';
          const { data : clientItem } = await baseClientItem.load({
            filter: [['item_code', '=', row.item_code],
                    'and',
                    ['main_supplier', '=', true]],
            skip:0,
            take:1
            })
          if (clientItem.length > 0) {
            main_supplier = clientItem[0].client.name;
          }
          const cost = {
            exist: false,
            quantity: 0,
            unit_price: 0,
            supply_price: 0,
            vat: 0
          }
     
          if (row.fk_business_cost_id){
            cost.exist = true;
            cost.quantity = row.quantity;
            cost.unit_price = row.business_cost.purchase_unit_price;
            const response = calcPriceSummary(methods.getFirstItemName(vars.dataSource.vat_type), cost.quantity * cost.unit_price)
            cost.supply_price = response.supply_price;
            cost.vat = response.vat;
          }
          grid.on("initNewRow", (e) => {
            e.data.item_code = row.item_code;
            e.data.main_supplier = main_supplier;
            e.data.excution_plan_quantity = cost.exist ? cost.quantity : row.quantity;
            e.data.not_excution_plan_quantity = cost.exist ? cost.quantity : row.quantity;
            e.data.assign_quantity = 0; // 할당수량량
            e.data.purchase_unit_price = 0;
            e.data.purchase_supply_price = 0;
            e.data.unit_price = cost.exist ? cost.unit_price : 0;
            e.data.supply_price = cost.exist ? cost.supply_price : 0;
            e.data.delivery_price = 0;
            e.data.vat_type = methods.getFirstItemName(vars.dataSource.vat_type);
            e.data.vat = cost.exist ? cost.vat : 0;
            e.data.closing_yn = 0;
            e.data.confirmed = 0;
            e.data.delivery_require = 0;
            e.data.delivery_date = null; 
            e.data.order_date = null; 
            e.data.note = '';
            e.data.warehouse_code = vars.warehouse.wh_code;
            e.data.warehouse = { ...vars.warehouse };
            e.data.register = authService.getUserName();
            e.data.created = currentDateTime();
            e.data.fk_project_item_id = row.id;
            e.data.item = { ...row.item }; 
          })
          grid.addRow();
          grid.off("initNewRow");
        }
        
        
        vars.dlg.addProjectItem.show = false;
      },

      async addSelectedPlanItemRows(planItems){
        const grid = vars.grid.projectExcutionPlanItem;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }
        for (let row of planItems) {
          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          Object.assign(data, row);
          delete data.id;
          delete data.fk_project_item_id;
          delete data.fk_project_excution_plan_id;
          delete data.project_excution_plan;
          delete data.project_item;
          data.not_excution_plan_quantity = data.excution_plan_quantity;
          data.assign_quantity = 0; 
          data.closing_yn = 0; 
          data.register = authService.getUserName(); 
          data.created = currentDateTime();
        }
        grid.refresh();
      },
      async addSelectedPlanSubcontractRows(planSubcontract){
        const grid = vars.grid.projectExcutionPlanSubcontract;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }
        for (let row of planSubcontract) {
          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.subcontract_name = row.subcontract_name; 
          data.subcontract_company = row.subcontract_company; 
          data.expect_amount = row.expect_amount; 
          data.supply_price = row.supply_price; 
          data.vat_type = row.vat_type; 
          data.vat = row.vat; 
          data.register = authService.getUserName();
          data.created = currentDateTime();
        }
        grid.refresh();
      },
      async addSelectedPlanExpenseRows(planExpense){

        const grid = vars.grid.projectExcutionPlanExpense;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        for (let row of planExpense) {

          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.expense_description = row.expense_description; 
          data.expense_amount = row.expense_amount; 
          data.vat_type = row.vat_type; 
          data.vat = row.vat; 
          data.expense_source = row.expense_source;
          data.expense_date = row.expense_date;
          data.register = authService.getUserName();
          data.created = currentDateTime();
        }
        grid.refresh();
      },
      async addSelectedExcutionPlan(){
        const rows = await vars.grid.excutionPlan.getSelectedRowsData();

        let contract_amount = 0;
        let expect_amount = 0;
        let excution_amount = 0;
        for(const row of rows){
          contract_amount = contract_amount + row.contract_amount;
          expect_amount = expect_amount + row.expect_amount;
          excution_amount = excution_amount + row.excution_amount;
          const { data : planItems } = await projectExcutionPlanItem.load({
            filter: ['fk_project_excution_plan_id', '=', row.id],
            skip:0,
            take:1000
          })
          const { data : planSubcontract } = await projectExcutionPlanSubcontract.load({
            filter: ['fk_project_excution_plan_id', '=', row.id],
            skip:0,
            take:1000
          })

          const { data : planExpense } = await projectExcutionPlanExpense.load({
            filter: ['fk_project_excution_plan_id', '=', row.id],
            skip:0,
            take:1000
          })

          if(planItems.length){
            methods.addSelectedPlanItemRows(planItems)
          }

          if(planSubcontract.length){
            methods.addSelectedPlanSubcontractRows(planSubcontract)
          }

          if(planExpense.length){
            methods.addSelectedPlanExpenseRows(planExpense)
          }
        }
        vars.formData.contract_amount = contract_amount;
        vars.formData.expect_amount = expect_amount;
        vars.formData.excution_amount = excution_amount;

        vars.dlg.addExcutionPlan.show = false;
      },
      addFile ({component, data, column, rowIndex}) {
        return () => {
          const f = document.createElement('input')
          f.type = 'file'
          f.onchange = () => {
            if (f.files[0]) {
              vars.attchFiles[f.files[0].name] = f.files[0]
              component.cellValue(rowIndex, column.dataField, f.files[0].name)
            }
            f.onchange = undefined
            f.remove()
          }
          document.body.appendChild(f)
          f.click()
        }
      },
      async updateUploadFile(element){
        for (const key in element.data){
          if(vars.attchFiles[element.data[key]]){
            const fd = new FormData()
            fd.append('file', vars.attchFiles[element.data[key]], vars.attchFiles[element.data[key]].name)
            const {data: filename} = await uploadService.post('', fd)
            element.data[key+'_path'] = `project-excution-plan-subcontract/${filename}`
            delete vars.attchFiles[element.data[key]]
          }
        }
      },
      showAddPopup() {
        vars.dlg.addItem.show = true;
      },
      showAddPopup2() {
        vars.dlg.addItem2.show = true;
      },
      calculateSupplyPirceVat(vat_type, result_quantity, unit_price, newData){
        const supply_price = unit_price * result_quantity;
        const response = calcPriceSummary(vat_type, supply_price)
        newData.supply_price = response.supply_price;
        newData.vat = response.vat;
      },
      async setExcutionPlanQuantity(newData, value, currentRowData){
        newData.excution_plan_quantity = value;
        const quantity = value;
        const unit_price = currentRowData.unit_price;
        const purchase_unit_price = currentRowData.purchase_unit_price;
        newData.purchase_supply_price = purchase_unit_price * quantity;
        methods.calculateSupplyPirceVat(currentRowData.vat_type, quantity, unit_price, newData);
      },
      async setUnitPrice(newData, value, currentRowData){
        newData.unit_price = value;
        const quantity = currentRowData.excution_plan_quantity;
        const unit_price = value;

        methods.calculateSupplyPirceVat(currentRowData.vat_type, quantity, unit_price, newData)
        if(currentRowData.purchase_order_item){
          newData.purchase_order_item = {...currentRowData.purchase_order_item};
          newData.purchase_order_item.expect_unit_price = value;
        }
      },
      setItemPurchaseUnitPrice(newData, value, currentRowData){
        newData.purchase_unit_price = value;
        const quantity = currentRowData.excution_plan_quantity;
        newData.purchase_supply_price = value * quantity;
        if(currentRowData.purchase_order_item){
          newData.purchase_order_item = {...currentRowData.purchase_order_item};
          newData.purchase_order_item.unit_price = value;
        }
      },
      setPurchaseUnitPrice(newData, value, currentRowData){
        newData.purchase_unit_price = value;
        if(currentRowData.purchase_order_item){
          newData.purchase_order_item = {...currentRowData.purchase_order_item};
          newData.purchase_order_item.unit_price = value;
          newData.purchase_order_item.supply_price = value * newData.purchase_order_item.order_quantity;
        }

      },
      setVatType(newData, value, currentRowData){
        newData.vat_type = value;
        const quantity = currentRowData.excution_plan_quantity;
        const unit_price = currentRowData.unit_price;

        methods.calculateSupplyPirceVat(value, quantity, unit_price, newData)

      },
      setSubcontractExpectAmount(newData, value, currentRowData){
        const response = calcPriceSummary(currentRowData.vat_type, value);
        newData.expect_amount = value;
        newData.vat = currentRowData.vat_type == '포함' ? 0 : response.vat;
        if(currentRowData.purchase_order_item){
          newData.purchase_order_item = {...currentRowData.purchase_order_item};
          newData.purchase_order_item.expect_unit_price = value;
        }
      },
      setSubcontractVatType(newData, value, currentRowData){
        const response = calcPriceSummary(value, currentRowData.expect_amount);
        newData.vat_type = value;
        newData.vat = value == '포함' ? 0 : response.vat;
      },
      setExpenseAmount(newData, value, currentRowData){
        const response = calcPriceSummary(currentRowData.vat_type, value);
        newData.expense_amount = value;
        newData.vat =  currentRowData.vat_type == '포함' ? 0 : response.vat;
      },
      setExpenseVatType(newData, value, currentRowData){
        const response = calcPriceSummary(value, currentRowData.expense_amount);
        newData.vat_type = value;
        newData.vat = value == '포함' ? 0 : response.vat;
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
      setOrderDateModify(newData, value, currentRowData){
        newData.order_date_modify = value;
        newData.closing_yn = 0;
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
      enableDelete(){
        vars.disabled.delete = vars.formState.readOnly ? true : false;
      },
      enableSave(){
        vars.disabled.save = vars.formState.readOnly ? true : false;
      },
      enableEdit(){
        vars.disabled.edit = !vars.formState.readOnly ?  true : false;
      },
      onSavingAmount(){
        const param = {expect_amount : vars.formData.expect_amount, excution_amount : vars.formData.excution_amount}
        projectExcutionPlan.update(vars.formData.id, param);
      },
      onSavingItem(e) {
        e.promise = methods.onSavingItemImpl(e);
      },
      async onSavingItemImpl(e){
        for(const element of e.changes){
          if(element.type != 'remove'){
            delete element.data.item;
            delete element.data.basic_stock;
            delete element.data.warehouse;
            element.data.fk_project_excution_plan_id = vars.formData.id;
            await methods.updateUploadFile(element)
          }
        }
      },
      onEditingStartItem({component, key}){
        component.cellValue(component.getRowIndexByKey(key), 'modify_register', authService.getUserName());
        component.cellValue(component.getRowIndexByKey(key), 'modify_date', currentDateTime());
      },
      onFocusedCellChanged(e, item){
        vars.focus[item] = e;
      },
      onDataError(e){
        console.log("e : ", e)
        if (e.error.response.status == 605) {
          e.error.message = '연결된 데이터가 있어서 삭제가 안됩니다';
        } else if (e.error.response.status == 403) {
          e.error.message = '권한이 없습니다';
        }
      },
      async showAddProjectPopup(){
        if(!vars.formData.fk_project_management_id){
          await alert('프로젝트를 선택해 주세요.', '프로젝트 미선택');
          return;
        }

        await methods.loadProjectItem();

        if (!vars.grid.projectItem) {
          vars.dlg.addProjectItem.show = true;
          await new Promise(resolve => {
            const checkInterval = setInterval(() => {
              if (vars.grid.projectItem) {
                clearInterval(checkInterval);
                resolve();
              }
            }, 50);
          });
        }
        const notContains = [];
        for (const item of vars.grid.projectExcutionPlanItem.getVisibleRows()) {
          if (!item.id) {
            notContains.push(['id', '<>', item.data.fk_project_item_id], 'and');
          }
        }
        notContains.pop();
       
        if (vars.grid.projectItem) {
          vars.grid.projectItem.filter(notContains);
          vars.grid.projectItem.clearSelection();
          vars.grid.projectItem.refresh();
        }
       
        vars.dlg.addProjectItem.show = true;

      },
      showAddExcutionPlanPopup(){
        if (vars.grid.excutionPlan) {
          vars.grid.excutionPlan.clearSelection();
          vars.grid.excutionPlan.refresh();
        }
        vars.dlg.addExcutionPlan.show = true;
      },
      async loadProjectItem(){
        vars.filter.projectItem[0]['val']['val'] = vars.formData.fk_project_management_id;
        vars.dataSource.projectItem = getProjectItem(vars.filter.projectItem);
      },
      getFirstItemName(itemList) {
        if (!itemList || itemList.length <= 0) {
          return '';
        } else {
          return itemList[0].code_name;
        }
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
          methods.onSavingAmount();
        }
      },
      initNewRow(e, item){
        const userName = authService.getUserName();
        const vat_type = methods.getFirstItemName(vars.dataSource.vat_type);
        if(item == 'projectExcutionPlanSubcontract'){
          e.data.register = userName;
          e.data.created = currentDateTime();
          e.data.vat_type = vat_type;
          e.data.expect_amount = 0;
          e.data.vat = 0;
        }else if(item == 'projectExcutionPlanExpense'){
          e.data.register = userName;
          e.data.created = currentDateTime();
          e.data.vat_type = vat_type;
          e.data.expense_amount = 0;
          e.data.vat = 0;
          e.data.plan_amount = 0;
          e.data.day_amount = 0;
          e.data.time_amount = 0;
        }
      },
      calcConfirmed(rowData){
        if (rowData.delivery_date && rowData.purchase_unit_price > 0){
          return true;
        }
    
      },
      calcSummaryPlanItem(options){
        if(options.name === 'supply_price'){
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          }else if(options.summaryProcess === 'calculate'){
            options.totalValue += Number(options.value.supply_price);
          } else if (options.summaryProcess === 'finalize') {
            vars.summary.planItem.supply_price = options.totalValue;
            
          }
        }else if(options.name === 'vat'){
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          }else if(options.summaryProcess === 'calculate'){
            options.totalValue += Number(options.value.vat);
          } else if (options.summaryProcess === 'finalize') {
            vars.summary.planItem.vat = options.totalValue;
            vars.summary.planItem.total_price = vars.summary.planItem.supply_price + vars.summary.planItem.vat;
            methods.calExpectAmount();
          }
        }else if(options.name === 'purchase_supply_price'){
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          }else if(options.summaryProcess === 'calculate'){
            options.totalValue += Number(options.value.purchase_supply_price);
          } else if (options.summaryProcess === 'finalize') {
            vars.summary.planItem.purchase_supply_price = options.totalValue;
            methods.calExcutionAmount();
          }
        }else if(options.name === 'completion_price'){
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          }else if(options.summaryProcess === 'calculate'){
            options.totalValue += Number(options.value.purchase_supply_price);
          } else if (options.summaryProcess === 'finalize') {
            vars.summary.planItem.completion_price = options.totalValue;
            methods.calExcutionAmount();
            methods.setBusinessCompletionAmount(vars.formData);  // ✅ 추가

          }
        }
        
      },
      calcSummarySubcontract(options){
        if(options.name === 'expect_amount'){
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          }else if(options.summaryProcess === 'calculate'){
            options.totalValue += options.value.expect_amount;
          } else if (options.summaryProcess === 'finalize') {
            vars.summary.planSubcontract.supply_price = options.totalValue;
          }
        }else if(options.name === 'vat'){
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          }else if(options.summaryProcess === 'calculate'){
            options.totalValue +=options.value.vat;
          } else if (options.summaryProcess === 'finalize') {
            vars.summary.planSubcontract.vat = options.totalValue;
            vars.summary.planSubcontract.total_price = vars.summary.planSubcontract.supply_price + vars.summary.planSubcontract.vat;
            methods.calExpectAmount();
          }
        }else if(options.name === 'purchase_unit_price'){
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          }else if(options.summaryProcess === 'calculate'){
            options.totalValue += options.value.purchase_unit_price;
          } else if (options.summaryProcess === 'finalize') {
            vars.summary.planSubcontract.purchase_unit_price = options.totalValue;
            methods.calExcutionAmount();
          }
        }else if(options.name === 'completion_price'){
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          }else if(options.summaryProcess === 'calculate'){
            options.totalValue += Number(options.value.purchase_unit_price);
          } else if (options.summaryProcess === 'finalize') {
            vars.summary.planSubcontract.completion_price = options.totalValue;
            methods.calExcutionAmount();
            methods.setBusinessCompletionAmount(vars.formData);  // ✅ 추가
            
          }
        }
      },
      calcSummaryExpense(options){
        if(options.name === 'expense_amount'){
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          }else if(options.summaryProcess === 'calculate'){
            options.totalValue += options.value.expense_amount;
          } else if (options.summaryProcess === 'finalize') {
            vars.summary.planExpense.supply_price = options.totalValue;
          }
        }else if(options.name === 'vat'){
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          }else if(options.summaryProcess === 'calculate'){
            options.totalValue +=options.value.vat;
          } else if (options.summaryProcess === 'finalize') {
            vars.summary.planExpense.vat = options.totalValue;
            vars.summary.planExpense.total_price = vars.summary.planExpense.supply_price + vars.summary.planExpense.vat;
            methods.calExpectAmount();
          }
        }else if(options.name === 'excution_amount'){
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          }else if(options.summaryProcess === 'calculate'){
            options.totalValue += options.value.excution_amount;
          } else if (options.summaryProcess === 'finalize') {
            vars.summary.planExpense.excution_amount = options.totalValue;
            methods.calExcutionAmount();  
          }
        }else if(options.name === 'completion_price'){
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          }else if(options.summaryProcess === 'calculate'){
            options.totalValue += Number(options.value.plan_amount);
          } else if (options.summaryProcess === 'finalize') {
            vars.summary.planExpense.completion_price = options.totalValue;
            methods.calExcutionAmount();
            methods.setBusinessCompletionAmount(vars.formData);  // ✅ 추가
            
          }
        }
      },
      calExpectAmount(){
        const amount = vars.summary.planExpense.supply_price + vars.summary.planSubcontract.supply_price + vars.summary.planItem.supply_price;
        vars.formData.expect_amount = amount;
        if(vars.formData.contract_amount > 0 && vars.formData.expect_amount > 0){
          vars.formData.contract_to_expect_rate = (vars.formData.expect_amount / vars.formData.contract_amount * 100);
        }
        if(vars.formData.expect_amount > 0 && vars.formData.excution_amount > 0){
          vars.formData.expect_to_excution_rate = (vars.formData.excution_amount / vars.formData.expect_amount * 100);
        }
      },
      calExcutionAmount(){
        const amount = vars.summary.planItem.purchase_supply_price + vars.summary.planSubcontract.purchase_unit_price + vars.summary.planExpense.excution_amount;
        vars.formData.excution_amount = amount;
        if(vars.formData.contract_amount > 0 && vars.formData.excution_amount > 0){
          vars.formData.contract_to_excution_rate = (vars.formData.excution_amount / vars.formData.contract_amount * 100);
        }
        if(vars.formData.expect_amount > 0 && vars.formData.excution_amount > 0){
          vars.formData.expect_to_excution_rate = (vars.formData.excution_amount / vars.formData.expect_amount * 100);
        }
        
      },
      calculateTotalPriceWithDecimal(unitPrice, quantity) {
        const decimalPlaces = (unitPrice.toString().split('.')[1] || '').length;
        const conversionUnit = Math.pow(10, decimalPlaces);
        const roundedUnitPrice = Math.round(unitPrice * conversionUnit);
        const total = Math.floor(roundedUnitPrice * quantity / conversionUnit);

        return total;
      },
      async exportToPurchaseOrder(item){
        if(!vars.formData.id) return;

        const itemIdList = [];
        const rows = vars.grid[item].getVisibleRows();

        const rows_check = rows.filter(v => v.data.closing_yn);
        if(rows_check.length <= 0){
          alert('선택된 품목이 없습니다', '발주로 내보내기');
          return;
        }
        for(let row of rows_check){
          if(item === 'projectExcutionPlanItem'){
            if(!row.data.main_supplier || row.data.main_supplier == '') {
              alert('구매처를 입력하세요', '발주로 내보내기');
              return;
            }
            if(row.data.excution_plan_quantity <= 0){
              alert('발주계획수량이 0인 품목이 선택되었습니다', '발주로 내보내기');
              return;
            }
            if(!row.data.confirmed){
              alert('발주확정이 안된 품목이 선택되었습니다', '발주로 내보내기');
              return;
            }
          }else if(item === 'projectExcutionPlanSubcontract'){
            if(!row.data.subcontract_company || row.data.subcontract_company == '') {
              alert('공사업체를 입력하세요', '발주로 내보내기');
              return;
            }
          }
          
          itemIdList.push(row.data.id);
        }
        const params = {
          id: vars.formData.id,
          department: vars.formData.excution_plan_department,
          manager: vars.formData.excution_plan_manager,
          company_id: authService.getCompanyId(),
          excution_plan_ids: itemIdList,
        };
        try{
          let api = undefined;
          if(item === 'projectExcutionPlanItem'){
            api = new ApiService('/api/mes/v1/project/excution-item-to-order');
          }else if(item === 'projectExcutionPlanSubcontract'){
            api = new ApiService('/api/mes/v1/project/excution-subcontract-to-order');
          }
          await api.post('', params);
          await alert('발주로 내보내기가 완료되었습니다', '발주로 내보내기');
        }catch(ex){
          if (ex.response.status == 608) {
            await alert('미발주 수량이 없습니다', '발주로 내보내기');
          } else {
            await alert('발주로 내보내기가 실패했습니다', '발주로 내보내기');
          }
        }finally{
          methods.gridRefresh(vars.formData.id, item);
        }
      },
      async cellClick(e, item){
        if (!e.data || e.isEditing || !vars.formState.readOnly) return;
        if(e.column.caption === '발주여부' && e.data.id){
          let dataSource = undefined;
          if(item === 'projectExcutionPlanItem'){
            dataSource = projectExcutionPlanItem;
          }else if(item === 'projectExcutionPlanSubcontract'){
            dataSource = projectExcutionPlanSubcontract;
          }
          const { data } = await dataSource.byKey(e.data.id);
          if(data.closing_yn) return;
          vars.grid[item].cellValue(e.rowIndex, e.columnIndex, !e.data.closing_yn);
        } else if(e.column.caption === '발주확정' && e.data.id){
          await projectExcutionPlanItem.update(e.data.id, {confirmed: !e.data.confirmed});
          methods.gridRefresh(vars.formData.id, item);
        }
      },
      setBusinessCompletionAmount(formData) {
        const itemTotal = vars.summary.planItem?.purchase_supply_price || 0;
        const subcontractTotal = vars.summary.planSubcontract?.completion_price || 0;
        const expenseTotal = vars.summary.planExpense?.excution_amount || 0;

        const total = itemTotal + subcontractTotal + expenseTotal;

        // 디버깅용 로그 (필요시 삭제 가능)
        console.log('✅ 사업완료금액 계산');
        console.log(' - 주요자재:', itemTotal);
        console.log(' - 외주공사:', subcontractTotal);
        console.log(' - 경비:', expenseTotal);
        console.log(' = 총합:', total);

        formData.business_completion_amount = total;
      }



    };

    watch(
      () => props.id,
      () => methods.initById(props.id)
    );

    return {
      vars,
      methods,
      baseClient,
      generateItemButtonOption,
      numeral
    };
  },
};
</script>

<style lang="scss">
.dx-fileuploader-wrapper {
  padding: 0px;
  margin: 0px;
}
.dx-fileuploader-input-wrapper {
  padding: 0px;
  margin: 0px;
}
.approval-status {
  padding: 6px 20px;
  border-radius: 4px;
  border: 1px solid #d7d7d7;
  box-shadow: inset 0px 1px 3px 0px #38530d6b;
  background-color: #e3ffb8;
  color: #5c8816;
}
</style>
