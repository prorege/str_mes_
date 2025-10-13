<template>
    <dx-data-grid
        column-resizing-mode="widget"
        :data-source="vars.asResult"
        :show-borders="true"
        :column-auto-width="true"
        :remote-operations="true"
        :allow-column-resizing="true"
        :allow-column-reordering="true"
        @selection-changed="methods.onSelectionChanged"
        >
        <dx-column caption="A/S처리번호" data-field="receipt_number" data-type="string" />
        <dx-column caption="A/S접수번호" data-field="as_receipt.receipt_number" data-type="string" />
        <dx-column caption="프로젝트명" data-field="project_management.project_name" data-type="string" />
        <dx-column caption="프로젝트번호" data-field="project_management.project_number" data-type="string" />
        <dx-column caption="접수부서" data-field="as_receipt.department" data-type="string" />
        <dx-column caption="접수담당자" data-field="as_receipt.manager" data-type="string" />
        <dx-column caption="처리부서" data-field="result_department" data-type="string" />
        <dx-column caption="처리담당자" data-field="result_manager" data-type="string" />
        <dx-column caption="처리일자" data-field="result_date" data-type="date" format="yyyy-MM-dd" />
        <dx-column caption="접수일자" data-field="as_receipt.receipt_date" data-type="date" format="yyyy-MM-dd" />
        <dx-paging :page-size="20" />
        <dx-filter-row :visible="true" />
        <dx-selection :mode="vars.mode" select-all-mode="page" show-check-boxes-mode="always" />
    </dx-data-grid>
</template>
<script>
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { getAsResult } from '../../data-source/as';
import { watch, onMounted, reactive, ref } from 'vue';
import authService from '../../auth';

export default {
props: {
multiple: {
  type: Boolean,
  default: false,
},
filters: {
  type: Object
},
},
components: { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow },

setup(props, { emit }){
    onMounted(() => {
      methods.refresh();
    });
    const vars = reactive({
      mode: props.multiple ? 'multiple' : 'single',
      asResult: null,
      asResultFilter: [
        {
          name: 'fk_company_id',
          op: 'eq',
          val: authService._user.fk_company_id || 0,
        },
      ]

    })

    const methods = {
      refresh: async () => {
        if(props.filters){
          vars.asResultFilter.push(props.filters);
        }
        vars.asResult = getAsResult(vars.asResultFilter);
      },
      onSelectionChanged: ({ selectedRowsData }) => {
        if (!props.multiple && selectedRowsData)
            selectedRowsData = selectedRowsData[0];
          emit('change', selectedRowsData);
      },
    }

    watch(
      () => props.filters,
      () => methods.refresh()
    );

    return {
        vars,
        methods,
    };
  }
}
</script>