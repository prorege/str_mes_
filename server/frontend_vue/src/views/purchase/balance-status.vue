<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">매입잔액장</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div v-if="commonInit">
          <div class="search-status">
            <span class="search-title">일자</span>
            <dx-date-box v-model:value="formData.startDate" />
            <span class="search-bar">~</span>
            <dx-date-box v-model:value="formData.endDate" />

            <span class="search-tab"></span>

            <dx-button text="검색" icon="search" @click="searchDateRange()" />
          </div>
        </div>

      </div>

      <div class="dx-card responsive-paddings mt-1">
        <dx-data-grid
          key-expr="id"
          height="calc(100vh - 240px)"
          column-resizing-mode="widget"
          :data-source="dataSource.status"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="false"
          :focused-row-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          @row-dbl-click="goDetail"
          @initialized="evt => initialized(evt, 'status-list')"
          @exporting="onExporting"
        >
          <dx-column caption="업체아이디" data-field="client_id" :visible="false" />
          <dx-column caption="업체약칭" data-field="client_alias" :filter-operations="['contains', '=']" />
          <dx-column caption="업체명" data-field="client_name" :filter-operations="['contains', '=']" />
          <dx-column caption="당사담당자" data-field="client_manager" :filter-operations="['contains', '=']" />
          <dx-column caption="이월 미지급금" data-field="past_account_receivable"  data-type="number" format="currency" />
          <dx-column caption="매입" data-field="purchase_price"  data-type="number" format="currency" />
          <dx-column caption="계산서 부가세" data-field="vat" data-type="number" format="currency" />
          <dx-column caption="부가세 보정" data-field="vat_adjustment" data-type="number" format="currency" />
          <dx-column caption="매입합계" data-field="total_price" data-type="number" format="currency" />
          <dx-column caption="결재" data-field="payment_price" data-type="number" format="currency" />
          <dx-column caption="미지급금 잔액" data-field="account_receivable" data-type="number" format="currency" />

          <dx-summary>
            <dx-total-item column="" show-in-column="client_manager" summary-type="sum" display-format="합계금액 :" />
            <dx-total-item column="past_account_receivable" show-in-column="past_account_receivable" summary-type="sum" value-format="currency" display-format="{0}" />
            <dx-total-item column="purchase_price" show-in-column="purchase_price" summary-type="sum" value-format="currency" display-format="{0}" />
            <dx-total-item column="vat" show-in-column="vat" summary-type="sum" value-format="currency" display-format="{0}" />
            <dx-total-item column="vat_adjustment" show-in-column="vat_adjustment" summary-type="sum" value-format="currency" display-format="{0}" />
            <dx-total-item column="total_price" show-in-column="total_price" summary-type="sum" value-format="currency" display-format="{0}" />
            <dx-total-item column="payment_price" show-in-column="payment_price" summary-type="sum" value-format="currency" display-format="{0}" />
            <dx-total-item column="account_receivable" show-in-column="account_receivable" summary-type="sum" value-format="currency" display-format="{0}" />
          </dx-summary>
          <dx-export :enabled="true" />
          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
        </dx-data-grid>
      </div>
    </div>

    <dx-popup
      v-model:visible="dialog"
      content-template="popup-content"
      title="매입원장내역"
      :width="820"
      :height="660"
      :resize-enabled="true"
      @initialized="evt => initialized(evt, 'item-popup')"
    >
      <dx-toolbar-item 
        widget="dxButton"
        toolbar="top"
        location="before"
        :options="{
          text: '매입원장 출력',
          onClick: printProductReceipt
        }"
      />
      <dx-toolbar-item 
        widget="dxButton" 
        toolbar="top" 
        location="before" 
        :options="{ 
          text: 'Excel', 
          icon: 'xlsxfile', 
          onClick: savePurchaseBalanceItem}" 
      />
      <template #popup-content>
        <dx-data-grid
          column-resizing-mode="widget"
          :data-source="dataSource.detail"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="false"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          @initialized="evt => initialized(evt, 'balance-status-detail')"
        >
          <dx-column caption="" data-field="group_id" :group-index="0" />
          <dx-column caption="일자" data-field="action_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="유형" data-field="action_type" />
          <dx-column caption="업체명" data-field="company" />
          <dx-column caption="당사담당자" data-field="manager" />
          <dx-column caption="이월미지급금" data-field="past_account_receivable" data-type="number" format="currency" />
          <dx-column caption="매입" data-field="purchase_price" data-type="number" format="currency" />
          <dx-column caption="계산서 부가세" data-field="vat" data-type="number" format="currency" />
          <dx-column caption="부가세 보정" data-field="vat_adjustment" data-type="number" format="currency" />
          <dx-column caption="매입합계" data-field="total_purchase_price" data-type="number" format="currency" />
          <dx-column caption="결재" data-field="payment_price" data-type="number" format="currency" />
          <dx-column caption="미지급금 잔액" data-field="account_receivable" data-type="number" format="currency" />

          <dx-summary :calculate-custom-summary="calculateCustomSummary">
            <dx-group-item
              :align-by-column="true"
              column="purchase_price"
              summary-type="sum"
              value-format="currency"
              display-format="매입: {0}"
            />
            <dx-group-item
              :align-by-column="true"
              column="vat"
              summary-type="sum"
              value-format="currency"
              display-format="부가세: {0}"
            />
            <dx-group-item
              :align-by-column="true"
              column="vat_adjustment"
              summary-type="sum"
              value-format="currency"
              display-format="부가세 보정: {0}"
            />
            <dx-group-item
              :align-by-column="true"
              column="total_purchase_price"
              summary-type="sum"
              value-format="currency"
              display-format="매입합계: {0}"
            />
            <dx-group-item
              :align-by-column="true"
              column="payment_price"
              summary-type="sum"
              value-format="currency"
              display-format="결재: {0}"
            />

            <dx-group-item
              :show-in-group-footer="true"
              name="accumulate_purchase_price"
              summary-type="custom"
              value-format="currency"
              show-in-column="purchase_price"
              display-format="누적매입: {0}"
            />
            <dx-group-item
              :show-in-group-footer="true"
              name="accumulate_vat"
              summary-type="custom"
              value-format="currency"
              show-in-column="vat"
              display-format="누적부가세: {0}"
            />
            <dx-group-item
              :show-in-group-footer="true"
              name="accumulate_vat_adjustment"
              summary-type="custom"
              value-format="currency"
              show-in-column="vat_adjustment"
              display-format="누적부가세보정: {0}"
            />
            <dx-group-item
              :show-in-group-footer="true"
              name="accumulate_total_purchase_price"
              summary-type="custom"
              value-format="currency"
              show-in-column="total_purchase_price"
              display-format="누적매입합계: {0}"
            />
            <dx-group-item
              :show-in-group-footer="true"
              name="accumulate_payment_price"
              summary-type="custom"
              value-format="currency"
              show-in-column="payment_price"
              display-format="누적결재: {0}"
            />

            <dx-group-item
              :show-in-group-footer="true"
              name="last_account_receivable"
              summary-type="custom"
              value-format="currency"
              show-in-column="account_receivable"
              display-format="미지급금 잔액: {0}"
            />
          </dx-summary>

          <dx-paging :page-size="10" />
        </dx-data-grid>

        <table class="summary-table" style="width: 1200px;">
          <tr>
            <td>누계</td>
            <th>이월 미지급금</th>
            <td>{{ summary.past_account_receivable.value }}</td>
            <th>매입</th>
            <td>{{ summary.purchase_price.value }}</td>
            <th>계산서 부가세</th>
            <td>{{ summary.vat.value }}</td>
            <th>매입 합계</th>
            <td>{{ summary.total_purchase_price.value }}</td>
            <th>결재 합계</th>
            <td>{{ summary.total_payment_price.value }}</td>
            <th>미지급금 잔액</th>
            <td>{{ summary.total_account_receivable.value }}</td>
          </tr>
        </table>
      </template>
    </dx-popup>
  </div>
