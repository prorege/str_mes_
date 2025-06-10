<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings">
        <div class="content-header">
          <dx-toolbar>
            <dx-item location="before"
              ><div class="content-title">권한그룹관리</div></dx-item
            >
          </dx-toolbar>
        </div>
        <dx-data-grid
          :data-source="setupGroup"
          :column-auto-width="true"
          :allow-column-reordering="true"
          :show-borders="true"
          :show-row-lines="true"
          @saving="saveSetupGroupHandler"
        >
          <dx-filter-row :visible="true" />
          <dx-header-filter :visible="false" />
          <dx-search-panel :visible="false" :width="240" placeholder="검색" />
          <dx-paging :enabled="true" :page-size="1000" />
          <dx-column
            data-field="group_name"
            caption="권한그룹명"
            :allow-editing="true"
          >
            <dx-required-rule message="권한그룹명을 입력하세요" />
          </dx-column>
          <dx-column
            data-field="group_detail"
            caption="설명"
            :allow-editing="true"
            :allow-filtering="false"
          />
          <dx-column type="buttons">
            <dx-button
              hint="상세설정"
              icon="more"
              :visible="isDetailIconVisible"
              @click="detailIconClick"
            />
            <dx-button name="delete" />
          </dx-column>
          <dx-editing
            mode="batch"
            :allow-adding="enable_add"
            :allow-updating="enable_update"
            :allow-deleting="enable_delete"
            :use-icons="true"
          />
        </dx-data-grid>
        <dx-popup
          title="메뉴권한관리"
          :key="detailPopupKey"
          :width="850"
          :height="550"
          :visible="isDetailPopupVisible"
          :close-on-outside-click="true"
          :resize-enabled="true"
        >
          <template #content>
            <dx-tree-list
              key-expr="menu.id"
              parent-id-expr="menu.parent_id"
              :root-value="-1"
              :data-source="dataSetupGroupAuth"
              :show-borders="true"
              :show-row-lines="true"
              :column-auto-width="true"
              :allow-column-reordering="true"
              @saved="onSetupGroupAuthSaved"
            >
              <dx-header-filter :visible="false" />
              <dx-filter-row :visible="false" />
              <dx-search-panel
                :visible="false"
                :width="240"
                placeholder="검색"
              />
              <dx-paging :enabled="true" :page-size="1000" />
              <dx-column
                data-field="menu.menu_name"
                caption="메뉴명"
                :allow-editing="false"
              />
              <dx-column
                data-field="auth_show"
                caption="보기"
                data-type="boolean"
              />
              <dx-column
                data-field="auth_add"
                caption="신규"
                data-type="boolean"
              />
              <dx-column
                data-field="auth_update"
                caption="수정"
                data-type="boolean"
              />
              <dx-column
                data-field="auth_delete"
                caption="삭제"
                data-type="boolean"
              />
              <dx-column
                data-field="auth_print"
                caption="인쇄"
                data-type="boolean"
              />
              <dx-column
                data-field="auth_excel"
                caption="엑셀"
                data-type="boolean"
              />
              <dx-editing
                mode="batch"
                :allow-updating="isEditableAuth"
                :allow-adding="false"
                :allow-deleting="false"
                :use-icons="true"
              />
            </dx-tree-list>
          </template>
        </dx-popup>
      </div>
    </div>
  </div>
</template>

<script>
import {
  DxDataGrid,
  DxColumn,
  DxSearchPanel,
  DxFilterRow,
  DxHeaderFilter,
  DxEditing,
  DxRequiredRule,
  DxButton,
} from 'devextreme-vue/data-grid';
import { DxTreeList, DxPaging } from 'devextreme-vue/tree-list';
import { DxPopup } from 'devextreme-vue/popup';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';

import { ref, reactive } from 'vue';
import { setupGroup, setupGroupAuth } from '../../data-source/setup';
import authService from '@/auth'

