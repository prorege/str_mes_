<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before"
              ><div class="content-title">프로젝트등록</div></dx-item
            >
            <dx-item
              location="after"
              locate-in-menu="auto"
              widget="dxButton"
              :options="{
                text: '기성고검토보고서',
                icon: '',
                onClick: methods.progressPaymentReport,
                visible: false
              }"
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
          <dx-group-item :col-count="5">
            <dx-group-item>
              <dx-simple-item
                data-field="project_number"
                :editor-options="{
                  onValueChanged: methods.onValueChanged,
                  placeholder: '(자동 or 직접입력)',
                  ...methods.generateItemButtonOption(
                    'search',
                    methods.createFindPopupFn('project', '프로젝트조회')
                  ),
                }"
              >
                <dx-label text="프로젝트번호" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="project_name"
                :editor-options="{
                  onValueChanged: methods.onValueChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="프로젝트명" :show-colon="false" />
                <dx-required-rule message="프로젝트명을 입력하세요" />
              </dx-simple-item>
              <dx-simple-item
                data-field="project_date"
                editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  showClearButton: true,
                  useMaskBehavior: true,
                  ...vars.formState,
                }"
              >
                <dx-label text="등록일자" :show-colon="false" />
              </dx-simple-item>
                <dx-simple-item data-field="progress_status" editor-type="dxSelectBox" :editor-options="{
                    dataSource: vars.dataSource.progress_status,
                    valueExpr: 'code_name',
                    displayExpr: 'code_name',
                    ...vars.formState,
                  }">
                <dx-label text="진행단계" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>

            <dx-group-item>
              <dx-simple-item
                data-field="order_company"
                :editor-options="{
                  ...methods.generateItemButtonOption(
                    'search',
                    methods.createFindPopupFn('order_company', '계약업체조회', { name: vars.formData.order_company })
                  ),
                  ...vars.formState,
                  onEnterKey: methods.createFindPopupFn('order_company', '계약업체조회', { name: vars.formData.order_company }),
                }"
              >
                <dx-label text="계약업체" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="contract_company"
                :editor-options="{
                  ...methods.generateItemButtonOption(
                    'search',
                    methods.createFindPopupFn('contract_company', '수요기관조회', { name: vars.formData.contract_company })
                  ),
                  ...vars.formState,
                  onEnterKey: methods.createFindPopupFn('contract_company', '수요기관조회', { name: vars.formData.contract_company }),
                }"
              >
                <dx-label text="수요기관" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="project_department"
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
                data-field="project_manager"
                editor-type="dxSelectBox"
                :editor-options="{
                  onValueChanged: methods.onValueChanged,
                  dataSource: vars.dataSource.project_manager,
                  displayExpr: 'emp_name',
                  valueExpr: 'emp_name',
                  ...vars.formState,
                }"
              >
                <dx-label text="등록담당자" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>

            <dx-group-item>
              <dx-simple-item
                data-field="contract_date"
                editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  showClearButton: true,
                  useMaskBehavior: true,
                  ...vars.formState,
                }"
              >
                <dx-label text="계약일자" :show-colon="false" />
              </dx-simple-item>

              <dx-simple-item
                data-field="commencement_date"
                editor-type="dxDateBox"
                :editor-options="{
                  onValueChanged: methods.onContractAmountChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="착공일자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="defect_end_date"
                editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  showClearButton: true,
                  useMaskBehavior: true,
                  ...vars.formState,
                }"
              >
                <dx-label text="하자만기" :show-colon="false" />
              </dx-simple-item>
            
              
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item
                data-field="completion_date"
                editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  showClearButton: true,
                  useMaskBehavior: true,
                  ...vars.formState,
                }"
              >
                <dx-label text="준공일자" :show-colon="false" />
              </dx-simple-item>
              
              <dx-simple-item
                data-field="company_amount"
                editor-type="dxNumberBox"
                :editor-options="{
                  format: 'currency',
                  onValueChanged: methods.onCompanyAmountChanged,
                }"
              >
                <dx-label text="계약금액" :show-colon="false" />
              </dx-simple-item>

              <dx-simple-item
                data-field="defect_period" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.defect_period,
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  onValueChanged: methods.defectPeriodChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="하자기간" :show-colon="false" />
              </dx-simple-item>
              
              <dx-simple-item data-field="company_vat_type" editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: vars.dataSource.vat_type,
                  displayExpr: 'code_name',
                  valueExpr: 'code_name',
                  onValueChanged: methods.onCompanyVatTypeChanged,
                  ...vars.formState,
                }"
              >
                <dx-label text="부가세구분" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
                <dx-simple-item data-field="business.business_number" :editor-options="methods.businessNumberOptions()">
                  <dx-label text="연결 영업" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item data-field="excution_plan.excution_plan_number" :editor-options="methods.excutionPlanNumberOptions()">
                  <dx-label text="연결 실행계획" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item
                  data-field="subcontracting_rate"
                  editor-type="dxTextBox"
                  :editor-options="{
                    readOnly: true
                  }"
                >
                <dx-label text="하도급률" :show-colon="false" />
              </dx-simple-item>
                <dx-simple-item data-field="project_important" editor-type="dxSelectBox" :editor-options="{
                  dataSource: vars.dataSource.project_important,
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  ...vars.formState,
                }">
                  <dx-label text="중요" :show-colon="false" />
                </dx-simple-item>
            </dx-group-item>
          </dx-group-item>
          <dx-group-item :col-count=5>
            <dx-group-item :col-span=2>
              <dx-simple-item data-field="location" :editor-options="{
                ...vars.formState,
              }">
                <dx-label text="현장주소" :show-colon="false" />
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
          <dx-item title="고객정보관리">
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
                  :data-source="vars.dataSource.customer_information"
                  :on-initialized="evt => methods.onGridInitialized(evt, 'customer_information')"
                  @saving="(e) => methods.onSavingItem(e, 'customer_information')"
                  @data-error-occurred="methods.onDataError"
                  @focused-cell-changed="evt => methods.onFocusedCellChanged(evt, 'customer_information')"
                  @init-new-row="evt => methods.initNewRow(evt, 'customer_information')"
                  >
                  <dx-grid-toolbar>
                      <dx-grid-item template="addCustomerInformationRowButton" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item template="customerInformationSaveButton" location="after" :visible="false" />
                      <dx-grid-item name="revertButton" location="after" />
                  </dx-grid-toolbar>
                  <template #addCustomerInformationRowButton>
                      <dx-button text="고객정보 추가" icon="add" @click="methods.addItemRowButton('customer_information')" />
                  </template>
                  <template #customerInformationSaveButton>
                      <dx-button text="저장" icon="save" @click="methods.itemSaveButton('customer_information')" />
                  </template>
                  <dx-column type="buttons" :visible="!vars.formState.readOnly"/>
                  <dx-column caption="일자" data-field="information_date" data-type="date" format="yyyy-MM-dd" />
                  <dx-column caption="고객담당자" data-field="manager">
                    <!-- <dx-lookup value-expr="emp_name" display-expr="emp_name" :data-source="vars.dataSource.employee_list" /> -->
                  </dx-column>
                  <dx-column caption="연락처" data-field="manager_mobile" />
                  <dx-column caption="이메일" data-field="manager_email" />
                  <dx-column caption="메모" data-field="note" />
                  <dx-column caption="등록자" data-field="register" :allow-editing="false" />
                  <dx-column caption="등록일자" data-field="register_date" data-type="date" format="yyyy-MM-dd" :allow-editing="false" />
                  <dx-scrolling mode="standard" />
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
          <dx-item title="계약품목">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 416px)"
                  column-resizing-mode="widget"
                  :on-initialized="
                    evt => methods.onGridInitialized(evt, 'items')
                  "
                  :remote-operations="true"
                  :data-source="vars.dataSource.items"
                  :show-borders="true"
                  :allow-column-reordering="true"
                  :allow-column-resizing="true"
                  :column-auto-width="true"
                  :select-text-on-edit-start="true"
                  :row-alternation-enabled="true"
                  :focused-row-enabled="true"
                  @data-error-occurred="methods.onDataError"
                  @saving="methods.onSavingItem"
                >
                  <dx-grid-toolbar>
                    <dx-item template="addBusinessCostButton" location="after" :visible="!vars.formState.readOnly"/>
                    <dx-item template="addQuoteItemButton" location="after" :visible="!vars.formState.readOnly"/>
                    <dx-item template="exportToShipmentOrder" location="before" :visible="vars.formState.readOnly && vars.disabled.exportToShipmentOrder" />
                    <dx-item template="exportToWorkOrder" location="before" :visible="vars.formState.readOnly && vars.disabled.exportToWorkOrder" />
                    <dx-grid-item template="itemsAddRowButton" :visible="!vars.formState.readOnly"/>
                    <dx-grid-item template="itemSaveButtonItems" location="after" :visible="!vars.formState.readOnly" />
                    <dx-grid-item name="revertButton" />
                  </dx-grid-toolbar>
                  <template #addBusinessCostButton>
                    <dx-button text="원가검토추가" icon="add" @click="methods.showAddBusinessCostButton" />
                  </template>
                  <template #addQuoteItemButton>
                    <dx-button text="견적품목추가" icon="add" @click="methods.showAddQuoteItemButton" />
                  </template>
                  <template #exportToShipmentOrder>
                    <dx-button text="수주로 내보내기" icon="export" @click="methods.exportToShipmentOrder" />
                  </template>
                  <template #exportToWorkOrder>
                    <dx-button text="작지로 내보내기" icon="export" @click="methods.exportToWorkOrder" />
                  </template>
                  <template #itemsAddRowButton>
                    <dx-button text="품목찾기" icon="add" @click="methods.showAddPopup"/>
                  </template>
                  <template #itemSaveButtonItems>
                      <dx-button text="저장" icon="save" @click="methods.itemSaveButton('items')" />
                  </template>
                  <dx-column type="buttons" :visible="!vars.formState.readOnly"/>
                  <dx-column
                    data-field="item_code"
                    caption="품목코드"
                    :allow-editing="false"
                  />
                  <dx-column
                    data-field="item.item_name"
                    caption="품명"
                    :allow-editing="false"
                  />
                  <dx-column
                    data-field="item.item_standard"
                    caption="규격"
                    :allow-editing="false"
                  />
                  <dx-column
                    data-field="quantity"
                    caption="수량"
                    data-type="number"
                    format="fixedPoint"
                    :set-cell-value="methods.setQuantity"
                  />
                  <dx-column
                    data-field="not_ordered"
                    caption="미수주수량"
                    data-type="number"
                    format="fixedPoint"
                  />
                  <dx-column
                    data-field="fk_project_management_id"
                    caption="프로젝트아이디"
                    :visible="false"
                  />
                  <dx-column
                    data-field="shipment_order.order_number"
                    caption="수주번호"
                    :allow-editing="false"
                  />
                  <dx-column
                    data-field="work_order.number"
                    caption="작지번호"
                    :allow-editing="false"
                  />

                  <dx-editing
                    :allow-adding="!vars.formState.readOnly"
                    :allow-updating="!vars.formState.readOnly"
                    :allow-deleting="!vars.formState.readOnly"
                    mode="batch"
                  />
                  <dx-scrolling mode="standard" />
                </dx-data-grid>
              </div>
            </template>
          </dx-item>
          <dx-item title="참여직원">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 416px)"
                  date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                  column-resizing-mode="widget"
                  :on-initialized="
                    evt => methods.onGridInitialized(evt, 'projectParticipant')
                  "
                  :remote-operations="true"
                  :data-source="vars.dataSource.projectParticipant"
                  :show-borders="true"
                  :allow-column-reordering="true"
                  :allow-column-resizing="true"
                  :column-auto-width="true"
                  :select-text-on-edit-start="true"
                  :row-alternation-enabled="true"
                  :focused-row-enabled="true"
                  @saving="methods.onSavingItem"
                  @focused-cell-changed="evt => methods.onFocusedCellChanged(evt, 'projectParticipant')"
                  @init-new-row="evt => methods.initNewRow(evt, 'projectParticipant')"
                >
                  <dx-grid-toolbar>
                      <dx-grid-item template="addRowButtonParticipant" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item template="itemSaveButtonParticipant" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item name="revertButton" location="after" />
                  </dx-grid-toolbar>
                  <template #addRowButtonParticipant>
                      <dx-button text="참여직원 추가" icon="add" @click="methods.addItemRowButton('projectParticipant')" />
                  </template>
                  <template #itemSaveButtonParticipant>
                      <dx-button text="저장" icon="save" @click="methods.itemSaveButton('projectParticipant')" />
                  </template>
                  <dx-column type="buttons" :visible="!vars.formState.readOnly"/>
                  <dx-column data-field="project_manager" caption="담당자"
                  :editor-options="{
                    ...methods.generateItemButtonOption('search', methods.createFindPopupFn('project_manager', '담당자 조회'))
                  }" />
                  <dx-column data-field="job_type" caption="직무유형" />
                  <dx-column data-field="note" caption="내용" />
                  <dx-editing
                    :allow-adding="!vars.formState.readOnly"
                    :allow-updating="!vars.formState.readOnly"
                    :allow-deleting="!vars.formState.readOnly"
                    mode="batch"
                  />
                  <dx-scrolling mode="standard" />
                </dx-data-grid>
              </div>
            </template>
          </dx-item>
          <dx-item title="관련업체">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 416px)"
                  date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                  column-resizing-mode="widget"
                  :on-initialized="
                    evt => methods.onGridInitialized(evt, 'projectCompany')
                  "
                  :remote-operations="false"
                  :data-source="vars.dataSource.projectCompany"
                  :show-borders="true"
                  :allow-column-reordering="true"
                  :allow-column-resizing="true"
                  :column-auto-width="true"
                  :select-text-on-edit-start="true"
                  :row-alternation-enabled="true"
                  :focused-row-enabled="true"
                  @saving="methods.onSavingItem"
                  @focused-cell-changed="evt => methods.onFocusedCellChanged(evt, 'projectCompany')"
                  @cell-click="methods.projectCompanyCellClick"
                >
                  <dx-grid-toolbar>
                      <dx-grid-item template="addRowButtonProjectCompany" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item template="itemSaveButtonProjectCompany" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item name="revertButton" location="after" />
                  </dx-grid-toolbar>
                  <template #addRowButtonProjectCompany>
                      <dx-button text="관련업체 추가" icon="add" @click="methods.addItemRowButton('projectCompany')" />
                  </template>
                  <template #itemSaveButtonProjectCompany>
                      <dx-button text="저장" icon="save" @click="methods.itemSaveButton('projectCompany')" />
                  </template>
                  <dx-column type="buttons" :visible="!vars.formState.readOnly"/>
                  <dx-column caption="업체명" data-field="company_name" :editor-options="{ 
                    ...methods.generateItemButtonOption('search', methods.createFindPopupFn('company_name', '업체 조회'))}"
                    cell-template="company_name"
                    >
                  </dx-column>
                  <dx-column caption="업체구분" data-field="company_type">
                    <dx-lookup
                      :data-source="vars.dataSource.company_type"
                      value-expr="code_name"
                      display-expr="code_name"
                    />
                  </dx-column>

                  <dx-column caption="담당자" data-field="company_manager" :editor-options="{
                      buttons:[
                        {name: 'search', location: 'after', options: {
                          stylingMode: 'text',
                          icon: 'search',
                          onClick: methods.managerOnClick
                        }}
                      ], 
                    }" />
                    
                  <dx-column caption="연락처" data-field="company_manager_phone" />
                  <dx-column caption="참고사항" data-field="note" />
                  <dx-editing mode="batch"
                    :allow-adding="!vars.formState.readOnly"
                    :allow-updating="!vars.formState.readOnly"
                    :allow-deleting="!vars.formState.readOnly"
                  />
                  <dx-scrolling mode="standard" />
                  <template #company_name="{data}">
                      <div class="company_name">{{ data.data[data.column.dataField] }}</div>
                  </template>
                </dx-data-grid>
              </div>
            </template>
          </dx-item>
          <dx-item title="계약자료">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 416px)"
                  date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                  column-resizing-mode="widget"
                  :on-initialized="
                    evt => methods.onGridInitialized(evt, 'projectDocument')
                  "
                  :remote-operations="true"
                  :data-source="vars.dataSource.projectDocument"
                  :show-borders="true"
                  :allow-column-reordering="true"
                  :allow-column-resizing="true"
                  :column-auto-width="true"
                  :select-text-on-edit-start="true"
                  :row-alternation-enabled="true"
                  :focused-row-enabled="true"
                  @saving="methods.onSavingItem"
                  @row-removing="methods.onDocumentRemoving"
                >
                  <dx-grid-toolbar>
                      <dx-grid-item template="addRowButtonProjectDocument" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item template="itemSaveButtonProjectDocument" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item name="revertButton" location="after" />
                  </dx-grid-toolbar>
                  <template #addRowButtonProjectDocument>
                      <dx-button text="계약자료 추가" icon="add" @click="methods.addItemRowButton('projectDocument')" />
                  </template>
                  <template #itemSaveButtonProjectDocument>
                      <dx-button text="저장" icon="save" @click="methods.itemSaveButton('projectDocument')" />
                  </template>
                  <dx-column type="buttons" :visible="!vars.formState.readOnly"/>
                  <dx-column caption="문서번호" data-field="document_number" />
                  <dx-column caption="문서명" data-field="document_name" />
                  <dx-column caption="참고사항" data-field="note" />
                  <dx-column caption="첨부파일" data-field="file_name" cell-template="download" edit-cell-template="upload" />
                  <dx-editing
                    :allow-adding="!vars.formState.readOnly"
                    :allow-updating="!vars.formState.readOnly"
                    :allow-deleting="!vars.formState.readOnly"
                    mode="batch"
                  />
                  <dx-scrolling mode="standard" />
                  <template #download="{data}">
                    <a :href="`/api/mes/v1/${data.data['file_path']}`" download>{{data.data[data.column.dataField]}}</a>
                  </template>
                  <template #upload="{data}">
                    <dx-text-box :value="data.data[data.column.dataField]">
                      <dx-text-box-button location="after" name="upload"
                        :options="{
                          hint: '업로드', icon: 'upload',
                          onClick: methods.addFile(data)
                        }"
                      />
                    </dx-text-box>
                  </template>
                </dx-data-grid>
              </div>
            </template>
          </dx-item>
          <dx-item title="일지등록">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 416px)"
                  date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                  column-resizing-mode="widget"
                  :on-initialized="
                    evt => methods.onGridInitialized(evt, 'projectDailyLog')
                  "
                  :remote-operations="true"
                  :data-source="vars.dataSource.projectDailyLog"
                  :show-borders="true"
                  :allow-column-reordering="true"
                  :allow-column-resizing="true"
                  :column-auto-width="true"
                  :select-text-on-edit-start="true"
                  :row-alternation-enabled="true"
                  :focused-row-enabled="true"
                  @saving="methods.onSavingItem"
                  @row-removing="methods.onDailyLogRemoving"
                  @init-new-row="evt => methods.initNewRow(evt, 'projectDailyLog')"
                >
                  <dx-grid-toolbar>
                      <dx-grid-item template="addRowButtonProjectDailyLog" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item template="itemSaveButtonProjectDailyLog" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item name="revertButton" location="after" />
                  </dx-grid-toolbar>
                  <template #addRowButtonProjectDailyLog>
                      <dx-button text="일지 추가" icon="add" @click="methods.addItemRowButton('projectDailyLog')" />
                  </template>
                  <template #itemSaveButtonProjectDailyLog>
                      <dx-button text="저장" icon="save" @click="methods.itemSaveButton('projectDailyLog')" />
                  </template>
                  <dx-column type="buttons" :visible="!vars.formState.readOnly"/>
                  <dx-column caption="일자" data-field="log_date" data-type="datetime" format="yyyy-MM-dd HH:mm" />
                  <dx-column caption="업무유형" data-field="work_type">
                    <dx-lookup
                      :data-source="vars.dataSource.work_type"
                      value-expr="code_name"
                      display-expr="code_name"
                    />
                  </dx-column>
                  <dx-column caption="업무내용" data-field="content" />
                  <dx-column caption="첨부파일" data-field="attachment" cell-template="download" edit-cell-template="upload" />
                  <dx-column caption="등록자" data-field="register" :allow-editing="false" />
                  <dx-column caption="등록시간" data-field="register_date" data-type="date" :allow-editing="false" />
                  <dx-editing
                    :allow-adding="!vars.formState.readOnly"
                    :allow-updating="!vars.formState.readOnly"
                    :allow-deleting="!vars.formState.readOnly"
                    mode="batch"
                  />
                  <dx-scrolling mode="standard" />
                  <template #download="{data}">
                    <a :href="`/api/mes/v1/${data.data['attachment_path']}`" download>{{data.data[data.column.dataField]}}</a>
                  </template>
                  <template #upload="{data}">
                    <dx-text-box :value="data.data[data.column.dataField]">
                      <dx-text-box-button location="after" name="upload"
                        :options="{
                          hint: '업로드', icon: 'upload',
                          onClick: methods.addFile(data)
                        }"
                      />
                    </dx-text-box>
                  </template>
                </dx-data-grid>
              </div>
            </template>
          </dx-item>
          <dx-item title="기성관리">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 416px)"
                  width="100%"
                  date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                  column-resizing-mode="widget"
                  :on-initialized="
                    evt => methods.onGridInitialized(evt, 'projectCostLog')
                  "
                  :remote-operations="true"
                  :data-source="vars.dataSource.projectCostLog"
                  :show-borders="true"
                  :allow-column-reordering="true"
                  :allow-column-resizing="true"
                  :column-auto-width="true"
                  :select-text-on-edit-start="true"
                  :row-alternation-enabled="true"
                  :focused-row-enabled="true"
                  @saving="methods.onSavingItem"
                  @init-new-row="evt => methods.initNewRow(evt, 'projectCostLog')"
                >
                  <dx-grid-toolbar>
                      <dx-grid-item template="addRowButtonProjectCostLog" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item template="itemSaveButtonProjectCostLog" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item name="revertButton" location="after" />
                  </dx-grid-toolbar>
                  <template #addRowButtonProjectCostLog>
                      <dx-button text="기성 추가" icon="add" @click="methods.addItemRowButton('projectCostLog')" />
                  </template>
                  <template #itemSaveButtonProjectCostLog>
                      <dx-button text="저장" icon="save" @click="methods.itemSaveButton('projectCostLog')" />
                  </template>
                  <dx-column type="buttons" :visible="!vars.formState.readOnly">
                    <dx-grid-button name="edit" @click="methods.onEditRowButtonCostLog" />
                    <dx-grid-button name="delete" @click="methods.onDeleteRowButtonCostLog" />
                  </dx-column>
                  <dx-column caption="일자" data-field="cost_date" data-type="date" format="yyyy-MM-dd" :set-cell-value="methods.setCostDate">
                    <dx-grid-required-rule message="일자는 필수 입력 항목입니다." />
                  </dx-column>
                  <dx-column caption="전월기성" data-field="prev_cost" data-type="number" format="currency" :allow-editing="false" />
                  <!-- 계산서발행 컬럼 추가 -->
                  <dx-column 
                    caption="계산서발행" 
                    data-field="invoice_status"
                    :width="120"
                    :allow-editing="false"
                    cell-template="invoiceStatusCell"
                  />
                  <dx-column 
                    data-field="fk_sales_id"
                    :visible="false"
                    :allow-editing="false"
                  />
                  <dx-column caption="당월기성" data-field="curr_cost" data-type="number" format="currency" :set-cell-value="methods.setCurrCost" />
                  <dx-column caption="누적기성" data-field="cumulative_cost" data-type="number" format="currency" :allow-editing="false" />
                  <dx-column caption="잔여기성" data-field="remaining_cost" data-type="number" format="currency" :allow-editing="false" />
                  <dx-column caption="총기성률" data-field="total_cost_rate" data-type="number" format="percent" :allow-editing="false" />
                  <dx-column caption="비고" data-field="etc" />
                  <dx-column caption="등록자" data-field="register" :allow-editing="false" />
                  <dx-column caption="등록시간" data-field="register_date" data-type="date" :allow-editing="false" />
                  <dx-editing
                    :allow-adding="!vars.formState.readOnly"
                    :allow-updating="!vars.formState.readOnly"
                    :allow-deleting="!vars.formState.readOnly"
                    new-row-position="last"
                    mode="row"
                  />
                  <dx-scrolling mode="standard" />
                  <!-- 템플릿 추가 -->
                  <template #invoiceStatusCell="{data}">
                    <!-- 발행완료 상태: 클릭하면 해당 매출계산서 페이지로 이동 -->
                    <div 
                      v-if="data.data.invoice_status === '발행완료'" 
                      class="invoice-complete invoice-complete--link"
                      @click="() => methods.onNavigateToSalesStatement(data)"
                      title="클릭하면 매출계산서로 이동합니다"
                    >
                      발행완료 🔗
                    </div>

                    <!-- 미발행 상태 + 저장된 행 + 읽기모드: 계산서발행 버튼 표시 -->
                    <dx-button 
                      v-else-if="data.data.id && vars.formState.readOnly"
                      text="계산서발행"
                      type="default"
                      styling-mode="outlined"
                      :width="100"
                      @click="() => methods.onInvoiceCostLog(data)"
                    />

                    <!-- 편집중이거나 저장 전: 비활성 -->
                    <span v-else>-</span>

                  </template>
                </dx-data-grid>
              </div>
            </template>
          </dx-item>
          <dx-item title="외주기성관리">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 416px)"
                  width="100%"
                  date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                  column-resizing-mode="widget"
                  :on-initialized="
                    evt => methods.onGridInitialized(evt, 'projectOutCostLog')
                  "
                  :remote-operations="true"
                  :data-source="vars.dataSource.projectOutCostLog"
                  :show-borders="true"
                  :allow-column-reordering="true"
                  :allow-column-resizing="true"
                  :column-auto-width="true"
                  :select-text-on-edit-start="true"
                  :row-alternation-enabled="true"
                  :focused-row-enabled="true"
                  @saving="methods.onSavingItem"
                  @init-new-row="evt => methods.initNewRow(evt, 'projectOutCostLog')"
                >
                  <dx-grid-toolbar>
                      <dx-grid-item template="addRowButtonProjectOutCostLog" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item template="itemSaveButtonProjectOutCostLog" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item name="revertButton" location="after" />
                  </dx-grid-toolbar>
                  <template #addRowButtonProjectOutCostLog>
                      <dx-button text="외주기성 추가" icon="add" @click="methods.addItemRowButton('projectOutCostLog')" />
                  </template>
                  <template #itemSaveButtonProjectOutCostLog>
                      <dx-button text="저장" icon="save" @click="methods.itemSaveButton('projectOutCostLog')" />
                  </template>
                  <dx-column type="buttons" :visible="!vars.formState.readOnly">
                    <dx-grid-button name="edit" @click="methods.onEditRowButtonOutCostLog" />
                    <dx-grid-button name="delete" @click="methods.onDeleteRowButtonOutCostLog" />
                  </dx-column>
                  <dx-column caption="일자" data-field="cost_date" data-type="date" format="yyyy-MM-dd" :set-cell-value="methods.setOutCostDate">
                    <dx-grid-required-rule message="일자는 필수 입력 항목입니다." />
                  </dx-column>
                  <dx-column caption="전월기성" data-field="prev_cost" data-type="number" format="currency" :allow-editing="false" />
                  <dx-column caption="당월기성" data-field="curr_cost" data-type="number" format="currency" :set-cell-value="methods.setOutCurrCost" />
                  <dx-column caption="누적기성" data-field="cumulative_cost" data-type="number" format="currency" :allow-editing="false" />
                  <dx-column caption="잔여기성" data-field="remaining_cost" data-type="number" format="currency" :allow-editing="false" />
                  <dx-column caption="총기성률" data-field="total_cost_rate" data-type="number" format="percent" :allow-editing="false" />
                  <dx-column caption="비고" data-field="etc" />
                  <dx-column caption="등록자" data-field="register" :allow-editing="false" />
                  <dx-column caption="등록시간" data-field="register_date" data-type="date" :allow-editing="false" />
                  <dx-editing
                    :allow-adding="!vars.formState.readOnly"
                    :allow-updating="!vars.formState.readOnly"
                    :allow-deleting="!vars.formState.readOnly"
                    new-row-position="last"
                    mode="row"
                  />
                  <dx-scrolling mode="standard" />
                </dx-data-grid>
              </div>
            </template>
          </dx-item>
          <dx-item title="준공계" :visible="false">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 416px)"
                  date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                  column-resizing-mode="widget"
                  :on-initialized="
                    evt => methods.onGridInitialized(evt, 'projectCompletion')
                  "
                  :remote-operations="true"
                  :data-source="vars.dataSource.projectCompletion"
                  :show-borders="true"
                  :allow-column-reordering="true"
                  :allow-column-resizing="true"
                  :column-auto-width="true"
                  :select-text-on-edit-start="true"
                  :row-alternation-enabled="true"
                  :focused-row-enabled="true"
                  @saving="methods.onSavingItem"
                  @row-removing="methods.onCompletionRemoving"
                  @init-new-row="evt => methods.initNewRow(evt, 'projectCompletion')"
                >
                  <dx-grid-toolbar>
                      <dx-grid-item template="completionReportButton" location="after" :visible="vars.formState.readOnly" />
                      <dx-grid-item template="addRowButtonProjectCompletion" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item template="itemSaveButtonProjectCompletion" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item name="revertButton" location="after" />
                  </dx-grid-toolbar>
                  <template #completionReportButton>
                    <dx-button class="completion-button" text="계측제어조합 납품완료계" @click="methods.onReportShow('measurementDCompletion')" />
                    <dx-button class="completion-button" text="계측제어조합 완료계" @click="methods.onReportShow('measurementCompletion')" />
                    <dx-button class="completion-button" text="씨에스테크 납품완료계" @click="methods.onReportShow('csTechDCompletion')" />
                    <dx-button class="completion-button" text="씨에스테크 완료계" @click="methods.onReportShow('csTechCompletion')" />
                    <dx-button class="completion-button" text="씨에스테크 준공계" @click="methods.onReportShow('csTechCCompletion')" />
                    <dx-button class="completion-button" text="에스텍 납품완료계" @click="methods.onReportShow('stechDCompletion')" />
                    <dx-button class="completion-button" text="에스텍 완료계" @click="methods.onReportShow('stechCompletion')" />
                    <dx-button class="completion-button" text="에스텍 준공계" @click="methods.onReportShow('stechCCompletion')" />
                    <dx-button class="completion-button" text="자동제어조합 납품완료계" @click="methods.onReportShow('autoDCompletion')" />
                    <dx-button class="completion-button" text="자동제어조합 완료계" @click="methods.onReportShow('autoCompletion')" />
                  </template>
                  <template #addRowButtonProjectCompletion>
                      <dx-button text="준공 추가" icon="add" @click="methods.addItemRowButton('projectCompletion')" />
                  </template>
                  <template #itemSaveButtonProjectCompletion>
                      <dx-button text="저장" icon="save" @click="methods.itemSaveButton('projectCompletion')" />
                  </template>
                  <dx-column type="buttons" :visible="!vars.formState.readOnly">
                    <dx-grid-button name="edit"/>
                    <dx-grid-button name="delete" />
                  </dx-column>
                  <dx-column caption="문서명" data-field="document_name">
                    <dx-lookup 
                    :data-source="vars.dataSource.completion"
                    value-expr="code_name"
                    display-expr="code_name"
                    />
                  </dx-column>
                  <dx-column caption="첨부파일" data-field="file_name" cell-template="download" edit-cell-template="upload" />
                  <template #download="{data}">
                    <a :href="`/api/mes/v1/${data.data['file_path']}`" download>{{data.data[data.column.dataField]}}</a>
                  </template>
                  <template #upload="{data}">
                    <dx-text-box :value="data.data[data.column.dataField]">
                      <dx-text-box-button location="after" name="upload"
                        :options="{
                          hint: '업로드', icon: 'upload',
                          onClick: methods.addFile(data)
                        }"
                      />
                    </dx-text-box>
                  </template>

                  <dx-editing
                    :allow-adding="!vars.formState.readOnly"
                    :allow-updating="!vars.formState.readOnly"
                    :allow-deleting="!vars.formState.readOnly"
                    mode="row"
                  />
                  <dx-scrolling mode="standard" />
                </dx-data-grid>
              </div>
            </template>
          </dx-item>
          <dx-item title="자재승인원">
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
                  :data-source="vars.dataSource.materialApproval"
                  :on-initialized="evt => methods.onGridInitialized(evt, 'materialApproval')"
                  @saving="(e) => methods.onSavingItem(e, 'materialApproval')"
                  @data-error-occurred="methods.onDataError"
                  @focused-cell-changed="evt => methods.onFocusedCellChanged(evt, 'materialApproval')"
                  @init-new-row="evt => methods.initNewRow(evt, 'materialApproval')"
                  @row-removing="methods.onMaterialApprovalRemoving"
                  >
                  <dx-grid-toolbar>
                      <dx-grid-item template="addMaterialApprovalRowButton" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item template="materialApprovalSaveButton" location="after" :visible="false" />
                      <dx-grid-item name="revertButton" location="after" />
                  </dx-grid-toolbar>
                  <template #addMaterialApprovalRowButton>
                      <dx-button text="자재승인원 추가" icon="add" @click="methods.addItemRowButton('materialApproval')" />
                  </template>
                  <template #materialApprovalSaveButton>
                      <dx-button text="저장" icon="save" @click="methods.itemSaveButton('materialApproval')" />
                  </template>
                  <dx-column type="buttons" :visible="!vars.formState.readOnly"/>
                  <dx-column caption="문서번호" data-field="document_number" />
                  <dx-column caption="참고사항" data-field="etc" />
                  <dx-column caption="첨부파일" data-field="file_name" cell-template="download" edit-cell-template="upload" />
                  <template #download="{data}">
                    <a :href="`/api/mes/v1/${data.data['file_path']}`" download>{{data.data[data.column.dataField]}}</a>
                  </template>
                  <template #upload="{data}">
                    <dx-text-box :value="data.data[data.column.dataField]">
                      <dx-text-box-button location="after" name="upload"
                        :options="{
                          hint: '업로드', icon: 'upload',
                          onClick: methods.addFile(data)
                        }"
                      />
                    </dx-text-box>
                  </template>
                  <dx-scrolling mode="standard" />
                  <dx-editing mode="batch"
                    :use-icons="true"
                    :allow-adding="true"
                    :allow-updating="true"
                    :allow-deleting="true"
                    />
                </dx-data-grid>
              </div>
            </template>
          </dx-item>
          <dx-item title="착공계" :visible="false">
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
                  :data-source="vars.dataSource.projectConstruction"
                  :on-initialized="evt => methods.onGridInitialized(evt, 'projectConstruction')"
                  @saving="(e) => methods.onSavingItem(e, 'projectConstruction')"
                  @data-error-occurred="methods.onDataError"
                  @focused-cell-changed="evt => methods.onFocusedCellChanged(evt, 'projectConstruction')"
                  @init-new-row="evt => methods.initNewRow(evt, 'projectConstruction')"
                  @row-removing="methods.onConstructionRemoving"
                  >
                  <dx-grid-toolbar>
                      <dx-grid-item template="constructionReportButton" location="after" :visible="vars.formState.readOnly" />
                      <dx-grid-item template="addProjectConstructionRowButton" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item template="projectConstructionSaveButton" location="after" :visible="false" />
                      <dx-grid-item name="revertButton" location="after" />
                  </dx-grid-toolbar>
                  <template #constructionReportButton>
                    <dx-button text="계측제어조합 착수계" @click="methods.onReportShow('measurementConstruction')" />
                    <dx-button text="씨에스테크 착공계"  @click="methods.onReportShow('csTechConstruction')" />
                    <dx-button text="씨에스테크 착수계"  @click="methods.onReportShow('csTechCommencement')" />
                    <dx-button text="에스텍 착공계"  @click="methods.onReportShow('stechConstruction')" />
                    <dx-button text="에스텍 착수계"  @click="methods.onReportShow('stechCommencement')" />
                    <dx-button text="자동제어조합 착수계"  @click="methods.onReportShow('autoCommencement')" />
                  </template>
                  <template #addProjectConstructionRowButton>
                      <dx-button text="착공계 추가" icon="add" @click="methods.addItemRowButton('projectConstruction')" />
                  </template>
                  <template #projectConstructionSaveButton>
                      <dx-button text="저장" icon="save" @click="methods.itemSaveButton('projectConstruction')" />
                  </template>
                  <dx-column type="buttons" :visible="!vars.formState.readOnly">
                    <dx-grid-button name="edit"/>
                    <dx-grid-button name="delete" />
                  </dx-column>
                  <dx-column caption="문서명" data-field="document_name">
                    <dx-lookup 
                    :data-source="vars.dataSource.construction"
                    value-expr="code_name"
                    display-expr="code_name"
                    />
                  </dx-column>
                  <dx-column caption="첨부파일" data-field="file_name" cell-template="download" edit-cell-template="upload" />
                  <template #download="{data}">
                    <a :href="`/api/mes/v1/${data.data['file_path']}`" download>{{data.data[data.column.dataField]}}</a>
                  </template>
                  <template #upload="{data}">
                    <dx-text-box :value="data.data[data.column.dataField]">
                      <dx-text-box-button location="after" name="upload"
                        :options="{
                          hint: '업로드', icon: 'upload',
                          onClick: methods.addFile(data)
                        }"
                      />
                    </dx-text-box>
                  </template>
                  <dx-scrolling mode="standard" />
                  <dx-editing mode="batch"
                    :use-icons="true"
                    :allow-adding="true"
                    :allow-updating="true"
                    :allow-deleting="true"
                    />
                </dx-data-grid>
              </div>
            </template>
          </dx-item>
        </dx-tab-panel>
      </div>
    </div>
    <dx-popup
      title="원가검토추가"
      content-template="popup-content"
      v-model:visible="vars.dlg.addBusinessCost.show"
      :width="680"
      :height="500"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="(evt) => methods.onGridInitialized(evt, 'find-business-cost-popup')"
    >
      <template #popup-content>
        <dx-data-grid
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="vars.dataSource.businessCost"
          :on-initialized="(evt) => methods.onGridInitialized(evt, 'businessCost')"
        >
          <dx-grid-toolbar>
            <dx-item template="addItemButton" location="before" />
          </dx-grid-toolbar>
          <template #addItemButton>
            <dx-button text="선택된 항목 추가" icon="add" @click="methods.addSelectedCostRows" />
          </template>
          <dx-column caption="순서" data-field="item_order" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item_name" />
          <dx-column caption="규격" data-field="item_standard" />
          <dx-column caption="단위" data-field="unit" />
          <dx-column caption="견적수량" data-field="quote_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="견적단가" data-field="quote_unit_price" data-type="number" format="currency" />
          <dx-column caption="견적금액" data-field="quote_supply_price" data-type="number" format="currency" />
          <dx-column caption="구매단가" data-field="purchase_unit_price" data-type="number" format="currency" />
          <dx-column caption="구매금액" data-field="purchase_supply_price" data-type="number" format="currency" />
          <dx-column caption="영업건명" data-field="business.business_name" />
          <dx-paging :page-size="20" />
          <dx-sorting mode="multiple"/>
          <dx-filter-row :visible="true" />
          <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick" />
        </dx-data-grid>
      </template>
    </dx-popup>
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
      <template #popup-content>
        <dx-data-grid
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="vars.dataSource.quoteItem"
          :on-initialized="(evt) => methods.onGridInitialized(evt, 'quoteItem')"
        >
          <dx-grid-toolbar>
            <dx-item template="addItemButton" location="before" />
          </dx-grid-toolbar>
          <template #addItemButton>
            <dx-button text="선택된 항목 추가" icon="add" @click="methods.addSelectedQuoteRows" />
          </template>
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
          v-if="vars.dlg.finder.key === 'order_company'"
          :filters="vars.dlg.finder.data"
          @change="methods.finderReturnHandler"
        />
        <data-grid-client
          v-else-if="vars.dlg.finder.key === 'contract_company'"
          :filters="vars.dlg.finder.data"
          @change="methods.finderReturnHandler"
        />
        <data-grid-client
          v-else-if="vars.dlg.finder.key === 'company_name'"
          :filters="vars.dlg.finder.data"
          @change="methods.finderReturnHandler"
        />
        <data-grid-project
          v-else-if="vars.dlg.finder.key === 'project'"
          @change="methods.finderReturnHandler"
        />
        <data-grid-business v-else-if="vars.dlg.finder.key === 'business'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />

        <data-grid-excution-plan v-else-if="vars.dlg.finder.key === 'excution_plan'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />

        <data-grid-client-manager v-else-if="vars.dlg.finder.key === 'company_manager'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />

        <data-grid-employee v-else-if="vars.dlg.finder.key === 'project_manager'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
    
        <div v-else-if="vars.dlg.finder.key === 'etc'">
          <div class="mb-2">
            <dx-text-area
              :height="430"
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
                icon: 'save',
                text: '저장',
                onClick: methods.finderReturnHandler,
              }"
            />
          </dx-toolbar>
        </div>
      </template>
    </dx-popup>
    <dx-popup
        title="거래처정보"
        content-template="popup-client-detail"
        v-model:visible="vars.disabled.clientDetail"
        width="70%"
        height="80%"
        :resize-enabled="true"
        :close-on-outside-click="true"
        @initialized="evt => methods.onGridInitialized(evt, 'find-popup-client-detail')"
        >
        <template #popup-client-detail>
            <popup-client-detail :client-name="vars.dataSource.clientDetail"/>
        </template>
    </dx-popup>

    <popup-measurement-d-completion-report
      :fk_project_management_id="vars.formData.id"
      v-model:visible="vars.dlg.report.measurementDCompletion.show"
    />
    <popup-measurement-completion-report
      :fk_project_management_id="vars.formData.id"
      v-model:visible="vars.dlg.report.measurementCompletion.show"
    />
    <popup-cs-tech-completion-report
      :fk_project_management_id="vars.formData.id"
      v-model:visible="vars.dlg.report.csTechCompletion.show"
    />
    <popup-cs-tech-d-completion-report
      :fk_project_management_id="vars.formData.id"
      v-model:visible="vars.dlg.report.csTechDCompletion.show"
    />
    <popup-cs-tech-c-completion-report
      :fk_project_management_id="vars.formData.id"
      v-model:visible="vars.dlg.report.csTechCCompletion.show"
    />
    <popup-stech-d-completion-report
      :fk_project_management_id="vars.formData.id"
      v-model:visible="vars.dlg.report.stechDCompletion.show"
    />
    <popup-stech-completion-report
      :fk_project_management_id="vars.formData.id"
      v-model:visible="vars.dlg.report.stechCompletion.show"
    />
    <popup-stech-c-completion-report
      :fk_project_management_id="vars.formData.id"
      v-model:visible="vars.dlg.report.stechCCompletion.show"
    />
    <popup-auto-d-completion-report
      :fk_project_management_id="vars.formData.id"
      v-model:visible="vars.dlg.report.autoDCompletion.show"
    />
    <popup-auto-completion-report
      :fk_project_management_id="vars.formData.id"
      v-model:visible="vars.dlg.report.autoCompletion.show"
    />
    <popup-measurement-construction-report
      :fk_project_management_id="vars.formData.id"
      v-model:visible="vars.dlg.report.measurementConstruction.show"
    />
    <popup-cs-tech-construction-report
      :fk_project_management_id="vars.formData.id"
      v-model:visible="vars.dlg.report.csTechConstruction.show"
    />
    <popup-cs-tech-commencement-report
      :fk_project_management_id="vars.formData.id"
      v-model:visible="vars.dlg.report.csTechCommencement.show"
    />
    <popup-stech-construction-report
      :fk_project_management_id="vars.formData.id"
      v-model:visible="vars.dlg.report.stechConstruction.show"
    />
    <popup-stech-commencement-report
      :fk_project_management_id="vars.formData.id"
      v-model:visible="vars.dlg.report.stechCommencement.show"
    />
    <popup-auto-commencement-report
      :fk_project_management_id="vars.formData.id"
      v-model:visible="vars.dlg.report.autoCommencement.show"
    />
    <popup-progress-payment-report
      v-model:visible="vars.dlg.report.progressPayment.show"
      :project-id="vars.formData.id || 0"
    />
  </div>
