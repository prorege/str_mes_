<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">재고이동요청현황</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div>
          <div class="search-status">
            <span class="search-title">요청일자</span>
            <dx-date-box v-model:value="vars.formData.startDate" />
            <span class="search-bar">~</span>
            <dx-date-box v-model:value="vars.formData.endDate" />
            <span class="search-tab"></span>
            <SearchButtonGroup @change="({startDate, endDate}) => { vars.formData.startDate = startDate; vars.formData.endDate = endDate; }" />
              <span class="search-tab"></span>
            <dx-check-box text="미출고" v-model:value="vars.formData.notShipped" />
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
          :filter-sync-enabled="true"
          :data-source="dataSource"
          :on-initialized="evt => methods.onGridInitialized(evt, 'status')"
          @row-dbl-click="methods.goDetail"
          @exporting="methods.onExporting"
        >
          <dx-column caption="요청번호" data-field="stock_move_request.number" :filter-operations="['contains', '=']" />
          <dx-column caption="요청일자" data-field="stock_move_request.target_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
          <dx-column caption="담당부서" data-field="stock_move_request.department" />
          <dx-column caption="담당자" data-field="stock_move_request.manager" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="수량" data-field="quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="미출고수량" data-field="not_shipped" data-type="number" format="fixedPoint" />
          <dx-column caption="출고창고" data-field="warehouse_release.wh_name" />
          <dx-column caption="입고창고" data-field="warehouse_receive.wh_name" />
          <dx-column caption="단가" data-field="unit_price" data-type="number" format="₩,##0" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="금액" data-field="supply_price" data-type="number" format="₩,##0" :calculate-cell-value="methods.calcSupplyPrice" />
          <dx-column caption="주공급업체약칭" data-field="client_alias" />
          <dx-column caption="주공급업체" data-field="client_company" />
          <dx-column caption="작업지시번호" data-field="work_order.number" />
          <dx-column caption="프로젝트번호" data-field="project_management.project_number" />

          <dx-export :enabled="true" />
          <dx-paging :page-size="20" />
          <dx-sorting mode="multiple" />
          <dx-filter-row :visible="true" />
          <dx-column-chooser mode="select" :enabled="true" />
        </dx-data-grid>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment';

import { useRouter } from 'vue-router';
import { reactive } from 'vue';

import { alert } from 'devextreme/ui/dialog';
import DxButton from 'devextreme-vue/button';
import DxCheckBox from 'devextreme-vue/check-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxExport, DxPaging, DxSorting, DxFilterRow, DxColumnChooser } from 'devextreme-vue/data-grid';
import ArrayStore from 'devextreme/data/array_store';
import stateStore from '@/utils/state-store';
import { stockMoveRequestItem } from '../../data-source/stock';
import SearchButtonGroup from '../../components/search-button-group.vue';

export default {
  components: {
    DxButton,
    DxCheckBox,
    DxDateBox,
    DxToolbar, DxItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem,
    DxDataGrid, DxColumn, DxExport, DxPaging, DxSorting, DxFilterRow, DxColumnChooser,
    SearchButtonGroup
  },
  setup() {
    const router = useRouter();
    const vars = {};
    vars.grid = {};
    vars.formData = reactive({
      notShipped: false,
      startDate: new Date(),
      endDate: new Date(),
    });
    const dataSource = new ArrayStore({ key: 'grid_id', data: [] })
    // vars.formData.startDate.setDate(vars.formData.startDate.getDate() - 7);

    const methods = {
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`stock-move-request-${key}`, evt.component);

        // methods.initSorting();
        // methods.searchDateRange();
      },
      initSorting() {
        const columns = vars.grid['status'].getVisibleColumns();
        const col = columns.filter(item => item.sortOrder);
        if (col.length == 0) {
          const defaultName = 'stock_move_request.target_date';
          const defaultSort = columns.filter(item => item.name == defaultName);
          if (defaultSort.length > 0) {
            vars.grid['status'].columnOption(defaultSort[0].index, 'sortOrder', 'desc');
          }
        }
      },
      goDetail({ data }) {
        router.push({ path: `/stock/move-request/${data.stock_move_request.id}` });
      },
      calcSupplyPrice(rowData) {
        let supply_price = 0;
        if (rowData.quantity && rowData.unit_price) {
          supply_price = rowData.quantity * rowData.unit_price;
        }
        rowData.supply_price = supply_price;
        return supply_price;
      },
      getParams () {
        return { 
          filter: [
            [
              'stock_move_request.target_date', '>=',
              moment(vars.formData.startDate)
                .startOf('day')
                .format('YYYY-MM-DD 00:00:00'),
            ],
            'and',
            [
              'stock_move_request.target_date', '<=',
              moment(vars.formData.endDate)
                .endOf('day')
                .format('YYYY-MM-DD 23:59:59'),
            ],
          ],
          sort: [
            {selector : 'stock_move_request.target_date', desc: true}
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
        // const dateFilter = filter.find(v => typeof v === 'object' && v[0] === 'stock_move_request.target_date')
        // if (dateFilter) dateFilter[2] = filterValue
        // else filter.push(['stock_move_request.target_date', 'between', filterValue])

        // if (vars.formData.notShipped) {
        //   filter.push('and');
        //   filter.push(['not_shipped', '>', 0]);
        // }
        // else {
        //   const index = filter.findIndex(v => typeof v === 'object' && v[0] === 'not_shipped')
        //   if (index >= 0) console.info(`remove filter: ${filter.splice(index - 1, 2)}`)
        // }
        
        // vars.grid['status'].option('filterValue', filter)
        try{
          dataSource.clear()
          vars.grid['status'].beginCustomLoading('데이터를 집계중입니다')
          const params = methods.getParams(); 
          if (vars.formData.notShipped) {
            params.filter.push('and');
            params.filter.push(['not_shipped', '>', 0]);
          }
          const { data } = await stockMoveRequestItem.load(params);

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
      async onExporting(evt) {
        stockMoveRequestItem.exportData(evt.component, '재고이동요청현황', `재고이동요청현황_${Date.now()}.xlsx`);
        evt.cancel = true;
      },
    };

    return { vars, methods, stockMoveRequestItem, dataSource };
  },
};
</script>