</template>

<script setup>
import {
  DxDataGrid,
  DxColumn,
  DxPaging,
  DxSummary,
  DxGroupItem,
  DxFilterRow,
  DxExport,
  DxTotalItem
} from 'devextreme-vue/data-grid';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import DxLookup from 'devextreme-vue/select-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import DxButton from 'devextreme-vue/button';
import ApiService from '../../utils/api-service';
import { ref, reactive, computed } from 'vue';
import moment from 'moment';
import numeral from 'numeral';
import {printDocument} from '@/utils/print-document';
import { exportDataGrid } from 'devextreme/excel_exporter';
import { Workbook } from 'exceljs';
import { saveAs } from 'file-saver';
import { getClientByName } from '@/data-source/base'
import { purchaseReceivingItem, purchasePaymentItem, purchaseReceivingReturnItem, purchaseStatement } from '../../data-source/purchase';
import { groupBy, orderBy } from 'lodash'

const api = new ApiService('/api/mes/v1/purchase/balance');
const commonInit = ref(false);
const dialog = ref(false);
const startDate = new Date();
startDate.setDate(startDate.getDate() - 7);
let loadingPrintData = false

const detailItem = ref()

const formData = reactive({
  startDate: startDate,
  endDate: new Date(),
});

const components = {};

const dataSource = reactive({
  status: [],
  detail: [],
  sum: {
    past_account_receivable: 0,
    purchase_price: 0,
    vat: 0,
    total_purchase_price: 0,
    total_payment_price: 0,
    total_account_receivable: 0,
  },
});

