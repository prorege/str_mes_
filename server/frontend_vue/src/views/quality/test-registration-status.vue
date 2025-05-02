<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">

        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">검사등록현황</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div>
          <dx-form :form-data="formdata">
            <dx-group-item :col-count="5">
              <dx-simple-item data-field="startdate" editor-type="dxDateBox">
                <dx-label text="검사일자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="enddate" editor-type="dxDateBox">
                <dx-label text="~" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item item-type="button" horizontal-alignment="left"
                :button-options="{ text: '검색', icon: 'search', type: 'normal', onClick: searchDateRange, }"
              />
            </dx-group-item>
          </dx-form>
        </div>

      </div>

      <div class="dx-card responsive-paddings mt-1">
        <dx-data-grid
          height="calc(100vh - 230px)"
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :hover-state-enabled="true"
          :focused-row-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :data-source="qualityTestRegistration"
          @exporting="onExporting"
          @row-dbl-click="goDetailPage"
          @initialized="evt => initialized(evt, 'status-list')"
        >
          <dx-column caption="검사번호" data-field="qa_number" :filter-operations="['contains', '=']" />
          <dx-column caption="검사일자" data-field="qa_date" data-type="date" format="yyyy-MM-dd" sort-order="desc" />
          <dx-column caption="검사구분" data-field="test_type" />
          <dx-column caption="설비명" data-field="equipment" />
          <dx-column caption="LOTNO." data-field="lot_no" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item_name" />
          <dx-column caption="규격" data-field="standard" />
          <dx-column caption="검사수량" data-field="process_quantity" />
          <dx-column caption="불량수량" data-field="bad_quantity" />
          <dx-column caption="양품수량" data-field="good_quantity" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="검사성적서" data-field="qa_standard_path" cell-template="download" />
          <dx-column caption="공정명" data-field="process_name" />

          <!-- <dx-column data-field="vat" caption="검사항목" />
          <dx-column data-field="vat" caption="검사규격" />
          <dx-column data-field="vat" caption="공차(+)" />
          <dx-column data-field="vat" caption="공차(-)" />
          <dx-column data-field="vat" caption="검사규격상세" />
          <dx-column data-field="vat" caption="검사방법" />
          <dx-column data-field="vat" caption="작업자" />
          <dx-column data-field="vat" caption="측정값" />
          <dx-column data-field="vat" caption="측정단위" />
          <dx-column data-field="vat" caption="측정장비" /> -->

          <dx-export :enabled="true" />
          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />

          <template #download="{data}">
            <a v-if="data.value"
              download
              :href="`/api/mes/v1/quality/quality_management_download/${data.value}`"
            >
              {{ data.value }}
            </a>
            <span class="dimmed" v-else>없음</span>
          </template>
        </dx-data-grid>
      </div>
    </div>
  </div>
</template>

<script setup>
import moment from 'moment';

import { reactive } from 'vue';
import { useRouter } from 'vue-router';

import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem, } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxExport, DxFilterRow, } from 'devextreme-vue/data-grid';

import { qualityTestRegistration } from '../../data-source/quality';

const router = useRouter();
const formdata = reactive({
  startdate: new Date(),
  enddate: new Date(),
});
const components = {};

function initialized(evt, key) {
  components[key] = evt.component;
}

function goDetailPage({ data }) {
  router.push({ path: `/quality/test-registration/${data.id}` });
}

async function searchDateRange() {
  components['status-list'].filter([
    [
      'qa_date',
      '>=',
      moment(formdata.startdate).startOf('day').format('YYYY-MM-DDTHH:mm:ss'),
    ],
    'and',
    [
      'qa_date',
      '<=',
      moment(formdata.enddate).endOf('day').format('YYYY-MM-DDTHH:mm:ss'),
    ],
  ]);
}

function onExporting (evt) {
  qualityTestRegistration.exportData(evt.component, '검사등록현황', `검사등록현황_${Date.now()}.xlsx`)
  evt.cancel = true
}
</script>

<style>
.dimmed {
  color: #a0a0a0;
  font-style: italic;
}
</style>
