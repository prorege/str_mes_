<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings">
        <div class="content-header">
          <dx-toolbar>
            <dx-item location="before">
              <div class="content-title">거래처관리</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div class="pa-2">
          <dx-data-grid
            ref="grid"
            class="fixed-header-table"
            height="calc(100vh - 168px)"
            column-resizing-mode="widget"
            :data-source="baseClient"
            :remote-operations="true"
            :show-borders="true"
            :allow-column-reordering="true"
            :allow-column-resizing="true"
            :column-auto-width="true"
            :focused-row-enabled="true"
            @initialized="evt => methods.initialized(evt, 'client-grid')"
            @exporting="methods.onExporting"
            @init-new-row="methods.initInsertedRow"
            @editing-start="methods.clientEditStart"
            @row-validating="methods.rowValidating"
            @row-dbl-click="methods.rowDblClick"
          >
            <!--dx-column data-field="id" caption="번호" :allow-editing="false" sort-order="desc" /-->
            <dx-grid-toolbar>
              <dx-item name="addRowButton" />
              <dx-item name="columnChooserButton" />
              <dx-item location="after" template="excelUploadButton" />
              <dx-item location="after" template="excelSampleDownloadButton" />
              <dx-item location="after" name="exportButton" />
            </dx-grid-toolbar>
            <template #excelUploadButton>
              <dx-button icon="upload" @click="methods.excelUpload" />
            </template>
            <template #excelSampleDownloadButton>
              <dx-button icon="download" @click="methods.excelSampleDownload" />
            </template>

            <dx-column caption="생성시간" data-field="created" data-type="date" format="yyyy-MM-dd" :allow-editing="false" :visible="false" />
            <dx-column caption="업체약칭" data-field="alias" :allow-editing="true" :visible="true">
              <dx-required-rule message="업체약칭을 입력하세요" />
              <dx-async-rule
                message="이미 존재하는 업체약칭입니다"
                :validation-callback="methods.aliasValidation"
              />
            </dx-column>
            <dx-column caption="업체명" data-field="name" :allow-editing="true" :visible="true" :set-cell-value="methods.setCellValue">
              <dx-required-rule message="업체명을 입력하세요" />
            </dx-column>
            <dx-column caption="주소" data-field="address" :allow-editing="true" :visible="true" :editor-options="vars.findAddress.columnOptions" />
            <dx-column caption="상세주소" data-field="address_detail" :allow-editing="true" :visible="false" />
            <dx-column caption="우편번호" data-field="zip_code" :allow-editing="true" :visible="false" />
            <dx-column caption="대표전화번호" data-field="phone" :allow-editing="true" :visible="true" />
            <dx-column caption="팩스번호" data-field="fax" :allow-editing="true" :visible="true" />
            <dx-column caption="대표 이메일" data-field="email" :allow-editing="true" :visible="true" />
            <dx-column caption="홈페이지" data-field="homepage" :allow-editing="true" :visible="true" />
            <dx-column caption="계산서 담당자" data-field="bill_manager" :allow-editing="true" :visible="false" />
            <dx-column caption="계산서 이메일" data-field="bill_email" :allow-editing="true" :visible="false" />
            <dx-column caption="업체분류" data-field="client_type" :allow-editing="true" :visible="false" >
              <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.common.company_type" />
            </dx-column>
            <dx-column caption="지역구분" data-field="district_type" :allow-editing="true" :visible="false">
              <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.common.region" />
            </dx-column>
            <dx-column caption="당사담당자" data-field="manager" :allow-editing="true" :visible="false">
              <dx-lookup value-expr="emp_name" display-expr="emp_name" :data-source="vars.common.employee" />
            </dx-column>
            <dx-column caption="거래중지여부" data-field="trade_yn" editor-type="dxCheckBox" :allow-editing="true" :visible="true" />
            <dx-column caption="영세율" data-field="zero_tax_rate_yn" editor-type="dxCheckBox" :allow-editing="true" :visible="true" />
            <dx-column caption="변경전 업체약칭" data-field="before_alias" :allow-editing="true" :visible="true" />
            <dx-column caption="변경후 업체약칭" data-field="after_alias" :allow-editing="true" :visible="true" />
            <dx-column caption="법인번호" data-field="corp_number" :allow-editing="true" :visible="true">
              <dx-async-rule
                message="이미 사용중인 법인번호입니다"
                :validation-callback="methods.duplicationCorpNum"
              />
            </dx-column>
            <dx-column caption="사업자번호" data-field="business_number" :allow-editing="true" :visible="true" >
              <dx-async-rule :validation-callback="methods.duplicationBusnNum" />
              <dx-async-rule :validation-callback="methods.validationBusnNum" />
            </dx-column>
            <dx-column caption="사업자상호" data-field="business_name" :allow-editing="true" :visible="true" />
            <dx-column caption="대표자명" data-field="ceo_name" :allow-editing="true" :visible="true" />
            <dx-column caption="업태" data-field="business_status" :allow-editing="true" :visible="true" />
            <dx-column caption="종목" data-field="business_sector" :allow-editing="true" :visible="true" />
            <dx-column caption="업체명(영문)" data-field="name_en" :allow-editing="true" :visible="true" />
            <dx-column caption="대표자명(영문)" data-field="ceo_name_en" :allow-editing="true" :visible="true" />
            <dx-column caption="전화번호(국제)" data-field="phone_en" :allow-editing="true" :visible="true" />
            <dx-column caption="팩스번호(국제)" data-field="fax_en" :allow-editing="true" :visible="true" />
            <dx-column caption="주소(영문)" data-field="address_en" :allow-editing="true" :visible="true" />
            <dx-column caption="최초등록자" data-field="register_id" :allow-editing="false" :visible="true" />
            <dx-column caption="최초수정자" data-field="modify_id" :allow-editing="false" :visible="true" />
            <dx-column caption="최종수정일자" data-field="last_updated_date" data-type="date" format="yyyy-MM-dd" :allow-editing="false" :visible="true" />
            <dx-column caption="비고" data-field="etc" :allow-editing="true" :visible="true" />

            <dx-export :enabled="true" />
            <dx-editing mode="popup"
              :use-icons="true"
              :allow-adding="true"
              :allow-updating="true"
              :allow-deleting="true"
            >
              <dx-grid-popup
                title="거래처정보"
                :width="1000"
                :height="'90vh'"
                :show-title="true"
                :resize-enabled="true"
              >
              </dx-grid-popup>
              <dx-form
                :col-count="1"
                :show-colon-after-label="false"
                @initialized="evt => methods.initialized(evt, 'client-form')"
              >
                <dx-group-item :col-count="2" css-class="pa-4">
                  <dx-simple-item data-field="alias">
                    <dx-label text="업체약칭" />
                  </dx-simple-item>
                  <dx-simple-item data-field="corp_number" :editor-options="{ mask: '000000 - 0000000' }">
                    <dx-label text="법인번호" />
                  </dx-simple-item>

                  <dx-simple-item data-field="name">
                    <dx-label text="정식상호" />
                  </dx-simple-item>
                  <dx-group-item :col-count="5">
                    <dx-simple-item :col-span="4" data-field="business_number" :editor-options="{ mask: '000 - 00 - 00000' }">
                      <dx-label text="사업자번호" />
                    </dx-simple-item>
                    <dx-simple-item :col-span="1" data-field="zero_tax_rate_yn">
                      <dx-label text="영세율" />
                    </dx-simple-item>
                  </dx-group-item>
                  <dx-simple-item data-field="address" editor-type="dxTextArea">
                    <dx-label text="주소" />
                  </dx-simple-item>
                  <dx-simple-item :col-span="1" data-field="business_name">
                      <dx-label text="사업자상호" />
                  </dx-simple-item>
                  <dx-simple-item data-field="address_detail" editor-type="dxTextArea">
                    <dx-label text="상세주소" />
                  </dx-simple-item>
                  <dx-simple-item data-field="ceo_name">
                    <dx-label text="대표자명" />
                  </dx-simple-item>
                  <dx-simple-item data-field="zip_code">
                      <dx-label text="우편번호" />
                  </dx-simple-item>
                  <dx-simple-item data-field="business_status">
                    <dx-label text="업태" />
                  </dx-simple-item>
                  <dx-simple-item data-field="business_sector">
                    <dx-label text="종목" />
                  </dx-simple-item>
                  <dx-simple-item data-field="phone">
                    <dx-label text="대표전화번호" />
                  </dx-simple-item>
                  <dx-simple-item data-field="fax">
                    <dx-label text="팩스번호" />
                  </dx-simple-item>
                  <dx-simple-item data-field="name_en">
                    <dx-label text="업체명(영문)" />
                  </dx-simple-item>

                  <dx-simple-item data-field="email">
                    <dx-label text="대표 이메일" />
                  </dx-simple-item>
                  <dx-simple-item data-field="ceo_name_en">
                    <dx-label text="대표자명(영문)" />
                  </dx-simple-item>

                  <dx-simple-item data-field="homepage">
                    <dx-label text="홈페이지" />
                  </dx-simple-item>
                  <dx-simple-item data-field="phone_en">
                    <dx-label text="전화번호(국제)" />
                  </dx-simple-item>

                  <dx-simple-item data-field="bill_manager">
                    <dx-label text="계산서 담당자" />
                  </dx-simple-item>
                  <dx-simple-item data-field="fax_en">
                    <dx-label text="팩스번호(국제)" />
                  </dx-simple-item>

                  <dx-simple-item data-field="bill_email">
                    <dx-label text="계산서 이메일" />
                  </dx-simple-item>
                  <dx-simple-item data-field="address_en">
                    <dx-label text="주소(영문)" />
                  </dx-simple-item>

                  <dx-group-item :col-count="2">
                    <dx-simple-item data-field="client_type">
                      <dx-label text="업체분류" />
                    </dx-simple-item>
                    <dx-simple-item data-field="district_type">
                      <dx-label text="지역구분" />
                    </dx-simple-item>
                  </dx-group-item>
                  <dx-simple-item data-field="etc" 
                    :editor-options="generateItemButtonOption(
                      'rename',
                      methods.createPopupFn('etc', '비고')
                    )">
                    <dx-label text="비고" />
                  </dx-simple-item>

                  <dx-group-item :col-count="2">
                    <dx-simple-item data-field="manager">
                      <dx-label text="당사담당자" />
                    </dx-simple-item>
                    <dx-simple-item data-field="trade_yn">
                      <dx-label text="거래중지" />
                    </dx-simple-item>
                  </dx-group-item>
                  <dx-group-item :col-count="2">
                    <dx-simple-item data-field="register_id">
                      <dx-label text="최초등록자" />
                    </dx-simple-item>
                    <dx-simple-item data-field="created">
                      <dx-label text="최초등록일자" />
                    </dx-simple-item>
                  </dx-group-item>

                  <dx-group-item :col-count="2">
                    <dx-simple-item data-field="before_alias">
                      <dx-label text="변경전 업체약칭" />
                    </dx-simple-item>
                    <dx-simple-item data-field="after_alias">
                      <dx-label text="변경후 업체약칭" />
                    </dx-simple-item>
                  </dx-group-item>
                  <dx-group-item :col-count="2">
                    <dx-simple-item data-field="modify_id">
                      <dx-label text="최종수정자" />
                    </dx-simple-item>
                    <dx-simple-item data-field="last_updated_date">
                      <dx-label text="최종수정일자" />
                    </dx-simple-item>
                  </dx-group-item>
                  <dx-group-item :col-span="2" template="secondGrid">
                  </dx-group-item>
                </dx-group-item>
              </dx-form>
            </dx-editing>
            <dx-column-chooser mode="select" :enabled="true" />
            <dx-filter-row :visible="true" />
            <dx-paging :page-size="20" />

            <template #secondGrid>
              <dx-data-grid
                class="fixed-header-table"
                height="100%"
                :disabled="vars.disableClientManagerGrid.value"
                :data-source="baseClientManager"
                :remote-operations="true"
                :show-borders="true"
                :allow-column-resizing="true"
                :column-auto-width="true"
                :select-text-on-edit-start="true"
                @initialized="evt => methods.initialized(evt, 'client-manager')"
                @init-new-row="methods.initManagerInsertedRow"
              >
                <dx-column caption=" 번호" data-field="id" sort-order="desc" :allow-editing="false" />
                <dx-column caption="생성시간" data-field="created" data-type="date" format="yyyy-MM-dd" :allow-editing="false" :visible="false" />
                <dx-column caption="거래처담당자" data-field="name" :allow-editing="true" :visible="true" />
                <dx-column caption="부서" data-field="department" :allow-editing="true" :visible="true" />
                <dx-column caption="직급" data-field="position" :allow-editing="true" :visible="true">
                  <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.common.position_code" />
                </dx-column>
                <dx-column caption="휴대폰번호" data-field="mobile" :allow-editing="true" :visible="true" />
                <dx-column caption="이메일주소" data-field="email" :allow-editing="true" :visible="true" />
                <dx-column caption="직통전화번호" data-field="direct_phone" :allow-editing="true" :visible="true" />
                <dx-column caption="내선번호" data-field="ext_phone" :allow-editing="true" :visible="true" />
                <dx-column caption="비고" data-field="etc" :allow-editing="true" :visible="true" />
                <dx-column caption="거래처 ID" data-field="fk_client_id" :allow-editing="false" :visible="false" />

                <dx-editing mode="row"
                  :use-icons="true"
                  :allow-adding="true"
                  :allow-updating="true"
                  :allow-deleting="true"
                />
                <dx-paging :page-size="20" />
              </dx-data-grid>
            </template>
          </dx-data-grid>
        </div>
      </div>
    </div>

    <dx-popup
      v-model:visible="vars.findAddress.popup.value"
      content-template="popup-content"
      title="주소찾기"
      :close-on-outside-click="true"
      :width="680"
      :height="500"
      :resize-enabled="true"
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
            :data-source="vars.findAddress.store"
            :show-borders="true"
            :allow-column-reordering="true"
            :allow-column-resizing="true"
            :column-auto-width="true"
            :remote-operations="true"
            @initialized="evt => methods.initialized(evt, 'find-address')"
            @row-click="methods.findAddressSelect"
          >
            <dx-column caption="도로명주소" data-field="road" />
            <dx-column caption="지번주소" data-field="jibun" />
            <dx-column caption="우편번호" data-field="zip" />
            <dx-paging :page-size="20" />
          </dx-data-grid>
        </div>
      </template>
    </dx-popup>

    <dx-popup
      v-model:visible="vars.dlg.show"
      content-template="popup-content"
      :title="vars.dlg.title"
      :close-on-outside-click="false"
      :width="680"
      :height="500"
      :key="vars.dlg.key"
      :resize-enabled="true"
    >
      <template #popup-content>
        <div v-if="vars.dlg.key === 'etc'">
          <dx-text-area :height="260" v-model="vars.formData.etc" />
          <div class="popup-footer">
            <dx-button text="저장" type="default" icon="save" @click="methods.setEtcValue" />
          </div>
        </div>
      </template>
    </dx-popup>

    <input
      hidden
      type="file"
      ref="excelRef"
      accept=".xlsx,.xls"
      @change="methods.excelFileChange"
    />
  </div>
