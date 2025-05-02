<template>
    <div>
      <div class="content-block">
        <div class="dx-card responsive-paddings back-colored">
  
          <div class="content-header">
            <dx-toolbar class="back-colored">
              <dx-item location="before">
                <div class="content-title">실행계획발주보내기</div>
              </dx-item>
            </dx-toolbar>
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
            :allow-column-reordering="false"
            :row-alternation-enabled="true"
            :data-source="dataSource"
            :on-initialized="evt => methods.onGridInitialized(evt, 'status')"
            @row-dbl-click="methods.goExcutionPlanDetail"
            @cell-click="methods.cellClick"
          >
            <dx-grid-toolbar>
                <dx-grid-item template="exportToPurchaseOrder" location="before" />
            </dx-grid-toolbar>
            <template #exportToPurchaseOrder>
                <dx-button text="발주로 내보내기" icon="export" @click="methods.exportToPurchaseOrder" />
            </template>
            <dx-column caption="발주여부" data-field="closing_yn" data-type="boolean" />
            <dx-column caption="발주번호" data-field="" cell-template="order_number" />
            <dx-column caption="실행계획번호" data-field="project_excution_plan.excution_plan_number" />
            <dx-column caption="결재상태" data-field="project_excution_plan.approval_status" />
            <dx-column caption="발주일자" data-field="order_date" data-type="date" format="yyyy-MM-dd" />
            <dx-column caption="변경납기일자" data-field="order_date_modify" data-type="date" format="yyyy-MM-dd" />
            <dx-column caption="발주처" data-field="main_supplier" />
            <dx-column caption="발주확정" data-field="confirmed" data-type="boolean" />
            <dx-sorting mode="single" />
            <dx-paging :enabled="false" />
            <dx-column-chooser mode="select" :enabled="true" />
            <template #order_number="{data}">
                <div class="order_number" @click="methods.emptyOrderNumber(data)">발주 바로가기</div>
            </template>
          </dx-data-grid>
        </div>
      </div>
    </div>
</template>

<script>
import moment from 'moment';

import { reactive, onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

import { alert } from 'devextreme/ui/dialog';
import DxButton from 'devextreme-vue/button';
import DxCheckBox from 'devextreme-vue/check-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxColumnChooser, DxToolbar as DxGridToolbar, DxItem as DxGridItem } from 'devextreme-vue/data-grid';
import DxLookup from 'devextreme-vue/select-box';
import stateStore from '@/utils/state-store';
import ArrayStore from 'devextreme/data/array_store';
import CustomStore from 'devextreme/data/custom_store';
import { projectExcutionPlanItem, getProjectExcutionPlanItem } from '../../data-source/project';
import SearchButtonGroup from '../../components/search-button-group.vue';
import { purchaseOrderItem } from '../../data-source/purchase';
import ApiService from '../../utils/api-service';
import authService from '../../auth';

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
    DxGridToolbar, DxGridItem,
},
setup() {
    const router = useRouter();
    const vars = {};
    vars.grid = {};

    const dataSource = ref(getProjectExcutionPlanItem([
        { name: 'project_excution_plan', op: 'has', val: { name: 'approval_status', op: 'eq', val: '승인완료'}},
        { name: 'confirmed', op: 'eq', val: true},
        { name: 'order_date', op: 'lte', val: moment().format('YYYY-MM-DD HH:mm:ss')},
        { name: 'closing_yn', op: 'eq', val: false}
    ]))

    const methods = {
        onGridInitialized(evt, key) {
            vars.grid[key] = evt.component;
            stateStore.bind(`excution-plan-to-order-${key}`, evt.component);
        },
        goExcutionPlanDetail({ data }) {
            router.push({ path: `/project/excution-plan/${data.id}` });
        },
        async exportToPurchaseOrder() {
            const itemIdList = [];
            const rows = vars.grid.status.getVisibleRows();

            const rows_check = rows.filter(v => v.data.closing_yn);
            if(rows_check.length <= 0){
                alert('선택된 품목이 없습니다', '발주로 내보내기');
                return;
            }
            for(let row of rows_check){
                itemIdList.push(row.data.id);
            }
            const params = {
                id: null,
                department: rows_check[0].data.project_excution_plan.excution_plan_department,
                manager: rows_check[0].data.project_excution_plan.excution_plan_manager,
                company_id: authService.getCompanyId(),
                excution_plan_ids: itemIdList,
            };
            try{
                const api = new ApiService('/api/mes/v1/project/excution-item-to-order');
                await api.post('', params);
                alert('발주로 내보내기가 완료되었습니다', '발주로 내보내기');
            }catch(ex){
                alert('발주로 내보내기가 실패했습니다', '발주로 내보내기');
            }
        },
        async cellClick(e) {
            if(e.rowIndex == -1) return;
            if(e.column.caption != '발주여부') return;
            const { data } = await dataSource.value.byKey(e.data.id);
            if (data.closing_yn) return;
            vars.grid.status.cellValue(e.rowIndex, e.columnIndex, !e.data.closing_yn);
        },
        async emptyOrderNumber(row) {
            const { data } = await purchaseOrderItem.load({filter : [ 'fk_excution_plan_item_id', '=', row.data.id] })
            if(data.length <= 0) return;
            window.open(
                `/purchase/order/${data[0].order.id}`, 
                '_blank',
                'noopener,noreferrer'
            );
            vars.grid.status.refresh();
        }
    };
    return { vars, methods, dataSource };

}
}
</script>
<style scoped>
.search-title{
width: 60px;
}
.order_number {
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    border: 1px solid #4a8ac5;
    border-radius: 6px;
    font-size: 11px;
    background-color: #5b9bd5;
    transition: all 0.2s ease;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    margin: 2px;
    color: #fff;
}

.order_number:hover {
    background-color: #fff;
    color: #5b9bd5;
    border-color: #5b9bd5;
    box-shadow: 0 2px 4px rgba(91,155,213,0.2);
}

.order_number:active {
    background-color: #f8f9fa;
    color: #5b9bd5;
    transform: translateY(1px);
    box-shadow: 0 1px 2px rgba(91,155,213,0.1);
}
</style>
  