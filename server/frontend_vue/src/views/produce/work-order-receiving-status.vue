<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before"
              ><div class="content-title">작지입고현황</div></dx-item
            >
          </dx-toolbar>
        </div>

        <div>
          <div class="search-status">
            <span class="search-title">작업지시일자</span>
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
          :filter-sync-enabled="true"
          :on-initialized="evt => methods.onInitialized(evt, 'status')"
          @row-dbl-click="methods.goDetail"
          @exporting="methods.onExporting"
        >
          
          <dx-column caption="작지번호" data-field="work_order.number" :filter-operations="['contains', '=']" />
          <dx-column caption="작지일자" data-field="work_order.target_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
          <dx-column caption="작지담당자" data-field="work_order.manager" />
          <dx-column caption="참고사항" data-field="work_order.note" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="작지수량" data-field="required_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="입고수량" data-type="number" format="fixedPoint" :calculate-display-value="methods.calculateReceivingQuantity" />
          <dx-column caption="미입고수량" data-field="unproduced_quantity" data-type="number" format="fixedPoint" :calculate-display-value="methods.calcUnproducedQuantity" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="대분류" data-field="item.main_category" />
          <dx-column caption="중분류" data-field="item.middle_category" />
          <dx-column caption="소분류" data-field="item.sub_category" />
          <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :calculate-display-value="methods.availableStock" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :calculate-display-value="methods.currentStock" />
          <dx-column caption="고객업체약칭" data-field="client_alias" />
          <dx-column caption="고객업체" data-field="client_company" />
          <dx-column caption="고객사품번" data-field="client_item_number" />
          <dx-column caption="품목설명" data-field="item.item_detail" />
          <dx-column caption="프로젝트번호" data-field="project_management.project_number" />
          <dx-column caption="종료" data-field="end_yn" data-type="boolean" />

          <dx-export :enabled="true" />
          <dx-paging :page-size="20" />
          <dx-sorting mode="single" />
          <dx-filter-row :visible="true" />
          <dx-column-chooser mode="select" :enabled="true" />

          <dx-master-detail :enabled="true" template="masterDetailTemplate" />
          <template #masterDetailTemplate="{ data: data }">
            <work-order-receiving-detail :template-data="data" />
          </template>
        </dx-data-grid>
      </div>
    </div>
  </div>
</template>

<script>
import {
  DxDataGrid,
  DxColumn,
  DxPaging,
  DxSorting,
  DxFilterRow,
  DxColumnChooser,
  DxMasterDetail,
  DxExport
} from 'devextreme-vue/data-grid';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxCheckBox from 'devextreme-vue/check-box';
import DxButton from 'devextreme-vue/button';
import { useRouter } from 'vue-router';
import { produceWorkOrderItem1 } from '../../data-source/produce';
import { reactive } from 'vue';
import ArrayStore from 'devextreme/data/array_store';
import stateStore from '@/utils/state-store';
import moment from 'moment';
import { alert } from 'devextreme/ui/dialog';
import WorkOrderReceivingDetail from './work-order-receiving-detail.vue';
import SearchButtonGroup from '../../components/search-button-group.vue';

export default {
  components: {
    DxDataGrid,
    DxColumn,
    DxPaging,
    DxSorting,
    DxColumnChooser,
    DxMasterDetail,
    DxFilterRow,
    DxToolbar,
    DxItem,
    DxDateBox,
    DxCheckBox,
    DxButton,
    DxExport,
    WorkOrderReceivingDetail,
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
      onInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`produce-work-order-receiving-${key}`, evt.component);

        // methods.initSorting();
        // methods.searchDateRange();
      },
      initSorting() {
        const columns = vars.grid['status'].getVisibleColumns();
        const col = columns.filter(item => item.sortOrder);
        if (col.length == 0) {
          const defaultName = 'work_order.target_date';
          const defaultSort = columns.filter(item => item.name == defaultName);
          if (defaultSort.length > 0) {
            vars.grid['status'].columnOption(
              defaultSort[0].index,
              'sortOrder',
              'desc'
            );
          }
        }
      },
      goDetail(e) {
        router.push({ path: `/produce/work-order/${e.data.work_order.id}` });
      },
        getParams () {
        return { 
          filter: [
            [
              'work_order.target_date', '>=',
              moment(vars.formData.startDate)
                .startOf('day')
                .format('YYYY-MM-DD 00:00:00'),
            ],
            'and',
            [
              'work_order.target_date', '<=',
              moment(vars.formData.endDate)
                .endOf('day')
                .format('YYYY-MM-DD 23:59:59'),
            ],
            'and',
            ['end_yn', '=', false]
          ],
          sort: [
            {selector : 'work_order.target_date', desc: true}
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

        // if (!vars.grid['status']) return
        // const filterValue = [
        //   moment(vars.formData.startDate).startOf('day').toDate(),
        //   moment(vars.formData.endDate).endOf('day').toDate()
        // ]
        // const filter = vars.grid['status'].option('filterValue') || []
        // const dateFilter = filter.find(v => typeof v === 'object' && v[0] === 'work_order.target_date')
        // if (dateFilter) dateFilter[2] = filterValue
        // else filter.push(['work_order.target_date', 'between', filterValue])

        // filter.push('and')
        // filter.push(['end_yn', '=', false])

        // if (vars.formData.notShipped) {
        //   filter.push('and');
        //   filter.push(['unproduced_quantity', '>', 0]);
        // }
        // else {
        //   const index = filter.findIndex(v => typeof v === 'object' && v[0] === 'unproduced_quantity')
        //   if (index >= 0) console.info(`remove filter: ${filter.splice(index - 1, 2)}`)
        // }
        
        // vars.grid['status'].option('filterValue', filter)
      try{
          dataSource.clear()
          vars.grid['status'].beginCustomLoading('데이터를 집계중입니다')
          const params = methods.getParams(); 
          if (vars.formData.notShipped) {
            params.filter.push('and');
            params.filter.push(['unproduced_quantity', '>', 0]);
          }

          const { data } = await produceWorkOrderItem1.load(params);

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
      calculateReceivingQuantity(rowData) {
        const requiredQuantity = rowData.required_quantity ? rowData.required_quantity : 0;
        const unproducedQuantity = rowData.unproduced_quantity ? rowData.unproduced_quantity : 0;
        return requiredQuantity - unproducedQuantity;
      },
      calcUnproducedQuantity(rowData) {
        if (rowData.end_yn) {
          return '0';
        }
        return rowData.unproduced_quantity;
      },
      availableStock(rowData) {
        if (!rowData.basic_stock) return '0';
        return rowData.basic_stock.available_stock;
      },
      currentStock(rowData) {
        if (!rowData.basic_stock) return '0';
        return rowData.basic_stock.current_stock;
      },
      onExporting (evt) {
        produceWorkOrderItem1.exportData(evt.component, '작지입고현황', `작지입고현황_${Date.now()}.xlsx`)
        evt.cancel = true
      }
    };

    return { vars, methods, produceWorkOrderItem1, dataSource };
  },
};
</script>
