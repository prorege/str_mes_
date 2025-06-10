<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings">
        <div class="content-header">
          <dx-toolbar>
            <dx-item location="before"
              ><div class="content-title">메뉴관리</div></dx-item
            >
          </dx-toolbar>
        </div>
        <dx-tree-list
          id="menus"
          key-expr="id"
          parent-id-expr="parent_id"
          :key="menuTreeKey"
          :data-source="menus"
          :root-value="-1"
          :show-borders="true"
          :show-row-lines="true"
          :column-auto-width="true"
          :expanded-row-keys="expandedRowKeys"
          v-model:selected-row-keys="selectedRowKeys"
          @selection-changed="onSelectionChanged"
          @row-inserting="onRowInserting"
          @row-updated="onRowUpdated"
          @content-ready="selectFirstRow"
        >
          <dx-row-dragging
            :on-drag-change="onDragChange"
            :on-reorder="onReorder"
            :allow-drop-inside-item="allowDropInsideItem"
            :allow-reordering="allowReordering"
            :show-drag-icons="showDragIcons"
          />
          <dx-editing
            :allow-updating="true"
            :allow-deleting="false"
            mode="cell"
          />
          <dx-paging :enabled="true" :page-size="1000" />
          <dx-selection :recursive="false" mode="multiple" />
          <dx-column
            data-field="menu_name"
            caption="메뉴"
            :allow-sorting="false"
          />
        </dx-tree-list>
      </div>
    </div>
  </div>
</template>
<script>
import {
  DxTreeList,
  DxColumn,
  DxRowDragging,
  DxSelection,
  DxEditing,
  DxPaging,
} from 'devextreme-vue/tree-list';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';

import { ref, reactive, onMounted } from 'vue';
import ApiService from '../../utils/api-service';

