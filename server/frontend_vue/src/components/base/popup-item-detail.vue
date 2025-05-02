<script setup>
import moment from 'moment';
import { DxPopup } from 'devextreme-vue/popup';
import { DxScrollView } from 'devextreme-vue/scroll-view';
import {
  DxForm,
  DxTab,
  DxLabel,
  DxGroupItem,
  DxSimpleItem,
  DxTabbedItem,
  DxTabPanelOptions,
} from 'devextreme-vue/form';
import {
  DxDataGrid,
  DxColumn,
  DxPaging,
  DxExport,
} from 'devextreme-vue/data-grid';
import {
  ref,
  reactive,
  watch,
  computed,
  nextTick,
  defineProps,
  defineEmits,
} from 'vue';
import { getSetupBasicStock } from '@/data-source/setup';
import {
  baseItem,
  getBaseClientItem,
  getBaseDesign,
} from '@/data-source/base';
import {
  getShipmentReleaseItem,
  getShipmentReleaseItemByRank,
} from '../../data-source/shipment';
import authService from '@/auth';
import stateStore from '@/utils/state-store';
import ApiService from '../../utils/api-service';

const props = defineProps({
  itemId: { type: Number },
});
const emit = defineEmits(['update:visible']);
const init = ref(false);
const formData = reactive({});
const components = {};
const bomTreeReverseService = new ApiService('/api/mes/v1/base/bom-reversal');
const etcDetailDialog = ref(false);

const clientItem = getBaseClientItem([
  { name: 'item_code', op: 'eq', val: '' },
  { name: 'fk_company_id', op: 'eq', val: authService.getCompanyId() },
]);
const stock = getSetupBasicStock([
  { name: 'item_code', op: 'eq', val: '' },
  { name: 'fk_company_id', op: 'eq', val: authService.getCompanyId() },
]);
const design = getBaseDesign([{ name: 'item_code', op: 'eq', val: '' }]);

const releaseItem = getShipmentReleaseItem([
  { name: 'item_code', op: 'eq', val: '' },
]);
const releaseItemByRank = getShipmentReleaseItemByRank([
  { name: 'item_code', op: 'eq', val: '' },
]);
const bomTreeReverse = ref();

baseItem.transform = (item) => {
  item.purchase_price = parseFloat(item.purchase_price);
  item.sales_price = parseFloat(item.sales_price);
};

watch(
  () => props.itemId,
  () => initById(props.itemId)
);

const itemImage = computed(() => {
  if (!formData.item_img) return null;
  if (formData.item_img.startsWith('data:')) return formData.item_img;
  return `/api/mes/v1/base/item-image/${formData.item_img}`;
});

async function initById(itemId) {
  init.value = false;
  if (!itemId) return;
  
  const { data: itemData } = await baseItem.byKey(props.itemId);
  Object.assign(formData, itemData);


  clientItem.defaultFilters[0].val = itemData.item_code;
  releaseItem.defaultFilters[0].val = itemData.item_code;
  releaseItemByRank.defaultFilters[0].val = itemData.item_code;
  stock.defaultFilters[0].val = itemData.item_code;
  design.defaultFilters[0].val = itemData.item_code;

  const { data: bomTreeReverseItems } = await bomTreeReverseService.get(
    String(props.itemId)
  );
  bomTreeReverse.value = bomTreeReverseItems;

  await nextTick();

  if (components['popup-client-item']) components['popup-client-item'].refresh();
  if (components['stock']) components['stock'].refresh();
  if (components['release-item']) components['release-item'].refresh();
  // if (components['price']) components['price'].refresh()
  if (components['bomTreeReverse']) components['bomTreeReverse'].refresh();
  init.value = true;
}

function initialized(e, key) {
  components[key] = e.component;
  if (!['popup-client-item'].includes(key)) stateStore.bind(key, e.component);
}

function envHzLevel1(row) {
  return row.item_code === formData.item_code ? row.item_code : '';
}

