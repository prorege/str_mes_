<template>
        <dx-data-grid
            column-resizing-mode="widget"
            :data-source="vars.business"
            :show-borders="true"
            :column-auto-width="true"
            :remote-operations="true"
            :allow-column-resizing="true"
            :allow-column-reordering="true"
            @selection-changed="methods.onSelectionChanged"
            >
            <dx-column caption="영업번호" data-field="business_number" data-type="string" />
            <dx-column caption="영업건명" data-field="business_name" data-type="string" />
            <dx-column caption="영업일자" data-field="business_date" data-type="date" format="yyyy-MM-dd" sort-order="desc" />
            <dx-column caption="관련업체명" data-field="client_company" data-type="string" />
            <dx-column caption="업체담당자" data-field="client_manager" data-type="string" />
            <dx-column caption="영업금액" data-field="business_amount" data-type="number" :format="{ type: 'fixedPoint'}" />
            <dx-column caption="담당부서" data-field="business_department" data-type="string" />
            <dx-column caption="당사담당자" data-field="business_manager" data-type="string" />
            <dx-column caption="현재단계" data-field="business_status" data-type="string" />
            <dx-column caption="진행현황" data-field="business_progress" data-type="string" />
            <dx-column caption="중요" data-field="business_important" data-type="string" />
            <dx-column caption="최종수정자" data-field="modify_manager" data-type="string" />
            <dx-column caption="최종수정일자" data-field="modify_date" data-type="date" format="yyyy-MM-dd" />
            <dx-column caption="프로젝트번호" data-field="project.project_number" data-type="string" />
            
            <dx-paging :page-size="20" />
            <dx-filter-row :visible="true" />
            <dx-selection :mode="vars.mode" select-all-mode="page" show-check-boxes-mode="always" />
        </dx-data-grid>
</template>
<script>
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { getProjectBusiness } from '../../data-source/project';
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
          business: null,
          businessFilter: [
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
              vars.businessFilter.push(props.filters);
            }
            vars.business = getProjectBusiness(vars.businessFilter);
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