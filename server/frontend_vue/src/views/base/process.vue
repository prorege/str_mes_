<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings">
        <div class="content-header">
          <dx-toolbar>
            <dx-item location="before"
              ><div class="content-title">공정관리</div></dx-item
            >
          </dx-toolbar>
        </div>
        <dx-data-grid
          id="process" height="calc(100vh - 150px)"
          :data-source="baseProcess"
          :root-value="-1"
          :key="processKey"
          :show-borders="true"
          :show-row-lines="true"
          :column-auto-width="true"
          :remote-operations="true"
          :expanded-row-keys="expandedRowKeys"
          :focused-row-enabled="true"
          v-model:selected-row-keys="selectedRowKeys"
          @init-new-row="onRowAdded"
          @row-updated="onRowUpdated"
          @toolbar-preparing="onToolbarPreparing"
        >
          <dx-filter-row :visible="true" />
          <dx-header-filter :visible="false" />
          <dx-search-panel :visible="false" :width="240" placeholder="검색" />
          <dx-editing
            mode="row"
            :allow-adding="true"
            :allow-updating="true"
            :allow-deleting="true"
            :use-icons="true"
          />
          <dx-paging :page-size="20"/>
          <!--dx-column
            data-field="id"
            sort-order="desc"
            :allow-editing="false"
            :width="80"
          /-->
          <dx-column
            data-field="process_code"
            caption="공정 코드"
            :allow-sorting="false">
            <dx-required-rule message="창고 코드를 입력하세요"/>
          </dx-column>
          <dx-column
            data-field="process_name"
            caption="공정명"
            :allow-sorting="false"
            ><dx-required-rule message="창고명을 입력하세요"
          /></dx-column>
          <dx-column data-field="ct" caption="C/T" :allow-sorting="false" />
          <dx-column data-field="unit" caption="단위" :allow-sorting="false">
            <dx-lookup
              :data-source="unitFormat"
              value-expr="code_name"
              display-expr="code_name"
            />
          </dx-column>
          <dx-column
            data-field="unit_price"
            caption="단가"
            :format="{ type: 'fixedPoint', precision: 2 }"
            :allow-sorting="false"
          />
          <dx-column data-field="etc" caption="비고" :allow-sorting="false" />
        </dx-data-grid>
      </div>
    </div>
  </div>
</template>

<script>
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import {
  DxDataGrid,
  DxColumn,
  DxEditing,
  DxPaging,
  DxRequiredRule,
  DxSearchPanel,
  DxHeaderFilter,
  DxFilterRow,
  DxLookup,
} from 'devextreme-vue/data-grid';
import { ref, reactive, onMounted } from 'vue';
import { baseProcess, baseCode } from '../../data-source/base';
import authService from '../../auth'

export default {
  components: {
    DxDataGrid,
    DxColumn,
    DxEditing,
    DxPaging,
    DxToolbar,
    DxItem,
    DxRequiredRule,
    DxSearchPanel,
    DxHeaderFilter,
    DxFilterRow,
    DxLookup,
  },
  setup() {
    const processKey = ref(0);
    const expandedRowKeys = reactive([1]);
    const selectedRowKeys = reactive([]);
    const unitFormat = reactive([]);

    onMounted(() => {
      baseCode
        .load({ filter: ['code_name', '=', '단위'] })
        .then(data => {
          if (data.totalCount > 0) {
            const parentId = data.data[0].id;
            baseCode
              .load({
                filter: ['parent_code_id', '=', parentId],
                sort: [{ selector: 'code_order' }],
              })
              .then(data => {
                unitFormat.length = 0;
                data.data.forEach(item => {
                  unitFormat.push(item);
                });
                refreshDataGrid();
              });
          }
        });
    });

    const onRowAdded = e => {
      e.data.fk_company_id = authService.getCompanyId()
    }

    const onRowUpdated = e => {
      console.log(e);
    };

    const refreshDataGrid = () => {
      processKey.value += 1;
    };

    const onToolbarPreparing = e => {
      let toolbarItems = e.toolbarOptions.items;
      toolbarItems.forEach(function(item) {
        if (item.name === 'addRowButton') {
          item.options.text = '신규';
          item.options.hint = '신규';
        }
      });
    };

    return {
      processKey,
      baseProcess,
      expandedRowKeys,
      selectedRowKeys,
      unitFormat,
      onRowAdded,
      onRowUpdated,
      onToolbarPreparing,
    };
  },
};
</script>

<style></style>
