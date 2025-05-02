<script setup>
import {ref} from 'vue'
import {
  DxDataGrid,
  DxColumn,
  DxPaging,
  DxFilterRow,
  DxColumnChooser,
  DxExport,
} from 'devextreme-vue/data-grid'
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar'
import { DxDateBox } from 'devextreme-vue/date-box'
import DxButton from 'devextreme-vue/button'
import moment from 'moment'
import SearchButtonGroup from '@/components/search-button-group.vue'

import {
  getSalesOrderItem,
} from '@/data-source/export'
import { useRouter } from 'vue-router'
import authService from '@/auth'

const ready = ref(false)
const grid = ref(null)
const router = useRouter()
const dataSource = getSalesOrderItem()
const formData = ref({
  startDate: new Date(),
  endDate: new Date(),
})

ready.value = true

function init (component) {
  grid.value = component
  searchDateRange()
}

function getParams (key) {
  return [
    [
      key, '>=',
      moment(formData.value.startDate)
        .startOf('day')
        .format('YYYY-MM-DD 00:00:00'),
    ],
    'and',
    [
      key, '<=',
      moment(formData.value.endDate)
        .endOf('day')
        .format('YYYY-MM-DD 23:59:59'),
    ],
  ]
}

async function searchDateRange () {
  if (formData.value.startDate > formData.value.endDate) {
    await alert('조회 일자가 잘못 되었습니다', '조회');
    return;
  }

  const params = getParams('export_order.order_date')
  grid.value.filter(params)
}

function onRowDblClick ({data}) {
  if (!data.export_order) return
  router.push({ path: `/export/sales-order/${data.export_order.id}` });
}

function getStockValue (row, key) {
  if (!row.basic_stock) return '0'
  return row.basic_stock[key] || '0'
}

function calcSupplyPrice(rowData) {
  let supply_price = 0;
  if (rowData.order_quantity && rowData.unit_price) {
    supply_price = rowData.order_quantity * rowData.unit_price;
  }
  rowData.supply_price = supply_price;
  return supply_price;
}

</script>

<template>
    <div class="content-block" v-if="ready">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">Sales Order Status</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div>
          <div class="search-status">
            <span class="search-title">Order Date</span>
            <dx-date-box v-model:value="formData.startDate" />
            
            <span class="search-bar">~</span>
            <dx-date-box v-model:value="formData.endDate" />
            
            <span class="search-tab"></span>
            <SearchButtonGroup @change="({startDate, endDate}) => { formData.startDate = startDate; formData.endDate = endDate; }" />
            
              <span class="search-tab"></span>
            <dx-button text="검색" icon="search" @click="searchDateRange()" />
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
          :data-source="dataSource"
          @initialized="({component}) => init(component)"
          @row-dbl-click="onRowDblClick"
        >
          <dx-column caption="Order No" data-field="export_order.order_number" :filter-operations="['contains', '=']" />
          <dx-column caption="Order Date" data-field="export_order.order_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" :sort-index="0" sort-order="desc" />
          <dx-column caption="Item Code" data-field="item_code" />
          <dx-column caption="Itme Name" data-field="item.item_name" />
          <dx-column caption="Sub Name" data-field="item.item_standard" />
          <dx-column caption="Qty" data-field="order_quantity" data-type="number" format="fixedPoint" :allow-sorting="false" />
          <dx-column caption="Export Price" data-field="unit_price" data-type="number" :format="{ type: 'fixedPoint', precision: 4 }" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="Amount" data-field="supply_price" data-type="number" :format="{ type: 'fixedPoint', precision: 4 }" :calculate-cell-value="calcSupplyPrice" />
          <dx-column caption="할당수량" data-field="assign_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="미선적량" data-field="not_shipped" data-type="number" format="fixedPoint" />
          <dx-column caption="Req Date" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="Con Date" data-field="contact_delivery_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="LOT NO(생산주차)" data-field="lot" />
          <dx-column caption="출고창고" data-field="warehouse.wh_name" :allow-sorting="false" />
          <dx-column caption="Description" data-field="item.item_detail" :allow-editing="false" />
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :allow-editing="false" :allow-sorting="false" :calculate-display-value="(row) => getStockValue(row, 'available_stock')" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :allow-editing="false" :allow-sorting="false" :calculate-display-value="(row) => getStockValue(row, 'current_stock')" />
          <dx-column caption="수주아이디" data-field="fk_export_sales_order_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />
          <dx-column caption="창고코드" data-field="warehouse_code" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />

          <dx-export :enabled="true" />
          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-column-chooser mode="select" :enabled="true" />
        </dx-data-grid>
      </div>
    </div>
</template>