<template>
  <dx-form :form-data="vars.company" :show-colon-after-label="false">
    <template #avatar-template="{}">
      <div
        class="form-avatar"
        :style="{
          backgroundImage: `url(data:;base64,${vars.company.logo})`,
        }"
      />
    </template>
    <dx-group-item :col-count="7" css-class="first-group">
      <dx-group-item :col-span="1">
        <dx-simple-item template="avatar-template" />
        <dx-simple-item
          :button-options="
            methods.generateItemButtonOption('', methods.saveCompany, 'after', {
              text: '로고 변경',
              type: 'default',
              width: '128px',
              onClick: methods.popupChangeLogo,
            })
          "
          item-type="button"
          horizontal-alignment="left"
        ></dx-simple-item>
      </dx-group-item>
      <dx-group-item :col-span="3">
        <dx-simple-item data-field="name"
          ><dx-label :text="'업체명'"
        /></dx-simple-item>
        <dx-simple-item data-field="ceo_name"
          ><dx-label :text="'대표자명'"
        /></dx-simple-item>
        <dx-simple-item data-field="corp_number"
          ><dx-label :text="'법인번호'"
        /></dx-simple-item>
        <dx-simple-item data-field="business_status"
          ><dx-label :text="'업태'"
        /></dx-simple-item>
      </dx-group-item>
      <dx-group-item :col-span="3">
        <dx-simple-item data-field="name_en"
          ><dx-label :text="'업체명(영문)'"
        /></dx-simple-item>
        <dx-simple-item data-field="ceo_name_en"
          ><dx-label :text="'대표자명(영문)'"
        /></dx-simple-item>
        <dx-simple-item data-field="business_number"
          ><dx-label :text="'사업자번호'"
        /></dx-simple-item>
        <dx-simple-item data-field="business_sector"
          ><dx-label :text="'종목'"
        /></dx-simple-item>
      </dx-group-item>
    </dx-group-item>

    <dx-group-item :col-count="2" css-class="second-group">
      <dx-group-item :col-span="1">
        <dx-simple-item data-field="phone"
          ><dx-label :text="'대표전화번호'"
        /></dx-simple-item>
        <dx-simple-item data-field="fax"
          ><dx-label :text="'팩스번호'"
        /></dx-simple-item>
        <dx-simple-item data-field="email"
          ><dx-label :text="'이메일'"
        /></dx-simple-item>
      </dx-group-item>
      <dx-group-item :col-span="1">
        <dx-simple-item data-field="phone_en"
          ><dx-label :text="'전화번호(국제)'"
        /></dx-simple-item>
        <dx-simple-item data-field="fax_en"
          ><dx-label :text="'팩스번호(국제)'"
        /></dx-simple-item>
        <dx-simple-item data-field="homepage"
          ><dx-label :text="'홈페이지'"
        /></dx-simple-item>
      </dx-group-item>
      <dx-group-item :col-span="2">
        <dx-group-item :col-count="4">
          <dx-simple-item
            :col-span="3"
            data-field="address"
            :editor-options="
              methods.generateItemButtonOption('find', methods.findAddress)
            "
            ><dx-label :text="'주소'"
          /></dx-simple-item>
          <dx-simple-item data-field="zip_code"
            ><dx-label :text="'우편번호'"
          /></dx-simple-item>
        </dx-group-item>
        <dx-simple-item data-field="address_en">
          <dx-label :text="'주소(영문)'" />
        </dx-simple-item>
      </dx-group-item>
    </dx-group-item>

    <dx-group-item :col-count="2" css-class="third-group">
      <dx-group-item :col-span="1">
        <dx-simple-item data-field="bill_manager">
          <dx-label :text="'계산서담당자'" />
        </dx-simple-item>
        <dx-simple-item
          data-field="system_start_date"
          editor-type="dxDateBox"
          :editor-options="vars.datetimeOptions"
        >
          <dx-label :text="'시스템시작일'" />
        </dx-simple-item>
        <dx-simple-item
          data-field="basic_stock_date"
          editor-type="dxDateBox"
          :editor-options="vars.datetimeOptions"
        >
          <dx-label :text="'기초재고등록일'" />
        </dx-simple-item>
        <dx-simple-item
          data-field="register_id"
          :editor-options="{ readOnly: true }"
        >
          <dx-label :text="'최초등록자'" />
        </dx-simple-item>
      </dx-group-item>
      <dx-group-item :col-span="1">
        <dx-simple-item data-field="bill_email">
          <dx-label :text="'계산서이메일'" />
        </dx-simple-item>
        <dx-simple-item
          data-field="last_updated_date"
          editor-type="dxDateBox"
          :editor-options="vars.datetimeOptions"
        >
          <dx-label :text="'최종수정일자'" />
        </dx-simple-item>
        <dx-simple-item
          data-field="basic_balance_date"
          editor-type="dxDateBox"
          :editor-options="vars.datetimeOptions"
        >
          <dx-label :text="'기초잔액등록일'" />
        </dx-simple-item>
        <dx-simple-item
          data-field="modify_id"
          :editor-options="{ readOnly: true }"
        >
          <dx-label :text="'최종수정자'" />
        </dx-simple-item>
      </dx-group-item>
    </dx-group-item>
    <dx-group-item :col-count="4" css-class="fourth-group">
      <dx-empty-item :col-span="3" />
      <dx-simple-item
        :col-span="1"
        :button-options="
          methods.generateItemButtonOption('', methods.saveCompany, 'after', {
            text: '저장',
            type: 'default',
            width: '128px',
            onClick: methods.saveCompany,
          })
        "
        item-type="button"
        horizontal-alignment="right"
      ></dx-simple-item>
    </dx-group-item>
  </dx-form>
  <div id="app-container">
    <dx-popup
      id="popup"
      content-template="popup-content"
      v-model:visible="vars.logoUpload.popupVisible"
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
              vars.logoUpload.isDropZoneActive
                ? 'dx-theme-accent-as-border-color dropzone-active'
                : 'dx-theme-border-color',
            ]"
          >
            <img
              id="dropzone-image"
              :src="vars.logoUpload.imageSource"
              v-if="vars.logoUpload.imageSource"
              alt=""
            />
            <div
              id="dropzone-text"
              class="flex-box"
              v-if="vars.logoUpload.textVisible"
            >
              <span>새로운 로고를 끌어다 놓으세요.</span>
            </div>
            <dx-progress-bar
              id="upload-progress"
              :min="0"
              :max="100"
              width="30%"
              :show-status="false"
              :visible="vars.logoUpload.progressVisible"
              :value="vars.logoUpload.progressValue"
            />
          </div>
          <dx-file-uploader
            id="file-uploader"
            dialog-trigger="#dropzone-external"
            drop-zone="#dropzone-external"
            :multiple="false"
            :allowed-file-extensions="vars.logoUpload.allowedFileExtensions"
            upload-mode="instantly"
            upload-url="/api/server/v1/logo-upload"
            :visible="false"
            @drop-zone-enter="methods.logo.onDropZoneEnter"
            @drop-zone-leave="methods.logo.onDropZoneLeave"
            @uploaded="methods.logo.onUploaded"
            @progress="methods.logo.onProgress"
            @upload-started="methods.logo.onUploadStarted"
            @value-changed="methods.logo.onValueChanged($event)"
          />
        </div>
      </template>
    </dx-popup>
  </div>
  <dx-toast
    v-model:visible="vars.toast.visible"
    v-model:message="vars.toast.message"
    v-model:type="vars.toast.type"
    :width="vars.toast.width"
  />