</template>

<script>
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import {
  DxDataGrid,
  DxForm,
  DxColumn,
  DxPaging,
  DxLookup,
  DxEditing,
  DxExport,
  DxFilterRow,
  DxAsyncRule,
  DxRequiredRule,
  DxColumnChooser,
  DxPopup as DxGridPopup,
  DxToolbar as DxGridToolbar,
} from 'devextreme-vue/data-grid';
import DxTextArea from 'devextreme-vue/text-area';
import { DxLabel, DxGroupItem, DxSimpleItem } from 'devextreme-vue/form';
import { DxPopup } from 'devextreme-vue/popup';
import DxTextBox from 'devextreme-vue/text-box';
import { DxButton } from 'devextreme-vue/button';
import { baseClient, baseCodeLoader, baseClientManager } from '@/data-source/base';
import FindAddressStore from '../../data-source/find-address';
import findBusinessNumber from '../../data-source/find-business-number';
import authService from '../../auth';
import ApiService from '../../utils/api-service';
import { notifyError } from '../../utils/notify';
import { generateItemButtonOption } from '../../utils/util';
import stateStore from '@/utils/state-store';
import { ref, reactive } from 'vue';
import moment from 'moment';
import { saveAs } from 'file-saver';
import { loadEmployee } from '../../utils/data-loader';


