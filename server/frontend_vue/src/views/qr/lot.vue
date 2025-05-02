<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">LOT관리</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div>
          <div class="search-status">
            <span class="search-bar">생산주차</span>
            <dx-text-box v-model:value="vars.formData.lot" @enter-key="methods.searchByProcessTag" />
            <span class="search-tab"></span>
            <dx-button text="생산주차로 검색" icon="search" @click="methods.searchByProcessTag()" />
          </div>
        </div>
        
      </div>

      <div class="dx-card responsive-paddings mt-1">
        <DxTabPanel
          :defer-rendering="false"
          @selection-changed="methods.tabChange">
          <DxTabPanelItem title="구매입고">
            <dx-data-grid
              class="table-margin"
              height="calc(100vh - 300px)"
              column-resizing-mode="widget"
              :show-borders="true"
              :column-auto-width="true"
              :remote-operations="true"
              :focused-row-enabled="true"
              :allow-column-resizing="true"
              :allow-column-reordering="true"
              :row-alternation-enabled="true"
              :data-source="purchaseReceivingItem"
              @initialized="evt => methods.initStatusGrid(evt.component)"
              @exporting="methods.onExporting"
              @row-dbl-click="methods.goReceivingDetail"
            >
              <dx-column caption="입고번호" data-field="receiving.receiving_number" :filter-operations="['contains', '=']" />
              <dx-column caption="입고일자" data-field="receiving.receiving_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
              <dx-column caption="공급업체" data-field="receiving.client_company" />
              <dx-column caption="입고부서" data-field="receiving.receiving_department" />
              <dx-column caption="입고담당자" data-field="receiving.receiving_manager" />
              <dx-column caption="입고구분" data-field="receiving.receiving_type" />
              <dx-column caption="품목코드" data-field="item_code" />
              <dx-column caption="품명" data-field="item.item_name" />
              <dx-column caption="규격" data-field="item.item_standard" />
              <dx-column caption="LOT번호" data-field="lot_number" />
              <dx-column caption="공급처LOT번호" data-field="supplier_lot_number" />
              <dx-column caption="발주수량" data-field="order_quantity" data-type="number" format="fixedPoint" />
              <dx-column caption="입고수량" data-field="receiving_quantity" data-type="number" format="fixedPoint" />
              <dx-column caption="단가" data-field="unit_price" :format="{ type: 'fixedPoint', precision: 2 }" />
              <dx-column caption="단위" data-field="item.unit" />
              <dx-column caption="공급가" data-field="supply_price" :format="{ type: 'fixedPoint', precision: 2 }" />
              <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
              <dx-column caption="품목대분류" data-field="item.main_category" />
              <dx-column caption="품목중분류" data-field="item.middle_category" />
              <dx-column caption="품목소분류" data-field="item.sub_category" />
              <dx-column caption="발주번호" data-field="order_number" />
              <dx-column caption="공급사품번" data-field="client_item_number" />
              <dx-column caption="품목설명" data-field="item.item_detail" />
              <dx-column caption="참고사항" data-field="note" />
              <dx-column caption="프로젝트번호" data-field="project_management.project_number" />
              <dx-column caption="종결" data-field="closing_yn" />

              <dx-sorting mode="single" />
              <dx-export :enabled="true" />
              <dx-paging :page-size="20" />
              <dx-column-chooser mode="select" :enabled="true" />
            </dx-data-grid>
          </DxTabPanelItem>
          <DxTabPanelItem title="생산입고">
            <dx-data-grid
              class="table-margin"
              height="calc(100vh - 300px)"
              column-resizing-mode="widget"
              :show-borders="true"
              :column-auto-width="true"
              :remote-operations="false"
              :focused-row-enabled="true"
              :allow-column-resizing="true"
              :allow-column-reordering="true"
              :row-alternation-enabled="true"
              :data-source="processItemStore"
              @initialized="evt => methods.initProduceGrid(evt.component)"
              @exporting="methods.onExporting"
            >
              <dx-column caption="생산실적번호" data-field="number" :filter-operations="['contains', '=']" />
              <dx-column caption="작지번호" data-field="order_number" :filter-operations="['contains', '=']" />
              <dx-column caption="생산일자" data-field="created" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
              <dx-column caption="생산주차" data-field="process_tag" />
              <dx-column caption="품목코드" data-field="item_code" />
              <dx-column caption="품명" data-field="item.item_name" />
              <dx-column caption="규격" data-field="item.item_standard" />
              <dx-column caption="담당자" data-field="worker" />
              <dx-column caption="작업시작" data-field="work_start_time" />
              <dx-column caption="작업종료" data-field="work_end_time" />
              <dx-column caption="휴게시간" data-field="work_rest_time" />
              <dx-column caption="완료수량" data-field="process_quantity" data-type="number" format="fixedPoint" />
              <dx-column caption="불량수량" data-field="bad_quantity" data-type="number" format="fixedPoint" />
              <dx-column caption="단위" data-field="item.unit" :allow-sorting="false" />

              <dx-sorting mode="single" />
              <dx-export :enabled="true" />
              <dx-paging :page-size="20" />
              <dx-column-chooser mode="select" :enabled="true" />
            </dx-data-grid>
          </DxTabPanelItem>
          <DxTabPanelItem title="출고">
            <dx-data-grid
              class="table-margin"
              height="calc(100vh - 300px)"
              column-resizing-mode="widget"
              :show-borders="true"
              :column-auto-width="true"
              :remote-operations="true"
              :focused-row-enabled="true"
              :allow-column-resizing="true"
              :allow-column-reordering="true"
              :row-alternation-enabled="true"
              :data-source="shipmentReleaseItem"
              @initialized="evt => methods.initReleaseGrid(evt.component)"
              @exporting="methods.onExporting"
            >
            <dx-column caption="출고번호" data-field="release.release_number" :filter-operations="['contains', '=']" />
            <dx-column caption="출고일자" data-field="release.release_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
            <dx-column caption="생산주차" data-field="lot_number" />
            <dx-column caption="출고담당자" data-field="release.release_manager" />
            <dx-column caption="출고구분" data-field="release.release_type" />
            <dx-column caption="품목코드" data-field="item_code" />
            <dx-column caption="품명" data-field="item.item_name" />
            <dx-column caption="규격" data-field="item.item_standard" />
            <dx-column caption="출고창고" data-field="warehouse.wh_name" />
            <dx-column caption="단가" data-field="unit_price" :format="{ type: 'fixedPoint', precision: 2 }" />
            <dx-column caption="단위" data-field="item.unit" />
            <dx-column caption="공급가" data-field="supply_price" :format="{ type: 'fixedPoint', precision: 2 }" :calculate-cell-value="methods.calcSupplyPrice" />
            <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
            <dx-column caption="미계산서" data-field="non_invoice" data-type="number" format="fixedPoint" />
            <dx-column caption="수주번호" data-field="order_number" />
            <dx-column caption="고객사품번" data-field="client_item_number" />
            <dx-column caption="참고사항" data-field="note" />
            <dx-column caption="프로젝트번호" data-field="project_management.project_number" />
            <dx-column caption="종결" data-field="closing_yn" />

              <dx-sorting mode="single" />
              <dx-export :enabled="true" />
              <dx-paging :page-size="20" />
              <dx-column-chooser mode="select" :enabled="true" />
            </dx-data-grid>
          </DxTabPanelItem>
        </DxTabPanel>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment';

