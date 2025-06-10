<template>
    <dx-data-grid
    column-resizing-mode="widget"
    :data-source="dataSource"
    :show-borders="true"
    :allow-column-reordering="true"
    :allow-column-resizing="true"
    :column-auto-width="true"
    :remote-operations="true"
    @initialized="({ component }) => grid = component"
    >   
        <dx-grid-toolbar>
            <dx-grid-item template="addItemButton" location="before" />
        </dx-grid-toolbar>
        <template #addItemButton>
          <dx-button text="선택된 항목 추가" icon="add" @click="addSelectedRows" />
        </template>
        <dx-column caption="이름" data-field="emp_name" :allow-editing="false" />
        <dx-column caption="직급" data-field="emp_position" :allow-editing="false" />
        <dx-column caption="직통번호" data-field="emp_direct_phone" :allow-editing="false" />
        <dx-column caption="전화번호" data-field="emp_mobile" :allow-editing="false" />
        <dx-column caption="이메일" data-field="emp_email" :allow-editing="false" />
        <dx-paging :page-size="20" />
        <dx-selection
        select-all-mode="page"
        show-check-boxes-mode="onClick"
        mode="multiple"
        />
        <dx-filter-row :visible="true" />
    </dx-data-grid>
</template>
<script setup>
import { DxDataGrid, DxColumn, DxPaging, DxSelection, DxFilterRow, DxItem as DxGridItem, DxToolbar as DxGridToolbar, } from 'devextreme-vue/data-grid'
import { ref, reactive, watch, defineEmits, defineProps } from 'vue'
import { getBaseEmployee } from '@/data-source/base'
import { DxButton } from 'devextreme-vue/button';
const emit = defineEmits(['change'])
const grid = ref();
const dataSource = ref();
dataSource.value = getBaseEmployee();

async function addSelectedRows () {
    if(grid.value){
        const rows = await grid.value.getSelectedRowsData();
        if(rows){
            emit('change', rows)
        }
    }
  
}
</script>