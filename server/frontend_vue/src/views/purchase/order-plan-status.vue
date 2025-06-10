<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">발주계획현황</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div>
          <div class="search-status">
            <span class="search-title">발주계획일자</span>
            <dx-date-box v-model:value="vars.formData.startDate" />
            
            <span class="search-bar">~</span>
            <dx-date-box v-model:value="vars.formData.endDate" />
            
            <span class="search-tab"></span>
            <SearchButtonGroup @change="({startDate, endDate}) => { vars.formData.startDate = startDate; vars.formData.endDate = endDate; }" />
            
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
          :on-initialized="evt => methods.onGridInitialized(evt, 'status')"
          @exporting="methods.onExporting"
          @row-dbl-click="methods.goDetail"
        >
          <dx-column caption="발주계획번호" data-field="order_plan.order_plan_number" :filter-operations="['contains', '=']" />
          <dx-column caption="발주계획일자" data-field="order_plan.order_plan_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
          <dx-column caption="발주구분" data-field="order_plan.order_type" />
          <dx-column caption="주공급업체약칭" data-field="main_supplier_alias" />
          <dx-column caption="주공급업체" data-field="main_supplier" />
          <dx-column caption="실수요자" data-field="end_user" />
          <dx-column caption="발주계획부서" data-field="order_plan.order_plan_department" />
          <dx-column caption="발주계획담당자" data-field="order_plan.order_plan_manager" />
          <dx-column caption="입고창고" data-field="warehouse.wh_name" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="발주계획수량" data-field="order_plan_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="미발주수량" data-field="unordered_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="단가" data-field="unit_price" data-type="number" format="₩,##0" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="공급가" data-field="supply_price" format="₩,##0" :calculate-cell-value="methods.calcSupplyPrice" />
          <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="수주번호" data-field="order_number" />
          <dx-column caption="수주일자" data-field="order_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="품목대분류" data-field="item.main_category" />
          <dx-column caption="품목중분류" data-field="item.middle_category" />
          <dx-column caption="품목소분류" data-field="item.sub_category" />
          <dx-column caption="자산구분" data-field="item.asset_type" />
          <dx-column caption="안전재고" data-field="item.safety_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="프로젝트번호" data-field="project_management.project_number" />

          <dx-sorting mode="single" />
          <dx-export :enabled="true" />
          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-column-chooser mode="select" :enabled="true" />
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
import { DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxColumnChooser } from 'devextreme-vue/data-grid';
import ArrayStore from 'devextreme/data/array_store';
import stateStore from '@/utils/state-store';
import { purchaseOrderPlanItem } from '../../data-source/purchase';
import SearchButtonGroup from '../../components/search-button-group.vue';

export default {
  components: {
    DxButton,
    DxCheckBox,
    DxDateBox,
    DxToolbar, DxItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem,
    DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxColumnChooser,
    SearchButtonGroup,
  },
  setup() {
    const router = useRouter();
    const vars = {};
    vars.grid = {};
    vars.formData = reactive({
      startDate: new Date(),
      endDate: new Date(),
    });
    const dataSource = new ArrayStore({ key: 'grid_id', data: [] })
    // vars.formData.startDate.setDate(vars.formData.startDate.getDate() - 7);

    const methods = {
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`purchase-order-plan-${key}`, evt.component);

        // methods.initSorting();
        // methods.searchDateRange();
      },
      initSorting() {
        const columns = vars.grid['status'].getVisibleColumns();
        const col = columns.filter(item => item.sortOrder);
        if (col.length == 0) {
          const defaultName = 'order_plan.order_plan_date';
          const defaultSort = columns.filter(item => item.name == defaultName);
          if (defaultSort.length > 0) {
            vars.grid['status'].columnOption(defaultSort[0].index, 'sortOrder', 'desc');
          }
        }
      },
      goDetail({ data }) {
        router.push({ path: `/purchase/order-plan/${data.order_plan.id}` });
      },
      calcSupplyPrice(rowData) {
        let supply_price = 0;
        if (rowData.order_plan_quantity && rowData.unit_price) {
          supply_price = rowData.order_plan_quantity * rowData.unit_price;
        }
        rowData.supply_price = supply_price;
        return supply_price;
      },
       getParams () {
        return { 
          filter: [
            [
              'order_plan.order_plan_date', '>=',
              moment(vars.formData.startDate)
                .startOf('day')
                .format('YYYY-MM-DD 00:00:00'),
            ],
            'and',
            [
              'order_plan.order_plan_date', '<=',
              moment(vars.formData.endDate)
                .endOf('day')
                .format('YYYY-MM-DD 23:59:59'),
            ],
          ],
          sort: [
            {selector : 'order_plan.order_plan_date', desc: true}
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
        // const dateFilter = filter.find(v => typeof v === 'object' && v[0] === 'order_plan.order_plan_date')
        // if (dateFilter) dateFilter[2] = filterValue
        // else filter.push(['order_plan.order_plan_date', 'between', filterValue])

        // vars.grid['status'].option('filterValue', filter)
         try{
          dataSource.clear()
          vars.grid['status'].beginCustomLoading('데이터를 집계중입니다')
          const params = methods.getParams(); 
      
          const { data } = await purchaseOrderPlanItem.load(params);

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
        purchaseOrderPlanItem.exportData(evt.component, '발주계획현황', `발주계획현황_${Date.now()}.xlsx`)
        evt.cancel = true
      }
    };

    return { vars, methods, purchaseOrderPlanItem, dataSource };
  },
};
</script>
