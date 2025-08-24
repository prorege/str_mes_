<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">나의 결재함</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div v-if="vars.init.value">
          <div class="search-status search-line">
            <span class="search-title">상신일자</span>
            <dx-date-box v-model:value="vars.formData.startDate" />
            <span class="search-bar">~</span>
            <dx-date-box v-model:value="vars.formData.endDate" />

            <span class="search-tab"></span>

            <SearchButtonGroup @change="({startDate, endDate}) => { vars.formData.startDate = startDate; vars.formData.endDate = endDate; }" />
          </div>
          <div class="search-status">
            <span class="search-title">상신자</span>
            <dx-lookup
              value-expr="id"
              display-expr="emp_name"  
              v-model:value="vars.formData.manager"
              :data-source="vars.dataSource.employee"
            />

            <span class="search-tab"></span>

            <span class="search-title">결재처리</span>
            <dx-lookup
              value-expr="code_name"
              display-expr="code_name"  
              v-model:value="vars.formData.approval_result"
              :data-source="vars.dataSource.approval_result"
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
          :data-source="vars.dataSource.approvalLineResult"
          :on-row-prepared="methods.onRowPrepared"
          :on-initialized="evt => methods.onGridInitialized(evt, 'status')"
          @data-error-occurred="methods.onDataError"
        >
          <dx-column caption="상신일자" data-field="approval.approval_date" data-type="date" format="yyyy-MM-dd" :allow-editing="false" />
          <dx-column caption="문서명" data-field="approval.document_name" :allow-editing="false" />
          <dx-column caption="상신번호" data-field="approval.approval_number" :allow-editing="false" />
          <dx-column caption="상신자" data-field="request_employee.emp_name" :allow-editing="false" />
          <dx-column caption="결재문서" data-field="approval_attachment" cell-template="attachment-template" :allow-editing="false" alignment="center" :allow-sorting="false" />
          <dx-column caption="결재처리" data-field="approval_result" :allow-editing="false" alignment="center" cell-template="approval-result-template" />
          <dx-column caption="반려사유" data-field="approval_reason" :allow-editing="false" />
          <dx-column caption="처리일시" data-field="approval_date" data-type="date" format="yyyy-MM-dd" :allow-editing="false" />
          <template #attachment-template="{ data }">
            <span class="attachment-template-button" @click="methods.documentPopupShow(data)">문서보기</span>
          </template>
          <template #approval-result-template="{ data }">
            <span :class="`approval-result-template ${data.data.approval_result == '결재완료' ? 'approve' : 'reject'}`" @click="methods.onApprovalResultClick(data)">{{ data.data.approval_result }}</span>
          </template>
  
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
      v-model:visible="vars.dlg.orderReport.show"
      content-template="popup-content"
      title="수주사항보고서"
      :close-on-outside-click="true"
      width="1400px"
      height="800px"
      :resize-enabled="true"
      :scroll-by-content="true"
      @hidden="methods.onPopupHidden"
      @initialized="evt => methods.onGridInitialized(evt, 'popup-order-report')"
    >
    <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ 
          text: '결재', 
          icon: '',
          onClick: methods.handleApproval,
          type: 'add',
        }"
      />
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ 
          text: '반려', 
          icon: '',
          onClick: methods.handleRejection,
          type: 'remove',
        }"
      />
      <template #popup-content>
        <dx-scroll-view width="100%" height="100%">
          <data-order-report :fk_business_id="vars.dlg.orderReport.fk_business_id" :fk_request_emp_id="vars.dlg.orderReport.fk_request_emp_id" />
        </dx-scroll-view>
      </template>
    </dx-popup>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';
import moment from 'moment';
import numeral from 'numeral';
import { notifyInfo, notifyError } from '../../utils/notify';
import { ref, reactive, onMounted } from 'vue';
import { confirm, alert, custom } from 'devextreme/ui/dialog';
import { DxScrollView } from 'devextreme-vue/scroll-view';
import DxButton from 'devextreme-vue/button';
import DxLookup from 'devextreme-vue/select-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxTextBox, DxButton as DxTextBoxButton } from 'devextreme-vue/text-box';
import { DxDataGrid, DxColumn, DxPaging, DxEditing, DxSorting, DxSelection, DxFilterRow, DxItem as DxGridItem, DxColumnChooser, DxToolbar as DxGridToolbar, DxLookup as DxGridLookup, DxButton as DxGridButton } from 'devextreme-vue/data-grid';

