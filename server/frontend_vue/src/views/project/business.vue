<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">영업건등록</div>
            </dx-item>
            <dx-item location="after">
              <div class="barobill-state" v-if="vars.dataSource.approval">{{ vars.dataSource.approval }}</div>
            </dx-item>
            <dx-item location="after" locate-in-menu="auto" widget="dxButton" :options="{text: '신규', type: 'add', icon: 'add', disabled: vars.disabled.new, onClick: methods.newItem}"/>
            <dx-item location="after" locate-in-menu="auto" widget="dxButton" :options="{text: '수정', type: 'rename', icon: 'rename', disabled: vars.disabled.edit, onClick: methods.editItem}"/>
            <dx-item location="after" locate-in-menu="auto" widget="dxButton" :options="{text: '삭제', type: 'remove', icon: 'remove', disabled: vars.disabled.delete, onClick: methods.deleteItem}" />
            <dx-item location="after" locate-in-menu="auto" widget="dxButton" :options="{text: '저장', type: 'save', icon: 'save', disabled: vars.disabled.save, onClick: methods.saveItem}" />
            <dx-item location="after" locate-in-menu="auto" widget="dxButton" :options="{text: '출력', type: 'print', icon: 'print', disabled: vars.disabled.printDocument, onClick: methods.printDocument}" />
            <dx-item location="after" locate-in-menu="auto" widget="dxButton" :options="{text: '엑셀업로드', icon: 'upload', onClick: methods.excelUpload}" />
          </dx-toolbar>
        </div>
        <dx-form :form-data="vars.formData">
          <dx-group-item :col-count="4">
            <dx-group-item>
                <dx-simple-item
                  data-field="business_number"
                  :editor-options="{
                    placeholder: '(자동 or 직접입력)',
                    ...generateItemButtonOption('search', methods.createFindPopupFn('business', '영업조회')),
                  }"
                >
                  <dx-label text="영업 건 번호" :show-colon="false" />
                </dx-simple-item>

                <dx-simple-item data-field="business_date" editor-type="dxDateBox" :editor-options="{ 
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss', 
                  ...vars.formState
                }">
                  <dx-label text="영업일자" :show-colon="false"/>
                </dx-simple-item>

                <dx-simple-item data-field="business_name" :editor-options="{
                  onValueChanged: methods.onValueChanged, 
                  ...vars.formState }">
                  <dx-label text="영업 건 명" :show-colon="false" />
                  <dx-required-rule message="영업명을 입력하세요" />
                </dx-simple-item>
                <dx-simple-item data-field="client_company"
                :editor-options="{
                  onEnterKey: methods.createFindPopupFn('client', '업체조회', {
                    name: vars.formData.client_company,
                  }),
                  ...generateItemButtonOption('search', methods.createFindPopupFn('client', '업체조회')),
                  ...vars.formState,
                }"
              >
                  <dx-label text="계약상대자" :show-colon="false" />
                  <dx-required-rule message="계약상대자를 선택하세요" />
                </dx-simple-item>     
            </dx-group-item>
            <dx-group-item>
                <dx-simple-item data-field="business_department" editor-type="dxSelectBox" :editor-options="{
                    dataSource: vars.dataSource.department,
                    valueExpr: 'department_name',
                    displayExpr: 'department_name',
                    acceptCustomValue: true,
                    onValueChanged: methods.onDepartmentChanged,
                    ...vars.formState,
                  }">
                  <dx-label text="담당부서" :show-colon="false" />
                </dx-simple-item>

                <dx-simple-item data-field="business_manager" editor-type="dxSelectBox" :editor-options="{
                  onValueChanged: methods.onValueChanged,
                  dataSource: vars.dataSource.employee,
                  valueExpr: 'emp_name',
                  displayExpr: 'emp_name',
                  disabled: vars.disabled.business_manager,
                  ...vars.formState,
                }">
                  <dx-label text="당사담당자" :show-colon="false" />
                </dx-simple-item>

                <dx-simple-item data-field="business_amount" editor-type="dxNumberBox" :editor-options="{
                  format: '₩,##0',
                  onValueChanged: methods.onBusinessAmountChanged,
                  ...vars.formState
                }">
                  <dx-label text="영업금액" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item data-field="contract_company"
                :editor-options="{
                  ...generateItemButtonOption(
                    'search',
                    methods.createFindPopupFn('contract_company', '수요기관')
                  ),
                  ...vars.formState,
                }"
              >
                <dx-label text="수요기관" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
                <dx-simple-item data-field="business_type" editor-type="dxSelectBox" :editor-options="{
                  dataSource: vars.dataSource.business_type,
                  valueExpr: 'code_name',
                  displayExpr: 'code_name',
                  ...vars.formState,
                }">
                  <dx-label text="영업구분" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item data-field="classification" :editor-options="{
                  ...vars.formState,
                }">
                  <dx-label text="종목" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item data-field="location" :editor-options="{
                  ...vars.formState,
                  buttons: [
                    {
                      name: 'icon',
                      location: 'after',
                      options: {
                        stylingMode: 'text',
                        icon: 'search',
                        onClick: methods.findAddressPopup,
                      }
                    }
                  ]
                }">
                  <dx-label text="현장지역" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item data-field="completion_date" editor-type="dxDateBox" :editor-options="{
                dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                ...vars.formState
              }">
                <dx-label text="준공예정일" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
                <dx-group-item :col-count="2">
                  <dx-simple-item data-field="business_progress" editor-type="dxSelectBox" :editor-options="{
                    dataSource: vars.dataSource.business_progress,
                    valueExpr: 'code_name',
                    displayExpr: 'code_name',
                    ...vars.formState,
                  }">
                    <dx-label text="진행현황" :show-colon="false" />
                  </dx-simple-item>
                  <dx-simple-item data-field="contract_type" editor-type="dxSelectBox" :editor-options="{
                    dataSource: vars.dataSource.contract_type,
                    valueExpr: 'code_name',
                    displayExpr: 'code_name',
                    ...vars.formState,
                  }">
                  <dx-label text="계약유형" :show-colon="false" />
                </dx-simple-item>
                </dx-group-item>
            
                <dx-simple-item data-field="project.project_number" :editor-options="methods.projectNumberOptions()">
                  <dx-label text="연결 프로젝트" :show-colon="false" />
                </dx-simple-item>

                <dx-group-item :col-count="2" css-class="form-group">
                  <dx-simple-item data-field="gross_profit" editor-type="dxNumberBox" :editor-options="{
                  readOnly: true,
                  format: '₩,##0',
                  }">
                  <dx-label text="매출총이익" :show-colon="false" />
                  </dx-simple-item>
                  <dx-simple-item data-field="gross_profit_rate" editor-type="dxNumberBox" :editor-options="{
                    readOnly: true,
                    format: '#0.00%'
                    }">
                    <dx-label text="GM" :show-colon="false" />
                  </dx-simple-item>
                  <dx-simple-item data-field="operating_profit" editor-type="dxNumberBox" :editor-options="{
                      readOnly: true,
                      format: '₩,##0',
                      }">
                      <dx-label text="순수익" :show-colon="false" />
                    </dx-simple-item>
                  
                    <dx-simple-item data-field="operating_profit_rate" editor-type="dxNumberBox" :editor-options="{
                    readOnly: true,
                    format: '#0.00%'
                    }">
                    <dx-label text="OP" :show-colon="false" />
                  </dx-simple-item>
              </dx-group-item>
            </dx-group-item>
          </dx-group-item>
        </dx-form>
      </div>
      <!-- 시작 -->
      <div class="dx-card responsive-paddings mt-1">
        <dx-tab-panel
        v-model:selected-index="vars.tab.index"
        :swipe-enabled="false"
        :animation-enabled="false"
        :defer-rendering="false">
          <dx-item title="고객정보관리">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 430px)"
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
          <!-- 끝 -->
          <dx-item title="고객이력관리">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 430px)"
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
                  :data-source="vars.dataSource.customer_history"
                  :on-initialized="evt => methods.onGridInitialized(evt, 'customer_history')"
                  @saving="(e) => methods.onSavingItem(e, 'customer_history')"
                  @data-error-occurred="methods.onDataError"
                  @focused-cell-changed="evt => methods.onFocusedCellChanged(evt, 'customer_history')"
                  @init-new-row="evt => methods.initNewRow(evt, 'customer_history')"
                  >
                  <dx-grid-toolbar>
                      <dx-grid-item template="addCustomerHistoryRowButton" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item template="customerHistorySaveButton" location="after" :visible="false" />
                      <dx-grid-item name="revertButton" location="after" />
                  </dx-grid-toolbar>
                  <template #addCustomerHistoryRowButton>
                      <dx-button text="고객이력 추가" icon="add" @click="methods.addItemRowButton('customer_history')" />
                  </template>
                  <template #customerHistorySaveButton>
                      <dx-button text="저장" icon="save" @click="methods.itemSaveButton('customer_history')" />
                  </template>
                  <dx-column type="buttons" :visible="!vars.formState.readOnly"/>
                  <dx-column caption="일자" data-field="history_date" data-type="date" format="yyyy-MM-dd" />
                  <dx-column caption="담당자" data-field="manager">
                    <!-- <dx-lookup value-expr="emp_name" display-expr="emp_name" :data-source="vars.dataSource.employee_list" /> -->
                  </dx-column>
                  <dx-column caption="접촉방법" data-field="contact_method" />
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
          <dx-item title="진행현황">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 430px)"
                  date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                  column-resizing-mode="widget"
                  :show-borders="true"
                  :remote-operations="false"
                  :column-auto-width="true"
                  :focused-row-enabled="true"
                  :allow-column-resizing="true"
                  :allow-column-reordering="true"
                  :row-alternation-enabled="true"
                  :select-text-on-edit-start="true"
                  :data-source="vars.dataSource.progress"
                  :on-initialized="evt => methods.onGridInitialized(evt, 'progress')"
                  @saving="(e) => methods.onSavingItem(e, 'progress')"
                  @data-error-occurred="methods.onDataError"
                  @focused-cell-changed="evt => methods.onFocusedCellChanged(evt, 'progress')"
                  @init-new-row="evt => methods.initNewRow(evt, 'progress')"
                >
                <dx-grid-toolbar>
                    <dx-grid-item template="addProgressRowButton" location="after" :visible="!vars.formState.readOnly" />
                    <dx-grid-item template="progressSaveButton" location="after" :visible="false" />
                    <dx-grid-item name="revertButton" location="after" />
                </dx-grid-toolbar>
                <template #addProgressRowButton>
                    <dx-button text="진행현황 추가" icon="add" @click="methods.addItemRowButton('progress')" />
                </template>
                <template #progressSaveButton>
                    <dx-button text="저장" icon="save" @click="methods.itemSaveButton('progress')" />
                </template>
                <dx-column type="buttons" :visible="!vars.formState.readOnly"/>
                <dx-column caption="진행일자" data-field="progress_date" data-type="date" format="yyyy-MM-dd" />
                <dx-column caption="업체담당자" data-field="client_manager" />
                <dx-column caption="진행방법" data-field="progress_method" data-type="string">
                  <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.dataSource.progress_method" />
                </dx-column>
                <dx-column caption="진행방법" data-field="note" data-type="string" />

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
          <dx-item title="견적현황">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 430px)"
                  date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                  column-resizing-mode="widget"
                  :show-borders="true"
                  :remote-operations="false"
                  :column-auto-width="true"
                  :focused-row-enabled="true"
                  :allow-column-resizing="true"
                  :allow-column-reordering="true"
                  :row-alternation-enabled="true"
                  :select-text-on-edit-start="true"
                  :data-source="vars.dataSource.quote"
                  @saving="(e) => methods.onSavingItem(e, 'quote')"
                  @data-error-occurred="methods.onDataError"
                  @focused-cell-changed="evt => methods.onFocusedCellChanged(evt, 'quote')"
                  @init-new-row="evt => methods.initNewRow(evt, 'quote')"
                  :on-initialized="evt => methods.onGridInitialized(evt, 'quote')"
                  >
                    <dx-grid-toolbar>
                      <dx-grid-item template="addQuoteRowButton" location="after" :visible="!vars.formState.readOnly" />  
                      <dx-grid-item template="quoteSaveButton" location="after" :visible="false" />
                      <dx-grid-item name="revertButton" location="after" />
                    </dx-grid-toolbar>
                    <template #addQuoteRowButton>
                      <dx-button text="견적현황 추가" icon="add" @click="methods.addItemRowButton('quote')" />
                    </template>
                    <template #quoteSaveButton>
                      <dx-button text="저장" icon="save" @click="methods.itemSaveButton('quote')" />
                    </template>
                    <dx-column type="buttons" :visible="!vars.formState.readOnly"/>

                    <dx-column caption="견적일자" data-field="quote_date" data-type="date" format="yyyy-MM-dd" :allow-editing="true" />
                    <dx-column caption="담당자" data-field="quote_manager" :allow-editing="true" />
                    <dx-column caption="참고사항" data-field="note" :allow-editing="true" />
                    <dx-column caption="첨부파일" data-field="file_name" cell-template="download" edit-cell-template="upload" />
                    <dx-scrolling mode="standard" />
                    <dx-editing mode="batch"
                      :use-icons="true"
                      :allow-adding="!vars.formState.readOnly"
                      :allow-updating="!vars.formState.readOnly"
                      :allow-deleting="!vars.formState.readOnly"
                    />
                    <template #download="{data}">
                    <a :href="`/api/mes/v1/file-manager/download/${data.data['file_path']}/${data.data['file_name']}`" download>{{data.data[data.column.dataField]}}</a>
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
          <dx-item title="참고사항">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 430px)"
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
                  :data-source="vars.dataSource.note"
                  :on-initialized="evt => methods.onGridInitialized(evt, 'note')"
                  @saving="(e) => methods.onSavingItem(e, 'note')"
                  @data-error-occurred="methods.onDataError"
                  @focused-cell-changed="evt => methods.onFocusedCellChanged(evt, 'note')"
                  @init-new-row="evt => methods.initNewRow(evt, 'note')"
                  >
                  <dx-grid-toolbar>
                      <dx-grid-item template="addNoteRowButton" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item template="noteSaveButton" location="after" :visible="false" />
                      <dx-grid-item name="revertButton" location="after" />
                  </dx-grid-toolbar>
                  <template #addNoteRowButton>
                      <dx-button text="참고사항 추가" icon="add" @click="methods.addItemRowButton('note')" />
                  </template>
                  <template #noteSaveButton>
                      <dx-button text="저장" icon="save" @click="methods.itemSaveButton('note')" />
                  </template>
                  <dx-column type="buttons" :visible="!vars.formState.readOnly"/>
                  <dx-column caption="등록자" data-field="note_manager" />
                  <dx-column caption="등록일자" data-field="note_date" data-type="date" format="yyyy-MM-dd" />
                  <dx-column caption="참고내용" data-field="note_detail" />
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
          <dx-item title="원가검토">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 430px)"
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
                  :data-source="vars.dataSource.cost"
                  :on-initialized="evt => methods.onGridInitialized(evt, 'cost')"
                  @saving="(e) => methods.onSavingItem(e, 'cost')"
                  @data-error-occurred="methods.onDataError"
                  @focused-cell-changed="evt => methods.onFocusedCellChanged(evt, 'cost')"
                  @init-new-row="evt => methods.initNewRow(evt, 'cost')"
                  @cell-dbl-click="methods.itemPopupClick"

                  >
          
                  <dx-grid-toolbar>
        
                      <dx-grid-item template="orderReportButton" location="after" :visible="vars.formState.readOnly" />
                      <dx-grid-item template="costExportButton" location="after" />
                      <dx-grid-item template="costRate" location="after" />
                      <dx-grid-item template="addCostRowButton" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item template="addPrevBusinessButton" location="after" :visible="!vars.formState.readOnly" />
                      <dx-grid-item template="costSaveButton" location="after" :visible="false" />
                      <dx-grid-item name="revertButton" location="after" />
                  </dx-grid-toolbar>
                  <template #addPrevBusinessButton>
                    <dx-button
                      text="이전 프로젝트에서 가져오기"
                      @click="methods.showAddPrevBusinessPopup"
                      />
                  </template>
                  <template #orderReportButton>
                    <dx-button
                      text="수주사항보고서"
                      @click="methods.orderReportButton"
                      />
                  </template>
                  <template #costExportButton>
                    <dx-button
                      icon="xlsxfile"
                      hint="엑셀로 내보내기"
                      @click="methods.exportCostToExcel"
                      type="default"
                      styling-mode="text"
                    />
                  </template>

                  <template #addCostRowButton>
                      <dx-button text="품목찾기" icon="add" @click="methods.showItemAddPopup" />
                  </template>
                  <template #costSaveButton>
                      <dx-button text="저장" icon="save" @click="methods.itemSaveButton('cost')" />
                  </template>
                  <template #costRate>
                      <dx-number-box 
                        :value="vars.formData.rate" mode="number" label="요율" format="percent" width="80px" :on-value-changed="methods.onRateChange" :read-only="vars.formState.readOnly" :element-attr="{class : 'number-box'}"/>
                  </template>
                  <dx-column type="buttons" :visible="!vars.formState.readOnly"/>
                  <dx-column caption="순서" data-field="item_order" />
                  <dx-column caption="품목코드" data-field="item_code" :allow-editing="false" />
                  <dx-column caption="품명" data-field="item.item_name" :allow-editing="false" />
                  <dx-column caption="규격" data-field="item.item_standard" :allow-editing="false" />
                  <dx-column caption="단위" data-field="item.unit" :allow-editing="false" />
                  <dx-column caption="견적수량" data-field="quote_quantity"  data-type="number" format=",###.#" :set-cell-value="methods.setQuoteQuantity" />
                  <dx-column caption="견적단가" data-field="quote_unit_price"  data-type="number" format="currency" :visible="false" :set-cell-value="methods.setQuoteUnitPrice" />
                  <dx-column caption="견적금액" data-field="quote_supply_price" data-type="number" format="currency" :visible="false" :allow-editing="false" />
                  <dx-column caption="구매단가" data-field="purchase_unit_price" data-type="number" format="currency" :set-cell-value="methods.setPurchaseUnitPrice" />
                  <dx-column caption="구매금액" data-field="purchase_supply_price" data-type="number" format="currency" :allow-editing="false" />
                  <dx-column caption="비고" data-field="etc" :allow-editing="true" :width="400" />
                  <dx-column caption="DC Rate" data-field="dc_rate" data-type="number" format="percent" :visible="false" />
                  <dx-summary :recalculate-while-editing="true" :calculate-custom-summary="methods.calculateCustomSummary">
                    <dx-total-item column="quote_supply_price" summary-type="sum" value-format="₩,##0" display-format="견적금액합계: {0}" />
                    <dx-total-item column="purchase_supply_price" summary-type="sum" value-format="₩,##0" display-format="구매금액합계: {0}" />
                    <dx-total-item name="purchase_supply_price" summary-type="custom" />
                  </dx-summary>
                  <dx-paging :enabled="false" />
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
          <dx-item title="영업기초자료">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 430px)"
                  date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                  column-resizing-mode="widget"
                  :show-borders="true"
                  :remote-operations="false"
                  :column-auto-width="true"
                  :focused-row-enabled="true"
                  :allow-column-resizing="true"
                  :allow-column-reordering="true"
                  :row-alternation-enabled="true"
                  :select-text-on-edit-start="true"
                  :data-source="vars.dataSource.basic"
                  @saving="(e) => methods.onSavingItem(e, 'basic')"
                  @data-error-occurred="methods.onDataError"
                  @focused-cell-changed="evt => methods.onFocusedCellChanged(evt, 'basic')"
                  @init-new-row="evt => methods.initNewRow(evt, 'basic')"
                  :on-initialized="evt => methods.onGridInitialized(evt, 'basic')"
                  >
                    <dx-grid-toolbar>
                      <dx-grid-item template="addBasicRowButton" location="after" :visible="!vars.formState.readOnly" />  
                      <dx-grid-item template="basicSaveButton" location="after" :visible="false" />
                      <dx-grid-item name="revertButton" location="after" />
                    </dx-grid-toolbar>
                    <template #addBasicRowButton>
                      <dx-button text="영업기초자료 추가" icon="add" @click="methods.addItemRowButton('basic')" />
                    </template>
                    <template #basicSaveButton>
                      <dx-button text="저장" icon="save" @click="methods.itemSaveButton('basic')" />
                    </template>
                    <dx-column type="buttons" :visible="!vars.formState.readOnly"/>

                    <dx-column caption="일자" data-field="basic_date" data-type="date" format="yyyy-MM-dd" :allow-editing="true" />
                    <dx-column caption="담당자" data-field="basic_manager" :allow-editing="true" />
                    <dx-column caption="참고사항" data-field="note" :allow-editing="true" />
                    <dx-column caption="첨부파일" data-field="file_name" cell-template="download" edit-cell-template="upload" />
                    <dx-scrolling mode="standard" />
                    <dx-editing mode="batch"
                      :use-icons="true"
                      :allow-adding="!vars.formState.readOnly"
                      :allow-updating="!vars.formState.readOnly"
                      :allow-deleting="!vars.formState.readOnly"
                    />
                    <template #download="{data}">
                    <a :href="`/api/mes/v1/file-manager/download/${data.data['file_path']}/${data.data['file_name']}`" download>{{data.data[data.column.dataField]}}</a>
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
        </dx-tab-panel>
      <popup-item-detail
        v-model:visible="vars.itemDetail.visible"
        :item-id="vars.itemDetail.id"
      />
      </div>
    </div>

    <dx-popup
      content-template="popup-content"
      v-model:visible="vars.dlg.finder.show"
      :width="vars.dlg.finder.key === 'location' ? '15%' : '70%'"
      :height="500"
      :key="vars.dlg.finder.key"
      :title="vars.dlg.finder.title"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'multiuse-popup')"
    >
      <template #popup-content>
        <data-grid-business v-if="vars.dlg.finder.key === 'business'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-client v-else-if="vars.dlg.finder.key === 'contract_company'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-client v-else-if="vars.dlg.finder.key === 'client'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-grid-project v-else-if="vars.dlg.finder.key === 'project'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <data-location-select v-else-if="vars.dlg.finder.key === 'location'" :dataSource="vars.dataSource.location" @change="methods.finderReturnHandler" />
      </template>
    </dx-popup>
    <dx-popup
          title="주소찾기"
          content-template="popup-content"
          v-model:visible="vars.findAddress.popup"
          :width="680"
          :height="500"
          :resize-enabled="true"
          :close-on-outside-click="true"
        >
          <template #popup-content>
            <div>
              <div style="margin-bottom: 10px">
                <dx-text-box
                  v-model="vars.findAddress.keyword"
                  :buttons="vars.findAddress.textBoxOptions"
                  @enter-key="methods.findAddressSubmit"
                />
              </div>
              <dx-data-grid
                :height="340"
                :show-borders="true"
                :column-auto-width="true"
                :remote-operations="true"
                :allow-column-resizing="true"
                :allow-column-reordering="true"
                :data-source="vars.findAddress.store"
                @row-click="methods.findAddressSelect"
                @initialized="evt => methods.onGridInitialized(evt, 'find-address')"
              >
                <dx-column data-field="road" caption="도로명주소" />
                <dx-column data-field="jibun" caption="지번주소" />
                <dx-column data-field="zip" caption="우편번호" />
                <dx-paging :page-size="20" />
              </dx-data-grid>
            </div>
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
      @initialized="evt => methods.onGridInitialized(evt, 'add-base-item-popup')"
    >
      <template #popup-content>
        <popup-item
          :toggle="vars.dlg.addItem.show"
          @baseItemChange="methods.addSelectedRows"
        />
      </template>
    </dx-popup>

    <dx-popup
      v-model:visible="vars.dlg.prevBusiness.show"
      content-template="popup-content"
      title="이전 프로젝트에서 가져오기"
      :close-on-outside-click="true"
      width="70%"
      :height="500"
      :resize-enabled="true"
    >
      <template #popup-content>
        <data-business @change="methods.prevBusinessChange" />
      </template>
    </dx-popup>
    
    <dx-popup
      v-model:visible="vars.dlg.businessCost.show"
      content-template="popup-content"
      title="원가검토"
      :close-on-outside-click="true"
      width="70%"
      :height="500"
      :resize-enabled="true"
    >
      <template #popup-content>
        <data-business-cost :business_id="vars.dlg.businessCost.fk_business_id" @change="methods.addPrevBusinessCost" />
      </template>
    </dx-popup>
    <dx-popup
      v-model:visible="vars.dlg.orderReport.show"
      content-template="popup-content"
      title="수주사항보고서"
      :close-on-outside-click="true"
      width="1400px"
      height="800px"
      :resize-enabled="true"
      :scroll-by-content="true"
    >
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ 
          text: '상신요청', 
          icon: 'export',
          onClick: methods.sendRequest,
          type: 'normal',
        }"
      />
      <template #popup-content>
        <dx-scroll-view width="100%" height="100%">
          <data-order-report :fk_business_id="vars.dlg.orderReport.fk_business_id" :fk_request_emp_id="vars.dlg.orderReport.fk_request_emp_id" />
        </dx-scroll-view>
      </template>
    </dx-popup>
    <input
      hidden
      type="file"
      :ref="vars.excelRef"
      accept=".xlsx,.xls"
      @change="methods.excelFileChange"
    />
  </div>
