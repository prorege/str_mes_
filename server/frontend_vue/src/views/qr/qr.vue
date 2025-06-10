<script setup>
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar'
import DxForm, {DxGroupItem, DxSimpleItem, DxLabel} from 'devextreme-vue/form'
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup'
import { DxNumberBox } from 'devextreme-vue/number-box'
import { DxScrollView } from 'devextreme-vue/scroll-view'
import { 
  DxDataGrid, DxColumn, DxPaging, 
  DxFilterRow, DxColumnChooser, DxSelection, 
  DxSorting, DxToolbar as DxGridToolbar 
} from 'devextreme-vue/data-grid'

import authService from '@/auth'
import { purchaseReceivingItem } from '@/data-source/purchase'
import { performanceItem1 } from '@/data-source/produce'
import { shipmentReleaseItem } from '@/data-source/shipment'
import { baseClient } from '@/data-source/base'
import stateStore from '@/utils/state-store'
import { notifyError } from '@/utils/notify'
import printDocument from '@/utils/print-document'

import moment from 'moment'
import QRCode from 'qrcode'
import { reactive, ref, nextTick } from 'vue'

const companyKeyFilter = {name: 'fk_company_id', op: 'eq', val: authService.getCompanyId()}
purchaseReceivingItem.defaultFilters = [
  {name: 'item', op: 'has', val: { name: 'lot_check', op: 'eq', val: true }}, 
  {name: 'receiving', op: 'has', val: companyKeyFilter}
]
performanceItem1.defaultFilters = [
  {name: 'item', op: 'has', val: { name: 'lot_check', op: 'eq', val: true }}, 
  {name: 'performance_registration', op: 'has', val: companyKeyFilter}
]
shipmentReleaseItem.defaultFilters = [
  {name: 'item', op: 'has', val: { name: 'lot_check', op: 'eq', val: true }}
]

const components = {}
const recvType = ref('생산입고')
const search = reactive({
  startdate: moment().startOf('month').toDate(), 
  enddate: moment().endOf('month').toDate(),
  type: '생산입고'
})

const printDialog = reactive({ show: false, data: [], paper: '20x20mm', label: '2x2' })

function initialized (evt, key) {
  components[key] = evt.component
  stateStore.bind(key, evt.component)

  switch (key) {
    case 'qr-produce': {
      loadGrid()
      break
    }
    case 'qr-purchase': {
      components['qr-purchase'].filter([
        ['receiving.receiving_date', '>=', moment(search.startdate).format('YYYY-MM-DD 00:00:00')],
        ['receiving.receiving_date', '<=', moment(search.enddate).format('YYYY-MM-DD 23:59:59')],
      ]);
      break
    }
    case 'qr-release': {
      components['qr-release'].filter([
        ['release.release_date', '>=', moment(search.startdate).format('YYYY-MM-DD 00:00:00')],
        ['release.release_date', '<=', moment(search.enddate).format('YYYY-MM-DD 23:59:59')],
      ]);
      break
    }
  }
}

function loadGrid () {
  recvType.value = search.type
  
  if (search.type === '생산입고') {
    components['qr-produce'].filter([
      ['performance_registration.target_date', '>=', moment(search.startdate).format('YYYY-MM-DD 00:00:00')],
      ['performance_registration.target_date', '<=', moment(search.enddate).format('YYYY-MM-DD 23:59:59')],
    ]);

    nextTick(() => {
      components['qr-produce'].repaint()
    })
  }
  else if (search.type === '구매입고') {
    components['qr-purchase'].filter([
      ['receiving.receiving_date', '>=', moment(search.startdate).format('YYYY-MM-DD 00:00:00')],
      ['receiving.receiving_date', '<=', moment(search.enddate).format('YYYY-MM-DD 23:59:59')],
    ]);

    nextTick(() => {
      components['qr-purchase'].repaint()
    })
  }
  else if (search.type === '출고') {
    components['qr-release'].filter([
      ['release.release_date', '>=', moment(search.startdate).format('YYYY-MM-DD 00:00:00')],
      ['release.release_date', '<=', moment(search.enddate).format('YYYY-MM-DD 23:59:59')],
    ]);

    nextTick(() => {
      components['qr-release'].repaint()
    })
  }
}

function getQrImage (...codes) {
  const code = codes.join('|')
  return new Promise((resolve, reject) => {
    QRCode.toDataURL(code, {margin: 0}, (err, url) => {
      if (err) return reject(err)
      resolve(url)
    })
  })
}

