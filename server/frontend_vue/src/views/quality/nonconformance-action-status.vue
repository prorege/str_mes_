<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">부적합조치현황</div>
            </dx-item>
          </dx-toolbar>
        </div>
        
        <div>
          <dx-form :form-data="formdata">
            <dx-group-item :col-count="5">
              <dx-simple-item data-field="startdate" editor-type="dxDateBox">
                <dx-label text="조치일자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="enddate" editor-type="dxDateBox">
                <dx-label text="~" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item item-type="button" horizontal-alignment="left"
                :button-options="{text: '검색', icon: 'search', type: 'normal', onClick: searchDateRange}"
              />
            </dx-group-item>
          </dx-form>
        </div>

      </div>

      <div class="dx-card responsive-paddings mt-1">
        <dx-data-grid
          height="calc(100vh - 234px)"
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :focused-row-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :data-source="qualityNonconformanceActionItem"
          @initialized="evt => initialized(evt, 'status-list')"
          @row-dbl-click="goDetail"
          @exporting="onExporting"
        >
          <dx-column caption="작지번호" data-field="work_order.number" :filter-operations="['contains', '=']" />
          <dx-column caption="실적번호" data-field="performance.number" :filter-operations="['contains', '=']" />
          <dx-column caption="검사번호" data-field="quality_management.qa_number" :filter-operations="['contains', '=']" />
          <dx-column caption="작지일자" data-field="work_order.target_date"  data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="LOT No" data-field="non_conformance_action.lot_no" />
          <dx-column caption="제품코드" data-field="item.item_code" />
          <dx-column caption="제품명" data-field="item.item_name" />
          <dx-column caption="공정명" data-field="non_conformance_action.process_name" />
          <dx-column caption="설비명" data-field="non_conformance_action.equipment_name" />
          <dx-column caption="검사자" data-field="non_conformance_action.qa_manager" />
          <dx-column caption="불량유형" data-field="non_conformance_action.bad_type" />
          <dx-column caption="검사수량" data-field="quality_management.process_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="불량수량" data-field="quality_management.bad_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="조치일자" data-field="action_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
          <dx-column caption="조치담당자" data-field="action_manager" />
          <dx-column caption="조치수량" data-field="action_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="조치내용" data-field="action_detail" />
          <dx-column caption="적요" data-field="note" />
          <dx-column caption="조치확인자" data-field="action_checker" />
          <dx-column caption="확인일자" data-field="confirm_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="자산구분" data-field="item.asset_type" />
          <dx-column caption="대분류" data-field="item.main_category" />
          <dx-column caption="중분류" data-field="item.middle_category" />
          <dx-column caption="소분류" data-field="item.sub_category" />

          <dx-export :enabled="true" />
          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
        </dx-data-grid>
      </div>
    </div>
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
  DxExport
} from 'devextreme-vue/data-grid';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { useRouter } from 'vue-router';
import { qualityNonconformanceActionItem } from '../../data-source/quality';
import { reactive } from 'vue';
import moment from 'moment';

const router = useRouter();
const formdata = reactive({
  startdate: new Date(),
  enddate: new Date(),
});
const components = {};
qualityNonconformanceActionItem.defaultFilters = undefined;

function initialized(evt, key) {
  components[key] = evt.component;
}

function goDetail({ column, data }) {
  if (column.name === 'work_order.number') {
    router.push({ path: `/produce/work-order/${data.fk_work_order_id}` });
  } else if (column.name === 'quality_management.qa_number') {
    router.push({
      path: `/quality/test-registration/${data.fk_quality_management_id}`,
    });
  } else if (column.name === 'performance.number') {
    router.push({
      path: `/produce/performance-registration/${data.fk_performance_id}`,
    });
  }
}

async function searchDateRange() {
  components['status-list'].filter([
    [
      'action_date',
      '>=',
      moment(formdata.startdate).startOf('day').format('YYYY-MM-DDTHH:mm:ss'),
    ],
    'and',
    [
      'action_date',
      '<=',
      moment(formdata.enddate).endOf('day').format('YYYY-MM-DDTHH:mm:ss'),
    ],
  ]);
}

function onExporting (evt) {
  qualityNonconformanceActionItem.exportData(evt.component, '부적합조치현황', `부적합조치현황_${Date.now()}.xlsx`)
  evt.cancel = true
}
</script>