</template>

<script>
import moment from 'moment';
import numeral from 'numeral';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxScrollView } from 'devextreme-vue/scroll-view';
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
  DxRequiredRule as DxGridRequiredRule,
  DxSelection,
  DxFilterRow,
  DxPaging,
  DxLookup,
  DxScrolling,
  DxColumnChooser,
  DxToolbar as DxGridToolbar,
  DxItem as DxGridItem,
  DxButton as DxGridButton
} from 'devextreme-vue/data-grid';
import { DxTabPanel } from 'devextreme-vue/tab-panel';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxTextBox, DxButton as DxTextBoxButton } from 'devextreme-vue/text-box';
import { DxButton } from 'devextreme-vue/button';
import { DxFileUploader } from 'devextreme-vue/file-uploader';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import { confirm, alert } from 'devextreme/ui/dialog';
import { onMounted, ref, reactive, computed, watch, nextTick } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import stateStore from '@/utils/state-store';
import {
  projectRegistration,
  getProjectRegistration,
  getProjectItem,
  getProjectParticipant,
  getProjectCompany,
  getProjectDocument,
  getProjectDailyLog,
  getProjectCostLog,
  getProjectOutCostLog,
  getProjectCompletion,
  getProjectBusinessCost,
  getProjectMaterialApproval,
  getProjectCustomerInformation,
  getProjectBusinessNote,
  getProjectConstruction,
  projectExcutionPlan,
  projectBusiness,
  projectExcutionPlanSubcontract
} from '../../data-source/project';
import {
  baseCodeLoader,
  baseClient,
  baseItem,
  baseDepartment,
  baseEmployee,
  baseClientManager
} from '../../data-source/base';
import { getShipmentQuoteItem, shipmentQuote } from '../../data-source/shipment';
import DataGridClient from '../../components/base/data-client.vue';
import DataGridProject from '../../components/project/data-project.vue';
import DataGridBusiness from '@/components/project/data-business.vue';
import DataGridExcutionPlan from '@/components/project/data-excution-plan.vue';
import DataGridItem from '../../components/base/data-item.vue';
import PopupItem from '../../components/base/popup-item.vue';
import DataGridClientManager from '../../components/base/data-client-manager.vue';
import DataGridEmployee from '../../components/base/data-employee.vue';
import DataGridEmployeeSelect from '../../components/base/data-employee-select.vue';
import authService from '../../auth';
import ApiService from '../../utils/api-service';
import { notifyInfo, notifyError } from '../../utils/notify';
import { currentDateTime, calcPriceSummary } from '../../utils/util';
import PopupClientDetail from '@/components/base/popup-client-detail';
import { loadEmployee, loadWarehouse, loadDepartment, loadClientManager } from '../../utils/data-loader';
import { DxNumberBox } from 'devextreme-vue/number-box';
import ArrayStore from 'devextreme/data/array_store';
import DataMeasurementReport from '@/components/project/data-measurement-report.vue';
import DataAutoReport from '@/components/project/data-auto-report.vue';
import PopupMeasurementDCompletionReport from '@/components/project/popup-measurement-d-completion-report.vue';
import PopupMeasurementCompletionReport from '@/components/project/popup-measurement-completion-report.vue';
import PopupCsTechCompletionReport from '@/components/project/popup-cs-tech-completion-report.vue';
import PopupCsTechDCompletionReport from '@/components/project/popup-cs-tech-d-completion-report.vue';
import PopupCsTechCCompletionReport from '@/components/project/popup-cs-tech-c-completion-report.vue';
import PopupStechDCompletionReport from '@/components/project/popup-stech-d-completion-report.vue';
import PopupStechCompletionReport from '@/components/project/popup-stech-completion-report.vue';
import PopupStechCCompletionReport from '@/components/project/popup-stech-c-completion-report.vue';
import PopupAutoDCompletionReport from '@/components/project/popup-auto-d-completion-report.vue';
import PopupAutoCompletionReport from '@/components/project/popup-auto-completion-report.vue';
import PopupMeasurementConstructionReport from '@/components/project/popup-measurement-construction-report.vue';
import PopupCsTechConstructionReport from '@/components/project/popup-cs-tech-construction-report.vue';
import PopupCsTechCommencementReport from '@/components/project/popup-cs-tech-commencement-report.vue';
import PopupStechConstructionReport from '@/components/project/popup-stech-construction-report.vue';
import PopupStechCommencementReport from '@/components/project/popup-stech-commencement-report.vue';
import PopupAutoCommencementReport from '@/components/project/popup-auto-commencement-report.vue';
import PopupProgressPaymentReport from '@/components/approval/popup-progress-payment-report.vue';
export default {
  components: {
    DxToolbar,
    DxItem,
    DxTextArea,
    DxScrollView,
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
    DataGridClient,
    DataGridProject,
    DataGridItem,
    DxRequiredRule,
    DxGridRequiredRule,
    DxGridToolbar,
    DxGridItem,
    PopupClientDetail,
    DataGridBusiness,
    projectBusiness,
    DataGridExcutionPlan,
    DataGridClientManager,
    DataGridEmployee,
    PopupItem,
    DxNumberBox,
    DataGridEmployeeSelect,
    DxGridButton,
    DataMeasurementReport,
    DataAutoReport,
    PopupMeasurementDCompletionReport,
    PopupMeasurementCompletionReport,
    PopupCsTechCompletionReport,
    PopupCsTechDCompletionReport,
    PopupCsTechCCompletionReport,
    PopupStechDCompletionReport,
    PopupStechCompletionReport,
    PopupStechCCompletionReport,
    PopupAutoDCompletionReport,
    PopupAutoCompletionReport,
    PopupMeasurementConstructionReport,
    PopupCsTechConstructionReport,
    PopupCsTechCommencementReport,
    PopupStechConstructionReport,
    PopupStechCommencementReport,
    PopupAutoCommencementReport,
    PopupProgressPaymentReport,
  },
  props: {
    id: [String, Number],
    business_id: [String, Number],
  },
  setup(props) {
    // variable 설정
    const uploadService = new ApiService('/api/mes/v1/project-attachment');
    const router = useRouter();
    const route = useRoute();
    const vars = { dlg: {} };
    vars.init = ref(false);
    vars.loading = ref(false);
    vars.formState = reactive({ readOnly: true });
    vars.warehouse = {};
    vars.focus = reactive({
      projectCompany: null,
      projectParticipant: null,
    })
    vars.grid = {
      items: null,
      projectParticipant: null,
      projectCompany: null,
      projectDocument: null,
      businessCost: null,
      quoteItem: null,
      materialApproval: null,
      projectDailyLog: null,
      projectCostLog: null,
      projectCompletion: null,
      fk_project_management_id : null,
    };
    vars.dlg.addItem = reactive({ show: false });
    vars.dlg.addBusinessCost = reactive({ show: false });
    vars.dlg.addQuoteItem = reactive({ show: false });
    vars.dlg.finder = reactive({
      show: false,
      title: '',
      key: null,
      data: null,
    });

    vars.dlg.report = {
      measurementCompletion: reactive({ show: false }),
      measurementDCompletion: reactive({ show: false }),
      csTechCompletion: reactive({ show: false }),
      csTechDCompletion: reactive({ show: false }),
      csTechCCompletion: reactive({ show: false }),
      stechDCompletion: reactive({ show: false }),
      stechCompletion: reactive({ show: false }),
      stechCCompletion: reactive({ show: false }),
      autoDCompletion: reactive({ show: false }),
      autoCompletion: reactive({ show: false }),
      measurementConstruction: reactive({ show: false }),
      csTechConstruction: reactive({ show: false }),
      csTechCommencement: reactive({ show: false }),
      stechConstruction: reactive({ show: false }),
      stechCommencement: reactive({ show: false }),
      autoCommencement: reactive({ show: false }),
    }
    vars.dlg.report.progressPayment = reactive({ show: false });
    vars.formData = reactive({
      business: null,
      id: null,
      created: '', // 생성시간
      project_number: '', // 프로젝트번호
      project_name: '', // 계약건명
      project_date: '', // 등록 일자
      order_company: '', // 계약업체
      contract_company: '', // 수요기관
      project_department: '', // 등록부서
      project_manager: '', // 등록담당자
      contract_date: '', // 계약일자
      defect_end_date: '', // 하자만기
      //contract_amount: 0, // 원청금액
      commencement_date : '', //착공일자
      non_invoice: 0,
      contract_vat_type: '', // 부가세 구분
      company_vat_type: '', // 부가세 구분
      completion_date: '', // 준공일자
      defect_period: '', // 하자기간
      company_amount: 0, // 계약금액
      subcontracting_rate: 0, // 하도급율
      progress_status: '', // 진행단계
      project_important: '', // 중요
      location: '', // 현장주소
      fk_business_id: null,
      fk_company_id: authService._user.fk_company_id,
    });
    vars.attchFiles = reactive({})
    vars.filter = reactive({
      items: [
        {
          name: 'fk_project_management_id',
          op: 'eq',
          val: props.id || 0,
        },
      ],
      projectParticipant: [
        {
          name: 'fk_project_management_id',
          op: 'eq',
          val: props.id || 0,
        },
      ],
      projectCompany: [
        {
          name: 'fk_project_management_id',
          op: 'eq',
          val: props.id || 0,
        },
      ],
      projectDocument: [
        {
          name: 'fk_project_management_id',
          op: 'eq',
          val: props.id || 0,
        },
      ],
      projectDailyLog: [
        {
          name: 'fk_project_management_id',
          op: 'eq',
          val: props.id || 0,
        },
      ],
      projectCostLog: [
        {
          name: 'fk_project_management_id',
          op: 'eq',
          val: props.id || 0,
        },
      ],
      projectOutCostLog: [
        {
          name: 'fk_project_management_id',
          op: 'eq',
          val: props.id || 0,
        },
      ],
      projectCompletion: [
        {
          name: 'fk_project_management_id',
          op: 'eq',
          val: props.id || 0,
        },
      ],
      materialApproval: [
        {
          name: 'fk_project_management_id',
          op: 'eq',
          val: props.id || 0,
        },
      ],
      projectConstruction: [
        {
          name: 'fk_project_management_id',
          op: 'eq',
          val: props.id || 0,
        },
      ],
      customer_information: [
        { 
          name: 'fk_business_id', op: 'eq', val: 0 
        }
      ],
      note : [
        { 
          name: 'fk_business_id', op: 'eq', val: 0 
        }
      ],
      businessCost: { fk_business_id : 0 },
      quoteItem: { fk_business_id : 0 },
    });
    vars.dataSource = reactive({
      baseItem: null,
      items: null,
      progress_status: null,
      project_important: null,
      department: null,
      project_manager: null,
      projectParticipant: null,
      projectCompany: null,
      company_type: null,
      clientDetail: null,
      defect_period: null,
      businessCost: null,
      quoteItem: null,
      materialApproval: null,
      vat_type: null,
      projectDailyLog: null,
      projectCostLog: null,
      projectCompletion: null,
      work_type: null,
      projectOutCostLog: null,
      projectConstruction: null,
      construction: null,
      completion: null,
    });
    vars.dataSource.note = getProjectBusinessNote(vars.filter.note);

    vars.dataSource.customer_information = getProjectCustomerInformation(vars.filter.customer_information);

    vars.dataSource.items = getProjectItem(vars.filter.items);
    
    vars.dataSource.projectParticipant = getProjectParticipant(vars.filter.projectParticipant);

    vars.dataSource.projectCompany = getProjectCompany(vars.filter.projectCompany);

    vars.dataSource.projectDocument = getProjectDocument(vars.filter.projectDocument);

    vars.dataSource.projectDailyLog = getProjectDailyLog(vars.filter.projectDailyLog);

    vars.dataSource.projectCostLog = getProjectCostLog(vars.filter.projectCostLog);

    vars.dataSource.projectOutCostLog = getProjectOutCostLog(vars.filter.projectOutCostLog);

    vars.dataSource.projectCompletion = getProjectCompletion(vars.filter.projectCompletion);

    vars.dataSource.materialApproval = getProjectMaterialApproval(vars.filter.materialApproval);

    vars.dataSource.projectConstruction = getProjectConstruction(vars.filter.projectConstruction);

    vars.disabled = reactive({
      edit: true,
      delete: true,
      save: true,
      clientDetail: false,
      exportToShipmentOrder: false,
      exportToWorkOrder: false,
    });
    vars.costLogInvoice = reactive({
      rowData: null,
      rowIndex: null
    });

    
    onMounted(async () => {
      await loadDepartment(vars.dataSource);
      await methods.loadBaseCode();
      methods.initById(props.id);
      if(props.business_id){
        await methods.initByBusiness(props.business_id)
      }
      
    });

    // public methods
    const methods = {
      // 프로젝트 찾기를 누르면 돋보기 누르면 쭉 뜸. 프로젝트를 눌렀을 때 조회하는 method
      async initById(id) {

        vars.init.value = true;
        methods.gridItemsRefresh(id);
        methods.gridProjectParticipantRefresh(id);
        methods.gridProjectCompanyRefresh(id);
        methods.gridProjectDocumentRefresh(id);
        methods.gridProjectDailyLogRefresh(id);
        methods.gridProjectCostLogRefresh(id);
        methods.gridProjectOutCostLogRefresh(id);
        methods.gridProjectCompletionRefresh(id);
        methods.gridMaterialApprovalRefresh(id);
        methods.gridProjectConstructionRefresh(id);
        // 아이디 없으면 끝냄(props)
        if (!id) {
          methods.clearFormData();
          methods.gridQuoteItemsRefresh();
          methods.gridBusinessCostRefresh();
          vars.disabled.edit = true;
          vars.disabled.delete = true;
          vars.disabled.save = true;
          return;
        }

        let { data } = await projectRegistration.byKey(id);
        // 필터를 넣어줌
        vars.filter.customer_information[0].val = data.fk_business_id ? data.fk_business_id : 0;
        vars.filter.note[0].val = data.fk_business_id ? data.fk_business_id : 0;
        // 이 시점에서 값을 조회되도록 해줌
        vars.dataSource.customer_information = getProjectCustomerInformation(vars.filter.customer_information);
        vars.dataSource.note = getProjectBusinessNote(vars.filter.note);

        Object.assign(vars.formData, data);
        methods.gridQuoteItemsRefresh();
        methods.gridBusinessCostRefresh();
        vars.disabled.edit = false;
        methods.enableDelete();
        methods.enableSave();

        methods.exportToVisible();

      },
      clearFormData() {
        vars.formData.business = null;
        vars.formData.id = null;
        vars.formData.created = null;
        vars.formData.project_number = '';
        vars.formData.project_name = '', // 계약건명
        vars.formData.project_date = '', // 등록 일자
        vars.formData.order_company = '', // 원발주처
        vars.formData.contract_company = '', // 
        vars.formData.project_department = '', // 
        vars.formData.project_manager = '', // 
        vars.formData.contract_date = '', // 
        vars.formData.defect_end_date = '', // 
        //vars.formData.contract_amount = 0, // 
        vars.formData.commencement_date = '', //착공일자
        vars.formData.non_invoice = 0, // 미계산서
        vars.formData.contract_vat_type = '', // 
        vars.formData.company_vat_type = '', // 
        vars.formData.completion_date = '', // 계약완료
        vars.formData.subcontracting_rate = 0, // 
        vars.formData.defect_period = '', // 
        vars.formData.company_amount = 0, // 
        vars.formData.progress_status = '', // 
        vars.formData.project_important = '', // 
        vars.formData.location = '', // 
        vars.formData.modify_manager = null;
        vars.formData.modify_date = null;
        vars.formData.fk_business_id = null;
        vars.formData.fk_company_id = authService.getCompanyId();
      },
      generateItemSelectOption(items = [], value = '', searchEnabled = false) {
        return { value, searchEnabled, items };
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
        stateStore.bind(`project-registration-${key}`, evt.component);
      },
      loadBaseCode(){
        return baseCodeLoader(['부가세구분', '진행단계', '중요', '업체구분', '하자기간', '업무유형', '착공계(문서명)', '준공계(문서명)']).then(response =>{
          // vars.dataSource.vat_type = response['부가세구분'];
          vars.dataSource.vat_type = response['부가세구분'].filter((v)=> v.code_name != "영세");
          vars.dataSource.progress_status = response['진행단계'];
          vars.dataSource.project_important = response['중요'];
          vars.dataSource.company_type = response['업체구분'];
          vars.dataSource.defect_period = response['하자기간']
          vars.dataSource.work_type = response['업무유형']
          vars.dataSource.construction = response['착공계(문서명)']
          vars.dataSource.completion = response['준공계(문서명)']
        })
        .then(() => (vars.init.value = true));
      },
      async newItem() {
        methods.gridItemsRefresh();
        methods.gridProjectParticipantRefresh();
        methods.gridProjectCompanyRefresh();
        methods.gridProjectDocumentRefresh();
        methods.gridProjectDailyLogRefresh();
        methods.gridProjectCostLogRefresh();
        methods.gridProjectOutCostLogRefresh();
        methods.gridProjectCompletionRefresh();
        methods.gridQuoteItemsRefresh();
        methods.gridBusinessCostRefresh();
        if (vars.formData.id || vars.formData.fk_business_id) {
          methods.clearFormData();
          methods.redirect();
        }
        setTimeout(() => {
          methods.clearFormData();
          methods.setFormData();
        }, 200);
      },
      async initByBusiness(business_id){
        const {data : business } = await projectBusiness.load({
          filter: [
            ['id', '=', business_id]
          ]
        }) 
        vars.formData.business = business[0];
        vars.formData.fk_business_id = business_id;
        vars.formData.project_name = business[0].business_name;
        // vars.formData.project_number = business[0].business_number;
        vars.formData.company_amount = business[0].business_amount;
        vars.formData.non_invoice = business[0].business_amount;
        vars.formData.order_company = business[0].client_company;
        vars.formData.contract_company = business[0].contract_company;
        methods.setFormData();        
        methods.gridQuoteItemsRefresh();
        methods.gridBusinessCostRefresh();
      },
      setFormData(){
        vars.formData.project_department = authService.getDepartmentName();
        vars.formData.project_manager = authService.getUserName();
        vars.formData.contract_date = currentDateTime();
        vars.formData.project_date = currentDateTime();
        vars.formData.defect_end_date = currentDateTime();
        vars.formData.completion_date = currentDateTime();
        vars.formData.fk_company_id = authService.getCompanyId();
        vars.formData.progress_status = methods.getFirstItemName(vars.dataSource.progress_status);
        vars.formData.project_important = methods.getFirstItemName(vars.dataSource.project_important);
        vars.formData.contract_vat_type = methods.getFirstItemName(vars.dataSource.vat_type);
        vars.formData.company_vat_type = methods.getFirstItemName(vars.dataSource.vat_type);
        vars.formData.defect_period = methods.getFirstItemName(vars.dataSource.defect_period);

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
      addItemHidden(){
        const grid = vars.grid.items;
        if(!grid) return;
        grid.refresh();
      },

      
      async gridItemsRefresh(id) {
        if (!id) id = 0;
        vars.filter.items[0].val = id;
        vars.dataSource.items.defaultFilters = vars.filter.items;
        if (vars.grid.items) {
          vars.grid.items.cancelEditData();
          vars.grid.items.refresh();
        }
      },
      async gridQuoteItemsRefresh(){
        let fk_business_id = 0;
        if(vars.formData?.fk_business_id) fk_business_id = vars.formData.fk_business_id;
        vars.filter.quoteItem.fk_business_id = fk_business_id;
        methods.loadQuoteItem();
        if(vars.grid.quoteItem){
          vars.grid.quoteItem.cancelEditData();
          vars.grid.quoteItem.refresh();
        }
        
      },
      async gridBusinessCostRefresh(){
        let fk_business_id = 0;
        if(vars.formData?.fk_business_id) fk_business_id = vars.formData.fk_business_id;
        vars.filter.businessCost.fk_business_id = fk_business_id;
        methods.loadBusinessCost();
        if(vars.grid.businessCost){
          vars.grid.businessCost.cancelEditData();
          vars.grid.businessCost.refresh();
        }
      },
      async gridProjectParticipantRefresh(id) {
        if (!id) id = 0;
        vars.filter.projectParticipant[0].val = id;
        vars.dataSource.projectParticipant.defaultFilters = vars.filter.projectParticipant;
        if (vars.grid.projectParticipant) {
          vars.grid.projectParticipant.cancelEditData();
          vars.grid.projectParticipant.refresh();
        }
      },
      async gridProjectCompanyRefresh(id) {
        if (!id) id = 0;
        vars.filter.projectCompany[0].val = id;
        vars.dataSource.projectCompany.defaultFilters = vars.filter.projectCompany;
        if (vars.grid.projectCompany) {
          vars.grid.projectCompany.cancelEditData();
          vars.grid.projectCompany.refresh();
        }
      },
      async gridProjectDocumentRefresh(id) {
        if (!id) id = 0;
        vars.filter.projectDocument[0].val = id;
        vars.dataSource.projectDocument.defaultFilters = vars.filter.projectDocument;
        if (vars.grid.projectDocument) {
          vars.grid.projectDocument.cancelEditData();
          vars.grid.projectDocument.refresh();
        }
      },
      async gridProjectDailyLogRefresh(id) {
        if (!id) id = 0;
        vars.filter.projectDailyLog[0].val = id;
        vars.dataSource.projectDailyLog.defaultFilters = vars.filter.projectDailyLog;
        if (vars.grid.projectDailyLog) {
          vars.grid.projectDailyLog.cancelEditData();  
          vars.grid.projectDailyLog.refresh();
        }
      },
      async gridProjectCostLogRefresh(id) {
        if (!id) id = 0;
        vars.filter.projectCostLog[0].val = id;
        vars.dataSource.projectCostLog.defaultFilters = vars.filter.projectCostLog;
        if (vars.grid.projectCostLog) {
          vars.grid.projectCostLog.cancelEditData();  
          vars.grid.projectCostLog.refresh();
        }
      },
      async gridProjectOutCostLogRefresh(id) {
        if (!id) id = 0;
        vars.filter.projectOutCostLog[0].val = id;
        vars.dataSource.projectOutCostLog.defaultFilters = vars.filter.projectOutCostLog;
        if (vars.grid.projectOutCostLog) {
          vars.grid.projectOutCostLog.cancelEditData();
          vars.grid.projectOutCostLog.refresh();
        }
      },
      async gridProjectCompletionRefresh(id) {
        if (!id) id = 0;
        vars.filter.projectCompletion[0].val = id;
        vars.dataSource.projectCompletion.defaultFilters = vars.filter.projectCompletion;
        if (vars.grid.projectCompletion) {
          vars.grid.projectCompletion.cancelEditData();  
          vars.grid.projectCompletion.refresh();
        }
      },
      async gridMaterialApprovalRefresh(id) {
        if (!id) id = 0;
        vars.filter.materialApproval[0].val = id;
        vars.dataSource.materialApproval.defaultFilters = vars.filter.materialApproval;
        if (vars.grid.materialApproval) {
          vars.grid.materialApproval.cancelEditData();
          vars.grid.materialApproval.refresh();
        }
      },
      async gridProjectConstructionRefresh(id) {
        if (!id) id = 0;
        vars.filter.projectConstruction[0].val = id;
        vars.dataSource.projectConstruction.defaultFilters = vars.filter.projectConstruction;
        if (vars.grid.projectConstruction) {
          vars.grid.projectConstruction.cancelEditData();
          vars.grid.projectConstruction.refresh();
        }
      },
      finderReturnHandler(data) {
        switch (vars.dlg.finder.key) {
          case 'project': {
            methods.redirect(data.id);
            vars.formState.readOnly = true;
            break;
          }
          case 'order_company': {
            vars.formData.order_company = data.name;
            break;
          }
          case 'contract_company': {
            vars.formData.contract_company = data.name;
            break;
          }
          case 'company_name': {
            if(vars.focus.projectCompany){
              vars.grid.projectCompany.cellValue(
                vars.focus.projectCompany.rowIndex,
                'company_name',
                data.name
              );
            }else{
              vars.grid.projectCompany.cellValue(
                0,
                'company_name',
                data.name
              );
            }
            break;
          }
          case 'company_manager':{
            if(vars.focus.projectCompany){
              vars.grid.projectCompany.cellValue(
                vars.focus.projectCompany.rowIndex,
                'company_manager',
                data.name
              )
              if(data.mobile){
                vars.grid.projectCompany.cellValue(
                vars.focus.projectCompany.rowIndex,
                'company_manager_phone',
                data.mobile
              )
              }
              
            }
            break;
          }
          case 'business': {
            vars.filter.quoteItem.fk_business_id = data.id;
            vars.filter.businessCost.fk_business_id = data.id;
            vars.formData.fk_business_id = data.id;
            vars.formData.business = data;
            vars.formData.project_name = data.business_name;
            // vars.formData.project_number = data.business_number;
            vars.formData.company_amount = data.business_amount;
            vars.formData.non_invoice = data.business_amount;
            vars.formData.contract_company = data.contract_company;
            methods.gridQuoteItemsRefresh();
            methods.gridBusinessCostRefresh();
            break;
          }
          case 'excution_plan': {
            vars.formData.fk_excution_plan_id = data.id;
            vars.formData.excution_plan = data;
            break;
          }
          case 'project_manager': {
            if(vars.focus.projectParticipant){
              vars.grid.projectParticipant.cellValue(
                vars.focus.projectParticipant.rowIndex,
                'project_manager',
                data.emp_name
              )
            }else{
              vars.grid.projectParticipant.cellValue(
                0,
                'project_manager',
                data.emp_name
              );
            }
            break;
          }
        }

        vars.dlg.finder.show = false;
        vars.dlg.finder.title = '';
        vars.dlg.finder.key = null;
        vars.dlg.finder.data = null;
      },
      async managerOnClick(){
        if(!vars.grid.projectCompany || !vars.focus.projectCompany)return;
 
        const cellValue = vars.grid.projectCompany.cellValue(vars.focus.projectCompany.rowIndex, 'company_name');
    
        if(!cellValue) return;

        const { data } = await baseClient.load({
          filter: [
            ['name', '=', cellValue]
          ]
        })
  
        if(!data.length) return;

        vars.dlg.finder.key = 'company_manager';
        vars.dlg.finder.data = { fk_client_id: data[0].id };
        vars.dlg.finder.title = '업체담당자조회';
        vars.dlg.finder.show = true;

      },
      updateEtcValue(v) {
        vars.dlg.finder.data = v;
      },
      async saveItem() {
        let isSelect = await confirm('저장하시겠습니까?', '저장');
        if (!isSelect) {
          return;
        }
        
        vars.loading.value = true;
        try {
          const items = vars.grid.items;
          const projectParticipant = vars.grid.projectParticipant;
          const projectCompany = vars.grid.projectCompany;
          const projectDocument = vars.grid.projectDocument;
          const projectDailyLog = vars.grid.projectDailyLog;
          const projectCostLog = vars.grid.projectCostLog;
          const projectOutCostLog = vars.grid.projectOutCostLog;
          const projectCompletion = vars.grid.projectCompletion;
          const materialApproval = vars.grid.materialApproval;
          const projectConstruction = vars.grid.projectConstruction;
          const projectNote = vars.grid.note;
          const projectCustomerInformation = vars.grid.customer_information;
          if (vars.formData.id) {
            // 기존 정보 업데이트
            vars.formData.modify_manager = authService.getUserName();
            vars.formData.modify_date = moment().format('YYYY-MM-DD HH:mm:ss');
            const updateDate = Object.assign({}, vars.formData);
            if(updateDate.business){
              updateDate.business.business_name = vars.formData.project_name;
            }
            if(updateDate.excution_plan){
              updateDate.excution_plan.contract_amount = updateDate.company_amount;
            }

            const { data } = await projectRegistration.update(
              vars.formData.id,
              updateDate
            );
            if (projectNote) {
              await projectNote.saveEditData();
            }

            if (projectCustomerInformation) {
              await projectCustomerInformation.saveEditData();
            }            
            if (items) {
              await items.saveEditData();
              await methods.exportToVisible();
            }
 
            if (projectParticipant) {
              await projectParticipant.saveEditData();
            }

            if (projectCompany) {
              await projectCompany.saveEditData();
            }
            
            if (projectDocument) {
              await projectDocument.saveEditData();
            }

            if (projectDailyLog) {
              await projectDailyLog.saveEditData();
            }

            if (projectCostLog) {
              await projectCostLog.saveEditData();
            }

            if (projectOutCostLog) {
              await projectOutCostLog.saveEditData();
            }

            if (projectCompletion) {
              await projectCompletion.saveEditData();
            }

            if (materialApproval) {
              await materialApproval.saveEditData();
            }

            if (projectConstruction) {
              await projectConstruction.saveEditData();
            }

            vars.formState.readOnly = true;

            notifyInfo('저장되었습니다');
            methods.enableSave();
            methods.enableDelete();

          } else {
            // 채번이 없을 경우 자동 채번
            delete vars.formData.created;
            delete vars.formData.id;
            if(vars.formData.business){
              vars.formData.business.business_name = vars.formData.project_name;
            }
            let { data } = await projectRegistration.insert(vars.formData);
            vars.formData.id = data.id;

            if (projectNote && projectNote.hasEditData()) {
              await projectNote.saveEditData();
            }
            if (projectCustomerInformation && projectCustomerInformation.hasEditData()) {
              await projectCustomerInformation.saveEditData();
            }                        
            if (items && items.hasEditData()) {
              await items.saveEditData();
            }

            if (projectParticipant && projectParticipant.hasEditData()) {
              await projectParticipant.saveEditData();
            }
            
            if (projectCompany && projectCompany.hasEditData()) {
              await projectCompany.saveEditData();
            }
      
            if (projectDocument && projectDocument.hasEditData()) {
              await projectDocument.saveEditData();
            }

            if (projectDailyLog && projectDailyLog.hasEditData()) {
              await projectDailyLog.saveEditData();
            }

            if (projectCostLog && projectCostLog.hasEditData()) {
              await projectCostLog.saveEditData();
            }

            if (projectOutCostLog && projectOutCostLog.hasEditData()) {
              await projectOutCostLog.saveEditData();
            }

            if (projectCompletion && projectCompletion.hasEditData()) {
              await projectCompletion.saveEditData();
            }

            if (materialApproval && materialApproval.hasEditData()) {
              await materialApproval.saveEditData();
            }

            if (projectConstruction && projectConstruction.hasEditData()) {
              await projectConstruction.saveEditData();
            }

            notifyInfo('저장되었습니다');
            methods.redirect(data.id);
            vars.formState.readOnly = true;
          }
        } catch (ex) {
          if (ex.response.status === 602) {
            notifyError('이미 존재하는 프로젝트번호 입니다');
          } else {
            console.error(ex);
            notifyError('저장 할 내용이 없습니다');
          }
        } finally {
          vars.loading.value = false;
        }
        console.log('저장 직전 날짜:', vars.formData.commencement_date);

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
              vars.dataSource.project_manager = data;
            });
            vars.warehouse = { ...selectItem.warehouse };
        }else{
          vars.warehouse = {};
        }
      },
      setCostDate(newData, value, currentRowData){
  
        const getVisibleRows = vars.grid.projectCostLog.getVisibleRows();
        const filteredRows = getVisibleRows.filter(row => row.data.id !== undefined);
        if(filteredRows.length == 0){
          newData.cost_date = moment(value).format('YYYY-MM-DD');
          return;
        }
        
        const maxKeyRow = filteredRows.reduce((max, row) => {
          return (row.data.id > max.data.id) ? row : max;
        }, filteredRows[0]);

        const newCostDate = moment(value).format('YYYY-MM-DD');
        
    
        if (moment(maxKeyRow.data.cost_date).isBefore(newCostDate)) {
          newData.cost_date = newCostDate;
        } else {
          notifyError('일자는 이전 기성 일자보다 이후여야 합니다');
        }
  
      },
      setOutCostDate(newData, value, currentRowData){
        
        const getVisibleRows = vars.grid.projectOutCostLog.getVisibleRows();
        const filteredRows = getVisibleRows.filter(row => row.data.id !== undefined);
        if(filteredRows.length == 0){
          newData.cost_date = moment(value).format('YYYY-MM-DD');
          return;
        }
        const maxKeyRow = filteredRows.reduce((max, row) => {
          return (row.data.id > max.data.id) ? row : max;
        }, filteredRows[0]);

        const newCostDate = moment(value).format('YYYY-MM-DD');
        
        if (moment(maxKeyRow.data.cost_date).isBefore(newCostDate)) {
          newData.cost_date = newCostDate;
        } else {
          notifyError('일자는 이전 외주기성 일자보다 이후여야 합니다');
        }
      },
      setCurrCost(newData, value, currentRowData){
        const remaining_cost = currentRowData.remaining_cost + currentRowData.curr_cost;
        const cumulative_cost = currentRowData.cumulative_cost - currentRowData.curr_cost;
   
        newData.curr_cost = value;
        newData.remaining_cost = remaining_cost - value;
        newData.cumulative_cost = cumulative_cost + value;
        newData.total_cost_rate = (newData.cumulative_cost / vars.formData.company_amount);
      },
      setOutCurrCost(newData, value, currentRowData){
        const remaining_cost = currentRowData.remaining_cost + currentRowData.curr_cost;
        const cumulative_cost = currentRowData.cumulative_cost - currentRowData.curr_cost;
   
        newData.curr_cost = value;
        newData.remaining_cost = remaining_cost - value;
        newData.cumulative_cost = cumulative_cost + value;
        newData.total_cost_rate = (newData.cumulative_cost / (remaining_cost + cumulative_cost));

      },
      onEditRowButtonCostLog(e){
        const grid = vars.grid.projectCostLog.getVisibleRows()
          .sort((a, b) => a.data.key - b.data.key);
  
        const maxKey = grid.reduce((max, row) => {
          return (row.data.id > max) ? row.data.id : max;
        }, grid[0].data.id);
        if(maxKey == e.row.key){
          e.component.editRow(e.row.rowIndex)
        }else{
          notifyError('마지막 기성 외에는 내역을 수정할 수 없습니다');
        }
      },
      onEditRowButtonOutCostLog(e) {
        const grid = vars.grid.projectOutCostLog.getVisibleRows()
          .sort((a, b) => a.data.key - b.data.key);
  
        const maxKey = grid.reduce((max, row) => {
          return (row.data.id > max) ? row.data.id : max;
        }, grid[0].data.id);
        if(maxKey == e.row.key){
          e.component.editRow(e.row.rowIndex)
        }else{
          notifyError('마지막 외주기성 외에는 내역을 수정할 수 없습니다');
        }
      },
      onDeleteRowButtonCostLog(e){
        const grid = vars.grid.projectCostLog.getVisibleRows()
          .sort((a, b) => a.data.key - b.data.key);
  
        const maxKey = grid.reduce((max, row) => {
          return (row.data.id > max) ? row.data.id : max;
        }, grid[0].data.id);
        if(maxKey == e.row.key){
          e.component.deleteRow(e.row.rowIndex)
        }else{
          notifyError('마지막 기성 외에는 내역을 삭제할 수 없습니다');
        }
      },
      onDeleteRowButtonOutCostLog(e){
        const grid = vars.grid.projectOutCostLog.getVisibleRows()
          .sort((a, b) => a.data.key - b.data.key);
  
        const maxKey = grid.reduce((max, row) => {
          return (row.data.id > max) ? row.data.id : max;
        }, grid[0].data.id);
        if(maxKey == e.row.key){
          e.component.deleteRow(e.row.rowIndex)
        }else{
          notifyError('마지막 외주기성 외에는 내역을 삭제할 수 없습니다');
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
            await projectRegistration.remove(vars.formData.id);
            await alert('삭제되었습니다', '삭제 확인');
            methods.redirect();
            vars.formState.readOnly = true;
            methods.gridItemsRefresh();
            methods.gridProjectParticipantRefresh();
            methods.gridProjectCompanyRefresh();
            methods.gridProjectDocumentRefresh();
            methods.gridProjectDailyLogRefresh();
            methods.gridProjectCostLogRefresh();
            methods.gridProjectOutCostLogRefresh();
            methods.gridProjectCompletionRefresh();
            methods.gridMaterialApprovalRefresh();
            methods.gridProjectConstructionRefresh();
            methods.gridQuoteItemsRefresh();
            methods.gridBusinessCostRefresh();
          }
        }
        catch(ex){
          console.error(ex);
          notifyError('연결된 데이터가 있어서 삭제가 안됩니다');
        }
      
      },
      redirect(id) {
        if (id) router.replace({ path: `/project/registration/${id}` });
        else router.replace({ path: `/project/registration` });
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
      // ❌ 삭제: 더 이상 사용되지 않음
      // onContractVatTypeChanged(e) { ... }

      // ✅ 유지
      onCompanyVatTypeChanged(e) {
        if (!e.event) return;
        methods.calculateContractRatio();
      },

      // ❌ 삭제: contract_amount와 연결되었으므로 제거
      // onContractAmountChanged(e) { ... }

      // ✅ 유지
      onCompanyAmountChanged(e) {
        if (!e.event) return;
        vars.formData.non_invoice = e.value;
        methods.calculateContractRatio();
      },

      // 🔄 수정된 계산 로직: company_amount만 사용
      calculateContractRatio() {
        if (vars.formData.company_amount === 0) {
          vars.formData.subcontracting_rate = '0.00%';
          return;
        }

        const company_response = calcPriceSummary(
          vars.formData.company_vat_type,
          vars.formData.company_amount
        );

        // 하도급률이 의미 있다면 하도급 금액 기준으로 계산 (예: company_amount 중 하도급 비율)
        // 지금은 기준이 하나뿐이라 비율은 항상 100% (또는 0%로 설정할 수도 있음)
        const ratio = 100;

        vars.formData.subcontracting_rate = ratio.toFixed(2) + '%';
      },

      // onContractVatTypeChanged(e){
      //   if(!e.event) return;
      //   methods.calculateContractRatio();
      // },
      // onCompanyVatTypeChanged(e) {
      //   if(!e.event) return;
      //   methods.calculateContractRatio();
      // },
      // onContractAmountChanged(e){
      //   if(!e.event) return;
      //   methods.calculateContractRatio();
      // },
      // onCompanyAmountChanged(e){
      //   if(!e.event) return;
      //   vars.formData.non_invoice = e.value;
      //   methods.calculateContractRatio();
      // },
      // calculateContractRatio() {
      //     if (vars.formData.contract_amount === 0) {
      //       vars.formData.subcontracting_rate = 0 + "%";
      //       return;
      //     }
      //     const contract_response = calcPriceSummary(vars.formData.contract_vat_type, vars.formData.contract_amount);
      //     const company_response = calcPriceSummary(vars.formData.company_vat_type, vars.formData.company_amount);

      //     const ratio = (company_response.supply_price / contract_response.supply_price) * 100;

      //     const roundedRatio = Math.ceil(ratio * 1000) / 1000;
   
      //     vars.formData.subcontracting_rate = roundedRatio.toFixed(2) + "%";
      //     return;
      // },
      defectPeriodChanged(e){
        if(!vars.formData.completion_date) return;
        methods.calDefectPeriod(e.value);
        
      },
      calDefectPeriod(v){
        const regex = /^(\d+)(일|달|월|년)$/;
        const match = v.match(regex);
        if (!match) {
          return;
        }
        const number = parseInt(match[1], 10);
        const unit = match[2];

        const completionDate = new Date(vars.formData.completion_date);
        switch (unit) {
        case '일':
            completionDate.setDate(completionDate.getDate() + number);
            break;
        case '달':
        case '월':
            completionDate.setMonth(completionDate.getMonth() + number);
            break;
        case '년':
            completionDate.setFullYear(completionDate.getFullYear() + parseInt(number));
            break;
        default:
            throw new Error("알 수 없는 단위입니다.");
        }
        vars.formData.defect_end_date = completionDate.toISOString();
      },
      isFilledFormRequiredData(){
        if(vars.formData.project_name && vars.formData.project_manager){
          return true;
        }
        return false;
      },
      async addSelectedRows(rows) {
        const grid = vars.grid.items;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        for (let row of rows) {
          await grid.addRow();
          /*
          grid.cellValue(0, 'quantity', 0); // 수량
          grid.cellValue(0, 'item_code', row.item_code); // 품목코드
          grid.cellValue(0, 'item.item_name', row.item_name); // 품명
          grid.cellValue(0, 'item.item_standard', row.item_standard); // 규격
          grid.cellValue(0, 'item.fk_project_management_id', props.id); // 프로젝트번호
          */
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.quantity = 0; // 수량
          data.not_ordered = 0; // 미수주수량
          data.item_code = row.item_code; // 품목코드
          data.item = { ...row }; // 품목
        }
        vars.dlg.addItem.show = false;
      },
      async addSelectedCostRows(){
        const grid = vars.grid.items;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }
        const rows = vars.grid.businessCost.getSelectedRowsData();
        for (let row of rows) {
          await grid.addRow();
        
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code; // 품목코드
          data.item = { ...row.item }; // 품목
          data.quantity = row.quote_quantity; // 수량
          data.not_ordered = row.quote_quantity; // 미수주수량
          data.fk_business_cost_id = row.id; // 원가검토 FK
        }
        vars.dlg.addBusinessCost.show = false;
      },
      async addSelectedQuoteRows(){
        const grid = vars.grid.items;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }
        const rows = vars.grid.quoteItem.getSelectedRowsData();
        for (let row of rows) {
          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.quantity = row.quote_quantity; // 수량
          data.not_ordered = row.quote_quantity; // 미수주수량
          data.item_code = row.item_code; // 품목코드
          data.item = { ...row.item }; // 품목
          data.fk_shipment_quote_item_id = row.id; // 견적 품목 FK
        }
        vars.dlg.addQuoteItem.show = false;
      },
      showAddPopup() {
        vars.dlg.addItem.show = true;
      },
      showAddBusinessCostButton(){
        if(!vars.grid.businessCost){
          vars.dlg.addBusinessCost.show = true;
          setTimeout(() => {
            methods.showAddBusinessCost();
          }, 50);
          return;
        }
        methods.showAddBusinessCost();
      },
      showAddQuoteItemButton(){
        if(!vars.grid.quoteItem){
          vars.dlg.addQuoteItem.show = true;
          setTimeout(() => {
            methods.showAddQuoteItem();
          }, 50);
          return;
        }
        methods.showAddQuoteItem();
      },
      showAddQuoteItem(){
        const notContains = [];
  
        for (const item of vars.grid.items.getVisibleRows()){
          if(item.data.fk_shipment_quote_item_id){
            notContains.push(['id', '<>', item.data.fk_shipment_quote_item_id], 'and');
          }
        }
        notContains.pop();
      
        if (vars.grid.quoteItem){
          vars.grid.quoteItem.filter(notContains);
          vars.grid.quoteItem.clearSelection();
          vars.grid.quoteItem.refresh();
        } 
        vars.dlg.addQuoteItem.show = true;
        
      },
      showAddBusinessCost(){
        const notContains = [];
        for (const item of vars.grid.items.getVisibleRows()){
          if(item.data.fk_business_cost_id){
            notContains.push(['id', '<>', item.data.fk_business_cost_id], 'and');
          }
        }
        notContains.pop();
        if(vars.grid.businessCost){
          vars.grid.businessCost.filter(notContains);
          vars.grid.businessCost.clearSelection();
          vars.grid.businessCost.refresh();
        }
        vars.dlg.addBusinessCost.show = true;
      },
      loadBaseItem() {
        baseItem
          .load({
            filter: [['fk_company_id', '=', authService._user.fk_company_id]],
          })
          .then(({ data }) => {
            vars.dataSource.baseItem = data;
          });
      },
      async loadBusinessCost(){
        vars.dataSource.businessCost = getProjectBusinessCost([
          {
            name: 'fk_business_id',
            op: 'eq',
            val: vars.filter.businessCost.fk_business_id,
          },
        ]);
      },
      async loadQuoteItem() {
        const { data } = await shipmentQuote.load({filter:['fk_business_id', '=', vars.filter.quoteItem.fk_business_id],take:1, skip:0, sort: [{ selector: 'quote_number', desc: true}]})
        let quote_number = ''
        if(data.length){
          quote_number = data[0].quote_number;
        }
        vars.dataSource.quoteItem = getShipmentQuoteItem([
          {
            name: 'quote',
            op: 'has',
            val: {
              name: 'quote_number',
              op: 'eq',
              val: quote_number,
            },
          },
          {
            name: 'fk_parent_id',
            op: 'is_null',
          }
        ]);
      },
      setQuantity(newData, value, currentRowData) {
        const diff = value - currentRowData.quantity;
        const notOrdered = currentRowData.not_ordered + diff;
        if (notOrdered >= 0) {
          newData.not_ordered = notOrdered;
          newData.quantity = value;
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
      async updateUploadFile(element){
        for (const key in element.data){
          
          if(vars.attchFiles[element.data[key]]){
            const fd = new FormData()
            fd.append('file', vars.attchFiles[element.data[key]], vars.attchFiles[element.data[key]].name)
            
            if(key == 'file_name'){
              const {data: filename} = await uploadService.post('document', fd)
              element.data['file_path'] = `project-document/${filename}`
            }else if (key == 'attachment'){
              const {data: filename} = await uploadService.post('daily-log', fd)
              element.data['attachment_path'] = `project-daily-log/${filename}`
            }
            delete vars.attchFiles[element.data[key]]
          }
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
      onSavingItem(e, item) {
        if (item == 'customer_information' || item == 'note') {
          e.promise = methods.onSavingItemImpl2(e);
        } else {
          e.promise = methods.onSavingItemImpl(e);
        }
      },
      async onSavingItemImpl(e){
        for(const element of e.changes){
          if(element.type != 'remove'){
            element.data.fk_project_management_id = vars.formData.id;
            delete element.data.item;
            await methods.updateUploadFile(element);
          }
        }
      },

      async onSavingItemImpl2(e) {
        for(const element of e.changes){
          if(element.type != 'remove'){
            element.data.fk_business_id = vars.formData.fk_business_id;        // ✅ 외래키 (영업건 ID)      
            // delete element.data.item;
          }
        }
      },

      onFocusedCellChanged(e, item){
        vars.focus[item] = e;
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
        if (!grid) return;

        if (item === 'projectOutCostLog') {
          if (!vars.formData.fk_excution_plan_id) {
            alert('실행계획이 존재하지 않습니다', '외주기성 추가');
            return;
          }

          const subcontract = await projectExcutionPlanSubcontract.load({
            filter: [['fk_project_excution_plan_id', '=', vars.formData.fk_excution_plan_id]]
          });

          if (subcontract?.totalCount <= 0) {
            alert('실행계획에 외주공사가 존재하지 않습니다', '외주기성 추가');
            return;
          }

          const visibleRows = grid.getVisibleRows();
          
          // 첫 행 추가 시 초기값 설정
          if (visibleRows.length === 0) {
            // const amount = subcontract?.data?.reduce((acc, curr) => acc + curr.expect_amount, 0) || 0;
            const amount = subcontract.data[0].expect_amount;
            if (amount <= 0) {
              alert('외주공사 예정금액이 0원입니다', '외주기성 추가');
              return;
            }

            grid.on("initNewRow", (e) => {
              e.data.prev_cost = 0;
              e.data.curr_cost = 0;
              e.data.cumulative_cost = 0;
              e.data.remaining_cost = amount;
              e.data.total_cost_rate = 0;
              e.data.register = authService.getUserName();
              e.data.register_date = currentDateTime();
            });
            await grid.addRow();
            grid.off("initNewRow");
          } else {
            await grid.addRow();
          }
          return;
        }

        await grid.addRow();
      },
      async itemSaveButton(item){
        if(!vars.formData.id) return;
        const grid = vars.grid[item];
        if(grid && grid.hasEditData()){
          await grid.saveEditData();
        }
      },
      async initNewRow(e, item){
        const userName = authService.getUserName();
        if(item == 'projectParticipant'){
          // e.data.project_manager = userName;
        }else if(item == 'projectDailyLog'){
          e.data.register = userName;
          e.data.register_date = currentDateTime();
        }else if(item == 'projectCostLog'){
          const getVisibleRows = vars.grid.projectCostLog.getVisibleRows();
          if(getVisibleRows.length <= 0){
            e.data.prev_cost = 0;
            e.data.curr_cost = 0;
            e.data.cumulative_cost = 0;
            e.data.remaining_cost = vars.formData.company_amount;
            e.data.total_cost_rate = 0;
          }else{
            e.data.prev_cost = getVisibleRows[getVisibleRows.length - 1].data.cumulative_cost;
            e.data.curr_cost = 0;
            e.data.cumulative_cost = getVisibleRows[getVisibleRows.length - 1].data.cumulative_cost;
            e.data.remaining_cost = getVisibleRows[getVisibleRows.length - 1].data.remaining_cost;
            e.data.total_cost_rate = getVisibleRows[getVisibleRows.length - 1].data.total_cost_rate;
          }
          e.data.register = userName;
          e.data.register_date = currentDateTime();
        }else if(item == 'projectOutCostLog') {
          const getVisibleRows = vars.grid.projectOutCostLog.getVisibleRows();
          if(getVisibleRows.length <= 0){
            return;
          }else{
            e.data.prev_cost = getVisibleRows[getVisibleRows.length - 1].data.cumulative_cost;
            e.data.curr_cost = 0;
            e.data.cumulative_cost = getVisibleRows[getVisibleRows.length - 1].data.cumulative_cost;
            e.data.remaining_cost = getVisibleRows[getVisibleRows.length - 1].data.remaining_cost;
            e.data.total_cost_rate = getVisibleRows[getVisibleRows.length - 1].data.total_cost_rate;
          }
          e.data.register = userName;
          e.data.register_date = currentDateTime();
        }else if(item == 'projectCompletion'){
          e.data.register = userName;
          e.data.register_date = currentDateTime();
        }
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
      async onDocumentRemoving(e){
        const apiService = new ApiService('/api/server/v1/project-document');
        return await apiService.post(`remove/${e.data.id}`) 
      },
      async onCompletionRemoving(e){
        const apiService = new ApiService('/api/server/v1/project-completion');
        return await apiService.post(`remove/${e.data.id}`) 
      },
      async onConstructionRemoving(e){
        const apiService = new ApiService('/api/server/v1/project-construction');
        return await apiService.post(`remove/${e.data.id}`) 
      },
      async onMaterialApprovalRemoving(e){
        const apiService = new ApiService('/api/server/v1/project-material-approval');
        return await apiService.post(`remove/${e.data.id}`) 
      },
      async onDailyLogRemoving(e){
        const apiService = new ApiService('/api/server/v1/project-daily-log');
        return await apiService.post(`remove/${e.data.id}`) 
      },
      projectCompanyCellClick(e){
        if(!vars.formState.readOnly) return;
        if(e.column && e.column.name == 'company_name'){
          vars.disabled.clientDetail = true;
          vars.dataSource.clientDetail = e.data.company_name;
        }
      },
      businessNumberOptions(){
        if(vars.formState.readOnly){
          return {
            readOnly: true,
            buttons: [
            {
              name: 'business_number',
              location: 'after',
              options:{
                icon: 'link',
                stylingMode: 'text',
                disabled: false,
                onClick: methods.redirectToBusiness
              },
            },
            ],
          }
        }else{
          return {
            ...methods.generateItemButtonOption(
              'search',
              methods.createFindPopupFn('business', '영업 조회', {name : 'fk_project_management_id', op: 'is_null'})
            ),
            ...vars.formState,
          }
        }
      },
      excutionPlanNumberOptions(){
        if(vars.formState.readOnly){
          return {
            readOnly: true,
            buttons: [
            {
              name: 'excution_plan_number',
              location: 'after',
              options:{
                icon: 'link',
                stylingMode: 'text',
                disabled: false,
                onClick: methods.redirectToExcutionPlan
              },
            },
            ],
          }
        }else{
          return {
            ...methods.generateItemButtonOption(
              'search',
              methods.createFindPopupFn('excution_plan', '실행계획 조회', {name : 'fk_project_management_id', op: 'is_null'})
            ),
            ...vars.formState,
          }
        }
      },
      async redirectToBusiness(){
        if(!vars.formData.id){
          return;
        }
        if(!vars.formData.fk_business_id){
          await alert('영업번호가 존재하지 않습니다', '영업으로 이동');
          return;
        }
        const response = await projectBusiness.load({
          filter: [
            ['id', '=', vars.formData.fk_business_id]
          ]
        });
        if(response.data.length > 0){
          router.replace({path: `/project/business/${response.data[0].id}`});
        }else{
          await alert('영업번호가 존재하지 않습니다', '영업으로 이동');
          return;
        }
      },
      async redirectToExcutionPlan(){
        if(!vars.formData.id){
          return;
        }
        if(!vars.formData.fk_excution_plan_id){
          let isSelect = await confirm('실행계획번호가 존재하지 않습니다. 실행계획을 등록 하시겠습니까?', '실행계획 등록');
          if(!isSelect) return;
          router.replace({path: `/project/excution-plan/project/${vars.formData.id}`});
          return;
        }
        const response = await projectExcutionPlan.load({
          filter: [
            ['id', '=', vars.formData.fk_excution_plan_id]
          ]
        });
        if(response.data.length > 0){
          router.replace({path: `/project/excution-plan/${response.data[0].id}`});
        }else{
          await alert('실행계획번호가 존재하지 않습니다', '실행계획으로 이동');
          return;
        }
      },
      async exportToVisible() {
          if (!vars.grid.items) return;

          const dataSource = vars.grid.items.getDataSource();
          if (!dataSource._isLoaded) {
              await dataSource.load();
          }
          const items = dataSource._items;
          const shipmentFilter = items.filter(v => v.fk_shipment_order_id != '' && v.fk_shipment_order_id != null)
          const workFilter = items.filter(v => v.fk_work_order_id != '' && v.fk_work_order_id != null)
        
          vars.disabled.exportToShipmentOrder = shipmentFilter.length == items.length ? false : true;
          vars.disabled.exportToWorkOrder = workFilter.length == items.length ? false : true;

      },

      async exportToShipmentOrder(){
        if(!vars.formData.id) return;
        const rows = vars.grid.items.getVisibleRows()
    
        const itemIdList = rows.filter(row => row.data.not_ordered).map(row => row.data.id);
        if(!itemIdList.length){
          alert('품목이 없습니다', '수주로 내보내기');
          return;
        }
        const params = {
          project_management_id: vars.formData.id,
          department: authService.getDepartmentName() ? authService.getDepartmentName() : '',
          manager: authService.getUserName(),
          company_id: authService.getCompanyId(),
          project_item_ids: itemIdList,
          order_company: vars.formData.order_company,
          warehouse_code: vars.warehouse.wh_code,
        };

        try{
          const api = new ApiService('/api/mes/v1/project/registration-to-shipment-order')
          await api.post('', params)
          await alert('수주로 내보내기가 완료되었습니다', '수주로 내보내기');
        }catch(ex){
          if (ex.response.status == 608) {
            await alert('미수주 수량이 없습니다', '수주로 내보내기');
          } else {
            await alert('수주로 내보내기가 실패했습니다', '수주로 내보내기');
          }
        }finally{
          vars.grid.items.refresh();
          methods.exportToVisible();
        }
      },
      async exportToWorkOrder(){
        if(!vars.formData.id) return;
        const rows = vars.grid.items.getVisibleRows()

        const itemIdList = rows.filter(row => !row.data.work_order_number).map(row => row.data.id);

        if(!itemIdList.length){
          alert('품목이 없습니다', '작지로 내보내기');
          return;
        }
        const params = {
          project_management_id: vars.formData.id,
          department: authService.getDepartmentName() ? authService.getDepartmentName() : '',
          manager: authService.getUserName(),
          company_id: authService.getCompanyId(),
          project_item_ids: itemIdList,
          contract_company: vars.formData.contract_company,
          warehouse_code: vars.warehouse.wh_code,
        };

        
        try{
          const api = new ApiService('/api/mes/v1/project/registration-to-work-order')
          await api.post('', params)
          await alert('작지로 내보내기가 완료되었습니다', '작지로 내보내기');

        }catch(ex){
          if (ex.response.status == 608) {
            await alert('미작지 수량이 없습니다', '작지로 내보내기');
          } else {
            await alert('작지로 내보내기가 실패했습니다', '작지로 내보내기');
          }
        }finally{
          vars.grid.items.refresh();
          methods.exportToVisible();
        }
        
        
      },
      onReportShow(reportType){
        if (!vars.formData.id) return;
        console.log('onReportShow', vars.dlg.report.measurementDCompletion.show);
        vars.dlg.report[reportType].show = true;
      },
      onReportHiding(reportType){
        vars.dlg.report[reportType].show = false;
      },
      progressPaymentReport() {
        if (!vars.formData.id) {
          alert('프로젝트를 선택해 주세요.', '프로젝트 미선택');
          return;
        }
        let isVisibleRows = vars.grid['projectCostLog'].getVisibleRows().length > 0 ? true : false;
        if(!isVisibleRows){
          alert('기성관리 내역이 없습니다', '프로젝트 미선택');
          return;
        }
        isVisibleRows = vars.grid['projectOutCostLog'].getVisibleRows().length > 0 ? true : false;
        if(!isVisibleRows){
          alert('외주기성관리 내역이 없습니다', '프로젝트 미선택');
          return;
        }
        vars.dlg.report.progressPayment.show = true;
      },
      async onInvoiceCostLog(cellData) {
        const rowData = cellData.data;

        if (!rowData.id) {
          alert('저장 후 세금계산서를 발행할 수 있습니다.', '세금계산서 발행');
          return;
        }        
        if (rowData.invoice_status === '발행완료') {
          alert('이미 발행된 세금계산서입니다.', '세금계산서 발행');
          return;
        }
        if (!rowData.curr_cost || rowData.curr_cost <= 0) {
          alert('당월기성 금액이 없습니다.', '세금계산서 발행');
          return;
        }
        const isConfirm = await confirm(
          `당월기성 ${numeral(rowData.curr_cost).format('0,0')}원에 대한 세금계산서를 발행하시겠습니까?`,
          '세금계산서 발행'
        );
        if (!isConfirm) return;
        
        const queryParams = new URLSearchParams({
          from: 'project-cost',
          projectId: vars.formData.id,
          projectNumber: vars.formData.project_number || '',
          projectName: vars.formData.project_name || '',
          clientCompany: vars.formData.order_company || '',
          amount: rowData.curr_cost,
          costLogId: rowData.id,
          costDate: rowData.cost_date ? moment(rowData.cost_date).format('YYYY-MM-DD') : ''
        });
        
        router.push({
          path: '/shipment/sales-statement',
          query: Object.fromEntries(queryParams)
        });
      },
      /* 발행완료 클릭 시 → 해당 매출계산서 페이지로 이동*/
      onNavigateToSalesStatement(cellData) {
        const rowData = cellData.data;
        if (!rowData.fk_sales_id) {
          alert('연결된 매출계산서 정보를 찾을 수 없습니다.', '매출계산서 이동');
          return;
        }

        router.push({
          path: `/shipment/sales-statement/${rowData.fk_sales_id}`
        });
      },
    };

    watch(
      () => props.id,
      () => methods.initById(props.id)
    );

    // 아래 watch 추가 ↓
    watch(
      () => route.query.refresh,
      (newVal) => {
        if (newVal && vars.formData.id) {
          methods.gridProjectCostLogRefresh(vars.formData.id);
        }
      }
    );

    return {
      vars,
      methods,
      baseItem,
      baseClient,
    };
  },
};
</script>

<style lang="scss">

.report {
    font-family: '맑은 고딕', 'Malgun Gothic', sans-serif; 
    -webkit-print-color-adjust: exact; 
    width: 210mm; 
    height: 297mm; 
    box-sizing: border-box; 
    padding: 8px;
    font-size: 15px;
    border: 1px dotted #9c9c9c;
    table {width: 100%; border-collapse: collapse; table-layout: fixed;}
    table.fixed { table-layout: fixed; }

    display: flex;
    flex-direction: column;

    .content-header {
        margin-top: 30px;
        margin-bottom: 25px;
    }
    .content-body {
        width: 85%;
        margin: 0 auto;
        .content-body-container {
            width: 100%;
            .body-1 {
                width: 100%;
                padding-bottom: 10px;
                border-bottom: 1px solid #000;

                .underline {
                    width: 100%;
                    height: 17px;
                    background-color: #bbd1f8;
             
                }
            }
            .body-2 {
                padding-top: 10px;          
            }
        }
    }    
    .content-footer {
        
        margin-top: auto;
        margin-bottom: 50px;
        .underline {
            width: 85%;
            height: 17px;
            background-color: #ebebeb;
        
        }

    }
}

.report-style-A-content-box {
  display: flex;
  gap: 10px;
  .report-style-A-content-box-title {
    width: 60px;
    display: flex;
    justify-content: space-between;
    flex-shrink: 0;
  }
  .report-style-A-content-box-content {
    flex: 1;
    min-width: 0;
  }
  .width-65 {
    width: 65px;
  }
  .width-75 {
    width: 75px;
  }
  .width-78 {
    width: 78px;
  }
  .width-120 {
    width: 120px;
  }

}
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
.completion-button {
  .dx-button-content {
    padding: 7px;
  }
}
.invoice-complete {
  color: #4caf50;
  font-weight: bold;
  text-align: center;
  padding: 4px 8px;
  background-color: #e8f5e9;
  border-radius: 4px;
}

.invoice-complete--link {
  cursor: pointer;
  text-decoration: underline;
  transition: opacity 0.2s;

  &:hover {
    opacity: 0.75;
    background-color: #c8e6c9;
  }
}
</style>
