<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">소요량계산</div>
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
          </dx-toolbar>
        </div>
        <dx-form :form-data="vars.formData">
          <dx-group-item :col-count="4">
            <dx-group-item>
              <dx-simple-item
                data-field="number"
                :editor-options="{
                  placeholder: '(자동 or 직접입력)',
                  ...generateItemButtonOption('search', methods.createFindPopupFn('measure-requirement', '소요량계산 조회')),
                }"
              >
                <dx-label text="소요량 산출번호" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="target_date"
                editor-type="dxDateBox"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                  ...vars.formState,
                }"
              >
                <dx-label text="일자" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item
                data-field="department"
                editor-type="dxSelectBox"
                :editor-options="{
                  valueExpr: 'department_name',
                  displayExpr: 'department_name',
                  dataSource: vars.dataSource.department,
                  onValueChanged: methods.onDepartmentChanged,
                  acceptCustomValue: true,
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
                  dataSource: vars.dataSource.employee,
                  disabled: vars.disabled.manager,
                  ...vars.formState,
                }"
              >
                <dx-label text="담당자" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item
                data-field="note"
                :editor-options="{ ...vars.formState }"
              >
                <dx-label text="참고사항" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="purchase_order_plan_number"
                :editor-options="{
                  readOnly: true,
                  buttons: [
                    {
                      name: 'order_plan_number',
                      location: 'after',
                      options: {
                        icon: 'link',
                        stylingMode: 'text',
                        disabled: false,
                        onClick: methods.redirectOrderPlanNumber,
                      },
                    },
                  ],
                }"
              >
                <dx-label text="발주계획번호" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item
                data-field="etc"
                editor-type="dxTextArea"
                :editor-options="{
                  height: '80px',
                  labelMode: 'hidden',
                  placeholder: '비고',
                  ...generateItemButtonOption('rename', methods.createFindPopupFn('etc', '비고', vars.formData.etc)),
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
          :swipe-enabled="false"
          :animation-enabled="false"
          v-model:selected-index="vars.tab.index"
        >
          <dx-item title="생산계획">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 416px)"
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
                  :disabled="vars.disabled.items"
                  :data-source="vars.dataSource.item1"
                  :on-initialized="(evt) => methods.onGridInitialized(evt, 'item1')"
                  @saving="methods.onSavingItem"
                  @cell-dbl-click="methods.itemPopupClick"
                  @data-error-occurred="methods.onDataError"
                  @focused-cell-changed="methods.onFocusedCellChanged"
                >
                  <dx-grid-toolbar>
                    <dx-item template="addFromPlan" location="before" :visible="!vars.formData.closing_yn && !vars.formState.readOnly" />
                    <dx-item template="addFromWorkOrder" location="before" :visible="!vars.formData.closing_yn && !vars.formState.readOnly" />
                    <dx-item template="addItem" name="addRowButton" :visible="!vars.formData.closing_yn && !vars.formState.readOnly" />
                    <dx-item name="saveButton" :visible="!!vars.formData.id" />
                    <dx-item name="revertButton" />
                    <dx-item name="columnChooserButton" />
                  </dx-grid-toolbar>
                  <template #addFromPlan>
                    <dx-button text="생산계획에서 가져오기" icon="add" @click="methods.showAddPlanItem" />
                  </template>
                  <template #addFromWorkOrder>
                    <dx-button text="작업지시잔량에서 가져오기" icon="add" @click="methods.showAddWorkOrderItem" />
                  </template>
                  <template #addItem>
                    <dx-button icon="add" @click="methods.showAddBaseItem" />
                  </template>

                  <dx-column caption="품목코드" data-field="item_code" width="180" :allow-editing="false" />
                  <dx-column caption="품명" data-field="item.item_name" :allow-editing="false" />
                  <dx-column caption="규격" data-field="item.item_standard" :allow-editing="false" />
                  <dx-column caption="BOM여부" data-field="item.bom_yn" data-type="boolean" :allow-editing="false" />
                  <dx-column caption="생산계획수량" data-field="production_plan_quantity" data-type="number" format="fixedPoint" :set-cell-value="methods.setQuantity" />
                  <dx-column caption="단가" data-field="unit_price" data-type="number" format="₩,##0" :set-cell-value="methods.setUnitPrice" />
                  <dx-column caption="단위" data-field="item.unit" :allow-editing="false" />
                  <dx-column caption="공급가" data-field="supply_price" data-type="number" format="₩,##0" :allow-editing="false" />
                  <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
                  <dx-column caption="미작지수량" data-field="unordered_quantity" data-type="number" format="fixedPoint" :allow-editing="false" />
                  <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :allow-editing="false" />
                  <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :allow-editing="false" />
                  <dx-column caption="입고창고" data-field="warehouse.wh_name" :set-cell-value="methods.setWarehouse">
                    <dx-lookup value-expr="wh_name" display-expr="wh_name" :data-source="vars.dataSource.warehouse" />
                  </dx-column>
                  <dx-column caption="수주번호" data-field="order_number" :allow-editing="false" />
                  <dx-column caption="발주계획번호" data-field="purchase_order_plan_number" :allow-editing="false" />
                  <dx-column caption="프로젝트번호" data-field="project_management.project_number"
                    :editor-options="{ ...generateItemButtonOption('search', methods.createFindPopupFn('project', '프로젝트조회')) }"
                    :set-cell-value="methods.setProjectManagement"
                  />
                  <dx-column caption="고객업체" data-field="client_company"
                    :editor-options="{ ...generateItemButtonOption('search', methods.createFindPopupFn('client', '고객업체조회')) }"
                  />
                  <dx-column caption="고객사품번" data-field="client_item_number" />
                  <dx-column caption="실수요자" data-field="end_user" :allow-editing="false" />
                  <dx-column caption="품목설명" data-field="item.item_detail" :allow-editing="false" />
                  <dx-column caption="소요량계산 아이디" data-field="fk_measure_requirement_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
                  <dx-column caption="생산계획품목 아이디" data-field="fk_plan_item_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
                  <dx-column caption="창고코드" data-field="warehouse_code" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />

                  <dx-summary :recalculate-while-editing="true" :calculate-custom-summary="methods.calculateCustomSummary">
                    <dx-total-item name="supply_price" summary-type="custom" />
                  </dx-summary>

                  <dx-scrolling mode="standard" />
                  <dx-column-chooser mode="select" :enabled="true" />
                  <dx-editing mode="batch" 
                    :allow-adding="!vars.formData.closing_yn && !vars.formState.readOnly"
                    :allow-updating="!vars.formData.closing_yn && !vars.formState.readOnly"
                    :allow-deleting="!vars.formData.closing_yn && !vars.formState.readOnly"
                  />
                </dx-data-grid>
              </div>
            </template>
          </dx-item>

          <dx-item title="소요량계산">
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
                  :allow-column-resizing="true"
                  :allow-column-reordering="true"
                  :select-text-on-edit-start="true"
                  :disabled="vars.disabled.items"
                  :data-source="vars.dataSource.item2"
                  :on-initialized="(evt) => methods.onGridInitialized(evt, 'item2')"
                  @init-new-row="methods.onItem2Insert"
                  @cell-dbl-click="methods.itemPopupClick"
                  @focused-cell-changed="methods.onFocusedCellChanged2"
                >
                  <dx-grid-toolbar>
                    <dx-item template="calculate" location="before" :visible="!vars.formData.closing_yn" />
                    <dx-item template="exportPlan" location="before" :visible="!vars.formData.closing_yn" />
                    <dx-item name="saveButton" />
                    <dx-item name="revertButton" />
                    <dx-item name="exportButton" />
                    <dx-item name="columnChooserButton" />
                  </dx-grid-toolbar>
                  <template #calculate>
                    <dx-button text="소요량 재계산하기" icon="formula" @click="methods.calculateConsume" />
                  </template>
                  <template #exportPlan>
                    <dx-button text="발주계획으로 보내기" icon="export" @click="methods.exportOrderPlan" />
                  </template>

                  <dx-column caption="품목코드" data-field="item_code" width="180" :allow-editing="false" />
                  <dx-column caption="품명" data-field="item.item_name" :allow-editing="false" />
                  <dx-column caption="규격" data-field="item.item_standard" :allow-editing="false" />
                  <dx-column caption="자산구분" data-field="item.asset_type" :allow-editing="false" />
                  <dx-column caption="안전재고" data-field="item.safety_stock" data-type="number" format="fixedPoint" :allow-editing="false" />
                  <dx-column caption="MOQ" data-field="item.moq" data-type="number" format="fixedPoint" :allow-editing="false" />
                  <dx-column caption="소요량" data-field="requirement_quantity" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
                  <dx-column caption="발주계획량" data-field="order_plan_quantity" data-type="number" format="fixedPoint" :allow-editing="false" :set-cell-value="methods.setQuantity2" />
                  <dx-column caption="미발주 계획수량" data-field="unordered_plan_quantity" data-type="number" format="fixedPoint" :allow-editing="false" />
                  <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :allow-editing="false" />
                  <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :allow-editing="false" />
                  <dx-column caption="입고창고" data-field="warehouse.wh_name" :set-cell-value="methods.setWarehouse">
                    <dx-lookup value-expr="wh_name" display-expr="wh_name" :data-source="vars.dataSource.warehouse" />
                  </dx-column>
                  <dx-column caption="단가" data-field="unit_price" data-type="number" format="₩,##0" :set-cell-value="methods.setUnitPrice2" />
                  <dx-column caption="공급가" data-field="supply_price" data-type="number" format="₩,##0" :allow-editing="false" />
                  <dx-column caption="대분류" data-field="item.main_category" :allow-editing="false" />
                  <dx-column caption="중분류" data-field="item.middle_category" :allow-editing="false" />
                  <dx-column caption="소분류" data-field="item.sub_category" :allow-editing="false" />
                  <dx-column caption="공급업체" data-field="client_company"
                    :editor-options="{ ...generateItemButtonOption('search', methods.createFindPopupFn('client2', '공급업체조회')) }"
                  />
                  <dx-column caption="수주번호" data-field="order_number" :visible="false" />
                  <dx-column caption="프로젝트번호" data-field="project_management.project_number" :visible="false" />
                  <dx-column caption="실수요자" data-field="end_user" :visible="false" />
                  <dx-column caption="납기일자" data-field="delivery_date" data-type="date" format="yyyy-MM-dd" :visible="false" />
                  <dx-column caption="소요량계산 아이디" data-field="fk_measure_requirement_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
                  <dx-column caption="생산계획품목 아이디" data-field="fk_plan_item_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
                  <dx-column caption="창고코드" data-field="warehouse_code" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />

                  <dx-export :enabled="true" />
                  <dx-scrolling mode="standard" />
                  <dx-column-chooser mode="select" :enabled="true" />
                  <dx-editing mode="batch"
                    :allow-adding="!vars.formData.closing_yn && !vars.formState.readOnly"
                    :allow-updating="!vars.formData.closing_yn && !vars.formState.readOnly"
                    :allow-deleting="!vars.formData.closing_yn && !vars.formState.readOnly"
                  />
                </dx-data-grid>
              </div>
            </template>
          </dx-item>
        </dx-tab-panel>

        <div class="mt-2">
          <table class="summary-table">
            <tr>
              <th>공급가</th>
              <td>{{ vars.summary.supply_price.value }}</td>
              <th>부가세</th>
              <td>{{ vars.summary.vat.value }}</td>
              <th>합계금액</th>
              <td>{{ vars.summary.total_price.value }}</td>
            </tr>
          </table>
        </div>
      </div>
    </div>

    <dx-popup
      title="생산계획에서 가져오기"
      content-template="popup-content"
      v-model:visible="vars.dlg.addPlanItem.show"
      width="70%"
      :height="500"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="(evt) => methods.onGridInitialized(evt, 'load-plan-popup')"
    >
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ text: '선택된 항목 추가', icon: 'add', onClick: methods.addPlanItem }"
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
          :on-initialized="(evt) => methods.onGridInitialized(evt, 'planItem')"
        >
          <dx-column caption="생산계획번호" data-field="production_plan.number" :sort-index="0" sort-order="desc" />
          <dx-column caption="발주계획번호" data-field="purchase_order_plan_number" />
          <dx-column caption="고객업체" data-field="client_company" />
          <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" :sort-index="1" sort-order="desc" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="자산구분" data-field="item.asset_type" />
          <dx-column caption="생산계획수량" data-field="production_plan_quantity" data-type="number" format="fixedPoint" />
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
      title="작업지시잔량에서 가져오기"
      content-template="popup-content"
      v-model:visible="vars.dlg.addWorkOrderItem.show"
      width="70%"
      :height="500"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="(evt) => methods.onGridInitialized(evt, 'load-work-order-popup')"
    >
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ text: '선택된 항목 추가', icon: 'add', onClick: methods.addWorkOrderItem }"
      />

      <template #popup-content>
        <dx-data-grid
          column-resizing-mode="widget"
          :show-borders="true"
          :remote-operations="true"
          :column-auto-width="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="vars.dataSource.workOrderItem"
          :on-initialized="(evt) => methods.onGridInitialized(evt, 'workOrderItem')"
        >
          <dx-column caption="작업지시번호" data-field="work_order.number" :sort-index="1" sort-order="desc" />
          <dx-column caption="작업지시일자" data-field="work_order.target_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
          <dx-column caption="고객업체" data-field="client_company" />
          <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="자산구분" data-field="item.asset_type" />
          <dx-column caption="작업지시수량" data-field="required_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="미생산수량" data-field="unproduced_quantity" data-type="number" format="fixedPoint" />
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
      v-model:visible="vars.dlg.addItem.show"
      width="70%"
      :height="500"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="(evt) => methods.onGridInitialized(evt, 'base-item-popup')"
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
          :on-initialized="(evt) => methods.onGridInitialized(evt, 'baseItem')"
        >
          <dx-grid-toolbar>
            <dx-item template="addItemButton" location="after" />
            <dx-grid-item name="addRowButton" location="after" />
          </dx-grid-toolbar>
          <template #addItemButton>
            <dx-button text="선택된 항목 추가" icon="add" @click="methods.addBaseItem" />
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
      :height="320"
      :key="vars.dlg.finder.key"
      :title="vars.dlg.finder.title"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="(evt) => methods.onGridInitialized(evt, 'multiuse-popup')"
    >
      <template #popup-content>
        <data-grid-client v-if="vars.dlg.finder.key === 'client'" @change="methods.finderReturnHandler" />
        <data-grid-client v-else-if="vars.dlg.finder.key === 'client2'" @change="methods.finderReturnHandler" />
        <data-grid-project v-else-if="vars.dlg.finder.key === 'project'" @change="methods.finderReturnHandler" />
        <data-grid-measure-requirement v-else-if="vars.dlg.finder.key === 'measure-requirement'" @change="methods.finderReturnHandler" />
        <div v-else-if="vars.dlg.finder.key === 'etc'">
          <div class="mb-2">
            <dx-text-area :height="190" :value="vars.dlg.finder.data" @update:value="methods.updateEtcValue" />
          </div>
          <dx-toolbar>
            <dx-item widget="dxButton" toolbar="top" location="after"
              :options="{ text: '닫기', icon: null, onClick: methods.finderReturnHandler, }"
            />
          </dx-toolbar>
        </div>
      </template>
    </dx-popup>

    <popup-item-detail v-model:visible="vars.itemDetail.visible" :item-id="vars.itemDetail.id" />
  </div>