import { baseCodeLoader } from '../../data-source/base';
import SearchButtonGroup from '@/components/search-button-group.vue';
import { loadEmployee } from '../../utils/data-loader';
import { approvalLineResult, getApprovalLineResult, approval, approvalDocumentStatus, approvalDocument } from '../../data-source/approval';
import authService from '@/auth';
import stateStore from '@/utils/state-store';
import ApiService from '@/utils/api-service';
import { baseEmployee } from '../../data-source/base';
import DataOrderReport from '@/components/approval/data-order-report.vue';

export default {
  components: {
    DxButton,
    DxLookup,
    DxDateBox,
    DxToolbar, DxItem,
    DxPopup, DxToolbarItem,
    DxTextBox, DxTextBoxButton,
    DxDataGrid, DxColumn, DxPaging, DxEditing, DxSorting, DxSelection, DxFilterRow, DxGridItem, DxColumnChooser, DxGridToolbar, DxGridLookup, DxGridButton,
    SearchButtonGroup,
    DxScrollView,
    DataOrderReport,
  },
  setup() {
    const router = useRouter();
    const vars = { dlg: {} };

    vars.init = ref(false);
    vars.grid = {};
    vars.now = new Date();

    vars.dlg.orderReport = reactive({ show: false, fk_business_id: 0, fk_request_emp_id: 0, data: null });
    vars.formData = reactive({
      manager: '',
      approval_result: '',
      startDate: new Date(vars.now.getFullYear(), vars.now.getMonth(), vars.now.getDate() - 7),
      endDate: new Date(vars.now.getFullYear(), vars.now.getMonth(), vars.now.getDate(), 23, 59, 59),
    });

    vars.dataSource = reactive({
      employee: [],
      approval_result: [],
      attachment: [],
      approvalLineResult: getApprovalLineResult(
        [
          {
            name: 'fk_approval_emp_id',
            op: 'eq',
            val: authService.user?.emp_id,
          },
          {
            name: 'approval',
            op: 'has',
            val: { name: 'approval_status', op: 'neq', val: '상신대기' },
          },
        ]
      ),
    });
    vars.dataSource.approvalLineResult.load().then((res) => {
      console.log("res : ", res);
    })
   
    onMounted(async () => {
      await methods.loadBaseCode();
      // loadEmployee(vars.dataSource);
      baseEmployee.load().then((res) => {
      vars.dataSource.employee = [{emp_name: '전체'}, ...res.data];
    })

      vars.init.value = true
    });

    const methods = {
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`approval-approval-${key}`, evt.component);

        methods.searchDateRange();
      },
      async searchDateRange() {
        if (vars.formData.startDate > vars.formData.endDate) {
          await alert('조회 일자가 잘못 되었습니다', '조회');
          return;
        }

        try {
          vars.grid['status'].beginCustomLoading('데이터를 집계중입니다')
          
          const filters = [];
          vars.grid['status'].clearFilter();

          if (vars.formData.startDate) {
            filters.push(['approval', 'has', { name :'approval_date', op : 'gte', val : moment(vars.formData.startDate).format('YYYY-MM-DD HH:mm:ss')}]);
          }
          if (vars.formData.endDate) {
            filters.push(['approval', 'has', { name :'approval_date', op : 'lte', val : moment(vars.formData.endDate).format('YYYY-MM-DD HH:mm:ss')}]);
          }

          if (vars.formData.manager && vars.formData.manager != '전체') {
            filters.push(['approval', 'has', { name :'fk_request_emp_id', op : 'eq', val : vars.formData.manager}]);
          }

          if (vars.formData.approval_result && vars.formData.approval_result != '전체') {
            filters.push(['approval_result', '=', vars.formData.approval_result]);
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
          '결재처리',
        ])
          .then(response => {
            vars.dataSource.approval_result = response['결재처리'];
          })
      },
      async documentPopupShow(data){
        try {
          const formData = data.data;
          vars.dlg.orderReport.data = formData;
          if (formData.approval.fk_business_id) {
            vars.dlg.orderReport.fk_business_id = formData.approval.fk_business_id;
          }

          vars.dlg.orderReport.show = true;
          vars.dlg.orderReport.fk_request_emp_id = formData.approval.fk_request_emp_id;

        } catch (error) {
          alert("오류 발생<br/>관리자에게 문의하세요", "오류")
          console.log("error : ", error);
        }
       
      },
      onRowPrepared(e) {
        if(e.rowType != 'data') return;
        const data = e.data;
        if (data.approval_result == '대기중' && data.active_yn == 0) {
          e.rowElement.style.display = 'none';
        }

      },
      async onApprovalResultClick(data){
        if(data.data.approval_result != '대기중') return;

        await custom({
            title: '결재처리',
            message: '결재처리를 하시겠습니까?',
            buttons: [
              { text: '결재', onClick: () => 'approve' },
              { text: '반려', onClick: () => 'reject' },
              { text: '취소', onClick: () => 'cancel' }
            ],
        }).show().then(result =>{
            switch (result) {
              case 'approve':
                methods.handleApproval(data);
                break;
              case 'reject':
                methods.handleRejection(data);
                break;
              case 'cancel':
                notifyInfo('취소되었습니다');
                break;
              default:
                break;
            }
        });

      },
      async handleApproval(data){
        const resultData = vars.dlg.orderReport.data;
        if(resultData.approval_result == '결재완료'){
          alert('이미 결재가 완료 됐습니다.', '결재');
          return;
        }
        let isSelect = await confirm('결재 하시겠습니까?', '결재');
        if (!isSelect) {
          return;
        }
       
        try {
          await approvalLineResult.update(resultData.id, {'approval_result': '결재완료', 'approval_reason': '', 'closing_yn': true, 'approval_date': moment().format('YYYY-MM-DD HH:mm:ss')})
          await approval.update(resultData.fk_approval_id, {'approval_reason': ''});
          notifyInfo('결재처리가 완료되었습니다');
          vars.grid['status'].refresh();
          vars.grid['popup-order-report'].hide();
        }catch (ex) {
          console.error(ex);
        }
      },
      async handleRejection(data){
        const resultData = vars.dlg.orderReport.data;
        const { data : _approval } = await approval.byKey(resultData.fk_approval_id);
        const _approvalLineResult = _approval.approval_line_result;
 
        const currentIndex = _approvalLineResult.findIndex(item => item.id == resultData.id);
        const nextItem = _approvalLineResult[currentIndex + 1] || null;

        if (nextItem && (nextItem.approval_result == '결재완료' || nextItem.approval_result == '반려')) {
          alert('이미 상위 결재자가 결재 또는 반려를 완료했습니다.', '반려');
          return;
        }

        if(resultData.approval_result == '반려'){
          alert('이미 반려가 완료 됐습니다.', '반려');
          return;
        }
        let isSelect = await confirm('반려 하시겠습니까?', '반려');
        if (!isSelect) {
          return;
        }
        custom({
          title: '반려사유',
          messageHtml: `
              <div>
                  <label for="rejectionReason">반려 사유:</label>
                  <input type="text" id="rejectionReason" placeholder="반려 사유를 입력하세요" 
                        style="width: 100%; padding: 8px; margin-top: 5px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;" maxlength="300" />
              </div>
          `,
          buttons: [
            { text: '확인', onClick: () => {
              const rejectionReason = document.getElementById('rejectionReason').value;
              return rejectionReason;
            } },
            { text: '취소', onClick: () => {
              return null;
            } }
          ],
        }).show().then(async (result) => {
          if (result !==  null) {
            const params = {
              'approval_result': '반려',
              'approval_reason': result,
              'closing_yn': false,
              'active_yn': 1,
              'approval_date': moment().format('YYYY-MM-DD HH:mm:ss')
            }
            await approvalLineResult.update(resultData.id, params)
            if (nextItem) {
              await approvalLineResult.update(nextItem.id, {'active_yn': 0});
            }
            await approval.update(resultData.fk_approval_id, {'approval_reason': result})
            notifyInfo('반려처리가 완료되었습니다');
            vars.grid['status'].refresh();
            vars.grid['popup-order-report'].hide();
          }else{
            notifyInfo('반려처리가 취소되었습니다');
          }
        });
      },
      onPopupHidden() {
        vars.dlg.orderReport.data = null;
        vars.dlg.orderReport.fk_business_id = 0;
        vars.dlg.orderReport.fk_request_emp_id = 0;
        vars.dlg.orderReport.show = false;
      },
    };

    return { vars, methods };
  },
};
</script>

<style>
.approval-result-template {
  margin-right: 10px;
  border-radius: 5px;
  padding: 0 5px;
  color: #ffffff;
  cursor: pointer;
}
.approve {
  background-color: #46A046 !important;
}
.reject {
  background-color: #CE312C !important;
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
</style>
