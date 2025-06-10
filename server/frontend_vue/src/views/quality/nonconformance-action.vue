<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">부적합조치등록</div>
            </dx-item>
          </dx-toolbar>
        </div>
        <div>
          <dx-form :form-data="formdata">
            <dx-group-item :col-count="5">
              <dx-simple-item data-field="startdate" editor-type="dxDateBox">
                <dx-label text="작지일자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="enddate" editor-type="dxDateBox">
                <dx-label text="~" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                item-type="button"
                horizontal-alignment="left"
                :button-options="{
                  icon: 'search',
                  text: '검색',
                  type: 'normal',
                  onClick: searchDateRange,
                }"
              />
            </dx-group-item>
          </dx-form>
        </div>
      </div>
      <div class="dx-card responsive-paddings mt-1">
        <dx-data-grid
          height="calc(100vh - 234px)"
          date-serialization-format="yyyy-MM-ddTHH:mm:ss"
          column-resizing-mode="widget"
          :on-initialized="evt => initialized(evt, 'status-list')"
          :data-source="nonconformanceAction"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-reordering="true"
          :allow-column-resizing="true"
          :hover-state-enabled="true"
          :focus-state-enabled="true"
          :row-alternation-enabled="true"
          :scrolling="{ mode: 'virtual', rowRenderingMode: 'virtual' }"
          @cell-click="goDetail"
        >
          <dx-column
            data-field="done"
            caption="조치여부"
            :filter-operations="['=']"
          />
          <dx-column data-field="work_order.number" caption="작지번호" />
          <dx-column data-field="performance.number" caption="실적번호" />
          <dx-column
            data-field="work_order.target_date"
            caption="작지일자"
            data-type="date"
            format="yyyy-MM-dd"
            sort-order="desc"
          />
          <dx-column data-field="lot_no" caption="LOT NO." />
          <dx-column data-field="item.item_code" caption="제품코드" />
          <dx-column data-field="item.item_name" caption="제품명" />
          <dx-column data-field="process_name" caption="공정명" />
          <dx-column data-field="equipment_name" caption="설비명" />
          <dx-column data-field="qa_manager" caption="검사자" />
          <dx-column data-field="bad_type" caption="불량유형" />
          <dx-column data-field="bad_quantity" caption="불량수량" />
          <dx-column data-field="action_quantity" caption="재작업수량" />

          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
        </dx-data-grid>
      </div>
    </div>

    <dx-popup
      v-model:visible="dialog.show"
      content-template="popup-content"
      title="조치등록"
      :show-title="true"
      width="70%"
      :height="460"
      :resize-enabled="true"
      @initialized="evt => initialized(evt, 'item-popup')"
      @hiding="onHiding"
    >
      <template #popup-content>
        <dx-data-grid
          date-serialization-format="yyyy-MM-ddTHH:mm:ss"
          column-resizing-mode="widget"
          :data-source="qualityNonconformanceActionItem"
          :show-borders="true"
          :allow-column-reordering="true"
          :allow-column-resizing="true"
          :column-auto-width="true"
          :remote-operations="true"
          @initialized="evt => initialized(evt, 'action-item')"
          @init-new-row="onNewActionRow"
          @saving="onActionSaving"
          @saved="onActionSaved"
        >
          <dx-grid-toolbar>
            <dx-grid-item name="addRowButton" />
            <!--dx-grid-item
              widget="dxButton"
              :options="{ icon: 'close', onClick: closePopup }"
            /-->
          </dx-grid-toolbar>

          <dx-column
            data-field="action_date"
            caption="조치일자"
            data-type="date"
            format="yyyy-MM-dd"
          />
          <dx-column data-field="action_manager" caption="조치담당자">
            <dx-lookup
              :data-source="common.employee"
              display-expr="emp_name"
              value-expr="emp_name"
            />
          </dx-column>

          <dx-column
            data-field="action_quantity"
            caption="조치수량"
            data-type="number"
          />
          <dx-column data-field="action_detail" caption="조치내용">
            <dx-lookup
              :data-source="common.actionType"
              value-expr="code_name"
              display-expr="code_name"
            />
          </dx-column>
          <dx-column data-field="note" caption="적요" />
          <dx-column data-field="action_checker" caption="조치확인자">
            <dx-lookup
              :data-source="common.employee"
              display-expr="emp_name"
              value-expr="emp_name"
            />
          </dx-column>
          <dx-column
            data-field="confirm_date"
            caption="확인일자"
            data-type="date"
            format="yyyy-MM-dd"
          />
          <dx-paging :page-size="20" />
          <dx-editing
            :allow-adding="true"
            :allow-updating="true"
            :allow-deleting="true"
            :use-icons="true"
            mode="row"
          />
        </dx-data-grid>
      </template>
    </dx-popup>
  </div>
