<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings">
        <div class="content-header">
          <dx-toolbar>
            <dx-item location="before">
              <div class="content-title">품목관리</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <dx-data-grid
          class="fixed-header-table"
          date-serialization-format="yyyy-MM-ddTHH:mm:ss"
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :focused-row-enabled="true"
          :allow-column-resizing="true"
          :select-text-on-edit-start="true"
          :data-source="vars.baseItem"
          :on-initialized="evt => methods.onInitialized(evt, 'gridItem')"
          @exporting="methods.onExporting"
          @data-error-occurred="methods.onDataError"
          @cell-dbl-click="methods.itemPopupClick"
        >
          <dx-grid-toolbar>
            <dx-item location="after" template="addItem" />
            <dx-item name="columnChooserButton" />
            <dx-item name="exportButton" />
            <dx-item location="after" template="excelUploadButton" />
            <dx-item location="after" template="excelSampleDownloadButton" />
          </dx-grid-toolbar>
          <template #addItem>
            <dx-button icon="add" @click="methods.newItem" />
          </template>
          <template #excelUploadButton>
            <dx-button icon="upload" @click="methods.excelUpload" />
          </template>
          <template #excelSampleDownloadButton>
            <dx-button icon="download" @click="methods.excelSampleDownload" />
          </template>

          <dx-column caption="품목코드" data-field="item_code" :allow-editing="false" />
          <dx-column caption="품명" data-field="item_name" :allow-editing="true" />
          <dx-column caption="규격" data-field="item_standard" :allow-editing="true" />
          <dx-column caption="단위" data-field="unit" :allow-editing="true">
            <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.dataSource.unit" />
          </dx-column>
          <dx-column caption="대분류" data-field="main_category" :allow-editing="true">
            <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.dataSource.main_category" />
          </dx-column>
           <dx-column caption="품목그룹" data-field="item_group" :allow-editing="true">
            <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.dataSource.item_group" />
          </dx-column>
          <dx-column caption="중분류" data-field="middle_category" :allow-editing="true" :visible="false">
            <dx-lookup value-expr="code_name" display-expr="code_name"  :data-source="vars.dataSource.middle_category_all" />
          </dx-column>
          <dx-column caption="소분류" data-field="sub_category" :allow-editing="true" :visible="false">
            <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.dataSource.sub_category_all" />
          </dx-column>
          <dx-column caption="자산구분" data-field="asset_type" :allow-editing="true">
            <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.dataSource.asset_type" />
          </dx-column>
          <dx-column caption="품목설명" data-field="item_detail" :allow-editing="true" />
          <dx-column caption="품목번호" data-field="id" :visible="false" :allow-editing="false" />
          <dx-column caption="최초등록일자" data-field="created" data-type="date" format="yyyy-MM-dd" :visible="false" :allow-editing="false" />
          <dx-column caption="MOQ" data-field="moq" :visible="false" />
          <dx-column caption="포장단위수량" data-field="packing_quantity" :visible="false" />
          <dx-column caption="이송단위수량" data-field="transfer_quantity" :visible="false" />
          <dx-column caption="표준납기일" data-field="delivery_date" :visible="false" />
          <dx-column caption="수입검사" data-field="import_check" data-type="boolean" :visible="false" />
          <dx-column caption="출하검사" data-field="shipment_check" data-type="boolean" :visible="false" />
          <dx-column caption="LOT관리" data-field="lot_check" data-type="boolean" :visible="false" />
          <dx-column caption="안전재고" data-field="safety_stock" :visible="false" />
          <dx-column caption="매출단가" data-field="sales_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :visible="false" />
          <dx-column caption="매입단가" data-field="purchase_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :visible="false" />
          <dx-column caption="참고1" data-field="note1" :visible="false" />
          <dx-column caption="참고2" data-field="note2" :visible="false" />
          <dx-column caption="비고" data-field="etc" :visible="false" />
          <dx-column caption="HS Code" data-field="hs_code" :visible="false" />
          <dx-column caption="변경전 품목코드" data-field="before_item_code" :visible="false" />
          <dx-column caption="변경후 품목코드" data-field="after_item_code" :visible="false" />
          <dx-column caption="사용종료" data-field="end_of_use" data-type="boolean" :visible="false" />
          <dx-column caption="종료일자" data-field="end_date" data-type="date" format="yyyy-MM-dd" :visible="false" />
          <dx-column caption="최초등록자" data-field="register_id" :visible="false" :allow-editing="false" />
          <dx-column caption="최종수정자" data-field="modify_id" :visible="false" :allow-editing="false" />
          <dx-column caption="최종수정일자" data-field="modify_date" data-type="date" format="yyyy-MM-dd" :visible="false" :allow-editing="false" />
          <dx-column type="buttons">
            <dx-grid-button hint="상세설정" icon="edit" :visible="true" @click="methods.editItem" />
            <dx-grid-button name="delete" />
          </dx-column>

          <dx-export :enabled="true" />
          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-column-chooser mode="select" :enabled="true" />
          <dx-editing mode="cell" :use-icons="true" :allow-adding="false" :allow-updating="false" :allow-deleting="true" />
        </dx-data-grid>

        <dx-popup
          title="품목관리"
          content-template="popup-content"
          v-model:visible="vars.addItem.visible"
          width="70%"
          height="80%"
          :resize-enabled="true"
          :close-on-outside-click="true"
          :onHiding="methods.addItemOnHiding"
          @initialized="evt => methods.onInitialized(evt, 'detail-popup')"
        >
          <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
            :options="{ text: 'QR라벨인쇄', icon: 'print', onClick: methods.prepareQRLabel }"
          />
          <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
            :options="{ text: '저장', icon: 'save', onClick: methods.onClickItemSave }"
          />

          <template #popup-content>
            <dx-scroll-view width="100%" height="100%">
              <dx-form
                :col-count="1"
                :form-data="vars.formData"
                :show-colon-after-label="false"
                :on-initialized="evt => methods.onInitialized(evt, 'formEditItem')"
              >
                <template #image-template="{}">
                  <div class="form-image">
                    <img class="item-image" alt="" v-if="vars.formData.item_img" :src="vars.itemImage.value" />
                  </div>
                </template>
                <dx-group-item :col-count="4">
                  <dx-group-item :col-span="2" :col-count="2">
                    <dx-group-item :col-span="1">
                      <dx-simple-item template="image-template" />
                      <dx-simple-item
                        item-type="button"
                        horizontal-alignment="left"
                        :button-options="generateItemButtonOption('', methods.saveCompany, 'after', {
                          text: '이미지 변경',
                          type: 'default',
                          width: '90%',
                          onClick: methods.onClickAddImage,
                        })"
                      ></dx-simple-item>
                    </dx-group-item>
                    <dx-group-item :col-span="1" :col-count="1">
                      <dx-simple-item data-field="item_code" :col-span="1" :editor-options="{ readOnly: vars.item.readOnly }">
                        <dx-label text="품목코드" :show-colon="false" />
                        <dx-required-rule message="품목코드를 입력하세요" />
                        <dx-async-rule
                          message="이미 존재하는 품목코드입니다"
                          :validation-callback="methods.itemCodeValidation"
                        />
                      </dx-simple-item>
                      <dx-simple-item
                        data-field="main_category"
                        editor-type="dxSelectBox"
                        :editor-options="{
                          dataSource: vars.dataSource.main_category,
                          displayExpr: 'code_name',
                          valueExpr: 'code_name',
                        }"
                      >
                        <dx-label text="대분류" :show-colon="false" />
                      </dx-simple-item>
                      <dx-simple-item
                        data-field="asset_type"
                        editor-type="dxSelectBox"
                        :editor-options="{
                          dataSource: vars.dataSource.asset_type,
                          displayExpr: 'code_name',
                          valueExpr: 'code_name',
                        }"
                      >
                        <dx-label text="자산구분" :show-colon="false" />
                        <dx-required-rule message="자산구분을 입력하세요" />
                      </dx-simple-item>
                      <dx-simple-item
                        data-field="safety_stock"
                        editor-type="dxNumberBox"
                        :col-span="1"
                        :editor-options="{
                          format: 'fixedPoint',
                        }"
                      >
                        <dx-label text="안전재고" :show-colon="false" />
                      </dx-simple-item>
                      <dx-simple-item data-field="import_check" :col-span="1" editor-type="dxCheckBox">
                        <dx-label text="수입검사" :show-colon="false" />
                      </dx-simple-item>
                    </dx-group-item>
                    <dx-group-item :col-span="2" :col-count="2">
                      <dx-simple-item data-field="item_detail" :col-span="2"
                        :editor-options="generateItemButtonOption('rename', methods.createPopupFn('item_detail', '품목설명'))"
                      >
                        <dx-label text="품목설명" :show-colon="false" />
                      </dx-simple-item>
                      <dx-simple-item data-field="hs_code" :col-span="2">
                        <dx-label text="HS Code" :show-colon="false" />
                      </dx-simple-item>
                      <dx-simple-item data-field="note1" :col-span="2">
                        <dx-label text="참고1" :show-colon="false" />
                      </dx-simple-item>
                      <dx-simple-item data-field="note2" :col-span="2">
                        <dx-label text="참고2" :show-colon="false" />
                      </dx-simple-item>
                      <dx-simple-item data-field="etc" :col-span="2"
                        :editor-options="generateItemButtonOption('rename', methods.createPopupFn('etc', '비고'))"
                      >
                        <dx-label text="비고" :show-colon="false" />
                      </dx-simple-item>
                    </dx-group-item>
                  </dx-group-item>
                  <dx-group-item :col-span="2" :col-count="2">
                    <dx-simple-item data-field="item_name" :col-span="1">
                      <dx-label text="품명" :show-colon="false" />
                      <dx-required-rule message="품명을 입력하세요" />
                    </dx-simple-item>
                    <dx-simple-item data-field="item_standard" :col-span="1">
                      <dx-label text="규격" :show-colon="false" />
                    </dx-simple-item>
                     <dx-simple-item 
                     data-field="item_group"
                     editor-type="dxSelectBox" 
                      :editor-options="{
                        dataSource: vars.dataSource.item_group,
                        displayExpr: 'code_name',
                        valueExpr: 'code_name',
                      }"
                     >
                      <dx-label text="품목 그룹" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item data-field="client.alias" :editor-options="{
                  ...generateItemButtonOption('search', methods.createPopupFn('client_alias', '제조사')),
                }">
                      <dx-label text="제조사" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item
                      data-field="middle_category"
                      editor-type="dxSelectBox" 
                      :visible="false" 
                      :editor-options="{
                        dataSource: vars.dataSource.middle_category,
                        displayExpr: 'code_name',
                        valueExpr: 'code_name',
                        onValueChanged: methods.onMiddleCategoryChanged,
                      }"
                    >
                      <dx-label text="중분류" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item
                      data-field="sub_category"
                      editor-type="dxSelectBox"
                      :visible="false" 
                      :editor-options="{
                        dataSource: vars.dataSource.sub_category,
                        displayExpr: 'code_name',
                        valueExpr: 'code_name',
                      }"
                    >
                      <dx-label text="소분류" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item
                      data-field="moq"
                      editor-type="dxNumberBox"
                      :col-span="1"
                      :editor-options="{
                        format: 'fixedPoint',
                      }"
                    >
                      <dx-label text="MOQ" :show-colon="false" />
                    </dx-simple-item>

                    <dx-simple-item
                      data-field="unit"
                      editor-type="dxSelectBox"
                      :editor-options="{
                        dataSource: vars.dataSource.unit,
                        displayExpr: 'code_name',
                        valueExpr: 'code_name',
                      }"
                    >
                      <dx-label text="단위" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item
                      data-field="packing_quantity"
                      editor-type="dxNumberBox"
                      :col-span="1"
                      :editor-options="{ format: 'fixedPoint' }"
                    >
                      <dx-label text="포장단위수량" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item
                      data-field="transfer_quantity"
                      editor-type="dxNumberBox"
                      :col-span="1"
                      :editor-options="{ format: 'fixedPoint' }"
                    >
                      <dx-label text="이송단위수량" :show-colon="false" />
                    </dx-simple-item>

                    <dx-group-item :col-count="2">
                      <dx-simple-item data-field="shipment_check" :col-span="1" editor-type="dxCheckBox">
                        <dx-label text="출하검사" :show-colon="false" location="right" />
                      </dx-simple-item>
                      <dx-simple-item data-field="lot_check" :col-span="1" editor-type="dxCheckBox">
                        <dx-label text="LOT관리" :show-colon="false" location="right" />
                      </dx-simple-item>
                    </dx-group-item>
                    
                    <dx-simple-item data-field="delivery_date" :col-span="1">
                      <dx-label text="표준납기일" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item data-field="sales_price" editor-type="dxNumberBox" :col-span="1" :editor-options="{ format: 'currency' }">
                      <dx-label text="매출단가" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item data-field="purchase_price" editor-type="dxNumberBox" :col-span="1"
                      :editor-options="{ format: {type: 'currency', precision: 2} }"
                    >
                      <dx-label text="매입단가" :show-colon="false" />
                    </dx-simple-item>

                    <dx-simple-item data-field="before_item_code" :col-span="1">
                      <dx-label text="변경전 품목코드" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item data-field="after_item_code" :col-span="1">
                      <dx-label text="변경후 품목코드" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item data-field="end_of_use" :col-span="1" editor-type="dxCheckBox">
                      <dx-label text="사용종료" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item
                      data-field="end_date"
                      editor-type="dxDateBox"
                      :col-span="1"
                      :editor-options="{ dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss' }"
                    >
                      <dx-label text="종료일자" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item
                      data-field="register_id"
                      :editor-options="{ readOnly: true }"
                    >
                      <dx-label text="최초등록자" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item
                      data-field="created"
                      editor-type="dxDateBox"
                      :col-span="1"
                      :editor-options="{
                        readOnly: true,
                        dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                      }"
                    >
                      <dx-label text="최초등록일자" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item
                      data-field="modify_id"
                      :editor-options="{ readOnly: true }"
                    >
                      <dx-label text="최종수정자" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item
                      data-field="modify_date"
                      editor-type="dxDateBox"
                      :col-span="1"
                      :editor-options="{
                        readOnly: true,
                        dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                      }"
                    >
                      <dx-label text="최종수정일자" :show-colon="false" />
                    </dx-simple-item>
                  </dx-group-item>
                </dx-group-item>
                <dx-group-item :visible="vars.formData.item_group == 'LED 모듈'" :col-count="4">
                  <dx-simple-item data-field="color_type">
                      <dx-label text="지원색상" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item data-field="dot_number">
                      <dx-label text="Dot 구성" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item data-field="dot_pitch">
                      <dx-label text="Dot Pitch" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item data-field="module_size">
                      <dx-label text="모듈크기" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item data-field="dot_size">
                      <dx-label text="필셀 수" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item data-field="drive_mode">
                      <dx-label text="구동 모드" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item data-field="in_out_point">
                      <dx-label text="적용장소" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item data-field="brightness">
                      <dx-label text="밝기(cd/m2)" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item data-field="watt">
                      <dx-label text="소비전력" :show-colon="false" />
                    </dx-simple-item>
                </dx-group-item>
                <dx-group-item :visible="!!vars.formData.id">
                  <dx-tabbed-item>
                    <dx-tab-panel-options :defer-rendering="false" />
                    <dx-tab title="거래처 품목코드">
                      <dx-data-grid
                        class="fixed-header-table"
                        height="420px"
                        column-resizing-mode="widget"
                        :show-borders="true"
                        :column-auto-width="true"
                        :remote-operations="true"
                        :allow-column-resizing="true"
                        :data-source="vars.clientItem"
                        :on-initialized="evt => methods.onInitialized(evt, 'gridClientItem')"
                        @saving="methods.onSavingClientItem"
                      >
                        <dx-grid-toolbar>
                          <dx-item name="addRowButton" template="addButton" />
                          <dx-item name="saveButton" />
                          <dx-item name="revertButton" />
                        </dx-grid-toolbar>
                        <template #addButton>
                          <dx-button icon="add" @click="methods.showAddClientPopup" />
                        </template>
                        <dx-column caption="주공급업체" data-field="main_supplier" data-type="boolean" :allow-editing="true" :visible-index="0"/>
                        <dx-column caption="거래처명" data-field="client.name" :allow-editing="false" />
                        <dx-column caption="거래처품번" data-field="client_item_code" />
                        <dx-column caption="단가구분" data-field="unit_price_type">
                          <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.dataSource.unit_price_type" />
                        </dx-column>
                        <dx-column caption="단가" data-field="unit_price" data-type="number" :format="',##0.00000'" />
                        <dx-column caption="참고" data-field="note" />
                        <dx-column caption="등록일자" data-field="created" data-type="date" format="yyyy-MM-dd" :allow-editing="false" :sort-index="0" sort-order="desc" />
                        <dx-column caption="비고" data-field="etc" />
                        <dx-column caption="거래처ID" data-field="client_id" :visible="false" />
                        <dx-column caption="품목코드" data-field="item_code" :visible="false" />
                        <dx-column caption="회사ID" data-field="fk_company_id" :visible="false" />
                        
                        <dx-editing mode="batch"
                          :use-icons="true"
                          :allow-adding="true"
                          :allow-updating="true"
                          :allow-deleting="true"
                        >
                        </dx-editing>
                      </dx-data-grid>
                    </dx-tab>

                    <dx-tab title="단가이력정보">
                      <dx-data-grid
                        class="fixed-header-table"
                        height="420px"
                        column-resizing-mode="widget"
                        :data-source="vars.releaseItemByRank"
                        :remote-operations="true"
                        :show-borders="true"
                        :allow-column-resizing="true"
                        :column-auto-width="true"
                      >
                        <dx-column caption="출고단가" data-field="unit_price"  data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
                        <dx-column caption="출고수량" data-field="release_quantity" data-type="number" format="fixedPoint" />
                        <dx-column caption="출고번호" data-field="release.release_number" />
                        <dx-column caption="출고일자" data-field="release.release_date" data-type="date" format="yyyy-MM-dd" />
                        <dx-column caption="고객업체" data-field="release.client_company" />
                        <dx-column caption="영업부서" data-field="release.release_department" />
                        <dx-column caption="영업담당" data-field="release.release_manager" />

                        <dx-paging :page-size="20" />
                      </dx-data-grid>
                    </dx-tab>

                    <dx-tab title="창고별재고">
                      <dx-data-grid
                        class="fixed-header-table"
                        height="420px"
                        column-resizing-mode="widget"
                        :data-source="vars.stock"
                        :remote-operations="true"
                        :show-borders="true"
                        :allow-column-resizing="true"
                        :column-auto-width="true"
                      >
                        <dx-column caption="창고명" data-field="warehouse.wh_name" />
                        <dx-column caption="현재고" data-field="current_stock" data-type="number" format="fixedPoint" />
                        <dx-column caption="할당재고" data-field="assign_stock" data-type="number" format="fixedPoint" />
                        <dx-column caption="가용재고" data-field="available_stock" data-type="number" format="fixedPoint" />
                        
                        <dx-paging :page-size="20" />
                      </dx-data-grid>
                    </dx-tab>

                    <dx-tab title="도면관리">
                      <dx-data-grid
                        class="fixed-header-table"
                        height="420px"
                        date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                        column-resizing-mode="widget"
                        :data-source="vars.design"
                        :show-borders="true"
                        :remote-operations="true"
                        :column-auto-width="true"
                        :allow-column-resizing="true"
                        @saving="methods.onSavingItemCode"
                        @focused-cell-changed="methods.onFocusedDesignChanged"
                      >
                        <dx-column caption="도면번호" data-field="design_number" />
                        <dx-column caption="등록일" data-field="registration_date" data-type="date" format="yyyy-MM-dd" />
                        <dx-column caption="설변구분" data-field="design_type">
                          <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.dataSource.design_type" />
                        </dx-column>
                        <dx-column caption="설변사항" data-field="note" />
                        <dx-column caption="도면파일첨부" data-field="design_file_name" cell-template="download" edit-cell-template="upload" />
                        <dx-column caption="도면파일" data-field="design_file" :visible="false" />
                        
                        <dx-paging :page-size="20" />
                        <dx-editing mode="row"
                          :use-icons="true"
                          :allow-adding="true"
                          :allow-updating="true"
                          :allow-deleting="true"
                        >
                        </dx-editing>

                        <template #download="{data}">
                          <a :href="data.data[data.column.dataField]" download>{{data.data[data.column.dataField]}}</a>
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
                    </dx-tab>
                    
                    <dx-tab title="BOM 역전개">
                      <dx-data-grid
                        class="fixed-header-table"
                        height="420px"
                        column-resizing-mode="widget"
                        :data-source="vars.bomTreeReverse"
                        :remote-operations="true"
                        :show-borders="true"
                        :column-auto-width="true"
                      >
                        <dx-column caption="주품목" data-field="root_item_name" />
                        <dx-column caption="주품목(모델)" data-field="root_item_code" />
                        <dx-column caption="소요량" data-field="requirement" />
                        <dx-column caption="모품목" data-field="parent_item_name" />
                        <dx-column caption="모품목(모델)" data-field="parent_item_code" />
                        <dx-export :enabled="true" />
                      </dx-data-grid>
                    </dx-tab>

                  </dx-tabbed-item>
                </dx-group-item>
              </dx-form>
            </dx-scroll-view>
          </template>
        </dx-popup>

        <dx-popup
          id="popup"
          content-template="popup-content"
          v-model:visible="vars.addImage.visible"
          :close-on-outside-click="true"
          :show-close-button="false"
          :show-title="false"
          :width="350"
          :height="350"
        >
          <template #popup-content>
            <div class="widget-container flex-box">
              <div
                id="dropzone-external"
                class="flex-box"
                :class="[
                  vars.imageUpload.isDropZoneActive
                    ? 'dx-theme-accent-as-border-color dropzone-active'
                    : 'dx-theme-border-color',
                ]"
              >
                <img id="dropzone-image" alt="" v-if="vars.formData.item_img" :src="vars.itemImage.value" />
                <div id="dropzone-text" class="flex-box" v-if="vars.imageUpload.textVisible">
                  <span>새로운 이미지를 끌어다 놓으세요.</span>
                </div>
              </div>
              <dx-file-uploader
                id="file-uploader"
                dialog-trigger="#dropzone-external"
                drop-zone="#dropzone-external"
                :multiple="false"
                :allowed-file-extensions="vars.imageUpload.allowedFileExtensions"
                upload-mode="useButtons"
                :visible="false"
                @drop-zone-enter="methods.onDropZoneEnter"
                @drop-zone-leave="methods.onDropZoneLeave"
                @value-changed="methods.onValueChangedImage($event)"
              />
            </div>
          </template>
        </dx-popup>

        <dx-popup
          id="popup"
          content-template="popup-content"
          v-model:visible="vars.addDesign.visible"
          :close-on-outside-click="true"
          :show-close-button="false"
          :show-title="false"
          :width="350"
          :height="350"
        >
          <template #popup-content>
            <div class="widget-container flex-box">
              <div
                id="dropzone-external"
                class="flex-box"
                :class="[
                  vars.designUpload.isDropZoneActive
                    ? 'dx-theme-accent-as-border-color dropzone-active'
                    : 'dx-theme-border-color',
                ]"
              >
                <img id="dropzone-image" alt="" v-if="vars.designUpload.img" :src="vars.designImage.value" />
                <div id="dropzone-text" class="flex-box" v-if="vars.designUpload.textVisible">
                  <span>새로운 이미지를 끌어다 놓으세요.</span>
                </div>
              </div>
              <dx-file-uploader
                id="file-uploader"
                upload-mode="useButtons"
                drop-zone="#dropzone-external"
                dialog-trigger="#dropzone-external"
                :multiple="false"
                :visible="false"
                :allowed-file-extensions="vars.designUpload.allowedFileExtensions"
                @drop-zone-enter="methods.onDesignDropZoneEnter"
                @drop-zone-leave="methods.onDesignDropZoneLeave"
                @value-changed="methods.onValueChangedDesign($event)"
              />
            </div>
          </template>
        </dx-popup>

        <dx-popup
          v-model:visible="vars.addClient.visible"
          content-template="popup-content"
          title="거래처찾기"
          :close-on-outside-click="true"
          :width="680"
          :height="460"
          :resize-enabled="true"
          @initialized="evt => methods.onInitialized(evt, 'popupClient')"
        >
          <dx-toolbar-item
            widget="dxButton"
            toolbar="top"
            location="after"
            :options="{ text: '선택된 항목 추가', icon: 'add', onClick: methods.addClients }"
          />

          <template #popup-content>
            <dx-data-grid
              column-resizing-mode="widget"
              :on-initialized="evt => methods.onInitialized(evt, 'gridClient')"
              :data-source="vars.client"
              :show-borders="true"
              :allow-column-reordering="true"
              :allow-column-resizing="true"
              :column-auto-width="true"
              :remote-operations="true"
            >
              <dx-column caption="업체명" data-field="name" />
              <dx-column caption="업체약칭" data-field="alias" />
              <dx-column caption="법인번호" data-field="corp_number" />
              <dx-column caption="사업자번호" data-field="business_number" />
              <dx-column caption="대표자명" data-field="ceo_name" />

              <dx-paging :page-size="20" />
              <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick" />
              <dx-filter-row :visible="true" />
            </dx-data-grid>
          </template>
        </dx-popup>

        <dx-popup
          content-template="popup-content"
          v-model:visible="vars.printQr.visible"
          :close-on-outside-click="true"
          :show-close-button="false"
          :show-title="false"
          :width="650"
          :height="300"
          @initialized="evt => methods.onInitialized(evt, 'multiuse-popup')"
        >
          <dx-toolbar-item location="after" widget="dxButton" :options="{icon: 'close', text: '닫기', onClick: methods.closeQRLabel}" />
          <dx-toolbar-item location="after" widget="dxButton" :options="{icon: 'print', text: '확인', onClick: methods.printQRLabel}" />
          <template #popup-content>
            <dx-form :form-data="vars.printQr" :col-count="2">
              <dx-simple-item>
                <template #default>
                  <img class="qr-image" :src="vars.printQr.image" />
                </template>
              </dx-simple-item>
              <dx-group-item>
                <dx-simple-item>
                  <template #default>품목코드: {{vars.formData.item_code}}</template>
                </dx-simple-item>
                <dx-simple-item>
                  <template #default>품목이름: {{vars.formData.item_name}}</template>
                </dx-simple-item>
                <dx-simple-item data-field="text"
                  :editor-options="{
                    buttons: [{
                      name: 'refresh',
                      location: 'after',
                      options: { icon: 'refresh', onClick: methods.refreshQRImage }
                    }]
                  }">
                  <dx-label text="추가입력" />
                </dx-simple-item>
                <dx-simple-item data-field="quantity" editor-type="dxNumberBox"
                  :editor-options="{ showSpinButtons: true }">
                  <dx-label text="인쇄수량" />
                </dx-simple-item>
              </dx-group-item>
            </dx-form>
          </template>
        </dx-popup>

        <dx-popup
          v-model:visible="vars.dlg.show"
          content-template="popup-content"
          :title="vars.dlg.title"
          :close-on-outside-click="false"
          :width="680" :height="600"
          :key="vars.dlg.key"
          :resize-enabled="true"
        >
          <template #popup-content>
            <div v-if="vars.dlg.key === 'etc'">
              <dx-text-area :height="'calc(100% - 50px)'" v-model="vars.formData.etc" />
              <div class="popup-footer">
                <dx-button text="저장" type="default" icon="save" @click="methods.setGridValue('etc') "/>
              </div>
            </div>
            <div v-else-if="vars.dlg.key === 'item_detail'">
              <dx-text-area :height="'calc(100% - 50px)'" v-model="vars.formData.item_detail" />
              <div class="popup-footer">
                <dx-button text="저장" type="default" icon="save" @click="methods.setGridValue('item_detail') "/>
              </div>
            </div>
            <data-grid-client v-else-if="vars.dlg.key === 'client_alias'" :filters="vars.dlg.data" @change="methods.finderReturnHandler" />
          </template>
        </dx-popup>
      </div>
    </div>
    <input
      hidden
      type="file"
      ref="excelRef"
      accept=".xlsx,.xls"
      @change="methods.excelFileChange"
    />

    <popup-item-detail
      v-model:visible="vars.itemDetail.visible"
      :item-id="vars.itemDetail.id"
    />
  </div>
