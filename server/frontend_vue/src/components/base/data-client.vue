<template>
  <dx-data-grid
    column-resizing-mode="widget"
    :data-source="baseClient"
    :show-borders="true"
    :allow-column-reordering="true"
    :allow-column-resizing="true"
    :column-auto-width="true"
    :remote-operations="true"
    @initialized="onInitialized"
    @init-new-row="initClinetInsertedRow"
    @selection-changed="onSelectionChanged"
  >
    <dx-grid-toolbar>
        <dx-grid-item template="addRowButton" location="before" />
    </dx-grid-toolbar>
    <template #addRowButton>
        <dx-button text="업체추가" icon="add" @click="addRowButton" />
    </template>
    <dx-column caption="업체약칭" data-field="alias" data-type="string">
      <dx-grid-required-rule />
    </dx-column>
    <dx-column caption="업체명" data-field="name" data-type="string" :filter-value="vars.filterValue">
      <dx-grid-required-rule />
    </dx-column>
    <dx-column caption="생성일자" data-field="created" data-type="date" format="yyyy-MM-dd" :allow-editing="false" sort-order="desc" :sort-index="0" />
    <dx-column caption="사업자번호" data-field="business_number" data-type="string" />
    <dx-column caption="대표자" data-field="ceo_name" data-type="string" />
    <dx-column caption="주소" data-field="address" data-type="string" />
    <dx-column caption="거래처구분" data-field="client_type" data-type="string" />
    <dx-column caption="비고" data-field="etc" data-type="string" />

    <dx-paging :page-size="20" />
    <dx-selection
      select-all-mode="page"
      show-check-boxes-mode="always"
      :mode="mode"
    />
    <dx-editing mode="row"
      :use-icons="true"
      :allow-adding="true"
      :allow-updating="true"
      :allow-deleting="true"
    />
    <dx-filter-row :visible="true" />
  </dx-data-grid>
</template>

<script>
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow, DxEditing, DxRequiredRule as DxGridRequiredRule, DxToolbar as DxGridToolbar, DxItem as DxGridItem } from 'devextreme-vue/data-grid';
import { DxButton } from 'devextreme-vue/button';
import { baseClient } from '../../data-source/base';
import { reactive, watch } from 'vue'
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
  components: { DxDataGrid, DxColumn, DxSelection, DxPaging, DxFilterRow, DxEditing, DxGridRequiredRule, DxGridToolbar, DxGridItem, DxButton },
  setup(props, { emit }) {
    baseClient.defaultFilters = [{ name: 'trade_yn', op: 'eq', val: false }]
    const onSelectionChanged = ({ selectedRowsData }) => {
      if (!props.multiple && selectedRowsData)
        selectedRowsData = selectedRowsData[0];
      emit('change', selectedRowsData);
    };
    let component = undefined
    const vars = reactive({ filterValue: '' })

    function onInitialized (e) {
      component = e.component
      setFilter()
    }

    function setFilter () {
      if (!component) return
      if (!props.filters || !props.filters.name) {
        vars.filterValue = ''
        return
      }

      if (props.filters.name) {
        vars.filterValue = props.filters.name
      }
    }

    function initClinetInsertedRow({data}){
      data.fk_company_id = authService.getCompanyId();
    }
    function addRowButton(){
      if(component){
        component.addRow();
      }
    }
    watch(
      () => props.filters,
      () => setFilter()
    );

    return {
      vars,
      mode: props.multiple ? 'multiple' : 'single',
      baseClient,
      onSelectionChanged, onInitialized, initClinetInsertedRow, addRowButton
    };
  },
};
</script>
