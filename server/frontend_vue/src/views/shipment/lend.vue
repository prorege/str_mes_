<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">가출고</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div>
          <div class="search-status">
            <span class="search-title">가출고일자</span>
            <dx-date-box v-model:value="vars.formData.startDate" />

            <span class="search-bar">~</span>
            <dx-date-box v-model:value="vars.formData.endDate" />

            <span class="search-tab"></span>
            <dx-button text="검색" icon="search" @click="methods.searchDateRange()" />
          </div>
        </div>

      </div>

      <div class="dx-card responsive-paddings mt-1">
        <dx-data-grid
          height="calc(100vh - 230px)"
          date-serialization-format="yyyy-MM-ddTHH:mm:ss"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :focused-row-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :data-source="shipmentLend"
          :on-initialized="evt => methods.onGridInitialized(evt, 'status')"
          @saving="methods.onSavingItem"
          @data-error-occurred="methods.onDataError"
          @cell-hover-changed="methods.onCellHoverChanged"
        >
          <dx-grid-toolbar>
            <dx-grid-item name="addRowButton" :options="{ onClick: methods.showAddPopup }" />
            <dx-grid-item template="edit" location="after" />
            <dx-grid-item name="saveButton" />
            <dx-grid-item name="revertButton" />
            <dx-grid-item name="columnChooserButton" />
          </dx-grid-toolbar>
          <template #edit>
            <dx-button icon="edit" @click="methods.toggleEdit" />
          </template>

          <dx-column caption="가출고번호" data-field="lend_number" :allow-editing="false" :filter-operations="['contains', '=']" />
          <dx-column caption="가출고일자" data-field="lend_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
          <dx-column caption="가출고담당자" data-field="lend_manager" />
          <dx-column caption="관련업체" data-field="client_company" :filter-value="vars.filter.client"
            :editor-options="{ ...generateItemButtonOption('search', methods.createFindPopupFn('client', '업체조회')), }"
          />
          <dx-column caption="품목코드" data-field="item_code" :allow-editing="false" />
          <dx-column caption="품명" data-field="item.item_name" :allow-editing="false" />
          <dx-column caption="규격" data-field="item.item_standard" :allow-editing="false" />
          <dx-column caption="가출고수량" data-field="quantity" data-type="number" format="fixedPoint" :set-cell-value="methods.setQuantity" />
          <dx-column caption="미회수수량" data-field="not_retrieved_quantity" data-type="number" format="fixedPoint" :allow-editing="false" />
          <dx-column caption="참고사항" data-field="note" />
          <dx-column caption="비고" data-field="etc" />

          <dx-sorting mode="single" />
          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-column-chooser mode="select" :enabled="true" />
          <dx-editing mode="batch"
            :use-icons="true"
            :allow-adding="true"
            :allow-updating="!vars.disabled.edit"
            :allow-deleting="true"
          />
        </dx-data-grid>
      </div>
    </div>

    <dx-popup
      title="품목찾기"  
      content-template="popup-content"
      v-model:visible="vars.dlg.addItem.show"
      :width="680"
      :height="460"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'item-popup')"
    >
      <dx-toolbar-item widget="dxButton" toolbar="top" location="after"
        :options="{ icon: 'add', text: '선택된 항목 추가', onClick: methods.addSelectedRows }"
      />

      <template #popup-content>
        <dx-data-grid
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="baseItem"
          :on-initialized="evt => methods.onGridInitialized(evt, 'baseItem')"
        >
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item_name" />
          <dx-column caption="규격" data-field="item_standard" />
          <dx-column caption="자산구분" data-field="asset_type" />
          <dx-column caption="대분류" data-field="main_category" />
          <dx-column caption="중분류" data-field="middle_category" />
          <dx-column caption="소분류" data-field="sub_category" />

          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-selection mode="multiple" select-all-mode="page" show-check-boxes-mode="onClick" />
        </dx-data-grid>
      </template>
    </dx-popup>

    <dx-popup
      content-template="popup-content"  
      v-model:visible="vars.dlg.finder.show"
      :width="680"
      :height="500"
      :key="vars.dlg.finder.key"
      :title="vars.dlg.finder.title"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'find-popup')"
    >
      <template #popup-content>
        <data-grid-client v-if="vars.dlg.finder.key === 'client'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
        <div v-else-if="vars.dlg.finder.key === 'etc'">
          <div class="mb-2">
            <dx-text-area :height="440" :value="vars.dlg.finder.data" @update:value="methods.updateEtcValue" />
          </div>
          <dx-toolbar>
            <dx-item widget="dxButton" toolbar="top" location="after"
              :options="{ icon: null, text: '닫기', onClick: methods.finderReturnHandler }"
            />
          </dx-toolbar>
        </div>
      </template>
    </dx-popup>
  </div>
</template>

<script>
import moment from 'moment';

import { reactive } from 'vue';
import { useRouter } from 'vue-router';

import DxButton from 'devextreme-vue/button';
import DxCheckBox from 'devextreme-vue/check-box';
import DxTextArea from 'devextreme-vue/text-area';
import { DxDateBox } from 'devextreme-vue/date-box';
import { confirm, alert } from 'devextreme/ui/dialog';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxEditing, DxSorting, DxSelection, DxFilterRow, 
         DxColumnChooser, DxToolbar as DxGridToolbar, DxItem as DxGridItem } from 'devextreme-vue/data-grid';

import { baseItem } from '../../data-source/base';
import { shipmentLend } from '../../data-source/shipment';

import DataGridClient from '../../components/base/data-client.vue';

import authService from '../../auth';
import stateStore from '@/utils/state-store';
import { generateItemButtonOption } from '../../utils/util';

