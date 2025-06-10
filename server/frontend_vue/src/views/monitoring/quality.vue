<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">품질현황</div>
            </dx-item>
          </dx-toolbar>
        </div>
        <div>
          <div class="search-status">
            <span class="search-title">생산일자</span>
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
          key-expr="id"
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="false"
          :focused-row-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :data-source="vars.dataSource.item1"
          :on-initialized="evt => methods.onInitialized(evt, 'status')"
          @exporting="methods.onExporting"
        >
          <dx-column caption="생산일자" data-field="target_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="품목중분류" data-field="middle_category" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item_name" />
          <dx-column caption="규격" data-field="item_standard" />
          <dx-column caption="생산수량" data-field="check_quantity" data-type="number" format="fixedPoint" :calculate-display-value="methods.checkQuantity" />
          <dx-column caption="양품수량" data-field="good_quantity" data-type="number" format="fixedPoint" :calculate-display-value="methods.goodQuantity" />
          <dx-column caption="불량수량" data-field="bad_quantity" data-type="number" format="fixedPoint" :calculate-display-value="methods.badQuantity" />
          <dx-column caption="불량률(%)" data-field="bad_percentage" data-type="number" :calculate-display-value="methods.badPercentage" />
          <!-- TODO 기준코드에 있는 불량유형을 가져와서 컬럼으로 넣어야함 -->
          <dx-column caption="납땜불량" data-field="bad1" />
          <dx-column caption="하네스불량" data-field="bad2" />
          <dx-column caption="성능불량_ON" data-field="bad3" />
          <dx-column caption="성능불량_OFF" data-field="bad4" />

          <dx-summary>
            <dx-total-item column="bad1" summary-type="sum" :customize-text="methods.customizeBad1" />
            <dx-total-item column="bad2" summary-type="sum" :customize-text="methods.customizeBad2" />
            <dx-total-item column="bad3" summary-type="sum" :customize-text="methods.customizeBad3" />
            <dx-total-item column="bad4" summary-type="sum" :customize-text="methods.customizeBad4" />
          </dx-summary>

          <dx-paging :page-size="20" />
          <dx-sorting mode="single" />
        </dx-data-grid>
      </div>

      <div class="dx-card responsive-paddings mt-1">
        <dx-chart id="chart" title="월별 불량수량" :data-source="vars.dataSource.monthlyChart">
          <dx-common-series-settings
            type="bar" 
            argument-field="month"
            hover-mode="allArgumentPoints"
            selection-mode="allArgumentPoints"
          >
            <dx-chart-label :visible="true">
              <dx-format type="fixedPoint" :precision="0" />
            </dx-chart-label>
          </dx-common-series-settings>

          <dx-series name="납땜불량" value-field="bad1" />
          <dx-series name="하네스불량" value-field="bad2" />
          <dx-series name="성능불량_ON" value-field="bad3" />
          <dx-series name="성능불량_OFF" value-field="bad4" />

          <dx-legend vertical-alignment="bottom" horizontal-alignment="center" />
        </dx-chart>
      </div>

      <div class="dx-card responsive-paddings mt-1">
        <dx-pie-chart
          id="pie"
          type="doughnut"
          palette="Soft Pastel"
          title="유형별 불량현황"
          :data-source="vars.dataSource.percentage"
        >
          <dx-pie-series argument-field="type" value-field="val">
            <dx-pie-label :visible="true">
              <dx-connector :visible="true" :width="1" />
            </dx-pie-label>
          </dx-pie-series>
          <dx-pie-size :width="500"/>
          <dx-tooltip :enabled="true" />
        </dx-pie-chart>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment';

import { reactive } from 'vue';
import { useRouter } from 'vue-router';

import { alert } from 'devextreme/ui/dialog';
import DxButton from 'devextreme-vue/button';
import DxCheckBox from 'devextreme-vue/check-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxDataGrid, DxColumn, DxPaging, DxSorting, DxSummary, DxTotalItem } from 'devextreme-vue/data-grid';
import { DxChart, DxSize, DxSeries, DxFormat, DxLegend, DxCommonSeriesSettings, DxLabel as DxChartLabel } from 'devextreme-vue/chart';
import DxPieChart, { DxSize as DxPieSize, DxSeries as DxPieSeries, DxFormat as DxPieFormat, DxLegend as DxPieLegend, DxTooltip, DxConnector, DxLabel as DxPieLabel } from 'devextreme-vue/pie-chart';

