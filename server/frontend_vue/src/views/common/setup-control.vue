<script setup>
import {
  DxDataGrid,
  DxColumn,
  DxEditing,
  DxPaging,
  DxLookup,
  DxItem,
  DxToolbar
} from 'devextreme-vue/data-grid';
import DxButton from 'devextreme-vue/button';
import { DxSelectBox } from 'devextreme-vue/select-box'
import { setupMenu, getSetupMenu } from '@/data-source/setup'
import { ref, reactive ,watch, onMounted, nextTick, onUnmounted } from 'vue'
import { beforeExitConfirm } from '../../utils/util';
import auth from '../../auth';
import { useRouter, useRoute } from 'vue-router';
import { confirm, alert } from 'devextreme/ui/dialog';
const router = useRouter();
const route = useRoute();
let grid = undefined
const formState = ref(false);
beforeExitConfirm.check(()=> formState.value);
const displayExpr = [
  { name: '상용안함', value: false},
  { name: '사용함', value: true},
];
const updated = reactive({})

setupMenu.defaultFilters = [{name: 'menu_name', op: 'eq', val: '가입고'}]

async function saveButton(){
  if(grid?.hasEditData()){
    grid.saveEditData();
    if(Object.keys(updated).length > 0){
      for(let menu in updated){
        const {data : related} = await getSetupMenu().load({
          filter: [
            ['menu_name', 'contain', menu]
          ],
        })
        if(related){
          for (const { id } of related) {
            await setupMenu.update(id, { menu_enable: updated[menu] });
          }
        }
      }
    beforeExitConfirm.clear();
    await nextTick();
    await alert('메뉴가 수정 됐습니다. 재로그인 부탁드립니다.', '통제관리');
    auth.logOut();
    router.push({
      path: '/login-form',
      query: { redirect: route.path },
    });
    }
    
  }else{
    formState.value = false;
  }
}
function initialized (component) {
  grid = component
}
function setCellValue(newData, value, currentRowData){
  const getVisibleRows = grid.getVisibleRows();
  const findData = getVisibleRows.find((v) => v.data.menu_name == currentRowData.menu_name);
  if(findData.oldData?.menu_enable != value){
      updated[currentRowData.menu_name] = value;
  }else{
      delete updated[currentRowData.menu_name];
  }
  formState.value = Object.keys(updated).length > 0 ? true : false;
  newData.menu_enable = value;
}
</script>

<template>
  <div>
    <dx-data-grid
       height="200"
      :data-source="setupMenu"
      :column-auto-width="true"
      :allow-column-reordering="true"
      :show-borders="true"
      :show-row-lines="true"
      @initialized="(evt) => initialized(evt.component)">
      <dx-paging :enabled="true" :page-size="1000" />
      <dx-toolbar>
        <dx-item template="saveButton" location="before" />
        <dx-item name="revertButton" location="before" />
      </dx-toolbar>
      <template #saveButton>
        <dx-button text="저장" icon="save" @click="saveButton" />
      </template>
      <dx-column
        data-field="menu_name"
        caption="메뉴"
        :allow-editing="false"
      />
      <dx-column
        data-field="menu_enable"
        data-type="boolean"
        caption="사용유무"
        :allow-editing="true"
        :set-cell-value="setCellValue"
      >
      <dx-lookup value-expr="value" display-expr="name" :data-source="displayExpr" />
      </dx-column>
      <dx-editing
        mode="batch"
        :allow-adding="false"
        :allow-updating="true"
        :allow-deleting="false"
        :use-icons="true"
      />
    </dx-data-grid>

  </div>
</template>

<style lang="scss" scoped>
</style>