export default {
  components: {
    DxButton,
    DxCheckBox,
    DxTextArea,
    DxDateBox,
    DxToolbar, DxItem,
    DxPopup, DxToolbarItem,
    DxForm, DxLabel,  DxGroupItem, DxSimpleItem,
    DxDataGrid, DxColumn, DxPaging, DxEditing, DxSorting, DxSelection, DxFilterRow, DxColumnChooser, DxGridToolbar, DxGridItem,
    DataGridClient,
  },
  setup() {
    const router = useRouter();
    const vars = {};
    vars.grid = {};
    vars.dlg = {};
    vars.dlg.finder = reactive({
      show: false,
      title: '',
      key: null,
      data: null,
    });
    vars.dlg.addItem = reactive({ show: false });
    vars.focus = {
      status: null,
    };
    vars.filter = reactive({
      client: null,
    });
    vars.formData = reactive({
      startDate: new Date(),
      endDate: new Date(),
    });
    vars.formData.startDate.setDate(vars.formData.startDate.getDate() - 7);
    vars.disabled = reactive({
      edit: true
    })

    const methods = {
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`shipment-lend-${key}`, evt.component);

        methods.initSorting();
        methods.searchDateRange();
      },
      initSorting() {
        const columns = vars.grid['status'].getVisibleColumns();
        const col = columns.filter(item => item.sortOrder);
        if (col.length == 0) {
          const defaultName = 'lend_date';
          const defaultSort = columns.filter(item => item.name == defaultName);
          if (defaultSort.length > 0) {
            vars.grid['status'].columnOption(defaultSort[0].index, 'sortOrder', 'desc');
          }
        }
      },
      async toggleEdit() {
        if (vars.disabled.edit) {
          let isSelect = await confirm('수정하시겠습니까?', '수정');
          if (!isSelect) { return; }
        }
        vars.disabled.edit = !vars.disabled.edit;
      },
      setQuantity(newData, value, currentRowData) {
        newData.quantity = value;
        newData.not_retrieved_quantity = currentRowData.not_retrieved_quantity + (value - currentRowData.quantity);
      },
      createFindPopupFn(key, title, data = null) {
        const _key = key;
        const _title = title;
        const _data = data;
        return () => {
          vars.dlg.finder.key = _key;
          vars.dlg.finder.data = _data;
          vars.dlg.finder.title = _title;
          vars.dlg.finder.show = true;
        };
      },
      finderReturnHandler(data) {
        switch (vars.dlg.finder.key) {
          case 'client': {
            if (vars.focus.status.rowType == 'data') {
              vars.focus.status.component.cellValue(
                vars.focus.status.rowIndex,
                vars.focus.status.columnIndex,
                data.name
              );
            } else if (vars.focus.status.rowType == 'filter') {
              vars.filter.client = data.name;
            }
            break;
          }
          case 'etc': {
            vars.formData.etc = vars.dlg.finder.data;
            break;
          }
        }

        vars.dlg.finder.show = false;
        vars.dlg.finder.title = '';
        vars.dlg.finder.key = null;
        vars.dlg.finder.data = null;
      },
      showAddPopup() {
        if (vars.grid.baseItem) {
          vars.grid.baseItem.clearSelection();
          vars.grid.baseItem.clearFilter();
          vars.grid.baseItem.refresh();
        }
        vars.dlg.addItem.show = true;
      },
      async addSelectedRows() {
        const grid = vars.grid.status;
        await grid.pageIndex(0);
        const firstRowKey = grid.getKeyByRowIndex(0);
        if (firstRowKey) {
          await grid.navigateToRow(firstRowKey);
        }

        const rows = await vars.grid.baseItem.getSelectedRowsData();
        for (let row of rows) {
          await grid.addRow();
          const data = await grid.byKey(grid.getKeyByRowIndex(0));
          data.lend_number = '(자동생성)'; // 가출고번호
          data.lend_date = new Date(); // 가출고일자
          data.lend_manager = authService.getUserName();
          data.client_company = '';
          data.item_code = row.item_code; // 품목코드
          data.item = { ...row }; // 품목
          data.quantity = 0; // 가출고수량
          data.not_retrieved_quantity = 0; // 미회수수량
          data.note = ''; // 참고사항
          data.etc = ''; // 비고
          data.fk_company_id = authService.getCompanyId();
        }
        vars.dlg.addItem.show = false;
      },
      onSavingItem(e) {
        e.changes.forEach(element => {
          if (element.type != 'remove') {
            element.data.fk_company_id = authService.getCompanyId();
            delete element.data.lend_number;
            delete element.data.item;
          }
        });
      },
      onDataError(e) {
        if (e.error.response.status == 605) {
          e.error.message = '연결된 데이터가 있어서 삭제가 안됩니다';
        } else if (e.error.response.status == 403) {
          e.error.message = '권한이 없습니다';
        }
      },
      onCellHoverChanged(e) {
        if (!vars.dlg.finder.show) { vars.focus.status = e; }
      },
      async searchDateRange() {
        if (vars.formData.startDate > vars.formData.endDate) {
          await alert('조회 일자가 잘못 되었습니다', '조회');
          return;
        }
        vars.grid['status'].filter([
          [
            'lend_date',
            '>=',
            moment(vars.formData.startDate).startOf('day').format('YYYY-MM-DD 00:00:00'),
          ],
          'and',
          [
            'lend_date',
            '<=',
            moment(vars.formData.endDate).endOf('day').format('YYYY-MM-DD 23:59:59'),
          ],
        ]);
      },
    };

    return { vars, methods, shipmentLend, baseItem, generateItemButtonOption };
  },
};
</script>
