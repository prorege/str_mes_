<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">상품수불장</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div v-if="vars.init.value">
          <div class="search-status search-line">
            <span class="search-title">조회일자</span>
            <dx-date-box v-model:value="vars.formData.startDate" />
            <span class="search-bar">~</span>
            <dx-date-box v-model:value="vars.formData.endDate" />

            <span class="search-tab"></span>

            <SearchButtonGroup @change="({startDate, endDate}) => { vars.formData.startDate = startDate; vars.formData.endDate = endDate; }" />
          </div>
          <div class="search-status">
            <span class="search-title">품목코드</span>
            <dx-text-box :value="vars.formData.itemCode">
              <dx-text-box-button name="search" location="after"
                :options="{ icon: 'search', stylingMode: 'text', onClick: () => (vars.dlg.findItem.show = true) }"
              />
            </dx-text-box>

            <span class="search-tab"></span>

            <span class="search-title">창고선택</span>
            <dx-lookup
              value-expr="wh_name"
              display-expr="wh_name"  
              v-model:value="vars.formData.warehouseName"
              :data-source="vars.dataSource.warehouse"
            />

            <span class="search-tab"></span>

            <dx-button text="검색" icon="search" @click="methods.searchDateRange()" />
          </div>
        </div>

      </div>

      <div class="dx-card responsive-paddings mt-1">
        <dx-data-grid
          key-expr="id"
          height="calc(100vh - 340px)"
          column-resizing-mode="widget"
          :data-source="vars.dataSource.status"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="false"
          :focused-row-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          @initialized="evt => methods.onGridInitialized(evt, 'status-list')"
        >
          <dx-grid-toolbar>
            <dx-item template="print" location="before" />
          </dx-grid-toolbar>
          <template #print>
            <dx-button icon="print" text="상품수불장 출력" @click="methods.printProductReceipt" />
          </template>

          <dx-column caption="" data-field="group_id" :group-index="0" />
          <dx-column caption="수불일자" data-field="action_date"  data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="입출고유형" data-field="inout_type" />
          <dx-column caption="업체" data-field="company" />
          <dx-column caption="단가" data-field="unit_price" data-type="number" format="₩,##0.00" />
          <dx-column caption="이월재고" data-field="past_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="입고수량" data-field="receiving_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="출고수량" data-field="release_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="누적재고" data-field="sum_by_case" data-type="number" format="fixedPoint" />
          <dx-column caption="입출고번호" data-field="number" />
          <dx-column caption="누적입고수량" data-field="accumulate_receiving_stock" data-type="number" format="fixedPoint" :visible="false" />
          <dx-column caption="누적출고수량" data-field="accumulate_release_stock" data-type="number" format="fixedPoint" :visible="false" />

          <dx-summary :calculate-custom-summary="methods.calculateCustomSummary">
            <dx-group-item
              :align-by-column="true"
              column="receiving_stock"
              summary-type="sum"
              value-format="fixedPoint"
              display-format="입고수량: {0}"
            />
            <dx-group-item
              :align-by-column="true"
              column="release_stock"
              summary-type="sum"
              value-format="fixedPoint"
              display-format="출고수량: {0}"
            />
            <dx-group-item
              :show-in-group-footer="true"
              column="accumulate_receiving_stock"
              summary-type="max"
              value-format="fixedPoint"
              show-in-column="receiving_stock"
              display-format="누적입고수량: {0}"
            />
            <dx-group-item
              :show-in-group-footer="true"
              column="accumulate_release_stock"
              summary-type="max"
              value-format="fixedPoint"
              show-in-column="release_stock"
              display-format="누적출고수량: {0}"
            />
            <dx-group-item
              :show-in-group-footer="true"
              name="last_stock_summary"
              summary-type="custom"
              value-format="fixedPoint"
              show-in-column="sum_by_case"
              display-format="누적재고수량: {0}"
            />
          </dx-summary>

          <dx-paging :page-size="20" />
        </dx-data-grid>

        <div class="mt-2">
          <table class="summary-table">
            <tr>
              <td>누계</td>
              <th>이월재고</th>
              <td>{{ vars.dataSource.sum.past_stock }}</td>
              <th>입고수량</th>
              <td>{{ vars.dataSource.sum.receiving_stock }}</td>
              <th>출고수량</th>
              <td>{{ vars.dataSource.sum.release_stock }}</td>
              <th>누적재고</th>
              <td>{{ vars.dataSource.sum.sum_by_case }}</td>
            </tr>
          </table>
        </div>
      </div>
    </div>

    <dx-popup
      title="품목찾기"  
      content-template="popup-content"
      v-model:visible="vars.dlg.findItem.show"
      width="70%"
      :height="460"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'find-item-popup')"
    >
      <template #popup-content>
        <dx-data-grid
          column-resizing-mode="widget"
          :show-borders="true"
          :remote-operations="true"
          :column-auto-width="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="vars.dataSource.baseItem"
          :on-initialized="evt => methods.onGridInitialized(evt, 'baseItem')"
          @selection-changed="methods.selectItem"
        >
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item_name" />
          <dx-column caption="규격" data-field="item_standard" />
          <dx-column caption="자산구분" data-field="asset_type" />

          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-selection mode="single" select-all-mode="page" show-check-boxes-mode="onClick"/>
        </dx-data-grid>
      </template>
    </dx-popup>
  </div>
