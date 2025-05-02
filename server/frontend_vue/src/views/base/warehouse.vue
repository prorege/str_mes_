<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings">
        <div class="content-header">
          <dx-toolbar>
            <dx-item location="before">
              <div class="content-title">창고관리</div>
            </dx-item>
          </dx-toolbar>
        </div>
        <dx-data-grid
          id="warehouse"
          v-model:selected-row-keys="selectedRowKeys"
          :data-source="baseWarehouse"
          :selection="{ mode: 'single' }"
          :show-borders="true"
          :show-row-lines="true"
          :column-auto-width="true"
          :remote-operations="true"
          :hover-state-enabled="true"
          :focused-row-enabled="true"
          :expanded-row-keys="expandedRowKeys"
          :on-initialized="evt => methods.onInitialized(evt, 'warehouse')"
          @row-inserting="methods.onRowInserting"
          @row-removing="methods.onRowRemoving"
        >
          <dx-column caption="창고 코드" data-field="wh_code" :allow-sorting="false">
            <dx-required-rule message="창고 코드를 입력하세요" />
          </dx-column>
          <dx-column caption="창고명" data-field="wh_name" :allow-sorting="false">
            <dx-required-rule message="창고명을 입력하세요" />
          </dx-column>
          <dx-column caption="설명" data-field="wh_detail" :allow-sorting="false" />
          <dx-column caption="원가마감 적용" data-field="use_cost_closing" data-type="boolean" :allow-sorting="false" />
          <dx-column caption="순서" data-field="wh_order" sort-order="asc" :visible="false" />
          <dx-column type="buttons">
            <dx-button name="edit" />
            <dx-button name="delete" />
          </dx-column>

          <dx-row-dragging
            :on-reorder="methods.onReorder"
            :show-drag-icons="true"
            :allow-reordering="true"
            :allow-drop-inside-item="false"
          />
          <dx-editing mode="row"
            :use-icons="true"
            :allow-adding="true"
            :allow-updating="true"
            :allow-deleting="true"
          />
          <dx-paging :enabled="true" :page-size="1000" />
        </dx-data-grid>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, onMounted } from 'vue';

import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxDataGrid, DxColumn, DxPaging, DxButton, DxEditing, DxRowDragging, DxRequiredRule } from 'devextreme-vue/data-grid';

import authService from '../../auth';
import { baseWarehouse } from '../../data-source/base';

export default {
  components: {
    DxToolbar, DxItem,
    DxDataGrid, DxColumn, DxPaging, DxButton, DxEditing, DxRowDragging, DxRequiredRule,
  },
  setup() {
    const vars = {};
    const expandedRowKeys = reactive([1]);
    const selectedRowKeys = reactive([]);
    vars.tree = {
      warehouse: null,
    };

    onMounted(() => {});

    var methods = {
      onInitialized(evt, key) {
        vars.tree[key] = evt.component;
      },
      onRowInserting(e) {
        e.data['wh_order'] = e.component.totalCount() + 1;
        e.data['fk_company_id'] = authService.getCompanyId();
      },
      onRowRemoving(e) {
        const visibleRows = e.component.getVisibleRows();
        visibleRows.forEach(function(item) {
          if (item.data['wh_order'] > e.data['wh_order']) {
            methods.requestUpdateOrder(
              item.data['id'],
              item.data['wh_order'] - 1
            );
          }
        });
      },
      onReorder(e) {
        const visibleRows = e.component.getVisibleRows();

        let isNewRow = false;
        visibleRows.forEach(function(item) {
          if (item.isNewRow == true) {
            isNewRow = true;
          }
        });
        if (isNewRow == true) return;

        if (e.toIndex > e.fromIndex) {
          for (let i = e.fromIndex + 1; i <= e.toIndex; i++) {
            const itemData = visibleRows[i]['data'];
            methods.requestUpdateOrder(
              itemData['id'],
              itemData['wh_order'] - 1
            );
          }
        } else {
          for (let i = e.toIndex; i < e.fromIndex; i++) {
            const itemData = visibleRows[i]['data'];
            methods.requestUpdateOrder(
              itemData['id'],
              itemData['wh_order'] + 1
            );
          }
        }

        methods.requestUpdateOrder(e.itemData['id'], e.toIndex + 1);
      },
      requestUpdateOrder(id, order) {
        baseWarehouse.update(id, { wh_order: order }).then(() => {
          vars.tree.warehouse.refresh();
        });
      },
    };

    return {
      vars,
      methods,
      baseWarehouse,
      expandedRowKeys,
      selectedRowKeys,
    };
  },
};
</script>

<style></style>