async function printSelectProduceItem () {
  const rows = components['qr-produce'].getSelectedRowsData()
  if (!rows.length) return notifyError('선택된 항목이 없습니다')
  printDialog.data = []

  // 생산입고 : 입고번호 + 품목코드 + 양품수량 
  // 2023-11-20: 작지번호 + 입고번호 + 생산주차 + 품목코드 + 양품수량 
  for (const row of rows) {
    printDialog.data.push({
      number: row.performance_registration.number,
      item_code: row.item.item_code,
      name: row.item.item_name,
      quantity: row.production_receiving_quantity,
      qr: await getQrImage(
        row.work_order_number,
        row.performance_registration.number, 
        row.lot,
        row.item.item_code,
        goodQuantity(row)) 
    })
  }
  printDialog.show = true
}

async function printSelectPurchaseItem () {
  const rows = components['qr-purchase'].getSelectedRowsData()
  if (!rows.length) return notifyError('선택된 항목이 없습니다')
  printDialog.data = []
  const loadedClient = {}

  // 구매입고 : 품목코드|업체약칭|입고번호 (변경전: 입고일자 + 공급업체 + 품명 + 규격)
  for (const row of rows) {
    if (!loadedClient[row.receiving.client_company]) {
      const {data: client} = await baseClient.load({filter: ['name', '=', row.receiving.client_company]})
      if (client.length) {
        loadedClient[row.receiving.client_company] = client[0].alias
      }
    }

    console.log([row.item.item_name,
        loadedClient[row.receiving.client_company],
        row.receiving.receiving_number].join('|'))
    
    printDialog.data.push({
      number: row.receiving.receiving_number,
      item_code: row.item.item_code,
      name: row.item.item_name,
      quantity: row.receiving_quantity,
      qr: await getQrImage(
        row.item.item_code,
        loadedClient[row.receiving.client_company],
        row.receiving.receiving_number
      ),
    })
  }
  printDialog.show = true
}

async function printSelectReleaseItem () {
  const rows = components['qr-release'].getSelectedRowsData()
  if (!rows.length) return notifyError('선택된 항목이 없습니다')
  printDialog.data = []

  // 출고 : 출고일자 + 고객업체 + 품명 + 규격 + 프로젝트번호
  //       20230607|영성테크놀로지|MS-406CU-GH(#22)||
  for (const row of rows) {
    printDialog.data.push({
      number: row.release_number,
      item_code: row.item.item_code,
      name: row.item.item_name,
      quantity: row.release_quantity,
      qr: await getQrImage(
        moment(row.release.release_date).format('YYYYMMDD'),
        row.release.client_company,
        row.item.item_name,
        row.item.standard,
        row.project_management.project_number),
    })
  }
  printDialog.show = true
}

function printQRLabel () {
  const params = {paper: printDialog.paper, label: printDialog.label, items: []}
  for (const item of printDialog.data) {
    for (let i=0; i<item.quantity; i++) {
      params.items.push(item)
    }
  }
  printDocument('qr', params)
}

function closePrintPopup () {
  printDialog.show = false
}

function workOrderQuantity(rowData) {
  if (!rowData.work_order_quantity) return '0';
  return rowData.work_order_quantity;
}
function productionReceivingQuantity(rowData) {
  if (!rowData.production_receiving_quantity) return '0';
  return rowData.production_receiving_quantity;
}
function checkQuantity(rowData) {
  if (!rowData.check_quantity) return '0';
  return rowData.check_quantity;
}
function badQuantity(rowData) {
  if (!rowData.bad_quantity) return '0';
  return rowData.bad_quantity;
}
function goodQuantity(rowData) {
  if (!rowData.good_quantity) return '0';
  return rowData.good_quantity;
}
function availableStock(rowData) {
  if (!rowData.basic_stock) return '0';
  return rowData.basic_stock.available_stock;
}
function currentStock(rowData) {
  if (!rowData.basic_stock) return '0';
  return rowData.basic_stock.current_stock;
}
function calcSupplyPrice(rowData) {
  let supply_price = 0;
  if (rowData.release_quantity && rowData.unit_price) {
    supply_price = rowData.release_quantity * rowData.unit_price;
  }
  rowData.supply_price = supply_price;
  return supply_price;
}
</script>

