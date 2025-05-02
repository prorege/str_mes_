<template>
  <dx-tree-list
    key-expr="id"
    parent-id-expr="parent_id"
    column-resizing-mode="widget"
    :root-value="-1"
    :data-source="setupMenu"
    :show-borders="true"
    :show-row-lines="true"
    :column-auto-width="true"
    :allow-column-reordering="true"
    @toolbar-preparing="onToolbarPreparing"
  >
    <dx-header-filter :visible="false" />
    <dx-filter-row :visible="false" />
    <dx-search-panel :visible="false" :width="240" placeholder="검색" />
    <dx-paging :enabled="true" :page-size="1000" />
    <dx-column data-field="menu_name" caption="메뉴명" :allow-editing="false" />
    <dx-column data-field="menu_initial" caption="채번이니셜" />
    <dx-column data-field="menu_format" caption="연월일표기"
      ><dx-lookup
        :data-source="numberingDateFormat"
        value-expr="id"
        display-expr="name"
    /></dx-column>
    <dx-column data-field="menu_middle_letter" caption="중간자" />
    <dx-column data-field="menu_last_digit" caption="뒷자리수">
      <dx-lookup
        :data-source="numberingPostDigit"
        value-expr="id"
        display-expr="name"
      />
    </dx-column>
    <dx-column data-field="etc" caption="비고" />
    <dx-editing
      mode="batch"
      :allow-updating="true"
      :allow-adding="false"
      :allow-deleting="false"
      :use-icons="true"
    />
  </dx-tree-list>
</template>

<script>
import {
  DxTreeList,
  DxColumn,
  DxSearchPanel,
  DxFilterRow,
  DxHeaderFilter,
  DxEditing,
  DxLookup,
  DxPaging,
} from 'devextreme-vue/tree-list';
import { reactive } from 'vue';
import { setupMenu } from '../../data-source/setup';

export default {
  components: {
    DxTreeList,
    DxColumn,
    DxSearchPanel,
    DxFilterRow,
    DxHeaderFilter,
    DxEditing,
    DxLookup,
    DxPaging,
  },
  setup() {
    setupMenu.defaultFilters = [{name: 'menu_initial_enable', op: 'eq', val: true }]
    const numberingDateFormat = reactive([
      {
        id: 1,
        name: 'YYYYMMDD',
      },
      {
        id: 2,
        name: 'YYYYMM',
      },
      {
        id:3,
        name: 'YYYY',
      }
    ]);
    const numberingPostDigit = reactive([
      {
        id: 2,
        name: '2',
      },
      {
        id: 3,
        name: '3',
      },
      {
        id: 4,
        name: '4',
      },
    ]);

    const onToolbarPreparing = e => {
      let toolbarItems = e.toolbarOptions.items;
      toolbarItems.forEach(function(item) {
        if (item.name === 'searchPanel') {
          item.location = 'before';
        }
      });
    };

    const generateItemButtonOption = (
      icon,
      callback,
      location = 'after',
      options = {}
    ) => {
      let buttonOptions = { stylingMode: 'text', icon, onClick: callback };
      return {
        ...options,
        buttons: [{ name: icon, location, options: buttonOptions }],
      };
    };

    

    return {
      setupMenu,
      numberingPostDigit,
      numberingDateFormat,
      onToolbarPreparing,
      generateItemButtonOption,
    };
  },
};
</script>

<style></style>