import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';

import DxButton from 'devextreme-vue/button';
import DxTextBox from 'devextreme-vue/text-box';
import DxCheckBox from 'devextreme-vue/check-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem } from 'devextreme-vue/form';
import { DxTabPanel, DxItem as DxTabPanelItem } from 'devextreme-vue/tab-panel'
import { DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxColumnChooser, } from 'devextreme-vue/data-grid';
import ArrayStore from 'devextreme/data/array_store';

import stateStore from '@/utils/state-store';
import { purchaseReceivingItem } from '@/data-source/purchase';
import { getProcessMaterialConsumption, getPerformanceItem1, processPerformanceRegistration } from '@/data-source/produce';
import { getShipmentReleaseItem } from '@/data-source/shipment';
import ApiService from '@/utils/api-service';
import { notifyError } from '@/utils/notify';
import { uniq, orderBy } from 'lodash'

export default {
  components: {
    DxButton,
    DxTextBox,
    DxCheckBox,
    DxDateBox,
    DxToolbar, DxItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem,
    DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxColumnChooser,
    DxTabPanel, DxTabPanelItem
  },
  setup() {
    const router = useRouter();
    const vars = {};
    vars.grid = {};
    vars.formData = reactive({
      lot_number: '',
      lot: ''
    });

    vars.tab = ref('구매입고')

    const processMaterialConsumption = getProcessMaterialConsumption()
    const releaseItemByLot = new ApiService('/api/mes/v1/shipment/release-item-by-lot')
    const releaseItemByLotStore = new ArrayStore({ key: 'id', data: [] })
    const processItemStore = new ArrayStore({ key: 'number', data: [] })
    const shipmentReleaseItem = getShipmentReleaseItem()
    const performanceItem1 = getPerformanceItem1()

    const methods = {
      initStatusGrid (component) {
        vars.grid.status = component
        stateStore.bind('status', component)
        methods.initSorting();
        component.filter(['lot_number', '=', ''])
      },
      initProduceGrid (component) {
        vars.grid.produce = component
        stateStore.bind('produce', component)
        // component.filter(['process_tag', '=', ''])
      },
      initReleaseGrid (component) {
        vars.grid.release = component
        stateStore.bind('release', component)
        component.filter(['lot_number', '=', '!!'])
      },
      initSorting() {
        const columns = vars.grid['status'].getVisibleColumns();
        const col = columns.filter(item => item.sortOrder);
        if (col.length == 0) {
          const defaultName = 'receiving.receiving_date';
          const defaultSort = columns.filter(item => item.name == defaultName);
          if (defaultSort.length > 0) {
            vars.grid['status'].columnOption(defaultSort[0].index, 'sortOrder', 'desc');
          }
        }
      },
      goReceivingDetail({ data }) {
        router.push({ path: `/purchase/receiving/${data.receiving.id}` });
      },
      async searchByProcessTag () {
        if (!vars.formData.lot) {
          return notifyError('생산주차를 입력해 주세요')
        }

        purchaseReceivingItem.defaultFilters = undefined
        vars.grid.status.clearFilter()

        processItemStore.clear()
        vars.grid.produce.clearFilter()
        const { data: res1 } = await processPerformanceRegistration.load({ filter: ['process_tag', '=', vars.formData.lot] })
        const { data: res2 } = await performanceItem1.load({ filter: ['lot', '=', vars.formData.lot] })

        let processNumber;

        res2.forEach(v => {
          const matched = res1.filter(m => (m.item_code === v.item_code && m.order_number === v.work_order_number))
          if (!matched.length) return
          const ordered = orderBy(matched, ['fk_process_id'], ['desc'])
          processItemStore.insert(ordered[0])
          processNumber = ordered[0].number;
        })

        if (processNumber) { 
          const consStore = getProcessMaterialConsumption()
          const { data: resp } = await consStore.load({ filter: ['process_number', '=', processNumber] })

          const lots = uniq(resp.filter(v => v).map(v => v.lot_number))
          if (lots.length) {
            purchaseReceivingItem.defaultFilters = [{ name: 'lot_number', op: 'in', val: lots }]
            vars.grid.status.refresh()
          } else {
            vars.grid.status.filter(['lot_number', '=', ''])
          }
        } else {
            vars.grid.status.filter(['lot_number', '=', ''])
        }
        // vars.grid.produce.filter(['process_performance_registration.process_tag', '=', vars.formData.lot])
        // vars.grid.produce.filter(['process_tag', '=', vars.formData.lot])

        vars.grid.produce.refresh()

        vars.grid.release.filter(['lot_number', 'contain', vars.formData.lot])
      },
      async searchByLotNumber() {
        purchaseReceivingItem.defaultFilters = undefined
        vars.grid.status.clearFilter()

        vars.grid.status.filter(['lot_number', '=', vars.formData.lot_number])
        vars.grid.produce.filter(['lot_number', '=', vars.formData.lot_number])

        const {data} = await releaseItemByLot.get(vars.formData.lot_number)
        releaseItemByLotStore.clear()
        if (data) data.forEach((v) => {
          releaseItemByLotStore.insert(v)
        })
        
        vars.grid.release.refresh()
      },
      onExporting (evt) {
        purchaseReceivingItem.exportData(evt.component, '입고현황', `입고현황_${Date.now()}.xlsx`)
        evt.cancel = true
      },
      tabChange ({addedItems}) {
        vars.tab.value = addedItems[0].title
      },
      calcSupplyPrice (rowData){
        let supply_price = 0;
        if(rowData.unit_price && rowData.release_quantity){
          supply_price = rowData.unit_price * rowData.release_quantity
        }
        rowData.supply_price = supply_price;
        return supply_price
      }
    };

    return {
      vars, methods, 
      purchaseReceivingItem, 
      processMaterialConsumption,
      shipmentReleaseItem,
      releaseItemByLotStore,
      processItemStore,
      performanceItem1,
      processPerformanceRegistration,
    };
  },
};
</script>

<style lang="scss" scoped>
.table-margin {
  padding: 10px;
}
</style>