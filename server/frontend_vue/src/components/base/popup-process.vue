<template>
  <dx-popup
    :visible="props.visible"
    content-template="popup-content"
    title="공정 선택"
    width="430px"
    height="450px"
    :resize-enabled="true"
    :close-on-outside-click="true"
    @update:visible="(value) => emit('update:visible', value)"
  >
    <DxToolbarItem
      widget="dxButton" toolbar="top" location="after"
      :options="{ text: '선택된 항목 추가', icon: 'add', onClick: addSelectedRows }"
    />

    <template #popup-content>
      <dx-scroll-view width="100%" height="100%">

        <dx-data-grid
          column-resizing-mode="widget"
          :data-source="baseProcess"
          :show-borders="true"
          :allow-column-reordering="true"
          :allow-column-resizing="true"
          :column-auto-width="true"
          :remote-operations="true"
          @initialized="({ component }) => grid = component"
        >
          <dx-column caption="번호" data-field="id" :visible="false" />
          <dx-column caption="공정코드" data-field="process_code" :visible="false" />
          <dx-column caption="공정명" data-field="process_name" sort-order="desc" />
          <dx-column caption="단위" data-field="unit" />

          <dx-paging :page-size="20" />
          <dx-selection
            select-all-mode="allPages"
            show-check-boxes-mode="always"
            mode="multiple"
          />
          <dx-filter-row :visible="true" />
        </dx-data-grid>

      </dx-scroll-view>
    </template>
  </dx-popup>
</template>

<script setup>
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxScrollView } from 'devextreme-vue/scroll-view';
import { DxDataGrid, DxColumn, DxPaging, DxLookup, DxSelection, DxFilterRow } from 'devextreme-vue/data-grid';
import { baseProcess } from '@/data-source/base';
import { ref, reactive, watch, defineEmits, defineProps } from 'vue'

const emit = defineEmits(['selected', 'update:visible'])
const props = defineProps({
  visible: { type: Boolean }
})
const grid = ref()

watch(
  () => props.visible,
  () => {
    if (props.visible && grid.value) {
      grid.value.clearSelection()
    }
  }
)

function addSelectedRows () {
  emit('selected', grid.value.getSelectedRowsData())
  emit('update:visible', false)
}

</script>