<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">출고원가보정</div>
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
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="false"
          :focused-row-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :data-source="dataSource.status"
          :on-row-updating="onRowUpdating"
          @initialized="evt => initialized(evt, 'status-list')"
        >
          <dx-column caption="출고일자" data-field="release_date" data-type="datetime" format="yyyy-MM-dd HH:mm:ss" :sort-index="1" sort-order="desc" :allow-editing="false" />
          <dx-column caption="출고번호" data-field="release_number" data-type="string" :allow-editing="false" />
          <dx-column caption="품목대분류" data-field="main_category" data-type="string" :allow-editing="false" />
          <dx-column caption="출고구분" data-field="menu_type" data-type="string" :allow-editing="false" />
          <dx-column caption="출고유형" data-field="release_type" data-type="string" :allow-editing="false" />
          <dx-column caption="품목코드" data-field="item_code" data-type="string" :allow-editing="false" />
          <dx-column caption="품명" data-field="item_name" data-type="string" :allow-editing="false" />
          <dx-column caption="규격" data-field="item_standard" data-type="string" :allow-editing="false" />
          <dx-column caption="출고수량" data-field="release_quantity" data-type="number" format="fixedPoint" :allow-editing="false" />
          <dx-column caption="출고단가" data-field="unit_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" :allow-editing="false" />
          <dx-column caption="출고원가" data-field="cost_price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
          <dx-column caption="아이디" data-field="item_id" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />

          <dx-paging :page-size="20" />
          <dx-export :enabled="true" />
          <dx-filter-row :visible="true" />
          <dx-editing mode="batch"
            :allow-updating="true"
          />
        </dx-data-grid>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  DxDataGrid,
  DxColumn,
  DxPaging,
  DxEditing,
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
import { shipmentReleaseItem } from '../../data-source/shipment';
import { stockEtcItem, stockMoveReleaseItem } from '../../data-source/stock';
import authService from '../../auth';
import { loadWarehouse } from '../../utils/data-loader';
import moment from 'moment';
import numeral from 'numeral';
import { groupBy } from 'lodash'
import {printDocument} from '@/utils/print-document';

const api = new ApiService('/api/mes/v1/cost/correction');
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
    console.log(data);
    dataSource.status = data.objects
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

function onRowUpdating(e) {
  if (e.oldData.menu_type == '출고') {
    shipmentReleaseItem.update(e.oldData.item_id, {
      cost_price: e.newData.cost_price
    });
  } else if (e.oldData.menu_type == '기타출고') {
    stockEtcItem.update(e.oldData.item_id, {
      cost_price: e.newData.cost_price
    });
  } else if (e.oldData.menu_type == '재고이동출고') {
    stockMoveReleaseItem.update(e.oldData.item_id, {
      cost_price: e.newData.cost_price
    });
  }
}

// async function exportData() {
//   if (!components['status-list']) return
//   stockMoveReleaseItem.exportData(components['status-list'], '재고이동출고현황', `재고이동출고현황_${Date.now()}.xlsx`);
// }
</script>