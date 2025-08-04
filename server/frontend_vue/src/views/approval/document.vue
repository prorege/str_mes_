<template>
    <div>
      <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
      <div class="content-block">
        <div class="dx-card responsive-paddings back-colored">
          <div class="content-header">
            <dx-toolbar class="back-colored">
              <dx-item location="before"
                ><div class="content-title">전자결재 결재선 지정</div></dx-item
              >
            </dx-toolbar>
          </div>
        </div>
        <div class="dx-card responsive-paddings mt-1">
          <dx-data-grid
            height="calc(100vh - 230px)"
            date-serialization-format="yyyy-MM-ddTHH:mm:ss"
            :show-borders="true"
            :column-auto-width="true"
            :remote-operations="true"
            :focused-row-enabled="true"
            :allow-column-resizing="true"
            :allow-column-reordering="true"
            :row-alternation-enabled="true"
            :data-source="vars.dataSource.approvalDocumentStatus"
            :on-initialized="evt => methods.onGridInitialized(evt, 'status')"
            @saving="methods.onSavingItem"
            @data-error-occurred="methods.onDataError"
          >
            <dx-grid-toolbar>
              <dx-grid-item template="edit" location="after" />
              <dx-grid-item name="saveButton" />
              <dx-grid-item name="revertButton" />
              <dx-grid-item name="columnChooserButton" />
            </dx-grid-toolbar>
            <template #edit>
              <dx-button icon="edit" @click="methods.toggleEdit" />
            </template>
  
            <dx-column caption="문서번호" data-field="document_number" :allow-editing="false" alignment="center" :header-cell-template="(e) => methods.emptyHeaderTemplate(e, '문서번호')" />
            <dx-column caption="문서명" width="110" data-field="document_name" :allow-editing="false" alignment="center"
            :header-cell-template="(e) => methods.emptyHeaderTemplate(e, '문서명')"
            />
            <dx-column caption="결재선 지정" alignment="center">
              <dx-column
                data-field="1"
                caption="기안"
                :allow-editing="!vars.disabled.edit"
                width="120px"
                alignment="center"
              >
                <dx-lookup
                  :data-source="vars.dataSource.employee"
                  value-expr="emp_name"
                  display-expr="emp_name"
                />
              </dx-column>
              <dx-column
                data-field="2"
                caption="팀장"
                :allow-editing="!vars.disabled.edit"
                width="120px"
                alignment="center"
              >
                <dx-lookup
                    :data-source="vars.dataSource.employee"
                    value-expr="emp_name"
                    display-expr="emp_name"
                />
              </dx-column>
              <dx-column
                data-field="3"
                caption="PM검토"
                :allow-editing="!vars.disabled.edit"
                width="120px"
                alignment="center"
              >
                <dx-lookup
                    :data-source="vars.dataSource.employee"
                    value-expr="emp_name"
                    display-expr="emp_name"
                />
              </dx-column>
              <dx-column
                data-field="4"
                caption="PE검토"
                :allow-editing="!vars.disabled.edit"
                width="120px"
                alignment="center"
              >
                <dx-lookup
                    :data-source="vars.dataSource.employee"
                    value-expr="emp_name"
                    display-expr="emp_name"
                />
              </dx-column>
              <dx-column
                data-field="5"
                caption="대표이사"
                :allow-editing="!vars.disabled.edit"
                width="120px"
                alignment="center"
              >
                <dx-lookup
                    :data-source="vars.dataSource.employee"
                    value-expr="emp_name"
                    display-expr="emp_name"
                />
              </dx-column>
            </dx-column>
            <dx-column caption="등록자" data-field="register" :allow-editing="false" alignment="center" :header-cell-template="(e) => methods.emptyHeaderTemplate(e, '등록자')" />
            <dx-column caption="등록일자" data-field="register_date" data-type="date" format="yyyy-MM-dd" :allow-editing="false" alignment="center" :header-cell-template="(e) => methods.emptyHeaderTemplate(e, '등록일자')" />

            <dx-sorting mode="single" />
            <dx-paging :page-size="20" />
            <dx-column-chooser mode="select" :enabled="true" />
            <dx-editing mode="batch"
              :use-icons="true"
              :allow-adding="false"
              :allow-updating="!vars.disabled.edit"
              :allow-deleting="false"
            />
          </dx-data-grid>
        </div>
      </div>
    </div>
