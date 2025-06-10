<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">매출이익현황</div>
            </dx-item>
          </dx-toolbar>
        </div>
        <div>
          <div class="search-status">
            <span class="search-title">출고일자</span>
            <dx-date-box v-model:value="vars.formData.startDate" />
            <span class="search-bar">~</span>
            <dx-date-box v-model:value="vars.formData.endDate" />
            <span class="search-tab"></span>
            <SearchButtonGroup @change="({startDate, endDate}) => { vars.formData.startDate = startDate; vars.formData.endDate = endDate; }" />
            <span class="search-tab"></span>
            <dx-check-box text="미계산서" v-model:value="vars.formData.notSales" />
            <span class="search-tab"></span>
            <dx-button text="검색" icon="search" @click="methods.searchDateRange()" />
          </div>
        </div>
      </div>
      <div class="dx-card responsive-paddings mt-1">
        <dx-data-grid
          height="calc(100vh - 230px)"
          date-serialization-format="yyyy-MM-ddTHH:mm:ss"
          column-resizing-mode="widget"
          :on-initialized="evt => methods.onGridInitialized(evt, 'status')"
          :data-source="dataSource"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-reordering="true"
          :allow-column-resizing="true"
          :row-alternation-enabled="true"
          :focused-row-enabled="true"
          @row-dbl-click="methods.goReleaseDetail"
          @exporting="methods.onExporting"
        >
          <dx-column caption="매출년월" :calculate-cell-value="methods.calcYearMonth" />
          <dx-column caption="출고번호" data-field="release.release_number" :filter-operations="['contains', '=']" />
          <dx-column caption="출고일자" data-field="release.release_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
          <dx-column caption="고객업체약칭" data-field="release.client_alias" />
          <dx-column caption="고객업체" data-field="release.client_company" />
          <dx-column caption="업체분류" data-field="release.client_type" />
          <dx-column caption="담당부서" data-field="release.department" />
          <dx-column caption="업체담당자" data-field="release.manager" />
          <dx-column caption="출고구분" data-field="release.release_type" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="출고수량" data-field="release_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="출고창고" data-field="warehouse.wh_name" />
          <dx-column caption="단가" data-field="unit_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
          <dx-column caption="원가" data-field="cost_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
          <dx-column caption="원가금액" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :calculate-cell-value="methods.calcTotalCost" />
          <dx-column caption="마진금액" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :calculate-cell-value="methods.calcProfit" />
          <dx-column caption="마진율" :calculate-cell-value="methods.calcMarginRate" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="공급가" data-field="supply_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :calculate-cell-value="methods.calcSupplyPrice" />
          <dx-column caption="미계산서" data-field="non_invoice" data-type="number" format="fixedPoint" />
          <dx-column caption="품목대분류" data-field="item.main_category" />
          <dx-column caption="수주번호" data-field="order_number" />
          <dx-column caption="고객사품번" data-field="client_item_number" />

          <dx-export :enabled="true" />
          <dx-paging :page-size="20" />
          <dx-sorting mode="single" />
          <dx-filter-row :visible="true" />
          <dx-column-chooser mode="select" :enabled="true" />
        </dx-data-grid>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment';

import { useRouter } from 'vue-router';
import { reactive } from 'vue';

import { alert } from 'devextreme/ui/dialog';
import DxButton from 'devextreme-vue/button';
import DxCheckBox from 'devextreme-vue/check-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxExport, DxPaging, DxSorting, DxFilterRow, DxColumnChooser } from 'devextreme-vue/data-grid';
import ArrayStore from 'devextreme/data/array_store';
import stateStore from '@/utils/state-store';
import { shipmentReleaseItemWithClient } from '../../data-source/shipment';
import SearchButtonGroup from '../../components/search-button-group.vue';

