<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">출고현황</div>
            </dx-item>
          </dx-toolbar>
        </div>
        <div>
          <div class="search-status">
            <span class="search-title">출고일자</span>
            <dx-date-box :on-value-changed="(e) => vars.formData.startDate = e.value" :on-initialized="(e) => methods.onDateBoxInitialized(e, 'startDate')" />

            <span class="search-bar">~</span>
            <dx-date-box :on-value-changed="(e) => vars.formData.endDate = e.value" :on-initialized="(e) => methods.onDateBoxInitialized(e, 'endDate')" />

            <span class="search-tab"></span>
            <SearchButtonGroup
              @change="({ startDate, endDate }) => {
                vars.formData.startDate = startDate;
                vars.formData.endDate = endDate;

                methods.updateStartDate();
                methods.updateEndDate();
              }"
            />

            <span class="search-tab"></span>
            <dx-check-box text="미계산서" :on-value-changed="(e) => vars.formData.notSales = e.value" v-model:value="vars.formData.notSales" />

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
          @row-dbl-click="methods.goReleaseDetail"
        >
          <dx-column caption="출고번호" data-field="release.release_number" data-type="string" :filter-operations="['contains', '=']" />
          <dx-column caption="출고일자" data-field="release.release_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
          <dx-column caption="고객업체약칭" data-field="release.client_alias" data-type="string" />
          <dx-column caption="고객업체" data-field="release.client_company" data-type="string" />
          <dx-column caption="견적부서" data-field="release.release_department" data-type="string" />
          <dx-column caption="출고담당자" data-field="release.release_manager" data-type="string" />
          <dx-column caption="출고구분" data-field="release.release_type" data-type="string" />
          <dx-column caption="품목코드" data-field="item_code" data-type="string" />
          <dx-column caption="품명" data-field="item.item_name" data-type="string" />
          <dx-column caption="규격" data-field="item.item_standard" data-type="string" />
          <dx-column caption="수주수량" data-field="order_item.order_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="출고수량" data-field="release_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="출고창고" data-field="warehouse.wh_name" data-type="string" />
          <dx-column caption="단가" data-field="unit_price" data-type="number" format="currency" />
          <dx-column caption="단위" data-field="item.unit" data-type="string" />
          <dx-column caption="공급가" data-field="supply_price" data-type="number" format="currency" :calculate-cell-value="methods.calcSupplyPrice" />
          <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="미계산서" data-field="non_invoice" data-type="number" format="fixedPoint" />
          <dx-column caption="품목대분류" data-field="item.main_category" data-type="string" />
          <dx-column caption="품목중분류" data-field="item.middle_category" data-type="string" />
          <dx-column caption="품목소분류" data-field="item.sub_category" data-type="string" />
          <dx-column caption="수주번호" data-field="order_number" data-type="string" />
          <dx-column caption="고객사품번" data-field="client_item_number" data-type="string" />
          <dx-column caption="품목설명" data-field="item.item_detail" data-type="string" />
          <dx-column caption="업체분류" data-field="client.client_type" data-type="string" />
          <dx-column caption="당사담담자" data-field="client.manager" data-type="string" />
          <dx-column caption="참고사항" data-field="note" data-type="string" />
          <dx-column caption="프로젝트번호" data-field="project_management.project_number" data-type="string" />
          <dx-column caption="종결" data-field="closing_yn" data-type="boolean" />

          <dx-summary>
            <dx-total-item column="release_quantity" summary-type="sum" value-format="fixedPoint" display-format="출고수량: {0}" />
            <dx-total-item column="supply_price" summary-type="sum" value-format="₩,##0" display-format="공급가: {0}" />
          </dx-summary>

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
import { DxDataGrid, DxColumn, DxExport, DxPaging, DxSorting, DxFilterRow, DxColumnChooser, DxSummary, DxTotalItem } from 'devextreme-vue/data-grid';
import ArrayStore from 'devextreme/data/array_store';
import stateStore from '@/utils/state-store';
import { shipmentReleaseItem } from '../../data-source/shipment';
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
    vars.formData = {
      notSales: false,
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
        stateStore.bind(`shipment-release-${key}`, evt.component);

        // methods.initSorting();
        // methods.searchDateRange();
      },
      initSorting() {
        const columns = vars.grid['status'].getVisibleColumns();
        const col = columns.filter((item) => item.sortOrder);
        if (col.length == 0) {
          const defaultName = 'release.release_date';
          const defaultSort = columns.filter((item) => item.name == defaultName);
          if (defaultSort.length > 0) {
            vars.grid['status'].columnOption(defaultSort[0].index, 'sortOrder', 'desc');
          }
        }
      },
      goReleaseDetail({ data }) {
        router.push({ path: `/shipment/release/${data.release.id}` });
      },
      calcSupplyPrice(rowData) {
        let supply_price = 0;
        if (rowData.release_quantity && rowData.unit_price) {
          supply_price = rowData.release_quantity * rowData.unit_price;
        }
        rowData.supply_price = supply_price;
        return supply_price;
      },
      getParams () {
        return { 
          filter: [
            [
              'release.release_date', '>=',
              moment(vars.formData.startDate)
                .startOf('day')
                .format('YYYY-MM-DD 00:00:00'),
            ],
            'and',
            [
              'release.release_date', '<=',
              moment(vars.formData.endDate)
                .endOf('day')
                .format('YYYY-MM-DD 23:59:59'),
            ],
          ],
          sort: [
            {selector : 'release.release_date', desc: true}
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
          if (vars.formData.notSales) {
            params.filter.push('and');
            params.filter.push(['non_invoice', '>', 0]);
          }
          const { data } = await shipmentReleaseItem.load(params);

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
        shipmentReleaseItem.exportData(evt.component, '출고현황', `출고현황_${Date.now()}.xlsx`);
        evt.cancel = true;
      },
    };

    return { vars, methods, shipmentReleaseItem, dataSource };
  },
};
</script>
