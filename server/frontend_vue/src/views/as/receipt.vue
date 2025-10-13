<template>
    <div v-if="vars.init.value">
      <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
      <div class="content-block">
        <div class="dx-card responsive-paddings back-colored">
          <div class="content-header">
            <dx-toolbar class="back-colored">
              <dx-item location="before"
                ><div class="content-title">A/S접수</div></dx-item
              >
              <dx-item
                location="after"
                locate-in-menu="auto"
                widget="dxButton"
                :options="{
                  text: '신규',
                  type: 'add',
                  icon: 'add',
                  onClick: methods.newItem,
                  visible: true
                }"
              />
              <dx-item
                location="after"
                locate-in-menu="auto"
                widget="dxButton"
                :options="{
                  text: '수정',
                  type: 'rename',
                  icon: 'rename',
                  disabled: vars.disabled.edit,
                  onClick: methods.editItem,
                }"
              />
              <dx-item
                location="after"
                locate-in-menu="auto"
                widget="dxButton"
                :options="{
                  text: '삭제',
                  type: 'remove',
                  icon: 'remove',
                  disabled: vars.disabled.delete,
                  onClick: methods.deleteItem,
                }"
              />
              <dx-item
                location="after"
                locate-in-menu="auto"
                widget="dxButton"
                :options="{
                  text: '저장',
                  type: 'save',
                  icon: 'save',
                  disabled: vars.disabled.save,
                  onClick: methods.saveItem,
                }"
              />
            </dx-toolbar>
          </div>
          <dx-form
          :form-data="vars.formData">
            <dx-group-item :col-count="4">
              <dx-group-item>
                <dx-simple-item
                  data-field="receipt_number"
                  :editor-options="{
                    onValueChanged: methods.onValueChanged,
                    placeholder: '(자동 or 직접입력)',
                    ...methods.generateItemButtonOption(
                      'search',
                      methods.createFindPopupFn('receipt_number', 'A/S접수조회')
                    ),
                  }"
                >
                  <dx-label text="A/S접수번호" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item
                  data-field="project_management.project_number"
                  :editor-options="{
                    ...vars.formState,
                    onValueChanged: methods.onValueChanged,
                    ...methods.generateItemButtonOption(
                      'search',
                      methods.createFindPopupFn('project', '프로젝트조회')
                    ),
                  }"
                >
                  <dx-label text="프로젝트번호" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item
                  data-field="project_management.project_name"
                  editor-type="dxTextBox"
                  :editor-options="{
                    ...vars.formState,
                    onValueChanged: methods.onValueChanged,
                    ...methods.generateItemButtonOption(
                      'search',
                      methods.createFindPopupFn('project', '프로젝트조회')
                    ),
                  }"
                >
                  <dx-label text="프로젝트 명" :show-colon="false" />
                </dx-simple-item>
                  <dx-simple-item 
                  data-field="receipt_manager" 
                  editor-type="dxTextBox" 
                  :editor-options="{
                      ...vars.formState,
                    }">
                  <dx-label text="접수 담당자" :show-colon="false" />
                </dx-simple-item>
              </dx-group-item>
              <dx-group-item>
                <dx-simple-item
                  data-field="project_management.order_company"
                  :editor-options="{
                    readOnly: true,
                  }"
                >
                  <dx-label text="계약업체" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item
                  data-field="project_management.contract_company"
                  :editor-options="{
                    readOnly: true,
                  }"
                >
                  <dx-label text="수요기관" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item
                  data-field="department"
                  editor-type="dxSelectBox"
                  :editor-options="{
                    dataSource: vars.dataSource.department,
                    displayExpr: 'department_name',
                    valueExpr: 'department_name',
                    onValueChanged: methods.selectDepartment,
                    ...vars.formState,
                  }"
                >
                  <dx-label text="등록부서" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item
                  data-field="manager"
                  editor-type="dxSelectBox"
                  :editor-options="{
                    onValueChanged: methods.onValueChanged,
                    dataSource: vars.dataSource.employee,
                    displayExpr: 'emp_name',
                    valueExpr: 'emp_name',
                    ...vars.formState,
                  }"
                >
                  <dx-label text="등록담당자" :show-colon="false" />
                </dx-simple-item>
              </dx-group-item>
  
              <dx-group-item>
                <dx-simple-item
                  data-field="project_management.contract_date"
                  editor-type="dxDateBox"
                  :editor-options="{
                    dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                    showClearButton: true,
                    useMaskBehavior: true,
                    readOnly: true,
                  }"
                >
                  <dx-label text="계약일자" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item
                  data-field="project_management.defect_end_date"
                  editor-type="dxDateBox"
                  :editor-options="{
                    dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                    showClearButton: true,
                    useMaskBehavior: true,
                    readOnly: true,
                  }"
                >
                  <dx-label text="하자만기" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item
                    data-field="client_manager"
                    editor-type="dxTextBox"
                    :editor-options="{
                        ...vars.formState,
                    }"
                >
                    <dx-label text="고객사 담당자" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item
                    data-field="receipt_date"
                    editor-type="dxDateBox"
                    :editor-options="{
                        dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                        showClearButton: true,
                        useMaskBehavior: true,
                        ...vars.formState,
                    }"
                >
                    <dx-label text="접수일자" :show-colon="false" />
                </dx-simple-item>
              </dx-group-item>
              <dx-group-item>
                <dx-simple-item
                  data-field="project_management.completion_date"
                  editor-type="dxDateBox"
                  :editor-options="{
                    dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                    showClearButton: true,
                    useMaskBehavior: true,
                    readOnly: true,
                  }"
                >
                  <dx-label text="준공일자" :show-colon="false" />
                </dx-simple-item>
                
                <dx-simple-item
                  data-field="project_management.defect_period" 
                  editor-type="dxTextBox"
                  :editor-options="{
                    readOnly: true,
                  }"
                >
                  <dx-label text="하자기간" :show-colon="false" />
                </dx-simple-item>
                
                <dx-simple-item data-field="client_manager_phone" editor-type="dxTextBox"
                  :editor-options="{
                    ...vars.formState,
                  }"
                >
                  <dx-label text="담당자 연락처" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item data-field="paid_type" editor-type="dxSelectBox"
                  :editor-options="{
                    dataSource: vars.dataSource.paid_type,
                    displayExpr: 'code_name',
                    valueExpr: 'code_name',
                    ...vars.formState,
                  }">
                    <dx-label text="유무상 구분" :show-colon="false" />
                  </dx-simple-item>
              </dx-group-item>
            </dx-group-item>
            <dx-group-item :col-count=4>
              <dx-group-item :col-span=4>
                <dx-simple-item data-field="receipt_detail" :editor-options="{
                  ...vars.formState,
                }">
                  <dx-label text="접수내용" :show-colon="false" />
                </dx-simple-item>
              </dx-group-item>
            </dx-group-item>
          </dx-form>
        </div>
  
        <div class="dx-card responsive-paddings mt-1">
          <dx-tab-panel 
            :animation-enabled="false" 
            :swipe-enabled="false" 
            :defer-rendering="false" 
          >
            <dx-item title="담당자 지정">
              <template #default>
                <div class="pa-2">
                  <dx-data-grid
                    class="fixed-header-table"
                    height="calc(100vh - 516px)"
                    data-serialization-format="yyyy-MM-ddTHH:mm:ss"
                    column-resizing-mode="widget"
                    :show-borders="true"
                    :remote-operations="false"
                    :column-auto-width="true"
                    :focused-row-enabled="true"
                    :allow-column-resizing="true"
                    :allow-column-reordering="true"
                    :row-alternation-enabled="true"
                    :select-text-onedit-start="true"
                    :data-source="vars.dataSource.item"
                    :on-initialized="evt => methods.onGridInitialized(evt, 'item')"
                    @saving="methods.onSavingItem"
                    @data-error-occurred="methods.onDataError"
                    @init-new-row="methods.initNewRow"
                    >
                    <dx-grid-toolbar>
                        <dx-grid-item template="addItemRowButton" location="after" :visible="!vars.formState.readOnly" />
                        <dx-grid-item template="itemSaveButton" location="after" :visible="false" />
                        <dx-grid-item name="revertButton" location="after" />
                    </dx-grid-toolbar>
                    <template #addItemRowButton>
                        <dx-button text="담당자 추가" icon="add" @click="methods.addItemRowButton('item')" />
                    </template>
                    <template #itemSaveButton>
                        <dx-button text="저장" icon="save" @click="methods.itemSaveButton('item')" />
                    </template>
                    <dx-column type="buttons" :visible="!vars.formState.readOnly"/>
                    <dx-column caption="담당자" data-field="manager" width="100" />
                    <dx-column caption="담당자 연락처" data-field="manager_phone" />
                    <dx-scrolling mode="standard" />
                    <dx-editing mode="batch"
                      :use-icons="true"
                      :allow-adding="!vars.formState.readOnly"
                      :allow-updating="!vars.formState.readOnly"
                      :allow-deleting="!vars.formState.readOnly"
                      />
                  </dx-data-grid>
                </div>
              </template>
            </dx-item>
          </dx-tab-panel>
        </div>
      </div>
      <dx-popup
        v-model:visible="vars.dlg.finder.show"
        content-template="popup-content"
        width="60%"
        height="60%"
        :title="vars.dlg.finder.title"
        :close-on-outside-click="true"
        :key="vars.dlg.finder.key"
        :resize-enabled="true"
        @initialized="evt => methods.onGridInitialized(evt, 'find-popup')"
      >
        <template #popup-content>
          <data-grid-as-receipt
            v-if="vars.dlg.finder.key === 'receipt_number'"
            @change="methods.finderReturnHandler"
          />
          <data-grid-project v-else-if="vars.dlg.finder.key === 'project'" @change="methods.finderReturnHandler" />
  
      
        </template>
      </dx-popup>
      <dx-popup
          title="거래처정보"
          content-template="popup-client-detail"
          v-model:visible="vars.disabled.clientDetail"
          width="70%"
          height="80%"
          :resize-enabled="true"
          :close-on-outside-click="true"
          @initialized="evt => methods.onGridInitialized(evt, 'find-popup-client-detail')"
          >
          <template #popup-client-detail>
              <popup-client-detail :client-name="vars.dataSource.clientDetail"/>
          </template>
      </dx-popup>
    </div>
