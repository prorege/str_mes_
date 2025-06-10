<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">매출원장</div>
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
            <span class="search-title">거래처</span>
            <dx-text-box :value="formData.clientName">
              <dx-text-box-button name="search" location="after"
                :options="{ icon: 'search', stylingMode: 'text', onClick: () => (dlg.findClient.show = true) }"
              />
            </dx-text-box>

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
          @initialized="evt => initialized(evt, 'status-list')"
          @exporting="onExporting"
        >
        <dx-grid-toolbar>
          <dx-item template="export" location="before" :visible="true" />
        </dx-grid-toolbar>
        <template #export>
          <dx-button text="매출원장출력" icon="export" @click="printProductReceipt" />
          <dx-button text="Excel" icon="xlsxfile" @click="saveSalesBalanceItem" />
        </template>

          <dx-column caption="" data-field="group_id" :group-index="0" />
          <dx-column caption="일자" data-field="action_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="유형" data-field="action_type" />
          <dx-column caption="업체명" data-field="company" />
          <dx-column caption="당사담당자" data-field="manager" />
          <dx-column caption="이월미수금" data-field="past_account_receivable" data-type="number" format="currency" />
          <dx-column caption="매출" data-field="sales_price" data-type="number" format="currency" />
          <dx-column caption="계산서 부가세" data-field="vat" data-type="number" format="currency" />
          <dx-column caption="부가세 보정" data-field="vat_adjustment" data-type="number" format="currency" />
          <dx-column caption="매출합계" data-field="total_sales_price" data-type="number" format="currency" />
          <dx-column caption="입금" data-field="deposit_price" data-type="number" format="currency" />
          <dx-column caption="미수금 잔액" data-field="account_receivable" data-type="number" format="currency" />

          <dx-summary :calculate-custom-summary="calculateCustomSummary">
            <dx-group-item
              :align-by-column="true"
              column="sales_price"
              summary-type="sum"
              value-format="currency"
              display-format="매출: {0}"
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
              column="total_sales_price"
              summary-type="sum"
              value-format="currency"
              display-format="매출합계: {0}"
            />
            <dx-group-item
              :align-by-column="true"
              column="deposit_price"
              summary-type="sum"
              value-format="currency"
              display-format="입금: {0}"
            />

            <dx-group-item
              :show-in-group-footer="true"
              name="accumulate_sales_price"
              summary-type="custom"
              value-format="currency"
              show-in-column="sales_price"
              display-format="누적매출: {0}"
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
              name="accumulate_total_sales_price"
              summary-type="custom"
              value-format="currency"
              show-in-column="total_sales_price"
              display-format="누적매출합계: {0}"
            />
            <dx-group-item
              :show-in-group-footer="true"
              column="accumulate_deposit_price"
              summary-type="max"
              value-format="currency"
              show-in-column="deposit_price"
              display-format="누적입금: {0}"
            />

            <dx-group-item
              :show-in-group-footer="true"
              name="last_account_receivable"
              summary-type="custom"
              value-format="currency"
              show-in-column="account_receivable"
              display-format="미수금 잔액: {0}"
            />
          </dx-summary>

          <dx-export :enabled="true" />
          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
        </dx-data-grid>

        <table class="summary-table" style="width: 1200px;">
          <tr>
            <td>누계</td>
            <th>이월 미수금</th>
            <td>{{ summary.past_account_receivable.value }}</td>
            <th>매출</th>
            <td>{{ summary.sales_price.value }}</td>
            <th>부가세</th>
            <td>{{ summary.vat.value }}</td>
            <th>매출 합계</th>
            <td>{{ summary.total_sales_price.value }}</td>
            <th>입금 합계</th>
            <td>{{ summary.total_deposit_price.value }}</td>
            <th>미수금 잔액</th>
            <td>{{ summary.total_account_receivable.value }}</td>
          </tr>
        </table>

      </div>
    </div>

    <dx-popup
      title="업체찾기"  
      content-template="popup-content"
      v-model:visible="dlg.findClient.show"
      :width="680"
      :height="460"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => initialized(evt, 'find-item-popup')"
    >
      <template #popup-content>
        <dx-data-grid
          :show-borders="true"
          :remote-operations="true"
          :column-auto-width="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="dataSource.baseClient"
          :on-initialized="evt => initialized(evt, 'baseClient')"
          @selection-changed="selectItem"
        >
          <dx-column caption="업체약칭" data-field="alias" data-type="string" />
          <dx-column caption="업체명" data-field="name" data-type="string" />
          <dx-column caption="사업자번호" data-field="business_number" data-type="string" />
          <dx-column caption="대표자" data-field="ceo_name" data-type="string" />
          <dx-column caption="주소" data-field="address" data-type="string" />

          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-selection mode="single" select-all-mode="page" show-check-boxes-mode="onClick"/>
        </dx-data-grid>
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
  DxSelection,
  DxItem as DxGridItem, DxToolbar as DxGridToolbar, DxButton as DxGridButton
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
import { getClientByName, getBaseClient } from '@/data-source/base'
import { shipmentReleaseItem, shipmentDepositItem, shipmentReleaseReturnItem, shipmentSalesStatement } from '@/data-source/shipment';
import { groupBy, orderBy } from 'lodash'
import { DxTextBox, DxButton as DxTextBoxButton } from 'devextreme-vue/text-box';
import { confirm, alert } from 'devextreme/ui/dialog';
import { formatDate } from 'devextreme/localization';

