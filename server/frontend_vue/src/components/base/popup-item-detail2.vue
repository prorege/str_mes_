<template>
    <dx-popup
          title="품목관리"
          content-template="popup-content"
          width="70%"
          height="80%"
          :resize-enabled="true"
          :close-on-outside-click="true"
          :onHiding="methods.addItemOnHiding"
        >
          <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
            :options="{ text: '다름이름으로저장', icon: 'save', onClick: methods.onClickItemSaveAs }"
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
                :on-initialized="evt => methods.onInitialized(evt, 'form-edit-item')"
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
                      <dx-simple-item data-field="item_code" :col-span="1">
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
                    <dx-simple-item data-field="item_name" :col-span="1" editor-type="dxSelectBox" :editor-options="{
                        acceptCustomValue: true,
                        dataSource: vars.dataSource.item_name,
                        displayExpr: 'code_name',
                        valueExpr: 'code_name',
                    }">
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
                        :on-initialized="evt => methods.onInitialized(evt, 'grid-client-item')"
                        @saving="methods.onSavingClientItem"
                      >
                        <dx-grid-toolbar>
                          <dx-grid-item name="addRowButton" template="addButton" />
                          <dx-grid-item name="saveButton" />
                          <dx-grid-item name="revertButton" />
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
                        :on-initialized="evt => methods.onInitialized(evt, 'grid-release-item')"
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
                        :on-initialized="evt => methods.onInitialized(evt, 'grid-stock')"
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
                        :on-initialized="evt => methods.onInitialized(evt, 'grid-design')"
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
                        :on-initialized="evt => methods.onInitialized(evt, 'grid-bom-tree-reverse')"
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
                    <dx-button text="저장" type="default" icon="save" @click="methods.closePopup"/>
                  </div>
                </div>
                <div v-else-if="vars.dlg.key === 'item_detail'">
                  <dx-text-area :height="'calc(100% - 50px)'" v-model="vars.formData.item_detail" />
                  <div class="popup-footer">
                    <dx-button text="저장" type="default" icon="save" @click="methods.closePopup"/>
                  </div>
                </div>
                <data-grid-client v-else-if="vars.dlg.key === 'client_alias'" :filters="vars.dlg.data" @change="methods.finderReturnHandler" />
              </template>
            </dx-popup>
          </template>
          
        </dx-popup>

        
</template>

