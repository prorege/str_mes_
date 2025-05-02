<script setup>
import {ref} from 'vue'
import {
  DxDataGrid,
  DxColumn,
  DxPaging,
  DxSorting,
  DxFilterRow,
  DxColumnChooser,
  DxMasterDetail,
  DxExport,
  DxGroupPanel,
  DxGrouping,
  DxSummary,
  DxGroupItem,
  DxEditing,
  DxPopup,
  DxForm,
  DxItem as DxGridItem
} from 'devextreme-vue/data-grid'
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar'
import { DxDateBox } from 'devextreme-vue/date-box'
import DxButton from 'devextreme-vue/button'
import moment from 'moment'
import SearchButtonGroup from '@/components/search-button-group.vue'
import DxCheckBox from 'devextreme-vue/check-box'

import {baseCode } from '@/data-source/base'
import {processPerformanceRegistration, performanceItem1, getProcessMaterialConsumption} from '@/data-source/produce'
import authService from '@/auth'

import {groupBy} from 'lodash'
import { getBaseBom, getBaseBomProcess } from '../../data-source/base'

const ready = ref(false)
const grid = ref(null)
const materialGrid = ref(null)
const groupView = ref(undefined)
const dataSource = ref([])
const employeeList = ref([])
const formData = ref({
  startDate: new Date(),
  endDate: new Date(),
})

const processMaterialConsumption = getProcessMaterialConsumption()
const materialGridData = getProcessMaterialConsumption()

let currentProcessNumber = undefined

loadManager().then(() => ready.value = true)

function init (component) {
  grid.value = component
  searchDateRange()
}

function onInitMaterialGrid (component) {
  materialGrid.value = component
  if (currentProcessNumber) {
    component.filter(['process_number', '=', currentProcessNumber])
  }
}

async function loadManager () {
  const {data: parentItem} = await baseCode.load({filter: [['code_name', '=', '현장공정담당자'], 'and', ['fk_company_id', '=', authService.getCompanyId()]]})
  if (!parentItem.length) return
  const parentId = parentItem[0].id

  const {data: codes} = await baseCode.load({filter: ['parent_code_id', '=', parentId]})
  employeeList.value = codes
}

function getParams (key) {
  return { 
    filter: [
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
    ],
    skip: 0,
    take: 3000
  }
}

async function searchDateRange () {
  if (formData.value.startDate > formData.value.endDate) {
    await alert('조회 일자가 잘못 되었습니다', '조회');
    return;
  }
  grid.value.beginCustomLoading('데이터를 집계중입니다')
  const params = getParams('created')
  params.sort = [{selector : 'fk_process_id', desc: true}]
  const {data} = await processPerformanceRegistration.load(params)
  const groupByOrder = await getPerformanceItems()
  data.forEach(v => workHour(v))
  
 for (const orderNumber in groupBy(data, 'order_number')) {
    const item = data.find(v => v.order_number === orderNumber);
    const processTags = groupBy(data, 'order_number')[orderNumber]?.map(i => i.process_tag).filter(tag => tag !== null);

    item.lot = processTags && processTags.length > 0 ? processTags.filter(tag => tag).join(', ') : "-";

    if (!groupByOrder[orderNumber]) continue;
    const summary = groupByOrder[orderNumber].reduce((t, i) => {
      t.production_receiving_quantity += i.production_receiving_quantity;
      t.bad_quantity += i.bad_quantity;
      t.good_quantity += i.good_quantity;
      return t;
    }, { production_receiving_quantity: 0, bad_quantity: 0, good_quantity: 0 });

    item.sum_receiving_quantity = summary.production_receiving_quantity;
    item.sum_bad_quantity = summary.bad_quantity;
    item.sum_good_quantity = summary.good_quantity;



    let baseBom = getBaseBom({})
    let {data : base_bom} = await baseBom.load({ filter: ['item_id', '=', item.item.id] });

    const bomProcess = getBaseBomProcess({})
    const {data: baseBomProcess} = await bomProcess.load({filter: [['bom_id', '=', base_bom[0].id], ['process_id', '=', item.process.id]]})
 
    if(!baseBomProcess[0].ct)continue

    data.filter(v => v.order_number === orderNumber && v.process.id === 8).forEach(v => v.base_bom_process_ct = baseBomProcess[0].ct)
  }
  grid.value.endCustomLoading()
  dataSource.value = data
}
async function getPerformanceItems () {
  const params = getParams('created')
  const {data} = await performanceItem1.load(params)
  return groupBy(data, 'work_order_number')
}

