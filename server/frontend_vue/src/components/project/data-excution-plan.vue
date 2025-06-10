<template>
    <dx-data-grid
        column-resizing-mode="widget"
        :data-source="vars.excutionPlan"
        :show-borders="true"
        :column-auto-width="true"
        :remote-operations="true"
        :allow-column-resizing="true"
        :allow-column-reordering="true"
        @selection-changed="methods.onSelectionChanged"
        >
        <dx-column caption="실행계획번호" data-field="excution_plan_number" data-type="string" />
        <dx-column caption="프로젝트명" data-field="project_management.project_name" data-type="string" />
        <dx-column caption="등록일자" data-field="excution_plan_date" data-type="date" format="yyyy-MM-dd" sort-order="desc" />
        <dx-column caption="등록자" data-field="excution_plan_manager" data-type="string" />
        <dx-column caption="결재상태" data-field="approval_status" data-type="string" />
        <dx-column caption="예정금액" data-field="expect_amount" data-type="number" :format="{ type: 'fixedPoint'}" />
        <dx-column caption="최종수정자" data-field="modify_manager" data-type="string" />
        <dx-column caption="최종수정일자" data-field="modify_date" data-type="date" format="yyyy-MM-dd" sort-order="desc" />
        
        <dx-paging :page-size="20" />
        <dx-filter-row :visible="true" />
        <dx-selection :mode="vars.mode" select-all-mode="page" show-check-boxes-mode="always" />
    </dx-data-grid>
</template>
<script>
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { getProjectExcutionPlan } from '../../data-source/project';
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
      excutionPlan: null,
      excutionPlanFilter: [
        {
          name: 'fk_company_id',
          op: 'eq',
          val: authService._user.fk_company_id || 0,
        }
      ]

    })

    const methods = {
      refresh: async () => {
        if(props.filters){
          vars.excutionPlanFilter.push(props.filters);
        }
        vars.excutionPlan = getProjectExcutionPlan(vars.excutionPlanFilter);
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