<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">수주현황(관리자)</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div>
          <div class="search-status">
            <span class="search-title">수주일자</span>
            <dx-date-box v-model:value="vars.formData.startDate" />

            <span class="search-bar">~</span>
            <dx-date-box v-model:value="vars.formData.endDate" />

            <span class="search-tab"></span>
            <SearchButtonGroup @change="({startDate, endDate}) => { vars.formData.startDate = startDate; vars.formData.endDate = endDate; }" />

            <span class="search-tab"></span>
            <dx-check-box text="출고요청 미확인" v-model:value="vars.formData.notRequestConfirmed" />

            <span class="search-tab"></span>
            <dx-button text="검색" icon="search" @click="methods.searchDateRange()" />
          </div>
        </div>

      </div>

      <div class="dx-card responsive-paddings mt-1">
        <dx-data-grid
          height="calc(100vh - 230px)"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :focused-row-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :data-source="shipmentOrderItem"
          :on-initialized="evt => methods.onGridInitialized(evt, 'status')"
          @exporting="methods.onExporting"
          @row-dbl-click="methods.goOrderDetail"
        >
          <dx-column caption="수주확정" data-field="order.confirmed" data-type="boolean" />
          <dx-column caption="출고요청" data-field="release_request" data-type="boolean" />
          <dx-column caption="출고요청수량" data-field="release_request_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="출고요청일자" data-field="release_request_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="출고요청확인" data-field="release_request_confirm" data-type="boolean" />
          <dx-column caption="창고확인" data-field="warehouse_confirm" data-type="boolean" />
          <dx-column caption="출고수량" data-field="release_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="출고번호" data-field="order.release_number" />
          <dx-column caption="수주번호" data-field="order.order_number" :filter-operations="['contains', '=']" />
          <dx-column caption="수주일자"  data-field="order.order_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
          <dx-column caption="고객업체" data-field="order.client_company" />
          <dx-column caption="수주부서" data-field="order.order_department" />
          <dx-column caption="수주담당자" data-field="order.order_manager" />
          <dx-column caption="수주구분" data-field="order.order_type" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="수주수량" data-field="order_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="할당수량" data-field="assign_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="단가" data-field="unit_price" :format="{ type: 'fixedPoint', precision: 2 }" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="공급가" data-field="supply_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :calculate-cell-value="methods.calcSupplyPrice" />
          <dx-column caption="매입가" data-field="item.purchase_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
          <dx-column caption="마진율" data-field="" :calculate-cell-value="methods.calcMarginRate" />
          <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="미출고" data-field="not_shipped" data-type="number" format="fixedPoint" />
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :calculate-display-value="methods.availableStock" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :calculate-display-value="methods.currentStock" />
          <dx-column caption="품목대분류" data-field="item.main_category" />
          <dx-column caption="품목중분류" data-field="item.middle_category" />
          <dx-column caption="품목소분류" data-field="item.sub_category" />
          <dx-column caption="자산구분" data-field="item.asset_type" />
          <dx-column caption="안전재고" data-field="item.safety_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="프로젝트번호" data-field="project_management.project_number" />

          <dx-sorting mode="single" />
          <dx-export :enabled="true" />
          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-column-chooser mode="select" :enabled="true" />
        </dx-data-grid>
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
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxColumnChooser } from 'devextreme-vue/data-grid';

import stateStore from '@/utils/state-store';
import { shipmentOrderItem } from '../../data-source/shipment';
import SearchButtonGroup from '../../components/search-button-group.vue';

export default {
  components: {
    DxButton,
    DxCheckBox,
    DxDateBox,
    DxToolbar,
    DxItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem,
    DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxColumnChooser,
    SearchButtonGroup
  },
  setup() {
    const router = useRouter();
    const vars = {};
    vars.grid = {};
    vars.formData = reactive({
      notRequestConfirmed: false,
      startDate: new Date(),
      endDate: new Date(),
    });
    vars.formData.startDate.setDate(vars.formData.startDate.getDate() - 7);

    const methods = {
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`shipment-order-${key}`, evt.component);

        methods.initSorting();
        methods.searchDateRange();
      },
      initSorting() {
        const columns = vars.grid['status'].getVisibleColumns();
        const col = columns.filter(item => item.sortOrder);
        if (col.length == 0) {
          const defaultName = 'order.order_date';
          const defaultSort = columns.filter(item => item.name == defaultName);
          if (defaultSort.length > 0) {
            vars.grid['status'].columnOption(defaultSort[0].index,'sortOrder','desc');
          }
        }
      },
      goOrderDetail({ data }) {
        router.push({ path: `/shipment/order/${data.order.id}` });
      },
      calcSupplyPrice(rowData) {
        let supply_price = 0;
        if (rowData.order_quantity && rowData.unit_price) {
          supply_price = rowData.order_quantity * rowData.unit_price;
        }
        rowData.supply_price = supply_price;
        return supply_price;
      },
      calcMarginRate(rowData) {
        return ((rowData.unit_price - rowData.item.purchase_price) / rowData.item.purchase_price) * 100;
      },
      availableStock(rowData) {
        if (!rowData.basic_stock) { return '0'; }
        return rowData.basic_stock.available_stock;
      },
      currentStock(rowData) {
        if (!rowData.basic_stock) { return '0'; }
        return rowData.basic_stock.current_stock;
      },
      async searchDateRange() {
        if (vars.formData.startDate > vars.formData.endDate) {
          await alert('조회 일자가 잘못 되었습니다', '조회');
          return;
        }

        let filter = [
          [
            'order.order_date',
            '>=',
            moment(vars.formData.startDate).startOf('day').format('YYYY-MM-DD 00:00:00'),
          ],
          'and',
          [
            'order.order_date',
            '<=',
            moment(vars.formData.endDate).endOf('day').format('YYYY-MM-DD 23:59:59'),
          ],
        ];
        if (vars.formData.notRequestConfirmed) {
          filter.push('and');
          filter.push(['release_request_confirm', '=', 0]);
        }
        vars.grid['status'].filter(filter);
      },
      async onExporting (evt) {
        shipmentOrderItem.exportData(evt.component, '수주현황', `수주현황_${Date.now()}.xlsx`)
        evt.cancel = true
      }
    };

    return { vars, methods, shipmentOrderItem };
  },
};
</script>
