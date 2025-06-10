<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings">
        <div class="content-header">
          <dx-toolbar>
            <dx-item location="before">
              <div class="content-title">통제관리</div>
            </dx-item>
          </dx-toolbar>
        </div>
        <dx-form :form-data="vars.formData" :show-colon-after-label="false">
          <dx-group-item>
            <dx-empty-item />
            <dx-simple-item data-field="not_use_minus_stock">
              <dx-label :text="'(-) 수불 처리 불가'" />
            </dx-simple-item>
            <dx-simple-item data-field="not_use_prereceiving">
              <dx-label :text="'가입고 사용 안함'" />
            </dx-simple-item>
            <dx-simple-item data-field="not_use_lot">
              <dx-label :text="'LOT 사용 안함'" />
            </dx-simple-item>
            <dx-empty-item />
            <dx-simple-item
              :col-span="1"
              :button-options="
                generateItemButtonOption('', methods.saveControl, 'after', {
                  text: '저장',
                  type: 'default',
                  width: '128px',
                  onClick: methods.saveControl,
                })
              "
              item-type="button"
              horizontal-alignment="left"
            ></dx-simple-item>
          </dx-group-item>
        </dx-form>
      </div>
    </div>
  </div>
</template>

<script>
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import {
  DxForm,
  DxLabel,
  DxGroupItem,
  DxSimpleItem,
  DxEmptyItem,
} from 'devextreme-vue/form';
import { onMounted, ref, reactive, computed, watch, nextTick } from 'vue';
import { generateItemButtonOption } from '../../utils/util';
import authService from '../../auth';
import { setupControl, getSetupControl } from '../../data-source/setup';
import { notifyInfo, notifyError } from '../../utils/notify';

export default {
  components: {
    DxToolbar,
    DxItem,
    DxForm,
    DxLabel,
    DxGroupItem,
    DxSimpleItem,
    DxEmptyItem,
  },
  setup() {
    const vars = { dlg: {} };
    vars.formData = reactive({
      id: null,
      not_use_minus_stock: false,
      not_use_prereceiving: false,
      not_use_lot: false,
    });

    onMounted(async () => {
      const data = await setupControl.load({
        filter: [['fk_company_id', '=', authService.getCompanyId()]],
        take: 1,
        skip: 0,
      });
      if (data.data.length <= 0) {
        vars.formData.id = null;
        vars.formData.not_use_minus_stock = false;
        vars.formData.not_use_prereceiving = false;
        vars.formData.not_use_lot = false;
        vars.formData.fk_company_id = authService.getCompanyId();
      } else {
        Object.assign(vars.formData, data.data[0]);
      }
    });

    const methods = {
      async saveControl() {
        try {
          if (!vars.formData.id) {
            const insertDate = Object.assign({}, vars.formData);
            delete insertDate.id;
            const { data } = await setupControl.insert(insertDate);
            vars.formData.id = data.id;
            notifyInfo('저장되었습니다');
          } else {
            const updateDate = Object.assign({}, vars.formData);
            await setupControl.update(vars.formData.id, updateDate);
            notifyInfo('저장되었습니다');
          }
        } catch (ex) {
          console.error(ex);
          notifyError('저장 할 내용이 없습니다');
        }
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
