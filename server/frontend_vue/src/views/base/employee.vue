<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings">
        <div class="content-header">
          <dx-toolbar>
            <dx-item location="before">
              <div class="content-title">부서/사원</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <dx-tab-panel
          :animation-enabled="false"
          :swipe-enabled="false"
          @selection-changed="methods.tabChanged"
        >
          <dx-item title="부서">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 210px)"
                  column-resizing-mode="widget"
                  :show-borders="true"
                  :column-auto-width="true"
                  :remote-operations="true"
                  :focused-row-enabled="true"
                  :allow-column-resizing="true"
                  :select-text-on-edit-start="true"
                  :data-source="baseDepartment"
                  @init-new-row="methods.groupRowInit"
                  @data-error-occurred="methods.onDataError"
                  @initialized="evt => methods.initialized(evt, 'group')"
                >
                  <dx-column caption="부서명" data-field="department_name" :allow-editing="true" :allow-hiding="false" />
                  <dx-column caption="부서장" data-field="depart_head_name" width="140" :allow-editing="true">
                    <dx-lookup value-expr="emp_name" display-expr="emp_name" :data-source="methods.employeeLookup" />
                  </dx-column>
                  <dx-column caption="지정창고" data-field="wh_code" width="140" :allow-editing="true">
                    <dx-lookup value-expr="wh_code" display-expr="wh_name" :data-source="vars.common.warehouse" />
                  </dx-column>
                  <dx-column caption="생성일" data-field="created" width="140" data-type="date" format="yyyy-MM-dd" :allow-editing="false" />

                  <dx-editing mode="row"
                    :use-icons="true"
                    :allow-adding="true"
                    :allow-updating="true"
                    :allow-deleting="true"
                  />
                  <dx-paging :page-size="20" />
                </dx-data-grid>
              </div>
            </template>
          </dx-item>
          <dx-item title="사원">
            <template #default>
              <div class="pa-2">
                <dx-data-grid
                  class="fixed-header-table"
                  height="calc(100vh - 210px)"
                  date-serialization-format="yyyy-MM-ddTHH:mm:ss"
                  column-resizing-mode="widget"
                  :show-borders="true"
                  :remote-operations="true"
                  :column-auto-width="true"
                  :focused-row-enabled="true"
                  :allow-column-resizing="true"
                  :select-text-on-edit-start="true"
                  :data-source="baseEmployee"
                  @saved="methods.onSaved"
                  @row-updating="methods.injectImage"
                  @editing-start="methods.onEditStart"
                  @row-inserting="methods.injectImage"
                  @init-new-row="methods.initInsertedRow"
                  @toolbar-preparing="methods.onGrid1ToolbarPreparing"
                  @initialized="evt => methods.initialized(evt, 'employee')"
                  @exporting="methods.onExporting"
                >
                  <dx-grid-toolbar>
                    <dx-item name="addRowButton" />
                    <dx-item template="excelUploadButton" location="after" />
                    <dx-item template="excelSampleDownloadButton" location="after" />
                    <dx-item name="exportButton" />
                  </dx-grid-toolbar>
                  <template #excelUploadButton>
                    <dx-button icon="upload" @click="methods.excelUpload" />
                  </template>
                  <template #excelSampleDownloadButton>
                    <dx-button icon="download" @click="methods.excelSampleDownload" />
                  </template>

                  <dx-column caption="생성일" data-field="created" data-type="date" format="yyyy-MM-dd" :allow-editing="false" :visible="false" />
                  <dx-column caption="사원코드" data-field="emp_code" :allow-editing="true" :visible="false">
                    <dx-required-rule message="사원코드를 입력하세요" />
                    <dx-async-rule message="이미 사용중인 사원코드입니다" :validation-callback="methods.duplicationCheck" />
                  </dx-column>
                  <dx-column caption="부서코드" data-field="fk_department_id" :allow-editing="true">
                    <dx-required-rule message="부서코드를 입력하세요" />
                    <dx-lookup value-expr="id" display-expr="department_name" :data-source="vars.common.department" />
                  </dx-column>
                  <dx-column caption="접속 비밀번호" data-field="emp_password" :visible="false" :allow-editing="true" :editor-options="{ mode: 'password' }">
                    <dx-required-rule message="접속 비밀번호를 입력하세요" />
                    <dx-async-rule message="접속 비밀번호를 입력하세요." :validation-callback="methods.passwordRuleCheck" />
                  </dx-column>
                  <dx-column caption="사원이름" data-field="emp_name" :allow-editing="true" :allow-hiding="false">
                    <dx-required-rule message="사원이름을 입력하세요" />
                  </dx-column>
                  <dx-column caption="주소" data-field="emp_addr" :visible="false" :allow-editing="true" :editor-options="vars.findAddress.columnOptions" />
                  <dx-column caption="상세주소" data-field="emp_addr_detail" :visible="false" :allow-editing="true" />
                  <dx-column caption="우편번호" data-field="emp_addr_zipcode" :visible="false" :allow-editing="true" />
                  <dx-column caption="직통번호" data-field="emp_direct_phone" :allow-editing="true" />
                  <dx-column caption="전화번호" data-field="emp_ext_phone" :visible="false" :allow-editing="true" />
                  <dx-column caption="핸드폰" data-field="emp_mobile" :visible="false" :allow-editing="true" />
                  <dx-column caption="직위코드" data-field="emp_position" :visible="false" :allow-editing="true">
                    <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.common.position_code" />
                  </dx-column>
                  <dx-column caption="이메일" data-field="emp_email" :visible="true" :allow-editing="true" />
                  <dx-column caption="입사일" data-field="emp_joindate" data-type="date" format="yyyy-MM-dd" :allow-editing="true" />
                  <dx-column caption="메모" data-field="memo" :visible="false" :allow-editing="true" />
                  <dx-column caption="영문이름" data-field="emp_name_en" :visible="false" :allow-editing="true" />
                  <dx-column caption="성별" data-field="emp_gender" :visible="false" :allow-editing="true">
                    <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.common.gender" />
                  </dx-column>
                  <dx-column caption="국가코드" data-field="emp_country" :visible="false" :allow-editing="true">
                    <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.common.country_code" />
                  </dx-column>
                  <dx-column caption="퇴사여부" data-field="resignation_yn" :visible="false" :allow-editing="true" />
                  <dx-column caption="퇴사일" data-field="resignation_date" data-type="date" format="yyyy-MM-dd" :visible="false" :allow-editing="true" />
                  <dx-column caption="퇴사코드" data-field="resignation_type" :visible="false" :allow-editing="true">
                    <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.common.resignation_code" />
                  </dx-column>
                  <dx-column caption="그룹코드" data-field="fk_setup_group_auth" :visible="false" :allow-editing="true">
                    <dx-required-rule message="그룹코드를 입력하세요" />
                    <dx-lookup value-expr="id" display-expr="group_name" :data-source="vars.common.group" />
                  </dx-column>

                  <dx-column caption="얼굴사진" data-field="emp_picture_path" :visible="false" :allow-editing="false" />
                  <dx-column caption="서명" data-field="emp_sign_path" :visible="false" :allow-editing="false" />
                  <dx-export :enabled="true" />
                  <dx-editing mode="popup"
                    :use-icons="true"
                    :allow-adding="true"
                    :allow-updating="true"
                    :allow-deleting="true"
                  >
                    <dx-grid-popup 
                      title="사원 정보"
                      :width="840"
                      :height="700"
                      :show-title="true"
                    >
                    </dx-grid-popup>
                    <dx-form
                      :col-count="1"
                      :show-colon-after-label="false"
                      @initialized="evt => methods.initialized(evt, 'edit-form')"
                    >
                      <dx-simple-item>
                        <template #default>
                          <div class="flex-end">
                            <div class="thumb">
                              <div class="thumb-label">사원사진</div>
                              <label for="thumb-file" class="thumb-photo">
                                <img
                                  v-if="vars.image.thumb"
                                  :src="vars.image.thumb"
                                />
                                <div style="text-align: center" v-else>
                                  클릭하여<br />이미지 선택
                                </div>
                              </label>
                            </div>
                            <div class="thumb">
                              <div class="thumb-label">사원사인</div>
                              <label for="sign-file" class="thumb-photo">
                                <img
                                  v-if="vars.image.sign"
                                  :src="vars.image.sign"
                                />
                                <div style="text-align: center" v-else>
                                  클릭하여<br />이미지 선택
                                </div>
                              </label>
                            </div>
                          </div>
                        </template>
                      </dx-simple-item>
                      <dx-group-item :col-count="3">
                        <dx-simple-item data-field="emp_code" />
                        <dx-simple-item data-field="emp_password" />
                        <dx-simple-item data-field="emp_name_en" />

                        <dx-simple-item data-field="emp_name" :col-span="2" />
                        <dx-simple-item data-field="created" />

                        <dx-simple-item data-field="emp_addr" :col-span="2" />
                        <dx-simple-item data-field="emp_gender" />

                        <dx-simple-item data-field="emp_addr_detail" />
                        <dx-simple-item data-field="emp_addr_zipcode" />
                        <dx-simple-item data-field="emp_country" />

                        <dx-simple-item data-field="emp_ext_phone" />
                        <dx-simple-item data-field="emp_direct_phone" />
                        <dx-simple-item data-field="resignation_yn" />

                        <dx-simple-item data-field="emp_mobile" />
                        <dx-simple-item data-field="emp_position" />
                        <dx-simple-item data-field="resignation_date" />

                        <dx-simple-item data-field="emp_email" :col-span="2" />
                        <dx-simple-item data-field="resignation_type" />

                        <dx-simple-item
                          data-field="emp_joindate"
                          :col-span="2"
                        />
                        <dx-simple-item data-field="fk_setup_group_auth" />

                        <dx-simple-item data-field="memo" :col-span="2" />
                        <dx-simple-item data-field="fk_department_id" />
                      </dx-group-item>
                    </dx-form>
                  </dx-editing>
                  <dx-column-chooser mode="select" :enabled="true" />
                  <dx-filter-row :visible="true" />
                  <dx-paging :page-size="20" />
                </dx-data-grid>
              </div>
            </template>
          </dx-item>
        </dx-tab-panel>

        <dx-popup
          title="주소찾기"
          content-template="popup-content"
          v-model:visible="vars.findAddress.popup.value"
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
                @initialized="evt => methods.initialized(evt, 'find-address')"
              >
                <dx-column data-field="road" caption="도로명주소" />
                <dx-column data-field="jibun" caption="지번주소" />
                <dx-column data-field="zip" caption="우편번호" />
                <dx-paging :page-size="20" />
              </dx-data-grid>
            </div>
          </template>
        </dx-popup>
      </div>
    </div>
    <input hidden type="file" id="thumb-file" accept=".png,.jpg" @change="methods.thumbFileChange" />
    <input hidden type="file" id="sign-file" accept=".png,.jpg" @change="methods.signFileChange" />
    <input hidden type="file" ref="excelRef" accept=".xlsx,.xls" @change="methods.excelFileChange" />
  </div>