export default {
  components: {
    DxButton,
    DxCheckBox,
    DxDateBox,
    DxToolbar, DxItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem,
    DxDataGrid, DxColumn, DxExport, DxPaging, DxSorting, DxFilterRow, DxColumnChooser,
    SearchButtonGroup
  },
  setup() {
    const router = useRouter();
    const vars = {};
    vars.grid = {};
    vars.formData = reactive({
      notSales: false,
      startDate: new Date(),
      endDate: new Date(),
    });
    const dataSource = new ArrayStore({ key: 'grid_id', data: [] })
    // vars.formData.startDate.setDate(vars.formData.startDate.getDate() - 7);

    const methods = {
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`profit-status-${key}`, evt.component);

        // methods.initSorting();
        // methods.searchDateRange();
      },
      initSorting() {
        const columns = vars.grid['status'].getVisibleColumns();
        const col = columns.filter(item => item.sortOrder);
        if (col.length == 0) {
          const defaultName = 'release.release_date';
          const defaultSort = columns.filter(item => item.name == defaultName);
          if (defaultSort.length > 0) {
            vars.grid['status'].columnOption(defaultSort[0].index, 'sortOrder', 'desc');
          }
        }
      },
      goReleaseDetail({ data }) {
        router.push({ path: `/shipment/release/${data.release.id}` });
      },
      calcYearMonth(rowData) {
        if (rowData.release.release_date) {
          return rowData.release.release_date.substr(0, 7);
        } 
        return "";
      },
      calcSupplyPrice(rowData) {
        let supplyPrice = 0;
        if (rowData.release_quantity != null && rowData.unit_price != null) {
          supplyPrice = rowData.release_quantity * rowData.unit_price;
        }
        rowData.supply_price = supplyPrice;
        return supplyPrice;
      },
      calcTotalCost(rowData) {
        let totalCost = 0;
        if (rowData.release_quantity != null && rowData.cost_price != null) {
          totalCost = rowData.release_quantity * rowData.cost_price
        }
        return totalCost;
      },
      calcProfit(rowData) {
        let profit = 0.0;
        if (rowData.release_quantity != null && rowData.unit_price != null && rowData.cost_price != null) {
          profit = rowData.release_quantity * (rowData.unit_price - rowData.cost_price);
        }
        return profit;
      },
      calcMarginRate(rowData) {
        let marginRate = 0.0;
        if (rowData.unit_price != 0 && rowData.unit_price != null && rowData.cost_price != null) {
          marginRate = (rowData.unit_price - rowData.cost_price) * 100 / rowData.unit_price;
        }
        return marginRate.toFixed(2) + '%';
      },
       getParams () {
        return { 
          filter: [
            [
              'release.release_date', '>=',
              moment(vars.formData.startDate)
                .startOf('day')
                .format('YYYY-MM-DD 00:00:00'),
            ],
            'and',
            [
              'release.release_date', '<=',
              moment(vars.formData.endDate)
                .endOf('day')
                .format('YYYY-MM-DD 23:59:59'),
            ],
          ],
          sort: [
            {selector : 'release.release_date', desc: true}
          ],
          skip: 0,
          take: 10000
        }
      },
      async searchDateRange() {
        if (vars.formData.startDate > vars.formData.endDate) {
          await alert('조회 일자가 잘못 되었습니다', '조회');
          return;
        }

        // let filter = [
        //   [
        //     'release.release_date',
        //     '>=',
        //     moment(vars.formData.startDate).startOf('day').format('YYYY-MM-DD 00:00:00'),
        //   ],
        //   'and',
        //   [
        //     'release.release_date',
        //     '<=',
        //     moment(vars.formData.endDate).endOf('day').format('YYYY-MM-DD 23:59:59'),
        //   ],
        // ];
        // if (vars.formData.notSales) {
        //   filter.push('and');
        //   filter.push(['non_invoice', '>', 0]);
        // }
        // vars.grid['status'].filter(filter);
        try{
          dataSource.clear()
          vars.grid['status'].beginCustomLoading('데이터를 집계중입니다')
          const params = methods.getParams(); 
          if (vars.formData.notSales) {
            params.filter.push('and');
            params.filter.push(['non_invoice', '>', 0]);
          }
          const { data } = await shipmentReleaseItemWithClient.load(params);

          let i = 1;
          data.forEach((v) => {
            v.grid_id = i++
            dataSource.insert(v);
          });
        }catch(ex){
          console.error(ex)
        }finally{
          vars.grid['status'].endCustomLoading()
        }
        vars.grid['status'].refresh() 
      },
      async onExporting(evt) {
        shipmentReleaseItemWithClient.exportData(evt.component, '출고현황', `출고현황_${Date.now()}.xlsx`);
        evt.cancel = true;
      },
    };

    return { vars, methods, shipmentReleaseItemWithClient, dataSource };
  },
};
</script>
