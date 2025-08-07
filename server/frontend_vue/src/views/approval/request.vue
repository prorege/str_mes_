<template>
  <div>
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">나의 결재 상신 현황</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div v-if="vars.init.value">
          <div class="search-status search-line">
            <span class="search-title">상신일자</span>
            <dx-date-box v-model:value="vars.searchForm.startDate" />
            <span class="search-bar">~</span>
            <dx-date-box v-model:value="vars.searchForm.endDate" />

            <span class="search-tab"></span>

            <SearchButtonGroup @change="({startDate, endDate}) => { vars.searchForm.startDate = startDate; vars.searchForm.endDate = endDate; }" />
          </div>
          <div class="search-status">
            <span class="search-title">상신상황</span>
            <dx-lookup
              value-expr="code_name"
              display-expr="code_name"  
              v-model:value="vars.searchForm.approval_status"
              :data-source="vars.dataSource.approval_status"
            />

            <span class="search-tab"></span>

            <dx-button text="검색" icon="search" @click="methods.searchDateRange()" />
          </div>
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
          :data-source="vars.dataSource.approval"
          :on-initialized="evt => methods.onGridInitialized(evt, 'status')"
        >
          <dx-column caption="상신일자" data-field="approval_date" data-type="date" format="yyyy-MM-dd" :allow-editing="false" />
          <dx-column caption="문서명" data-field="approval_document.document_name" :allow-editing="false" />
          <dx-column caption="상신번호" data-field="approval_number" :allow-editing="false" />
          <dx-column caption="상신자" data-field="register" :allow-editing="false" />
          <dx-column caption="문서명" data-field="approval_attachment" cell-template="attachment-template" :allow-editing="false" :allow-sorting="false" alignment="center" width="110" />
          <dx-column caption="상신상황" data-field="approval_status" :allow-editing="false" alignment="center" cell-template="approval-status-template" />
          <dx-column caption="결재처리" alignment="center" data-field="approval_line_result" cell-template="approval-result-template" :allow-editing="false" :allow-sorting="false" />
          <dx-column caption="반려사유" data-field="approval_reason" :allow-editing="false" />
          <dx-column caption="결재처리일자" data-field="approval_result_date" data-type="date" format="yyyy-MM-dd" :allow-editing="false" />
          <template #attachment-template="{ data }">
            <span class="attachment-template-button" @click="methods.documentPopupShow(data)">문서보기</span>
          </template>
          <template #approval-result-template="{ data }">
            <span v-for="item in data.data.approval_line_result" :key="item.id" :class="`approval-result-template ${item.approval_result == '결재완료' ? 'approve' : 'reject'}`" >
              <span>{{ item.approval_manager }}</span>
              <span> : </span>
              <span>{{ item.approval_result == null ? '대기중' : item.approval_result }}</span>
            </span>
          </template>
          <template #approval-status-template="{ data }">
            <span :class="`approval-status-template ${data.data.approval_status == '상신완료' || data.data.approval_status == '결재완료' ? 'approve' : 'reject'}`">{{ data.data.approval_status }}</span>
          </template>

          <dx-sorting mode="single" />
          <dx-paging :page-size="20" />
          <dx-column-chooser mode="select" :enabled="true" />
        </dx-data-grid>
      </div>
    </div>
    <!-- <popup-approval v-if="vars.dlg.approval.visible" :visible="vars.dlg.approval.visible" @update:visible="(value) => methods.approvalPopupClose(value)" :data="vars.dlg.approval.data" :form-data="vars.dlg.approval.formData"/> -->
    <dx-popup
      title="첨부파일함"
      content-template="popup-content"
      v-model:visible="vars.dlg.attachment.show"
      width="auto"
      :height="500"
      :resize-enabled="true"
      :close-on-outside-click="true"
    >
      <template #popup-content>
        <dx-data-grid
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :cell-hint-enabled="true"
          :data-source="vars.dataSource.attachment"
          :on-initialized="evt => methods.onGridInitialized(evt, 'attachment')"
          >
          <dx-column caption="첨부파일명" data-field="file_name" width="280" />
          <dx-column caption="첨부파일명" data-field="file_path" :visible="false" />
          <dx-column type="buttons" width="120">
            <dx-grid-button text="다운로드" @click="methods.downloadAttachment" />
            <dx-grid-button text="열기" @click="methods.openAttachment" />
          </dx-column>
        </dx-data-grid>
      </template>
    </dx-popup>
  </div>
</template>

<script>
import moment from 'moment';
import { ref, reactive, onMounted } from 'vue';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import { confirm, alert } from 'devextreme/ui/dialog';
import DxButton from 'devextreme-vue/button';
import DxLookup from 'devextreme-vue/select-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxPopup } from 'devextreme-vue/popup';
import { DxDataGrid, DxColumn, DxPaging, DxSorting, DxColumnChooser, DxButton as DxGridButton } from 'devextreme-vue/data-grid';
import { baseCodeLoader } from '../../data-source/base';
import SearchButtonGroup from '@/components/search-button-group.vue';
import { loadEmployee } from '../../utils/data-loader';
import { approval, getApproval, approvalDocumentStatus } from '../../data-source/approval';
import authService from '@/auth';
import stateStore from '@/utils/state-store';
// import PopupApproval from '../../components/approval/popup-approval.vue';