</template>
<script>
import moment from 'moment';
import { useRouter } from 'vue-router';
import numeral from 'numeral';
import { ref, reactive, watch, onMounted, nextTick, computed } from 'vue'
import { confirm, alert } from 'devextreme/ui/dialog';
import { DxScrollView } from 'devextreme-vue/scroll-view';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxNumberBox } from 'devextreme-vue/number-box';
import { DxTextBox, DxButton as DxTextBoxButton } from 'devextreme-vue/text-box';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxButton } from 'devextreme-vue/button';
import { DxTabPanel } from 'devextreme-vue/tab-panel';
import { DxDataGrid, DxToolbar as DxGridToolbar, DxEditing, DxColumn, DxLookup, DxItem as DxGridItem, DxRequiredRule as DxGridRequiredRule, DxScrolling, DxSelection, DxPaging, DxSummary, DxTotalItem, } from 'devextreme-vue/data-grid';
import { DxForm, DxGroupItem, DxSimpleItem, DxLabel, DxRequiredRule } from 'devextreme-vue/form';
import { beforeExitConfirm, currentDateTime, generateItemButtonOption } from '../../utils/util';
import authService from '../../auth';
import stateStore from '@/utils/state-store';
import { loadDepartment, loadEmployee, loadClientManager } from '../../utils/data-loader';
import { notifyInfo, notifyError } from '../../utils/notify'
import { projectBusiness, getProjectBusinessNote, getProjectBusinessProgress, projectRegistration, getProjectCustomerInformation, getProjectCustomerHistory, getProjectBusinessQuote, getProjectBusinessCost, getProjectBusinessBasic, projectBusinessCost } from '../../data-source/project'
import { setupSgaExpense } from '../../data-source/setup';
import { getShipmentQuote } from '../../data-source/shipment';
import DataGridClient from '@/components/base/data-client.vue';
import DataGridBusiness from '@/components/project/data-business.vue';
import DataGridClientManager from '@/components/base/data-client-manager.vue';
import { baseClient, baseCodeLoader, baseEmployee } from '../../data-source/base';
import DataGridProject from '../../components/project/data-project.vue';
import DataLocationSelect from '../../components/base/data-location-select.vue';
import ApiService from '../../utils/api-service';
import FindAddressStore from '../../data-source/find-address';
import PopupItem from '../../components/base/popup-item.vue';
import PopupItemDetail from '@/components/base/popup-item-detail';
import ExcelJS from 'exceljs';
import DataBusinessCost from '@/components/project/data-business-cost.vue';
import DataBusiness from '@/components/project/data-business.vue';
import DataOrderReport from '@/components/approval/data-order-report.vue';
import { getApproval, approvalLine, approvalDocumentStatus, approval, approvalLineResult } from '../../data-source/approval';