</template>

<script setup>
import {
  DxForm,
  DxLabel,
  DxGroupItem,
  DxSimpleItem,
} from 'devextreme-vue/form';
import {
  DxDataGrid,
  DxColumn,
  DxPaging,
  DxFilterRow,
  DxEditing,
  DxLookup,
  DxToolbar as DxGridToolbar,
  DxItem as DxGridItem,
} from 'devextreme-vue/data-grid';
import { DxPopup } from 'devextreme-vue/popup';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { baseCodeLoader, baseEmployee } from '../../data-source/base';
import {
  getQualityNonconformanceAction,
  qualityNonconformanceActionItem,
} from '../../data-source/quality';
import { ref, reactive } from 'vue';
import moment from 'moment';
import authService from '../../auth';
import { notifyError, notifyInfo } from '../../utils/notify';

const dialog = ref({
  show: false,
  id: null,
  bad_quantity: 0,
  action_quantity: 0,
  done: null,
});
const formdata = reactive({
  startdate: new Date(),
  enddate: new Date(),
});
const common = reactive({ actionType: [], employee: [] });

const nonconformanceAction = getQualityNonconformanceAction([
  { name: 'bad_quantity', op: '>', val: 0 },
  { name: 'fk_work_order_id', op: 'is_not_null' },
]);
qualityNonconformanceActionItem.defaultFilters = [
  { name: 'fk_non_conformance_action_id', op: 'eq', val: 0 },
];

const components = {};

!(async () => {
  const { data: employee } = await baseEmployee.load();
  common.employee = employee;
  const response = await baseCodeLoader(
    ['조치내용'],
    authService.getCompanyId()
  );
  common.actionType = response['조치내용'];
})();

function initialized(evt, key) {
  components[key] = evt.component;
}

function goDetail({ column, data }) {
  if (column.name !== 'bad_quantity') return;
  qualityNonconformanceActionItem.defaultFilters[0].val = data.id;
  dialog.value.show = true;
  dialog.value.id = data.id;
  dialog.value.bad_quantity = data.bad_quantity;
  dialog.value.action_quantity = 0;
  dialog.value.done = data.done;
  if (components['action-item']) components['action-item'].refresh();
}

function onHiding() {
  components['action-item'].cancelEditData();
  qualityNonconformanceActionItem.defaultFilters[0].val = 0;
  components['status-list'].refresh();
}

function onNewActionRow(evt) {
  evt.data.action_date = new Date();
  evt.data.action_quantity = 0;
  evt.data.action_detail = common.actionType[0].code_name;
  evt.data.action_checker = authService.getUserName();
  evt.data.confirm_date = new Date();
}

function onActionSaving(evt) {
  const total = evt.component
    .getVisibleRows()
    .reduce((sum, row) => sum + row.data.action_quantity, 0);
  if (total > dialog.value.bad_quantity) {
    evt.cancel = true;
    notifyError('조치 수량이 불량 수량 보다 많습니다');
    return;
  }

  evt.changes.forEach(row => {
    if (row.type === 'insert')
      row.data.fk_non_conformance_action_id = dialog.value.id;
  });
}

function onActionSaved(evt) {
  const totalAction = evt.component.getVisibleRows().reduce((sum, row) => {
    if (row.data.action_detail == '재작업') {
      return sum + row.data.action_quantity;
    }
    return sum;
  }, 0);
  const total = evt.component.getVisibleRows().reduce((sum, row) => {
    if (row.data.action_detail) {
      return sum + row.data.action_quantity;
    }
    return sum;
  }, 0);
  const updateValues = { action_quantity: totalAction };
  let message = '';
  if (total === dialog.value.bad_quantity) {
    updateValues.done = true;
    message = '부적합 조치가 완료되었습니다';
  } else if (dialog.value.done === true) {
    updateValues.done = false;
    message = '부적합 조치가 취소되었습니다';
  } else {
    message = '부적합 조치가 완료되었습니다';
  }
  nonconformanceAction
    .update(dialog.value.id, updateValues)
    .then(() => notifyInfo(message));
}

function closePopup() {
  components['item-popup'].hide();
}

async function searchDateRange() {
  components['status-list'].filter([
    [
      'work_order.target_date',
      '>=',
      moment(formdata.startdate)
        .startOf('day')
        .format('YYYY-MM-DDTHH:mm:ss'),
    ],
    'and',
    [
      'work_order.target_date',
      '<=',
      moment(formdata.enddate)
        .endOf('day')
        .format('YYYY-MM-DDTHH:mm:ss'),
    ],
  ]);
}
</script>
