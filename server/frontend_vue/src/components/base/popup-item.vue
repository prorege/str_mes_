<template>
    <dx-data-grid
      column-resizing-mode="widget"
      :data-source="vars.item"
      :show-borders="true"
      :allow-column-reordering="true"
      :allow-column-resizing="true"
      :column-auto-width="true"
      :remote-operations="true"
      @initialized="({ component }) => vars.component = component"
      @data-error-occurred="methods.onDataError"
      @init-new-row="methods.initNewRow"
    >
      <dx-grid-toolbar>
        <dx-grid-item template="addItemButton" location="before" />
        <dx-grid-item template="addRowButton" location="before" />
      </dx-grid-toolbar>
      <template #addItemButton>
        <dx-button text="선택된 항목 추가" icon="add" @click="methods.addSelectedRows" />
      </template>
      <template #addRowButton>
        <dx-button text="품목추가등록" icon="add" @click="methods.addRowButton" />
      </template>
      <dx-column caption="품목코드" data-field="item_code">
        <dx-grid-required-rule />
      </dx-column>
      <dx-column caption="품명" data-field="item_name">
        <dx-grid-required-rule />
      </dx-column>
      <dx-column caption="생성일자" data-field="created" data-type="date" format="yyyy-MM-dd" :allow-editing="false" sort-order="desc" :sort-index="0" />
      <dx-column caption="규격" data-field="item_standard" />
      <dx-column caption="자산구분" data-field="asset_type">
        <dx-lookup
          :data-source="vars.dataSource.asset_type"
          value-expr="code_name"
          display-expr="code_name" />
      </dx-column>
      <dx-column caption="품목그룹" data-field="item_group">
        <dx-lookup
          :data-source="vars.dataSource.item_group"
          value-expr="code_name"
          display-expr="code_name" />
      </dx-column>
      <dx-column caption="대분류" data-field="main_category" :visible="false" />
      <dx-column caption="중분류" data-field="middle_category" :visible="false" />
      <dx-column caption="소분류" data-field="sub_category" :visible="false" />
      <dx-column caption="고객사품번" data-field="client_item.client_item_code" :allow-editing="false" :visible="false" />
      <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :allow-editing="false" :calculate-display-value="methods.availableStock" />
      <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :allow-editing="false" :calculate-display-value="methods.currentStock" />
  
      <dx-paging :page-size="20" />
      <dx-selection
        select-all-mode="page"
        show-check-boxes-mode="onClick"
        mode="multiple"
      />
      <dx-filter-row :visible="true" />
      <dx-editing mode="row" :use-icons="true" :allow-adding="true" :allow-updating="true" :allow-deleting="true" />
    </dx-data-grid>
</template>

<script>
import { confirm, alert, custom } from 'devextreme/ui/dialog';
import { onMounted, reactive, ref, watch, } from 'vue';
import { baseClient, baseCodeLoader, getBaseItem } from '../../data-source/base';
import { DxButton } from 'devextreme-vue/button';
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow, DxToolbar as DxGridToolbar, DxItem as DxGridItem, DxRequiredRule as DxGridRequiredRule, DxLookup, DxEditing} from 'devextreme-vue/data-grid';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import authService from '../../auth';

export default {
  props: {
    multiple: {
      type: Boolean,
      default: false,
    },
    toggle: {
      type: Boolean,
      default: false,
    },
    filters: {
      type: String
    }
  },
  components: { DxDataGrid, DxColumn, DxSelection, DxPaging, DxFilterRow, DxGridToolbar, DxItem, DxGridItem, DxGridRequiredRule, DxLookup, DxEditing, DxToolbar, DxButton},
  setup(props, { emit }) {
    onMounted(async () => {
      methods.refresh();
      await methods.loadBaseCode();
    });

    const vars = reactive({
      item: null,
      itemFilter: [
        {
          name: 'fk_company_id',
          op: 'eq',
          val: authService._user.fk_company_id || 0,
        },
      ],
      dataSource: {
        asset_type: [],
        item_group: [],
      },
      component: undefined
    });


    const methods = {
      refresh: async () => {
        vars.item = getBaseItem(null, null, props.filters);
      },
      async addSelectedRows(){
        if(vars.component){
          const rows = await vars.component.getSelectedRowsData();
          if(rows){
            emit('baseItemChange', rows);
          }
        }
        
      },
      addRowButton(){
        if(vars.component){
          vars.component.addRow();
        }
      },
      loadBaseCode(){
        return baseCodeLoader(
        ['자산구분', '품목그룹'],
        authService.getCompanyId()
      ).then(response => {
        vars.dataSource.asset_type = response['자산구분'];
        vars.dataSource.item_group = response['품목그룹'];
      })
      },
      availableStock(rowData) {
        if (!rowData.basic_stock) { return '0'; }
        return rowData.basic_stock.available_stock;
      },
      currentStock(rowData) {
        if (!rowData.basic_stock) { return '0'; }
        return rowData.basic_stock.current_stock;
      },
      initGird(){
        methods.refresh();
        if (vars.component) {
          vars.component.clearSelection();
          vars.component.clearFilter();
          vars.component.refresh();
        }

      },
      initNewRow(e){
        e.data.fk_company_id = authService._user.fk_company_id;
      },
      onDataError(e) {
        if (e.error.response.status == 605) {
          e.error.message = '연결된 데이터가 있어서 삭제가 안됩니다';
          alert(`${e.error.response.data.message}<br/><br/>테이블에 연결된 데이터가 있어서 삭제가 안됩니다.<br/>데이터 삭제 후 다시 시도해 주세요.`, '삭제 오류');
        }
      },
    };
    watch(
      () => props.toggle,
      () => methods.initGird()
    );

    return {
      vars,
      methods,
    };
  },
};
</script>