</template>

<script>
import moment from 'moment';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import DxTextArea from 'devextreme-vue/text-area';
import {
    DxForm,
    DxLabel,
    DxGroupItem,
    DxSimpleItem,
    DxEmptyItem,
    DxRequiredRule,
} from 'devextreme-vue/form';
import {
    DxSorting,
    DxDataGrid,
    DxColumn,
    DxEditing,
    DxSelection,
    DxFilterRow,
    DxPaging,
    DxLookup,
    DxScrolling,
    DxColumnChooser,
    DxToolbar as DxGridToolbar,
    DxItem as DxGridItem,
    DxButton as DxGridButton
} from 'devextreme-vue/data-grid';
import { DxTabPanel } from 'devextreme-vue/tab-panel';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxTextBox, DxButton as DxTextBoxButton } from 'devextreme-vue/text-box';
import { DxButton } from 'devextreme-vue/button';
import { DxFileUploader } from 'devextreme-vue/file-uploader';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import { confirm, alert } from 'devextreme/ui/dialog';
import { onMounted, ref, reactive, computed, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import stateStore from '@/utils/state-store';
import {
baseCodeLoader,
baseClient,
baseItem,
baseDepartment,
baseEmployee,
baseClientManager
} from '../../data-source/base';
import DataGridClient from '../../components/base/data-client.vue';
import DataGridAsReceipt from '../../components/as/data-as-receipt.vue';
import DataGridClientManager from '../../components/base/data-client-manager.vue';
import DataGridEmployee from '../../components/base/data-employee.vue';
import authService from '../../auth';
import { notifyInfo, notifyError } from '../../utils/notify';
import { currentDateTime } from '../../utils/util';
import PopupClientDetail from '@/components/base/popup-client-detail';
import { loadEmployee, loadWarehouse, loadDepartment, loadClientManager } from '../../utils/data-loader';
import { DxNumberBox } from 'devextreme-vue/number-box';
import { asReceipt, getAsReceiptItem } from '../../data-source/as';
import DataGridProject from '../../components/project/data-project.vue';
export default {
components: {
    DxToolbar,
    DxItem,
    DxTextArea,
    DxLoadPanel,
    DxForm,
    DxSelection,
    DxFilterRow,
    DxLabel,
    DxTextBox,
    DxTextBoxButton,
    DxButton,
    DxFileUploader,
    DxGroupItem,
    DxSimpleItem,
    DxEmptyItem,
    DxTabPanel,
    DxDataGrid,
    DxEditing,
    DxColumn,
    DxLookup,
    DxPopup,
    DxSorting,
    DxToolbarItem,
    DxScrolling,
    DxColumnChooser,
    DxPaging,
    DataGridClient,
    DataGridAsReceipt,
    DxRequiredRule,
    DxGridToolbar,
    DxGridItem,
    PopupClientDetail,
    DataGridClientManager,
    DataGridEmployee,
    DxNumberBox,
    DxGridButton,
    DataGridProject
},
props: {
    id: [String, Number],
},
setup(props) {

    const router = useRouter();
    const vars = { dlg: {} };
    vars.init = ref(true);
    vars.loading = ref(false);
    vars.formState = reactive({ readOnly: true });

    vars.grid = {
        fk_project_management_id : null,
    };
    vars.dlg.finder = reactive({
        show: false,
        title: '',
        key: null,
        data: null,
    });
    vars.formData = reactive({
      id: null,
      created: null,
      receipt_number: '',
      receipt_manager: '',
      receipt_detail: '',
      department: '',
      manager: '',
      client_manager: '',
      client_manager_phone: '',
      receipt_date: '',
      paid_type: '',
      fk_project_management_id: null,
      fk_company_id: authService.getCompanyId(),
      project_management: null,
    });
    vars.filter = {};
    vars.filter.item = [{ name: 'fk_as_receipt_id', op: 'eq', val: props.id || 0 }];
    vars.dataSource = reactive({
      item: getAsReceiptItem(vars.filter.item),
      paid_type: [{ code_name: '유상', code_value: '유상' }, { code_name: '무상', code_value: '무상' }],
      employee: [],
    });

    vars.disabled = reactive({
        edit: true,
        delete: true,
        save: true,
        clientDetail: false,
    });

    
    onMounted(async () => {
        await loadDepartment(vars.dataSource);
       
        methods.initById(props.id);
    
    });

    const methods = {
        async initById(id) {
          methods.gridItemRefresh(id);
          if (!id) {
              methods.clearFormData();
              vars.disabled.edit = true;
              vars.disabled.delete = true;
              vars.disabled.save = true;
              return;
          }

          let { data } = await asReceipt.byKey(id);

          Object.assign(vars.formData, data);
          vars.formState.readOnly = true;
          vars.disabled.edit = false;
          methods.enableDelete();
          methods.enableSave();
        },
        gridItemRefresh(id) {
          vars.dataSource.item.defaultFilters = methods.setIdToGridFilter(vars.filter.item, id);
          if (vars.grid.item) {
            vars.grid.item.cancelEditData();
            vars.grid.item.refresh();
          }
        },
        setIdToGridFilter(filter, id) {
          if (!id) { id = 0; }
          filter[0].val = id;
          return filter;
        },
        clearFormData() {
            vars.formData.id = null;
            vars.formData.created = null;
            vars.formData.receipt_number = '';
            vars.formData.receipt_manager = '';
            vars.formData.receipt_detail = '';
            vars.formData.department = '';
            vars.formData.manager = '';
            vars.formData.client_manager = '';
            vars.formData.client_manager_phone = '';
            vars.formData.receipt_date = '';
            vars.formData.paid_type = '';
            vars.formData.fk_project_management_id = null;
            vars.formData.project_management = null;
            vars.formData.fk_company_id = authService.getCompanyId();
        },
        generateItemButtonOption(
            icon,
            callback,
            location = 'after',
            options = {}
        ) {
            let buttonOptions = { stylingMode: 'text', icon, onClick: callback };
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
        onGridInitialized(evt, key) {
            vars.grid[key] = evt.component;
            stateStore.bind(`as-receipt-${key}`, evt.component);
        },
        async newItem() { 
          methods.gridItemRefresh();
          if (vars.formData.id) {
              methods.clearFormData();
              methods.redirect();
          }
          setTimeout(() => {
              methods.clearFormData();
              methods.setFormData();
          }, 200);
        },

        setFormData(){
            vars.formData.department = authService.getDepartmentName();
            vars.formData.manager = authService.getUserName();
            vars.formData.receipt_date = currentDateTime();
            vars.formData.paid_type = methods.getFirstItemName(vars.dataSource.paid_type);
            vars.formData.fk_company_id = authService.getCompanyId();
            vars.formState.readOnly = false;
        },
        async editItem() {
            if (!vars.formData.id) return;

            const saveFormData = Object.assign({}, vars.formData);
            vars.formState.readOnly = !vars.formState.readOnly;

            methods.enableSave();
            methods.enableDelete();

            await nextTick();
            Object.assign(vars.formData, saveFormData);
        },

        finderReturnHandler(data) {
            switch (vars.dlg.finder.key) {
              case 'project': {
                  vars.formData.project_management = data;
                  vars.formData.fk_project_management_id = data.id;
                  break;
              }
              case 'receipt_number': {
                  methods.redirect(data.id);
                  break;
              }
            }

            vars.dlg.finder.show = false;
            vars.dlg.finder.title = '';
            vars.dlg.finder.key = null;
            vars.dlg.finder.data = null;
        },
        async saveItem() {
            let isSelect = await confirm('저장하시겠습니까?', '저장');
            if (!isSelect) {
              return;
            }
            vars.loading.value = true;
            try {
            
            if (vars.formData.id) {       
                const updateDate = Object.assign({}, vars.formData);
                delete updateDate.created;
                delete updateDate.receipt_number;
                delete updateDate.project_management;
                const { data } = await asReceipt.update(
                  vars.formData.id,
                  updateDate
                );
                                            
                vars.formData.receipt_number = data.receipt_number;
                vars.formData.project_management = data.project_management;

                if (vars.grid.item && vars.grid.item.hasEditData()) {
                  await vars.grid.item.saveEditData();
                }

                vars.formState.readOnly = true;

                notifyInfo('저장되었습니다');
                methods.enableSave();
                methods.enableDelete();

            } else {

                delete vars.formData.created;
                delete vars.formData.id;
                delete vars.formData.project_management;
                let { data } = await asReceipt.insert(vars.formData);
                vars.formData.id = data.id;

                                
                if (vars.grid.item && vars.grid.item.hasEditData()) {
                  await vars.grid.item.saveEditData();
                }

                notifyInfo('저장되었습니다');
                methods.redirect(data.id);
                vars.formState.readOnly = true;
            }
            } catch (ex) {
              console.error(ex);
              notifyError('저장 할 내용이 없습니다');
    
            } finally {
            vars.loading.value = false;
            }

        },
        selectDepartment(e) {
            const selectItem = e.component.option('selectedItem');
            if (selectItem) {
              baseEmployee
                  .load({
                    filter: [
                        ['fk_company_id', '=', authService._user.fk_company_id],
                        ['fk_department_id', '=', selectItem.id],
                    ],
                    skip: 0,
                    take: 1000,
                  })
                  .then(({ data }) => {
                    vars.dataSource.employee = data;
                  });
            }else{
              vars.dataSource.employee = [];
            }
        },
        async deleteItem() {
            if (!vars.formData.id) {
            return;
            }

            const result = await confirm(
            '이 항목을 삭제하시겠습니까?',
            '삭제 확인'
            );
            try{
            if (result) {
                await asReceipt.remove(vars.formData.id);
                await alert('삭제되었습니다', '삭제 확인');
                methods.redirect();
                vars.formState.readOnly = true;
            }
            }
            catch(ex){
            console.error(ex);
            notifyError('연결된 데이터가 있어서 삭제가 안됩니다');
            }
        
        },
        redirect(id) {
            if (id) router.replace({ path: `/as/receipt/${id}` });
            else router.replace({ path: `/as/receipt` });
        },
        onValueChanged(e) {
            if (!e.value) {
                vars.disabled.save = true;
            } else {
                if(methods.isFilledFormRequiredData()){
                    methods.enableSave();
                }
            }
        },
        
        isFilledFormRequiredData(){
            if(vars.formData.department && vars.formData.manager){
            return true;
            }
            return false;
        },
        enableDelete() {
            if (vars.formState.readOnly) {
            vars.disabled.delete = true;
            } else {
            vars.disabled.delete = false;
            }
        },
        enableSave() {
            if (vars.formState.readOnly) {
            vars.disabled.save = true;
            } else {
            vars.disabled.save = false;
            }
        },
        onDataError(e) {
            console.log("e : ", e)
            if (e.error.response.status == 605) {
            e.error.message = '연결된 데이터가 있어서 삭제가 안됩니다';
            } else if (e.error.response.status == 606) {
            e.error.message = '출고수량이 현재고를 초과했습니다';
            } else if (e.error.response.status == 607) {
            e.error.message = '기초재고가 등록되지 않은 품목입니다';
            } else if (e.error.response.status == 403) {
            e.error.message = '권한이 없습니다';
            }
        },
        onSavingItem(e) {
          e.changes.forEach((element) => {
          if (element.type != 'remove') {
            element.data.fk_as_receipt_id = vars.formData.id;
          }
        });
        },
        getFirstItemName(itemList) {
            if (!itemList || itemList.length <= 0) {
            return '';
            } else {
            return itemList[0].code_name;
            }
        },
        async addItemRowButton(item){
            const grid = vars.grid[item];
            if(grid){
            await grid.addRow();
            }
        },
        async itemSaveButton(item){
            if(!vars.formData.id) return;
            const grid = vars.grid[item];
            if(grid && grid.hasEditData()){
            await grid.saveEditData();
            }
        },
        initNewRow(e){
            console.log("e : ", e);
        },



      };
  
      watch(
        () => props.id,
        () => methods.initById(props.id)
      );
  
      return {
        vars,
        methods,
        baseItem,
        baseClient,
      };
    },
  };
  </script>
  
  <style lang="scss">
  .vat-data-box{
    // border: 1px dashed #ddd;
    // border-radius: 15px;
    // padding: 3px;
    // margin-top: 3px;
  
  }
  .dx-fileuploader-wrapper {
    padding: 0px;
    margin: 0px;
  }
  .dx-fileuploader-input-wrapper {
    padding: 0px;
    margin: 0px;
  }
  .company_name{
    color:rgb(156, 50, 32); 
    
  }
  .company_name:hover{
    color: red;
    text-decoration: underline;
    cursor: pointer;
  }
  
  </style>
  