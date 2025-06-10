<template>
  <div v-if="vars.init.value">
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">검사등록관리</div>
            </dx-item>

            <dx-item widget="dxButton" location="after" locate-in-menu="auto"
              :options="{ text: '신규', type: 'add', icon: 'add', onClick: methods.newItem }"
            />
            <dx-item widget="dxButton" location="after" locate-in-menu="auto"
              :options="{ text: '수정', type: 'rename', icon: 'rename', disabled: !vars.formData.id, onClick: methods.editItem }" />
            <dx-item widget="dxButton" location="after" locate-in-menu="auto"
              :options="{ text: '삭제', type: 'remove', icon: 'remove', disabled: !vars.formData.id, onClick: methods.deleteItem }" />
            <dx-item widget="dxButton" location="after" locate-in-menu="auto"
              :options="{ text: '저장', type: 'save', icon: 'save', disabled: !vars.formData.worker, onClick: methods.saveItem }" />
          </dx-toolbar>
        </div>

        <div class="form-wrap">
          <dx-form
            :form-data="vars.formData"
            :show-colon-after-label="false"
            @initialized="evt => methods.initialized(evt, 'test-reg-form')"
          >
            <template #avatar-template="{}">
              <div class="form-avatar"></div>
            </template>

            <dx-group-item :col-count="5" css-class="first-group">
              <dx-group-item :col-span="3">
                <dx-group-item :col-count="2">
                  <dx-group-item :col-span="1">
                    <dx-group-item :col-count="2">
                      <dx-button-item
                        :button-options="{
                          text: '수입검사',
                          type: 'success',
                          width: '100%',
                          disabled: vars.disabled.setTestType,
                          onClick: methods.createFindPopupFn(
                            'receiving',
                            '수입검사'
                          ),
                        }"
                      />
                      <dx-button-item
                        :button-options="{
                          text: '출하검사',
                          type: 'success',
                          width: '100%',
                          disabled: vars.disabled.setTestType,
                          onClick: methods.createFindPopupFn(
                            'performance',
                            '출하검사'
                          ),
                        }"
                      />
                    </dx-group-item>
                    <dx-simple-item
                      editor-type="dxTextBox"
                      :editor-options="{
                        placeholder: '(QR Code Scan)',
                        ...vars.formState,
                        ...methods.generateItemButtonOption(
                          'fullscreen',
                          methods.openScanner
                        ),
                      }"
                    >
                      <dx-label text="바코드입력" />
                    </dx-simple-item>
                    <dx-simple-item
                      data-field="qa_number"
                      :editor-options="{
                        placeholder: '(자동 or 직접입력)',
                        ...vars.formState,
                        ...methods.generateItemButtonOption(
                          'search',
                          methods.createFindPopupFn(
                            'test-registration',
                            '검사조회'
                          )
                        ),
                      }"
                    >
                      <dx-label :text="'검사번호'" />
                    </dx-simple-item>
                    <dx-simple-item
                      data-field="qa_date"
                      editor-type="dxDateBox"
                      :editor-options="{
                        dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                        ...vars.formState,
                      }"
                    >
                      <dx-label :text="'검사일자'" />
                    </dx-simple-item>

                    <dx-empty-item />

                    <dx-simple-item
                      data-field="item_code"
                      :editor-options="{ readOnly: true }"
                    >
                      <dx-label :text="'품목코드'" />
                    </dx-simple-item>
                    <dx-simple-item
                      data-field="item_name"
                      :editor-options="{ readOnly: true }"
                    >
                      <dx-label :text="'품명'" />
                    </dx-simple-item>
                    <dx-simple-item
                      data-field="standard"
                      :editor-options="{ readOnly: true }"
                    >
                      <dx-label :text="'규격'" />
                    </dx-simple-item>
                  </dx-group-item>
                  <dx-group-item :col-span="1">
                    <dx-simple-item
                      data-field="qa_manager"
                      editor-type="dxSelectBox"
                      :editor-options="{
                        dataSource: vars.common.employee,
                        displayExpr: 'emp_name',
                        valueExpr: 'emp_name',
                        acceptCustomValue: true,
                        ...vars.formState,
                      }"
                    >
                      <dx-label :text="'검사자'" />
                      <dx-required-rule message="검사자를 선택하세요" />
                    </dx-simple-item>
                    <dx-simple-item
                      data-field="test_type"
                      :editor-options="{ readOnly: true }"
                    >
                      <dx-label :text="'검사구분'" />
                    </dx-simple-item>
                    <dx-simple-item
                      data-field="ref_number"
                      :editor-options="{ readOnly: true }"
                    >
                      <dx-label :text="vars.refNumber.value" />
                    </dx-simple-item>

                    <dx-empty-item />

                    <dx-simple-item
                      data-field="worker"
                      editor-type="dxSelectBox"
                      :editor-options="{
                        dataSource: vars.common.employee,
                        displayExpr: 'emp_name',
                        valueExpr: 'emp_name',
                        acceptCustomValue: true,
                        readOnly: true,
                      }"
                    >
                      <dx-label :text="'작업자'" />
                    </dx-simple-item>
                    <dx-simple-item
                      data-field="lot_no"
                      :editor-options="{ ...vars.formState }"
                    >
                      <dx-label :text="'LOT NO.'" />
                    </dx-simple-item>
                    <dx-simple-item
                      data-field="qa_standard_path"
                      template="attachment"
                    >
                      <dx-label :text="'검사성적서'" />
                    </dx-simple-item>
                  </dx-group-item>
                  <dx-simple-item
                    data-field="process_quantity"
                    editor-type="dxNumberBox"
                    :editor-options="{ readOnly: true }"
                  >
                    <dx-label :text="'검사수량'" />
                  </dx-simple-item>
                  <dx-simple-item
                    data-field="bad_quantity"
                    editor-type="dxNumberBox"
                    :editor-options="{
                      readOnly: true,
                      ...methods.generateItemButtonOption(
                        'refresh',
                        methods.updateBadCount
                      ),
                    }"
                  >
                    <dx-label :text="'불량수량'" />
                  </dx-simple-item>
                  <dx-simple-item
                    data-field="action_quantity"
                    editor-type="dxNumberBox"
                    :editor-options="{ readOnly: true }"
                  >
                    <dx-label :text="'재작업수량'" />
                  </dx-simple-item>
                  <dx-simple-item
                    data-field="good_quantity"
                    editor-type="dxNumberBox"
                    :editor-options="{ readOnly: true }"
                  >
                    <dx-label :text="'양품수량'" />
                  </dx-simple-item>
                </dx-group-item>
              </dx-group-item>
              <dx-simple-item :col-span="2" template="badItems" />
            </dx-group-item>

            <template #badItems>
              <dx-data-grid
                class="bad-case-grid"
                :data-source="qualityNonconformanceAction"
                :show-borders="true"
                :column-auto-width="true"
                :remote-operations="true"
                :allow-column-resizing="true"
                :allow-column-reordering="true"
                @initialized="evt => methods.initialized(evt, 'bad-case-grid')"
                @init-new-row="methods.initNewBadCase"
                @saving="methods.onSaving"
              >
                <!-- <dx-column data-field="id" data-type="number" caption="UID" :vi /> -->
                <dx-column caption="수량" data-field="bad_quantity" data-type="number" />
                <dx-column caption="불량유형" data-field="bad_type">
                  <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.common.bad_type" />
                </dx-column>
                <dx-column caption="불량사유" data-field="bad_reason" />

                <dx-grid-toolbar>
                  <dx-grid-item text="불량 등록" location="before" />
                  <dx-grid-item name="addRowButton" />
                  <dx-grid-item name="revertButton" />
                </dx-grid-toolbar>

                <dx-editing
                  :allow-adding="!vars.formState.readOnly"
                  :allow-updating="!vars.formState.readOnly"
                  :allow-deleting="!vars.formState.readOnly"
                  :use-icons="true"
                  mode="batch"
                />
                <dx-scrolling mode="standard" />
              </dx-data-grid>
            </template>

            <template #attachment>
              <dx-button
                text="다운로드"
                :disabled="!vars.formData.qa_standard_path"
                @click="
                  methods.attachmentDownload(vars.formData.qa_standard_path)
                "
              />
              &nbsp;
              <dx-button
                text="업로드"
                :disabled="vars.formState.readOnly"
                @click="methods.attachmentUpload()"
              />
            </template>
          </dx-form>
        </div>
      </div>
    </div>

    <dx-popup
      v-model:visible="vars.dlg.finder.show"
      content-template="popup-content"
      :title="vars.dlg.finder.title"
      :close-on-outside-click="true"
      :width="680"
      :height="320"
      :key="vars.dlg.finder.key"
      :resize-enabled="true"
      @initialized="evt => methods.initialized(evt, 'multiuse-popup')"
    >
      <template #popup-content>
        <data-grid-prereceiving-item
          v-if="vars.dlg.finder.key === 'receiving'"
          :fixed-filter="[{ name: 'check_yn', op: 'eq', val: false }]"
          @change="methods.finderReturnHandler"
        />
        <data-grid-performance-registration-item
          v-else-if="vars.dlg.finder.key === 'performance'"
          :fixed-filter="[{ name: 'check_yn', op: 'eq', val: false }]"
          @change="methods.finderReturnHandler"
        />
        <data-grid-test-registration
          v-else-if="vars.dlg.finder.key === 'test-registration'"
          @change="methods.finderReturnHandler"
        />
      </template>
    </dx-popup>

    <qr-reader v-if="vars.showQrReader.value" @read="methods.onReadQrData" />

    <input type="file" ref="upload" @change="methods.uploadFileChange" hidden />
  </div>