</template>

<script>
import { alert } from 'devextreme/ui/dialog';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxDataGrid, DxColumn, DxPaging, DxLookup, DxEditing, DxFilterRow, DxSelection, DxColumnChooser, 
DxButton as DxGridButton, DxToolbar as DxGridToolbar, DxExport } from 'devextreme-vue/data-grid';
import { DxButton } from 'devextreme-vue/button';
import { DxTextBox, DxButton as DxTextBoxButton } from 'devextreme-vue/text-box'
import { DxNumberBox } from 'devextreme-vue/number-box'
import DxTextArea from 'devextreme-vue/text-area'
import { DxScrollView } from 'devextreme-vue/scroll-view';
import { DxFileUploader } from 'devextreme-vue/file-uploader';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxForm, DxTab, DxLabel, DxAsyncRule, DxGroupItem, DxSimpleItem, DxTabbedItem, DxRequiredRule, DxTabPanelOptions } from 'devextreme-vue/form';
import { notifyInfo, notifyError } from '../../utils/notify';
import {
  baseItem,
  getBaseItem,
  baseCodeLoader,
  getBaseCode,
  baseBom,
  baseBomLink,
  getBaseClient,
  getBaseClientItem,
  getBaseDesign,
} from '../../data-source/base';
import {
  getShipmentReleaseItem,
  getShipmentReleaseItemByRank
} from '../../data-source/shipment';
import { getSetupBasicStock } from '../../data-source/setup';
import { setupGroup } from '../../data-source/setup';
import { ref, reactive, onMounted, nextTick, computed } from 'vue';
import authService from '../../auth';
import stateStore from '@/utils/state-store';
import { generateItemButtonOption } from '../../utils/util';
import ApiService from '../../utils/api-service';
import { saveAs } from 'file-saver';
import QRCode from 'qrcode'
import printDocument from '@/utils/print-document'
import PopupItemDetail from '@/components/base/popup-item-detail';
import moment from 'moment';
import DataGridClient from '@/components/base/data-client.vue';