const api = new ApiService('/api/mes/v1/shipment/sales/balance');
const commonInit = ref(false);
const dialog = ref(false);
const startDate = new Date();
startDate.setDate(startDate.getDate() - 7);
let loadingPrintData = false

const detailItem = ref()

const formData = reactive({
  startDate: startDate,
  endDate: new Date(),
  clientId: null,
  clientName: null,
});
const dlg = {};
dlg.findClient = reactive({ show: false });

const components = {};

const dataSource = reactive({
  status: [],
  detail: [],
  sum: {
    past_account_receivable: 0,
    sales_price: 0,
    vat: 0,
    total_sales_price: 0,
    total_deposit_price: 0,
    total_account_receivable: 0,
  },
  baseItem: null,
});

const summary = {};
summary.past_account_receivable = computed(() => '₩' + numeral(dataSource.sum.past_account_receivable).format('0,0'));
summary.sales_price = computed(() => '₩' + numeral(dataSource.sum.sales_price).format('0,0'));
summary.vat = computed(() => '₩' + numeral(dataSource.sum.vat).format('0,0'));
summary.total_sales_price = computed(() => '₩' + numeral(dataSource.sum.total_sales_price).format('0,0'));
summary.total_deposit_price = computed(() => '₩' + numeral(dataSource.sum.total_deposit_price).format('0,0'));
summary.total_account_receivable = computed(() => '₩' + numeral(dataSource.sum.total_account_receivable).format('0,0'));

!(async () => {
  commonInit.value = true;
  dataSource.baseClient = getBaseClient();
})();

function initialized(evt, key) {
  components[key] = evt.component;
}

function calculateCustomSummary(options) {
  const summaryProcesses = ['accumulate_vat_adjustment', 'accumulate_vat', 'accumulate_sales_price', 'accumulate_total_sales_price'];

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
  let sumSalesPrice = 0;
  let sumVat = 0;
  let sumVatAdjustment = 0;
  let sumTotalSalesPrice = 0;
  let sumDepositPrice = 0;
  let sumAccountReceivable = 0;
  response.objects.forEach(row => {
    sumPastAccountReceivable += parseInt(row.past_account_receivable, 10);
    sumSalesPrice += parseInt(row.sales_price, 10);
    sumVat += parseInt(row.vat, 10);
    sumVatAdjustment += parseInt(row.vat_adjustment, 10);
    sumTotalSalesPrice += parseInt(row.total_sales_price, 10) + parseInt(row.vat, 10);
    sumDepositPrice += parseInt(row.deposit_price, 10);
    sumAccountReceivable += parseInt(row.past_account_receivable, 10) + parseInt(row.total_sales_price, 10) + parseInt(row.vat, 10) - parseInt(row.deposit_price, 10);
    row.account_receivable = sumAccountReceivable;
    row.accumulate_sales_price = sumSalesPrice;
    row.accumulate_vat = sumVat;
    row.accumulate_vat_adjustment = sumVatAdjustment;
    row.accumulate_total_sales_price = sumTotalSalesPrice;
    row.accumulate_deposit_price = sumDepositPrice;
  });
  dataSource.detail = response.objects;
  dataSource.sum.past_account_receivable = sumPastAccountReceivable;
  dataSource.sum.sales_price = sumSalesPrice;
  dataSource.sum.vat = sumVat;
  dataSource.sum.total_sales_price = sumTotalSalesPrice;
  dataSource.sum.total_deposit_price = sumDepositPrice;
  dataSource.sum.total_account_receivable = sumAccountReceivable;
  dialog.value = true;
}