export default {
  components: {
    DxTreeList,
    DxColumn,
    DxRowDragging,
    DxSelection,
    DxEditing,
    DxPaging,
    DxToolbar,
    DxItem,
  },
  setup() {
    const allowDropInsideItem = ref(false);
    const allowReordering = ref(true);
    const showDragIcons = ref(true);
    const expandedRowKeys = reactive([]);
    const selectedRowKeys = reactive([]);
    const selectionMode = ref('all');
    const menuTreeKey = ref(0);
    const menus = reactive([]);

    onMounted(() => {
      getMenu();
    });

    const getMenu = async () => {
      let { data, status, statusText } = await apiGetMenuData();
      if (isApiSuccess(status, statusText)) {
        setMenuData(data);
      }
    };

    const apiGetMenuData = async () => {
      const apiService = new ApiService('/api/mes/v1/setup/');
      return await apiService.get(
        `menu?q={"order_by":[{"field":"parent_id","direction":"asc"},{"field":"menu_order","direction":"asc"}]}`
      );
    };

    const isApiSuccess = (status, statusText) => {
      if (status === 200 && statusText === 'OK') {
        return true;
      }
      return false;
    };

    const setMenuData = data => {
      setExpandedRowKeys(data.objects);

      menus.push(...data.objects);
      menuTreeKey.value += 1; // force refresh
    };

    const setExpandedRowKeys = items => {
      items.forEach(function(item) {
        if (item['parent_id'] == null) {
          expandedRowKeys.push(item['id']);
        }
      });
    };

    const onDragChange = e => {
      let visibleRows = e.component.getVisibleRows(),
        sourceNode = e.component.getNodeByKey(e.itemData.id),
        targetNode = visibleRows[e.toIndex].node;

      while (targetNode && targetNode.data) {
        if (targetNode.data.id === sourceNode.data.id) {
          e.cancel = true;
          break;
        }
        targetNode = targetNode.parent;
      }
    };

    const onReorder = e => {
      const visibleRows = e.component.getVisibleRows();
      if (e.dropInsideItem) {
        if (e.itemData.parentId == -1) {
          return;
        }
        console.log(visibleRows[e.toIndex]);
        if (!visibleRows[e.toIndex].data.isDirectory) {
          return;
        }
        e.itemData.parentId = visibleRows[e.toIndex].key;
      } else {
        const sourceData = e.itemData;
        const toIndex = e.fromIndex > e.toIndex ? e.toIndex - 1 : e.toIndex;
        let targetData = toIndex >= 0 ? visibleRows[toIndex].node.data : null;

        if (targetData && e.component.isRowExpanded(targetData.id)) {
          if (sourceData.parent_id == -1 && targetData.id != -1) {
            return;
          }
          sourceData.parent_id = targetData.id;
          targetData = null;
        } else {
          const parentId = targetData ? targetData.parent_id : -1;
          if (sourceData.parent_id == -1 && parentId != -1) {
            return;
          }
          if (sourceData.parent_id != -1 && parentId == -1) {
            return;
          }
          sourceData.parent_id = parentId;
        }

        const sourceIndex = menus.indexOf(sourceData);
        menus.splice(sourceIndex, 1);

        const targetIndex = menus.indexOf(targetData) + 1;
        menus.splice(targetIndex, 0, sourceData);
      }
      e.component.refresh();

      syncOrder();
      updateMenus();
    };

    const syncOrder = () => {
      let parentOrder = 1;
      let childOrder = {};
      menus.map(item => {
        if (item.parent_id == -1) {
          item.menu_order = parentOrder;
          parentOrder += 1;
          childOrder[item.id] = 1;
        }
      });

      menus.map(item => {
        if (item.parent_id != -1) {
          item.menu_order = childOrder[item.parent_id];
          childOrder[item.parent_id] += 1;
        }
      });
    };

    const updateMenus = async () => {
      menus.forEach(menu => {
        return apiUpdateMenu(menu);
      });
    };

    const apiUpdateMenu = async menu => {
      const apiService = new ApiService('/api/mes/v1/setup/');
      return await apiService.patch(`menu/${menu.id}`, menu);
    };

    const onSelectionChanged = ({ component }) => {
      const selectedData = component.getSelectedRowsData(selectionMode);
      menus.forEach(menu => {
        const save_enable = menu.menu_enable;
        menu.menu_enable = false;
        if (selectedData.includes(menu)) {
          menu.menu_enable = true;
        }
        if (save_enable != menu.menu_enable) {
          apiUpdateMenu(menu);
        }
      });
    };

    const onRowInserting = e => {
      const find = menus.reduce((previous, current) => {
        return previous.id > current.id ? previous : current;
      });

      e.data.id = find.id + 1;
      e.data.parent_id = -1;
      e.data.menu_depth = 1;
      e.data.menu_enable = false;
      e.data.menu_format = 1;
      e.data.menu_middle_letter = '-';
      e.data.menu_last_digit = 3;
      console.log(e.data);
    };

    const onRowUpdated = e => {
      const updatedMenu = menus.filter(menu => {
        return menu.id == e.data.id;
      });
      if (updatedMenu.length > 0) {
        apiUpdateMenu(updatedMenu[0]);
      }
    };

    const allowAdding = () => {
      return '';
    };

    const selectFirstRow = e => {
      selectedRowKeys.length = 0;
      e.component.forEachNode(node => {
        if (node.data.menu_enable) {
          selectedRowKeys.push(node.data.id);
        }
      });
    };

    return {
      menuTreeKey,
      menus,
      allowDropInsideItem,
      allowReordering,
      showDragIcons,
      expandedRowKeys,
      selectedRowKeys,
      selectionMode,
      onDragChange,
      onReorder,
      onSelectionChanged,
      onRowInserting,
      onRowUpdated,
      allowAdding,
      selectFirstRow,
    };
  },
};
</script>

<style>
.dx-sortable-dragging {
  opacity: 0.9;
}

.options {
  margin-top: 20px;
  padding: 20px;
  background-color: rgba(191, 191, 191, 0.15);
  position: relative;
}

.caption {
  font-size: 18px;
  font-weight: 500;
}

.option {
  margin-top: 10px;
  margin-right: 44px;
  display: inline-block;
}

.option:last-child {
  margin-right: 0;
}
</style>
