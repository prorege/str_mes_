<template>
  <dx-load-panel v-model:visible="loading" :show-pane="true" />
  <div class="content-block" v-if="loaded">
    <div class="dx-card responsive-paddings back-colored">
      <div class="content-header">
        <dx-toolbar class="back-colored">
          <dx-item location="before">
            <div class="content-title">생산진행상황</div>
          </dx-item>
          <dx-item
            location="after"
            widget="dxButton"
            :options="{
              text: '전체화면',
              type: 'normal',
              onClick: setFullscreen,
            }"
          />
        </dx-toolbar>
      </div>

      <div :key="refreshKey" ref="viewer" class="fullscreen-content">
        <dx-data-grid
          width="100%"
          height="100%"
          column-resizing-mode="widget"
          :data-source="dataSource"
          :show-borders="true"
          :row-alternation-enabled="true"
          :allow-column-reordering="true"
          :allow-column-resizing="true"
          :column-auto-width="true"
          :remote-operations="true"
          :on-initialized="evt => onGridInitialized(evt, 'status')"
        >
          <dx-grid-toolbar>
            <dx-item location="before" template="filter-tmpl" />
            <dx-item location="center" template="title-tmpl" />
            <dx-item location="after" template="date-tmpl" />
          </dx-grid-toolbar>

          <template #filter-tmpl>
            <DxSelectBox
              :value="warehouse.selected"
              :data-source="warehouse.items"
              value-expr="wh_code"
              display-expr="wh_name"
              @value-changed="warehouseChanged"
            />
          </template>

          <template #title-tmpl>
            <div class="status-title">
              생산 진행 현황 모니터링
            </div>
          </template>

          <template #date-tmpl>
            <div>일 시 : {{ currentDate }} {{ currentTime }}</div>
          </template>

          
          <dx-column
            data-field="item.item_name"
            caption="품명"
            css-class="column-dark"
            sort-order="asc"
          />
          <dx-column
            data-field="item.item_standard"
            caption="규격"
            css-class="column-dark"
          />
          <dx-column
            data-field="work_order_item.client_company"
            caption="수주고객업체"
            css-class="column-dark"
          />
          <dx-column
            data-field="order_number"
            caption="작지번호"
            css-class="column-dark"
          />
          <dx-column
            data-field="work_order_item.required_quantity"
            caption="지시수량"
            data-type="number"
            format="fixedPoint"
            css-class="column-green"
          />

          <dx-column
            caption="공정 진행 현황"
            css-class="column-green"
            cell-template="progress-tmpl"
          />
          <!-- dx-scrolling mode="infinite" / -->
          <dx-paging :page-size="vars.setting.page" />

          <template #progress-tmpl="{data}">
            <div class="progress-item-wrap">
              <div
                class="progress-item"
                :style="progressItemColor(idx)"
                v-for="(item, idx) in data.data.progress"
                :key="item.id"
              >
                <div class="progress-item-name">
                  <div>{{ item.process_name }}</div>
                  <!-- <div class="progress-item-count">
                    ({{ item.process_quantity }})
                  </div> -->
                </div>
              </div>
            </div>
          </template>
        </dx-data-grid>
      </div>
    </div>
  </div>
</template>

<script setup>
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import {
  DxDataGrid,
  DxColumn,
  DxSelection,
  DxEditing,
  DxPaging,
  DxFilterRow,
  DxScrolling,
  DxColumnChooser,
  DxLookup,
  DxToolbar as DxGridToolbar,
  DxItem as DxGridItem,
  DxRequiredRule as DxGridRequiredRule,
} from 'devextreme-vue/data-grid';
import { DxSelectBox } from 'devextreme-vue/select-box';
import { baseBom, baseBomProcess, getBaseWarehouse } from '@/data-source/base';
import {
  performanceItem1,
  getPerformanceItem1,
  processPerformanceRegistration,
} from '@/data-source/produce';
import { setupControl } from '@/data-source/setup';
import moment from 'moment';
import { onMounted, ref, reactive, onBeforeUnmount } from 'vue';
import authService from '../../auth';
import { useRoute } from 'vue-router'

//document.body.style.zoom = '1.8';
const vars = { dlg: {} };
const loading = ref(false);
const loaded = ref(false);
const viewer = ref(null);
const route = useRoute()
const refreshKey = ref(Date.now());
const common = { bom: [], process: [] };
vars.grid = { status: null };
vars.setting = reactive({
  page: 10,
});
let timerId = null;

const dataSource = ref([])
const currentDate = moment().format('YYYY-MM-DD');
const currentTime = ref(moment().format('HH:mm'));

const timerId2 = setInterval(() => {
  currentTime.value = moment().format('HH:mm');
}, 60 * 1000);

let timerId3
const warehouse = reactive({ selected: authService.getWarehouseCode(), items: [] })
const baseWarehouse = getBaseWarehouse()
baseWarehouse.load().then(({data}) => {
  warehouse.items = data
})

