<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings">
        
        <div class="content-header">
          <dx-toolbar>
            <dx-item location="before">
              <div class="content-title">은행관리</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <dx-data-grid
          :show-borders="true"
          :show-row-lines="true"
          :column-auto-width="true"
          :remote-operations="true"
          :hover-state-enabled="true"
          :focused-row-enabled="true"
          :data-source="baseBank"
          :on-initialized="evt => methods.onInitialized(evt, 'bank')"
          @init-new-row="methods.groupRowInit"
        >
          <dx-column caption="은행코드" data-field="bank_code">
            <dx-required-rule message="은행코드를 입력하세요" />
          </dx-column>
          <dx-column caption="은행이름" data-field="bank_name">
            <dx-required-rule message="은행이름을 입력하세요" />
          </dx-column>
          <dx-column caption="계좌번호" data-field="account_number" />
          <dx-column caption="은행주소" data-field="bank_address" />
          <dx-column caption="IBAN Code" data-field="iban_code" />
          <dx-column caption="BLZ No" data-field="blz_no" />
          <dx-column caption="SWIFT Code" data-field="swift_code" />
          <dx-column caption="비고" data-field="note" />

          <dx-editing mode="popup"
            :use-icons="true"
            :allow-adding="true"
            :allow-updating="true"
            :allow-deleting="true"
          >
            <dx-grid-popup 
              title="은행관리"
              :width="840"
              :height="400"
              :show-title="true"
            />
            <dx-form
              :col-count="1"
              :show-colon-after-label="false"
              @initialized="evt => methods.onInitialized(evt, 'edit-form')"
            >
              <dx-group-item :col-count="2">
                <dx-simple-item data-field="bank_code" />
                <dx-simple-item data-field="iban_code" />

                <dx-simple-item data-field="bank_name" />
                <dx-simple-item data-field="blz_no" />

                <dx-simple-item data-field="account_number" />
                <dx-simple-item data-field="swift_code" />

                <dx-simple-item data-field="bank_address" />
                <dx-simple-item data-field="note" />
              </dx-group-item>
            </dx-form>
          </dx-editing>
          <dx-filter-row :visible="true" />
          <dx-paging :enabled="true" :page-size="20" />
          <dx-column-chooser mode="select" :enabled="true" />
        </dx-data-grid>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment';

import { reactive, onMounted } from 'vue';

import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxDataGrid, DxForm, DxColumn, DxPaging, DxButton, DxEditing, DxFilterRow, DxColumnChooser, DxRequiredRule, DxPopup as DxGridPopup, } from 'devextreme-vue/data-grid';
import { DxGroupItem, DxSimpleItem } from 'devextreme-vue/form';

import authService from '../../auth';
import { baseBank } from '../../data-source/base';

export default {
  components: {
    DxToolbar, DxItem,
    DxDataGrid, DxForm, DxColumn, DxPaging, DxButton, DxEditing, DxFilterRow, DxColumnChooser, DxRequiredRule, DxGridPopup,
    DxGroupItem, DxSimpleItem,
  },
  setup() {
    const vars = {};
    vars.components = {};

    onMounted(() => {});

    var methods = {
      onInitialized(evt, key) {
        vars.components[key] = evt.component;
      },
      groupRowInit(e) {
        e.data.created = moment().format('YYYY-MM-DD HH:mm:ss');
        e.data.fk_company_id = authService.getCompanyId();
      },
    };

    return {
      vars,
      methods,
      baseBank,
    };
  },
};
</script>

<style></style>