function envHzLevel2(row) {
  return row.item_code === formData.item_code ? '' : row.item_code;
}

function envHzRoHSExpDate(row) {
  if (row.rohs_register_date && row.rohs_expiration_period) {
    return moment(row.rohs_register_date)
      .add(row.rohs_expiration_period, 'Y')
      .format('YYYY-MM-DD');
  }
  return '';
}

function detailDialog() {
  console.log('onDblClick');
  etcDetailDialog.value = true;
}

initById();
</script>

<template>
  <dx-popup
    :visible="props.visible"
    content-template="popup-content"
    title="품목상세정보"
    width="70%"
    height="80%"
    :resize-enabled="true"
    :close-on-outside-click="true"
    @update:visible="(value) => emit('update:visible', value)"
  >
    <template #popup-content>
      <dx-scroll-view width="100%" height="100%">
        <dx-form
          :form-data="formData"
          :col-count="1"
          :show-colon-after-label="false"
          :read-only="true"
          @initialized="(evt) => initialized(evt, 'popup-item-detail')"
        >
          <template #image-template="{}">
            <div class="form-image">
              <img
                class="item-image"
                :src="itemImage.value"
                v-if="formData.item_img"
                alt=""
              />
            </div>
          </template>
          <dx-group-item :col-count="4">
            <dx-group-item :col-span="2" :col-count="2">
              <dx-group-item :col-span="1">
                <dx-simple-item template="image-template" />
              </dx-group-item>
              <dx-group-item :col-span="1" :col-count="1">
                <dx-simple-item data-field="item_code" :col-span="1">
                  <dx-label text="품목코드" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item data-field="main_category">
                  <dx-label text="대분류" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item data-field="asset_type">
                  <dx-label text="자산구분" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item
                  data-field="safety_stock"
                  editor-type="dxNumberBox"
                  :col-span="1"
                >
                  <dx-label text="안전재고" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item
                  data-field="import_check"
                  editor-type="dxCheckBox"
                  :col-span="1"
                >
                  <dx-label text="수입검사" :show-colon="false" />
                </dx-simple-item>
              </dx-group-item>
              <dx-group-item :col-span="2" :col-count="2">
                <dx-simple-item data-field="item_detail" :col-span="2">
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
                <dx-simple-item
                  data-field="etc"
                  :col-span="2"
                  editor-type="dxTextArea"
                  :editor-options="{
                    height: 82,
                    buttons: [
                      {
                        name: 'rename',
                        location: 'after',
                        options: {
                          stylingMode: 'text',
                          icon: 'rename',
                          disabled: false,
                          onClick: detailDialog,
                        },
                      },
                    ],
                  }"
                >
                  <dx-label text="비고" :show-colon="false" />
                </dx-simple-item>
              </dx-group-item>
            </dx-group-item>
            <dx-group-item :col-span="2" :col-count="2">
              <dx-simple-item data-field="item_name" :col-span="1">
                <dx-label text="품명" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="item_standard" :col-span="1">
                <dx-label text="규격" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="item_group">
                <dx-label text="품목 그룹" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="client.alias">
                <dx-label text="제조사" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="middle_category" :visible="false" >
                <dx-label text="중분류" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="sub_category" :visible="false" >
                <dx-label text="소분류" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="moq"
                editor-type="dxNumberBox"
                :col-span="1"
                :editor-options="{ format: 'fixedPoint' }"
              >
                <dx-label text="MOQ" :show-colon="false" />
              </dx-simple-item>

              <dx-simple-item data-field="unit">
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
              <dx-simple-item
                data-field="sales_price"
                editor-type="dxNumberBox"
                :col-span="1"
                :editor-options="{ format: { type: 'currency', precision: 2 } }"
              >
                <dx-label text="매출단가" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="purchase_price"
                editor-type="dxNumberBox"
                :col-span="1"
                :editor-options="{ format: { type: 'currency', precision: 2 } }"
              >
                <dx-label text="매입단가" :show-colon="false" />
              </dx-simple-item>

              <dx-simple-item data-field="before_item_code" :col-span="1">
                <dx-label text="변경전 품목코드" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="after_item_code" :col-span="1">
                <dx-label text="변경후 품목코드" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="end_of_use"
                editor-type="dxCheckBox"
                :col-span="1"
              >
                <dx-label text="사용종료" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="end_date"
                editor-type="dxDateBox"
                :col-span="1"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                }"
              >
                <dx-label text="종료일자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="register_id">
                <dx-label text="최초등록자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="created"
                editor-type="dxDateBox"
                :col-span="1"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                }"
              >
                <dx-label text="최초등록일자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="modify_id">
                <dx-label text="최종수정자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="modify_date"
                editor-type="dxDateBox"
                :col-span="1"
                :editor-options="{
                  dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                }"
              >
                <dx-label text="최종수정일자" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
          </dx-group-item>
          <dx-group-item :visible="formData.item_group == 'LED 모듈'" :col-count="4">
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
          <dx-group-item>
            <dx-tabbed-item>
              <dx-tab-panel-options :defer-rendering="false" />

              <dx-tab title="거래처 품목코드">
                <dx-data-grid
                  class="fixed-header-table"
                  height="420px"
                  date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                  column-resizing-mode="widget"
                  :data-source="clientItem"
                  :show-borders="true"
                  :column-auto-width="true"
                  :remote-operations="true"
                  :allow-column-resizing="true"
                  @initialized="(evt) => initialized(evt, 'popup-client-item')"
                >
                  <dx-column
                    caption="주공급업체"
                    data-field="main_supplier"
                    :allow-editing="false"
                  />
                  <dx-column
                    caption="거래처명"
                    data-field="client.name"
                    :allow-editing="false"
                  />
                  <dx-column
                    caption="거래처품번"
                    data-field="client_item_code"
                  />
                  <dx-column caption="단가구분" data-field="unit_price_type" />
                  <dx-column
                    caption="단가"
                    data-field="unit_price"
                    data-type="number"
                    :format="{ type: 'fixedPoint', precision: 2 }"
                  />
                  <dx-column caption="참고" data-field="note" />
                  <dx-column
                    caption="등록일자"
                    data-field="created"
                    data-type="date"
                    format="yyyy-MM-dd"
                    :allow-editing="false"
                    :sort-index="0" sort-order="desc"
                  />
                  <dx-column caption="비고" data-field="etc" />
                  <dx-column
                    caption="거래처ID"
                    data-field="client_id"
                    :visible="false"
                  />
                  <dx-column
                    caption="품목코드"
                    data-field="item_code"
                    :visible="false"
                  />
                  <dx-column
                    caption="회사ID"
                    data-field="fk_company_id"
                    :visible="false"
                  />

                  <dx-paging :page-size="20" />
                </dx-data-grid>
              </dx-tab>

              <dx-tab title="단가이력정보">
                <dx-data-grid
                  class="fixed-header-table"
                  height="420px"
                  column-resizing-mode="widget"
                  :data-source="releaseItemByRank"
                  :remote-operations="true"
                  :show-borders="true"
                  :allow-column-resizing="true"
                  :column-auto-width="true"
                  @initialized="(evt) => initialized(evt, 'release-item')"
                >
                  <dx-column
                    caption="출고단가"
                    data-field="unit_price"
                    data-type="number"
                    :format="{ type: 'fixedPoint', precision: 2 }"
                  />
                  <dx-column
                    caption="출고수량"
                    data-field="release_quantity"
                    data-type="number"
                    format="fixedPoint"
                  />
                  <dx-column
                    caption="출고번호"
                    data-field="release.release_number"
                  />
                  <dx-column
                    caption="출고일자"
                    data-field="release.release_date"
                    data-type="date"
                    format="yyyy-MM-dd"
                  />
                  <dx-column
                    caption="고객업체"
                    data-field="release.client_company"
                  />
                  <dx-column
                    caption="영업부서"
                    data-field="release.release_department"
                  />
                  <dx-column
                    caption="영업담당"
                    data-field="release.release_manager"
                  />

                  <dx-paging :page-size="20" />
                </dx-data-grid>
              </dx-tab>

              <dx-tab title="창고별재고">
                <dx-data-grid
                  class="fixed-header-table"
                  height="420px"
                  column-resizing-mode="widget"
                  :data-source="stock"
                  :show-borders="true"
                  :column-auto-width="true"
                  :remote-operations="true"
                  :allow-column-resizing="true"
                  @initialized="(evt) => initialized(evt, 'stock')"
                >
                  <dx-column caption="창고명" data-field="warehouse.wh_name" />
                  <dx-column
                    caption="현재고"
                    data-field="current_stock"
                    data-type="number"
                    format="fixedPoint"
                  />
                  <dx-column
                    caption="할당재고"
                    data-field="assign_stock"
                    data-type="number"
                    format="fixedPoint"
                  />
                  <dx-column
                    caption="가용재고"
                    data-field="available_stock"
                    data-type="number"
                    format="fixedPoint"
                  />

                  <dx-paging :page-size="20" />
                </dx-data-grid>
              </dx-tab>

              <dx-tab title="도면관리">
                <dx-data-grid
                  class="fixed-header-table"
                  height="420px"
                  date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                  column-resizing-mode="widget"
                  :data-source="design"
                  :show-borders="true"
                  :remote-operations="true"
                  :column-auto-width="true"
                  :allow-column-resizing="true"
                  @initialized="(evt) => initialized(evt, 'design')"
                >
                  <dx-column caption="도면번호" data-field="design_number" />
                  <dx-column
                    caption="등록일"
                    data-field="registration_date"
                    data-type="date"
                    format="yyyy-MM-dd"
                  />
                  <dx-column caption="설변구분" data-field="design_type" />
                  <dx-column caption="설변사항" data-field="note" />
                  <dx-column
                    caption="도면파일첨부"
                    data-field="design_file_name"
                    cell-template="download"
                  />
                  <dx-column
                    caption="도면파일"
                    data-field="design_file"
                    :visible="false"
                  />

                  <dx-paging :page-size="20" />

                  <template #download="{ data }">
                    <a :href="data.data[data.column.dataField]" download>{{
                      data.data[data.column.dataField]
                    }}</a>
                  </template>
                </dx-data-grid>
              </dx-tab>

              <dx-tab title="BOM 역전개">
                <dx-data-grid
                  class="fixed-header-table"
                  height="420px"
                  column-resizing-mode="widget"
                  :data-source="bomTreeReverse"
                  :show-borders="true"
                  :remote-operations="true"
                  :column-auto-width="true"
                  @initialized="(evt) => initialized(evt, 'bomTreeReverse')"
                >
                  <dx-column caption="주품목" data-field="root_item_name" />
                  <dx-column
                    caption="주품목(모델)"
                    data-field="root_item_code"
                  />
                  <dx-column caption="소요량" data-field="requirement" />
                  <dx-column caption="모품목" data-field="parent_item_name" />
                  <dx-column
                    caption="모품목(모델)"
                    data-field="parent_item_code"
                  />
                  <dx-export :enabled="true" />
                </dx-data-grid>
              </dx-tab>
            </dx-tabbed-item>
          </dx-group-item>
        </dx-form>

        <dx-popup
          v-model:visible="etcDetailDialog"
          content-template="popup-content"
          title="비고"
          :width="680"
          :height="600"
          :resize-enabled="true"
        >
          <template #popup-content>
            <div style="white-space: pre-line">{{ formData.etc }}</div>
          </template>
        </dx-popup>
      </dx-scroll-view>
    </template>
  </dx-popup>
</template>
