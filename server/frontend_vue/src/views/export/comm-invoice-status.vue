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
  getCommInvoiceItem,
} from '@/data-source/export'
import { useRouter } from 'vue-router'
import authService from '@/auth'

const ready = ref(false)
const grid = ref(null)
const router = useRouter()
const dataSource = getCommInvoiceItem()
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

  const params = getParams('export_comm_invoice.invoice_date')
  grid.value.filter(params)
}

function onRowDblClick ({data}) {
  if (!data.export_comm_invoice) return
  router.push({ path: `/export/comm-invoice/${data.export_comm_invoice.id}` });
}

function calcSupplyPrice(rowData) {
  let supply_price = 0;
  if (rowData.invoice_quantity && rowData.unit_price) {
    supply_price = rowData.invoice_quantity * rowData.unit_price;
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
              <div class="content-title">Comm Invoice Status</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div>
          <div class="search-status">
            <span class="search-title">Invoice Date</span>
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
          <dx-column caption="Invoice No" data-field="export_comm_invoice.invoice_number" :filter-operations="['contains', '=']" />
          <dx-column caption="Invoice Date" data-field="export_comm_invoice.invoice_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" :sort-index="0" sort-order="desc" />
          <dx-column caption="Item Code" data-field="item_code" />
          <dx-column caption="Itme Name" data-field="item.item_name" />
          <dx-column caption="Sub Name" data-field="item.item_standard" />
          <dx-column caption="Qty" data-field="export_sales_order_item.order_quantity" format="fixedPoint" :allow-sorting="false" />
          <dx-column caption="출고수량" data-field="invoice_quantity" format="fixedPoint" />
          <dx-column caption="Export Price" data-field="unit_price" data-type="number" :format="{ type: 'fixedPoint', precision: 4 }" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="Amount" data-field="supply_price" data-type="number" :format="{ type: 'fixedPoint', precision: 4 }" :calculate-cell-value="calcSupplyPrice" />
          <dx-column caption="Req Date" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="Con Date" data-field="contact_delivery_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="LOT NO(생산주차)" data-field="lot" />
          <dx-column caption="출고창고" data-field="warehouse.wh_name" :allow-sorting="false" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :allow-sorting="false" />
          <dx-column caption="Order No" data-field="order_number" />
          <dx-column caption="Description" data-field="item.item_detail" />
          <dx-column caption="출고아이디" data-field="fk_export_comm_invoice_id" :visible="false" :show-in-column-chooser="false" />
          <dx-column caption="수주 품목 아이디" data-field="fk_export_sales_order_item_id" :visible="false" :show-in-column-chooser="false" />
          <dx-column caption="창고코드" data-field="warehouse_code" :allow-editing="false" />

          <dx-export :enabled="true" />
          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-column-chooser mode="select" :enabled="true" />
        </dx-data-grid>
      </div>
    </div>
</template>