async function searchDateRange() {
  try {
    if (!formData.clientId) {
      alert('거래처를 선택하세요.', '매출원장');
      return;
    }

    components['status-list'].beginCustomLoading('데이터를 집계중입니다')

    const params = {
      start: moment(formData.startDate).startOf('day').format('YYYY-MM-DD 00:00:00'),
      end: moment(formData.endDate).endOf('day').format('YYYY-MM-DD 23:59:59')
    };
    const { data: response } = await api.get(String(formData.clientId), { params });
    dataSource.status = response.objects;

    let sumPastAccountReceivable = 0;
    let sumSalesPrice = 0;
    let sumVat = 0;
    let sumVatAdjustment = 0;
    let sumTotalSalesPrice = 0;
    let sumDepositPrice = 0;
    let sumAccountReceivable = 0;
    response.objects.forEach(row => {
      sumPastAccountReceivable += parseInt(row.past_account_receivable, 10);
      sumSalesPrice += parseInt(row.sales_price, 10);
      sumVat += parseInt(row.vat, 10);
      sumVatAdjustment += parseInt(row.vat_adjustment, 10);
      sumTotalSalesPrice += parseInt(row.total_sales_price, 10) + parseInt(row.vat, 10);
      sumDepositPrice += parseInt(row.deposit_price, 10);
      sumAccountReceivable += parseInt(row.past_account_receivable, 10) + parseInt(row.total_sales_price, 10) + parseInt(row.vat, 10) - parseInt(row.deposit_price, 10);
      row.account_receivable = sumAccountReceivable;
      row.accumulate_sales_price = sumSalesPrice;
      row.accumulate_vat = sumVat;
      row.accumulate_vat_adjustment = sumVatAdjustment;
      row.accumulate_total_sales_price = sumTotalSalesPrice;
      row.accumulate_deposit_price = sumDepositPrice;
    });
    dataSource.detail = response.objects;
    dataSource.sum.past_account_receivable = sumPastAccountReceivable;
    dataSource.sum.sales_price = sumSalesPrice;
    dataSource.sum.vat = sumVat;
    dataSource.sum.total_sales_price = sumTotalSalesPrice;
    dataSource.sum.total_deposit_price = sumDepositPrice;
    dataSource.sum.total_account_receivable = sumAccountReceivable;
  }
  catch (ex) {
    console.error(ex)
  }
  finally {
    components['status-list'].endCustomLoading()
  }
}

function selectItem(data) {
  if (data.selectedRowsData.length > 0) {
    const client = data.selectedRowsData[0];
    formData.clientId = client.id;
    formData.clientName = client.name;
  }
  dlg.findClient.show = false;
}

