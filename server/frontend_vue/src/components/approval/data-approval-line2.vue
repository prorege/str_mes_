<template>
  <div style="display: flex; flex-direction: row; gap: 10px;">
    <div>
        <span>경영지원팀 결재선 지정</span>
        <dx-data-grid
            column-resizing-mode="widget"
            height="300px"
            :data-source="vars.dataSource.approvalLine"
            date-serialization-format="yyyy-MM-ddTHH:mm:ss"
            :show-borders="true"
            :column-auto-width="true"
            :remote-operations="true"
            :focused-row-enabled="true"
            :allow-column-resizing="true"
            :allow-column-reordering="true"
            :row-alternation-enabled="true"
            @init-new-row=" (e) => methods.onInitNewRow(e, '1')"
            @initialized="({ component }) => grid = component"
        >
        <dx-grid-toolbar>
            <dx-grid-item name="addRowButton" location="after" />
            <dx-grid-item name="deleteRowButton" location="after" />
            <dx-grid-item name="saveButton" location="after" />
            <dx-grid-item name="cancelButton" location="after" />
        </dx-grid-toolbar>
            <dx-column caption="순서" data-field="line_order" alignment="center" :sort-index="0" sort-order="asc" />
            <dx-column caption="직급, 직책" data-field="line_header" alignment="center">
                <dx-lookup 
                    :data-source="vars.dataSource.code" 
                    display-expr="code_name" 
                    value-expr="code_name"
                />
            </dx-column>
            <dx-column caption="상신자" data-field="fk_request_emp_id" :allow-editing="false" alignment="center">
                <dx-lookup :data-source="vars.dataSource.employee" display-expr="emp_name" value-expr="id" />
            </dx-column>
            <dx-column caption="결재자" data-field="fk_approval_emp_id" alignment="center">
                <dx-lookup :data-source="vars.dataSource.employee" display-expr="emp_name" value-expr="id" />
            </dx-column>
            <dx-scrolling mode="standard" />
            <dx-sorting mode="multiple" />
            <dx-editing mode="batch" :use-icons="true" :allow-adding="true" :allow-updating="true" :allow-deleting="true" />

        </dx-data-grid>
    </div>
    <div>
        <span>담당 부서 결재선 지정</span>
        <dx-data-grid
            column-resizing-mode="widget"
            height="300px"
            :data-source="vars.dataSource.approvalLine2"
            date-serialization-format="yyyy-MM-ddTHH:mm:ss"
            :show-borders="true"
            :column-auto-width="true"
            :remote-operations="true"
            :focused-row-enabled="true"
            :allow-column-resizing="true"
            :allow-column-reordering="true"
            :row-alternation-enabled="true"
            @init-new-row=" (e) => methods.onInitNewRow(e, '2')"
            @initialized="({ component }) => grid2 = component"
        >
        <dx-grid-toolbar>
            <dx-grid-item name="addRowButton" location="after" />
            <dx-grid-item name="deleteRowButton" location="after" />
            <dx-grid-item name="saveButton" location="after" />
            <dx-grid-item name="cancelButton" location="after" />
        </dx-grid-toolbar>
            <dx-column caption="순서" data-field="line_order" alignment="center" :sort-index="0" sort-order="asc" />
            <dx-column caption="직급, 직책" data-field="line_header" alignment="center">
                <dx-lookup 
                    :data-source="vars.dataSource.code" 
                    display-expr="code_name" 
                    value-expr="code_name"
                />
            </dx-column>
            <dx-column caption="상신자" data-field="fk_request_emp_id" :allow-editing="false" alignment="center">
                <dx-lookup :data-source="vars.dataSource.employee" display-expr="emp_name" value-expr="id" />
            </dx-column>
            <dx-column caption="결재자" data-field="fk_approval_emp_id" alignment="center">
                <dx-lookup :data-source="vars.dataSource.employee" display-expr="emp_name" value-expr="id" />
            </dx-column>
            <dx-scrolling mode="standard" />
            <dx-sorting mode="multiple" />
            <dx-editing mode="batch" :use-icons="true" :allow-adding="true" :allow-updating="true" :allow-deleting="true" />

        </dx-data-grid>
    </div>
    
        
  </div>
</template>

<script>
import { reactive, ref, watch, onMounted } from 'vue';
import { notifyInfo, notifyError } from '../../utils/notify';
import DxButton from 'devextreme-vue/button';
import { DxDataGrid, DxColumn, DxPaging, DxEditing, DxSorting, DxSelection, DxFilterRow, DxScrolling,
    DxColumnChooser, DxLookup, DxToolbar as DxGridToolbar, DxItem as DxGridItem } from 'devextreme-vue/data-grid';
import { baseEmployee, baseCodeLoader } from '../../data-source/base';
import { getApprovalLine } from '../../data-source/approval';
export default {
components: {
    DxButton,
    DxDataGrid, DxColumn, DxPaging, DxEditing, DxSorting, DxSelection, DxFilterRow, DxColumnChooser, DxGridToolbar, DxGridItem, DxLookup, DxScrolling,
},
props: {
    formData: {
        type: Object,
        required: true,
    },
},
setup(props) {
    const vars = {};
    const grid = ref();
    const grid2 = ref();
    vars.dataSource = reactive({
        employee: [],
        approvalLine: [],
        approvalLine2: [],
        code: [],
    });
   
    onMounted(async () => {
        await methods.loadBaseCode();
    })
    const methods = {
        loadBaseCode() {
            baseEmployee.load().then((res) => {
            vars.dataSource.employee = [{emp_name: ''}, ...res.data];
            })
            return baseCodeLoader([
            '직급',
            ])
            .then((response) => {
                vars.dataSource.code = response['직급'];
            })
        },
        onInitNewRow(e, type) {
            e.data.fk_document_id = props.formData.document_id;
            e.data.line_type = type;
            e.data.fk_request_emp_id = props.formData.emp_id;
        },
      
        setCellValue(newData, value, currentRowData) {
            newData.fk_approval_emp_id = value;
            const emp = vars.dataSource.employee.find(item => item.id == value);
            newData.line_header = emp.emp_position;
        }
    }
    watch(() => props.formData, () => {
        vars.dataSource.approvalLine = [];
        vars.dataSource.approvalLine2 = [];
        console.log("props.formData : ", props.formData)
        vars.dataSource.approvalLine = getApprovalLine([
            {
                name: 'fk_request_emp_id', op: 'eq', val: props.formData.emp_id
            },
            {
                name: 'fk_document_id', op: 'eq', val: props.formData.document_id
            },
            {
                name: 'line_type', op: 'eq', val: '1'
            }
        ])
        vars.dataSource.approvalLine2 = getApprovalLine([
            {
                name: 'fk_request_emp_id', op: 'eq', val: props.formData.emp_id
            },
            {
                name: 'fk_document_id', op: 'eq', val: props.formData.document_id
            },
            {
                name: 'line_type', op: 'eq', val: '2'
            }
        ])
        if(grid.value){
            grid.value.refresh();
        }
        if(grid2.value){
            grid2.value.refresh();
        }
    }, { immediate: true })
    return {
        vars,
        grid,
        grid2,
        methods,
    }
}
}
</script>

<style>

</style>