function workHour (rowData) {
  if (!rowData.work_start_time || !rowData.work_end_time) {
    rowData.formatted_rest = '00:00';
    rowData.work_duration_min = 0;
    rowData.work_duration = '00:00';
    rowData.sum_receiving_quantity = 0;
    rowData.sum_bad_quantity = 0;
    rowData.sum_good_quantity = 0;
    return;
  }

  const start = moment(rowData.work_start_time, 'HH:mm');
  const end = moment(rowData.work_end_time, 'HH:mm');

  const rest = moment.duration(rowData.work_rest_time || '00:00');
  const workCont = rowData.worker ? rowData.worker.split(',').length : 1;
  const restMinute = rest.asMinutes() * workCont;

  
  const hours = Math.floor(restMinute / 60);
  const minutes = restMinute % 60;

  const formattedRest = moment({ hours, minutes }).format('HH:mm');

  const adj = end.subtract(rest);
  const min = adj.diff(start, 'minute') * workCont;

  rowData.workerArr = rowData.worker.split(',')
  rowData.formatted_rest = formattedRest
  rowData.work_duration_min = min
  rowData.work_duration = `${String(Math.floor(min / 60)).padStart(2, '0')}:${String(min % 60).padStart(2, '0')}`

  rowData.sum_receiving_quantity = 0
  rowData.sum_bad_quantity = 0
  rowData.sum_good_quantity = 0
}
function calculateDisplayValue(rowData){
  if(rowData.fk_process_id === 8){
    return Math.round(rowData.work_duration_min / (rowData.process_quantity - rowData.bad_quantity) * 100) / 100;
  }

}
function timeToStr ({value}) {
  return `작업시간: ${String(Math.floor(value / 60)).padStart(2, '0')}:${String(value % 60).padStart(2, '0')}`
}

function sumOfQty (name) {
  return ({value}) => `${name}: ${value}`
}

function getProcessTag ({value}) {
  return `생산주차: ${value}`
}

function setEditMode (e) {
  if (e.column.type === 'button') return
  currentProcessNumber = e.data.number
  if (materialGrid.value) materialGrid.value.filter(['process_number', '=', currentProcessNumber])
  e.component.editRow(e.rowIndex)
}

async function onSaving (e) {
  for (const {data, key, type} of e.changes) {
    switch (type) {
      case 'update': {
        await processPerformanceRegistration.update(key, {
          bad_quantity: data.bad_quantity,
          process_quantity: data.process_quantity,
          work_end_time: data.work_end_time,
          work_rest_time: data.work_rest_time,
          work_start_time: data.work_start_time
        })
        break
      }
      case 'remove': {
        const { data } = await processMaterialConsumption.load({ filter: ['process_number', '=', key] })
        for (const item of data) {
          await processMaterialConsumption.remove(item.id)
        }
        await processPerformanceRegistration.remove(key)
        break
      } 
    }
  }
}
</script>