import stateStore from '@/utils/state-store';
import ApiService from '../../utils/api-service';

export default {
  components: {
    DxButton,
    DxCheckBox,
    DxDateBox,
    DxToolbar, DxItem,
    DxDataGrid, DxColumn, DxPaging, DxSorting, DxSummary, DxTotalItem,
    DxChart, DxSize, DxPieSize, DxSeries, DxFormat, DxLegend, DxCommonSeriesSettings, DxChartLabel,
    DxPieChart, DxPieSeries, DxPieFormat, DxPieLegend, DxTooltip, DxConnector, DxPieLabel,
  },
  setup() {
    const router = useRouter();
    const apiItem = new ApiService('/api/mes/v1/monitoring/nonconformance/item')
    const apiMonthlyChart = new ApiService('/api/mes/v1/monitoring/nonconformance');
    const apiPercentage = new ApiService('/api/mes/v1/monitoring/nonconformance/percentage');
    const vars = {};
    vars.grid = {};
    vars.formData = reactive({
      startDate: new Date(),
      endDate: new Date(),
    });
    vars.formData.startDate.setDate(vars.formData.startDate.getDate() - 7);
    vars.dataSource = reactive({
      item1: [],
      monthlyChart: []
    });

    const methods = {
      onInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`produce-perform-reg-${key}`, evt.component);

        methods.initSorting();
        methods.searchDateRange();
      },
      initSorting() {
        const columns = vars.grid['status'].getVisibleColumns();
        const col = columns.filter(item => item.sortOrder);
        if (col.length == 0) {
          const defaultName = 'performance_registration.target_date';
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
        router.push({
          path: `/produce/performance-registration/${data.performance_registration.id}`,
        });
      },
      async searchDateRange() {
        if (vars.formData.startDate > vars.formData.endDate) {
          await alert('조회 일자가 잘못 되었습니다', '조회');
          return;
        }
        apiItem.post('', {
          start_date: moment(vars.formData.startDate).startOf('day').format('YYYY-MM-DD 00:00:00'),
          end_date: moment(vars.formData.endDate).endOf('day').format('YYYY-MM-DD 23:59:59')
        }).then((res) => {
          vars.dataSource.item1 = res.data;
        });

        apiMonthlyChart.post('', '').then((res) => {
          vars.dataSource.monthlyChart = res.data;
        });
        
        apiPercentage.post('', '').then((res) => {
          vars.dataSource.percentage = res.data;
        })
      },
      checkQuantity(rowData) {
        if (!rowData.check_quantity) return '0';
        return rowData.check_quantity;
      },
      badQuantity(rowData) {
        if (!rowData.bad_quantity) return '0';
        return rowData.bad_quantity;
      },
      goodQuantity(rowData) {
        if (!rowData.good_quantity) return '0';
        return rowData.good_quantity;
      },
      badPercentage(rowData) {
        let bad_quantity = 0;
        if (rowData.bad_quantity) {
          bad_quantity = rowData.bad_quantity;
        }
        if (bad_quantity == 0) { return 0; }

        let check_quantity = 0;
        if (rowData.check_quantity) {
          check_quantity = rowData.check_quantity;
        }
        return (bad_quantity * 100) / check_quantity;
      },
      customizeBad1(data) {
        if (data.value) { return `납땜불량: ${data.value}`; } 
        else { return `납땜불량: 0`; }
      },
      customizeBad2(data) {
        if (data.value) { return `하네스불량: ${data.value}`; } 
        else { return `하네스불량: 0`; }
      },
      customizeBad3(data) {
        if (data.value) { return `성능불량_ON: ${data.value}`; } 
        else { return `성능불량_ON: 0`; }
      },
      customizeBad4(data) {
        if (data.value) { return `성능불량_OFF: ${data.value}`; } 
        else { return `성능불량_OFF: 0`; }
      },
    };

    return { vars, methods };
  },
};
</script>