const summary = {};
summary.past_account_receivable = computed(() => '₩' + numeral(dataSource.sum.past_account_receivable).format('0,0'));
summary.purchase_price = computed(() => '₩' + numeral(dataSource.sum.purchase_price).format('0,0'));
summary.vat = computed(() => '₩' + numeral(dataSource.sum.vat).format('0,0'));
summary.total_purchase_price = computed(() => '₩' + numeral(dataSource.sum.total_purchase_price).format('0,0'));
summary.total_payment_price = computed(() => '₩' + numeral(dataSource.sum.total_payment_price).format('0,0'));
summary.total_account_receivable = computed(() => '₩' + numeral(dataSource.sum.total_account_receivable).format('0,0'));

!(async () => {
  commonInit.value = true;
})();

function initialized(evt, key) {
  components[key] = evt.component;
}

function calculateCustomSummary(options) {
  const summaryProcesses = ['accumulate_vat_adjustment', 'accumulate_vat', 'accumulate_purchase_price', 'accumulate_total_purchase_price', 'accumulate_payment_price'];

  if (options.name === 'last_account_receivable') {
    if (options.summaryProcess === 'start') {
      options.totalValue = 0;
    } else if (options.summaryProcess === 'calculate') {
      options.totalValue = options.value.account_receivable;
    }
  } else if(summaryProcesses.includes(options.name)){
    if(options.summaryProcess === 'start'){
      options.totalArr = []
      options.totalValue = 0
    }else if(options.summaryProcess === 'calculate'){
      options.totalArr.push(options.value[options.name])
    }else if(options.summaryProcess === 'finalize'){
      options.totalValue = options.totalArr.pop();
    }
  }

}

