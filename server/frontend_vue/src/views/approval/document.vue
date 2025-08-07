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
            column-resizing-mode="widget"
            height="calc(100vh - 230px)"
            date-serialization-format="yyyy-MM-ddTHH:mm:ss"
            :show-borders="true"
            :column-auto-width="true"
            :remote-operations="true"
            :focused-row-enabled="true"
            :allow-column-resizing="true"
            :allow-column-reordering="true"
            :row-alternation-enabled="true"
            :data-source="vars.dataSource.approvalDocument"
            :on-initialized="evt => methods.onGridInitialized(evt, 'status')"
            @saving="methods.onSavingItem"
            @data-error-occurred="methods.onDataError"
          >
            <dx-grid-toolbar>
              <dx-grid-item template="edit" location="after" :visible="false" />
              <dx-grid-item name="saveButton" :visible="false" />
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
            <dx-column caption="결재선지정" data-field="approval_line" :allow-editing="false" alignment="center" cell-template="approvalLine" />
            <template #approvalLine="{ data }">
              <dx-button class="approval-line-button" icon="edit" text="결재선지정" @click="methods.approvalLineEdit(data)" />
            </template>
            <dx-column caption="등록자" data-field="register" :allow-editing="false" alignment="center" :header-cell-template="(e) => methods.emptyHeaderTemplate(e, '등록자')" />
            <dx-column caption="등록일자" data-field="register_date" data-type="date" format="yyyy-MM-dd" :allow-editing="false" alignment="center" :header-cell-template="(e) => methods.emptyHeaderTemplate(e, '등록일자')" />

            <dx-sorting mode="single" />
            <dx-paging :page-size="20" />
            <dx-column-chooser mode="select" :enabled="true" />
            <dx-editing mode="batch"
              :use-icons="true"
              :allow-adding="false"
              :allow-updating="false"
              :allow-deleting="false"
            />
          </dx-data-grid>
        </div>
      </div>
      <dx-popup
        v-model:visible="vars.dlg.approvalLine.show"
        content-template="popup-content"
        :title="`${vars.dlg.approvalLine.formData.document_name} 결재선 지정`"
        :close-on-outside-click="true"
        width="50%"
        height="auto"
        :resize-enabled="true"
        >
          <template #popup-content>
            <dx-scroll-view width="100%" height="100%">
              <data-approval-line :form-data="vars.dlg.approvalLine.formData" />
            </dx-scroll-view>
          </template>
        </dx-popup>
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
import { approvalDocument, getApprovalDocument, approval } from '../../data-source/approval';
import DataGridClient from '../../components/base/data-client.vue';
import DxScrollView from 'devextreme-vue/scroll-view';
import stateStore from '@/utils/state-store';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import { baseEmployee } from '../../data-source/base';
import authService from '../../auth';
import { confirm, alert } from 'devextreme/ui/dialog';
import DataApprovalLine from '@/components/approval/data-approval-line.vue';

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
    DataApprovalLine,
    DxScrollView,
},
setup() {
    const vars = {};

    vars.grid = {};
    vars.dlg = {};
    vars.dlg.approvalLine = reactive({ show: false, formData: {} });
    vars.loading = ref(false);
    vars.disabled = reactive({ 
    edit: true,
    form: {}
    })

    vars.dataSource = reactive({
    approvalDocument: approvalDocument,
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
    approvalLineEdit(data) {
      if (!data.data.id) return;
      try {
        vars.dlg.approvalLine.show = true;
        vars.dlg.approvalLine.formData = {
          document_id: data.data.id,
          emp_id: authService.user?.emp_id,
          document_name: data.data.document_name,
        }
      }catch(ex){
        console.error(ex);
        alert('오류가 발생 했습니다. 관리자에게 문의 바랍니다.', '오류');
      }
      
    },
    onSavingItem(e) {
        e.changes.forEach(element => {
          console.log("element : ", element)
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
        moment,
    };
},
};
</script>
<style scoped>
.approval-line-button {
  height: 30px !important;
  

}
:deep(.approval-line-button > .dx-button-content > .dx-button-text) {
 line-height: inherit !important;
}
:deep(.dx-datagrid .dx-row > td) {
  vertical-align: middle !important;
}
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