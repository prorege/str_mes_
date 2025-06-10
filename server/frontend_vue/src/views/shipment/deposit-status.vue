<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">

        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">입금현황</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div>
          <div class="search-status">
            <span class="search-title">입금일자</span>
            <dx-date-box :on-value-changed="(e) => vars.formData.startDate = e.value" :on-initialized="(e) => methods.onDateBoxInitialized(e, 'startDate')" />

            <span class="search-bar">~</span>
            <dx-date-box :on-value-changed="(e) => vars.formData.endDate = e.value" :on-initialized="(e) => methods.onDateBoxInitialized(e, 'endDate')" />

            <span class="search-tab"></span>
            <SearchButtonGroup @change="({startDate, endDate}) => { 
                vars.formData.startDate = startDate; 
                vars.formData.endDate = endDate; 

                methods.updateStartDate();
                methods.updateEndDate();
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
          :on-initialized="evt => methods.onGridInitialized(evt, 'status')"
          @exporting="methods.onExporting"
          @row-dbl-click="methods.goSalesDetail"
        >
          <dx-column caption="입금번호" data-field="deposit.deposit_number" data-type="string" :filter-operations="['contains', '=']" />
          <dx-column caption="입금일자" data-field="deposit.deposit_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
          <dx-column caption="고객업체약칭" data-field="deposit.client_alias" data-type="string" />
          <dx-column caption="고객업체" data-field="deposit.client_company" data-type="string" />
          <dx-column caption="업체분류" data-field="client.client_type" data-type="string" />
          <dx-column caption="당사담담자" data-field="client.manager" data-type="string" />
          <dx-column caption="영업부서" data-field="deposit.deposit_department" data-type="string" />
          <dx-column caption="영업담당자" data-field="deposit.deposit_manager" data-type="string" />
          <dx-column caption="비고" data-field="deposit.etc" data-type="string" />
          <dx-column caption="계산서번호" data-field="sales.sales_number" data-type="string" />
          <dx-column caption="금액" data-field="price" data-type="number" format="currency" />
          <dx-column caption="입금형태" data-field="deposit_type" data-type="string" />
          <dx-column caption="입금적요" data-field="etc" data-type="string" />

          <dx-summary>
            <dx-total-item column="price" summary-type="sum" value-format="currency" display-format="금액: {0}" />
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
import { DxDataGrid, DxColumn, DxExport, DxPaging, DxSorting, DxSummary, DxTotalItem, DxFilterRow, DxColumnChooser } from 'devextreme-vue/data-grid';
import ArrayStore from 'devextreme/data/array_store';
import stateStore from '@/utils/state-store';
import { shipmentDepositItem } from '../../data-source/shipment';
import SearchButtonGroup from '../../components/search-button-group.vue';

export default {
  components: {
    DxButton,
    DxCheckBox,
    DxDateBox,
    DxToolbar, DxItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem,
    DxDataGrid, DxColumn, DxExport, DxPaging, DxSorting, DxSummary, DxTotalItem, DxFilterRow, DxColumnChooser,
    SearchButtonGroup,
  },
  setup() {
    const router = useRouter();
    const vars = {};
    vars.grid = {};
    vars.dateBox = {};
    vars.formData = {
      notDeposit: false,
      startDate: new Date(),
      endDate: new Date(),
    };
    const dataSource = new ArrayStore({ key: 'grid_id', data: [] })
    // vars.formData.startDate.setDate(vars.formData.startDate.getDate() - 7);

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
        stateStore.bind(`shipment-deposit-${key}`, evt.component);

        // methods.initSorting();
        // methods.searchDateRange();
      },
      initSorting() {
        const columns = vars.grid['status'].getVisibleColumns();
        const col = columns.filter(item => item.sortOrder);
        if (col.length == 0) {
          const defaultName = 'deposit.deposit_date';
          const defaultSort = columns.filter(item => item.name == defaultName);
          if (defaultSort.length > 0) {
            vars.grid['status'].columnOption(defaultSort[0].index, 'sortOrder', 'desc');
          }
        }
      },
      goSalesDetail({ data }) {
        router.push({ path: `/shipment/deposit/${data.deposit.id}` });
      },
      getParams () {
        return { 
          filter: [
            [
              'deposit.deposit_date', '>=',
              moment(vars.formData.startDate)
                .startOf('day')
                .format('YYYY-MM-DD 00:00:00'),
            ],
            'and',
            [
              'deposit.deposit_date', '<=',
              moment(vars.formData.endDate)
                .endOf('day')
                .format('YYYY-MM-DD 23:59:59'),
            ],
          ],
          sort: [
            {selector : 'deposit.deposit_date', desc: true}
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
        // const dateFilter = filter.find(v => typeof v === 'object' && v[0] === 'deposit.deposit_date')
        // if (dateFilter) dateFilter[2] = filterValue
        // else filter.push(['deposit.deposit_date', 'between', filterValue])

        // vars.grid['status'].option('filterValue', filter)
        try{
          dataSource.clear()
          vars.grid['status'].beginCustomLoading('데이터를 집계중입니다')
          const params = methods.getParams();

          const { data } = await shipmentDepositItem.load(params);

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
        shipmentDepositItem.exportData(evt.component, '입금현황', `입금현황_${Date.now()}.xlsx`);
        evt.cancel = true;
      },
    };

    return { vars, methods, shipmentDepositItem, dataSource };
  },
};
</script>
