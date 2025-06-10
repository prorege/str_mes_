<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings">
        <div class="content-header">
          <dx-toolbar>
            <dx-item location="before"
              ><div class="content-title">코드변경관리</div></dx-item
            >
            <dx-item
              location="after"
              locate-in-menu="auto"
              widget="dxButton"
              :options="{ text: '수정', onClick: methods.editCode }"
            />
          </dx-toolbar>
        </div>
        <dx-form :form-data="vars.formData"
          >"
          <dx-group-item :col-count="3">
            <dx-group-item>
              <dx-simple-item
                data-field="change_type"
                :editor-options="{
                  searchEnabled: false,
                  dataSource: vars.types,
                  valueExpr: 'type',
                  displayExpr: 'name',
                  onValueChanged: methods.onTypeChanged,
                }"
                :validation-rules="vars.validationRules.type"
                editor-type="dxSelectBox"
              >
                <dx-label text="분류" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item
                data-field="previous_code"
                :editor-options="{
                  ...generateItemButtonOption(
                    'search',
                    methods.createFindPopupFn(vars.select.type, '코드조회')
                  ),
                  disabled: !vars.select.type,
                }"
              >
                <dx-label text="변경전" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item data-field="after_code">
                <dx-label text="변경후" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
          </dx-group-item>
          <dx-group-item :col-count="1">
            <dx-simple-item data-field="change_reason">
              <dx-label text="변경사유" :show-colon="false" />
            </dx-simple-item>
            <dx-simple-item data-field="name" :visible="false">
              <dx-label text="이름" :show-colon="false" />
            </dx-simple-item>
          </dx-group-item>
        </dx-form>
      </div>
    </div>
    <div class="content-block">
      <div class="dx-card responsive-paddings">
        <dx-tab-panel>
          <dx-item title="품목코드 변경 이력" icon="cart">
            <template #default>
              <div class="tab-first">
                <code-item-history />
              </div>
            </template>
          </dx-item>
          <dx-item title="업체코드 변경 이력" icon="home">
            <template #default>
              <div class="tab-second">
                <code-client-history />
              </div>
            </template>
          </dx-item>
        </dx-tab-panel>
      </div>
    </div>

    <dx-popup
      v-model:visible="vars.dlg.finder.show"
      content-template="popup-content"
      :title="vars.dlg.finder.title"
      :close-on-outside-click="true"
      :width="680"
      :height="500"
      :key="vars.dlg.finder.key"
      :resize-enabled="true"
      @initialized="evt => methods.onGridInitialized(evt, 'find-popup')"
    >
      <template #popup-content>
        <data-grid-item
          v-if="vars.dlg.finder.key == '1'"
          @change="methods.finderReturnHandler"
        />
        <data-grid-client
          v-else-if="vars.dlg.finder.key == '2'"
          @change="methods.finderReturnHandler"
        />
      </template>
    </dx-popup>
  </div>
</template>

<script>
import DxTabPanel, { DxItem } from 'devextreme-vue/tab-panel';
import DxToolbar from 'devextreme-vue/toolbar';
import {
  DxForm,
  DxLabel,
  DxGroupItem,
  DxSimpleItem,
} from 'devextreme-vue/form';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';

import { generateItemButtonOption } from '../../utils/util';

import DataGridClient from '../../components/base/data-client.vue';
import DataGridItem from '../../components/base/data-item.vue';

import CodeItemHistory from './code-item-history.vue';
import CodeClientHistory from './code-client-history.vue';

import { reactive } from 'vue';
import stateStore from '@/utils/state-store';
import authService from '../../auth';
import ApiService from '../../utils/api-service';

import { setupCodeChangeHistory } from '../../data-source/setup';

export default {
  components: {
    DxTabPanel,
    DxItem,
    DxToolbar,
    DxForm,
    DxLabel,
    DxGroupItem,
    DxSimpleItem,
    DxPopup,
    DxToolbarItem,
    CodeItemHistory,
    CodeClientHistory,
    DataGridItem,
    DataGridClient,
  },
  setup() {
    const apiService = new ApiService('/api/mes/v1/setup/change_code');
    const vars = { dlg: {} };
    vars.types = reactive([
      { type: 1, name: '품목코드' },
      { type: 2, name: '업체코드' },
    ]);
    vars.select = reactive({
      type: null,
    });
    vars.validationRules = reactive({
      type: [{ type: 'required', message: '분류를 선택하세요' }],
    });
    vars.formData = reactive({
      change_type: '',
      previous_code: '',
      after_code: '',
      change_reason: '',
      name: '',
    });
    vars.grid = {};
    vars.dlg.addItem = reactive({ show: false });
    vars.dlg.finder = reactive({
      show: false,
      title: '',
      key: null,
      data: null,
    });

    const methods = {
      editCode() {
        const params = {
          change_type: vars.formData.change_type,
          previous_code: vars.formData.previous_code,
          after_code: vars.formData.after_code,
          name: vars.formData.name,
          change_reason: vars.formData.change_reason,
          manager: authService.getUserName(),
          fk_company_id: authService.getCompanyId(),
        };
        apiService.post('', params);
        //setupCodeChangeHistory.insert(params);
      },
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`code-status-${key}`, evt.component);
      },
      onTypeChanged(e) {
        vars.select.type = e.value;
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
      finderReturnHandler(data) {
        switch (vars.dlg.finder.key) {
          case 1: {
            vars.formData.previous_code = data.item_code;
            vars.formData.name = data.item_name;
            break;
          }
          case 2: {
            vars.formData.previous_code = data.alias;
            vars.formData.name = data.name;
            break;
          }
        }
        vars.dlg.finder.show = false;
        vars.dlg.finder.title = '';
        vars.dlg.finder.key = null;
        vars.dlg.finder.data = null;
      },
    };

    return {
      vars,
      methods,
      generateItemButtonOption,
    };
  },
};
</script>

<style>
.tab-first,
.tab-second {
  padding: 8px;
}
</style>