</template>

<script>
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import DxTextArea from 'devextreme-vue/text-area';
import {
  DxForm,
  DxLabel,
  DxGroupItem,
  DxButtonItem,
  DxSimpleItem,
  DxEmptyItem,
  DxRequiredRule,
} from 'devextreme-vue/form';
import {
  DxDataGrid,
  DxColumn,
  DxSelection,
  DxEditing,
  DxPaging,
  DxFilterRow,
  DxScrolling,
  DxColumnChooser,
  DxLookup,
  DxToolbar as DxGridToolbar,
  DxItem as DxGridItem,
} from 'devextreme-vue/data-grid';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import DxButton from 'devextreme-vue/button';
import notify from 'devextreme/ui/notify';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import { confirm, alert } from 'devextreme/ui/dialog';
import { ref, computed, reactive, watch, nextTick, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import QrReader from '@/components/qr/reader';
import stateStore from '@/utils/state-store';
import {
  baseCodeLoader,
  baseClient,
  baseItem,
  baseEmployee,
} from '../../data-source/base';
import {
  qualityTestRegistration,
  qualityNonconformanceAction,
} from '../../data-source/quality';
import DataGridPrereceivingItem from '../../components/purchase/data-prereceiving-item.vue';
import DataGridTestRegistration from '../../components/quality/data-test-registration.vue';
import DataGridPerformanceRegistrationItem from '../../components/produce/data-performance-registration-item.vue';
import authService from '../../auth';
import ApiService from '../../utils/api-service';
import { saveAs } from 'file-saver';
import { notifyInfo } from '../../utils/notify';
import { beforeExitConfirm, currentDateTime } from '../../utils/util';

export default {
  components: {
    DxToolbar,
    DxItem,
    DxButton,
    DxTextArea,
    DxLoadPanel,
    DxForm,
    DxLabel,
    DxGroupItem,
    DxButtonItem,
    DxSimpleItem,
    DxEmptyItem,
    DxRequiredRule,
    DxDataGrid,
    DxEditing,
    DxColumn,
    DxSelection,
    DxPaging,
    DxPopup,
    DxToolbarItem,
    DxFilterRow,
    DxScrolling,
    DxColumnChooser,
    DataGridPrereceivingItem,
    DataGridPerformanceRegistrationItem,
    DataGridTestRegistration,
    DxGridToolbar,
    DxGridItem,
    DxLookup,
    QrReader,
  },
  props: {
    id: [String, Number],
  },
  setup(props) {
    // variable 설정
    const router = useRouter();
    const upload = ref();
    const vars = { dlg: {} };
    const fileUploadService = new ApiService(
      '/api/mes/v1/quality/quality_management_upload'
    );
    vars.init = ref(false);
    vars.loading = ref(false);
    vars.formState = reactive({ readOnly: true });
    vars.disabled = reactive({
      edit: true,
      delete: true,
      save: true,
      setTestType: true,
    });
    vars.components = {};
    vars.dlg.finder = reactive({
      show: false,
      title: '',
      key: null,
      data: null,
    });
    vars.common = {
      employee: [],
      bad_type: [],
    };
    vars.formData = reactive({
      id: null,
      qa_number: '',
      qa_date: '',
      equipment: '',
      item_code: '',
      item_name: '',
      test_type: '',
      ref_number: '',
      standard: '',
      qa_manager: '',
      qa_count: '',
      process_name: '',
      worker: '',
      lot_no: '',
      qa_standard_path: '',
      process_quantity: '',
      bad_quantity: '',
      good_quantity: '',
      action_quantity: '',
      fk_company_id: null,

      fk_work_order_id: null,
      fk_performance_id: null,
      fk_performance_item1_id: null,
    });
    vars.attachment = null;

    vars.refNumber = computed(() => {
      if (vars.formData.test_type === '수입검사') return '가입고번호';
      else if (vars.formData.test_type === '출하검사') return '생산입고번호';
      return '번호';
    });

    vars.showQrReader = ref(false);

    qualityNonconformanceAction.defaultFilters = [
      { name: 'fk_quality_management_id', op: 'eq', val: 0 },
      { name: 'fk_company_id', op: 'eq', val: authService.getCompanyId() },
    ];

    onMounted(() => {
      beforeExitConfirm.check(() => !vars.disabled.save)
    })

    !(async () => {
      const { data: employee } = await baseEmployee.load();
      vars.common.employee = employee;
      const response = await baseCodeLoader(
        ['불량유형'],
        authService.getCompanyId()
      );
      vars.common.bad_type = response['불량유형'];
      vars.init.value = true;
    })();

    // public methods
    const methods = {
      async initById(id) {
        vars.disabled.setTestType = true;

        if (!id) {
          vars.formData.id = null;
          vars.formData.qa_number = '';
          vars.formData.qa_date = '';
          vars.formData.equipment = '';
          vars.formData.item_code = '';
          vars.formData.item_name = '';
          vars.formData.test_type = '';
          vars.formData.ref_number = '';
          vars.formData.standard = '';
          vars.formData.qa_manager = '';
          vars.formData.qa_count = 0;
          vars.formData.process_name = '';
          vars.formData.worker = '';
          vars.formData.lot_no = '';
          vars.formData.qa_standard_path = '';
          vars.formData.process_quantity = 0;
          vars.formData.bad_quantity = 0;
          vars.formData.good_quantity = 0;
          vars.formData.action_quantity = 0;
          vars.formData.fk_company_id = null;
          vars.attachment = null;

          vars.formData.fk_work_order_id = null;
          vars.formData.fk_performance_id = null;
          vars.formData.fk_performance_item1_id = null;
          qualityNonconformanceAction.defaultFilters[0].val = 0;
          return;
        }

        vars.attachment = null;
        let { data } = await qualityTestRegistration.byKey(id);
        Object.assign(vars.formData, data);
        qualityNonconformanceAction.defaultFilters[0].val = id;
        if (vars.components['bad-case-grid'])
          vars.components['bad-case-grid'].refresh();
      },
      initialized(evt, key) {
        vars.components[key] = evt.component;
        stateStore.bind(key, evt.component);
      },
      generateItemSelectOption(items = [], value = '', searchEnabled = false) {
        return { value, searchEnabled, items };
      },
      generateItemButtonOption(
        icon,
        callback,
        location = 'after',
        options = {},
        defaultButtonOptions = {}
      ) {
        let buttonOptions = {
          stylingMode: 'text',
          icon,
          onClick: callback,
          ...defaultButtonOptions,
        };
        if (!('disabled' in buttonOptions)) buttonOptions.disabled = false;

        return {
          ...options,
          buttons: [{ name: icon, location, options: buttonOptions }],
        };
      },
      createFindPopupFn(key, title, data = null) {
        const _key = key,
          _title = title,
          _data = data;
        return () => {
          vars.dlg.finder.key = _key;
          vars.dlg.finder.data = _data;
          vars.dlg.finder.title = _title;
          vars.dlg.finder.show = true;
        };
      },
      async newItem() {
        if (vars.formData.id) {
          router.replace('/quality/test-registration');
          if (vars.components['test-reg-form'])
            vars.components['test-reg-form'].resetValues();
        }

        setTimeout(() => {
          vars.formData.qa_date = currentDateTime();
          vars.formData.qa_manager = authService.getUserName();
          vars.formData.fk_company_id = authService.getCompanyId();

          vars.formState.readOnly = false;
          vars.disabled.setTestType = false;
        }, 200);
      },
      async editItem() {
        if (!vars.formData.id) return;
        if (vars.formState.readOnly) {
          let isSelect = await confirm('수정하시겠습니까?', '수정');
          if (!isSelect) {
            return;
          }
        }

        const saveFormData = Object.assign({}, vars.formData);
        vars.formState.readOnly = !vars.formState.readOnly;

        await nextTick();
        Object.assign(vars.formData, saveFormData);
      },
      finderReturnHandler(data) {
        switch (vars.dlg.finder.key) {
          case 'receiving': {
            vars.formData.item_code = data.item_code;
            vars.formData.item_name = data.item.item_name;
            vars.formData.standard = data.item.item_standard;

            vars.formData.worker = data.prereceiving.receiving_manager;
            vars.formData.lot_no = undefined;
            vars.formData.test_type = '수입검사';
            vars.formData.ref_number = data.prereceiving.prereceiving_number;
            vars.formData.qa_standard_path = undefined;

            vars.formData.process_quantity = data.prereceiving_quantity; // data.check_quantity
            vars.formData.bad_quantity = 0;
            vars.formData.action_quantity = 0;
            vars.formData.good_quantity = data.prereceiving_quantity; // data.check_quantity
            vars.formData.item = data.item;
            vars.formData.prereceiving = data.prereceiving;
            vars.formData.fk_prereceiving_item = data.id;
            break;
          }
          case 'performance': {
            vars.formData.item_code = data.item_code;
            vars.formData.item_name = data.item.item_name;
            vars.formData.standard = data.item.item_standard;

            vars.formData.worker = data.work_order
              ? data.work_order.manager
              : authService.getUserName();
            vars.formData.lot_no = undefined;
            vars.formData.test_type = '출하검사';
            vars.formData.ref_number = data.performance_registration.number;
            vars.formData.qa_standard_path = undefined;

            vars.formData.process_quantity = data.production_receiving_quantity;
            vars.formData.bad_quantity = 0;
            vars.formData.action_quantity = 0;
            vars.formData.good_quantity = data.production_receiving_quantity;
            vars.formData.item = data.item;
            vars.formData.fk_performance_registration_item = data.id;

            vars.formData.fk_work_order_id = data.work_order
              ? data.work_order.id
              : null;
            vars.formData.fk_performance_id =
              data.fk_performance_registration_id;
            vars.formData.fk_performance_item1_id = data.id;
            break;
          }
          case 'test-registration': {
            // Object.assign(vars.formData, data)
            router.replace({ path: `/quality/test-registration/${data.id}` });
            vars.formState.readOnly = true;
            break;
          }
        }

        vars.dlg.finder.show = false;
        vars.dlg.finder.title = '';
        vars.dlg.finder.key = null;
        vars.dlg.finder.data = null;
      },
      async saveItem() {
        methods.updateBadCount();
        if (vars.formData.good_quantity < 0) {
          notify(
            { message: '불량수량은 검사수량보다 클 수 없습니다', width: 450 },
            'error',
            2000
          );
          return;
        }
        if (!vars.formData.test_type) {
          notify(
            { message: '검사내용을 입력해 주세요', width: 450 },
            'error',
            2000
          );
          return;
        }

        vars.loading.value = true;
        try {
          const updateDate = Object.assign({}, vars.formData);
          delete updateDate.id;
          delete updateDate.created;
          delete updateDate.qa_number;
          delete updateDate.item;
          delete updateDate.prereceiving;
          delete updateDate.fk_work_order_id;
          delete updateDate.fk_performance_id;
          delete updateDate.fk_performance_item1_id;

          if (vars.formData.id) {
            // 기존 정보 업데이트
            const { data } = await qualityTestRegistration.update(
              vars.formData.id,
              updateDate
            );
            vars.formData.qa_number = data.qa_number;
            await vars.components['bad-case-grid'].saveEditData();

            if (vars.attachment) {
              const fd = new FormData();
              fd.append('file', vars.attachment);
              const { data: filename } = await fileUploadService.patch(
                String(vars.formData.id),
                fd
              );
              vars.formData.qa_standard_path = filename;
              vars.attachment = null;
            }
            notifyInfo('저장되었습니다');
          } else {
            let { data } = await qualityTestRegistration.insert(updateDate);
            vars.formData.id = data.id;
            vars.formData.qa_number = data.qa_number;
            await vars.components['bad-case-grid'].saveEditData();

            if (vars.attachment) {
              const fd = new FormData();
              fd.append('file', vars.attachment);
              const { data: filename } = await fileUploadService.patch(
                String(data.id),
                fd
              );
              vars.formData.qa_standard_path = filename;
              vars.attachment = null;
            }
            beforeExitConfirm.clear()
            router.replace({ path: `/quality/test-registration/${data.id}` });
            notifyInfo('저장되었습니다');
          }

          vars.formState.readOnly = true;
          vars.disabled.setTestType = true;
        } catch (ex) {
          console.error(ex);
          notify(
            { message: '저장 할 내용이 없습니다', width: 450 },
            'error',
            2000
          );
          vars.formState.readOnly = false;
          vars.disabled.setTestType = false;
        } finally {
          vars.loading.value = false;
        }
      },
      async deleteItem() {
        const result = await confirm(
          '이 항목을 삭제하시겠습니까?',
          '삭제 확인'
        );
        if (result) {
          const rows = vars.components['bad-case-grid'].getVisibleRows();
          for (const row of rows) {
            await qualityNonconformanceAction.remove(row.key);
          }
          await qualityTestRegistration.remove(vars.formData.id);
          beforeExitConfirm.clear()
          await alert('삭제되었습니다', '삭제 확인');
          router.replace({ path: `/quality/test-registration` });
          vars.formState.readOnly = true;
        }
      },
      initNewBadCase(evt) {
        evt.data.bad_quantity = 0;
        evt.data.bad_type = vars.common.bad_type[0].code_name;
        if (vars.formData.id)
          evt.data.fk_quality_management_id = vars.formData.id;
      },
      updateBadCount() {
        if (!vars.formState.readOnly && vars.components['bad-case-grid']) {
          const rows = vars.components['bad-case-grid'].getVisibleRows();
          const badQty = rows.reduce(
            (sum, row) => sum + row.data.bad_quantity,
            0
          );
          vars.formData.bad_quantity = badQty;
          vars.formData.good_quantity = vars.formData.process_quantity - badQty;
        }
      },
      attachmentDownload() {
        saveAs(
          `/api/mes/v1/quality/quality_management_download/${vars.formData.qa_standard_path}`,
          vars.formData.qa_standard_path.split('__')[1]
        );
      },
      attachmentUpload() {
        upload.value.click();
      },
      uploadFileChange({ target }) {
        if (target.files.length) {
          vars.attachment = target.files[0];
          notifyInfo(`"${vars.attachment.name}"이 선택되었습니다`);
        } else vars.attachment = null;
        target.value = null;
      },
      onSaving(evt) {
        evt.changes.forEach(row => {
          if (row.type === 'insert') {
            row.data.qa_manager = vars.formData.qa_manager;
            row.data.fk_item_code = vars.formData.item.id;
            row.data.fk_quality_management_id = vars.formData.id;
            row.data.fk_company_id = authService.getCompanyId();
            row.data.done = false;
            if (vars.formData.fk_work_order_id) {
              row.data.fk_work_order_id = vars.formData.fk_work_order_id;
              row.data.fk_performance_id = vars.formData.fk_performance_id;
              row.data.fk_performance_item1_id =
                vars.formData.fk_performance_item1_id;
            }
          } else {
            console.log(row);
          }
        });
        console.log(evt.changes);
      },
      openScanner() {
        console.log('openScanner');
        vars.showQrReader.value = true;
      },
      onReadQrData(data) {
        vars.showQrReader.value = false;
        if (!data) notify('스캔이 취소됬습니다', 'warning', 2000);
        else notify(`${data.data}`, 'info', 2000);
      },
    };

    methods.initById(props.id);
    watch(
      () => props.id,
      () => methods.initById(props.id)
    );

    return {
      upload,
      vars,
      methods,
      baseItem,
      baseClient,
      qualityTestRegistration,
      qualityNonconformanceAction,
    };
  },
};
</script>
<style lang="scss" scoped>
.form-wrap {
  /* max-width: 780px; */
}
.form-avatar {
  height: 312px;
  width: 100%;
  border: 1px solid #d2d3d5;
  border-radius: 0%;
  background-size: 90%;
  background-repeat: no-repeat;
  background-position: center;
}

.bad-case-grid:deep {
  .dx-datagrid-borders > .dx-datagrid-header-panel {
    background-color: #f7f7f7;
  }
  .dx-datagrid-header-panel .dx-toolbar {
    background-color: #f7f7f7;
  }
}
</style>
