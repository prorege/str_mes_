<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">견적현황</div>
            </dx-item>
          </dx-toolbar>
        </div>
        <div>
          <div class="search-status">
            <span class="search-title">견적일자</span>
            <dx-date-box v-model:value="vars.formData.startDate" />
            <span class="search-bar">~</span>
            <dx-date-box v-model:value="vars.formData.endDate" />
            <span class="search-tab"></span>
            <SearchButtonGroup
              @change="
                ({ startDate, endDate }) => {
                  vars.formData.startDate = startDate;
                  vars.formData.endDate = endDate;
                }
              "
            />
            <span class="search-tab"></span>
            <dx-check-box text="미확정" v-model:value="vars.formData.notConfirmed" />
            
            <span class="search-tab"></span>
            <dx-check-box text="미수주" v-model:value="vars.formData.notOrdered" />
            
            <span class="search-tab"></span>
            <dx-button text="검색" icon="search" @click="methods.searchDateRange()" />
          </div>
        </div>
      </div>
      <div class="dx-card responsive-paddings mt-1">
        <dx-data-grid
          height="calc(100vh - 230px)"
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :focused-row-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :data-source="shipmentQuoteItem"
          :filter-sync-enabled="true"
          :on-initialized="(evt) => methods.onGridInitialized(evt, 'status')"
          @row-dbl-click="methods.goQuoteDetail"
          @exporting="methods.onExporting"
        >
          <dx-export :enabled="true" />
          <dx-column caption="견적확정" data-field="quote.confirmed" data-type="boolean" />
          <dx-column caption="견적번호" data-field="quote.quote_number" :filter-operations="['contains', '=']" />
          <dx-column caption="수주번호" data-field="quote.order_number" />
          <dx-column caption="견적일자" data-field="quote.quote_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
          <dx-column caption="고객업체" data-field="quote.client_company" />
          <dx-column caption="견적부서" data-field="quote.quote_department" />
          <dx-column caption="견적담당자" data-field="quote.quote_manager" />
          <dx-column caption="견적수량" data-field="quote_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="견적구분" data-field="quote.quote_type" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="단가" data-field="unit_price" data-type="number" format="currency" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="공급가" data-field="supply_price" data-type="number" format="currency" :calculate-cell-value="methods.calcSupplyPrice" />
          <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="미수주수량" data-field="not_ordered" data-type="number" format="fixedPoint" />
          <dx-column caption="가용재고" data-field="available_stock" data-type="number" format="fixedPoint" :calculate-display-value="methods.availableStock" />
          <dx-column caption="현재고" data-field="current_stock" data-type="number" format="fixedPoint" :calculate-display-value="methods.currentStock" />
          <dx-column caption="품목대분류" data-field="item.main_category" />
          <dx-column caption="품목중분류" data-field="item.middle_category" />
          <dx-column caption="품목소분류" data-field="item.sub_category" />
          <dx-column caption="자산구분" data-field="item.asset_type" />
          <dx-column caption="안전재고" data-field="item.safety_stock" data-type="number" format="fixedPoint" />

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
import {
  DxForm,
  DxLabel,
  DxGroupItem,
  DxSimpleItem,
} from 'devextreme-vue/form';
import {
  DxDataGrid,
  DxColumn,
  DxExport,
  DxPaging,
  DxSorting,
  DxFilterRow,
  DxColumnChooser,
} from 'devextreme-vue/data-grid';

import stateStore from '@/utils/state-store';
import { shipmentQuoteItem } from '../../data-source/shipment';
import SearchButtonGroup from '../../components/search-button-group.vue';

export default {
  components: {
    DxButton,
    DxCheckBox,
    DxDateBox,
    DxToolbar,
    DxItem,
    DxForm,
    DxLabel,
    DxGroupItem,
    DxSimpleItem,
    DxDataGrid,
    DxColumn,
    DxExport,
    DxPaging,
    DxSorting,
    DxFilterRow,
    DxColumnChooser,
    SearchButtonGroup,
  },
  setup() {
    const router = useRouter();
    const vars = {};
    vars.grid = {};
    vars.formData = reactive({
      notConfirmed: false,
      notOrdered: false,
      startDate: new Date(),
      endDate: new Date(),
    });
    // vars.formData.startDate.setDate(vars.formData.startDate.getDate() - 7);

    const methods = {
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`shipment-quote-${key}`, evt.component);

        methods.initSorting();
        methods.searchDateRange();
      },
      initSorting() {
        const columns = vars.grid['status'].getVisibleColumns();
        const col = columns.filter((item) => item.sortOrder);
        if (col.length == 0) {
          const defaultName = 'quote.quote_date';
          const defaultSort = columns.filter(
            (item) => item.name == defaultName
          );
          if (defaultSort.length > 0) {
            vars.grid['status'].columnOption(
              defaultSort[0].index,
              'sortOrder',
              'desc'
            );
          }
        }
      },
      calcSupplyPrice(rowData) {
        let supply_price = 0;
        if (rowData.quote_quantity && rowData.unit_price) {
          supply_price = rowData.quote_quantity * rowData.unit_price;
        }
        rowData.supply_price = supply_price;
        return supply_price;
      },
      availableStock(rowData) {
        if (!rowData.basic_stock) {
          return '0';
        }
        return rowData.basic_stock.available_stock;
      },
      currentStock(rowData) {
        if (!rowData.basic_stock) {
          return '0';
        }
        return rowData.basic_stock.current_stock;
      },
      goQuoteDetail({ data }) {
        router.push({ path: `/shipment/quote/${data.quote.id}` });
      },
      async searchDateRange() {
        if (vars.formData.startDate > vars.formData.endDate) {
          await alert('조회 일자가 잘못 되었습니다', '조회');
          return;
        }

        if (!vars.grid['status']) return

        const filterValue = [
          moment(vars.formData.startDate).startOf('day').toDate(),
          moment(vars.formData.endDate).endOf('day').toDate()
        ]
        
        const filter = vars.grid['status'].option('filterValue') || []
        const dateFilter = filter.find(v => typeof v === 'object' && v[0] === 'quote.quote_date')
        if (dateFilter) dateFilter[2] = filterValue
        else filter.push(['quote.quote_date', 'between', filterValue])
        vars.grid['status'].option('filterValue', filter)

        if (vars.formData.notConfirmed) {
          filter.push('and');
          filter.push(['quote.confirmed', '=', 0]);
        }
        else {
          const index = filter.findIndex(v => typeof v === 'object' && v[0] === 'quote.confirmed')
          if (index >= 0) console.info(`remove filter: ${filter.splice(index - 1, 2)}`)
        }

        if (vars.formData.notOrdered) {
          filter.push('and');
          filter.push(['not_ordered', '>', 0]);
        }
        else {
          const index = filter.findIndex(v => typeof v === 'object' && v[0] === 'not_ordered')
          if (index >= 0) console.info(`remove filter: ${filter.splice(index - 1, 2)}`)
        }

        vars.grid['status'].option('filterValue', filter)
      },
      onExporting(evt) {
        shipmentQuoteItem.exportData(
          evt.component,
          '견적현황',
          `견적현황_${Date.now()}.xlsx`
        );
        evt.cancel = true;
      },
    };

    return { vars, methods, shipmentQuoteItem };
  },
};
</script>
