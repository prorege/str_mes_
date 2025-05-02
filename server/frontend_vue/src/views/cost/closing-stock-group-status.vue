<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">품목그룹별 마감재고</div>
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

            <span class="search-bar">창고선택</span>
            <dx-lookup
              value-expr="wh_name"
              display-expr="wh_name"  
              v-model:value="formData.warehouseName"
              :data-source="dataSource.warehouse"
            />

            <span class="search-bar">자산구분</span>
            <dx-lookup
              value-expr="code_name"
              display-expr="code_name"  
              v-model:value="formData.assetType"
              :data-source="dataSource.assetType"
            />

            <span class="search-bar">품목대분류</span>
            <dx-lookup
              :search-enabled=true
              search-mode="contains"
              value-expr="code_name"
              display-expr="code_name"  
              v-model:value="formData.category"
              :data-source="dataSource.category"
            />

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
        >
          <dx-column caption="품목대분류" data-field="main_category" />
          <dx-column caption="이월재고" data-field="past_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="이월금액" data-field="past_price" data-type="number" format="₩,##0" />
          <dx-column caption="입고량" data-field="receiving_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="입고금액" data-field="receiving_price" data-type="number" format="₩,##0" />
          <dx-column caption="출고량" data-field="release_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="출고원가금액" data-field="release_price" data-type="number" format="₩,##0" />
          <dx-column caption="마감재고" data-field="closing_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="마감재고금액" data-field="closing_price" data-type="number" format="₩,##0" />

          <dx-grouping :auto-expand-all="true" />
          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-export :enabled="true" />
        </dx-data-grid>
      </div>
    </div>

    <dx-popup
      v-model:visible="dialog"
      content-template="popup-content"
      title="상품수불내역"
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
          text: '상품수불장 출력',
          onClick: printProductReceipt
        }"
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
          @initialized="evt => initialized(evt, 'payment-status-detail')"
        >
          <dx-column caption="" data-field="group_id" :group-index="0" />
          <dx-column caption="수불일자" data-field="action_date"  data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="입출고유형" data-field="inout_type" />
          <dx-column caption="업체" data-field="company" />
          <dx-column caption="단가" data-field="unit_price" data-type="number" format="currency" />
          <dx-column caption="이월재고" data-field="past_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="입고수량" data-field="receiving_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="출고수량" data-field="release_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="누적재고" data-field="sum_by_case" data-type="number" format="fixedPoint" />
          <dx-column caption="입출고번호" data-field="number" />
          <dx-column caption="누적입고수량" data-field="accumulate_receiving_stock" data-type="number" format="fixedPoint" :visible="false" />
          <dx-column caption="누적출고수량" data-field="accumulate_release_stock" data-type="number" format="fixedPoint" :visible="false" />

          <dx-summary :calculate-custom-summary="calculateCustomSummary">
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

          <dx-paging :page-size="10" />
        </dx-data-grid>

        <table class="summary-table">
          <tr>
            <td>누계</td>
            <th>이월재고</th>
            <td>{{ dataSource.sum.past_stock }}</td>
            <th>입고수량</th>
            <td>{{ dataSource.sum.receiving_stock }}</td>
            <th>출고수량</th>
            <td>{{ dataSource.sum.release_stock }}</td>
            <th>누적재고</th>
            <td>{{ dataSource.sum.sum_by_case }}</td>
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
  DxTotalItem,
  DxGroupItem,
  DxFilterRow,
  DxGrouping,
  DxExport,
} from 'devextreme-vue/data-grid';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import DxLookup from 'devextreme-vue/select-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import DxButton from 'devextreme-vue/button';
import ApiService from '../../utils/api-service';
import { ref, reactive } from 'vue';
import { baseCodeLoader } from '../../data-source/base';
import authService from '../../auth';
import { loadWarehouse } from '../../utils/data-loader';
import moment from 'moment';
import numeral from 'numeral';
import { groupBy, sortBy } from 'lodash'
import {printDocument} from '@/utils/print-document';

const api = new ApiService('/api/mes/v1/cost/statistics');
const commonInit = ref(false);
const dialog = ref(false);
const now = new Date();

const detailItem = ref()

const formData = reactive({
  startDate: new Date(now.getFullYear(), now.getMonth() - 1, 1),
  endDate: new Date(now.getFullYear(), now.getMonth(), 0),
  warehouseName: '',
  assetType: '',
  category: ''
});

const components = {};

const dataSource = reactive({
  warehouse: [],
  assetType: [],
  category: [],
  status: [],
  detail: [],
  sum: {
    past_stock: 0,
    receiving_stock: 0,
    release_stock: 0,
    sum_by_case: 0,
  },
});

!(async () => {
  await baseCodeLoader(['자산구분', '품목분류'], authService.getCompanyId()).then(
    response => {
      dataSource.assetType = response['자산구분'];
      dataSource.assetType.unshift({ code_name: '전체' });

      dataSource.category = response['품목분류'];
      dataSource.category.sort(function(a, b) {
        const upperA = a.code_name.toUpperCase();
        const upperB = b.code_name.toUpperCase();

        if (upperA > upperB) return 1;
        if (upperA < upperB) return -1;
        if (upperA == upperB) return 0;
      });
      dataSource.category.unshift({ code_name: '전체' });
    }
  );

  await loadWarehouse(dataSource);
  //dataSource.warehouse.unshift({'wh_name':'전체'});

  formData.warehouseName = dataSource.warehouse[0].wh_name;
  formData.category = dataSource.category[0].code_name;
  formData.assetType = '전체';
  formData.assetType = dataSource.assetType[0].code_name;


  commonInit.value = true;
})();