export default {
  components: {
    DxToolbar,
    DxGridToolbar,
    DxExport,
    DxItem,
    DxForm,
    DxLabel,
    DxGroupItem,
    DxSimpleItem,
    DxPopup,
    DxToolbarItem,
    DxDataGrid,
    DxSelection,
    DxColumn,
    DxEditing,
    DxPaging,
    DxColumnChooser,
    DxLookup,
    DxTabbedItem,
    DxTabPanelOptions,
    DxTab,
    DxAsyncRule,
    DxRequiredRule,
    DxFilterRow,
    DxScrollView,
    DxFileUploader,
    DxButton,
    DxGridButton,
    DxNumberBox,
    DxTextBox,
    PopupItemDetail,
    DxTextArea,
    DxTextBoxButton,
    DataGridClient
  },
  setup() {
    const excelRef = ref(null);
    const apiService = new ApiService('/api/mes/v1/excel/base/item');
    const uploadService = new ApiService('/api/mes/v1/mail-attachment');
    const bomTreeReverseService = new ApiService('/api/mes/v1/base/bom-reversal')
    
    const vars = {};
    vars.excelRef = ref(null);
    vars.formData = reactive({});
    vars.addItem = reactive({
      visible: false,
    });
    vars.addImage = reactive({
      visible: false,
    });
    vars.addDesign = reactive({
      visible: false,
    });
    vars.addClient = reactive({
      visible: false,
    });
    vars.printQr = reactive({
      visible: false,
      image: null,
      text: '',
      quantity: 1
    });
    vars.dataSource = reactive({
      asset_type: [],
      unit: [],
      unit_price_type: [],
      main_category: [],
      item_group: [],
      middle_category: [],
      sub_category: [],
      middle_category_all: [],
      sub_category_all: [],
      design_type: [],
    });
    vars.imageUpload = reactive({
      textVisible: true,
      popupVisible: false,
      isDropZoneActive: false,
      allowedFileExtensions: ['.jpg', '.jpeg', '.gif', '.png'],
    });
    vars.designUpload = reactive({
      textVisible: true,
      popupVisible: false,
      isDropZoneActive: false,
      allowedFileExtensions: ['.jpg', '.jpeg', '.gif', '.png'],
      img: ''
    });
    vars.baseItem = getBaseItem([
      { name: 'fk_company_id', op: 'eq', val: authService.getCompanyId() },
    ]);
  
    vars.baseItem.transform = (item) => {
      item.purchase_price = parseFloat(item.purchase_price)
      item.sales_price = parseFloat(item.sales_price)
    }
    vars.dlg = reactive({ show: false, title: '', key: null, data: null, });
    vars.stock = null;
    vars.design = null;
    vars.client = null;
    vars.clientItem = null;
    vars.releaseItem = null;
    vars.releaseItemByRank = null;
    vars.bomTreeReverse = null;

    vars.component = {};
    vars.item = reactive({
      readOnly: false,
    });
    vars.focus = {
      design: null
    }
    vars.itemImage = computed(() => {
      if (!vars.formData.item_img) return null;
      if (vars.formData.item_img.startsWith('data:'))
        return vars.formData.item_img;
      return `/api/mes/v1/base/item-image/${vars.formData.item_img}`;
    });
    vars.itemDetail = reactive({ visible: false, id: 0 });
    vars.designImage = computed(() => {
      if (!vars.designUpload.img) return null;
      if (vars.designUpload.img.startsWith('data:'))
        return vars.designUpload.img;
      return `/api/mes/v1/base/item-image/${vars.designUpload.img}`;
    });

    const attchFiles = {}

    onMounted(() => {
      methods.loadBaseCode();

      vars.client = getBaseClient([
        { name: 'fk_company_id', op: 'eq', val: authService.getCompanyId() },
      ]);
    });
    // Methods
    const methods = {
      onInitialized(e, key) {
        vars.component[key] = e.component;
        if (key.includes('grid') && !['gridClientItem'].includes(key)) {
          stateStore.bind(key, e.component);
        }
      },
      showAddItemPopup() {
        vars.addItem.visible = true;
      },
      showAddClientPopup() {
        if (vars.component.gridClient) {
          vars.component.gridClient.deselectAll();
          vars.component.gridClient.refresh().then(function() {
            vars.addClient.visible = true;
          });
        } else {
          vars.addClient.visible = true;
        }
      },
      hideAddClientPopup() {
        vars.addClient.visible = false;
      },
      async addClients() {
        const rows = await vars.component.gridClient.getSelectedRowsData();

        for (let row of rows) {
          await vars.component.gridClientItem.addRow();
          vars.component.gridClientItem.cellValue(0, 'client.name', row.name);
          vars.component.gridClientItem.cellValue(0, 'client_id', row.id);
          vars.component.gridClientItem.cellValue(
            0,
            'item_code',
            vars.formData.item_code
          );
          vars.component.gridClientItem.cellValue(
            0,
            'fk_company_id',
            authService.getCompanyId()
          );
          vars.component.gridClientItem.cellValue(0, 'created', new Date());
        }
        methods.hideAddClientPopup();
      },
      onClickAddImage() {
        vars.addImage.visible = true;
      },
      onClickAddDesign() {
        vars.designUpload.img = null;
        
        const design = vars.focus.design.component.cellValue(
          vars.focus.design.rowIndex,
          'design_file',
        );
        if (design) {
          vars.designUpload.img = design;
        }
        
        vars.designUpload.textVisible = true,
        vars.designUploadpopupVisible = false,
        vars.designUploadisDropZoneActive = false,
        vars.addDesign.visible = true;
      },
      onFocusedDesignChanged(e) {
        vars.focus.design = e;
      },
      async onMainCategoryChanged(e) {
        vars.formData.middle_category = null;
        vars.formData.sub_category = null;
        await methods.loadMiddleCategory(e.value);
        if (vars.component.formEditItem) vars.component.formEditItem.repaint();
      },
      async onMiddleCategoryChanged(e) {
        vars.formData.sub_category = null;
        await methods.loadSubCategory(e.value);
        if (vars.component.formEditItem) vars.component.formEditItem.repaint();
      },
      loadMiddleCategory(main_category) {
        return baseCodeLoader([main_category]).then(response => {
          vars.dataSource.middle_category = response[main_category];
        });
      },
      loadSubCategory(middle_category) {
        return baseCodeLoader([middle_category]).then(response => {
          vars.dataSource.sub_category = response[middle_category];
        });
      },
      loadBaseCode() {
        return baseCodeLoader(
          ['자산구분', '단위', '품목분류', '단가구분', '설변구분', '품목그룹'],
          authService.getCompanyId()
        ).then(response => {
          vars.dataSource.asset_type = response['자산구분'];
          vars.dataSource.unit = response['단위'];
          vars.dataSource.main_category = response['품목분류'];
          vars.dataSource.unit_price_type = response['단가구분'];
          vars.dataSource.design_type = response['설변구분'];
          vars.dataSource.item_group = response['품목그룹'];

          let middleFilter = [];
          vars.dataSource.main_category.forEach(item => {
            middleFilter.push({
              name: 'parent_code_id',
              op: 'eq',
              val: item.id,
            });
          });
          vars.dataSource.main_category.sort(function(a, b) {
            const upperA = a.code_name.toUpperCase();
            const upperB = b.code_name.toUpperCase();

            if (upperA > upperB) return 1;
            if (upperA < upperB) return -1;
            if (upperA == upperB) return 0;
          });

          const middleCategory = getBaseCode([{ or: middleFilter }]);
          middleCategory.load().then(response => {
            vars.dataSource.middle_category_all = response.data;

            let subFilter = [];
            response.data.forEach(item => {
              subFilter.push({
                name: 'parent_code_id',
                op: 'eq',
                val: item.id,
              });
            });
            const subCategory = getBaseCode([{ or: subFilter }]);
            subCategory.load().then(response => {
              vars.dataSource.sub_category_all = response.data;
              // vars.component.gridItem.refresh();
            });
          });
        });
      },
      onDropZoneEnter(e) {
        if (e.dropZoneElement.id === 'dropzone-external') {
          vars.imageUpload.isDropZoneActive = true;
        }
      },
      onDropZoneLeave(e) {
        if (e.dropZoneElement.id === 'dropzone-external') {
          vars.imageUpload.isDropZoneActive = false;
        }
      },
      onValueChangedImage(e) {
        const reader = new FileReader();
        reader.onload = () => {
          vars.imageUpload.isDropZoneActive = false;
          vars.imageUpload.textVisible = false;
          vars.formData.item_img = reader.result;
        };
        reader.readAsDataURL(e.value[0]);
      },
      onDesignDropZoneEnter(e) {
        if (e.dropZoneElement.id === 'dropzone-external') {
          vars.designUpload.isDropZoneActive = true;
        }
      },
      onDesignDropZoneLeave(e) {
        if (e.dropZoneElement.id === 'dropzone-external') {
          vars.designUpload.isDropZoneActive = false;
        }
      },
      onValueChangedDesign(e) {
        const reader = new FileReader();
        reader.onload = () => {
          vars.designUpload.isDropZoneActive = false;
          vars.designUpload.textVisible = false;
          vars.designUpload.img = reader.result;
          
          vars.focus.design.component.cellValue(
            vars.focus.design.rowIndex,
            'design_file',
            vars.designUpload.img
          );
        };
        reader.readAsDataURL(e.value[0]);
      },
      clearFormData(){
        vars.formData.id = undefined
        vars.formData.item_code = '';
        vars.formData.item_name = '';
        vars.formData.item_standard = '';
        vars.formData.packing_quantity = 0;
        vars.formData.transfer_quantity = 0;
        vars.formData.main_category = '';
        vars.formData.middle_category = '';
        vars.formData.sub_category = '';
        vars.formData.delivery_date = '';
        vars.formData.asset_type = '';
        vars.formData.moq = 0;
        vars.formData.etc = '';
        vars.formData.import_check = false;
        vars.formData.shipment_check = false;
        vars.formData.lot_check = false;
        vars.formData.before_item_code = '';
        vars.formData.after_item_code = '';
        vars.formData.item_detail = '';
        vars.formData.color_type = '';
        vars.formData.dot_number = '';
        vars.formData.dot_pitch = '';
        vars.formData.module_size = '';
        vars.formData.dot_size = '';
        vars.formData.drive_mode = '';
        vars.formData.in_out_point = '';
        vars.formData.brightness = '';
        vars.formData.watt = '';
        vars.formData.end_of_use = false;
        vars.formData.end_date = '';
        vars.formData.safety_stock = 0;
        vars.formData.unit = '';
        vars.formData.register_id = '';
        vars.formData.created = new Date();
        vars.formData.sales_price = 0;
        vars.formData.purchase_price = 0;
        vars.formData.cost_price = 0;
        vars.formData.modify_id = '';
        vars.formData.modify_date = '';
        vars.formData.note1 = '';
        vars.formData.note2 = '';
        vars.formData.item_img = '';
        vars.formData.client_company = '';
        vars.formData.item_group = '';
        vars.formData.fk_manufacturer_client_id = undefined;
        vars.formData.fk_company_id = authService.getCompanyId();
      },
      newItem() {
        methods.initImageUploader();
        methods.clearFormData();
        
        vars.item.readOnly = false;
        if (vars.component.formEditItem) {
          vars.component.formEditItem.repaint();
        }
        methods.showAddItemPopup();
      },
      async editItem(e) {
        methods.clearFormData();
        methods.initImageUploader();
        
        vars.formData.id = e.row.data.id;

        vars.stock = getSetupBasicStock([
          { name: 'item_code', op: 'eq', val: e.row.data.item_code },
          { name: 'fk_company_id', op: 'eq', val: authService.getCompanyId() },
        ]);
        vars.clientItem = getBaseClientItem([
          { name: 'item_code', op: 'eq', val: e.row.data.item_code },
          { name: 'fk_company_id', op: 'eq', val: authService.getCompanyId() },
        ]);
        vars.releaseItem = getShipmentReleaseItem([
          { name: 'item_code', op: 'eq', val: e.row.data.item_code },
        ])
        vars.releaseItemByRank = getShipmentReleaseItemByRank([
          { name: 'item_code', op: 'eq', val: e.row.data.item_code },
        ])
        vars.design = getBaseDesign([
          { name: 'item_code', op: 'eq', val: e.row.data.item_code },
        ])

        const {data: bomTreeReverseItems} = await bomTreeReverseService.get(String(e.row.data.id))
        vars.bomTreeReverse = bomTreeReverseItems

        const { data } = await baseItem.load({
          filter: [['id', '=', vars.formData.id]],
        });

        await methods.loadMiddleCategory(data[0].main_category);
        await methods.loadSubCategory(data[0].middle_category);
        
        await nextTick();
        Object.assign(vars.formData, data[0]);
        vars.formData.purchase_price = parseFloat(e.row.data.purchase_price);

        vars.item.readOnly = true;
        if (vars.component.formEditItem) {
          vars.component.formEditItem.repaint();
        }
        methods.showAddItemPopup();
      },
      async onClickItemSave() {
        if (!vars.formData.item_code || !vars.formData.item_name || !vars.formData.asset_type) {
          notifyError('필수 정보를 입력하세요');
          return;
        }

        try {
          const userId = authService._user.user_id;
          if (!vars.formData.register_id) {
            vars.formData.register_id = userId;
          }
          vars.formData.modify_id = userId;
          vars.formData.modify_date = new Date();
          delete vars.formData.client_company;
          if (vars.formData.id) {
            if (vars.component['gridClientItem'] && vars.component['gridClientItem'].hasEditData()) {
              await vars.component['gridClientItem'].saveEditData()
            }
            const params = {...vars.formData}
            delete params.client_item
            await baseItem.update(vars.formData.id, params);
          } else {
            await baseItem.insert(vars.formData);
          }
          notifyInfo('저장되었습니다');
          vars.itemDetail.id = null;
          vars.component.gridItem.refresh();
        } catch (ex) {
          console.error(ex);
          notifyError('저장 할 내용이 없습니다');
        }
      },
      initImageUploader() {
        vars.imageUpload.textVisible = true;
        vars.imageUpload.popupVisible = false;
        vars.imageUpload.isDropZoneActive = false;
      },
      newClient() {},
      createPopupFn(key, title, data = null) {
        const _key = key, _title = title, _data = data;
        return () => {
          vars.dlg.key = _key;
          vars.dlg.data = _data;
          vars.dlg.title = _title;
          vars.dlg.show = true;
        };
      },
      excelUpload() {
        excelRef.value.click();
      },
      async excelFileChange({ target }) {
        if (!target.files.length) return;

        vars.component.gridItem.beginCustomLoading(
          '엑셀 데이터를 읽고 있습니다'
        );
        const fd = new FormData();
        fd.append('file', target.files[0]);

        try {
          await apiService.post('', fd);
          vars.component.gridItem.refresh();
        } catch (ex) {
          if (ex.response.data) {
            notifyError(ex.response.data);
          }
        } finally {
          vars.component.gridItem.endCustomLoading();
          target.value = null;
        }
      },
      excelSampleDownload() {
        saveAs('/api/mes/v1/excel/base/item', '품목입력양식.xlsx');
      },
      refreshQRImage() {
        const code = [
          vars.formData.item_code,
          vars.formData.item_name,
          vars.printQr.text
        ].join('|')

        QRCode.toDataURL(code, {margin: 0}, (err, url) => {
          if (err) return alert(err.message)
          vars.printQr.image = url
        })
      },
      prepareQRLabel() {
        vars.printQr.visible = true
        methods.refreshQRImage()
      },
      closeQRLabel() {
        vars.printQr.visible = false
        vars.printQr.image = null
        vars.printQr.text = ''
        vars.printQr.quantity = 1
      },
      printQRLabel() {
        const params = {paper: '20x20mm', label: '2x2', items: []}
        for (let i=0; i<vars.printQr.quantity; i++) {
          params.items.push({
            qr: vars.printQr.image
          })
        }
        printDocument('qr', params)
      },
      onSavingClientItem(e) {
        const rows = e.component.getVisibleRows()
        const count = rows.reduce((t, i) => t = t + (i.data.main_supplier ? 1 : 0), 0)
        if (count !== 1) {
          e.cancel = true
          if (count === 0) notifyError('주공급업체 지정해 주세요')
          else notifyError('주공급업체는 하나만 설정할 수 있습니다')
        }
        else {
          e.changes.forEach(element => {
            if (element.type != 'remove') {
              delete element.data.client;
            }
          });
        }
      },
      async updateUploadFile (element) {
        for (const key in element.data) {
          console.log(`${key} / ${element.data[key]} / ${typeof element.data[key]}`)

          if (!(element.data[key] instanceof Date) && typeof element.data[key] === 'object') delete element.data[key]
          else if (attchFiles[key]) {
          // if (element.data[key] instanceof File) {
            const fd = new FormData()
            fd.append('file', attchFiles[key], attchFiles[key].name)
            const {data: filename} = await uploadService.post('', fd)
            element.data[key] = `/api/mes/v1/mail-attachment/${filename}`
            delete attchFiles[key]
            console.log(element.data)
          }
        }
      },
      async onSavingItemCodeImpl (e) {
        for (const element of e.changes) {
          console.log(JSON.stringify(element))
          switch (element.type) {
            case 'insert': {
              element.data.item_code = vars.formData.item_code;
              element.data.fk_item_id = vars.formData.id;
              await methods.updateUploadFile(element)
              break
            }
            case 'update': {
              await methods.updateUploadFile(element)
              break
            }
            default: {
              console.log(element.type)
            }
          }
        }
      },
      onSavingItemCode(e) {
        console.log('onSavingItemCode', e)
        e.promise = methods.onSavingItemCodeImpl(e)
      },
      itemCodeDuplicationCheck(itemCode) {
        return new Promise((resolve) => {
          try {
            baseItem.load({ filter: ['item_code', '=', itemCode] }).then((res) => {
              if (res.data && res.data.length > 0) {
                resolve(false);
              } else {
                resolve(true);
              }
            });
          } catch(ex) {
            resolve(false);
          }
        });
      },
      itemCodeValidation(params) {
        return methods.itemCodeDuplicationCheck(params.value)
      },
      itemPopupClick({ column, data }) {
        if (column.name === 'item_code') {
          vars.itemDetail.id = data.id;
          vars.itemDetail.visible = true;
        }
      },
      addFile ({component, data, column, rowIndex}) {
        return () => {
          const f = document.createElement('input')
          f.type = 'file'
          f.onchange = () => {
            if (f.files[0]) {
              attchFiles[column.dataField] = f.files[0]
              component.cellValue(rowIndex, column.dataField, f.files[0].name)
            }
            f.onchange = undefined
            f.remove()
          }
          document.body.appendChild(f)
          f.click()
        }
      },
      async getBomTree (itemId) {
        const {data: boms} = await baseBom.load({ filter: ['item_id', '=', itemId] })
        if (boms.length) {
          const {data: links} = await baseBomLink.load({ filter: ['root_id', '=', boms[0].id], skip: 0, take: 1000 })
          return links
        }
        return []
      },
      async importFromBom () {
        if (!vars.component.hazard) return
        vars.component.hazard.beginCustomLoading('BOM 정보 읽는 중')
        const tree = await methods.getBomTree(vars.formData.id)
        
        for (const link of tree) {
          const {data: item} = await baseItem.byKey(link.child_bom.item_id) 
        }

        await vars.component.hazard.refresh()
        // vars.component.hazard.cellValue(0, 'item_code', vars.formData.item_code)
        // vars.component.hazard.cellValue(0, 'item.item_name', vars.formData.item_name)
        // vars.component.hazard.cellValue(0, 'item.item_standard', vars.formData.item_standard)
        // vars.component.hazard.cellValue(0, 'supply_company', '')
        // await vars.component.hazard.saveEditData()

        vars.component.hazard.endCustomLoading()
      },

      setGridValue (key) {
        if (vars.component['gridItem']) {
          const rowIndex = vars.formData.id
            ? vars.component['gridItem'].getRowIndexByKey(vars.formData.id)
            : 0
          vars.component['gridItem'].cellValue(rowIndex, key, vars.formData[key]);
          console.log(`update date: ${vars.formData.id}, ${key}, ${vars.formData[key]}`)
        }
        vars.dlg.show = false;
      },
      finderReturnHandler(data) {
        switch (vars.dlg.key) {
          case 'client_alias': {
            vars.formData.fk_manufacturer_client_id = data.id;
            vars.formData.client = data;
            break;
          }
        }

        vars.dlg.key = null;
        vars.dlg.data = null;
        vars.dlg.title = '';
        vars.dlg.show = false;
      },
      onDataError(e){
        if (e.error.response.status == 605) {
          e.error.message = '연결된 데이터가 있어서 삭제가 안됩니다';
          alert(`${e.error.response.data.message}<br/><br/>테이블에 연결된 데이터가 있어서 삭제가 안됩니다.<br/>데이터 삭제 후 다시 시도해 주세요.`, '삭제 오류');
        }
      },
      onExporting (evt) {
        baseItem.exportData(evt.component, '품목', `품목_${Date.now()}.xlsx`)
        evt.cancel = true
      },
      addItemOnHiding(evt){
        delete vars.formData.basic_stock;
        delete vars.formData.client_item;
        delete vars.formData.client;
        delete vars.formData.created;
      }
    };

    return {
      vars,
      excelRef,
      methods,
      setupGroup,
      baseItem,
      generateItemButtonOption,
    };
  },
};
</script>

<style lang="scss" scoped>
.form-image {
  height: 160px;
  width: 90%;
  border: 1px solid #d2d3d5;
  border-radius: 5%;
  background-size: 90%;
  background-repeat: no-repeat;
  background-position: center;
}
.item-image {
  height: 100%;
  width: 100%;
  border-radius: 5%;
  background-repeat: no-repeat;
  background-position: center;
}

.qr-image {
  width: 50%;
}
.popup-footer {
  margin-top: 10px;
  display: flex;
  justify-content: center;
}
</style>
