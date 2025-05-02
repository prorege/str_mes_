<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">매출계산서현황</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div>
          <div class="search-status">
            <span class="search-title">발행일자</span>
            <dx-date-box :on-value-changed="(e) => vars.formData.startDate = e.value" :on-initialized="(e) => methods.onDateBoxInitialized(e, 'startDate')" />

            <span class="search-bar">~</span>
            <dx-date-box :on-value-changed="(e) => vars.formData.endDate = e.value" :on-initialized="(e) => methods.onDateBoxInitialized(e, 'endDate')" />

            <span class="search-tab"></span>
            <SearchButtonGroup @change="({startDate, endDate}) => { 
              vars.formData.startDate = startDate; 
              vars.formData.endDate = endDate; 
              methods.updateStartDate();
              methods.updateEndDate();
                }" />

            <span class="search-tab"></span>
            <dx-check-box text="미입금" v-model:value="vars.formData.notDeposit" />

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
          :remote-operations="{
            filtering: true,
            grouping: true,
            groupPaging: true,
            paging: true,
            sorting: true,
            summary:false
          }"
          :focused-row-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :data-source="dataSource"
          :filter-sync-enabled="true"
          :on-initialized="(evt) => methods.onGridInitialized(evt, 'status')"
          @exporting="methods.onExporting"
          @row-dbl-click="methods.goSalesDetail"
        >
          <dx-column caption="계산서번호" data-field="sales.sales_number" :filter-operations="['contains', '=']" />
          <dx-column caption="발행일자" data-field="sales.sales_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
          <dx-column caption="고객업체약칭" data-field="sales.client_alias" />
          <dx-column caption="고객업체" data-field="sales.client_company" />
          <dx-column caption="매출부서" data-field="sales.sales_department" />
          <dx-column caption="매출담당자" data-field="sales.sales_manager" />
          <dx-column caption="부가세구분" data-field="sales.vat_type" />
          <dx-column caption="계산서유형" data-field="sales.sales_type" />
          <dx-column caption="결재유형" data-field="sales.approval_type" />
          <dx-column caption="발행구분" data-field="sales.publish_type" />
          <dx-column caption="본지점구분" data-field="sales.office_type" />
          <dx-column caption="추가설명" data-field="note" />
          <dx-column caption="출고번호" data-field="release_number" />
          <dx-column caption="출고반품번호" data-field="release_return_number" />
          <dx-column caption="품목코드" data-field="item_code" />

          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="수량" data-field="quantity" data-type="number" :format="',##0'" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="단가" data-field="unit_price" data-type="number" format="currency" />
          <dx-column caption="공급가" data-field="supply_price" data-type="number" format="currency" />
          <dx-column caption="부가세" data-field="vat" data-type="number" format="currency" />
          <dx-column caption="금액" data-field="total_price" data-type="number" format="currency" />

          <dx-column caption="업체분류" data-field="client.client_type" />
          <dx-column caption="당사담담자" data-field="client.manager" />

          <dx-summary>
            <dx-total-item column="supply_price" show-in-column="supply_price" summary-type="sum" value-format="currency" display-format="{0}"/>
            <dx-total-item column="vat" show-in-column="vat" summary-type="sum" value-format="currency" display-format="{0}"/>
            <dx-total-item column="total_price" show-in-column="total_price" summary-type="sum" value-format="currency" display-format="{0}"/>
          </dx-summary>
          
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

import { useRouter } from 'vue-router';
import { reactive } from 'vue';

import { alert } from 'devextreme/ui/dialog';
import DxButton from 'devextreme-vue/button';
import DxCheckBox from 'devextreme-vue/check-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxExport, DxPaging, DxSorting, DxFilterRow, DxColumnChooser, DxSummary, DxTotalItem } from 'devextreme-vue/data-grid';
import ArrayStore from 'devextreme/data/array_store';
import stateStore from '@/utils/state-store';
import { shipmentSalesStatementItem } from '../../data-source/shipment';
import SearchButtonGroup from '../../components/search-button-group.vue';