<script>
import { reactive, ref, computed, nextTick, watch, onMounted } from 'vue';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup'; 
import { DxScrollView } from 'devextreme-vue/scroll-view';
import { DxForm, DxSimpleItem, DxGroupItem, DxLabel, DxAsyncRule, DxRequiredRule, DxTabPanelOptions, DxTab, DxTabbedItem} from 'devextreme-vue/form';
import { DxDataGrid, DxToolbar as DxGridToolbar, DxItem as DxGridItem, DxColumn, DxLookup, DxEditing, DxPaging, DxExport } from 'devextreme-vue/data-grid';
import { DxButton } from 'devextreme-vue/button';
import { DxTextBox, DxButton as DxTextBoxButton } from 'devextreme-vue/text-box';
import DxTextArea from 'devextreme-vue/text-area'
import { generateItemButtonOption } from '../../utils/util';
import stateStore from '@/utils/state-store';
import { getSetupBasicStock } from '../../data-source/setup';
import {
  getShipmentReleaseItem,
  getShipmentReleaseItemByRank,
  shipmentQuoteItem
} from '../../data-source/shipment';
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
import DataGridClient from '@/components/base/data-client.vue';
import authService from '../../auth';
import ApiService from '../../utils/api-service';
import { notifyInfo, notifyError } from '../../utils/notify';
export default {
    props: {
        row:{
          type: Object,
          default: null,
        },
        quote_item_id:{
          type: Number,
          default: 0
        },
    },
    components:{
        DxPopup,
        DxToolbarItem,
        DxScrollView,
        DxForm,
        DxSimpleItem,
        DxGroupItem,
        DxLabel,
        DxAsyncRule,
        DxRequiredRule,
        DxTabPanelOptions,
        DxTab,
        DxDataGrid,
        DxGridToolbar,
        DxGridItem,
        DxColumn,
        DxLookup,
        DxEditing,
        DxPaging,
        DxExport,
        DxButton,
        DxTextBox,
        DxTextBoxButton,
        DxTabbedItem,
        DxTextArea,
        DataGridClient
    },
    setup(props, { emit }){
        onMounted(async () => {
            await methods.loadBaseCode();
        });
        const vars = reactive({
          stock: null,
          clientItem: null,
          releaseItem: null,
          releaseItemByRank: null,
          design: null,
        });
        const bomTreeReverseService = new ApiService('/api/mes/v1/base/bom-reversal')
        const uploadService = new ApiService('/api/mes/v1/mail-attachment');
        vars.component = reactive({});
        vars.formData = reactive({});
        
        vars.stock = getSetupBasicStock([
          { name: 'item_code', op: 'eq', val: '' },
          { name: 'fk_company_id', op: 'eq', val: authService.getCompanyId() },
        ]);

        vars.clientItem = getBaseClientItem([
          { name: 'item_code', op: 'eq', val: '' },
          { name: 'fk_company_id', op: 'eq', val: authService.getCompanyId() },
        ]);
        vars.releaseItem = getShipmentReleaseItem([
          { name: 'item_code', op: 'eq', val: '' },
        ])
        vars.releaseItemByRank = getShipmentReleaseItemByRank([
          { name: 'item_code', op: 'eq', val: '' },
        ])
        vars.design = getBaseDesign([
         { name: 'item_code', op: 'eq', val: '' },
        ])
        vars.addItem = reactive({
            visible: false
        });
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
            item_name: [],
        });
        vars.imageUpload = reactive({
            textVisible: true,
            popupVisible: false,
            isDropZoneActive: false,
            allowedFileExtensions: ['.jpg', '.jpeg', '.gif', '.png'],
        });
        vars.dlg = reactive({ show: false, title: '', key: null, data: null, });

        const attchFiles = {}

        const methods = {
            async refresh(row) {
                if(!row) return;
                methods.initImageUploader();
                vars.formData.id = row.id;
                vars.stock.defaultFilters[0].val = row.item_code;
                vars.clientItem.defaultFilters[0].val = row.item_code;
                vars.releaseItem.defaultFilters[0].val = row.item_code;
                vars.releaseItemByRank.defaultFilters[0].val = row.item_code;
                vars.design.defaultFilters[0].val = row.item_code;
                

                const {data: bomTreeReverseItems} = await bomTreeReverseService.get(String(row.id))
                vars.bomTreeReverse = bomTreeReverseItems
                Object.assign(vars.formData, row);
                
                vars.formData.purchase_price = parseFloat(row.purchase_price);
                
                if(vars.component['grid-client-item']) vars.component['grid-client-item'].refresh();
                if(vars.component['grid-release-item']) vars.component['grid-release-item'].refresh();
                if(vars.component['grid-stock']) vars.component['grid-stock'].refresh();
                if(vars.component['grid-design']) vars.component['grid-design'].refresh();
                if(vars.component['grid-bom-tree-reverse']) vars.component['grid-bom-tree-reverse'].refresh();
  
                // await methods.loadMiddleCategory(row.main_category);
                // await methods.loadSubCategory(row.middle_category);

                if (vars.component['form-edit-item']) {
                vars.component['form-edit-item'].repaint();
                }
                await nextTick();
                // methods.showAddItemPopup();
                
            },
            async onClickItemSaveAs(){
              if (!props.quote_item_id) return;
              if (!vars.formData.item_code || !vars.formData.item_name || !vars.formData.asset_type) {
                  notifyError('필수 정보를 입력하세요');
                  return;
                }
              try{
                const userId = authService._user.user_id;
                if (!vars.formData.register_id) {
                  vars.formData.register_id = userId;
                }
                delete vars.formData.client_company;
                delete vars.formData.basic_stock;
                delete vars.formData.created;
                delete vars.formData.id;
                const {data} = await baseItem.insert(vars.formData);
                await shipmentQuoteItem.update(props.quote_item_id, { item_code: vars.formData.item_code })
                notifyInfo('다름이름으로 저장되었습니다');
                methods.refresh(data);

              } catch(ex){
                if(ex.response.status === 400){
                  notifyError('동알한 품목코드로 다름이름으로저장 할 수 없습니다.');
                }else{
                  console.error(ex);
                  notifyError('저장 할 내용이 없습니다');
                }
                
              }
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
                  delete vars.formData.basic_stock;
                  if (vars.formData.id) {
                    if (vars.component['grid-client-item'] && vars.component['grid-client-item'].hasEditData()) {
                      await vars.component['grid-client-item'].saveEditData()
                    }
                    const params = {...vars.formData}
                    delete params.client_item
                    await baseItem.update(vars.formData.id, params);
                  } else {
                    await baseItem.insert(vars.formData);
                  }
                  notifyInfo('저장되었습니다');
                  
                } catch (ex) {
                  console.error(ex);
                  notifyError('저장 할 내용이 없습니다');
                }                           
            },
            onInitialized(e, key){
                vars.component[key] = e.component;
                // if (key.includes('grid') && !['grid-client-item'].includes(key)) {
                //   stateStore.bind(key, e.component);
                // }
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
            addItemOnHiding(evt){
                delete vars.formData.basic_stock;
                delete vars.formData.client_item;
                delete vars.formData.client;
                delete vars.formData.created;
                emit('change', true);
            },
            onClickAddImage() {
                vars.addImage.visible = true;
            },
            itemCodeValidation(params) {
                return methods.itemCodeDuplicationCheck(params.value)
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
            loadBaseCode() {
                return baseCodeLoader(
                ['자산구분', '단위', '품목분류', '단가구분', '설변구분', '품목그룹', '품명'],
                authService.getCompanyId()
                ).then(response => {
                vars.dataSource.asset_type = response['자산구분'];
                vars.dataSource.unit = response['단위'];
                vars.dataSource.main_category = response['품목분류'];
                vars.dataSource.unit_price_type = response['단가구분'];
                vars.dataSource.design_type = response['설변구분'];
                vars.dataSource.item_group = response['품목그룹'];
                vars.dataSource.item_name = response['품명'];

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
            createPopupFn(key, title, data = null) {
                const _key = key, _title = title, _data = data;
                return () => {
                vars.dlg.key = _key;
                vars.dlg.data = _data;
                vars.dlg.title = _title;
                vars.dlg.show = true;
                };
            },
            closePopup () {
                vars.dlg.show = false;
            },
            async onMiddleCategoryChanged(e) {
                vars.formData.sub_category = null;
                await methods.loadSubCategory(e.value);
                if (vars.component['form-edit-item']) vars.component['form-edit-item'].repaint();
            },
            loadSubCategory(middle_category) {
                return baseCodeLoader([middle_category]).then(response => {
                vars.dataSource.sub_category = response[middle_category];
                });
            },
            loadMiddleCategory(main_category) {
                return baseCodeLoader([main_category]).then(response => {
                vars.dataSource.middle_category = response[main_category];
                });
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
            initImageUploader() {
                vars.imageUpload.textVisible = true;
                vars.imageUpload.popupVisible = false;
                vars.imageUpload.isDropZoneActive = false;
            },
            showAddItemPopup() {
                vars.addItem.visible = true;
            },
            onSavingItemCode(e) {
                e.promise = methods.onSavingItemCodeImpl(e)
            },
            async onSavingItemCodeImpl (e) {
                for (const element of e.changes) {
                // console.log(JSON.stringify(element))
                switch (element.type) {
                    case 'insert': {
                      element.data.item_code = vars.formData.item_code;
                      // element.data.fk_item_id = vars.formData.id;
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
            onFocusedDesignChanged(e) {
                vars.focus.design = e;
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
        };
        watch(
            () => props.row,
            () => methods.refresh(props.row)
        );
        return{
            vars,
            methods,
            generateItemButtonOption,
        }
    }
}
</script>