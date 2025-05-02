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
    @init-new-row="initManagerInsertedRow"
    @selection-changed="onSelectionChanged"
  >
    <dx-grid-toolbar>
        <dx-grid-item template="addRowButton" location="before" />
    </dx-grid-toolbar>
    <template #addRowButton>
        <dx-button text="담당자 추가" icon="add" @click="addRowButton" />
    </template>
    <dx-column caption="번호" data-field="id" sort-order="desc" :allow-editing="false" :visible="false"/>
    <dx-column caption="생성시간" data-field="created" data-type="date" format="yyyy-MM-dd" :allow-editing="false" :visible="false" sort-order="desc" :sort-index="0" />
    <dx-column caption="거래처담당자" data-field="name" :allow-editing="true" :visible="true">
      <dx-grid-required-rule />
    </dx-column>
    <dx-column caption="부서" data-field="department" :allow-editing="true" :visible="true" />
    <dx-column caption="직급" data-field="position" :allow-editing="true" :visible="true">
      <dx-lookup value-expr="code_name" display-expr="code_name" :data-source="common.position_code" />
    </dx-column>
    <dx-column caption="휴대폰번호" data-field="mobile" :allow-editing="true" :visible="true" />
    <dx-column caption="이메일주소" data-field="email" :allow-editing="true" :visible="true" />
    <dx-column caption="직통전화번호" data-field="direct_phone" :allow-editing="true" :visible="true" />
    <dx-column caption="내선번호" data-field="ext_phone" :allow-editing="true" :visible="true" />
    <dx-column caption="비고" data-field="etc" :allow-editing="true" :visible="true" />
    <dx-column caption="거래처 ID" data-field="fk_client_id" :allow-editing="false" :visible="false" />

    <dx-paging :page-size="20" />
    <dx-selection
      select-all-mode="page"
      show-check-boxes-mode="always"
      mode="single"
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

<script setup>
import moment from 'moment'
import { DxDataGrid, DxColumn, DxPaging, DxLookup, DxSelection, DxFilterRow, DxEditing, DxRequiredRule as DxGridRequiredRule, DxToolbar as DxGridToolbar, DxItem as DxGridItem } from 'devextreme-vue/data-grid';
import { DxButton } from 'devextreme-vue/button';
import { getBaseClientManager, baseCodeLoader } from '@/data-source/base';
import { ref, reactive, watch, defineEmits, defineProps } from 'vue'

const emit = defineEmits(['change'])
const props = defineProps({
  filters: { type: Object }
})
const common = reactive({ position_code: [] })
const grid = ref()
const dataSource = ref()
baseCodeLoader(['직급']).then(response => {
  common.position_code = response['직급']
})

setFilter()

watch(
  () => props.filters,
  () => setFilter()
)

function setFilter () {
  dataSource.value = getBaseClientManager([
    {
      name: 'fk_client_id',
      op:'eq',
      val: props.filters.fk_client_id
    }
  ])
  if (props.filters.name) grid.value?.option('filterValue', [['name', 'contains', props.filters.name]])
  if(grid.value){
    grid.value.refresh();
  }
}

function addRowButton(){
  if(grid.value){
    grid.value.addRow();
  }
}

function initManagerInsertedRow ({ data }) {
  console.log('initManagerInsertedRow')
  data.created = moment().format('YYYY-MM-DD HH:mm:ss')
  data.fk_client_id = props.filters.fk_client_id
}

function onSelectionChanged ({ selectedRowsData }) {
  emit('change', selectedRowsData[0])
}
</script>