export default {
  components: {
    DxPopup,
    DxDataGrid,
    DxColumn,
    DxSearchPanel,
    DxFilterRow,
    DxHeaderFilter,
    DxEditing,
    DxRequiredRule,
    DxButton,
    DxToolbar,
    DxItem,
    DxTreeList,
    DxPaging,
  },
  setup() {
    const detailPopupKey = ref(0);
    const enable_add = ref(true);
    const enable_update = ref(true);
    const enable_delete = ref(true);
    const isDetailPopupVisible = ref(false);
    const dataSetupGroupAuth = reactive([]);
    const auth = reactive({
      add: 1,
      update: 2,
      delete: 4,
      print: 8,
      excel: 16
    });
    setupGroup.defaultFilters = [{name: 'fk_company_id', op: 'eq', val: authService.getCompanyId()}]

    const refreshDetailPopup = () => {
      detailPopupKey.value += 1;
    };

    const detailIconClick = e => {
      loadSetupGroup(e.row.key);
    };

    const showDetailPopup = () => {
      isDetailPopupVisible.value = true;
    };

    const loadSetupGroup = group_id => {
      setupGroupAuth
        .load({ filter: ['fk_group_id', '=', group_id] })
        .then(data => {
          if (data.totalCount > 0) {
            emptyDataSetupGroupAuth();
            data.data.forEach(item => {
              const insertItem = createSetupGroupAuthObject(item);
              pushDataSetupGroupAuth(insertItem);
            });
            refreshDetailPopup();
            showDetailPopup();
          }
        });
    };

    const emptyDataSetupGroupAuth = () => {
      dataSetupGroupAuth.length = 0;
    };

    const pushDataSetupGroupAuth = item => {
      dataSetupGroupAuth.push(item);
    };

    const createSetupGroupAuthObject = item => {
      const createItem = {
        menu: item.menu,
        group: item.group,
        id: item.id,
        fk_group_id: item.fk_group_id,
        fk_menu_id: item.fk_menu_id,
        auth_show: item.menu_yn,
        auth_add: item.menu_auth & auth.add ? true : false,
        auth_update: item.menu_auth & auth.update ? true : false,
        auth_delete: item.menu_auth & auth.delete ? true : false,
        auth_print: item.menu_auth & auth.print ? true : false,
        auth_excel: item.menu_auth & auth.excel ? true : false,
      };
      return createItem;
    };

    const isDetailIconVisible = e => {
      return !e.row.isEditing && !e.row.isNewRow;
    };

    const isEditableAuth = e => {
      if (e.row.data.menu.parent_id == null) {
        return false;
      }
      return true;
    };

    const onSetupGroupAuthSaved = e => {
      const changes = e.changes;
      changes.forEach(item => {
        const updateGroupAuth = getDataSetupGroupAuth(item.key);
        if (updateGroupAuth) {
          updateAuthValue(updateGroupAuth);
          updateSetupGroupAuth(updateGroupAuth);
        }
      });
    };

    const getDataSetupGroupAuth = menu_id => {
      for (let i = 0; i < dataSetupGroupAuth.length; i++) {
        if (dataSetupGroupAuth[i].fk_menu_id == menu_id) {
          return dataSetupGroupAuth[i];
        }
      }
    };

    const updateAuthValue = setupGroupAuth => {
      setupGroupAuth.menu_yn = setupGroupAuth.auth_show
      setupGroupAuth.menu_auth = calculateAuthValue(setupGroupAuth);
    };

    const calculateAuthValue = setupGroupAuth => {
      let auth_value = 0;
      auth_value += setupGroupAuth.auth_add ? auth.add : 0;
      auth_value += setupGroupAuth.auth_update ? auth.update : 0;
      auth_value += setupGroupAuth.auth_delete ? auth.delete : 0;
      auth_value += setupGroupAuth.auth_print ? auth.print : 0;
      auth_value += setupGroupAuth.auth_excel ? auth.excel : 0;
      return auth_value;
    };

    const updateSetupGroupAuth = updateItem => {
      setupGroupAuth.update(updateItem.id, {
        menu_yn: updateItem.menu_yn,
        menu_auth: updateItem.menu_auth,
      }).catch(e => {
        isDetailPopupVisible.value = false;
      });
    };

    const saveSetupGroupHandler = (evt) => {
      const companyId = authService.getCompanyId()
      for (let item of evt.changes) {
        if (item.type !== 'insert') continue
        item.data.fk_company_id = companyId
      }
    }

    return {
      detailPopupKey,
      setupGroup,
      setupGroupAuth,
      dataSetupGroupAuth,
      enable_add,
      enable_update,
      enable_delete,
      isDetailPopupVisible,
      detailIconClick,
      isDetailIconVisible,
      isEditableAuth,
      onSetupGroupAuthSaved,
      saveSetupGroupHandler
    };
  },
};
</script>

<style></style>
