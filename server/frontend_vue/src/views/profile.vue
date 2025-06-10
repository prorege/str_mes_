<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings">
        <div class="content-header">
          <dx-toolbar>
            <dx-item location="before">
              <div class="content-title">내 정보 수정</div>
            </dx-item>
          </dx-toolbar>

          <dx-form 
            v-model:form-data="vars.profile"
            :disabled="vars.disabled.value"
            :col-count="5" 
            :show-colon-after-label="false"
            @initialized="(evt) => methods.initialized(evt, 'edit-form')">
            <dx-group-item>
              <dx-simple-item>
                <template #default>
                  <div class="thumb">
                    <label for="thumb-file" class="thumb-photo">
                      <img v-if="vars.profile.emp_picture_path" :src="vars.profile.emp_picture_path"/>
                      <div style="text-align: center" v-else>
                        클릭하여<br>이미지 선택
                      </div>
                    </label>
                    <div class="thumb-label">사진</div>
                  </div>
                </template>
              </dx-simple-item>
              <dx-simple-item>
                <template #default>
                  <div class="thumb">
                    <label for="sign-file" class="thumb-photo">
                      <img v-if="vars.profile.emp_sign_path" :src="vars.profile.emp_sign_path"/>
                      <div style="text-align: center" v-else>
                        클릭하여<br>이미지 선택
                      </div>
                    </label>
                    <div class="thumb-label">서명</div>
                  </div>
                </template>
              </dx-simple-item>
            </dx-group-item>
          
            <dx-group-item :col-count="3" :col-span="4" caption="기본 정보">
              <dx-simple-item data-field="emp_code" caption="사원번호" :editor-options="{readOnly: true}">
                <dx-label text="사원번호"/>
              </dx-simple-item>
              <dx-simple-item data-field="emp_name" caption="이름">
                <dx-label text="이름"/>
              </dx-simple-item>
              <dx-simple-item data-field="emp_name_en" caption="이름(영)">
                <dx-label text="이름(영)"/>
              </dx-simple-item>

              <dx-simple-item data-field="emp_addr" :col-span="2" caption="주소" :editor-options="vars.findAddress.columnOptions">
                <dx-label text="주소"/>
              </dx-simple-item>
              <dx-simple-item data-field="emp_addr_detail" caption="상세주소">
                <dx-label text="상세주소"/>
              </dx-simple-item>

              <dx-simple-item data-field="emp_addr_zipcode" caption="우편번호">
                <dx-label text="우편번호"/>
              </dx-simple-item>
              <dx-simple-item data-field="emp_email" :col-span="2" caption="이메일">
                <dx-label text="이메일"/>
              </dx-simple-item>

              <dx-simple-item data-field="emp_direct_phone" caption="직통번호">
                <dx-label text="직통번호"/>
              </dx-simple-item>
              <dx-simple-item data-field="emp_ext_phone" caption="내선번호">
                <dx-label text="내선번호"/>
              </dx-simple-item>
              <dx-simple-item data-field="emp_mobile" caption="핸드폰">
                <dx-label text="핸드폰"/>
              </dx-simple-item>

              <!--dx-simple-item data-field="emp_password" caption="비밀번호" :editor-options="{ mode: 'password', inputAttr: {autocomplete: 'new-password'}}">
                <dx-label text="비밀번호"/>
              </dx-simple-item>
              <dx-empty-item :col-span="2" /-->

              <dx-group-item :col-span="3">
                <dx-button-item
                  item-type="button"
                  horizontal-alignment="right"
                  :button-options="{text: '저장', type: 'success', onClick: methods.submit_basic}"
                />
              </dx-group-item>
              <dx-group-item caption="비밀번호 변경">
              <dx-simple-item data-field="emp_password" caption="기존 비밀번호" :editor-options="{mode: 'password', inputAttr: {autocomplete: 'new-password'}}">
                <dx-label text="기존 비밀번호"/>
              </dx-simple-item>
              <dx-simple-item data-field="emp_password_new" caption="신규 비밀번호" :editor-options="{mode: 'password', inputAttr: {autocomplete: 'new-password'}}">
                <dx-label text="신규 비밀번호 "/>
              </dx-simple-item>
              <dx-simple-item data-field="emp_password_new2" caption="신규 비밀번호 확인" :editor-options="{mode: 'password', inputAttr: {autocomplete: 'new-password'}}">
                <dx-label text="신규 비밀번호 확인"/>
              </dx-simple-item>
              <dx-group-item :col-span="3">
                <dx-button-item
                  item-type="button"
                  horizontal-alignment="right"
                  :button-options="{text: '비밀번호변경', type: 'success', onClick: methods.submit_passwd}"
                />
              </dx-group-item>
             </dx-group-item> 
            </dx-group-item>
             
          </dx-form>
        </div>
      </div>
    </div>

    <dx-popup
      v-model:visible="vars.findAddress.popup.value"
      content-template="popup-content"
      title="주소찾기"
      :close-on-outside-click="true"
      :width="680" :height="500"
      :resize-enabled="true">
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
            @row-click="methods.findAddressSelect">
            <dx-column data-field="road" caption="도로명주소" />
            <dx-column data-field="jibun" caption="지번주소" />
            <dx-column data-field="zip" caption="우편번호" />
            <dx-paging :page-size="20" />
          </dx-data-grid>
        </div>
      </template>
    </dx-popup>

    <input hidden type="file" id="thumb-file" accept=".png,.jpg" @change="methods.thumbFileChange"/>
    <input hidden type="file" id="sign-file" accept=".png,.jpg" @change="methods.signFileChange"/>
  </div>
</template>

