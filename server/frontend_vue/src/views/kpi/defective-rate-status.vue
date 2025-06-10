<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">Claim 건 수</div>
            </dx-item>
          </dx-toolbar>
        </div>
        <div>
          <div class="search-status">
            <span class="search-title">생산계획일자</span>
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
          :remote-operations="false"
          :hover-state-enabled="true"
          :focused-row-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :data-source="vars.dataSource.item1"
          :on-initialized="evt => methods.onInitialized(evt, 'status')"
          @exporting="methods.onExporting"
          @row-dbl-click="methods.goDetail"
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
          <dx-column caption="불량률" data-field="defective_rate" :calculate-display-value="methods.calculateDefectiveRate" />

          <dx-summary>
            <dx-total-item
              column="defective_rate"
              summary-type="avg"
              :customize-text="methods.customizeAvgRate"
            />
          </dx-summary>

          <dx-paging :page-size="20" />
          <dx-export :enabled="true" />
          <dx-filter-row :visible="true" />
        </dx-data-grid>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment';

import { reactive } from 'vue';
import { useRouter } from 'vue-router';

import DxButton from 'devextreme-vue/button';
import DxCheckBox from 'devextreme-vue/check-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxDataGrid, DxColumn, DxPaging, DxExport, DxSummary, DxSorting, DxTotalItem, DxFilterRow, DxColumnChooser } from 'devextreme-vue/data-grid';

import stateStore from '@/utils/state-store';
import { qualityTestRegistration, getQualityTestRegistration } from '../../data-source/quality';

export default {
  components: {
    DxButton,
    DxCheckBox,
    DxDateBox,
    DxToolbar, DxItem,
    DxDataGrid, DxColumn, DxPaging, DxExport, DxSummary, DxSorting, DxTotalItem, DxFilterRow, DxColumnChooser,
  },
  setup() {
    const router = useRouter();
    const vars = {};
    vars.grid = {};
    vars.formData = reactive({
      startDate: new Date(),
      endDate: new Date(),
    });
    vars.formData.startDate.setDate(vars.formData.startDate.getDate() - 7);
    vars.dataSource = reactive({
      item1: null
    })

    const methods = {
      onInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`defective-rate-${key}`, evt.component);

        methods.initSorting();
        methods.searchDateRange();
      },
      initSorting() {
        const columns = vars.grid['status'].getVisibleColumns();
        const col = columns.filter(item => item.sortOrder);
        if (col.length == 0) {
          const defaultName = 'qa_date';
          const defaultSort = columns.filter(item => item.name == defaultName);
          if (defaultSort.length > 0) {
            vars.grid['status'].columnOption(
              defaultSort[0].index,
              'sortOrder',
              'desc'
            );
          }
        }
      },
      goDetail({ data }) {
        router.push({ path: `/quality/test-registration/${data.id}` });
      },
      onExporting(evt) {
        qualityTestRegistration.exportData(evt.component, '불량률현황', `불량률현황_${Date.now()}.xlsx`)
        evt.cancel = true
      },
      customizeAvgRate(data) {
        if (data.value) {
          return `평균 불량률: ${data.value}`;
        } else {
          return `평균 불량률: 0`;
        }
      },
      calculateDefectiveRate(rowData) {
        let badQuantity = 0;
        if (rowData.bad_quantity) {
          badQuantity = rowData.bad_quantity;
        }
        let processQuantity = 0;
        if (rowData.process_quantity) {
          processQuantity = rowData.process_quantity;
        }
        return (badQuantity / processQuantity) * 100;
      },
      async searchDateRange() {
        vars.dataSource.item1 = getQualityTestRegistration([
          {name: 'qa_date', op: 'gte', val:  moment(vars.formData.startDate).startOf('day').format('YYYY-MM-DD 00:00:00')},
          {name: 'qa_date', op: 'lte', val: moment(vars.formData.endDate).endOf('day').format('YYYY-MM-DD 23:59:59')}
        ]);
      }
    }
    

    return { vars, methods, qualityTestRegistration };
  },
}
</script>

<style>
.dimmed {
  color: #a0a0a0;
  font-style: italic;
}
</style>