<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings">
        
        <div class="content-header">
          <dx-toolbar>
            <dx-item location="before">
              <div class="content-title">QR라벨관리</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div>
          <dx-form :form-data="search">
            <dx-group-item :col-count="5">
              <dx-simple-item data-field="startdate" editor-type="dxDateBox">
                <dx-label text="입고일자" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item data-field="enddate" editor-type="dxDateBox">
                <dx-label text="~" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item 
                data-field="type" 
                editor-type="dxSelectBox"
                :editor-options="{
                  dataSource: ['생산입고', '구매입고', '출고']
                }">
                <dx-label text="업무구분" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                item-type="button"
                horizontal-alignment="left"
                :button-options="{ text: '검색', icon: 'search', type: 'normal', onClick: loadGrid, }"
              />
            </dx-group-item>
          </dx-form>
        </div>

      </div>

      <div class="dx-card responsive-paddings mt-1" v-show="recvType === '생산입고'">
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
          :data-source="performanceItem1"
          @initialized="evt => initialized(evt, 'qr-produce')"
        >
          <dx-grid-toolbar>
            <dx-item text="생산입고품목" location="before" />
            <dx-item widget="dxButton" location="after" 
              :options="{ text: '선택된 항목 출력', icon: 'print', type: 'normal', onClick: printSelectProduceItem }"
            />
            <dx-item name="columnChooserButton" />
          </dx-grid-toolbar>

          <dx-column caption="생산입고번호" data-field="performance_registration.number" :filter-operations="['contains', '=']" />
          <dx-column caption="입고일자" data-field="performance_registration.target_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
          <dx-column caption="고객업체" data-field="client_company" />
          <dx-column caption="작지번호" data-field="work_order_number" />
          <dx-column caption="작지일자" data-field="work_order.target_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="담당자" data-field="performance_registration.manager" />
          <dx-column caption="품목코드" data-field="item.item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="작업지시수량" data-field="work_order_quantity" data-type="number" format="fixedPoint" :calculate-display-value="workOrderQuantity" />
          <dx-column caption="생산입고수량" data-field="production_receiving_quantity" data-type="number" format="fixedPoint" :calculate-display-value="productionReceivingQuantity" />
          <dx-column caption="검수수량" data-field="check_quantity" data-type="number" format="fixedPoint" :calculate-display-value="checkQuantity" />
          <dx-column caption="불량수량" data-field="bad_quantity" data-type="number" format="fixedPoint" :calculate-display-value="badQuantity" />
          <dx-column caption="양품수량" data-field="good_quantity" data-type="number" format="fixedPoint" :calculate-display-value="goodQuantity" />
          <dx-column caption="검수완료" data-field="check_yn" data-type="boolean" />
          <dx-column caption="입고창고" data-field="warehouse.wh_name" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :calculate-display-value="availableStock" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :calculate-display-value="currentStock" />
          <dx-column caption="품목대분류" data-field="item.main_category" />
          <dx-column caption="품목중분류" data-field="item.middle_category" />
          <dx-column caption="품목소분류" data-field="item.sub_category" />
          <dx-column caption="자산구분" data-field="item.asset_type" />
          <dx-column caption="안전재고" data-field="item.safety_stock" />
          <dx-column caption="프로젝트번호" data-field="project_management.project_number" />
          <dx-column caption="생산주차" data-field="lot" />

          <dx-sorting mode="single" />
          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-column-chooser mode="select" :enabled="true" />
          <dx-selection select-all-mode="page" show-check-boxes-mode="always" mode="multiple" />
        </dx-data-grid>
      </div>

      <div class="dx-card responsive-paddings mt-1" v-show="recvType === '구매입고'">
        <dx-data-grid
          height="calc(100vh - 230px)"
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :data-source="purchaseReceivingItem"
          @initialized="evt => initialized(evt, 'qr-purchase')"
        >
          <dx-grid-toolbar>
            <dx-item text="구매입고품목" location="before" />
            <dx-item widget="dxButton" location="after" 
              :options="{ text: '선택된 항목 출력', icon: 'print', type: 'normal', onClick: printSelectPurchaseItem }"
            />
            <dx-item name="columnChooserButton" />
          </dx-grid-toolbar>
          
          <dx-column caption="입고번호" data-field="receiving.receiving_number" :filter-operations="['contains', '=']" />
          <dx-column caption="입고일자" data-field="receiving.receiving_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
          <dx-column caption="공급업체" data-field="receiving.client_company" />
          <dx-column caption="입고부서" data-field="receiving.receiving_department" />
          <dx-column caption="입고담당자" data-field="receiving.receiving_manager" />
          <dx-column caption="입고구분" data-field="receiving.receiving_type" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="발주수량" data-field="order_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="입고수량" data-field="receiving_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="단가" data-field="unit_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="공급가" data-field="supply_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
          <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="품목대분류" data-field="item.main_category" />
          <dx-column caption="품목중분류" data-field="item.middle_category" />
          <dx-column caption="품목소분류" data-field="item.sub_category" />
          <dx-column caption="발주번호" data-field="order_number" />
          <dx-column caption="공급사품번" data-field="client_item_number" />
          <dx-column caption="품목설명" data-field="item.item_detail" />
          <dx-column caption="참고사항" data-field="note" />
          <dx-column caption="종결" data-field="closing_yn" />
          <dx-column caption="LOT번호" data-field="lot_number" />
          <dx-column caption="공급처 LOT번호" data-field="supplier_lot_number" />

          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-column-chooser mode="select" :enabled="true" />
          <dx-selection select-all-mode="page" show-check-boxes-mode="always" mode="multiple" />
        </dx-data-grid>
      </div>

      <div class="dx-card responsive-paddings mt-1" v-show="recvType === '출고'">
        <dx-data-grid
          height="calc(100vh - 230px)"
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :data-source="shipmentReleaseItem"
          @initialized="evt => initialized(evt, 'qr-release')"
        >
          <dx-grid-toolbar>
            <dx-item text="출고품목" location="before" />
            <dx-item widget="dxButton" location="after" 
              :options="{ text: '선택된 항목 출력', icon: 'print', type: 'normal', onClick: printSelectReleaseItem }"
            />
            <dx-item name="columnChooserButton" />
          </dx-grid-toolbar>
          
          <dx-column caption="출고번호" data-field="release.release_number" :filter-operations="['contains', '=']" />
          <dx-column caption="출고일자" data-field="release.release_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
          <dx-column caption="고객업체" data-field="release.client_company" />
          <dx-column caption="견적부서" data-field="release.release_department" />
          <dx-column caption="출고담당자" data-field="release.release_manager" />
          <dx-column caption="출고구분" data-field="release.release_type" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="수주수량" data-field="order_item.order_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="출고수량" data-field="release_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="단가" data-field="unit_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="공급가" data-field="supply_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :calculate-cell-value="calcSupplyPrice" />
          <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="품목대분류" data-field="item.main_category" />
          <dx-column caption="품목중분류" data-field="item.middle_category" />
          <dx-column caption="품목소분류" data-field="item.sub_category" />
          <dx-column caption="수주번호" data-field="order_number" />
          <dx-column caption="고객사품번" data-field="client_item_number" />
          <dx-column caption="품목설명" data-field="item.item_detail" />
          <dx-column caption="참고사항" data-field="note" />
          <dx-column caption="프로젝트번호" data-field="project_management.project_number" />
          <dx-column caption="종결" data-field="closing_yn" />

          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-column-chooser mode="select" :enabled="true" />
          <dx-selection select-all-mode="page" show-check-boxes-mode="always" mode="multiple" />
        </dx-data-grid>
      </div>
    </div>

    <dx-popup
      content-template="popup-content"  
      v-model:visible="printDialog.show"
      :width="680"
      :height="500"
      :show-title="false"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => initialized(evt, 'qr-popup')"
    >
      <dx-toolbar-item location="after" widget="dxButton" :options="{icon: 'close', text: '닫기', onClick: closePrintPopup}" />
      <dx-toolbar-item location="after" widget="dxButton" :options="{icon: 'print', text: '확인', onClick: printQRLabel}" />

      <template #popup-content>
        <dx-form>
          <dx-group-item>
          </dx-group-item>
        </dx-form>
        <dx-scroll-view width="100%" height="100%">
          <div class="qr-list">
            <div class="qr-list-item" v-for="row in printDialog.data" :key="row.number">
              <div class="qr-list-img"><img :src="row.qr" /></div>
              <div class="qr-list-name">{{row.name}}</div>
              <div class="qr-list-label">인쇄수량</div>
              <div class="qr-list-quantity">
                <dx-number-box v-model:value="row.quantity" :min="1" />
              </div>
            </div>
          </div>
        </dx-scroll-view>
      </template>
    </dx-popup>

  </div>
</template>

<style lang="scss" scoped>
.qr-popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  .qr-popup-title {
    font-size: 18px;
  }
  .qr-popup-fn .dx-button:not(:last-child) {
    margin: 0 10px;
  }
}
.qr-list {
  margin: -4px 0;
  .qr-list-item {
    display: flex;
    align-items: center;
    border: 1px solid #c0c0c0;
    border-radius: 6px;
    overflow: hidden;
    margin: 4px 0;
  }
  .qr-list-img {
    flex: 0 0 80px;
    font-size: 0;
    img { width: 100%; }
  }
  .qr-list-name {
    flex: 1 1 auto;
    padding: 0 20px;
    font-size: 16px;
  }
  .qr-list-label {
    flex: 0 0 52px;
  }
  .qr-list-quantity {
    flex: 0 0 100px;
    padding: 0 10px;
  }
}
</style>