</template>

<script>
import {
  DxForm,
  DxLabel,
  DxGroupItem,
  DxSimpleItem,
  DxEmptyItem,
} from 'devextreme-vue/form';
import { DxPopup } from 'devextreme-vue/popup';
import { DxFileUploader } from 'devextreme-vue/file-uploader';
import { DxProgressBar } from 'devextreme-vue/progress-bar';
import { DxToast } from 'devextreme-vue/toast';

import { onBeforeMount, reactive } from 'vue';
import ApiService from '../../utils/api-service';
import authService from '../../auth';

export default {
  components: {
    DxForm,
    DxGroupItem,
    DxSimpleItem,
    DxEmptyItem,
    DxLabel,
    DxPopup,
    DxFileUploader,
    DxProgressBar,
    DxToast,
  },
  setup() {
    onBeforeMount(() => {
      methods.getCompany();
    });

    const vars = reactive({
      logoUpload: {
        isDropZoneActive: false,
        imageSource: '',
        textVisible: true,
        progressVisible: false,
        progressValue: 0,
        allowedFileExtensions: ['.jpg', '.jpeg', '.gif', '.png'],
        popupVisible: false,
      },
      toast: {
        visible: false,
        message: '저장이 완료되었습니다.',
        type: 'success',
        width: 'auto',
      },
      datetimeOptions: {
        type: 'datetime',
      },
      company: {
        name: '',
        name_en: '',
        ceo_name: '',
        ceo_name_en: '',
        corp_number: '',
        business_number: '',
        business_status: '',
        business_sector: '',
        phone: '',
        phone_en: '',
        fax: '',
        fax_en: '',
        email: '',
        homepage: '',
        address: '',
        address_en: '',
        zip_code: '',
        bill_manager: '',
        bill_email: '',
        system_start_date: '',
        basic_stock_date: '',
        last_updated_date: '',
        basic_balance_date: '',
        register_id: '',
        modify_id: '',
        logo: '',
      },
    });

    const methods = {
      getCompany: async () => {
        let { data, status, statusText } = await methods.apiGetCompany();
        if (methods.isApiSuccess(status, statusText)) {
          methods.setCompany(data);
        }
      },
      apiGetCompany: async () => {
        const apiService = new ApiService('/api/mes/v1/common');
        return await apiService.get(
          `companies/${authService._user.fk_company_id}`
        );
      },
      isApiSuccess: (status, statusText) => {
        if (status === 200 && statusText === 'OK') {
          return true;
        }
        return false;
      },
      setCompany: data => {
        vars.company.name = data.name;
        vars.company.name_en = data.name_en;
        vars.company.ceo_name = data.ceo_name;
        vars.company.ceo_name_en = data.ceo_name_en;
        vars.company.corp_number = data.corp_number;
        vars.company.business_number = data.business_number;
        vars.company.business_status = data.business_status;
        vars.company.business_sector = data.business_sector;
        vars.company.phone = data.phone;
        vars.company.phone_en = data.phone_en;
        vars.company.fax = data.fax;
        vars.company.fax_en = data.fax_en;
        vars.company.email = data.email;
        vars.company.homepage = data.homepage;
        vars.company.address = data.address;
        vars.company.address_en = data.address_en;
        vars.company.zip_code = data.zip_code;
        vars.company.bill_manager = data.bill_manager;
        vars.company.bill_email = data.bill_email;
        vars.company.system_start_date = new Date(data.system_start_date);
        vars.company.basic_stock_date = new Date(data.basic_stock_date);
        vars.company.last_updated_date = new Date(data.last_updated_date);
        vars.company.basic_balance_date = new Date(data.basic_balance_date);
        vars.company.register_id = data.register_id;
        vars.company.modify_id = data.modify_id;
        vars.company.logo = data.logo;
      },
      saveCompany: () => {
        let params = methods.clone(vars.company);
        params = methods.updateDateFormatForSave(params);
        params.modify_id = authService._user.user_id;
        if (!params.register_id) {
          params.register_id = authService._user.user_id;
        }
        methods.apiUpdateCompany(params);
      },
      clone: obj => {
        let output = {};
        for (let i in obj) {
          output[i] = obj[i];
        }
        return output;
      },
      updateDateFormatForSave: params => {
        params.system_start_date = methods.formattedDate(
          params.system_start_date
        );
        params.basic_stock_date = methods.formattedDate(
          params.basic_stock_date
        );
        params.last_updated_date = methods.formattedDate(
          params.last_updated_date
        );
        params.basic_balance_date = methods.formattedDate(
          params.basic_balance_date
        );
        return params;
      },
      formattedDate: date => {
        return `${date.getFullYear()}-${date.getMonth() +
          1}-${date.getDate()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()}`;
      },
      apiUpdateCompany: async params => {
        const apiService = new ApiService('/api/mes/v1/common');
        apiService
          .patch(`companies/${authService._user.fk_company_id}`, params)
          .then(response => {
            if (response.status == 200) {
              methods.showSaveSuccessToast();
            } else {
              methods.showSaveFailToast();
            }
            methods.getCompany();
          });
      },
      showSaveSuccessToast: () => {
        vars.toast.message = '저장이 완료되었습니다.';
        vars.toast.type = 'success';
        vars.toast.visible = true;
      },
      showSaveFailToast: () => {
        vars.toast.message = '저장이 실패했습니다.';
        vars.toast.type = 'fail';
        vars.toast.visible = true;
      },
      findAddress: () => {
        console.log('findAddress');
      },
      popupChangeLogo: () => {
        if (vars.logoUpload.popupVisible == false) {
          vars.logoUpload.popupVisible = true;
        }
      },
      generateItemButtonOption: (
        icon,
        callback,
        location = 'after',
        options = {}
      ) => {
        let buttonOptions = { stylingMode: 'text', icon, onClick: callback };
        return {
          ...options,
          buttons: [{ name: icon, location, options: buttonOptions }],
        };
      },
      logo: {
        onDropZoneEnter: e => {
          if (e.dropZoneElement.id === 'dropzone-external') {
            vars.logoUpload.isDropZoneActive = true;
          }
        },
        onDropZoneLeave: e => {
          if (e.dropZoneElement.id === 'dropzone-external') {
            vars.logoUpload.isDropZoneActive = false;
          }
        },
        onUploaded: e => {
          const file = e.file;
          const fileReader = new FileReader();
          fileReader.onload = () => {
            vars.logoUpload.isDropZoneActive = false;
            vars.logoUpload.imageSource = fileReader.result;
          };
          fileReader.readAsDataURL(file);
          vars.logoUpload.textVisible = false;
          vars.logoUpload.progressVisible = false;
          vars.logoUpload.progressValue = 0;

          methods.getCompany();
        },
        onProgress: e => {
          vars.logoUpload.progressValue = (e.bytesLoaded / e.bytesTotal) * 100;
        },
        onUploadStarted: () => {
          vars.logoUpload.imageSource = '';
          vars.logoUpload.progressVisible = true;
        },
        onValueChanged: e => {
          var url = e.component.option('uploadUrl');
          url = url + '/' + authService._user.fk_company_id;
          e.component.option('uploadUrl', url);
        },
      },
    };

    return {
      vars,
      methods,
    };
  },
};
</script>

<style>
.first-group,
.second-group,
.third-group,
.fourth-group {
  padding: 20px;
}
.second-group,
.third-group {
  background-color: rgba(191, 191, 191, 0.15);
}
.third-group,
.fourth-group {
  margin-top: 10px;
}
.form-avatar {
  height: 128px;
  width: 128px;
  margin-right: 10px;
  border: 1px solid #d2d3d5;
  border-radius: 5%;
  background-size: 90%;
  background-repeat: no-repeat;
  background-position: center;
}
#dropzone-external {
  width: 310px;
  height: 350px;
  background-color: rgba(183, 183, 183, 0.1);
  border-width: 2px;
  border-style: dashed;
  padding: 10px;
}
#dropzone-external > * {
  pointer-events: none;
}
#dropzone-external.dropzone-active {
  border-style: solid;
}
.widget-container > span {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 16px;
}
#dropzone-image {
  max-width: 100%;
  max-height: 100%;
}
#dropzone-text > span {
  font-weight: 100;
  opacity: 0.5;
}
#upload-progress {
  display: flex;
  margin-top: 10px;
}
.flex-box {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
