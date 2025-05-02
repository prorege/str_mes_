<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">제품원가현황</div>
            </dx-item>
          </dx-toolbar>
        </div>
        <div>
          <div class="search-status">
            <span class="search-title">생산입고일자</span>
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
          height="calc(100vh - 280px)"
          date-serialization-format="yyyy-MM-ddTHH:mm:ss"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="false"
          :focused-row-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :data-source="vars.dataSource.performanceItem1"
          :on-initialized="evt => methods.onInitialized(evt, 'status')"
          @exporting="methods.onExporting"
          @row-dbl-click="methods.goDetail"
        >
          <dx-column caption="생산입고번호" data-field="performance_registration.number" :filter-operations="['contains', '=']" />
          <dx-column caption="입고일자" data-field="performance_registration.target_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
          <dx-column caption="생산입고수량" data-field="production_receiving_quantity" data-type="number" format="fixedPoint" :calculate-display-value="methods.productionReceivingQuantity" />
          <dx-column caption="생산제품" data-field="item.item_name" />
          <dx-column caption="제품원가" data-field="item.purchase_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
          <dx-column caption="금액" data-field="total_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :calculate-cell-value="methods.calculateTotalPrice" />
          <dx-column caption="품목중분류" data-field="item.middle_category" />

          <dx-sorting mode="single" />
          <dx-paging :page-size="20" />
          <dx-export :enabled="true" />
          <dx-filter-row :visible="true" />
          <dx-column-chooser mode="select" :enabled="true" />
        </dx-data-grid>
        
        <div class="mt-2">
          <table class="summary-table">
            <tr>
              <th>입고수량합계</th>
              <td>{{ vars.summary.quantity }}</td>
              <th>합계금액</th>
              <td>{{ vars.summary.total_price }}</td>
            </tr>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment';
import numeral from 'numeral';

import { reactive, computed, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';

import { alert } from 'devextreme/ui/dialog';
import DxButton from 'devextreme-vue/button';
import DxCheckBox from 'devextreme-vue/check-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
  
import { DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxColumnChooser } from 'devextreme-vue/data-grid';

import stateStore from '@/utils/state-store';
import { performanceItem1, getPerformanceItem1 } from '../../data-source/produce';

export default {
  components: {
    DxButton,
    DxCheckBox,
    DxDateBox,
    DxToolbar, DxItem,
    DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxColumnChooser,
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
    vars.summary = reactive({
      quantity: 0,
      total_price: '₩0'
    });
    vars.dataSource = reactive({
      performanceItem1: []
    });
    vars.timer = {
      summary: null
    }

    onBeforeUnmount(() => {
      if (vars.timer.summary) {
        clearInterval(vars.timer.summary);
      }
    });

    const methods = {
      onInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`product-cost-${key}`, evt.component);

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
        vars.dataSource.performanceItem1 = getPerformanceItem1([
          {name: 'performance_registration', op: 'has', val: {name: 'target_date', op: 'gte', val: moment(vars.formData.startDate).startOf('day').format('YYYY-MM-DD 00:00:00')}},
          {name: 'performance_registration', op: 'has', val: {name: 'target_date', op: 'lte', val: moment(vars.formData.endDate).endOf('day').format('YYYY-MM-DD 23:59:59')}},
        ]);

        clearInterval(vars.timer.summary);
        vars.timer.summary = setInterval(() => {
          methods.calcSummary();
        }, 1000);
      },
      workOrderQuantity(rowData) {
        if (!rowData.performance_registration) return '0';
        return rowData.performance_registration.required_quantity;
      },
      productionReceivingQuantity(rowData) {
        if (!rowData.production_receiving_quantity) return '0';
        return rowData.production_receiving_quantity;
      },
      calculateTotalPrice(rowData) {
        let quantity = 0;
        if (rowData.production_receiving_quantity) {
          quantity = rowData.production_receiving_quantity;
        }
        let price = 0;
        if (rowData.item && rowData.item.purchase_price) {
          price = rowData.item.purchase_price;
        }
        return quantity * price;
      },
      checkQuantity(rowData) {
        if (!rowData.check_quantity) return '0';
        return rowData.check_quantity;
      },
      badQuantity(rowData) {
        if (!rowData.bad_quantity) return '0';
        return rowData.bad_quantity;
      },
      actionQuantity(rowData) {
        if (!rowData.action_quantity) return '0';
        return rowData.action_quantity;
      },
      goodQuantity(rowData) {
        if (!rowData.good_quantity) return '0';
        return rowData.good_quantity;
      },
      availableStock(rowData) {
        if (!rowData.basic_stock) return '0';
        return rowData.basic_stock.available_stock;
      },
      currentStock(rowData) {
        if (!rowData.basic_stock) return '0';
        return rowData.basic_stock.current_stock;
      },
      onExporting(evt) {
        performanceItem1.exportData(
          evt.component,
          '생산입고현황',
          `생산입고현황_${Date.now()}.xlsx`
        );
        evt.cancel = true;
      },
      calcSummary() {
        let total_quantity = 0;
        let total_price = 0;
        const rows = vars.grid.status.getVisibleRows();
        for (const row of rows) {
          console.log(row);
          let quantity = 0;
          if (row.data.production_receiving_quantity) {
            quantity = row.data.production_receiving_quantity;
          }
          let price = 0;
          if (row.data.item && row.data.item.purchase_price) {
            price = row.data.item.purchase_price;
          }
          total_price += (quantity * price);
          total_quantity += quantity;
        }
        vars.summary.quantity = total_quantity;
        vars.summary.total_price = '₩' + numeral(total_price).format('0,0');
      },
    };

    return { vars, methods, performanceItem1 };
  },
};
</script>
