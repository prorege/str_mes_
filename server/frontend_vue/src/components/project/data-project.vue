<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="vars.project"
    :show-borders="true"
    :column-auto-width="true"
    :remote-operations="true"
    :allow-column-resizing="true"
    :allow-column-reordering="true"
    @selection-changed="methods.onSelectionChanged"
  >
    <dx-column caption="프로젝트번호" data-field="project_number" :sort-index="1" sort-order="desc" />
    <dx-column caption="프로젝트명" data-field="project_name" />
    <dx-column caption="등록일자" data-field="project_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
    <dx-column caption="원발주처" data-field="order_company" />
    <dx-column caption="원청업체" data-field="contract_company" />
    <dx-column caption="등록부서" data-field="project_department" />
    <dx-column caption="등록담당자" data-field="project_manager" />
    <dx-column caption="계약일자" data-field="contract_date" data-type="date" format="yyyy-MM-dd" />
    <dx-column caption="하자만기" data-field="defect_end_date" data-type="date" format="yyyy-MM-dd" />
    <dx-column caption="원청금액" data-field="contract_amount" />
    <dx-column caption="준공일자" data-field="completion_date" data-type="date" format="yyyy-MM-dd" />
    <dx-column caption="하자기간" data-field="defect_period" />
    <dx-column caption="자사금액" data-field="company_amount" />

    <dx-column caption="진행단계" data-field="progress_status" />
    <dx-column caption="연결영업 번호" data-field="business.business_number" />
    <dx-column caption="중요" data-field="project_important" />
    
    <dx-paging :page-size="20" />
    <dx-filter-row :visible="true" />
    <dx-selection :mode="vars.mode" select-all-mode="page" show-check-boxes-mode="always" />
  </dx-data-grid>
</template>

<script>
import { onMounted, reactive, watch } from 'vue';

import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';

import { getProjectRegistration } from '../../data-source/project';
import authService from '../../auth';

export default {
  props: {
    multiple: {
      type: Boolean,
      default: false,
    },
    filters: {
      type: Object
    }
  },
  components: { DxDataGrid, DxColumn, DxSelection, DxPaging, DxFilterRow },
  setup(props, { emit }) {
    onMounted(() => {
      methods.refresh();
    });

    const vars = reactive({
      mode: props.multiple ? 'multiple' : 'single',
      project: null,
      projectFilter: [
        {
          name: 'fk_company_id',
          op: 'eq',
          val: authService._user.fk_company_id || 0,
        },
      ],

    });

    const methods = {
      refresh: async () => {
        if(props.filters){
          vars.projectFilter.push(props.filters)
        }
        vars.project = getProjectRegistration(vars.projectFilter);
        
      },
      onSelectionChanged: ({ selectedRowsData }) => {
        if (!props.multiple && selectedRowsData)
          selectedRowsData = selectedRowsData[0];
        emit('change', selectedRowsData);
      },
    };
    watch(
      () => props.filters,
      () => methods.refresh()
    );
    return {
      vars,
      methods,
    };
  },
};
</script>
