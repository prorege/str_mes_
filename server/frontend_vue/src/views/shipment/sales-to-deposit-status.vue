<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">계산서·입금 현황</div>
            </dx-item>
          </dx-toolbar>
        </div>
        <div>
          <div class="search-status">
            <span class="search-title">발행일자</span>
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
          :on-initialized="evt => methods.onGridInitialized(evt, 'status')"
          :data-source="dataSource"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :focused-row-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :filter-sync-enabled="true"
          @row-dbl-click="methods.goSales"
          @exporting="methods.onExporting"
        >          
          <dx-column caption="계산서번호" data-field="sales_number" :filter-operations="['contains', '=']" />
          <dx-column caption="발행일자" data-field="sales_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
          <dx-column caption="고객업체약칭" data-field="client_alias" />
          <dx-column caption="고객업체" data-field="client_company" />
          <dx-column caption="업체담당자" data-field="client_manager" />
          <dx-column caption="매출부서" data-field="sales_department" />
          <dx-column caption="매출담당자" data-field="sales_manager" />
          <dx-column caption="세율" data-field="tax_rate" />
          <dx-column caption="계산서유형" data-field="sales_type" />
          <dx-column caption="결재유형" data-field="approval_type" />
          <dx-column caption="발행구분" data-field="publish_type" />
          <dx-column caption="본지점구분" data-field="office_type" />
          <dx-column caption="부가세구분" data-field="vat_type" />
          <dx-column caption="공급가" data-field="supply_price" data-type="number" format="currency" />
          <dx-column caption="부가세" data-field="vat" data-type="number" format="currency" />
          <dx-column caption="합계금액" data-field="total_price" data-type="number" format="currency" />
          <dx-column caption="미입금" data-field="not_deposit" data-type="number" format="currency" />
          <dx-column caption="비고" data-field="etc" />

          <dx-sorting mode="single" />
          <dx-export :enabled="true" />
          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-column-chooser mode="select" :enabled="true" />

          <dx-master-detail :enabled="true" template="masterDetailTemplate" />
          <template #masterDetailTemplate="{ data: data }">
            <sales-to-deposit-detail :template-data="data" />
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
import ArrayStore from 'devextreme/data/array_store';
import stateStore from '@/utils/state-store';
import { shipmentSalesStatement } from '../../data-source/shipment';
import SalesToDepositDetail from './sales-to-deposit-detail.vue';
import SearchButtonGroup from '../../components/search-button-group.vue';

export default {
  components: {
    DxButton,
    DxCheckBox,
    DxDateBox,
    DxToolbar, DxItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem,
    DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting,  DxFilterRow, DxMasterDetail, DxColumnChooser,
    SalesToDepositDetail,
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
        stateStore.bind(`shipment-sales-deposit-${key}`, evt.component);

        // methods.initSorting();
        // methods.searchDateRange();
      },
      initSorting() {
        const columns = vars.grid['status'].getVisibleColumns();
        const col = columns.filter(item => item.sortOrder);
        if (col.length == 0) {
          const defaultName = 'sales_date';
          const defaultSort = columns.filter(item => item.name == defaultName);
          if (defaultSort.length > 0) {
            vars.grid['status'].columnOption(defaultSort[0].index, 'sortOrder', 'desc');
          }
        }
      },
      goSales(e) {
        router.push({ path: `/shipment/sales-statement/${e.data.id}` });
      },
      getParams () {
        return { 
          filter: [
            [
              'sales_date', '>=',
              moment(vars.formData.startDate)
                .startOf('day')
                .format('YYYY-MM-DD 00:00:00'),
            ],
            'and',
            [
              'sales_date', '<=',
              moment(vars.formData.endDate)
                .endOf('day')
                .format('YYYY-MM-DD 23:59:59'),
            ],
          ],
          sort: [
            {selector : 'sales_date', desc: true}
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
        // const dateFilter = filter.find(v => typeof v === 'object' && v[0] === 'sales_date')
        // if (dateFilter) dateFilter[2] = filterValue
        // else filter.push(['sales_date', 'between', filterValue])

        // vars.grid['status'].option('filterValue', filter)
         try{
          dataSource.clear()
          vars.grid['status'].beginCustomLoading('데이터를 집계중입니다')
          const params = methods.getParams(); 
   
          const { data } = await shipmentSalesStatement.load(params);

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
        shipmentSalesStatement.exportData(evt.component, '계산서입금현황', `계산서입금현황_${Date.now()}.xlsx`)
        evt.cancel = true
      }
    };

    return { vars, methods, shipmentSalesStatement, dataSource };
  },
};
</script>