</template>

<script>
import numeral from 'numeral';

import { onMounted, ref, reactive, computed, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';

import { DxButton } from 'devextreme-vue/button';
import DxTextArea from 'devextreme-vue/text-area';
import { DxTabPanel } from 'devextreme-vue/tab-panel';
import { confirm, alert } from 'devextreme/ui/dialog';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import {
  DxForm,
  DxLabel,
  DxGroupItem,
  DxSimpleItem,
  DxRequiredRule,
} from 'devextreme-vue/form';
import {
  DxDataGrid,
  DxColumn,
  DxPaging,
  DxLookup,
  DxExport,
  DxEditing,
  DxSorting,
  DxSummary,
  DxTotalItem,
  DxSelection,
  DxFilterRow,
  DxScrolling,
  DxColumnChooser,
  DxToolbar as DxGridToolbar,
  DxItem as DxGridItem,
  DxRequiredRule as DxGridRequiredRule,
} from 'devextreme-vue/data-grid';

import PopupItemDetail from '@/components/base/popup-item-detail';
import DataGridClient from '../../components/base/data-client.vue';
import DataGridProject from '../../components/project/data-project.vue';
import DataGridOrderPlan from '../../components/purchase/data-order-plan.vue';
import DataGridMeasureRequirement from '../../components/produce/data-measure-requirement.vue';

import { getStock } from '../../data-source/setup';
import { purchaseOrderPlan } from '../../data-source/purchase';
import { baseCodeLoader, getBaseItem } from '../../data-source/base';
import {
  measureRequirement,
  getMeasureRequirementItem1,
  getMeasureRequirementItem2,
  getProducePlanItem,
  getProduceWorkOrderItem1,
} from '../../data-source/produce';

import authService from '../../auth';
import stateStore from '@/utils/state-store';
import ApiService from '../../utils/api-service';
import { notifyInfo, notifyError } from '../../utils/notify';
import {
  loadEmployee,
  loadWarehouse,
  loadDepartment,
} from '../../utils/data-loader';
import {
  sumSupplyPrice,
  calcPriceSummary,
  beforeExitConfirm,
  generateItemButtonOption,
  currentDateTime,
} from '../../utils/util';

export default {
  components: {
    DxButton,
    DxTextArea,
    DxTabPanel,
    DxLoadPanel,
    DxToolbar,
    DxItem,
    DxPopup,
    DxToolbarItem,
    DxForm,
    DxLabel,
    DxGroupItem,
    DxSimpleItem,
    DxRequiredRule,
    DxDataGrid,
    DxColumn,
    DxPaging,
    DxLookup,
    DxExport,
    DxEditing,
    DxSorting,
    DxSummary,
    DxTotalItem,
    DxSelection,
    DxFilterRow,
    DxScrolling,
    DxColumnChooser,
    DxGridToolbar,
    DxGridRequiredRule,
    DxGridItem,
    PopupItemDetail,
    DataGridClient,
    DataGridOrderPlan,
    DataGridProject,
    DataGridMeasureRequirement,
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
    vars.dlg.addItem = reactive({ show: false });
    vars.dlg.addPlanItem = reactive({ show: false });
    vars.dlg.addWorkOrderItem = reactive({ show: false });
    vars.grid = {
      baseItem: null,
      item1: null,
      item2: null,
      planItem: null,
      workOrderItem: null,
    };
    vars.dlg.finder = reactive({
      show: false,
      title: '',
      key: null,
      data: null,
    });
    vars.warehouse = {};
    vars.filter = reactive({
      baseItem: { clientId: null },
      item1: [
        { name: 'fk_measure_requirement_id', op: 'eq', val: props.id || 0 },
      ],
      item2: [
        { name: 'fk_measure_requirement_id', op: 'eq', val: props.id || 0 },
      ],
    });
    vars.disabled = reactive({
      new: false,
      edit: true,
      save: true,
      delete: true,
      items: true,
      manager: true,
      clientManager: true,
      tradeYn: false,
    });
    vars.dataSource = reactive({
      vat_type: [],
      client_company: [],
      client_manager: [],
      department: [],
      employee: [],
      warehouse: [],
      baseItem: null,
      planItem: null,
      workOrderItem: null,
      item_group: [],
      asset_type: [],
      item1: getMeasureRequirementItem1(vars.filter.item1),
      item2: getMeasureRequirementItem2(vars.filter.item2),
    });
    vars.focus = reactive({ item1: null, item2: null });
    vars.formData = reactive({});

    vars.summary = {};
    vars.summary.supply_price = computed(() => '₩' + numeral(vars.formData.supply_price).format('0,0'));
    vars.summary.vat = computed(() => '₩' + numeral(vars.formData.vat).format('0,0'));
    vars.summary.total_price = computed(() => '₩' + numeral(vars.formData.total_price).format('0,0'));

    vars.itemDetail = reactive({ visible: false, id: 0 });

    onMounted(async () => {
      await loadDepartment(vars.dataSource);
      await methods.loadBaseCode();
      methods.initById(props.id);
      loadWarehouse(vars.dataSource);
    });

    // public methods
    const methods = {
      async initById(id) {
        beforeExitConfirm.check(() => !vars.disabled.save);
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

        let { data } = await measureRequirement.byKey(id);
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
        vars.formData.supply_price = 0;
        vars.formData.vat = 0;
        vars.formData.total_price = 0;
        vars.formData.closing_yn = false;
        vars.formData.purchase_order_plan_number = null;
        vars.formData.fk_company_id = authService.getCompanyId();
      },
      async addPlanItem() {
        const grid = vars.grid.item1;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        const rows = [...(await vars.grid.planItem.getSelectedRowsData())];
        for (let row of rows) {
          // 생산계획
          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code; // 품목코드
          data.item = { ...row.item }; // 품목
          data.production_plan_quantity = row.production_plan_quantity; // 생산계획수량
          data.unit_price = row.unit_price; // 단가
          data.supply_price = data.production_plan_quantity * data.unit_price; // 공급가
          data.request_delivery_date = row.request_delivery_date; // 요청납기
          data.unordered_quantity = row.unordered_quantity; // 미작지수량
          data.basic_stock = { ...row.basic_stock }; // 기초재고
          data.warehouse = { ...vars.warehouse }; // 입고창고
          data.warehouse_code = vars.warehouse.wh_code; // 창고코드
          data.order_number = row.order_number; // 수주번호
          data.client_company = row.client_company; // 고객업체
          data.client_item_number = row.client_item_number; // 고객사품번
          data.end_user = row.end_user; // 실수요자
          data.purchase_order_plan_number = row.purchase_order_plan_number; // 발주계획번호
          data.fk_project_management_id = row.fk_project_management_id; // 프로젝트번호
          data.fk_plan_item_id = row.id; // 생산계획품목 아이디
          data.fk_work_order_item_id = null; // 작업지시품목 아이디
          data.fk_measure_requirement_id = vars.formData.id; // 소요량계산 아이디
          data.project_management = row.project_management ? row.project_management : null;
        }
        vars.dlg.addItem.show = false;
        vars.dlg.addPlanItem.show = false;
        grid.refresh();
      },
      async addWorkOrderItem() {
        const grid = vars.grid.item1;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        const rows = [...(await vars.grid.workOrderItem.getSelectedRowsData())];
        for (let row of rows) {
          // 작업지시
          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code; // 품목코드
          data.item = { ...row.item }; // 품목
          data.production_plan_quantity = row.unproduced_quantity; // 생산계획수량
          data.unit_price = row.plan_item ? row.plan_item.unit_price : 0; // 단가
          data.supply_price = data.production_plan_quantity * data.unit_price; // 공급가
          data.request_delivery_date = row.request_delivery_date; // 요청납기
          data.unordered_quantity = row.plan_item ? row.plan_item.unordered_quantity : 0; // 미작지수량
          data.basic_stock = { ...row.basic_stock }; // 기초재고
          data.warehouse = { ...vars.warehouse }; // 입고창고
          data.warehouse_code = vars.warehouse.wh_code; // 창고코드
          data.order_number = row.order_number; // 수주번호
          data.client_company = row.client_company; // 고객업체
          data.client_item_number = row.client_item_number; // 고객사품번
          data.end_user = row.end_user; // 실수요자
          data.fk_project_management_id = row.fk_project_management_id; // 프로젝트번호
          data.fk_plan_item_id = null; // 생산계획품목 아이디
          data.fk_work_order_item_id = row.id; // 작업지시품목 아이디
          data.fk_measure_requirement_id = vars.formData.id; // 소요량계산 아이디
          data.project_management = row.project_management ? row.project_management : null;
        }
        vars.dlg.addItem.show = false;
        vars.dlg.addWorkOrderItem.show = false;
        grid.refresh();
      },
      async addBaseItem() {
        const grid = vars.grid.item1;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        const rows = [...(await vars.grid.baseItem.getSelectedRowsData())];
        for (let row of rows) {
          const clientItemNumber = row.client_item
            ? row.client_item.client_item_code
            : null;
          const basicStock = row.basic_stock
            ? { ...row.basic_stock }
            : { current_stock: 0, available_stock: 0 };

          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.item_code = row.item_code; // 품목코드
          data.item = { ...row }; // 품목
          data.production_plan_quantity = 0; // 생산계획수량
          data.unit_price = row.sales_price ? row.sales_price : 0; // 단가
          data.supply_price = 0; // 공급가
          data.request_delivery_date = null; // 요청납기
          data.unordered_quantity = 0; // 미작지수량
          data.basic_stock = { ...basicStock }; // 기초재고
          data.warehouse = { ...vars.warehouse }; // 입고창고
          data.warehouse_code = vars.warehouse.wh_code; // 창고코드
          data.order_number = null; // 수주번호
          data.client_company = null; // 고객업체
          data.client_item_number = clientItemNumber; // 고객사품번
          data.end_user = null; // 실수요자
          data.fk_project_management_id = null; // 프로젝트번호
          data.fk_plan_item_id = null; // 생산계획품목 아이디
          data.fk_work_order_item_id = null; // 작업지시품목 아이디
          data.fk_measure_requirement_id = vars.formData.id; // 소요량계산 아이디
        }
        vars.dlg.addItem.show = false;
        vars.dlg.addPlanItem.show = false;
        grid.refersh();
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
      showAddBaseItem() {
        methods.gridClear(vars.grid.baseItem);
        vars.dlg.addItem.show = true;
      },
      showAddPlanItem() {
        const notContains = [];
        for (const item of vars.grid.item1.getVisibleRows()) {
          if (!item.id && item.data.fk_plan_item_id) {
            notContains.push(['id', '<>', item.data.fk_plan_item_id], 'and');
          }
        }
        notContains.pop();

        if (vars.grid.planItem) {
          vars.grid.planItem.filter(notContains);
          methods.gridClear(vars.grid.planItem);
        }
        vars.dlg.addPlanItem.show = true;
      },
      showAddWorkOrderItem() {
        const notContains = [];
        for (const item of vars.grid.item1.getVisibleRows()) {
          if (!item.id && item.data.fk_work_order_item_id) {
            notContains.push(
              ['id', '<>', item.data.fk_work_order_item_id],
              'and'
            );
          }
        }
        notContains.pop();

        if (vars.grid.workOrderItem) {
          vars.grid.workOrderItem.filter(notContains);
          methods.gridClear(vars.grid.workOrderItem);
        }
        vars.dlg.addWorkOrderItem.show = true;
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
      async gridItem2Refresh(id) {
        if (!id) id = 0;
        vars.filter.item2[0].val = id;
        vars.dataSource.item2.defaultFilters = vars.filter.item2;
        if (vars.grid.item2) {
          vars.grid.item2.cancelEditData();
          vars.grid.item2.refresh();
        }
      },
      async gridSaveEdit(grid) {
        if (grid && grid.hasEditData()) {
          await grid.saveEditData();
        }
      },
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`produce-mea-req-${key}`, evt.component);
      },
      async calculateConsume() {
        const rows = vars.grid.item1.getVisibleRows();
        for (let row of rows) {
          if (!row.data.item.bom_yn) {
            await alert('BOM이 구성되지 않은 품목이 있습니다', 'BOM 확인');
            return;
          }
        }

        const result = await confirm(
          '소요량 재계산 시 기존에 계산된 내용이 모두 삭제됩니다.<br/>계속하시겠습니까?',
          '소요량 재계산하기'
        );
        if (result) {
          const params = {
            mea_req_id: vars.formData.id,
            warehouse_code: vars.warehouse.wh_code,
          };
          const apiService = new ApiService('/api/mes/v1/update-mea-req');
          await apiService.post('', params);
          vars.grid.item2.refresh();
        }
      },
      async exportOrderPlan() {
        const result = await confirm(
          '발주계획으로 보내기 후 품목 변경이 불가능합니다.<br/>계속하시겠습니까?',
          '발주계획으로 보내기'
        );
        if (result) {
          const params = {
            mea_req_id: vars.formData.id,
            company_id: authService.getCompanyId(),
          };
          const apiService = new ApiService('/api/mes/v1/export-mea-req');
          await apiService.post('', params);
          beforeExitConfirm.clear();
          await alert(
            '발주계획으로 보내기가 완료되었습니다',
            '발주계획으로 보내기'
          );
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
            await measureRequirement.remove(vars.formData.id);
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
            await measureRequirement.update(vars.formData.id, vars.formData);
            await methods.gridSaveEdit(vars.grid.item1);
            await methods.gridSaveEdit(vars.grid.item2);

            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');

            methods.enableSave();
            methods.enableDelete();
          } else {
            // 채번이 없을 경우 자동 채번
            let { data } = await measureRequirement.insert(vars.formData);
            vars.formData.id = data.id;

            await methods.gridSaveEdit(vars.grid.item1);
            await methods.gridSaveEdit(vars.grid.item2);

            beforeExitConfirm.clear();
            methods.redirect(data.id);
            vars.formState.readOnly = true;
            notifyInfo('저장되었습니다');
          }
        } catch (ex) {
          if (ex.response.status === 602) {
            notifyError('이미 존재하는 소요량산출번호 입니다');
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
          case 'measure-requirement': {
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
          case 'client2': {
            vars.grid.item2.cellValue(
              vars.focus.item2.rowIndex,
              vars.focus.item2.columnIndex,
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
            console.log(vars.dlg.finder.data);
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
        methods.loadWorkOrderItem();
      },
      onFocusedCellChanged(e) {
        vars.focus.item1 = e;
      },
      onFocusedCellChanged2(e) {
        vars.focus.item2 = e;
      },
      onSavingItem(e) {
        e.changes.forEach((element) => {
          if (element.type != 'remove') {
            element.data.fk_measure_requirement_id = vars.formData.id;
            delete element.data.item;
            delete element.data.warehouse;
            delete element.data.basic_stock;
            delete element.data.plan_item;
            delete element.data.work_order_item;
            delete element.data.measure_requirement;
          }
        });
        methods.saveSummary();
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
      saveSummary() {
        const priceData = {
          supply_price: vars.formData.supply_price,
          vat: vars.formData.vat,
          total_price: vars.formData.total_price,
        };
        measureRequirement.update(vars.formData.id, priceData);
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
      setProjectManagement(newData, value, currentRowData){
        if(!value) return;
        newData.project_management = value;
        newData.fk_project_management_id = value.id;
      },
      loadBaseCode() {
        return baseCodeLoader(['부가세구분', '자산구분', '품목그룹',])
          .then((response) => {
            vars.dataSource.vat_type = [...response['부가세구분']];
            vars.dataSource.asset_type = response['자산구분'];
            vars.dataSource.item_group = response['품목그룹'];
          })
          .then(() => (vars.init.value = true));
      },
      setQuantity(newData, value, currentRowData) {
        newData.unordered_quantity =
          currentRowData.unordered_quantity +
          (value - currentRowData.production_plan_quantity);
        newData.production_plan_quantity = value;
        newData.unit_price = currentRowData.unit_price;
        newData.supply_price = value * newData.unit_price;
      },
      setUnitPrice(newData, value, currentRowData) {
        newData.production_plan_quantity =
          currentRowData.production_plan_quantity;
        newData.unit_price = value;
        newData.supply_price = newData.production_plan_quantity * value;
      },
      setQuantity2(newData, value, currentRowData) {
        newData.unordered_plan_quantity =
          currentRowData.unordered_plan_quantity +
          (value - currentRowData.order_plan_quantity);
        newData.order_plan_quantity = value;
        newData.unit_price = currentRowData.unit_price;
        newData.supply_price = value * newData.unit_price;
      },
      setUnitPrice2(newData, value, currentRowData) {
        newData.order_plan_quantity = currentRowData.order_plan_quantity;
        newData.unit_price = value;
        newData.supply_price = newData.order_plan_quantity * value;
      },
      calculateCustomSummary(options) {
        if (options.name === 'supply_price') {
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          } else if (options.summaryProcess === 'calculate') {
            options.totalValue += options.value.production_plan_quantity * options.value.unit_price;
          } else if (options.summaryProcess === 'finalize') {
            const response = calcPriceSummary(vars.formData.vat_type, options.totalValue);
            vars.formData.supply_price = response.supply_price;
            vars.formData.vat = response.vat;
            vars.formData.total_price = response.total_price;
          }
        }
      },
      loadBaseItem() {
        vars.dataSource.baseItem = getBaseItem(
          null,
          null,
          vars.warehouse.wh_code
        );
      },
      loadPlanItem() {
        vars.dataSource.planItem = getProducePlanItem([
          {
            name: 'not_measure_requirement',
            op: 'gt',
            val: 0,
          },
        ]);
      },
      loadWorkOrderItem() {
        vars.dataSource.workOrderItem = getProduceWorkOrderItem1([
          { name: 'unproduced_quantity', op: 'gt', val: 0 },
        ]);
      },
      checkPossibleSave() {
        if (vars.formData.department) {
          methods.enableSave();
          vars.disabled.items = false;
        }
      },
      redirect(id) {
        if (id) {
          router.replace({ path: `/produce/measure-requirement/${id}` });
        } else {
          router.replace({ path: `/produce/measure-requirement` });
        }
      },
      async redirectOrderPlanNumber() {
        if (!vars.formData.purchase_order_plan_number) {
          await alert(
            '발주계획번호가 존재하지 않습니다',
            '재고이동요청으로 이동'
          );
          return;
        }
        const response = await purchaseOrderPlan.load({
          filter: [
            [
              'order_plan_number',
              '=',
              vars.formData.purchase_order_plan_number,
            ],
            ['fk_company_id', '=', authService.getCompanyId()],
          ],
        });
        if (response.data.length > 0) {
          router.replace({
            path: `/purchase/order-plan/${response.data[0].id}`,
          });
        } else {
          await alert('발주계획번호가 존재하지 않습니다', '발주계획으로 이동');
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
