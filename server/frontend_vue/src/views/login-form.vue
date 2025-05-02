<template>
  <form class="login-form" @submit.prevent="onSubmit">
    <dx-form :form-data="formData" :disabled="loading">
      <dx-item
        data-field="user_id"
        editor-type="dxTextBox"
        :editor-options="{ stylingMode: 'filled', placeholder: '아이디', mode: 'text' }">
        <dx-required-rule message="아이디를 입력해 주세요" />
        <dx-label :visible="false" />
      </dx-item>
      <dx-item
        data-field='user_pw'
        editor-type='dxTextBox'
        :editor-options="{ stylingMode: 'filled', placeholder: '패스워드', mode: 'password' }">
        <dx-required-rule message="Password is required" />
        <dx-label :visible="false" />
      </dx-item>
      <dx-item
        data-field="rememberMe"
        editor-type="dxCheckBox"
        :editor-options="{ text: '아이디 저장하기', elementAttr: { class: 'form-text' } }">
        <dx-label :visible="false" />
      </dx-item>
      <dx-button-item>
        <dx-button-options
          width="100%"
          type="default"
          template="signInTemplate"
          :use-submit-behavior="true">
        </dx-button-options>
      </dx-button-item>
      <dx-item>
        <template #default>
          <dx-button-group
            :items="viewRoleOption"
            :selected-item-keys="[defViewRole]"
            key-expr="role"
            styling-mode="text"
            width="100%"
            @item-click="viewRoleSelected"
          />
        </template>
      </dx-item>
      <template #signInTemplate>
        <div>
          <span class="dx-button-text">
            <dx-load-indicator v-if="loading" width="24px" height="24px" :visible="true" />
            <span v-if="!loading">로그인</span>
          </span>
        </div>
      </template>
    </dx-form>
  </form>
</template>

<script>
import DxLoadIndicator from "devextreme-vue/load-indicator";
import DxButtonGroup from 'devextreme-vue/button-group';
import DxForm, {
  DxItem,
  DxRequiredRule,
  DxLabel,
  DxButtonItem,
  DxButtonOptions
} from "devextreme-vue/form";
import notify from 'devextreme/ui/notify'
import auth from "../auth"

import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default {
  setup() {
    
    const route = useRoute()
    const router = useRouter()

    let viewRole = 'user'
    const viewRoleOption = [
      { type: 'default', text: '사용자', role: 'user', hint: '사용자 화면' },
      { type: 'default', text: 'P D A', role: 'mobile', hint: 'PDA 화면' },
      { type: 'default', text: 'Kiosk', role: 'kiosk', hint: '키오스크 화면' }
    ]
    const formData = reactive({
      user_id: '',
      user_pw: ''
    });
    const loading = ref(false);

    const defViewRole = (() => {
      let role = sessionStorage.getItem('viewrole')
      if (!role) {
        if (/android/i.test(navigator.userAgent)) role = 'mobile'
        else role = 'user'
      }
      return role
    })()
    viewRole = defViewRole

    function onCreateAccountClick() {
      router.push("/create-account");
    }

    async function onSubmit () {
      const {user_id, user_pw} = formData
      loading.value = true
      const result = await auth.logIn(user_id, user_pw)

      if (!result.isOk) {
        loading.value = false;
        notify(result.message, "error", 2000);
      } else {
        sessionStorage.setItem('viewrole', viewRole)
        if (viewRole === 'mobile') router.push('/shipment/on-site');
        else if (viewRole === 'kiosk') {
          if(result.data.department.id === 10) {
              router.push('/produce/process_performance_registration_vietnam');
              document.body.requestFullscreen()
          }else{
              router.push('/produce/process-performance-registration');
              document.body.requestFullscreen()
          }
        }
        else router.push(route.query.redirect || '/home');
      }
    }

    async function onSubmitEx() {
      const { email, password } = formData;
      loading.value = true;
      const result = await auth.logIn(email, password);
      if (!result.isOk) {
        loading.value = false;
        notify(result.message, "error", 2000);
      } else {
        router.push(route.query.redirect || "/home");
      }
    }

    function viewRoleSelected ({itemData}) {
      viewRole = itemData.role
    }

    return {
      formData,
      loading,
      viewRole,
      defViewRole,
      viewRoleOption,
      viewRoleSelected,
      onCreateAccountClick,
      onSubmit,
      onSubmitEx
    };
  },
  components: {
    DxLoadIndicator,
    DxButtonGroup,
    DxForm,
    DxRequiredRule,
    DxItem,
    DxLabel,
    DxButtonItem,
    DxButtonOptions
  }
};
</script>

<style lang="scss">
@import "../themes/generated/variables.base.scss";

.login-form {
  .link {
    text-align: center;
    font-size: 16px;
    font-style: normal;

    a {
      text-decoration: none;
    }
  }

  .form-text {
    margin: 10px 0;
    color: rgba($base-text-color, alpha($base-text-color) * 0.7);
  }
}
</style>
