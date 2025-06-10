<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">가입고·입고 현황</div>
            </dx-item>
          </dx-toolbar>
        </div>
        
        <div>
          <div class="search-status">
            <span class="search-title">가입고일자</span>
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
          :on-initialized="evt => methods.onGridInitialized(evt, 'status')"
          @row-dbl-click="methods.goItem"
          @exporting="methods.onExporting"
        >          
          <dx-column caption="가입고번호" data-field="prereceiving.prereceiving_number" :filter-operations="['contains', '=']" />
          <dx-column caption="가입고일자" data-field="prereceiving.prereceiving_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
          <dx-column caption="고객업체약칭" data-field="prereceiving.client_alias" />
          <dx-column caption="고객업체" data-field="prereceiving.client_company" />
          <dx-column caption="입고부서" data-field="prereceiving.receiving_department" />
          <dx-column caption="입고담당자" data-field="prereceiving.receiving_manager" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="발주수량" data-field="order_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="가입고수량" data-field="prereceiving_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="미입고수량" data-field="not_shipped" data-type="number" format="fixedPoint" />
          <dx-column caption="단가" data-field="unit_price" data-type="number" format="₩,##0.00" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="공급가" data-field="supply_price" data-type="number" format="₩,##0.00" :calculate-cell-value="methods.calcSupplyPrice" />
          <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="검수수량" data-field="check_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="불량수량" data-field="bad_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="양품수량" data-field="good_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="LOT번호" data-field="lot_number" />
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :calculate-display-value="methods.availableStock" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :calculate-display-value="methods.currentStock" />
          <dx-column caption="입고창고" data-field="warehouse.wh_name" />
          <dx-column caption="고객사품번" data-field="client_item_number" />
          <dx-column caption="품목설명" data-field="item.item_detail" />
          <dx-column caption="프로젝트번호" data-field="project_management.project_number" />
          <dx-column caption="검수완료" data-field="check_yn" data-type="boolean" />
          <dx-column caption="종결" data-field="closing_yn" data-type="boolean" />

          <dx-sorting mode="single" />
          <dx-export :enabled="true" />
          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-column-chooser mode="select" :enabled="true" />

          <dx-master-detail :enabled="true" template="masterDetailTemplate" />
          <template #masterDetailTemplate="{ data: prereceiving }">
            <prereceiving-to-receiving-detail :template-data="prereceiving" />
          </template>
        </dx-data-grid>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment';
import ArrayStore from 'devextreme/data/array_store';
import { reactive } from 'vue';
import { useRouter } from 'vue-router';

import { alert } from 'devextreme/ui/dialog';
import DxButton from 'devextreme-vue/button';
import DxCheckBox from 'devextreme-vue/check-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxMasterDetail, DxColumnChooser } from 'devextreme-vue/data-grid';

import stateStore from '@/utils/state-store';
import { purchasePreReceivingItem } from '../../data-source/purchase';
import PrereceivingToReceivingDetail from './prereceiving-to-receiving-detail.vue';
import SearchButtonGroup from '../../components/search-button-group.vue';

export default {
  components: {
    DxButton,
    DxCheckBox,
    DxDateBox,
    DxToolbar, DxItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem,
    DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting,  DxFilterRow, DxMasterDetail, DxColumnChooser,
    PrereceivingToReceivingDetail,
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
        stateStore.bind(`purchase-prereceiving-receiving-${key}`, evt.component);

        // methods.initSorting();
        // methods.searchDateRange();
      },
      initSorting() {
        const columns = vars.grid['status'].getVisibleColumns();
        const col = columns.filter(item => item.sortOrder);
        if (col.length == 0) {
          const defaultName = 'prereceiving.prereceiving_date';
          const defaultSort = columns.filter(item => item.name == defaultName);
          if (defaultSort.length > 0) {
            vars.grid['status'].columnOption(defaultSort[0].index, 'sortOrder', 'desc');
          }
        }
      },
      goItem(e) {
        router.push({ path: `/purchase/pre-receiving/${e.data.prereceiving.id}` });
      },
      calcSupplyPrice(rowData) {
        let supply_price = 0;
        if (rowData.prereceiving_quantity && rowData.unit_price) {
          supply_price = rowData.prereceiving_quantity * rowData.unit_price;
        }
        rowData.supply_price = supply_price;
        return supply_price;
      },
      availableStock(rowData) {
        if (!rowData.basic_stock) return '0';
        return rowData.basic_stock.available_stock;
      },
      currentStock(rowData) {
        if (!rowData.basic_stock) return '0';
        return rowData.basic_stock.current_stock;
      },
       getParams () {
        return { 
          filter: [
            [
              'prereceiving.prereceiving_date', '>=',
              moment(vars.formData.startDate)
                .startOf('day')
                .format('YYYY-MM-DD 00:00:00'),
            ],
            'and',
            [
              'prereceiving.prereceiving_date', '<=',
              moment(vars.formData.endDate)
                .endOf('day')
                .format('YYYY-MM-DD 23:59:59'),
            ],
          ],
          sort: [
            {selector : 'prereceiving.prereceiving_date', desc: true}
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
        // const dateFilter = filter.find(v => typeof v === 'object' && v[0] === 'prereceiving.prereceiving_date')
        // if (dateFilter) dateFilter[2] = filterValue
        // else filter.push(['prereceiving.prereceiving_date', 'between', filterValue])

        // if (vars.formData.notShipped) {
        //   filter.push('and')
        //   filter.push(['not_shipped', '>', 0])
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
          const { data } = await purchasePreReceivingItem.load(params);

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
      async onExporting (evt) {
        purchasePreReceivingItem.exportData(evt.component, '가입고입고현황', `가입고입고현황_${Date.now()}.xlsx`)
        evt.cancel = true
      }
    };

    return { vars, methods, purchasePreReceivingItem, dataSource };
  },
};
</script>