async function saveSalesBalanceItem(){
  if (!dataSource.detail) return
  if (!formData.clientName) return
  const params = {}
    const { data: releaseItems } = await shipmentReleaseItem.load({
      filter: [
        ['release.release_date', '>=', moment(formData.startDate).format('YYYY-MM-DD 00:00:00')],
        ['release.release_date', '<=', moment(formData.endDate).format('YYYY-MM-DD 23:59:59')],
        ['release.client_company', '=', formData.clientName]
      ],
      sort: [
        { selector: 'release.release_date', desc: false }
      ]
    })
    
    const {data : releaseReturnItem } = await shipmentReleaseReturnItem.load({
      filter: [
        ['release_return.return_date', '>=', moment(formData.startDate).format('YYYY-MM-DD 00:00:00')],
        ['release_return.return_date', '<=', moment(formData.endDate).format('YYYY-MM-DD 23:59:59')],
        ['release_return.client_company', '=', formData.clientName]
      ],
      sort: [
        { selector: 'release_return.return_date', desc: false}
      ]
    })
 
    const { data: depositItems } = await shipmentDepositItem.load({
      filter: [
        ['deposit.deposit_date', '>=', moment(formData.startDate).format('YYYY-MM-DD 00:00:00')],
        ['deposit.deposit_date', '<=', moment(formData.endDate).format('YYYY-MM-DD 23:59:59')],
        ['deposit.client_company', '=', formData.clientName]
      ],
      sort: [
        { selector: 'deposit.deposit_date', desc: false }
      ]
    })

    const { data : salesStatement } = await shipmentSalesStatement.load({
      filter: [
        ['sales_date', '>=', moment(formData.startDate).format('YYYY-MM-DD 00:00:00')],
        ['sales_date', '<=', moment(formData.endDate).format('YYYY-MM-DD 23:59:59')],
        ['client_company', '=', formData.clientName]
      ],
      sort: [
        { selector: 'sales_date', desc: false }
      ]
    })
  
    let balance = 0
    params.past_balance = dataSource.detail
      .filter(v => v.action_type === '이월미수금')
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
      ...releaseItems.map((v, order) => {
        return {
          order,
          action_date: v.release.release_date,
          action_type: '출고',
          item_code: v.item.item_standard ? `${v.item.item_name} / ${v.item.item_standard}` : v.item.item_name,
          qty: v.release_quantity,
          unit_price: v.unit_price,
          amount: v.release_quantity * v.unit_price,
          note: v.note
        }
      }),
      ...releaseReturnItem.map((v, order) => {
        return {
          order,
          action_date: v.release_return.return_date,
          action_type: '반품',
          item_code: v.item.item_standard ? `${v.item.item_name} / ${v.item.item_standard}` : v.item.item_name,
          qty: -v.return_quantity,
          unit_price: v.unit_price,
          amount: -(v.return_quantity * v.unit_price)
        }
      }),
      ...depositItems.map((v, order) => {
        return {
          order,
          action_date: v.deposit.deposit_date,
          action_type: '입금',
          item_code: v.deposit_type,
          qty: 0,
          unit_price: 0,
          amount: v.price
        }
      }),
      ...salesStatement.map((v, order) => {
        return {
          order,
          action_date: v.sales_date,
          action_type: '계산서 부가세',
          item_code: '',
          qty: 0,
          unit_price : 0,
          amount: v.vat
        }
      })
    ]

    params.items = orderBy(params.items, ['action_date', 'order'], ['asc', 'asc'])

    params.items.forEach(v => {
      const d = moment(v.action_date)
      v.group_id = d.format('YYYY-MM')
      v.group_day = d.format('YYYY-MM-DD')

      balance = v.action_type === '입금' 
        ? balance - v.amount
        : balance + v.amount

      v.balance = balance
    })

    const monthGroup = groupBy(params.items, 'group_id')
    const acc = { qty: 0, balance: 0, deposit: 0, vat: 0 }
    params.month_group = Object.keys(monthGroup).map(month => {
      const list = monthGroup[month]
      const deposit = list.filter(v => v.action_type === '입금')
      const release = list.filter(v => v.action_type === '출고')
      const releaseReturn = list.filter(v => v.action_type === '반품')
      const vat = list.filter(v => v.action_type === '계산서 부가세')
      const monthReturnSumQty = releaseReturn.reduce((t, i) => t += i.qty, 0)
      const monthReturnSumPrice = releaseReturn.reduce((t, i) => t += i.amount, 0)
  
      const monthSumQty = release.reduce((t, i) => t += i.qty, 0) + monthReturnSumQty
      const monthSumPrice = release.reduce((t, i) => t += i.amount, 0) + monthReturnSumPrice
      const monthSumVat = vat.reduce((t, i) => t += i.amount, 0) 
      const monthSumDep = deposit.reduce((t, i) => t += i.amount, 0)
      acc.qty += monthSumQty 
      acc.balance += monthSumPrice 
      acc.deposit += monthSumDep
      acc.vat += monthSumVat

      return {
        list,
        month: moment(month, 'YYYY-MM').format('M월'),
        monthSumQty,
        monthSumPrice,
        monthSumVat,
        monthReturnSumQty,
        monthReturnSumPrice,
        monthSumDep,
        accSumQty: acc.qty,
        accSumPrice: acc.balance,
        accSumDep: acc.deposit,
        accSumVat: acc.vat
      }
    })

    const dayGroup = groupBy(params.items.filter(v => v.action_type !== '입금'), 'group_day')
    params.day_group = Object.keys(dayGroup).map(date => {
      const list = dayGroup[date]
      return {
        date,
        price: list.reduce((t, i) => t + i.amount, 0)
      }
    })
  

    const workbook = new Workbook();
    workbook.creator = 'MEC'
    workbook.created = new Date()
    const sheet = workbook.addWorksheet('매출원장')
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
              `매출합계 : ${numeral(item['monthSumPrice']).format('0,0')}`,
              `세액합계 : ${numeral(item['monthSumVat']).format('0,0')}`,
              `입금합계 : ${numeral(item['monthSumDep']).format('0,0')}`,
            ]);

            handleData([
              '',
              `수량누계 : ${numeral(item['accSumQty']).format('0,0')}`,
              `매출누계 : ${numeral(item['accSumPrice']).format('0,0')}`,
              `세액누계 : ${numeral(item['accSumVat']).format('0,0')}`,
              `입금누계 : ${numeral(item['accSumDep']).format('0,0')}`,
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
    
    const filename = `매출원장(${moment().format('YYYYMMDDHHmmss')}).xlsx`
    const mimeType = { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' };
    const buffer = await workbook.xlsx.writeBuffer()
    const blob = new Blob([buffer], mimeType)
    saveAs(blob, decodeURIComponent(filename));

}

async function printProductReceipt () {
  if (loadingPrintData) return
  if (!dataSource.detail) return
  if (!formData.clientName) return

  try {
    loadingPrintData = true
    const params = {}
    params.item = dataSource.detail
    params.info = {...formData}
    params.info.startDate = moment(params.info.startDate).format('YYYY년 M월 D일')
    params.info.endDate = moment(params.info.endDate).format('YYYY년 M월 D일')

    params.client = await getClientByName(formData.clientName)

    const { data: releaseItems } = await shipmentReleaseItem.load({
      filter: [
        ['release.release_date', '>=', moment(formData.startDate).format('YYYY-MM-DD 00:00:00')],
        ['release.release_date', '<=', moment(formData.endDate).format('YYYY-MM-DD 23:59:59')],
        ['release.client_company', '=', formData.clientName]
      ],
      sort: [
        { selector: 'release.release_date', desc: false }
      ]
    })
    
    const {data : releaseReturnItem } = await shipmentReleaseReturnItem.load({
      filter: [
        ['release_return.return_date', '>=', moment(formData.startDate).format('YYYY-MM-DD 00:00:00')],
        ['release_return.return_date', '<=', moment(formData.endDate).format('YYYY-MM-DD 23:59:59')],
        ['release_return.client_company', '=', formData.clientName]
      ],
      sort: [
        { selector: 'release_return.return_date', desc: false}
      ]
    })
 
    const { data: depositItems } = await shipmentDepositItem.load({
      filter: [
        ['deposit.deposit_date', '>=', moment(formData.startDate).format('YYYY-MM-DD 00:00:00')],
        ['deposit.deposit_date', '<=', moment(formData.endDate).format('YYYY-MM-DD 23:59:59')],
        ['deposit.client_company', '=', formData.clientName]
      ],
      sort: [
        { selector: 'deposit.deposit_date', desc: false }
      ]
    })

    const { data : salesStatement } = await shipmentSalesStatement.load({
      filter: [
        ['sales_date', '>=', moment(formData.startDate).format('YYYY-MM-DD 00:00:00')],
        ['sales_date', '<=', moment(formData.endDate).format('YYYY-MM-DD 23:59:59')],
        ['client_company', '=', formData.clientName]
      ],
      sort: [
        { selector: 'sales_date', desc: false }
      ]
    })
  
    let balance = 0
    params.past_balance = dataSource.detail
      .filter(v => v.action_type === '이월미수금')
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
      ...releaseItems.map((v, order) => {
        return {
          order,
          action_date: v.release.release_date,
          action_type: '출고',
          item_code: v.item.item_standard ? `${v.item.item_name} / ${v.item.item_standard}` : v.item.item_name,
          qty: v.release_quantity,
          unit_price: v.unit_price,
          amount: v.release_quantity * v.unit_price,
          note: v.note
        }
      }),
      ...releaseReturnItem.map((v, order) => {
        return {
          order,
          action_date: v.release_return.return_date,
          action_type: '반품',
          item_code: v.item.item_standard ? `${v.item.item_name} / ${v.item.item_standard}` : v.item.item_name,
          qty: -v.return_quantity,
          unit_price: v.unit_price,
          amount: -(v.return_quantity * v.unit_price)
        }
      }),
      ...depositItems.map((v, order) => {
        return {
          order,
          action_date: v.deposit.deposit_date,
          action_type: '입금',
          item_code: v.deposit_type,
          qty: 0,
          unit_price: 0,
          amount: v.price
        }
      }),
      ...salesStatement.map((v, order) => {
        return {
          order,
          action_date: v.sales_date,
          action_type: '계산서 부가세',
          item_code: '',
          qty: 0,
          unit_price : 0,
          amount: v.vat
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

      balance = v.action_type === '입금' 
        ? balance - v.amount
        : balance + v.amount

      v.balance = balance
    })

    const monthGroup = groupBy(params.items, 'group_id')
    const acc = { qty: 0, balance: 0, deposit: 0, vat: 0 }
    params.month_group = Object.keys(monthGroup).map(month => {
      const list = monthGroup[month]
      const deposit = list.filter(v => v.action_type === '입금')
      const release = list.filter(v => v.action_type === '출고')
      const releaseReturn = list.filter(v => v.action_type === '반품')
      const vat = list.filter(v => v.action_type === '계산서 부가세')
      const monthReturnSumQty = releaseReturn.reduce((t, i) => t += i.qty, 0)
      const monthReturnSumPrice = releaseReturn.reduce((t, i) => t += i.amount, 0)
  
      const monthSumQty = release.reduce((t, i) => t += i.qty, 0) + monthReturnSumQty
      const monthSumPrice = release.reduce((t, i) => t += i.amount, 0) + monthReturnSumPrice
      const monthSumVat = vat.reduce((t, i) => t += i.amount, 0) 
      const monthSumDep = deposit.reduce((t, i) => t += i.amount, 0)
      acc.qty += monthSumQty 
      acc.balance += monthSumPrice 
      acc.deposit += monthSumDep
      acc.vat += monthSumVat

      return {
        list,
        month: moment(month, 'YYYY-MM').format('M월'),
        monthSumQty,
        monthSumPrice,
        monthSumVat,
        monthReturnSumQty,
        monthReturnSumPrice,
        monthSumDep,
        accSumQty: acc.qty,
        accSumPrice: acc.balance,
        accSumDep: acc.deposit,
        accSumVat: acc.vat
      }
    })

    const dayGroup = groupBy(params.items.filter(v => v.action_type !== '입금'), 'group_day')
    params.day_group = Object.keys(dayGroup).map(date => {
      const list = dayGroup[date]
      return {
        date,
        price: list.reduce((t, i) => t + i.amount, 0)
      }
    })
    await printDocument('salesreceiptsummary', params);
  }
  catch (ex) {
    console.error('매출 원장 출력 중 에러', ex)
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
  exportData(evt.component, '매출잔액장', `매출잔액장_${Date.now()}.xlsx`)
  evt.cancel = true
}
</script>

<style>
.summary-table {
  width: 100%;
  margin-top: 10px;
}
</style>