dataRefresh()

function warehouseChanged ({value}) {
  warehouse.selected = value
  dataRefresh()
}

async function dataRefresh () {
  clearTimeout(timerId3)

  const params = {
    skip: 0, 
    take: 3000, 
    sort: [{selector: 'item.item_name', desc: false}],
    filter: [
      ['work_order_item.end_yn', '=', false],
      ['work_order_item.unproduced_quantity', '>', 0]
    ]
  }

  if (warehouse.selected) {
    params.filter.push(['work_order_item.warehouse_code', '=', warehouse.selected])
  }

  const {data} = await processPerformanceRegistration.load(params)
  dataSource.value = groupByData(data)
  loaded.value = true
  
  if (route.path === "/monitoring/produce-progress") timerId3 = setTimeout(() => dataRefresh(), 5 * 1000)
}

document.onfullscreenchange = () => {
  if (!document.fullscreenElement) {
    // if (timerId) clearTimeout(timerId);
    // timerId = setTimeout(() => {
    //   refreshKey.value = Date.now();
    //   timerId = null;
    // }, 1000);
  }
};

onMounted(async () => {
  const { data } = await setupControl.load({
    filter: [['fk_company_id', '=', authService.getCompanyId()]],
    take: 1,
    skip: 0,
  });
  if (data.length > 0) {
    //document.body.style.zoom = data[0].monitoring_zoom;
    vars.setting.page = data[0].monitoring_page;
  }
});

onBeforeUnmount(() => {
  if (timerId) clearTimeout(timerId);
  document.onfullscreenchange = null;
  //document.body.style.zoom = '1.0';
  clearInterval(timerId2);
  clearTimeout(timerId3);
});

function onGridInitialized(evt, key) {
  vars.grid[key] = evt.component;
}

function setFullscreen() {
  if (!viewer.value) return;
  viewer.value.requestFullscreen();
}

function groupByData (data) {
  let list = []
  for (const item of data) {
    const exists = list.find(v => v.fk_work_order_item === item.fk_work_order_item)
    if (exists) {
      const proc = exists.progress.find(v => v.id === item.fk_process_id)
      if (proc) proc.process_quantity += item.process_quantity
      else exists.progress.push({ 
        id: item.process.id, 
        process_name: item.process.process_name, 
        process_quantity: item.process_quantity
      })
    }
    else {
      item.progress = [{
        id: item.process.id, 
        process_name: item.process.process_name, 
        process_quantity: item.process_quantity
      }]
      list.push(item)
    }
  }

  for (const item of list) {
    item.progress = item.progress.filter(prog => prog.process_quantity >= item.work_order_item.required_quantity)
  }
   
  list = list.filter(item => item.progress.length && !item.progress.find(v => v.process_name === '포장'))
  return list
}

function progressItemColor(idx = 0) {
  const colors = [
    '#4572A7',
    '#AA4643',
    '#89A54E',
    '#80699B',
    '#3D96AE',
    '#DB843D',
    '#92A8CD',
    '#A47D7C',
    '#B5CA92',
  ];

  return { backgroundColor: colors[idx % 9] };
}

function getProgressBox({ data }) {
  console.log(data)
  const bom = common.bom.find(v => v.item_id === data.item.id);
  if (!bom) return [];
  const process = common.process.filter(v => v.bom_id === bom.id);
  process.forEach(v => {
    if (v.id === data.fk_process_id) v.count = data.process_quantity;
  });
  return process;
}
</script>

<style lang="scss" scoped>
.dx-card {
  width: 100%;
}
.fullscreen-content {
  position: relative;
  width: 100%;
  height: calc(100vh - 160px);
  margin-top: 10px;
  padding: 12px;
  border: 1px solid #d7d7d7;
  border-radius: 4px;

  box-sizing: border-box;
  background-color: white;
}

.chart-item {
  width: 100%;
  height: 100%;
  padding: 10px;
  box-sizing: border-box;
  border-radius: 4px;
  background-color: #d7d7d7;
  .chart-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    color: #808080;
    font-size: 16px;
    .item-info {
    }
    .work-info {
    }
  }
  .chart-content {
    width: calc(100% - 20px);
    height: calc(100% - 20px);
    padding: 10px;
    box-sizing: border-box;
  }
}
.progress-item {
  display: inline-block;
  width: 160px;
  height: 30px;
  margin: 0 10px;
  border-radius: 5px;
  background-color: #f7f7f7;
  position: relative;
  overflow: hidden;

  color: white;
  border: 1px solid white;
  box-shadow: 0px 2px 4px rgb(0 0 0 / 40%);
}
.progress-item-bar {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  background-color: #c2cf9f;
  z-index: 1;
}
.progress-item-name {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  z-index: 2;
}
.progress-item-count {
  color: #b4b4b4;
  margin-left: 4px;
}
</style>