async function goDetail({ data }) {
  detailItem.value = data
    const params = {
        start: moment(formData.startDate).format('YYYY-MM-DD 00:00:00'),
        end: moment(formData.endDate).endOf('day').format('YYYY-MM-DD 23:59:59'),
    };
    const { data: response } = await api.get(String(data.client_id), { params });

    let sumPastAccountReceivable = 0;
    let sumPurchasePrice = 0;
    let sumVat = 0;
    let sumVatAdjustment = 0;
    let sumTotalPurchasePrice = 0;
    let sumPaymentPrice = 0;
    let sumAccountReceivable = 0;
    response.objects.forEach(row => {
        sumPastAccountReceivable += parseInt(row.past_account_receivable, 10);
        sumPurchasePrice += parseInt(row.purchase_price, 10);
        sumVat += parseInt(row.vat, 10);
        sumVatAdjustment += parseInt(row.vat_adjustment, 10);
        sumTotalPurchasePrice += parseInt(row.total_purchase_price, 10) + parseInt(row.vat, 10);
        sumPaymentPrice += parseInt(row.payment_price, 10);
        sumAccountReceivable += parseInt(row.past_account_receivable, 10) + parseInt(row.total_purchase_price, 10) + parseInt(row.vat, 10) - parseInt(row.payment_price, 10);
        row.total_purchase_price = parseInt(row.purchase_price, 10) + parseInt(row.vat, 10);
        row.account_receivable = sumAccountReceivable;
        row.accumulate_purchase_price = sumPurchasePrice;
        row.accumulate_vat = sumVat;
        row.accumulate_vat_adjustment = sumVatAdjustment;
        row.accumulate_total_purchase_price = sumTotalPurchasePrice;
        row.accumulate_payment_price = sumPaymentPrice;
    });
    dataSource.detail = response.objects;
    dataSource.sum.past_account_receivable = sumPastAccountReceivable;
    dataSource.sum.purchase_price = sumPurchasePrice;
    dataSource.sum.vat = sumVat;
    dataSource.sum.total_purchase_price = sumTotalPurchasePrice;
    dataSource.sum.total_payment_price = sumPaymentPrice;
    dataSource.sum.total_account_receivable = sumAccountReceivable;
    dialog.value = true;
}

