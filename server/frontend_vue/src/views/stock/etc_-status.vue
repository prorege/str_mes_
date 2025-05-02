<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">재고보정현황</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div>
          <div class="search-status">
            <span class="search-title">기타입출고일자</span>
            <dx-date-box v-model:value="vars.formdata.startDate" />

            <span class="search-bar">~</span>
            <dx-date-box v-model:value="vars.formdata.endDate" />

            <span class="search-tab"></span>
            <SearchButtonGroup @change="({startDate, endDate}) => { vars.formdata.startDate = startDate; vars.formdata.endDate = endDate; }" />

            <span class="search-tab"></span>
            <dx-button text="검색" icon="search" @click="methods.searchDateRange()" />
          </div>
        </div>

      </div>

      <div class="dx-card responsive-paddings mt-1">
        <dx-data-grid
          height="calc(100vh - 240px)"
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
          :on-initialized="evt => methods.onGridInitialized(evt, 'status-list')"
          @exporting="methods.onExporting"
          @row-dbl-click="methods.goStockEtcDetail"
        >
          <dx-column caption="입출고번호" data-field="stock_etc.number" :filter-operations="['contains', '=']" />
          <dx-column caption="일자" data-field="stock_etc.target_date" data-type="date" format="yyyy-MM-dd" sort-order="desc" />
          <dx-column caption="담당자" data-field="stock_etc.manager" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="수량" data-field="quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="단가" data-field="unit_price" data-type="number" format="₩,##0" />
          <dx-column caption="금액" data-field="supply_price" data-type="number" format="₩,##0" />
          <dx-column caption="입출고유형" data-field="inout_type" />
          <dx-column caption="입출고창고" data-field="warehouse.wh_name" />
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="품목대분류" data-field="item.main_category" />
          <dx-column caption="품목중분류" data-field="item.middle_category" />
          <dx-column caption="품목소분류" data-field="item.sub_category" />
          <dx-column caption="자산구분" data-field="item.asset_type" />
          <dx-column caption="안전재고" data-field="item.safety_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="참고" data-field="note" />

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
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem, } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxExport, DxFilterRow, DxColumnChooser, } from 'devextreme-vue/data-grid';
import ArrayStore from 'devextreme/data/array_store';
import stateStore from '@/utils/state-store';
import { stockEtcItem } from '../../data-source/stock';
import SearchButtonGroup from '../../components/search-button-group.vue';

export default {
  components: {
    DxButton,
    DxDateBox,
    DxToolbar, DxItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem,
    DxDataGrid, DxColumn, DxPaging, DxExport, DxFilterRow, DxColumnChooser,
    SearchButtonGroup,
  },
  setup() {
    const router = useRouter();
    const vars = {};
    vars.formdata = reactive({
      startDate: new Date(),
      endDate: new Date(),
    });
    vars.dataGridInstance = {};
    const dataSource = new ArrayStore({ key: 'grid_id', data: [] })
    const methods = {
      onGridInitialized(evt, key) {
        vars.dataGridInstance[key] = evt.component;
        stateStore.bind(key, evt.component);

        // methods.searchDateRange();
      },
      goStockEtcDetail({ data }) {
        router.push({ path: `/stock/etc/${data.fk_stock_etc_id}` });
      },
      getParams () {
        return { 
          filter: [
            [
              'stock_etc.target_date', '>=',
              moment(vars.formdata.startDate)
                .startOf('day')
                .format('YYYY-MM-DD 00:00:00'),
            ],
            'and',
            [
              'stock_etc.target_date', '<=',
              moment(vars.formdata.endDate)
                .endOf('day')
                .format('YYYY-MM-DD 23:59:59'),
            ],
          ],
          sort: [
            {selector : 'stock_etc.target_date', desc: true}
          ],
          skip: 0,
          take: 10000
        }
      },
      async searchDateRange() {
        if (vars.formdata.startDate > vars.formdata.endDate) {
          await alert('조회 일자가 잘못 되었습니다', '조회');
          return;
        }
        try{
          dataSource.clear()
          vars.dataGridInstance['status-list'].beginCustomLoading('데이터를 집계중입니다')
          const params = methods.getParams(); 
 
          const { data } = await stockEtcItem.load(params);

          let i = 1;
          data.forEach((v) => {
            v.grid_id = i++
            dataSource.insert(v);
          });
        }catch(ex){
          console.error(ex)
        }finally{
          vars.dataGridInstance['status-list'].endCustomLoading()
        }
        vars.dataGridInstance['status-list'].refresh() 

        // if (!vars.dataGridInstance['status-list']) return
        // const filterValue = [
        //   moment(vars.formdata.startDate).startOf('day').toDate(),
        //   moment(vars.formdata.endDate).endOf('day').toDate()
        // ]
        // const filter = vars.dataGridInstance['status-list'].option('filterValue') || []
        // const dateFilter = filter.find(v => typeof v === 'object' && v[0] === 'stock_etc.target_date')
        // if (dateFilter) dateFilter[2] = filterValue
        // else filter.push(['stock_etc.target_date', 'between', filterValue])
        
        // vars.dataGridInstance['status-list'].option('filterValue', filter)
      },
      onExporting (evt) {
        stockEtcItem.exportData(evt.component, '기타입출고현황', `기타입출고현황_${Date.now()}.xlsx`)
        evt.cancel = true
      }
    };

    return { vars, methods, stockEtcItem, dataSource };
  },
};
</script>
