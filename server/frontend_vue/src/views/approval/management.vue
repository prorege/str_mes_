<template>
    <div>
      <div class="content-block">
        <div class="dx-card responsive-paddings back-colored">
  
          <div class="content-header">
            <dx-toolbar class="back-colored">
              <dx-item location="before">
                <div class="content-title">전자결재관리</div>
              </dx-item>
            </dx-toolbar>
          </div>
  
          <div>
            <div class="search-status search-line">
              <span class="search-title">요청일자</span>
              <dx-date-box v-model:value="vars.formData.startDate" />
              
              <span class="search-bar">~</span>
              <dx-date-box v-model:value="vars.formData.endDate" />
              
              <span class="search-tab"></span>
              <SearchButtonGroup @change="({startDate, endDate}) => { vars.formData.startDate = startDate; vars.formData.endDate = endDate; }" />
              
            </div>
            <div class="search-status">
              <span class="search-title">요청자</span>
              <dx-lookup
                value-expr="emp_name"
                display-expr="emp_name"
                v-model:value="vars.formData.employee"
                :data-source="vars.dataSource.employee"
                />
              <span class="search-tab"></span>
              <span class="search-title">결재결과</span>
              <dx-lookup 
                value-expr="code_name"
                display-expr="code_name"
                v-model:value="vars.formData.approval_status"
                :data-source="vars.dataSource.approval_status"
                />
              <span class="search-tab"></span>
              <dx-button text="검색" icon="search" @click="methods.searchDateRange()" />
              <span class="search-tab"></span>
              <dx-button text="초기화" icon="" @click="methods.searchReset()" />
            </div>
          </div>
  
        </div>
  
        <div class="dx-card responsive-paddings mt-1">
          <dx-data-grid
            height="calc(100vh - 230px)"
            column-resizing-mode="widget"
            :show-borders="true"
            :column-auto-width="true"
            :remote-operations="true"
            :focused-row-enabled="true"
            :allow-column-resizing="true"
            :allow-column-reordering="true"
            :row-alternation-enabled="true"
            :data-source="vars.dataSource.approvalManagement"
            :on-initialized="evt => methods.onGridInitialized(evt, 'approval')"
            @exporting="methods.onExporting"
            @cell-dbl-click="methods.cellDblClick"
            @context-menu-preparing="methods.onRowContextMenu"
          >
            <dx-column caption="요청일자" data-field="request_date" data-type="date" format="yyyy-MM-dd" />
            <dx-column caption="요청번호" data-field="request_number" cell-template="requestNumberTemplate" />
            <dx-column caption="요청자" data-field="request_name" />
            <dx-column caption="결재팀장" data-field="approval_leader" />
            <dx-column caption="결재처리" data-field="" cell-template="approvalProcessTemplate"  />
            <dx-column caption="반려사유" data-field="reject_reason" />
            <dx-column caption="결재결과" data-field="approval_status" cell-template="approvalResultTemplate" />
            <dx-column caption="결재일자" data-field="approval_date" data-type="date" format="yyyy-MM-dd" />
            <template #requestNumberTemplate="{ data }">
              <div class="request-number-container" title="실행계획으로 바로가기">
                <span>{{ data.data.request_number }}</span>
              </div>
            </template>
            <template #approvalProcessTemplate="{ data }">
              <div class="approval-container">
                <dx-button text="승인" class="approval-process-button approve" @click="methods.approve(data)" />
                <dx-button text="반려" class="approval-process-button reject" @click="methods.reject(data)" />
              </div>
            </template>
            <template #approvalResultTemplate="{ data }">
              <div class="approval-container">
                <span v-if="data.data.approval_status == null || data.data.approval_status == ''">대기</span>
                <dx-button v-else :text="data.data.approval_status" :class="`approval-process-button 
                ${methods.getButtonClassName(data.data.approval_status)}`" @click="methods.finalApprove(data)" />
              </div>
            </template>
            <dx-sorting mode="single" />
            <dx-export :enabled="true" />
            <dx-paging :page-size="20" />
            <dx-filter-row :visible="true" />
            <dx-column-chooser mode="select" :enabled="true" />
          </dx-data-grid>
        </div>
      </div>
    </div>
</template>

<script>
import moment from 'moment';
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';

import { alert, confirm, custom } from 'devextreme/ui/dialog';
import DxButton from 'devextreme-vue/button';
import DxCheckBox from 'devextreme-vue/check-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxColumnChooser } from 'devextreme-vue/data-grid';
import DxLookup from 'devextreme-vue/select-box';
import stateStore from '@/utils/state-store';
import CustomStore from 'devextreme/data/custom_store';
import { approvalManagement, getApprovalManagement } from '../../data-source/approval';
import SearchButtonGroup from '../../components/search-button-group.vue';
import { loadEmployee } from '../../utils/data-loader';
import { baseCodeLoader } from '../../data-source/base';
import { projectExcutionPlan } from '../../data-source/project';
import authService from '../../auth';
import { currentDateTime } from '../../utils/util';
export default {
components: {
    DxButton,
    DxCheckBox,
    DxDateBox,
    DxToolbar, DxItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem,
    DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxColumnChooser,
    SearchButtonGroup,
    DxLookup,
},
setup() {
    const router = useRouter();
    const vars = {};
    vars.grid = {};
    const currentDate = new Date();
    vars.formData = reactive({
      startDate: new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate() - 7),
      endDate: new Date(currentDate.getFullYear(), currentDate.getMonth(), currentDate.getDate(), 23, 59, 59),
      employee: null,
      approval_status: null,
    });
    vars.dataSource = reactive({
    employee: null,
    approval_status: null,
    approvalManagement: approvalManagement
    });

    
    onMounted(async () => {
    await loadEmployee(vars.dataSource);
    await methods.loadBaseCode();
    })
    const methods = {
    onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`approval-management-${key}`, evt.component);

        // methods.initSorting();
        methods.searchDateRange();
    },
    initSorting() {
        const columns = vars.grid['approval'].getVisibleColumns();
        const col = columns.filter(item => item.sortOrder);
        if (col.length == 0) {
        const defaultName = 'contract_date';
        const defaultSort = columns.filter(item => item.name == defaultName);
        if (defaultSort.length > 0) {
            vars.grid['approval'].columnOption(defaultSort[0].index, 'sortOrder', 'desc');
        }
        }
    },
    calcSupplyPrice(rowData) {
        let supply_price = 0;
        if (rowData.quote_quantity && rowData.unit_price) {
        supply_price = rowData.quote_quantity * rowData.unit_price;
        }
        rowData.supply_price = supply_price;
        return supply_price;
    },
    availableStock(rowData) {
        if (!rowData.basic_stock) return '0';
        return rowData.basic_stock.available_stock;
    },
    currentStock(rowData) {
        if (!rowData.basic_stock) return '0';
        return rowData.basic_stock.current_stock;
    },
    goProjectDetail({ data }) {
        router.push({ path: `/project/registration/${data.id}` });
    },
    searchDateRange() {
        if (vars.formData.startDate > vars.formData.endDate) {
            alert('조회 일자가 잘못 되었습니다', '조회');
            return;
        }

        try {
            vars.grid['approval'].beginCustomLoading('데이터를 집계중입니다');
            
            const filters = [];
            vars.grid['approval'].clearFilter();
            if(vars.formData.startDate){
              filters.push(['request_date', '>=', moment(vars.formData.startDate).format('YYYY-MM-DD HH:mm:ss')]);
            }
            if(vars.formData.endDate){
              filters.push(['request_date', '<=', moment(vars.formData.endDate).format('YYYY-MM-DD HH:mm:ss')]);
            }
            if(vars.formData.employee){
              filters.push(['request_name', '=', vars.formData.employee]);
            }
            if(vars.formData.approval_status){
              filters.push(['approval_status', '=', vars.formData.approval_status]);
            }
            vars.grid['approval'].filter(filters);
            vars.grid['approval'].refresh();
        } catch (ex) {
            console.log(ex);
        } finally {
            vars.grid['approval'].endCustomLoading();
        }
        // vars.grid['approval'].refresh();
    },
    loadBaseCode(){
        return baseCodeLoader(['결재상태']).then(response =>{
        vars.dataSource.approval_status = response['결재상태'];
        })
    },
    onExporting (evt) {
        approvalManagement.exportData(evt.component, '전자결재관리', `전자결재관리_${Date.now()}.xlsx`)
        evt.cancel = true
    },
    searchReset(){
        vars.formData.employee = null;
        vars.formData.approval_status = null;
    },
    async approve(object){
      if (object.data.approval_status == '팀장승인' || object.data.approval_status == '최종승인'){
        alert('이미 결재 완료된 결재입니다.', '승인');
        return;
      }
      else if (object.data.approval_status == '반려'){
        alert('결재 상태가 반려입니다.', '승인');
        // 
        return;
      }
      if (object.data.approval_leader != authService.getUserName()){
        alert('결재 담당자가 아닙니다.', '승인');
        return;
      }
    
      if (object.data.request_path == 'project_excution_plan'){
        let isSelect = await confirm('결재 승인 하시겠습니까?', '승인');
        if (!isSelect) return;
          await projectExcutionPlan.update(object.data.request_path_id, {approval_status: '팀장승인'});
          await approvalManagement.update(object.data.id, { approval_status: '팀장승인', approval_date: currentDateTime()});
          object.component.refresh();
      }
    },
    async reject(object){
      if (object.data.approval_status == '팀장승인' || object.data.approval_status == '최종승인' || object.data.approval_status == '반려'){
        alert('이미 결재 완료된 결재입니다.', '반려');
        return;
      }
      if (object.data.approval_leader != authService.getUserName()){
        alert('결재 담당자가 아닙니다.', '반려');
        return;
      }
      let isSelect = await confirm('결재 반려 하시겠습니까?', '반려');
      if (!isSelect) return;
      await custom({
          title: '반려 사유',
          messageHtml: `
              <div>
                  <label for="rejectionReason">반려 사유:</label>
                  <input type="text" id="rejectionReason" placeholder="반려 사유를 입력하세요" 
                        style="width: 100%; padding: 8px; margin-top: 5px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box;" />
              </div>
          `,
          buttons: [{
            text: '확인',
            onClick: () => {
              const rejectionReason = document.getElementById('rejectionReason').value;
              return rejectionReason;
            }
          },
          {
            text: '취소',
            onClick: () => {
              return null;
            }
          }]
        }).show().then(result => {
          if (result !== null) {
            projectExcutionPlan.update(object.data.request_path_id, {approval_status: '반려', reject_reason: result});
            approvalManagement.update(object.data.id, { approval_status: '반려', reject_reason: result, approval_date: currentDateTime()});
            object.component.refresh();
          } else {
            alert('반려가 취소 됐습니다.', '반려');
          }
        });
    },
    async finalApprove(object){
      if(object.data.approval_status != '팀장승인' ) return;
      if(authService.user.position != '대표') {
        alert('최종 승인 권한이 없습니다.', '승인');
        return;
      }
      let isSelect = await confirm('최종 승인 하시겠습니까?', '승인');
      if (!isSelect) return;
      await projectExcutionPlan.update(object.data.request_path_id, {approval_status: '최종승인'});
      await approvalManagement.update(object.data.id, { approval_status: '최종승인', approval_date: currentDateTime()});
      object.component.refresh();
      alert('최종 승인 완료되었습니다.', '승인');
    },

    cellDblClick(e){
      if(e.rowIndex == -1) return;
      if(e.column.name == 'request_number' && e.data.request_path == 'project_excution_plan'){
        window.open(
            `/project/excution-plan/${e.data.request_path_id}`,
            '_blank',
            'width=1200,height=800,top=100,left=100'
        );
      }
    },
    onRowContextMenu(e) {
      if (e.target === "content") {
        e.items = [
          {
            text: "삭제하기",
            onItemClick: async () => {
              if(authService.user.position == '대표' || authService.user.position == '팀장' || authService.user.position == '이사'){
                let isSelect = await confirm('삭제 하시겠습니까?', '삭제');
                if (!isSelect) return;
                await projectExcutionPlan.update(e.row.data.request_path_id, {approval_status: '승인요청'});
                await approvalManagement.remove(e.row.data.id);
                e.component.refresh();
              }
              else{
                alert('삭제 권한이 없습니다.', '삭제');
              }
            },
          },
        ];
      }
    },
    getButtonClassName(status){
      if(status == '팀장승인') return 'approve_leader';
      if(status == '최종승인') return 'approve';
      return 'reject';
    }

    };

    return { vars, methods, approvalManagement };
},
};
</script>
<style scoped>
.search-title{
width: 60px;
}
.approval-container{
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}
.approval-process-button {
  width: 70px;
  height: 20px;
  font-size: 10px;
  text-align: center;
  line-height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 5px;
  padding: 0;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.1s;
}

::v-deep .approval-process-button > .dx-button-content {
  padding: 0;
}

.approve {
  background-color: #008000; 
  color: #fff;
}

.approve_leader {
  background-color: #0000FF;
  color: #fff;
}

.approve:hover {
  background-color: #00a000;
}

.approve:active {
  background-color: #006000;
  transform: translateY(1px);
}

.reject {
  background-color: #FF0000;
  color: #fff;
}

.reject:hover {
  background-color: #FF3030;
}

.reject:active {
  background-color: #CC0000;
  transform: translateY(1px);
}

.request-number-container {
  cursor: pointer;
  text-decoration: underline;
}
</style>
  