export default {
  components: {
    DxButton,
    DxCheckBox,
    DxDateBox,
    DxToolbar, DxItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem,
    DxDataGrid, DxColumn, DxExport, DxPaging, DxSorting, DxFilterRow, DxColumnChooser, DxSummary, DxTotalItem,
    SearchButtonGroup,
  },
  setup() {
    const router = useRouter();
    const vars = {};
    vars.grid = {};
    vars.dateBox = {};
    vars.formData = reactive({
      notDeposit: false,
      startDate: new Date(),
      endDate: new Date(),
    });
    // vars.formData.startDate.setDate(vars.formData.startDate.getDate() - 7);
    const dataSource = new ArrayStore({ key: 'grid_id', data: [] })
    const methods = {
      onDateBoxInitialized(evt, key) {
        vars.dateBox[key] = evt.component;
        if (key == 'startDate') {
          vars.dateBox[key].option('value', vars.formData.startDate);
        } else if (key == 'endDate') {
          vars.dateBox[key].option('value', vars.formData.endDate);
        }
      },
      updateStartDate() {
        vars.dateBox.startDate.option('value', vars.formData.startDate);
      },
      updateEndDate() {
        vars.dateBox.endDate.option('value', vars.formData.endDate);
      },
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`shipment-sales-${key}`, evt.component);

        // methods.initSorting();
        // methods.searchDateRange();
      },
      initSorting() {
        const columns = vars.grid['status'].getVisibleColumns();
        const col = columns.filter(item => item.sortOrder);
        if (col.length == 0) {
          const defaultName = 'sales.sales_date';
          const defaultSort = columns.filter(item => item.name == defaultName);
          if (defaultSort.length > 0) {
            vars.grid['status'].columnOption(defaultSort[0].index, 'sortOrder', 'desc');
          }
        }
      },
      goSalesDetail({ data }) {
        router.push({ path: `/shipment/sales-statement/${data.sales.id}` });
      },
      getParams () {
        return { 
          filter: [
            [
              'sales.sales_date', '>=',
              moment(vars.formData.startDate)
                .startOf('day')
                .format('YYYY-MM-DD 00:00:00'),
            ],
            'and',
            [
              'sales.sales_date', '<=',
              moment(vars.formData.endDate)
                .endOf('day')
                .format('YYYY-MM-DD 23:59:59'),
            ],
          ],
          sort: [
            {selector : 'sales.sales_date', desc: true}
          ],
          skip: 0,
          take: 3000
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
        // const dateFilter = filter.find(v => typeof v === 'object' && v[0] === 'sales.sales_date')
        // if (dateFilter) dateFilter[2] = filterValue
        // else filter.push(['sales.sales_date', 'between', filterValue])

        // if (vars.formData.notDeposit) {
        //   filter.push('and');
        //   filter.push(['not_deposit', '>', 0]);
        // }
        // else {
        //   const index = filter.findIndex(v => typeof v === 'object' && v[0] === 'not_deposit')
        //   if (index >= 0) console.info(`remove filter: ${filter.splice(index - 1, 2)}`)
        // }

        // vars.grid['status'].option('filterValue', filter)
        try{
          dataSource.clear()
          vars.grid['status'].beginCustomLoading('데이터를 집계중입니다')
          const params = methods.getParams(); 
          if (vars.formData.notDeposit) {
            params.filter.push('and');
            params.filter.push(['not_deposit', '>', 0]);
          }
          const { data } = await shipmentSalesStatementItem.load(params);
          console.log("data : ", data)
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
        shipmentSalesStatementItem.exportData(evt.component, '계산서현황', `계산서현황_${Date.now()}.xlsx`);
        evt.cancel = true;
      },
    };

    return { vars, methods, shipmentSalesStatementItem, dataSource };
  },
};
</script>