export default {
  components: {
    DxButton,
    DxGridButton,
    DxLookup,
    DxDateBox,
    DxToolbar, DxItem,
    DxPopup,
    DxDataGrid, DxColumn, DxPaging, DxSorting, DxColumnChooser,
    SearchButtonGroup,
    DxLoadPanel,
  },
  setup() {
    const vars = { dlg: {} };
    vars.loading = ref(false);
    vars.init = ref(false);
    vars.grid = {};
    vars.now = new Date();
    vars.searchForm = reactive({
      approval_status: '',
      startDate: new Date(vars.now.getFullYear(), vars.now.getMonth(), vars.now.getDate() - 7),
      endDate: new Date(vars.now.getFullYear(), vars.now.getMonth(), vars.now.getDate(), 23, 59, 59),
    });
    vars.dlg.attachment = reactive({ show: false });
    vars.dlg.approval = reactive({ 
      visible: false,
      key: null,
      data: null,
      formData: null,
    });
    vars.dataSource = reactive({
      employee: [],
      approval_status: [],
      approval: getApproval([{
        'name': 'register',
        'op': 'eq',
        'val': authService.getUserName(),
      }]),
      attachment: [],
    });

    onMounted(async () => {
      await methods.loadBaseCode();
      loadEmployee(vars.dataSource);
      vars.init.value = true
    });

    const methods = {
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`approval-request-${key}`, evt.component);

        methods.searchDateRange();
      },
      async searchDateRange() {
        if (vars.searchForm.startDate > vars.searchForm.endDate) {
          await alert('조회 일자가 잘못 되었습니다', '조회');
          return;
        }

        try {
          vars.grid['status'].beginCustomLoading('데이터를 집계중입니다')
          
          const filters = [];
          vars.grid['status'].clearFilter();

          if (vars.searchForm.startDate) {
            filters.push(['approval_date', '>=', moment(vars.searchForm.startDate).format('YYYY-MM-DD HH:mm:ss')]);
          }
          if (vars.searchForm.endDate) {
            filters.push(['approval_date', '<=', moment(vars.searchForm.endDate).format('YYYY-MM-DD HH:mm:ss')]);
          }

          if (vars.searchForm.approval_status && vars.searchForm.approval_status != '전체') {
            filters.push(['approval_status', '=', vars.searchForm.approval_status]);
          }

          vars.grid['status'].filter(filters);
          
        }
        catch (ex) {
          console.error(ex)
        }
        finally {
          vars.grid['status'].endCustomLoading()
        }
      },
      async loadBaseCode(){
        return baseCodeLoader([
          '상신상황',
        ])
          .then(response => {
            vars.dataSource.approval_status = response['상신상황'];
          })
      },
      async documentPopupShow(data) {
        try {
          const formData = data.data;
          const response = await approvalDocumentStatus.load({
            filter: ['manager', '=', authService.getUserName()]
          });
          if (response.data) {
            formData.approval_document = response.data[formData.fk_document_id -1];
          }

          vars.dlg.approval.visible = true;
          vars.dlg.approval.key = formData.fk_document_id;
          vars.dlg.approval.data = formData.approval_document;
          vars.dlg.approval.formData = formData;
        } catch (error) {
          alert("오류 발생<br/>관리자에게 문의하세요", "오류")
          console.log("error : ", error);
        }
      
      },
      openAttachment(data){
        const file_path = data.row.data.file_path;
        const file_name = data.row.data.file_name;
        const file_extension = file_name.split('.').pop().toLowerCase();
        const allowedExtensions = ['pdf', 'png', 'jpg', 'jpeg'];

        if(allowedExtensions.includes(file_extension)){
          window.open(`/api/mes/v1/file-manager/read/${file_path}/${file_name}`, '_blank');
        }
        else{
          alert('허용되지 않는 파일 형식입니다', '첨부파일');
        }
      },
      downloadAttachment(data){
        const file_path = data.row.data.file_path;
        const file_name = data.row.data.file_name;
        location.href = `/api/mes/v1/file-manager/download/${file_path}/${file_name}`;
      },
      approvalPopupClose(value) {
        vars.dlg.approval.visible = value;
        vars.dlg.approval.key = null;
        vars.dlg.approval.data = null;
        vars.dlg.approval.formData = null;
        vars.grid['status'].refresh();
      },
    };

    return { vars, methods, approval, moment };
  },
};
</script>

<style scoped>
.attachment-template {
  text-decoration: underline;
  cursor: pointer;
}
.attachment-template-button{
  border: 1px solid #000000;
  text-align: center;
  padding: 0 5px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.85rem;
}
.attachment-template-button:hover {
  background-color: #808080;
  border-color: #808080;
  color: #ffffff;
}
.attachment-template-button:active {
  background-color: #e0e0e0;
  transform: scale(0.98);
}
.approval-result-template {
  margin-right: 10px;
  border-radius: 5px;
  padding: 0 5px;
  color: #ffffff;
}
.approval-status-template {
  border-radius: 5px;
  padding: 0 5px;
  color: #ffffff;
}
.approve {
  background-color: #46A046 !important;
}
.reject {
  background-color: #CE312C !important;
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