</template>

<script>
import moment from 'moment';
import numeral from 'numeral';

import { ref, reactive, onMounted } from 'vue';

import { alert } from 'devextreme/ui/dialog';
import DxButton from 'devextreme-vue/button';
import DxLookup from 'devextreme-vue/select-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxTextBox, DxButton as DxTextBoxButton } from 'devextreme-vue/text-box';
import { DxDataGrid, DxColumn, DxPaging, DxSummary, DxSelection, DxGroupItem, DxFilterRow, DxItem as DxGridItem, DxToolbar as DxGridToolbar } from 'devextreme-vue/data-grid';

import SearchButtonGroup from '@/components/search-button-group.vue';

import { baseCodeLoader, getBaseItem } from '@/data-source/base';

import authService from '@/auth';
import stateStore from '@/utils/state-store';
import ApiService from '@/utils/api-service';
import {printDocument} from '@/utils/print-document';
import { loadWarehouse } from '@/utils/data-loader';

export default {
  components: {
    DxButton,
    DxLookup,
    DxDateBox,
    DxToolbar, DxItem,
    DxPopup, DxToolbarItem,
    DxTextBox, DxTextBoxButton,
    DxDataGrid, DxColumn, DxPaging, DxSummary, DxSelection, DxGroupItem, DxFilterRow, DxGridItem, DxGridToolbar,
    SearchButtonGroup
  },
  setup() {
    const vars = { dlg: {} };
    vars.dlg.findItem = reactive({ show: false });
    vars.init = ref(false);
    vars.grid = {};
    vars.formData = reactive({
      itemCode: '',
      warehouseName: '',
      startDate: new Date(),
      endDate: new Date(),
    });
    vars.formData.startDate.setDate(vars.formData.startDate.getDate() - 7);
    vars.dataSource = reactive({
      baseItem: [],
      warehouse: [],
      sum: {
        past_stock: 0,
        receiving_stock: 0,
        release_stock: 0,
        sum_by_case: 0,
      }
    });
    vars.api = {
      statistics: new ApiService('/api/mes/v1/stock/statistics')
    }
    vars.detailItem = ref()


    onMounted(async () => {
      methods.loadBaseItem();
      await loadWarehouse(vars.dataSource);

      const defaultWarehouseName = '본사창고';
      for (const warehouse of vars.dataSource.warehouse) {
        if (warehouse.wh_name === defaultWarehouseName) {
          vars.formData.warehouseName = defaultWarehouseName;
        }
      }
      if (!vars.formData.warehouseName && vars.dataSource.warehouse.length > 0) {
        vars.formData.warehouseName = vars.dataSource.warehouse[0].wh_name;
      }

      vars.init.value = true
    });

    const methods = {
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`stock-item-${key}`, evt.component);

        //methods.searchDateRange();
      },
      loadBaseItem() {
        vars.dataSource.baseItem = getBaseItem(null, null, null);
      },
      selectItem(data) {
        if (data.selectedRowsData.length > 0) {
          const item = data.selectedRowsData[0];
          vars.formData.itemCode = item.item_code;
          vars.detailItem.value = { ...item }
        }
        vars.dlg.findItem.show = false;
      },
      calculateCustomSummary(options) {
        if (options.name === 'last_stock_summary') {
          if (options.summaryProcess === 'start') {
            options.totalValue = 0;
          } else if (options.summaryProcess === 'calculate') {
            options.totalValue = options.value.sum_by_case;
          }
        }
      },
      numberWithCommas(x) {
        return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      },
      async searchDateRange() {
        if (!vars.formData.itemCode) {
          await alert('품목코드를 선택하세요', '조회');
          return;
        }
        if (vars.formData.startDate > vars.formData.endDate) {
          await alert('조회 일자가 잘못 되었습니다', '조회');
          return;
        }

        try {
          vars.grid['status-list'].beginCustomLoading('데이터를 집계중입니다')
          
          const params = {
            item_code: vars.formData.itemCode,
            warehouse_name: vars.formData.warehouseName,
            start: moment(vars.formData.startDate).format('YYYYMMDD'),
            end: moment(vars.formData.endDate).endOf('day').format('YYYY-MM-DD HH:mm:ss'),
          };
          const { data: response } = await vars.api.statistics.post('item', params);
          let sumByCase = 0;
          let sumReceivingStock = 0;
          let sumReleaseStock = 0;
          response.objects.forEach(row => {
            sumByCase = sumByCase + (parseInt(row.past_stock, 10) + row.receiving_stock - row.release_stock);
            row.sum_by_case = sumByCase;
            sumReceivingStock = sumReceivingStock + row.receiving_stock;
            row.accumulate_receiving_stock = sumReceivingStock;
            sumReleaseStock = sumReleaseStock + row.release_stock;
            row.accumulate_release_stock = sumReleaseStock;
          });
          vars.dataSource.status = response.objects;
          vars.dataSource.sum.past_stock = methods.numberWithCommas(response.objects.reduce((sum, row) => sum + parseInt(row.past_stock, 10), 0));
          vars.dataSource.sum.receiving_stock = methods.numberWithCommas(response.objects.reduce((sum, row) => sum + row.receiving_stock, 0));
          vars.dataSource.sum.release_stock = methods.numberWithCommas(response.objects.reduce((sum, row) => sum + row.release_stock, 0));
          vars.dataSource.sum.sum_by_case = methods.numberWithCommas(sumByCase);
        }
        catch (ex) {
          console.error(ex)
        }
        finally {
          vars.grid['status-list'].endCustomLoading()
        }
      },
      async printProductReceipt() {
        if (!vars.dataSource.status) return

        const params = {}
        params.item = vars.detailItem.value
        params.list = []

        params.info = {...vars.formData}
        params.info.startDate = moment(params.info.startDate).format('YYYY년 M월 D일')
        params.info.endDate = moment(params.info.endDate).format('YYYY년 M월 D일')
        
        const list = [...vars.dataSource.status], years = {}
        for (const item of list) {
          const d = moment(item.action_date)
          item.year = d.format('YYYY년')
          item.month = d.format('M월')
          if (!(item.year in years)) years[item.year] = [];
          if (!years[item.year].includes(item.month)) years[item.year].push(item.month)
          item.action_date = d.format('YYYY-MM-DD')
          item.past_stock_str = numeral(parseInt(item.past_stock)).format('0,0')
          item.receiving_stock_str = numeral(parseInt(item.receiving_stock)).format('0,0')
          item.release_stock_str = numeral(parseInt(item.release_stock)).format('0,0')
          item.sum_by_case_str = numeral(parseInt(item.sum_by_case)).format('0,0')
          item.unit_price_str = numeral(parseFloat(item.unit_price)).format('0,0.00')
        }

        const acc = { input: 0, output: 0, stock: parseInt(list[0].past_stock || 0) }
        for(const year in years){

    
          for(const month of years[year]){

            const item = {};
            item.year = year;
            item.month = month;
            item.list = list.filter(v => v.year === year && v.month === month);
            item.mon_input = item.list.reduce((a, i) => a += parseFloat(i.receiving_stock), 0)
            item.mon_input_str = numeral(item.mon_input).format('0,0')
            item.mon_output = item.list.reduce((a, i) => a += parseFloat(i.release_stock), 0)
            item.mon_output_str = numeral(item.mon_output).format('0,0')

            acc.input += item.mon_input
            acc.output += item.mon_output
            acc.stock = acc.stock + item.mon_input - item.mon_output
            
            item.acc_input = numeral(acc.input).format('0,0')
            item.acc_output = numeral(acc.output).format('0,0')
            item.acc_stock = numeral(acc.stock).format('0,0')

            params.list.push(item)
          }
        }
        await printDocument('productreceiptsummary', params);
      },
    };

    return { vars, methods };
  },
};
</script>

<style>
.summary-table {
  width: 100%;
  margin-top: 10px;
}
</style>
