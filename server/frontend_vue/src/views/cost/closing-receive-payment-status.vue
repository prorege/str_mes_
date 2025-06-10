.<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">원가마감 재고수불집계</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div v-if="commonInit">
          <div>
            <div class="search-status search-line">
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
            <div class="search-status">
              <dx-check-box text="비유동재고" v-model:value="formData.zero_stock" :on-value-changed="zeroStockChanged" />
            </div>
          </div>
        </div>

      </div>

      <div class="dx-card responsive-paddings mt-1">
        <dx-data-grid
          key-expr="id"
          height="calc(100vh - 280px)"
          column-resizing-mode="widget"
          :data-source="dataSource.status"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="false"
          :focused-row-enabled="true"
          :filter-sync-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          @row-dbl-click="goDetail"
          @initialized="evt => initialized(evt, 'status-list')"
        >
          <dx-column caption="자산구분" data-field="asset_type" :filter-operations="['contains', '=']" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item_name" />
          <dx-column caption="규격" data-field="item_standard" />
          <dx-column caption="이월재고" data-field="past_stock" data-type="number" format=",##0" />
          <dx-column caption="이월금액" data-field="past_price" data-type="number" format="₩,##0" />
          <dx-column caption="입고량" data-field="receiving_stock" data-type="number" format=",##0" :filter-value="filter.receiving_stock" />
          <dx-column caption="입고금액" data-field="receiving_price" data-type="number" format="₩,##0" />
          <dx-column caption="출고량" data-field="release_stock" data-type="number" format=",##0" :filter-value="filter.release_stock" />
          <dx-column caption="출고원가금액" data-field="release_price" data-type="number" format="₩,##0" />
          <dx-column caption="마감재고" data-field="closing_stock" data-type="number" format=",##0" />
          <dx-column caption="마감재고금액" data-field="closing_price" data-type="number" format="₩,##0" />
          <dx-column caption="품목대분류" data-field="main_category" />

          <dx-summary>
            <dx-total-item column="past_price" summary-type="sum" value-format="₩,##0" display-format="이월금액: {0}" />
            <dx-total-item column="receiving_price" summary-type="sum" value-format="₩,##0" display-format="입고금액: {0}" />
            <dx-total-item column="release_price" summary-type="sum" value-format="₩,##0" display-format="출고원가금액: {0}" />
            <dx-total-item column="closing_price" summary-type="sum" value-format="₩,##0" display-format="마감재고금액: {0}" />
          </dx-summary>

          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-export :enabled="true" />
        </dx-data-grid>
      </div>
    </div>

    <dx-popup
      v-model:visible="dialog"
      content-template="popup-content"
      title="원가 재고수불내역"
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
          text: '원가 재고수불장 출력',
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
          <dx-column caption="단가" data-field="unit_price" data-type="number" format="₩,##0.00" />
          <dx-column caption="이월재고" data-field="past_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="이월재고금액" data-field="past_price" data-type="number" format="₩,##0.0000" />
          <dx-column caption="입고수량" data-field="receiving_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="입고금액" data-field="receiving_price" data-type="number" format="₩,##0.0000" />
          <dx-column caption="출고수량" data-field="release_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="출고원가금액" data-field="release_price" data-type="number" format="₩,##0.0000" />
          <dx-column caption="누적재고" data-field="sum_by_case" data-type="number" format="fixedPoint" />
          <dx-column caption="누적재고금액" data-field="sum_by_price" data-type="number" format="₩,##0.0000" />
          <dx-column caption="입출고번호" data-field="number" />
          <dx-column caption="누적입고수량" data-field="accumulate_receiving_stock" data-type="number" format="fixedPoint" :visible="false" />
          <dx-column caption="누적출고수량" data-field="accumulate_release_stock" data-type="number" format="fixedPoint" :visible="false" />
          <dx-column caption="누적출고금액" data-field="accumulate_release_price" data-type="number" format="₩,##0.0000" :visible="false" />

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
              column="receiving_price"
              summary-type="sum"
              value-format="₩,##0.0000"
              display-format="입고금액: {0}"
            />
            <dx-group-item
              :align-by-column="true"
              column="release_stock"
              summary-type="sum"
              value-format="fixedPoint"
              display-format="출고수량: {0}"
            />
            <dx-group-item
              :align-by-column="true"
              column="release_price"
              summary-type="sum"
              value-format="₩,##0.0000"
              display-format="출고원가금액: {0}"
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
              column="accumulate_receiving_price"
              summary-type="max"
              value-format="₩,##0.0000"
              show-in-column="receiving_price"
              display-format="누적입고금액: {0}"
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
              column="accumulate_release_price"
              summary-type="max"
              value-format="₩,##0.0000"
              show-in-column="release_price"
              display-format="누적출고금액: {0}"
            />
            <dx-group-item
              :show-in-group-footer="true"
              name="last_stock_summary"
              summary-type="custom"
              value-format="fixedPoint"
              show-in-column="sum_by_case"
              display-format="누적재고수량: {0}"
            />
            <dx-group-item
              :show-in-group-footer="true"
              name="last_stock_price"
              summary-type="custom"
              value-format="₩,##0.0000"
              show-in-column="sum_by_price"
              display-format="누적재고금액: {0}"
            />
          </dx-summary>

          <dx-paging :page-size="10" />
        </dx-data-grid>

        <div class="mt-2">
          <table class="summary-table-wide">
            <tr>
              <td>누계</td>
              <th>이월재고</th>
              <td>{{ dataSource.sum.past_stock }}</td>
              <th>이월재고금액</th>
              <td>{{ dataSource.sum.past_price }}</td>
              <th>입고수량</th>
              <td>{{ dataSource.sum.receiving_stock }}</td>
              <th>입고금액</th>
              <td>{{ dataSource.sum.receiving_price }}</td>
              <th>출고수량</th>
              <td>{{ dataSource.sum.release_stock }}</td>
              <th>출고원가금액</th>
              <td>{{ dataSource.sum.release_price }}</td>
              <th>누적재고</th>
              <td>{{ dataSource.sum.sum_by_case }}</td>
              <th>누적재고금액</th>
              <td>{{ dataSource.sum.sum_by_price }}</td>
            </tr>
          </table>
        </div>
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
  DxExport,
} from 'devextreme-vue/data-grid';
import DxCheckBox from 'devextreme-vue/check-box';
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
  category: '',
  zero_stock: false,
});
const filter = reactive({
  receiving_stock: null,
  release_stock: null,
})