export default {
  components: {
    DxTabPanel,
    DxLoadPanel, DxToolbar, DxItem, DxButton, DxForm, DxGroupItem, DxPopup, DxToolbarItem, DxSimpleItem, DxLabel, DxRequiredRule,DxScrolling,
    DataGridClient, DataGridBusiness, DataGridProject, DataGridClientManager, DataLocationSelect,
    DxDataGrid, DxGridToolbar, DxEditing, DxColumn, DxLookup, DxGridItem, DxGridRequiredRule, DxSelection, DxTextBox, DxPaging, DxTextBoxButton, PopupItem, DxNumberBox, DxSummary, DxTotalItem,
    PopupItemDetail,
    DataOrderReport,
    DxScrollView,
    DataBusinessCost,
    DataBusiness,
  },
  props: {
  id: [String, Number],
},
setup(props){
  const router = useRouter();

  const vars = {};
  vars.sga_expense_rate = 0;
  vars.excelRef = ref(null);
  vars.init = ref(false);
  vars.loading = ref(false);
  vars.filter = {};
  vars.filter.common = [{ name: 'fk_business_id', op: 'eq', val: props.id || 0}]
  vars.filter.baseItem = { 
    clientId: null,
  };
  vars.tab = reactive({
      index: 0,
    });
  vars.disabled = reactive({
    new: false,
    edit: true,
    delete: true,
    save: true,
    printDocument: true,
    manager: true,
  })
  vars.formState = reactive({ readOnly: true});
  vars.dataSource = reactive({
    location: [],
    employee: [],
    department: [],
    business_type: [],
    business_progress: [],
    business_important: [],
    contract_type: [],
    progress_method: [],
    employee_list: [],
    progress: getProjectBusinessProgress(vars.filter.common),
    quote: getProjectBusinessQuote(vars.filter.common),
    note: getProjectBusinessNote(vars.filter.common),
    customer_information: getProjectCustomerInformation(vars.filter.common),
    customer_history: getProjectCustomerHistory(vars.filter.common),
    cost: getProjectBusinessCost(vars.filter.common),
    basic: getProjectBusinessBasic(vars.filter.common),
    approval: '',
  })
  vars.attchFiles = reactive({})
  vars.focus = reactive({
    progress: null,
    quote: null,
    note: null,
    customer_information: null,
    customer_history: null,
    cost: null,
    basic: null,
  });
  vars.itemDetail = reactive({ visible: false, id: 0 });

  vars.formData = reactive({});
  vars.dlg = {};
  vars.dlg.finder = reactive({title : '', key: null, data: null, show: false});
  vars.dlg.addItem = reactive({ show: false });
  vars.dlg.prevBusiness = reactive({ show: false });
  vars.dlg.orderReport = reactive({ show: false, fk_business_id: 0, fk_request_emp_id: 0 });
  vars.dlg.businessCost = reactive({ show: false, fk_business_id: 0 });
  vars.findAddress = reactive({
    popup: false,
    store: new FindAddressStore(),
    keyword: null,
    textBoxOptions: [
        {
          name: 'icon',
          location: 'after',
          options: {
            stylingMode: 'text',
            icon: 'search',
            onClick: () => {
              methods.findAddressSubmit();
            },
          },
        },
      ],
  })
  vars.grid = {};
  onMounted(async () => {
    await loadDepartment(vars.dataSource);
    await methods.loadSgaExpenseRate();
    await methods.loadBaseCode();
    await methods.initById(props.id);
  })

  const methods = {
    async initById(id){
      await methods.gridItemRefresh(id, 'progress');
      await methods.gridItemRefresh(id, 'quote');
      await methods.gridItemRefresh(id, 'note');
      await methods.gridItemRefresh(id, 'cost');
      await methods.gridItemRefresh(id, 'basic');
      await methods.gridItemRefresh(id, 'customer_information');
      await methods.gridItemRefresh(id, 'customer_history');
      beforeExitConfirm.check(() => !vars.disabled.save);
      if (!id){
        methods.clearFormData();
        methods.disableAllAction();
        return
      }
      await methods.loadBusinessData(id);
      getApproval(vars.filter.common).load().then((response) => {
        if(response.totalCount > 0){
          vars.dataSource.approval = response.data[0]['approval_status'] || '미상신';
        } else {
          vars.dataSource.approval = '미상신';
        }
      }).catch((error) => {
        vars.dataSource.approval = '';
      })
      methods.enableEdit();
      methods.onClientChanged();
    },
    async loadBusinessData(id){
      try{
        const { data } = await projectBusiness.byKey(id);
        Object.assign(vars.formData, data);
      }
      catch(e){
        if(e.response.status === 404) {
          return methods.redirect();
        }
      }
    },
    async loadSgaExpenseRate(){
      const { data } = await setupSgaExpense.load();
      vars.sga_expense_rate = data[0]?.rate || 0;
    },
    newItem(){
      methods.gridRefreshAll();
      if(vars.formData.id){
        methods.clearFormData();
        methods.redirect();
      }
      setTimeout(() =>{
        methods.clearFormData();
        vars.formData.business_date = currentDateTime();
        vars.formData.completion_date = currentDateTime();
        vars.formData.business_department = authService.getDepartmentName();
        vars.formData.business_manager = authService.getUserName();
        vars.formData.business_type = methods.getFirstItemName(vars.dataSource.business_type);
        vars.formData.business_progress = methods.getFirstItemName(vars.dataSource.business_progress);
        vars.formData.business_important = methods.getFirstItemName(vars.dataSource.business_important);
        vars.formData.contract_type = methods.getFirstItemName(vars.dataSource.contract_type);
        vars.formData.fk_company_id = authService.getCompanyId();
        vars.formState.readOnly = false;
      }, 200);
    },
    gridRefreshAll(id) {

      const grid = ['customer_information', 'customer_history', 'progress', 'quote', 'note', 'cost', 'basic'];
      for (const item of grid) {
        vars.dataSource[item].defaultFilters = methods.setIdToGridFilter(vars.filter['common'], id);
        methods.gridRefresh(vars.grid[item]);
      }
    },
    gridRefresh(grid) {
      if (grid) {
        grid.cancelEditData();
        grid.refresh();
      }
    },
    setIdToGridFilter(filter, id) {
      if (!id) { id = 0; }
      filter[0].val = id;
      return filter;
    },
    async editItem(){
      if(!vars.formData.id) return;
      
      const saveFormData = Object.assign({}, vars.formData);
      vars.formState.readOnly = !vars.formState.readOnly;

      methods.enableSave();
      methods.enableDelete();
      await nextTick();
      Object.assign(vars.formData, saveFormData);
    },
    async deleteItem(){
      const result = await confirm('이 항목을 삭제하시겠습니까?', '삭제확인');
      if(result){
        try{
          if(vars.grid.quote){
            const {data : quote} = await vars.dataSource.quote.load();
            for (const item of quote){
              if(item.fk_business_id == vars.formData.id){
                await vars.dataSource.quote.remove(item.id);
              }
            }
          }
          if(vars.grid.basic){
            const {data : basic} = await vars.dataSource.basic.load();
            for (const item of basic){
              if(item.fk_business_id == vars.formData.id){
                await vars.dataSource.basic.remove(item.id);
              }
            }
          }
          await projectBusiness.remove(vars.formData.id);
          
          beforeExitConfirm.clear();
          await alert('삭제되었습니다.', '삭제 확인');
          methods.redirect();
          vars.formState.readOnly = true;
        }catch(ex){
          if(ex.response.status != 403){
            await alert('연결된 데이터가 있어서 삭제가 안됩니다.', '삭제확인');
          }
        }
      }
    },
    validationSaveDate(){
      if(!vars.formData.business_name){
        notifyError('영업명이 입력되지 않았습니다');
        return false;
      }
      return true;
    },
    async saveItem(){
      if(!methods.validationSaveDate()){
        return;
      }
      let isSelect = await confirm('저장하시겠습니까?', '저장');
      if(!isSelect) return;

      vars.loading.value = true;
      try{
        if(vars.formData.id){
          
          vars.formData.modify_manager = authService.getUserName();
          vars.formData.modify_date = moment().format('YYYY-MM-DD HH:mm:ss');
          const updateDate = Object.assign({}, vars.formData);
          delete updateDate.created;
          delete updateDate.business_number;
          const { data } = await projectBusiness.update(vars.formData.id, updateDate);
          vars.formData.business_number = data.business_number;

          if (vars.grid.progress) {
            await vars.grid.progress.saveEditData();
          }
          if (vars.grid.note) {
            await vars.grid.note.saveEditData();
          }
          if (vars.grid.customer_information) {
            await vars.grid.customer_information.saveEditData();
          }

          if (vars.grid.quote) {
            await vars.grid.quote.saveEditData();
          }

          if (vars.grid.customer_history) {
            await vars.grid.customer_history.saveEditData();
          }

          if (vars.grid.cost) {
            await vars.grid.cost.saveEditData();
          }

          if (vars.grid.basic) {
            await vars.grid.basic.saveEditData();
          }

          vars.formState.readOnly = true;
          notifyInfo('저장되었습니다');
          methods.enableSave();
          methods.enableEdit();
          methods.enableDelete();

        }else{
          let { data } = await projectBusiness.insert(vars.formData);
          vars.formData.id = data.id;

          const progress = vars.grid.progress;
          const note = vars.grid.note;
          const customer_information = vars.grid.customer_information;
          const customer_history = vars.grid.customer_history;
          const quote = vars.grid.quote;
          const cost = vars.grid.cost;
          const basic = vars.grid.basic;
          if (progress && progress.hasEditData()) {
              await progress.saveEditData();
          }
          if (note && note.hasEditData()) {
              await note.saveEditData();
          }
          if (customer_information && customer_information.hasEditData()) {
              await customer_information.saveEditData();
          }
          if (customer_history && customer_history.hasEditData()) {
              await customer_history.saveEditData();
          }
          if (quote && quote.hasEditData()) {
              await quote.saveEditData();
          }
          if (cost && cost.hasEditData()) {
              await cost.saveEditData();
          }
          if (basic && basic.hasEditData()) {
              await basic.saveEditData();
          }
          beforeExitConfirm.clear()
          notifyInfo('저장되었습니다');
          methods.redirect(data.id);
          vars.formState.readOnly = true;
        }
      } catch(ex){
        if (ex.response.status === 602) {
            notifyError('이미 존재하는 작업지시번호 입니다');
          } else {
            console.error(ex);
            notifyError('저장 할 내용이 없습니다');
          }
      }finally{
        vars.loading.value = false;
      }
    },
    async sendRequest(){
  
      try {
        if (!vars.formData.id){
          notifyError('저장된 데이터가 없습니다');
          return;
        }
        if (vars.dataSource.approval !== '미상신'){
          notifyError('이미 상신요청이 완료되었습니다.');
          return;
        }
        vars.loading.value = true;
     
        const { data : approvalLineData } = await approvalLine.load({
          filter: [
            ['fk_request_emp_id', '=', authService.user?.emp_id],
            'and',
            ['fk_document_id', '=', 1]
          ],
          sort: [
            {
              selector: 'line_order',
              desc: false
            }
          ]
        });
        // console.log("approvalLineData : ", approvalLineData);
        if (!approvalLineData.length) {
          alert('결재선이 존재하지 않습니다. 결재선을 지정해주세요.', '결재선 지정');
          return;
        }

        const result = await confirm('상신하시겠습니까?', '상신');
        if (!result) return;
        
        const approvalFormData = {
          fk_business_id: vars.formData.id,
          fk_company_id: authService.getCompanyId(),
          fk_document_id: 1,
          approval_date: currentDateTime(),
          approval_status: '상신완료',
          register: authService.getUserName(),
          title: '',
          content: '',
          etc: '',
          approval_document: {id: 1},
          fk_request_emp_id: authService.user?.emp_id,
        }
        const { data : approvalData } = await approval.insert(approvalFormData);
        // console.log("approvalData : ", approvalData);
        if (approvalData.id) {  
          let count = 0;
          for (const line of approvalLineData) {
            const arFormData = {
              approval_result: '대기중',
              fk_approval_id: approvalData.id,
              fk_approval_line_id: line.id,
              approval_manager: line.approval_employee.emp_name,
              fk_approval_emp_id: line.fk_approval_emp_id,
            }
            if (count == 0) {
              arFormData.active_yn = true;
            }
            count++;
            const { data : approvalLineResultData } = await approvalLineResult.insert(arFormData);
            // console.log("approvalLineResultData : ", approvalLineResultData);
            count++;
          }
          vars.dataSource.approval = '상신완료';
          notifyInfo('상신 요청이 완료 됐습니다.');
        }
        
      }
      catch(ex){
        console.error(ex);
        notifyError('상신 요청 중 오류가 발생했습니다.');
      }
      finally{
        vars.loading.value = false;
      }
     
      
    },
    // 품목코드 클릭 시 품목 상세 정보 popup
    // itemPopupClick({ column, data }) {
    //   if (column.name === 'item_code') {
    //     vars.itemDetail.id = data.id;
    //     vars.itemDetail.visible = true;
    //   }
    // },
    itemPopupClick({ column, data }) {
      if (column.dataField === 'item_code') {
        const itemId = data.item?.id;
        if (!itemId) {
          console.warn('품목 ID가 없습니다:', data);
          return;
        }
        vars.itemDetail.id = itemId;
        vars.itemDetail.visible = true;
      }
    },
    setQuoteQuantity(newData, value, currentRowData){
      let quote_quantity = value;
      const quote_unit_price = currentRowData.quote_unit_price || 0;
      const purchase_unit_price = currentRowData.purchase_unit_price || 0;
      const item_code = currentRowData.item_code || '';
      const business_amount = vars.formData.business_amount || 0;
      

      newData.quote_quantity = value;
      newData.quote_supply_price = quote_quantity * quote_unit_price;
      newData.purchase_supply_price = quote_quantity * purchase_unit_price;

      if (item_code === 'PME-010' && business_amount > 0) {
         newData.purchase_unit_price = business_amount * 0.03;
         newData.purchase_supply_price = quote_quantity * newData.purchase_unit_price;
      }
      if (item_code === 'PME-009' && business_amount > 0) {
        newData.purchase_unit_price = business_amount * 0.02;
        newData.purchase_supply_price = quote_quantity * newData.purchase_unit_price;
      }
      if (item_code === 'PME-012' && business_amount > 0) {
        newData.purchase_unit_price = business_amount * 0.008;
        newData.purchase_supply_price = quote_quantity * newData.purchase_unit_price;
      }
    },
    setQuoteUnitPrice(newData, value, currentRowData){
      const quote_unit_price = value;
      const quote_quantity = currentRowData.quote_quantity || 0;

      newData.quote_unit_price = value;
      newData.quote_supply_price = quote_quantity * quote_unit_price;
    },
    setPurchaseUnitPrice(newData, value, currentRowData){
      const purchase_unit_price = value;
      const quote_quantity = currentRowData.quote_quantity || 0;
      if (vars.formData.rate > 0 && purchase_unit_price > 0){
        newData.quote_unit_price = purchase_unit_price * vars.formData.rate;
        newData.quote_supply_price = quote_quantity * newData.quote_unit_price;
      }
      newData.purchase_unit_price = value;
      newData.purchase_supply_price = quote_quantity * purchase_unit_price;
    },
    calculateCustomSummary(options){
      if (options.name === 'purchase_supply_price'){
        if (options.summaryProcess === 'start'){
          options.totalValue = 0;
        } else if (options.summaryProcess === 'calculate'){
          options.totalValue += options.value.purchase_supply_price;
        } else if (options.summaryProcess === 'finalize'){
          const total_price = options.totalValue; // 수주원가 vars.formData.business_amount// 수주금액

          if(vars.sga_expense_rate > 0 && vars.formData.business_amount > 0 && total_price > 0){
            const gross_profit = vars.formData.business_amount - total_price;
            const gross_profit_rate = gross_profit / vars.formData.business_amount;
            const operating_profit = gross_profit - (total_price * vars.sga_expense_rate);
            const operating_profit_rate = operating_profit / vars.formData.business_amount;
            vars.formData.gross_profit = gross_profit;
            vars.formData.gross_profit_rate = gross_profit_rate;
            vars.formData.operating_profit = operating_profit;
            vars.formData.operating_profit_rate = operating_profit_rate;
          }
        }
      } 

    },
    async gridItemRefresh(id, item){
      if(!id) id = 0;
      vars.filter.common[0].val = id;
      vars.dataSource[item].defaultFilters = vars.filter.common;
      if(vars.grid[item]){
        vars.grid[item].cancelEditData();
        vars.grid[item].refresh();
      }
    },
    onSavingItem(e, item){
      e.promise = methods.onSavingItemImpl(e, item);
    },
    async onSavingItemImpl(e, item){
      for(const element of e.changes){
        if(element.type != 'remove'){
          element.data.fk_business_id = vars.formData.id;
          if (item == 'cost') {
            delete element.data.item;
          }
          await methods.updateUploadFile(element, item)
          
        }
      }
    },
    async updateUploadFile(element, item){
      const uploadService = new ApiService('/api/mes/v1/file-manager')
      for (const key in element.data){
        if(vars.attchFiles[element.data[key]]){
          const fd = new FormData()
          fd.append('file', vars.attchFiles[element.data[key]], vars.attchFiles[element.data[key]].name)
          let path = '';
          if(item == 'quote'){
            path = 'project-business-quote';
          }else if(item == 'basic'){
            path = 'project-business-basic';
          }
          fd.append('path', path)
          const {data: filename} = await uploadService.post('upload', fd)
          element.data['file_path'] = `${path}/${filename}`
          delete vars.attchFiles[element.data[key]]
        }
      }
    },
    printDocument(){
      console.log("printDocument")
    },
    excelUpload(){
      vars.excelRef.value.click();
    },
    async excelFileChange({target}){
      if(!target.files.length) return;
      vars.loading.value = true;
      const fd = new FormData();
      fd.append('file', target.files[0]);
      try {
        const apiService = new ApiService('/api/mes/v1/project/business/excel/upload');
        await apiService.post('', fd);
        notifyInfo('엑셀 업로드가 정상적으로 저장됐습니다.');
      } catch(ex) {
        console.log(ex);
        const errorMessage = ex.response?.data?.message || '엑셀 업로드 중 오류가 발생했습니다';
        notifyError(errorMessage);
      } finally {
        vars.loading.value = false;
        target.value = null;
      }
    },
    onGridInitialized(evt, key){
      vars.grid[key] = evt.component;
      stateStore.bind(`project-business-${key}`, evt.component);
    },
    async loadBaseCode(){
      await baseEmployee.load().then(response=>{
        vars.dataSource.employee_list = response.data;
      });
      return baseCodeLoader(['진행현황', '중요', '진행방법', '영업구분', '지역구분', '계약유형']).then(response =>{
        vars.dataSource.business_progress = response['진행현황']
        vars.dataSource.business_important = response['중요']
        vars.dataSource.progress_method = response['진행방법']
        vars.dataSource.business_type = response['영업구분']
        vars.dataSource.location = response['지역구분']
        vars.dataSource.contract_type = response['계약유형']
      })
      .then(() => (vars.init.value = true));
    },
    onDepartmentChanged(e){
      if(!e.value){
        vars.disabled.save = true;
        vars.disabled.business_manager = true;
        vars.formData.business_manager = null;
        vars.dataSource.employee = [];
      }else{
        const selectItem = e.component.option('selectedItem');

        if(selectItem){
          loadEmployee(vars.dataSource, selectItem.id);
          vars.disabled.business_manager = false;
        }
      }
      methods.checkPossibleSave();
    },
    onBusinessAmountChanged(e){
      if(!e.event) return;
      const grid = vars.grid.cost;
      if (!grid) return;
      const rows = grid.getVisibleRows();
      for(let row of rows){
        grid.cellValue(row.rowIndex, 'item_code', row.data.item_code);
        grid.cellValue(row.rowIndex, 'quote_quantity', row.data.quote_quantity);
      }
    },
    createFindPopupFn(key, title, data = null) {
      const _key = key;
      const _title = title;
      const _data = data;
      if(vars.grid['multiuse-popup']){
        vars.grid['multiuse-popup'].repaint();
      }
      return () => {
        vars.dlg.finder.key = _key;
        vars.dlg.finder.data = _data;
        vars.dlg.finder.title = _title;
        vars.dlg.finder.show = true;
      };
    },
    clearFormData(){
      vars.formData.project = null;
      vars.formData.id = null;
      vars.formData.created = null;
      vars.formData.business_number = '';
      vars.formData.business_name = '';
      vars.formData.business_date = '';
      vars.formData.completion_date = '';
      vars.formData.client_company = '';
      vars.formData.contract_company = '', 
      vars.formData.business_amount = 0;
      vars.formData.rate = 0;
      vars.formData.gross_profit = 0;
      vars.formData.gross_profit_rate = 0;
      vars.formData.operating_profit = 0;
      vars.formData.operating_profit_rate = 0;
      vars.formData.business_department = '';
      vars.formData.business_manager = '';
      vars.formData.business_type = '';
      vars.formData.classification = '';
      vars.formData.location = '';
      vars.formData.business_progress = '';
      vars.formData.business_important = '';
      vars.formData.contract_type = '';
      vars.formData.modify_manager = null;
      vars.formData.modify_date = null;
      vars.formData.fk_project_management_id = null;
      vars.formData.fk_company_id = authService.getCompanyId();

      vars.dataSource.approval = '';
    },
    disableAllAction(){
      vars.disabled.new = false;
      vars.disabled.edit = true;
      vars.disabled.delete = true;
      vars.disabled.save = true;
      vars.disabled.printDocument = true;
      vars.disabled.business_manager = true;
    },
    enableSave(){
      vars.disabled.save = vars.formState.readOnly ? true : false;
    },
    enableDelete(){
      vars.disabled.delete = vars.formState.readOnly ? true : false;
    },
    enableEdit(){
      vars.disabled.edit = !vars.formState.readOnly ?  true : false;
    },
    finderReturnHandler(data){
      switch(vars.dlg.finder.key){
        case 'business': {
          methods.redirect(data.id);
          vars.formState.readOnly = true;
          break;
        }
        case 'client': {
          vars.formData.client_company = data.name;
          methods.onClientChanged();
          break;
        }
        case 'contract_company': {
            vars.formData.contract_company = data.name;
            break;
        }
        case 'project': {
          vars.formData.fk_project_management_id = data.id;
          vars.formData.project = data;
          break;
        }
        case 'location': {
          vars.formData.location = data.map(v => v.code_name).join(',')
          break;
        }
      }
      vars.dlg.finder.show = false;
      vars.dlg.finder.title = '';
      vars.dlg.finder.key = null;
      vars.dlg.finder.data = null;
    },
    async onClientChanged(){
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

      if(!client){
        // vars.disabled.edit = true;
        // vars.disabled.delete = true;
        // vars.disabled.save = true;
        // vars.disabled.tradeYn = false;
      }else{
        if(!methods.isFormReadOnly()){
          let isSelect = true;
          if(client.trade_yn){
            isSelect = await confirm('거래중지 업체입니다. 계속 진행하시겠습니까?', '계약업체');
          }
          if(!isSelect){
            vars.formData.client_company = '';
          }
        }
      }
      methods.checkPossibleSave()
    },
    showItemAddPopup(){
      vars.dlg.addItem.show = true;
    },
    showAddPrevBusinessPopup(){
      vars.dlg.prevBusiness.show = true;
    },
    async prevBusinessChange(row) {
      console.log(row);
      if (!row?.id) {
        await alert('잘못된 선택입니다', '이전 프로젝트에서 가져오기');
        
        return;
      }

      vars.dlg.businessCost.fk_business_id = row.id;
      vars.dlg.businessCost.show = true;
   
    },
    async addPrevBusinessCost(rows){
      if(!rows) return;
      try {
        const grid = vars.grid.cost;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }
        for (const cost of rows) {
          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.dc_rate = cost.dc_rate;
          data.item_code = cost.item_code;
          data.item = cost.item;
          data.item_order = cost.item_order;
          data.purchase_unit_price = cost.purchase_unit_price;
          data.purchase_supply_price = cost.purchase_supply_price;
          data.quote_quantity = cost.quote_quantity;
          data.quote_unit_price = cost.quote_unit_price;
          data.quote_supply_price = cost.quote_supply_price;
        }
        grid.refresh();
        // vars.dlg.prevBusiness.show = false;
        vars.dlg.businessCost.show = false;
      } catch (error) {
        console.error(error);
      }
      
    },
    async addSelectedRows(rows){
      const grid = vars.grid.cost;
      await grid.pageIndex(0);
      const firstRowKey = grid.getKeyByRowIndex(0);
      if (firstRowKey) {
        await grid.navigateToRow(firstRowKey);
      }
      for (let row of rows) {
        let quote_unit_price = 0;
        if (vars.formData.rate > 0 && row.purchase_price > 0){
          quote_unit_price = row.purchase_price * (1 + vars.formData.rate);
        }
        await grid.addRow();
        const data = await grid.byKey(grid.getKeyByRowIndex(0));
        data.item_code = row.item_code;
        data.quote_quantity = 0;
        data.quote_unit_price = quote_unit_price;
        data.quote_supply_price = 0;
        data.purchase_unit_price = row.purchase_price || 0;
        data.purchase_supply_price = 0;
        data.dc_rate = 0;
        data.item = row;
      }
      grid.refresh();
      vars.dlg.addItem.show = false;
    },
    addItemRowButton(item){
      if(vars.grid[item]){
        vars.grid[item].addRow();
      }
    },
    async itemSaveButton(item){
      if(!vars.formData.id) return;
      const grid = vars.grid[item];
      if(grid && grid.hasEditData()){
        await grid.saveEditData();
      }
    },
    initNewRow(evt, item){
      const nowDate = moment().format('YYYY-MM-DD HH:mm:ss');
      const userName = authService.getUserName();
      if(item == 'progress'){
        evt.data.progress_date = nowDate;
        evt.data.client_manager = userName
      }else if(item == 'note'){
        evt.data.note_date = nowDate;
        evt.data.note_manager = userName;
      }else if(item == 'cost'){
        if(vars.grid.cost){
          const rows = vars.grid.cost.getVisibleRows();
          evt.data.item_order = rows.length + 1;
        }
      
        evt.data.quote_supply_price = 0;
      }else if(item == 'customer_information'){
        evt.data.information_date = nowDate;
        evt.data.manager = userName;
        evt.data.register = userName;
        evt.data.register_date = nowDate;
      }else if(item == 'customer_history'){
        evt.data.history_date = nowDate;
        evt.data.manager = userName;
        evt.data.register = userName;
        evt.data.register_date = nowDate;
      }else if(item == 'quote'){
        evt.data.quote_date = nowDate;
        evt.data.quote_manager = userName;
      }else if(item == 'basic'){
        evt.data.basic_date = nowDate;
        evt.data.basic_manager = userName;
      }
    },
    getFirstItemName(itemList) {
        if (!itemList || itemList.length <= 0) {
          return '';
        } else {
          return itemList[0].code_name;
        }
    },
    findAddressSubmit(){
      vars.findAddress.store.keyword = vars.findAddress.keyword;
      vars.grid['find-address'].refresh();
    },
    findAddressSelect(data){
      if(data.key){
        const address = data.key;
        const splitAddress = address.split(' ');
        const result = splitAddress.slice(0, 2).join(' ');  
        vars.formData.location = result;
      }
      vars.findAddress.popup = false;
    },
    findAddressPopup(){
      vars.findAddress.popup = true;
    },
    redirect(id){
      if(id){
        router.replace({ path: `/project/business/${id}` });
      }else{
        router.replace({ path: `/project/business/` });
      }
    },
    onFocusedCellChanged(e, item) {
        vars.focus[item] = e;
    },
    isFormReadOnly(){
      return vars.formState.readOnly;
    },
    onValueChanged(e){
      if(!e.value){
        vars.disabled.save = true;
      }else{
        methods.checkPossibleSave();
      }
    },
    onRateChange(e) {
      if(!e.event) return;
      vars.formData.rate = e.value;
      let rows = vars.grid.cost.getVisibleRows();
      for(let row of rows){
        let quote_unit_price = 0;
        if (vars.formData.rate > 0 && row.data.purchase_unit_price > 0){
          quote_unit_price = row.data.purchase_unit_price * vars.formData.rate;
          vars.grid.cost.cellValue(row.rowIndex, 'quote_unit_price', quote_unit_price);
        }
      }
    },
    checkPossibleSave(){
      if(methods.isFilledFormRequiredData()){
        methods.syncStatusSave();
      }
    },
    isFilledFormRequiredData(){
      if(vars.formData.client_company && vars.formData.business_manager && vars.formData.business_name){
        return true;
      }
      return false; 
    },
    syncStatusSave(){
      if(methods.isFormReadOnly()){
        vars.disabled.save = true;
      }else{
        vars.disabled.save = false;

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
    projectNumberOptions(){
      if(vars.formState.readOnly){
        return {
          readOnly: true,
          buttons: [
          {
            name: 'project_number',
            location: 'after',
            options:{
              icon: 'link',
              stylingMode: 'text',
              disabled: false,
              onClick: methods.redirectToProject
            },
          },
          ],
        }
      }else{
        return {
            ...generateItemButtonOption(
              'search',
              methods.createFindPopupFn('project', '프로젝트 조회', {name : 'fk_business_id', op: 'is_null'})
            ),
            ...vars.formState,
          }
      }
    },
    async redirectToProject(){
      if(!vars.formData.id){
        return;
      }
      if(!vars.formData.fk_project_management_id){
        let isSelect = await confirm('프로젝트번호가 존재하지 않습니다. 프로젝트를 등록 하시겠습니까?', '프로젝트 등록');
        if(!isSelect) return;
        router.replace({path: `/project/registration/business/${vars.formData.id}`})
        return;
      }


      const response = await projectRegistration.load({
        filter: [
          ['id', '=', vars.formData.fk_project_management_id]
        ]
      });
      if(response.data.length > 0){
        router.replace({path: `/project/registration/${response.data[0].id}`});
      }else{
        await alert('프로젝트번호가 존재하지 않습니다', '프로젝트로 이동');
        return;
      }
    },
    
    exportCostToExcel() {
      const grid = vars.grid.cost;
      if (!grid) {
        notifyError('원가검토 표가 초기화되지 않았습니다.');
        return;
      }

      import('devextreme/excel_exporter').then(({ exportDataGrid }) => {
        const workbook = new ExcelJS.Workbook();
        const worksheet = workbook.addWorksheet('원가검토');

        exportDataGrid({
          component: grid,
          worksheet: worksheet,
          autoFilterEnabled: true,
        }).then(() => {
          workbook.xlsx.writeBuffer().then((buffer) => {
            const blob = new Blob([buffer], { type: 'application/octet-stream' });
            const fileName = `원가검토_${moment().format('YYYYMMDD_HHmmss')}.xlsx`;
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = fileName;
            link.click();
          });
        });
      });
    },
    async orderReportButton() {
      const { data : approvalLineData } = await approvalLine.load({
        filter: [
          ['fk_request_emp_id', '=', authService.user?.emp_id],
          'and',
          ['fk_document_id', '=', 1]
        ],
        sort: [
          {
            selector: 'line_order',
            desc: false
          }
        ]
      });
      
      if (!approvalLineData.length) {
        alert('결재선이 존재하지 않습니다. 결재선을 지정해주세요.', '결재선 지정');
        return;
      }
      vars.dlg.orderReport.fk_business_id = vars.formData.id;
      vars.dlg.orderReport.fk_request_emp_id = authService.user?.emp_id;
      vars.dlg.orderReport.show = true;
    },

   
  };

  watch(
    () => props.id,
    () => methods.initById(props.id)
  )
  return {
    vars,
    methods,
    generateItemButtonOption
  }
},


}

</script>
<style lang="scss" scoped>
.number-box{
  margin: 0;
}
::v-deep(.form-group > div:first-child > div:first-child > div:first-child > div:first-child > div:first-child > div:first-child > div:first-child > div:first-child > div:nth-child(1)) {
  flex: 2 1 0px !important;
}
::v-deep(.form-group > div:first-child > div:first-child > div:first-child > div:first-child > div:first-child > div:first-child > div:nth-child(2) > div:first-child > div:nth-child(1)) {
  flex: 2 1 0px !important;
}
.barobill-state {
  padding: 6px 20px;
  border-radius: 4px;
  border: 1px solid #d7d7d7;
  box-shadow: inset 0px 1px 3px 0px #38530d6b;
  background-color: #e3ffb8;
  color: #5c8816;
}
</style>