<template>
    <div class="content-block" v-if="ready">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">공정실적등록현황</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div>
          <div class="search-status">
            <span class="search-title">실적등록일자</span>
            <dx-date-box v-model:value="formData.startDate" />
            
            <span class="search-bar">~</span>
            <dx-date-box v-model:value="formData.endDate" />
            
            <span class="search-tab"></span>
            <SearchButtonGroup @change="({startDate, endDate}) => { formData.startDate = startDate; formData.endDate = endDate; }" />
            
              <span class="search-tab"></span>
            <dx-button text="검색" icon="search" @click="searchDateRange()" />

            <span class="search-tab"></span>
            <DxCheckBox text="요약보기" @value-changed="({value}) => groupView = value ? 0 : undefined" />
          </div>
        </div>

      </div>
      <div class="dx-card responsive-paddings mt-1">
        <dx-data-grid
          height="calc(100vh - 230px)"
          key-expr="number"
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="false"
          :focused-row-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :data-source="dataSource"
          @saving="onSaving"
          @cell-dbl-click="setEditMode"
          @initialized="({component}) => init(component)"
        >
          <dx-column caption="작지번호" data-field="order_number" :group-index="groupView" />
          <dx-column caption="실적번호" data-field="number" :filter-operations="['contains', '=']" />
          <dx-column caption="실적등록일자" data-field="created" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" :sort-index="0" sort-order="desc" />
          <dx-column caption="생산품명" data-field="item.item_name" :allow-sorting="false" />
          <dx-column caption="담당자" data-field="worker" />
          <dx-column caption="공정명" data-field="process.process_name" :allow-sorting="false" />
          <dx-column caption="작업시작" data-field="work_start_time" />
          <dx-column caption="작업종료" data-field="work_end_time" />
          <dx-column caption="휴게시간" data-field="formatted_rest" />
          <dx-column caption="휴게시간" data-field="work_rest_time" :allow-sorting="false" :visible="false"/>
          <dx-column caption="작업시간" data-field="work_duration" :allow-sorting="false" />
          <dx-column caption="완료수량" data-field="process_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="불량수량" data-field="bad_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="공임공수" data-field="base_bom_process_ct" />
          <dx-column caption="개당공수" :calculate-display-value="calculateDisplayValue" />
          <dx-column caption="품목코드" data-field="item.item_code" :allow-sorting="false" />
          <dx-column caption="단위" data-field="item.unit" :allow-sorting="false" />
          <dx-column caption="고객업체약칭" data-field="work_order_item.client_alias" :allow-sorting="false" />
          <dx-column caption="고객업체" data-field="work_order_item.client_company" :allow-sorting="false" />
          <dx-column caption="품목설명" data-field="item.item_detail" :allow-sorting="false" />
          <dx-column caption="입고합계" data-field="sum_receiving_quantity" :allow-sorting="false" />
          <dx-column caption="불량합계" data-field="sum_bad_quantity" :allow-sorting="false" />
          <dx-column caption="양품합계" data-field="sum_good_quantity" :allow-sorting="false" />
          <dx-column caption="process_tag" data-field="process_tag" :allow-sorting="false" />

          <DxGroupPanel :visible="false"/>
          <DxGrouping :auto-expand-all="true"/>
          <DxSummary>
            <DxGroupItem column="work_duration_min" summary-type="sum" :customize-text="timeToStr" />
            <DxGroupItem column="sum_receiving_quantity" summary-type="sum" :customize-text="sumOfQty('입고합계')" />
            <DxGroupItem column="bad_quantity" summary-type="sum" :customize-text="sumOfQty('불량합계')" />
            <DxGroupItem column="sum_good_quantity" summary-type="sum" :customize-text="sumOfQty('양품합계')" />
            <DxGroupItem column="lot" summary-type="max" :customize-text="getProcessTag" />
          </DxSummary>

          <DxEditing mode="popup"
            :use-icons="true"  
            :allow-updating="true"
            :allow-adding="false"
            :allow-deleting="true"
          >
            <DxPopup title="공정실적등록정보 수정"
              :show-title="true"
              :width="700"
              :height="720"
            />
            <DxForm :show-colon-after-label="false">
              <!-- <DxGridItem data-field="worker" editor-type="dxTagBox"
                :editor-options="{ dataSource: employeeList, displayExpr: 'code_name', valueExpr: 'code_name' }"
              /> -->
              <DxGridItem data-field="work_start_time" editor-type="dxDateBox"
                :editor-options="{ type: 'time', pickerType: 'rollers', displayFormat: 'HH:mm' }"
              />
              <DxGridItem data-field="work_end_time" editor-type="dxDateBox"
                :editor-options="{ type: 'time', pickerType: 'rollers', displayFormat: 'HH:mm' }"
              />
              <DxGridItem data-field="work_rest_time" editor-type="dxDateBox"
                :editor-options="{ type: 'time', pickerType: 'rollers', displayFormat: 'HH:mm' }"
              />
              <DxGridItem data-field="process_quantity" data-type="number" />
              <DxGridItem data-field="bad_quantity" data-type="number" />
              <DxGridItem item-type="empty"></DxGridItem>

              <DxGridItem :col-span="2" item-type="group">
                <DxGridItem item-type="simple">
                  <template #default>
                    <dx-data-grid
                      height="410px"
                      column-resizing-mode="widget"
                      :show-borders="true"
                      :column-auto-width="true"
                      :remote-operations="true"
                      :focused-row-enabled="true"
                      :allow-column-resizing="true"
                      :allow-column-reordering="true"
                      :row-alternation-enabled="true"
                      :data-source="materialGridData"
                      @initialized="({component}) => onInitMaterialGrid(component)"
                    >
                      <dx-column caption="ID" data-field="id" :visible="false" :allow-editing="false" sort-order="desc" :show-in-column-chooser="false" />
                      <dx-column caption="자재LOT번호" data-field="lot_number" :allow-editing="false" />
                      <dx-column caption="품목코드" data-field="item_code" :allow-editing="false" />
                      <dx-column caption="투입수량" data-field="quantity" :allow-editing="false" />
                      <dx-column caption="생성시간" data-field="created" :visible="false" :allow-editing="false" />
                      <dx-column caption="생산실적번호" data-field="process_number" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />

                      <dx-paging :page-size="3"/>
                      <dx-editing mode="batch" :use-icons="true" :allow-adding="false" :allow-updating="false" :allow-deleting="false" />
                    </dx-data-grid>
                  </template>
                </DxGridItem>
              </DxGridItem>
            </DxForm>
          </DxEditing>

          <dx-export :enabled="true" />
          <dx-paging :page-size="20" />
          <dx-sorting mode="single" />
          <dx-filter-row :visible="true" />
          <dx-column-chooser mode="select" :enabled="true" />
        </dx-data-grid>
      </div>
    </div>
</template>