async function searchDateRange() {
  try {
    components['status-list'].beginCustomLoading('데이터를 집계중입니다')
    const params = {
      start: moment(formData.startDate).startOf('day').format('YYYY-MM-DD 00:00:00'),
      end: moment(formData.endDate).endOf('day').format('YYYY-MM-DD 23:59:59')
    };
    const { data } = await api.get('', { params });
    dataSource.status = data.objects;
  }
  catch (ex) {
    console.error(ex)
  }
  finally {
    components['status-list'].endCustomLoading()
  }
}
async function savePurchaseBalanceItem(){
  const params = {}
  const { data: receivingItem } = await purchaseReceivingItem.load({
    filter: [
        ['receiving.receiving_date', '>=', moment(formData.startDate).format('YYYY-MM-DD 00:00:00')],
        ['receiving.receiving_date', '<=', moment(formData.endDate).format('YYYY-MM-DD 23:59:59')],
        ['receiving.client_company', '=', detailItem.value.client_name]
    ],
    sort: [
        { selector: 'receiving.receiving_date', desc: false }
    ]
  })
    
  const {data : receivingReturnItem } = await purchaseReceivingReturnItem.load({
    filter: [
        ['receiving_return.return_date', '>=', moment(formData.startDate).format('YYYY-MM-DD 00:00:00')],
        ['receiving_return.return_date', '<=', moment(formData.endDate).format('YYYY-MM-DD 23:59:59')],
        ['receiving_return.client_company', '=', detailItem.value.client_name]
    ],
    sort: [
        { selector: 'receiving_return.return_date', desc: false}
    ]
  })
 
  const { data: paymentItem } = await purchasePaymentItem.load({
    filter: [
        ['payment.payment_date', '>=', moment(formData.startDate).format('YYYY-MM-DD 00:00:00')],
        ['payment.payment_date', '<=', moment(formData.endDate).format('YYYY-MM-DD 23:59:59')],
        ['payment.client_company', '=', detailItem.value.client_name]
    ],
    sort: [
        { selector: 'payment.payment_date', desc: false }
    ]
  })

  const { data : statement } = await purchaseStatement.load({
    filter: [
        ['statement_date', '>=', moment(formData.startDate).format('YYYY-MM-DD 00:00:00')],
        ['statement_date', '<=', moment(formData.endDate).format('YYYY-MM-DD 23:59:59')],
        ['client_company', '=', detailItem.value.client_name]
    ],
    sort: [
        { selector: 'statement_date', desc: false }
    ]
  })
  
    let balance = 0
    params.past_balance = dataSource.detail
    .filter(v => v.action_type === '이월미지급금')
    .map(v => {
        const amount = parseInt(v.past_account_receivable, 10)
        balance = amount
        return {
          group_id: v.group_id,
          action_date: v.action_date,
          action_type: v.action_type,
          item_code: '',
          qty: 0,
          unit_price: 0,
          amount,
          balance: amount
        }
  })
      
  params.items = [
    ...receivingItem.map((v, order) => {
        return {
          order,
          action_date: v.receiving.receiving_date,
          action_type: '입고',
          item_code: v.item.item_standard ? `${v.item.item_name} / ${v.item.item_standard}` : v.item.item_name,
          qty: v.receiving_quantity,
          unit_price: v.unit_price,
          amount: v.receiving_quantity * v.unit_price,
          note: v.note
        }
   }),
  ...receivingReturnItem.map((v, order) => {
        return {
          order,
          action_date: v.receiving_return.return_date,
          action_type: '반품',
          item_code: v.item.item_standard ? `${v.item.item_name} / ${v.item.item_standard}` : v.item.item_name,
          qty: -v.return_quantity,
          unit_price: v.receiving_item.unit_price,
          amount: -(v.return_quantity * v.receiving_item.unit_price)
        }
   }),
   ...paymentItem.map((v, order) => {
        return {
          order,
          action_date: v.payment.payment_date,
          action_type: '결재',
          item_code: v.payment_type,
          qty: 0,
          unit_price: 0,
          amount: v.price
        }
   }),
   ...statement.map((v, order) => {
        return {
          order,
          action_date: v.statement_date,
          action_type: '계산서 부가세',
          item_code: '',
          qty: 0,
          unit_price : 0,
          amount: Number(v.vat)
        }
   })
  ]

    params.items = orderBy(params.items, ['action_date', 'order'], ['asc', 'asc'])

    params.items.forEach(v => {
      const d = moment(v.action_date)
      v.group_id = d.format('YYYY-MM')
      v.group_day = d.format('YYYY-MM-DD')

      balance = v.action_type === '결재' 
        ? balance - v.amount
        : balance + v.amount

      v.balance = balance
    })

    const monthGroup = groupBy(params.items, 'group_id')
    const acc = { qty: 0, balance: 0, payment: 0, vat: 0 }
    params.month_group = Object.keys(monthGroup).map(month => {
    const list = monthGroup[month]
    const payment = list.filter(v => v.action_type === '결재')
    const receiving = list.filter(v => v.action_type === '입고')
    const receivingReturn = list.filter(v => v.action_type === '반품')
    const vat = list.filter(v => v.action_type === '계산서 부가세')
    const monthReturnSumQty = receivingReturn.reduce((t, i) => t += i.qty, 0)
    const monthReturnSumPrice = receivingReturn.reduce((t, i) => t += i.amount, 0)

    const monthSumQty = receiving.reduce((t, i) => t += i.qty, 0) + monthReturnSumQty
    const monthSumPrice = receiving.reduce((t, i) => t += i.amount, 0) + monthReturnSumPrice
    const monthSumVat = vat.reduce((t, i) => t += i.amount, 0) 
    const monthSumPay = payment.reduce((t, i) => t += i.amount, 0)
    acc.qty += monthSumQty 
    acc.balance += monthSumPrice 
    acc.payment += monthSumPay
    acc.vat += monthSumVat


    return {
        list,
        month: moment(month, 'YYYY-MM').format('M월'),
        monthSumQty,
        monthSumPrice,
        monthSumVat,
        monthReturnSumQty,
        monthReturnSumPrice,
        monthSumPay,
        accSumQty: acc.qty,
        accSumPrice: acc.balance,
        accSumPay: acc.payment,
        accSumVat: acc.vat
    }
  })

    const dayGroup = groupBy(params.items.filter(v => v.action_type !== '결재'), 'group_day')
    params.day_group = Object.keys(dayGroup).map(date => {
      const list = dayGroup[date]
      return {
        date,
        price: list.reduce((t, i) => t + i.amount, 0)
      }
    })
  

    const workbook = new Workbook();
    workbook.creator = 'STECH'
    workbook.created = new Date()
    const sheet = workbook.addWorksheet('매입원장')
    let index = 1

    const headerRow = sheet.getRow(index++);
    const headerTitles = ['일자', '거래구분', '품명/규격', '수량', '단가', '금액', '잔액', '참고사항'];
    headerTitles.forEach((title, colIndex) => headerRow.getCell(colIndex + 1).value = title);

    const handleData = (rowData) => {
    const row = sheet.getRow(index++);
    rowData.forEach((value, colIndex) => row.getCell(colIndex + 1).value = value);
    };
    
    const handlePastBalance = () => {
    const pastBalance = params['past_balance'][0];
    handleData([
            moment(pastBalance['action_date']).format('YYYY-MM-DD'),
            pastBalance['action_type'],
            pastBalance['item_code'],
            numeral(pastBalance['qty']).format('0,0'),
            numeral(pastBalance['unit_price']).format('0,0'),
            numeral(pastBalance['amount']).format('0,0'),
            numeral(pastBalance['balance']).format('0,0'),
            '',
        ]);
    };

    const handleMonthGroup = () => {
    params['month_group'].forEach(item => {
            item.list.forEach(list_item => {
              handleData([
                  moment(list_item.action_date).format('YYYY-MM-DD'),
                  list_item.action_type,
                  list_item.item_code,
                  numeral(list_item.qty).format('0,0'),
                  numeral(list_item.unit_price).format('0,0'),
                  numeral(list_item.amount).format('0,0'),
                  numeral(list_item.balance).format('0,0'),
                  list_item.note,
              ]);
            });

            handleData([
              item.month,
              `수량합계 : ${numeral(item['monthSumQty']).format('0,0')}`,
              `매입합계 : ${numeral(item['monthSumPrice']).format('0,0')}`,
              `세액합계 : ${numeral(item['monthSumVat']).format('0,0')}`,
              `결재합계 : ${numeral(item['monthSumPay']).format('0,0')}`,
            ]);

            handleData([
              '',
              `수량누계 : ${numeral(item['accSumQty']).format('0,0')}`,
              `매입누계 : ${numeral(item['accSumPrice']).format('0,0')}`,
              `세액누계 : ${numeral(item['accSumVat']).format('0,0')}`,
              `결재누계 : ${numeral(item['accSumPay']).format('0,0')}`,
            ]);
        });
    };

    const handleDayGroup = () => {
      handleData([''])
      handleData(['일자', '금액']);
      params['day_group'].forEach(item => {
          handleData([item.date, numeral(item.price).format('0,0')]);
      });
      handleData([
          '합계금액',
          numeral(params['day_group'].reduce((t, i) => t += i.price, 0)).format('0,0')
      ]);
    };
    handlePastBalance()
    handleMonthGroup()
    handleDayGroup()
    
    const filename = `매입원장(${moment().format('YYYYMMDDHHmmss')}).xlsx`
    const mimeType = { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' };
    const buffer = await workbook.xlsx.writeBuffer()
    const blob = new Blob([buffer], mimeType)
    saveAs(blob, decodeURIComponent(filename));

}

async function printProductReceipt () {
  if (loadingPrintData) return
  if (!dataSource.detail) return

  try {
    loadingPrintData = true
    const params = {}
    params.item = detailItem.value
    params.info = {...formData}
    params.info.startDate = moment(params.info.startDate).format('YYYY년 M월 D일')
    params.info.endDate = moment(params.info.endDate).format('YYYY년 M월 D일')
    params.client = await getClientByName(params.item.client_name)

    const { data: receivingItem } = await purchaseReceivingItem.load({
      filter: [
        ['receiving.receiving_date', '>=', moment(formData.startDate).format('YYYY-MM-DD 00:00:00')],
        ['receiving.receiving_date', '<=', moment(formData.endDate).format('YYYY-MM-DD 23:59:59')],
        ['receiving.client_company', '=', params.item.client_name]
      ],
      sort: [
        { selector: 'receiving.receiving_date', desc: false }
      ]
    })
    
    const {data : receivingReturnItem } = await purchaseReceivingReturnItem.load({
      filter: [
        ['receiving_return.return_date', '>=', moment(formData.startDate).format('YYYY-MM-DD 00:00:00')],
        ['receiving_return.return_date', '<=', moment(formData.endDate).format('YYYY-MM-DD 23:59:59')],
        ['receiving_return.client_company', '=', params.item.client_name]
      ],
      sort: [
        { selector: 'receiving_return.return_date', desc: false}
      ]
    })

    const { data: paymentItem } = await purchasePaymentItem.load({
      filter: [
        ['payment.payment_date', '>=', moment(formData.startDate).format('YYYY-MM-DD 00:00:00')],
        ['payment.payment_date', '<=', moment(formData.endDate).format('YYYY-MM-DD 23:59:59')],
        ['payment.client_company', '=', params.item.client_name]
      ],
      sort: [
        { selector: 'payment.payment_date', desc: false }
      ]
    })

    const { data : statement } = await purchaseStatement.load({
      filter: [
        ['statement_date', '>=', moment(formData.startDate).format('YYYY-MM-DD 00:00:00')],
        ['statement_date', '<=', moment(formData.endDate).format('YYYY-MM-DD 23:59:59')],
        ['client_company', '=', params.item.client_name]
      ],
      sort: [
        { selector: 'statement_date', desc: false }
      ]
    })
    let balance = 0
    params.past_balance = dataSource.detail
    .filter(v => v.action_type === '이월미지급금')
    .map(v => {
        const amount = parseInt(v.past_account_receivable, 10)
        balance = amount
        return {
          group_id: v.group_id,
          action_date: v.action_date,
          action_type: v.action_type,
          item_code: '',
          qty: 0,
          unit_price: 0,
          amount,
          balance: amount
        }
    })
    
    params.items = [
    ...receivingItem.map((v, order) => {
        return {
          order,
          action_date: v.receiving.receiving_date,
          action_type: '입고',
          item_code: v.item.item_standard ? `${v.item.item_name} / ${v.item.item_standard}` : v.item.item_name,
          qty: v.receiving_quantity,
          unit_price: v.unit_price,
          amount: v.receiving_quantity * v.unit_price,
          note: v.note
        }
    }),
    ...receivingReturnItem.map((v, order) => {
        return {
          order,
          action_date: v.receiving_return.return_date,
          action_type: '반품',
          item_code: v.item.item_standard ? `${v.item.item_name} / ${v.item.item_standard}` : v.item.item_name,
          qty: -v.return_quantity,
          unit_price: v.receiving_item.unit_price,
          amount: -(v.return_quantity * v.receiving_item.unit_price)
        }
    }),
    ...paymentItem.map((v, order) => {
        return {
          order,
          action_date: v.payment.payment_date,
          action_type: '결재',
          item_code: v.payment_type,
          qty: 0,
          unit_price: 0,
          amount: v.price
        }
    }),
    ...statement.map((v, order) => {
        return {
          order,
          action_date: v.statement_date,
          action_type: '계산서 부가세',
          item_code: '',
          qty: 0,
          unit_price : 0,
          amount: Number(v.vat)
        }
    })
      // ...releaseItems.filter(v => v.release.vat_type === '별도').map((v, order) => {
      //   return {
      //     order,
      //     action_date: v.release.release_date,
      //     action_type: '세액',
      //     item_code: v.note,
      //     qty: 0,
      //     unit_price: 0,
      //     amount: (v.release_quantity * v.unit_price) * 0.1
      //   }
      // }),
      // ...releaseReturnItem.filter(v => v.release_return.vat_type === '별도').map((v, order) => {
      //   return {
      //     order,
      //     action_date: v.release_return.return_date,
      //     action_type: '반품 세액',
      //     item_code: v.return_reason,
      //     qty: 0,
      //     unit_price: 0,
      //     amount: -((v.return_quantity * v.unit_price) * 0.1)
      //   }
      // })
    ]

    params.items = orderBy(params.items, ['action_date', 'order'], ['asc', 'asc'])

    params.items.forEach(v => {
      const d = moment(v.action_date)
      v.group_id = d.format('YYYY-MM')
      v.group_day = d.format('YYYY-MM-DD')

      balance = v.action_type === '결재' 
        ? balance - v.amount
        : balance + v.amount

      v.balance = balance
    })

    const monthGroup = groupBy(params.items, 'group_id')
    const acc = { qty: 0, balance: 0, payment: 0, vat: 0 }
    params.month_group = Object.keys(monthGroup).map(month => {
    const list = monthGroup[month]
    const payment = list.filter(v => v.action_type === '결재')
    const receiving = list.filter(v => v.action_type === '입고')
    const receivingReturn = list.filter(v => v.action_type === '반품')
    const vat = list.filter(v => v.action_type === '계산서 부가세')
    const monthReturnSumQty = receivingReturn.reduce((t, i) => t += i.qty, 0)
    const monthReturnSumPrice = receivingReturn.reduce((t, i) => t += i.amount, 0)

    const monthSumQty = receiving.reduce((t, i) => t += i.qty, 0) + monthReturnSumQty
    const monthSumPrice = receiving.reduce((t, i) => t += i.amount, 0) + monthReturnSumPrice
    const monthSumVat = vat.reduce((t, i) => t += i.amount, 0) 
    const monthSumPay = payment.reduce((t, i) => t += i.amount, 0)
    acc.qty += monthSumQty 
    acc.balance += monthSumPrice 
    acc.payment += monthSumPay
    acc.vat += monthSumVat

    return {
        list,
        month: moment(month, 'YYYY-MM').format('M월'),
        monthSumQty,
        monthSumPrice,
        monthSumVat,
        monthReturnSumQty,
        monthReturnSumPrice,
        monthSumPay,
        accSumQty: acc.qty,
        accSumPrice: acc.balance,
        accSumPay: acc.payment,
        accSumVat: acc.vat
    }
    })

    const dayGroup = groupBy(params.items.filter(v => v.action_type !== '결재'), 'group_day')
    params.day_group = Object.keys(dayGroup).map(date => {
      const list = dayGroup[date]
      return {
          date,
          price: list.reduce((t, i) => t + i.amount, 0)
      }
    })
    await printDocument('purchasereceiptsummary', params);
  }
  catch (ex) {
    console.error('매입 원장 출력 중 에러', ex)
  }
  finally {
    loadingPrintData = false
  }
}

async function exportData(component, sheetName, fileName) {
  const workbook = new Workbook();
  const worksheet = workbook.addWorksheet(sheetName);

  await exportDataGrid({ component, worksheet });
  const buffer = await workbook.xlsx.writeBuffer();
  saveAs(
    new Blob([buffer], { type: 'application/octet-stream' }),
    fileName
  );
}

async function onExporting (evt) {
  exportData(evt.component, '매입잔액장', `매입잔액장_${Date.now()}.xlsx`)
  evt.cancel = true
}
</script>

<style>
.summary-table {
  width: 100%;
  margin-top: 10px;
}
</style>