</template>


<script>
import moment from 'moment';
import { reactive, ref, watch } from 'vue';
import { notifyInfo, notifyError } from '../../utils/notify';
import DxButton from 'devextreme-vue/button';
import DxCheckBox from 'devextreme-vue/check-box';
import DxTextArea from 'devextreme-vue/text-area';
import DxTextBox from 'devextreme-vue/text-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxForm, DxLabel, DxGroupItem, DxEmptyItem, DxSimpleItem, DxButtonItem } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxEditing, DxSorting, DxSelection, DxFilterRow, 
        DxColumnChooser, DxLookup, DxToolbar as DxGridToolbar, DxItem as DxGridItem } from 'devextreme-vue/data-grid';
import { approvalDocumentStatus, getApprovalDocumentStatus, approval } from '../../data-source/approval';
import DataGridClient from '../../components/base/data-client.vue';
import stateStore from '@/utils/state-store';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import { baseEmployee } from '../../data-source/base';
import authService from '../../auth';
import { confirm, alert } from 'devextreme/ui/dialog';

export default {
components: {
    DxButton,
    DxCheckBox,
    DxTextArea,
    DxToolbar, DxItem,
    DxPopup, DxToolbarItem,
    DxForm, DxLabel, DxGroupItem, DxEmptyItem, DxSimpleItem, DxButtonItem,
    DxDataGrid, DxColumn, DxPaging, DxEditing, DxSorting, DxSelection, DxFilterRow, DxColumnChooser, DxGridToolbar, DxGridItem, DxLookup,
    DataGridClient,
    DxTextBox,
    DxLoadPanel,
},
setup() {
    const vars = {};

    vars.grid = {};
    vars.loading = ref(false);
    vars.disabled = reactive({ 
    edit: true,
    form: {}
    })

    vars.dataSource = reactive({
    approvalDocumentStatus: getApprovalDocumentStatus([{
        name: 'manager',
        op: 'eq',
        val: authService.getUserName(),
    }]),
    employee: [],
    })
    
    baseEmployee.load().then((res) => {
    vars.dataSource.employee = [{emp_name: ''}, ...res.data];
    })
    
    const methods = {
    onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`approval-document-${key}`, evt.component);

    },
    async toggleEdit() {
        if (vars.disabled.edit) {
        let isSelect = await confirm('수정하시겠습니까?', '수정');
        if (!isSelect) { return; }
        }
        vars.disabled.edit = !vars.disabled.edit;

    },
    onSavingItem(e) {
        e.changes.forEach(element => {
        if (element.type == 'update') {
            element.data.manager = authService.getUserName();
        }
        });
    },
    onDataError(e) {
        if (e.error.response.status == 605) {
            e.error.message = '연결된 데이터가 있어서 삭제가 안됩니다';
        } else if (e.error.response.status == 403) {
            e.error.message = '권한이 없습니다';
        }
    },
    emptyHeaderTemplate(container, caption) {
        const tdElement = container.closest('td');
        tdElement.style.verticalAlign = 'middle';
        tdElement.style.textAlign = 'center';
        tdElement.innerHTML = caption;
    },    
    };
    return {
        vars,
        methods,
        approvalDocumentStatus,
        moment,
    };
},
};
</script>
<style scoped>
:deep(.pointer-content input) {
cursor: pointer !important;
}

.approval-popup-header {
display: flex;
justify-content: space-between;
margin: 0 0 30px 0 !important;
}
.approval-line-table th,
.approval-line-table td {
border: 1px solid #dddddd;
padding: 0;
text-align: center;
vertical-align: middle;
background-color: #ffffff;
}
.approval-line-table {
border-collapse: collapse;  

}
</style>