<script>
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar'
import DxForm, {DxGroupItem, DxSimpleItem, DxButtonItem, DxEmptyItem, DxLabel} from "devextreme-vue/form"
import {DxDataGrid, DxColumn, DxPaging} from 'devextreme-vue/data-grid'
import {DxPopup} from 'devextreme-vue/popup'
import DxTextBox from 'devextreme-vue/text-box'
import { confirm } from 'devextreme/ui/dialog'
import {baseEmployee} from '@/data-source/base'
import FindAddressStore from '@/data-source/find-address'
import authService from '@/auth'
import { notifyInfo, notifyError } from '../utils/notify'
import {reactive, ref} from 'vue';

export default {
  components: {
    DxToolbar, DxItem,
    DxForm, DxGroupItem, DxSimpleItem, DxButtonItem, DxEmptyItem, DxLabel,
    DxDataGrid, DxColumn, DxPaging, DxPopup, DxTextBox
  },
  setup() {
    const vars = { profile: reactive({}), disabled: ref(true) }, methods = {}
    vars.origin = {}
    vars.components = {}
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
                vars.findAddress.keyword = vars.profile.emp_addr
                vars.findAddress.popup.value = true
              } 
            }
          }
        ]
      },
      textBoxOptions: [
        {
          name: 'icon', 
          location: 'after', 
          options: { 
            stylingMode: 'text', 
            icon: 'search', 
            onClick: () => {
              methods.findAddressSubmit()
            } 
          }
        }
      ]
    }

    baseEmployee.load({filter: ['emp_code', '=', authService.user.user_id]})
      .then(response => {
        if (!response.data.length) return
        Object.assign(vars.profile, response.data[0])
        vars.origin = response.data[0]
        vars.disabled.value = false
      })
      .catch(ex => {
        console.log(ex)
      })
    
    methods.initialized = (evt, key) => {
      vars.components[key] = evt.component
    }

    methods.thumbFileChange = (evt) => {
      if (!evt.target.files.length) return
      const reader = new FileReader()
      reader.readAsDataURL(evt.target.files[0])
      reader.onload = () => {
        vars.profile.emp_picture_path = reader.result
      }
      evt.target.value = null
    }
    
    methods.signFileChange = (evt) => {
      if (!evt.target.files.length) return
      const reader = new FileReader()
      reader.readAsDataURL(evt.target.files[0])
      reader.onload = () => {
        vars.profile.emp_sign_path = reader.result
      }
      evt.target.value = null
    }

    methods.findAddressSubmit = () => {
      vars.findAddress.store.keyword = vars.findAddress.keyword
      vars.components['find-address'].refresh()
    }

    methods.findAddressSelect = ({data}) => {
      vars.profile.emp_addr = data.road
      vars.profile.emp_addr_zipcode = data.zip
      vars.profile.emp_addr_detail = ''
      vars.findAddress.popup.value = false
    }

    methods.submit_basic = async () => {
      vars.disabled.value = true
      const params = {}
      for (let key in vars.profile) {
        if (vars.origin[key] === vars.profile[key]) continue
        params[key] = vars.profile[key]
      }

      if (Object.keys(params).length) {
        const referer = location.origin + '/base/'
        await baseEmployee.update(vars.profile.id, params, {headers: { 'Referer': '' }})
        notifyInfo('변경되었습니다')
      }
      else {
        notifyError('변경된 내용이 없습니다')
      }
      vars.disabled.value = false
    }

    methods.submit_passwd = async () => {
      if(vars.profile.emp_password == undefined) {
        alert("기존 비밀번호를 입력해 주세요.");
        return false;
      }

      if(vars.profile.emp_password_new == undefined) {
        alert("신규 비밀번호를 입력해 주세요.");
        return false;
      }

      if(vars.profile.emp_password == vars.profile.emp_password_new2) {
        alert("기존 비밀번호와 신규 비밀번호가 일치합니다. 다른 비밀번호를 사용하세요.");
        return false;
      }

      if(vars.profile.emp_password_new != vars.profile.emp_password_new2) {
        alert("신규 비밀번호가 일치하지 않습니다.");
        return false;
      }

      const reg = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/;

      if( !reg.test(vars.profile.emp_password_new) ) {
        alert("최소 8자리(하나 이상의 문자와 하나 이상의 숫자 및 하나 이상의 특수 문자)를 입력해 주세요.");
        return false;
      }

      vars.disabled.value = true
      const params = {}

      if (vars.profile.emp_password) {
        const confirmed = await confirm('비밀번호를 변경하시겠습니까?', '확인');
        if (confirmed) {
          params.emp_password = vars.profile.emp_password
          params.emp_password_new = vars.profile.emp_password_new
        }
      }

      if (Object.keys(params).length) {
        const referer = location.origin + '/base/'
        try {
          await baseEmployee.update(vars.profile.id, params, {headers: { 'Referer': '' }})
        } catch(ex) {
          alert("기존 비밀번호가 다릅니다.")
          vars.disabled.value = false
          return false;
        }
        notifyInfo('비밀번호가 변경되었습니다.')
      }
      else {
        notifyError('변경된 내용이 없습니다')
      }
      vars.disabled.value = false

      vars.profile.emp_password = vars.profile.emp_password_new = vars.profile.emp_password_new2 = undefined
    }

    return { vars, methods };
  }
};
</script>

<style lang="scss" scoped>
.flex-end {
  display: flex;
  justify-content: flex-end;
}
.thumb {
  .thumb-label {
    padding: 5px 10px;
    text-align: center;
  }
  .thumb-photo {
    width: auto; min-height: 180px;
    background-color: #ddd;
    border-radius: 5px;
    overflow: hidden;
    cursor: pointer;

    display: flex;
    align-items: center;
    justify-content: center;

    img {
      width: auto; height: 100%;
    }
  }
}
</style>
