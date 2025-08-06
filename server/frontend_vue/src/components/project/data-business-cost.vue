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
        <dx-column caption="순서" data-field="item_order" :allow-editing="false" />
        <dx-column caption="품목코드" data-field="item_code" :allow-editing="false" />
        <dx-column caption="품명" data-field="item.item_name" :allow-editing="false" />
        <dx-column caption="규격" data-field="item.item_standard" :allow-editing="false" />
        <dx-column caption="단위" data-field="item.unit" :allow-editing="false" />
        <dx-column caption="견적수량" data-field="quote_quantity" data-type="number" :allow-editing="false" />
        <dx-column caption="견적단가" data-field="quote_unit_price" data-type="number" format="currency" :allow-editing="false" />
        <dx-column caption="견적금액" data-field="quote_supply_price" data-type="number" format="currency" :allow-editing="false" />
        <dx-column caption="구매단가" data-field="purchase_unit_price" data-type="number" format="currency" :allow-editing="false" />
        <dx-column caption="구매금액" data-field="purchase_supply_price" data-type="number" format="currency" :allow-editing="false" />
        <dx-column caption="DC Rate" data-field="dc_rate" data-type="number" format="percent" :allow-editing="false" />
        <dx-paging :page-size="10" />
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
import { getProjectBusinessCost } from '@/data-source/project'
import { DxButton } from 'devextreme-vue/button';
const emit = defineEmits(['change'])
const grid = ref();
const dataSource = ref([]);

async function addSelectedRows () {
    if(grid.value){
        const rows = await grid.value.getSelectedRowsData();
        if(rows){
            emit('change', rows)
        }
    }
}
const props = defineProps({
    business_id: {
        type: Number,
        default: 0,
    }
})
watch(() => props.business_id, (newVal) => {
    dataSource.value = [];
    dataSource.value = getProjectBusinessCost([
        {name: 'fk_business_id', op: 'eq', val: newVal}
    ]);
    if(grid.value){
        grid.value.refresh();
    }
}, { immediate: true }) 
</script>