</template>

<script>
import { confirm, alert } from 'devextreme/ui/dialog';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxTabPanel } from 'devextreme-vue/tab-panel';
import {
  DxDataGrid,
  DxForm,
  DxColumn,
  DxPaging,
  DxLookup,
  DxEditing,
  DxFilterRow,
  DxAsyncRule,
  DxRequiredRule,
  DxColumnChooser,
  DxExport,
  DxPopup as DxGridPopup,
  DxToolbar as DxGridToolbar,
} from 'devextreme-vue/data-grid';
import { DxGroupItem, DxSimpleItem } from 'devextreme-vue/form';
import { DxPopup } from 'devextreme-vue/popup';
import DxTextBox from 'devextreme-vue/text-box';
import { DxButton } from 'devextreme-vue/button';
import {
  baseEmployee,
  baseWarehouse,
  baseDepartment,
  baseCodeLoader,
} from '../../data-source/base';
import FindAddressStore from '../../data-source/find-address';
import { setupGroup } from '../../data-source/setup';
import ApiService from '../../utils/api-service';
import { notifyError } from '../../utils/notify';
import { reactive, ref } from 'vue';
import moment from 'moment';
import { saveAs } from 'file-saver';
import authService from '../../auth';

export default {
  components: {
    DxToolbar,
    DxTextBox,
    DxItem,
    DxTabPanel,
    DxForm,
    DxGroupItem,
    DxSimpleItem,
    DxPopup,
    DxButton,
    DxDataGrid,
    DxColumn,
    DxEditing,
    DxPaging,
    DxColumnChooser,
    DxLookup,
    DxRequiredRule,
    DxAsyncRule,
    DxFilterRow,
    DxGridPopup,
    DxGridToolbar,
    DxExport
  },
  setup() {
    const vars = {}, methods = {};
    const excelRef = ref(null);
    const apiService = new ApiService('/api/mes/v1/excel/base/employee');

    // Vars
    vars.components = {};
    vars.image = reactive({ thumb: null, sign: null });
    vars.editKey = null;
    vars.common = reactive({
      gender: [],
      country_code: [],
      resignation_code: [],
      position_code: [],
      warehouse: [],
      department: [],
      group: [],
      employee: []
    });
    baseEmployee
      .load({
        filter: [['fk_company_id', '=', authService.getCompanyId()]],
        take: 1000,
        skip: 0,
      })
      .then(({ data }) => {
        vars.common.employee = data;
        if (vars.components['group']) vars.components['group'].refresh()
      });

    baseCodeLoader(['성별', '국적', '퇴사사유', '직급']).then(response => {
      vars.common.gender = response['성별'];
      vars.common.country_code = response['국적'];
      vars.common.resignation_code = response['퇴사사유'];
      vars.common.position_code = response['직급'];
    });

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
                const rowIndex = vars.components['employee'].getRowIndexByKey(
                  vars.editKey
                );
                vars.findAddress.keyword = vars.components[
                  'employee'
                ].cellValue(rowIndex, 'emp_addr');
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

    baseWarehouse.load({skip: 0, take: 1000}).then(response => {
      vars.common.warehouse = response.data;
    });

    setupGroup.load().then(response => {
      vars.common.group = response.data;
    });

    // 그룹코드
    // vars.common.group_auth_code = []

    // Methods
    methods.groupRowInit = evt => {
      evt.data.created = moment().format('YYYY-MM-DD HH:mm:ss');
      evt.data.fk_company_id = authService.getCompanyId();
    };

    methods.initInsertedRow = evt => {
      evt.component.columnOption('emp_code', 'allowEditing', true);
      vars.data = evt.data;
      const today = moment().format('YYYY-MM-DD HH:mm:ss');
      evt.data.created = today;
      evt.data.emp_joindate = today;
      evt.data.resignation_yn = false;
      evt.data.fk_company_id = authService.getCompanyId();
    };

    methods.employeeLookup = options => ({
      store: vars.common.employee,
      filter: options.data ? ['fk_department_id', '=', options.data.id] : null,
    });

    methods.initialized = (evt, key) => {
      vars.components[key] = evt.component;
    };

    methods.onEditStart = evt => {
      evt.component.columnOption('emp_code', 'allowEditing', false);
      vars.image.thumb = evt.data.emp_picture_path;
      vars.image.sign = evt.data.emp_sign_path;
      vars.editKey = evt.key;
    };

    methods.injectImage = evt => {
      const sendData = evt.data || evt.newData;
      console.log(sendData);
      // sendData.emp_picture_path = vars.image.thumb
      // sendData.emp_sign_path = vars.image.sign
    };

    methods.onSaved = () => {
      vars.image.thumb = null;
      vars.image.sign = null;
    };

    methods.thumbFileChange = evt => {
      if (!evt.target.files.length) {
        vars.image.thumb = null;
        return;
      }

      const reader = new FileReader();
      reader.readAsDataURL(evt.target.files[0]);
      reader.onload = () => {
        vars.image.thumb = reader.result;
        const rowIndex = vars.components['employee'].getRowIndexByKey(
          vars.editKey
        );
        vars.components['employee'].cellValue(
          rowIndex,
          'emp_picture_path',
          reader.result
        );
      };
      evt.target.value = null;
    };

    methods.signFileChange = evt => {
      if (!evt.target.files.length) {
        vars.image.sign = null;
        return;
      }

      const reader = new FileReader();
      reader.readAsDataURL(evt.target.files[0]);
      reader.onload = () => {
        vars.image.sign = reader.result;
        const rowIndex = vars.components['employee'].getRowIndexByKey(
          vars.editKey
        );
        vars.components['employee'].cellValue(
          rowIndex,
          'emp_sign_path',
          reader.result
        );
      };
      evt.target.value = null;
    };

    methods.tabChanged = evt => {
      baseDepartment.load().then(response => {
        vars.common.department = response.data;
      });
    };

    methods.duplicationCheck = async ({ data, value }) => {
      if (data.id) return true;

      try {
        const response = await baseEmployee.load({
          filter: ['emp_code', '=', value],
        });
        return !response.data.length;
      } catch (ex) {
        return false;
      }
    };
    methods.passwordRuleCheck = async ({ data, value}) => {
      if (!data.id) return true;
      const user = authService.user;
      if (user.user_type == 1) {
       return true;
      }
      else {
        try {
          const api = new ApiService('/api/mes/v1/base/employee/password-rule-check');
          const response = await api.post('', {
            emp_code: data.emp_code,
            emp_password: value
          }); 
          if (response.status == 200) {
            return true;
          }
          else {
            alert('오류가 있습니다. 관리자에게 문의 바랍니다.', '접속 비밀번호 오류');
            return false;
          }
        }
        catch (ex) {
          let message = '오류가 있습니다. 관리자에게 문의 바랍니다.';
          if(ex.response.status == 410){
            message = '접속 비밀번호가 틀립니다.';
            
          }
          else if(ex.response.status == 400){
            message = '사원 로그인 정보가 저장되지 않았습니다. <br/> 관리자 계정으로 로그인 후 접속 비밀번호를 입력 저장 후 사용 가능합니다.';
          }
          else {
            message = '오류가 있습니다. 관리자에게 문의 바랍니다.';
            
          }
          alert(message, '접속 비밀번호 오류');
          return false;
        }
      }
      
    }
    methods.findAddressSubmit = () => {
      vars.findAddress.store.keyword = vars.findAddress.keyword;
      vars.components['find-address'].refresh();
    };

    methods.findAddressSelect = ({ data }) => {
      const rowIndex = vars.components['employee'].getRowIndexByKey(
        vars.editKey
      );
      vars.components['employee'].beginUpdate();
      vars.components['employee'].cellValue(rowIndex, 'emp_addr', data.road);
      vars.components['employee'].cellValue(
        rowIndex,
        'emp_addr_zipcode',
        data.zip
      );
      vars.components['employee'].cellValue(rowIndex, 'emp_addr_detail', '');
      vars.components['employee'].endUpdate();
      vars.findAddress.popup.value = false;
    };

    methods.excelUpload = () => {
      excelRef.value.click();
    };

    methods.excelFileChange = async ({ target }) => {
      if (!target.files.length) return;

      vars.components['employee'].beginCustomLoading(
        '엑셀 데이터를 읽고 있습니다'
      );
      const fd = new FormData();
      fd.append('file', target.files[0]);

      try {
        await apiService.post('', fd);
        vars.components['employee'].refresh();
      } catch (ex) {
        if (ex.response.data) {
          notifyError(ex.response.data);
        }
      } finally {
        vars.components['employee'].endCustomLoading();
        target.value = null;
      }
    };

    methods.excelSampleDownload = () => {
      saveAs('/api/mes/v1/excel/base/employee', '사원입력양식.xlsx');
    };

    methods.onExporting = (evt) => {
      baseEmployee.exportData(evt.component, '사원현황', `사원현황.xlsx`);
      evt.cancel = true;
    };

    methods.onDataError = (e) => {
      if (e.error.response.status == 605) {
        e.error.message = '연결된 데이터가 있어서 삭제가 안됩니다';
      }
    };

    return {
      vars,
      methods,
      excelRef,
      setupGroup,
      baseEmployee,
      baseDepartment,
    };
  },
};
</script>

<style lang="scss" scoped>
.flex-end {
  display: flex;
  justify-content: flex-end;
}
.thumb {
  display: flex;
  align-items: flex-start;
  .thumb-label {
    padding: 5px 10px;
    margin: 0 10px;
    border: 1px solid #ddd;
  }
  .thumb-photo {
    width: 140px;
    height: 100px;
    background-color: #ddd;
    border-radius: 5px;
    overflow: hidden;
    cursor: pointer;

    display: flex;
    align-items: center;
    justify-content: center;

    img {
      width: auto;
      height: 100%;
    }
  }
}
</style>
