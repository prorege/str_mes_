<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">입고반품현황</div>
            </dx-item>
          </dx-toolbar>
        </div>
        <div>
          <div class="search-status">
            <span class="search-title">입고반품일자</span>
            <dx-date-box v-model:value="vars.formData.startDate" />
            
            <span class="search-bar">~</span>
            <dx-date-box v-model:value="vars.formData.endDate" />
            
            <span class="search-tab"></span>
            <SearchButtonGroup
              @change="({ startDate, endDate }) => {
                vars.formData.startDate = startDate;
                vars.formData.endDate = endDate;
              }"
            />

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
          :filter-sync-enabled="true"
          :focused-row-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :data-source="dataSource"
          :on-initialized="(evt) => methods.onGridInitialized(evt, 'status')"
          @exporting="methods.onExporting"
          @row-dbl-click="methods.goDetail"
        >
          <dx-column caption="반품번호" data-field="receiving_return.return_number" data-type="string" :filter-operations="['contains', '=']" />
          <dx-column caption="반품일자" data-field="receiving_return.return_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
          <dx-column caption="고객업체약칭" data-field="receiving_return.client_alias" data-type="string" />
          <dx-column caption="고객업체" data-field="receiving_return.client_company" data-type="string" />
          <dx-column caption="반품부서" data-field="receiving_return.return_department" data-type="string" />
          <dx-column caption="반품담당자" data-field="receiving_return.return_manager" data-type="string" />
          <dx-column caption="반품구분" data-field="receiving_return.return_type" data-type="string" />
          <dx-column caption="품목코드" data-field="item_code" data-type="string" />
          <dx-column caption="품명" data-field="item.item_name" data-type="string" />
          <dx-column caption="규격" data-field="item.item_standard" data-type="string" />
          <dx-column caption="반품수량" data-field="return_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="입고수량" data-field="receiving_item.receiving_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="단가" data-field="receiving_item.unit_price" data-type="number" format="₩,##0" />
          <dx-column caption="단위" data-field="item.unit" data-type="string" />
          <dx-column caption="공급가" data-field="supply_price" data-type="number" format="₩,##0" />
          <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="출고창고" data-field="warehouse_code" data-type="string" />
          <dx-column caption="반품사유" data-field="return_reason" data-type="string" />
          <dx-column caption="가용재고" data-field="basic_stock.available_stock" data-type="number" format="fixedPoint" :calculate-display-value="methods.availableStock" />
          <dx-column caption="현재고" data-field="basic_stock.current_stock" data-type="number" format="fixedPoint" :calculate-display-value="methods.currentStock" />
          <dx-column caption="품목대분류" data-field="item.main_category" data-type="string" />
          <dx-column caption="품목중분류" data-field="item.middle_category" data-type="string" />
          <dx-column caption="품목소분류" data-field="item.sub_category" data-type="string" />
          <dx-column caption="자산구분" data-field="item.asset_type" data-type="string" />
          <dx-column caption="안전재고" data-field="item.safety_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="업체분류" data-field="client.client_type" data-type="string" :allow-sorting="false" />
          <dx-column caption="당사담담자" data-field="client.manager" data-type="string" :allow-sorting="false" />

          <dx-export :enabled="true" />
          <dx-paging :page-size="20" />
          <dx-sorting mode="single" />
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
import { DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxColumnChooser } from 'devextreme-vue/data-grid';
import ArrayStore from 'devextreme/data/array_store';
import stateStore from '@/utils/state-store';
import { purchaseReceivingReturnItem } from '../../data-source/purchase';
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
        stateStore.bind(`purchase-receiving-return-${key}`, evt.component);

        // methods.initSorting();
        // methods.searchDateRange();
      },
      initSorting() {
        const columns = vars.grid['status'].getVisibleColumns();
        const col = columns.filter((item) => item.sortOrder);
        if (col.length == 0) {
          const defaultName = 'receiving_return.return_date';
          const defaultSort = columns.filter(
            (item) => item.name == defaultName
          );
          if (defaultSort.length > 0) {
            vars.grid['status'].columnOption(defaultSort[0].index, 'sortOrder', 'desc');
          }
        }
      },
      goDetail({ data }) {
        router.push({ path: `/purchase/receiving-return/${data.receiving_return.id}` });
      },
      availableStock(rowData) {
        if (!rowData.basic_stock) {
          return '0';
        }
        return rowData.basic_stock.available_stock;
      },
      currentStock(rowData) {
        if (!rowData.basic_stock) {
          return '0';
        }
        return rowData.basic_stock.current_stock;
      },
        getParams () {
        return { 
          filter: [
            [
              'receiving_return.return_date', '>=',
              moment(vars.formData.startDate)
                .startOf('day')
                .format('YYYY-MM-DD 00:00:00'),
            ],
            'and',
            [
              'receiving_return.return_date', '<=',
              moment(vars.formData.endDate)
                .endOf('day')
                .format('YYYY-MM-DD 23:59:59'),
            ],
          ],
          sort: [
            {selector : 'receiving_return.return_date', desc: true}
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
        // const dateFilter = filter.find(v => typeof v === 'object' && v[0] === 'receiving_return.return_date')
        // if (dateFilter) dateFilter[2] = filterValue
        // else filter.push(['receiving_return.return_date', 'between', filterValue])

        // vars.grid['status'].option('filterValue', filter)
        try{
          dataSource.clear()
          vars.grid['status'].beginCustomLoading('데이터를 집계중입니다')
          const params = methods.getParams(); 

          const { data } = await purchaseReceivingReturnItem.load(params);

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
        purchaseReceivingReturnItem.exportData(evt.component, '입고반품현황', `입고반품현황_${Date.now()}.xlsx`);
        evt.cancel = true;
      },
    };

    return { vars, methods, purchaseReceivingReturnItem, dataSource };
  },
};
</script>
