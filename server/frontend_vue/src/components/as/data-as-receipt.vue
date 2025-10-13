<template>
    <dx-data-grid
        column-resizing-mode="widget"
        :data-source="vars.asReceipt"
        :show-borders="true"
        :column-auto-width="true"
        :remote-operations="true"
        :allow-column-resizing="true"
        :allow-column-reordering="true"
        @selection-changed="methods.onSelectionChanged"
        >
        <dx-column caption="A/S접수번호" data-field="receipt_number" data-type="string" />
        <dx-column caption="프로젝트번호" data-field="project_management.project_number" data-type="string" />
        <dx-column caption="프로젝트명" data-field="project_management.project_name" data-type="string" />
        <dx-column caption="접수담당자" data-field="receipt_manager" data-type="string" />
        <dx-column caption="계약업체" data-field="project_management.order_company" data-type="string" />
        <dx-column caption="수요기관" data-field="project_management.contract_company" data-type="string" />
        <dx-column caption="등록부서" data-field="department" data-type="string" />
        <dx-column caption="등록담당자" data-field="manager" data-type="string" />
        <dx-column caption="계약일자" data-field="project_management.contract_date" data-type="date" format="yyyy-MM-dd" />
        <dx-column caption="하자만기" data-field="project_management.defect_end_date" data-type="date" format="yyyy-MM-dd" />
        <dx-column caption="고객사 담당자" data-field="client_manager" data-type="string" />
        <dx-column caption="고객사 담당자 연락처" data-field="client_manager_phone" data-type="string" />
        <dx-column caption="유무상구분" data-field="paid_type" data-type="string" />
        <dx-column caption="접수일자" data-field="receipt_date" data-type="date" format="yyyy-MM-dd" />
        <dx-paging :page-size="20" />
        <dx-filter-row :visible="true" />
        <dx-selection :mode="vars.mode" select-all-mode="page" show-check-boxes-mode="always" />
    </dx-data-grid>
</template>
<script>
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { getAsReceipt } from '../../data-source/as';
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
      asReceipt: null,
      asReceiptFilter: [
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
          vars.asReceiptFilter.push(props.filters);
        }
        vars.asReceipt = getAsReceipt(vars.asReceiptFilter);
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