export default {
  components: {
    DxToolbar,
    DxItem,
    DxButton,
    DxForm,
    DxLabel,
    DxGroupItem,
    DxSimpleItem,
    DxDataGrid,
    DxColumn,
    DxEditing,
    DxPaging,
    DxExport,
    DxColumnChooser,
    DxFilterRow,
    DxLookup,
    DxGridPopup,
    DxRequiredRule,
    DxAsyncRule,
    DxGridToolbar,
    DxTextArea,
    DxPopup,
    DxTextBox,
  },
  setup() {
    const vars = {}, methods = {};
    const grid = ref(null);

    const excelRef = ref(null);
    const apiExcel = new ApiService('/api/mes/v1/excel/base/client');

    baseClient.defaultFilters = {
      name: 'fk_company_id',
      op: 'eq',
      val: authService.getCompanyId(),
    };
    const clientCheck = baseClient.clone();

    // Vars
    vars.formData = {};
    vars.common = reactive({ position_code: [], region: [], company_type: [], employee: [] });

    vars.disableClientManagerGrid = ref(false);
    vars.editKey = null;
    vars.components = {};
    vars.findAddress = {
      popup: ref(false),
      store: new FindAddressStore(),
      keyword: null,
      columnOptions: {
        buttons: [
          {
            name: 'icon',
            location: 'after',
            options: {
              stylingMode: 'text',
              icon: 'search',
              onClick: () => {
                const rowIndex = vars.components[
                  'client-grid'
                ].getRowIndexByKey(vars.editKey);
                vars.findAddress.keyword = vars.components[
                  'client-grid'
                ].cellValue(rowIndex, 'address');
                vars.findAddress.popup.value = true;
              },
            },
          },
        ],
      },
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
    };

    vars.dlg = reactive({
      show: false,
      title: '',
      key: null,
      data: null,
    });

    baseCodeLoader(['직급', '업체분류', '지역구분']).then(response => {
      vars.common.position_code = response['직급'];
      vars.common.region = response['지역구분'];
      vars.common.company_type = response['업체분류'];
    });

    loadEmployee(vars.common)

    // Methods
    methods.initialized = (evt, key) => {
      vars.components[key] = evt.component;
      stateStore.bind(key, evt.component);
    };

    methods.isAddButtonVisible = ({ row }) => {
      return !row.isEditing;
    };

    methods.initInsertedRow = ({ component, data }) => {
      component.columnOption('alias', 'allowEditing', true);
      data.created = moment().format('YYYY-MM-DD HH:mm:ss');
      data.fk_company_id = authService.getCompanyId();
      vars.editKey = 0;
      vars.disableClientManagerGrid.value = true;
      baseClientManager.defaultFilters = [
        { name: 'fk_client_id', op: 'eq', val: 0 },
      ];
    };

    methods.initManagerInsertedRow = ({ data }) => {
      console.log('initManagerInsertedRow');
      data.created = moment().format('YYYY-MM-DD HH:mm:ss');
      data.fk_client_id = vars.formData.id;
    };

    methods.clientEditStart = evt => {
      console.log(evt);
      const clientId = evt.data.id || 0;
      vars.formData = evt.data;
      vars.editKey = evt.key;
      vars.disableClientManagerGrid.value = false;
      evt.component.columnOption('alias', 'allowEditing', false);
      baseClientManager.defaultFilters = [
        { name: 'fk_client_id', op: 'eq', val: clientId },
      ];
    };

    methods.findAddressSubmit = () => {
      vars.findAddress.store.keyword = vars.findAddress.keyword;
      vars.components['find-address'].refresh();
    };

    methods.findAddressSelect = ({ data }) => {
      console.log('findAddressSelect');
      const rowIndex = vars.editKey
        ? vars.components['client-grid'].getRowIndexByKey(vars.editKey)
        : 0;
      vars.components['client-grid'].beginUpdate();
      vars.components['client-grid'].cellValue(rowIndex, 'address', data.road);
      vars.components['client-grid'].cellValue(
        rowIndex,
        'address_en',
        data.eng
      );
      vars.components['client-grid'].cellValue(rowIndex, 'zip_code', data.zip);
      vars.components['client-grid'].cellValue(rowIndex, 'address_detail', '');
      vars.components['client-grid'].endUpdate();
      vars.findAddress.popup.value = false;
    };

    methods.duplicationCorpNum = ({ data, value }) => {
      if (!value) return Promise.resolve(true);

      const filter = [
        ['corp_number', '=', value],
        'and',
        ['fk_company_id', '=', authService.getCompanyId()],
      ];
      if (data.id) filter.push('and', ['id', '<>', data.id]);

      const skip = 0, take = 1;
      return clientCheck
        .load({ filter, skip, take })
        .then(response => !response.totalCount)
        .catch(ex => {
          console.error(ex.message);
          return false;
        });
    };
    methods.duplicationBusnNum = async function duplicationBusnNum({
      data,
      value,
    }) {
      if (!value) return true;
      const filter = [
        ['business_number', '=', value],
        'and',
        ['fk_company_id', '=', authService.getCompanyId()],
      ];
      if (data.id) filter.push('and', ['id', '<>', data.id]);

      const skip = 0,
        take = 1;
      const { totalCount, data: responseData } = await clientCheck.load({
        filter,
        skip,
        take,
      });
      if (totalCount === 0) return true;
      // throw Error(`"${responseData[0].name}"에서 이미 사용 중 입니다`); 
    };

    methods.validationBusnNum = async function validationBusnNum({
      data,
      value,
    }) {
      if (!value) return true;

      const getException = msg => {
        const exception = new Error();
        exception.self = true;
        exception.message = msg;
        return exception;
      };

      try {
        const ret = await findBusinessNumber(value);
        if (!ret.result.length || !ret.result[0].b_stt_cd)
          throw getException('등록되지 않은 사업자번호 입니다');
        if (ret.result[0].b_stt_cd === '01') return true;
        throw getException(`${ret.result[0].b_stt} 상태인 사업자 입니다`);
      } catch (ex) {
        if (ex.self) throw ex;
        else {
          console.log(ex);
          throw Error('조회에 실패했습니다');
        }
      }
    };

    methods.rowValidating = evt => {
      console.log(evt);
      if (
        evt.brokenRules.length === 1 &&
        evt.brokenRules[0].validationCallback.name === 'validationBusnNum'
      ) {
        evt.isValid = true;
      }
    };

    methods.excelUpload = () => {
      excelRef.value.click();
    };

    methods.excelFileChange = async ({ target }) => {
      if (!target.files.length) return;

      vars.components['client-grid'].beginCustomLoading(
        '엑셀 데이터를 읽고 있습니다'
      );
      const fd = new FormData();
      fd.append('file', target.files[0]);

      try {
        await apiExcel.post('', fd);
        vars.components['client-grid'].refresh();
      } catch (ex) {
        if (ex.response.data) {
          notifyError(ex.response.data);
        }
      } finally {
        vars.components['client-grid'].endCustomLoading();
        target.value = null;
      }
    };

    methods.excelSampleDownload = () => {
      saveAs('/api/mes/v1/excel/base/client', '거래처입력양식.xlsx');
    };

    methods.aliasDuplicationCheck = (alias) => {
      return new Promise((resolve) => {
        try {
          baseClient.load({ filter: ['alias', '=', alias] }).then((res) => {
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
    };

    methods.rowDblClick = ({rowIndex, component}) => {
      component.editRow(rowIndex)
    }

    methods.aliasValidation = (params) => {
      if (vars.formData.id) return Promise.resolve(true)
      return methods.aliasDuplicationCheck(params.value)
    };

    methods.createPopupFn = (key, title, data = null) => {
      const _key = key, _title = title, _data = data;
      return () => {
        vars.dlg.key = _key;
        vars.dlg.data = _data;
        vars.dlg.title = _title;
        vars.dlg.show = true;
      };
    }
    methods.setCellValue = (newData, value, currentRowData) => {
      if(!value) return;
      newData.name = value;
      newData.business_name = value;
    }
    methods.setEtcValue = () => {
      if (vars.components['client-grid']) {
        const rowIndex = vars.editKey
          ? vars.components['client-grid'].getRowIndexByKey(vars.editKey)
          : 0
        vars.components['client-grid'].cellValue(rowIndex, 'etc', vars.formData.etc);
        console.log(`update date: ${vars.editKey}, ${vars.formData.etc}`)
      }
      vars.dlg.show = false;
    }

    methods.onExporting = (evt) => {
      baseClient.exportData(evt.component, '거래처', `거래처_${Date.now()}.xlsx`)
      evt.cancel = true
    }

    return {
      vars,
      methods,
      excelRef,
      grid,
      baseClient,
      baseClientManager,
      generateItemButtonOption,
    };
  },
};
</script>