function initialized(evt, key) {
  components[key] = evt.component;
}

function calculateCustomSummary(options) {
  if (options.name === 'last_stock_summary') {
    if (options.summaryProcess === 'start') {
      options.totalValue = 0;
    } else if (options.summaryProcess === 'calculate') {
      options.totalValue = options.value.sum_by_case;
    }
  }
}

async function goDetail({ data }) {
  detailItem.value = data
  const params = {
    start: moment(formData.startDate).format('YYYYMMDD'),
    end: moment(formData.endDate).endOf('day').format('YYYY-MM-DD HH:mm:ss'),
  };
  const { data: response } = await api.get(String(data.item_id), { params });

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
  dataSource.detail = response.objects;
  dataSource.sum.past_stock = numberWithCommas(response.objects.reduce((sum, row) => sum + parseInt(row.past_stock, 10), 0));
  dataSource.sum.receiving_stock = numberWithCommas(response.objects.reduce((sum, row) => sum + row.receiving_stock, 0));
  dataSource.sum.release_stock = numberWithCommas(response.objects.reduce((sum, row) => sum + row.release_stock, 0));
  dataSource.sum.sum_by_case = numberWithCommas(sumByCase);
  dialog.value = true;
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

async function searchDateRange() {
  try {
    components['status-list'].beginCustomLoading('데이터를 집계중입니다')
    const params = {
      start: moment(formData.startDate).startOf('day').format('YYYY-MM-DD HH:mm:ss'),
      end: moment(formData.endDate).endOf('day').format('YYYY-MM-DD HH:mm:ss'),
      wh_name: formData.warehouseName === '전체' ? '' : formData.warehouseName,
      asset_type: formData.assetType === '전체' ? '' : formData.assetType,
      category: formData.category === '전체' ? '' : formData.category
    };
    const { data } = await api.get('', { params });
    const sorted = sortBy(data.objects, 'main_category')
    const grouped = groupBy(sorted, 'main_category')
    

    let result = []
    Object.keys(grouped).forEach((key, i) => {
      result.push({
        id: i + 1,
        main_category: key,
        ...grouped[key].reduce((t, a, currentIndex, array) => {
          t.available_stock += parseInt(a.available_stock)
          t.closing_stock += parseInt(a.closing_stock)
          t.current_stock += parseInt(a.current_stock)
          t.past_stock += parseInt(a.past_stock)
          t.receiving_stock += parseInt(a.receiving_stock)
          t.release_stock += parseInt(a.release_stock)
          t.safety_stock += parseInt(a.safety_stock)
          if (a.past_price) t.past_price += parseFloat(a.past_price)
          if (a.receiving_price) t.receiving_price += parseFloat(a.receiving_price)
          if (a.release_price) t.release_price += parseFloat(a.release_price)
          if (a.closing_price) t.closing_price += parseFloat(a.closing_price)
          if (currentIndex === array.length - 1) {
                  t.past_price = Math.floor(t.past_price);
                  t.receiving_price = Math.floor(t.receiving_price);
                  t.release_price = Math.floor(t.release_price);
                  t.closing_price = Math.floor(t.closing_price);
          }
          return t
        }, {
          available_stock: 0,
          closing_stock: 0,
          current_stock: 0,
          past_stock: 0,
          receiving_stock: 0,
          release_stock: 0,
          safety_stock: 0,
          past_price: 0,
          receiving_price: 0,
          release_price: 0,
          closing_price: 0,
        })
      })
    })
    dataSource.status = result
  }
  catch (ex) {
    console.error(ex)
  }
  finally {
    components['status-list'].endCustomLoading()
  }
}

async function printProductReceipt () {
  if (!dataSource.detail) return

  const params = {}
  params.item = detailItem.value
  params.list = []

  params.info = {...formData}
  params.info.startDate = moment(params.info.startDate).format('YYYY년 M월 D일')
  params.info.endDate = moment(params.info.endDate).format('YYYY년 M월 D일')
  
  const list = [...dataSource.detail], months = []
  for (const item of list) {
    const d = moment(item.action_date)
    item.month = d.format('M월')
    if (!months.includes(item.month)) months.push(item.month)
    item.action_date = d.format('YYYY-MM-DD')
    item.past_stock_str = numeral(parseInt(item.past_stock)).format('0,0')
    item.receiving_stock_str = numeral(parseInt(item.receiving_stock)).format('0,0')
    item.release_stock_str = numeral(parseInt(item.release_stock)).format('0,0')
    item.sum_by_case_str = numeral(parseInt(item.sum_by_case)).format('0,0')
    item.unit_price_str = numeral(parseInt(item.unit_price)).format('0,0.00')
  }

  const acc = { input: 0, output: 0, stock: parseInt(list[0].past_stock || 0) }
  for (const month of months) {
    const item = {}
    item.month = month
    item.list = list.filter(v => v.month === month)
    item.mon_input = item.list.reduce((a, i) => a += i.receiving_stock, 0)
    item.mon_output = item.list.reduce((a, i) => a += i.release_stock, 0)

    acc.input += item.mon_input
    acc.output += item.mon_output
    acc.stock = acc.stock + item.mon_input - item.mon_output
    
    item.acc_input = acc.input
    item.acc_output = acc.output
    item.acc_stock = acc.stock

    params.list.push(item)
  }
  await printDocument('productreceiptsummary', params);
}

// async function exportData() {
//   if (!components['status-list']) return
//   stockMoveReleaseItem.exportData(components['status-list'], '재고이동출고현황', `재고이동출고현황_${Date.now()}.xlsx`);
// }
</script>

<style>
.summary-table {
  width: 100%;
  margin-top: 10px;
}
</style>