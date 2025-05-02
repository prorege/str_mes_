<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">

        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">발주·입고 현황</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div>
          <div class="search-status">
            <span class="search-title">발주일자</span>
            <dx-date-box v-model:value="vars.formData.startDate" />
            
            <span class="search-bar">~</span>
            <dx-date-box v-model:value="vars.formData.endDate" />
            
            <span class="search-tab"></span>
            <SearchButtonGroup @change="({startDate, endDate}) => { vars.formData.startDate = startDate; vars.formData.endDate = endDate; }" />
            
            <span class="search-tab"></span>
            <dx-check-box text="미입고유무" v-model:value="vars.formData.notShipped" />
            
            <span class="search-tab"></span>
            <dx-button text="검색" icon="search" @click="methods.searchDateRange()" />
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
          :on-initialized="evt => methods.onGridInitialized(evt, 'status')"
          @exporting="methods.onExporting"
          @row-dbl-click="methods.goOrderDetail"
        >
          <dx-column caption="발주번호" data-field="order.order_number" :filter-operations="['contains', '=']" />
          <dx-column caption="발주일자" data-field="order.order_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
          <dx-column caption="공급업체약칭" data-field="order.client_alias" />
          <dx-column caption="공급업체" data-field="order.client_company" />
          <dx-column caption="발주담당자" data-field="order.order_manager" />
          <dx-column caption="발주구분" data-field="order.order_type" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="발주수량" data-field="order_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="입고수량"  data-field="receiving_quantity" data-type="number" format="fixedPoint" :allow-sorting="false"/>
          <dx-column caption="미입고수량" data-field="order_item.not_shipped" data-type="number" format="fixedPoint" :allow-sorting="false" />
          <dx-column caption="단가" data-field="unit_price" data-type="number" format="₩,##0" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="공급가" data-field="supply_price" data-type="number" format="₩,##0" :calculate-cell-value="methods.calcSupplyPrice" />
          <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="발주계획번호" data-field="order_plan_number" />
          <dx-column caption="공급사품번" data-field="client_item_number" />
          <dx-column caption="품목설명" data-field="item.item_detail" />
          <dx-column caption="프로젝트번호" data-field="project_management.project_number" />
          <dx-column caption="참고사항" data-field="note" />
          <dx-column caption="ID" data-field="id" :visible="false" :allow-editing="false" :show-in-column-chooser="false"/>

          <dx-sorting mode="single" />
          <dx-export :enabled="true" />
          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-column-chooser mode="select" :enabled="true" />

          <dx-master-detail :enabled="true" template="masterDetailTemplate" />
          <template #masterDetailTemplate="{ data: data }">
            <order-receiving-detail :template-data="data" />
          </template>
        </dx-data-grid>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment';

import { reactive } from 'vue';
import { useRouter } from 'vue-router';

import { alert } from 'devextreme/ui/dialog';
import DxButton from 'devextreme-vue/button';
import DxCheckBox from 'devextreme-vue/check-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxMasterDetail, DxColumnChooser } from 'devextreme-vue/data-grid';

import OrderReceivingDetail from './order-receiving-detail.vue';
import SearchButtonGroup from '../../components/search-button-group.vue';
import ArrayStore from 'devextreme/data/array_store';
import stateStore from '@/utils/state-store';
import { purchaseOrderReceivingStatus, purchaseReceivingItem } from '../../data-source/purchase';

export default {
  components: {
    DxButton,
    DxCheckBox,
    DxDateBox,
    DxToolbar, DxItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem,
    DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxMasterDetail, DxColumnChooser,
    OrderReceivingDetail,
    SearchButtonGroup,
  },
  setup() {
    const router = useRouter();
    const vars = {};
    vars.grid = {};
    vars.formData = reactive({
      startDate: new Date(),
      endDate: new Date(),
      notShipped: false,
    });
    const dataSource = new ArrayStore({ key: 'grid_id', data: [] })
    // vars.formData.startDate.setDate(vars.formData.startDate.getDate() - 7);

    const methods = {
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`purchase-order-receiving-${key}`, evt.component);

        // methods.initSorting();
        // methods.searchDateRange();
      },
      initSorting() {
        const columns = vars.grid['status'].getVisibleColumns();
        const col = columns.filter(item => item.sortOrder);
        if (col.length == 0) {
          const defaultName = 'order.order_date';
          const defaultSort = columns.filter(item => item.name == defaultName);
          if (defaultSort.length > 0) {
            vars.grid['status'].columnOption(defaultSort[0].index, 'sortOrder', 'desc');
          }
        }
      },
      goOrderDetail(e) {
        if (e.columnIndex != 0) {
          router.push({ path: `/purchase/order/${e.data.order.id}` });
        }
      },
      calculateNotReceivingQuantity(rowData) {
        const receivingQuantity = rowData.receiving_quantity ? rowData.receiving_quantity : 0;
        const orderQuantity = rowData.order_quantity ? rowData.order_quantity : 0;

        return orderQuantity - receivingQuantity;
      },
      calcSupplyPrice(rowData) {
        let supply_price = 0;
        if (rowData.order_quantity && rowData.unit_price) {
          supply_price = rowData.order_quantity * rowData.unit_price;
        }
        rowData.supply_price = supply_price;
        return supply_price;
      },
       getParams () {
        return { 
          filter: [
            [
              'order.order_date', '>=',
              moment(vars.formData.startDate)
                .startOf('day')
                .format('YYYY-MM-DD 00:00:00'),
            ],
            'and',
            [
              'order.order_date', '<=',
              moment(vars.formData.endDate)
                .endOf('day')
                .format('YYYY-MM-DD 23:59:59'),
            ],
          ],
          sort: [
            {selector : 'order.order_date', desc: true}
          ],
          skip: 0,
          take: 10000
        }
      },
      async searchDateRange() {
        if (vars.formData.startDate > vars.formData.endDate) {
          await alert('조회 일자가 잘못 되었습니다', '조회');
          return;
        }
        try{
          dataSource.clear()
          vars.grid['status'].beginCustomLoading('데이터를 집계중입니다')
          const params = methods.getParams(); 
          if (vars.formData.notShipped) {
            params.filter.push('and');
            params.filter.push(['not_shipped', '>', 0]);
          }
          const { data } = await purchaseOrderReceivingStatus.load(params);

          let i = 1;
          data.forEach((v) => {
            v.grid_id = i++
            dataSource.insert(v);
          });
        }catch(ex){
          console.error(ex)
        }finally{
          vars.grid['status'].endCustomLoading()
        }
        vars.grid['status'].refresh() 
      },
      onExporting (evt) {
        purchaseOrderReceivingStatus.exportData(evt.component, '발주입고현황', `발주입고현황_${Date.now()}.xlsx`)
        evt.cancel = true
      }
    };

    return { vars, methods, purchaseOrderReceivingStatus, dataSource };
  },
};
</script>