const components = {};

const dataSource = reactive({
  warehouse: [],
  assetType: [],
  category: [],
  status: [],
  detail: [],
  sum: {
    past_stock: 0,
    past_price: 0,
    receiving_stock: 0,
    receiving_price: 0,
    release_stock: 0,
    release_price: 0,
    sum_by_case: 0,
    sum_by_price: 0,
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

  dataSource.warehouse = dataSource.warehouse.filter(warehouse => warehouse.use_cost_closing)

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
  } else if (options.name === 'last_stock_price') {
    if (options.summaryProcess === 'start') {
      options.totalValue = 0;
    } else if (options.summaryProcess === 'calculate') {
      options.totalValue = options.value.sum_by_price;
    }
  }
}

async function goDetail({ data }) {
  detailItem.value = data

  const params = {
    item_code: data.item_code,
    warehouse_name: formData.warehouseName,
    start: moment(formData.startDate).format('YYYYMMDD'),
    end: moment(formData.endDate).endOf('day').format('YYYY-MM-DD HH:mm:ss'),
  };
  const { data: response } = await api.post('item', params);

  let sumByCase = 0;
  let sumReceivingStock = 0;
  let sumReleaseStock = 0;
  let sumByPrice = 0.0;
  let sumReceivingPrice = 0.0;
  let sumReleasePrice = 0.0;
  response.objects.forEach(row => {
    sumByCase = sumByCase + (parseInt(row.past_stock, 10) + row.receiving_stock - row.release_stock);
    row.sum_by_case = sumByCase;
    sumReceivingStock = sumReceivingStock + row.receiving_stock;
    row.accumulate_receiving_stock = sumReceivingStock;
    sumReleaseStock = sumReleaseStock + row.release_stock;
    row.accumulate_release_stock = sumReleaseStock;
    row.unit_price = Math.floor(Number(row.unit_price) * 100) / 100;
    sumByPrice = sumByPrice + (row.past_price + row.receiving_price - row.release_price);
    if (sumByCase == 0 && sumByPrice < 1) sumByPrice = 0
    row.sum_by_price = sumByPrice;
    row.sum_by_price = sumByPrice;
    sumReceivingPrice = parseFloat(sumReceivingPrice) + parseFloat(row.receiving_price);

    row.accumulate_receiving_price = sumReceivingPrice;
    sumReleasePrice = parseFloat(sumReleasePrice) + parseFloat(row.release_price);
    row.accumulate_release_price = sumReleasePrice;
  });
  dataSource.detail = response.objects;
  dataSource.sum.past_stock = numeral(response.objects.reduce((sum, row) => sum + parseInt(row.past_stock, 10), 0)).format('0,0');
  dataSource.sum.receiving_stock = numeral(response.objects.reduce((sum, row) => sum + row.receiving_stock, 0)).format('0,0');
  dataSource.sum.release_stock = numeral(response.objects.reduce((sum, row) => sum + row.release_stock, 0)).format('0,0');
  dataSource.sum.sum_by_case = numeral(sumByCase).format('0,0');

  dataSource.sum.past_price = numeral(response.objects.reduce((sum, row) => sum + parseFloat(row.past_price, 10), 0)).format('0,0.0000');
  dataSource.sum.receiving_price = numeral(response.objects.reduce((sum, row) => sum + parseFloat(row.receiving_price, 10), 0)).format('0,0.0000');
  dataSource.sum.release_price = numeral(response.objects.reduce((sum, row) => sum + parseFloat(row.release_price, 10), 0)).format('0,0.0000');
  dataSource.sum.sum_by_price = numeral(sumByPrice).format('0,0.0000');

  dialog.value = true;
}

async function searchDateRange() {
  try {
    components['status-list'].beginCustomLoading('데이터를 집계중입니다')
    const params = {
      start: moment(formData.startDate).startOf('day').format('YYYY-MM-DD HH:mm:ss'),
      end: moment(formData.endDate).endOf('day').format('YYYY-MM-DD HH:mm:ss'),
      wh_name: formData.warehouseName === '전체' ? '' : formData.warehouseName,
      asset_type: formData.assetType === '전체' ? '' : formData.assetType,
      category: formData.category === '전체' ? '' : formData.category,
    };
    const { data } = await api.get('', { params });
    for (const item of data.objects) {
      item.past_price = Math.round(item.past_price);
      item.receiving_price = Math.round(item.receiving_price);
      item.release_price = Math.round(item.release_price);
      item.closing_price = Math.round(item.closing_price);
    }

    dataSource.status = data.objects;
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
  
  const list = [...dataSource.detail], years = {}
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
      item.mon_input = item.list.reduce((a, i) => a += i.receiving_stock, 0)
      item.mon_input_str = numeral(item.mon_input).format('0,0')
      item.mon_output = item.list.reduce((a, i) => a += i.release_stock, 0)
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
}

function zeroStockChanged(e) {
  if (e.value) {
    filter.receiving_stock = 0;
    filter.release_stock = 0;
  } else {
    filter.receiving_stock = null;
    filter.release_stock = null;
  }
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
