<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">입고현황</div>
            </dx-item>
          </dx-toolbar>
        </div>
        
        <div>
          <div class="search-status">
            <span class="search-title">입고일자</span>
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
          @row-dbl-click="methods.goReceivingDetail"
        >
          <dx-column caption="프로젝트명" data-field="project_management.project_name" />
          <dx-column caption="입고번호" data-field="receiving.receiving_number" :filter-operations="['contains', '=']" />
          <dx-column caption="입고일자" data-field="receiving.receiving_date" data-type="date" format="yyyy-MM-dd" :show-in-column-chooser="false" />
          <dx-column caption="공급업체약칭" data-field="receiving.client_alias" />
          <dx-column caption="공급업체" data-field="receiving.client_company" />
          <dx-column caption="입고부서" data-field="receiving.receiving_department" />
          <dx-column caption="입고담당자" data-field="receiving.receiving_manager" />
          <dx-column caption="입고구분" data-field="receiving.receiving_type" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="발주번호" data-field="prereceiving_item.order_number" :filter-operations="['contains', '=']" />
          <dx-column caption="발주수량" data-field="order_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="입고수량" data-field="receiving_quantity" data-type="number" format="fixedPoint" />
          <dx-column caption="미입고수량" data-field="order_item.not_shipped" data-type="number" format="fixedPoint" />
          <dx-column caption="입고창고" data-field="warehouse.wh_name" data-type="string" />
          <dx-column caption="단가" data-field="unit_price" data-type="number" format="₩,##0" />
          <dx-column caption="단위" data-field="item.unit" />
          <dx-column caption="공급가" data-field="supply_price" data-type="number" format="₩,##0" />
          <dx-column caption="요청납기" data-field="request_delivery_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="품목대분류" data-field="item.main_category" />
          <dx-column caption="품목중분류" data-field="item.middle_category" />
          <dx-column caption="품목소분류" data-field="item.sub_category" />
          <dx-column caption="공급사품번" data-field="client_item_number" />
          <dx-column caption="품목설명" data-field="item.item_detail" />
          <dx-column caption="참고사항" data-field="note" />
          <dx-column caption="프로젝트번호" data-field="project_management.project_number" />
          <dx-column caption="LOT번호" data-field="lot_number" />
          <dx-column caption="종결" data-field="closing_yn" />

          <DxGridToolbar>
            <DxItem location="after" template="printTemplate" />
            <DxItem name="exportButton" />
            <DxItem name="columnChooserButton" />
          </DxGridToolbar>
          <template #printTemplate>
            <DxButton icon="print" @click="methods.openClientDialog" />
          </template>

          <dx-summary>
            <dx-total-item column="receiving_quantity" summary-type="sum" value-format="fixedPoint" display-format="입고수량: {0}" />
            <dx-total-item column="supply_price" summary-type="sum" value-format="₩,##0" display-format="공급가: {0}" />
          </dx-summary>

          <dx-sorting mode="single" />
          <dx-export :enabled="true" />
          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-column-chooser mode="select" :enabled="true" />
        </dx-data-grid>
      </div>
    </div>

    <dx-popup
      title="매입일보 출력 업체 선택"
      content-template="popup-content"
      v-model:visible="vars.selectClientDialog.show"
      width="480px"
      height="200px"
      :resize-enabled="false"
      :close-on-outside-click="true">
      <template #popup-content>
        <div>
          <dx-select-box 
            v-model="vars.selectClientDialog.value" 
            :items="vars.selectClientDialog.items" 
            :search-enabled=true
            search-mode="contains"
          />
          <div class="dialog-button-container">
            <dx-button icon="print" text="매입일보 출력" type="default" @click="methods.printDocument" />
          </div>
        </div>
      </template>
    </dx-popup>

  </div>
</template>

<script>
import moment from 'moment';
import numeral from 'numeral';
import { groupBy, orderBy } from 'lodash'

import { reactive } from 'vue';
import { useRouter } from 'vue-router';

import { alert } from 'devextreme/ui/dialog';
import DxButton from 'devextreme-vue/button';
import { DxPopup } from 'devextreme-vue/popup';
import DxCheckBox from 'devextreme-vue/check-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import { DxSelectBox } from 'devextreme-vue/select-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem } from 'devextreme-vue/form';
import { DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxColumnChooser, DxToolbar as DxGridToolbar, DxSummary, DxTotalItem } from 'devextreme-vue/data-grid';

import SearchButtonGroup from '../../components/search-button-group.vue';
import ArrayStore from 'devextreme/data/array_store';
import stateStore from '@/utils/state-store';
import { purchaseReceivingItem, getPurchaseReceivingItem } from '../../data-source/purchase';
import {printDocument} from '@/utils/print-document';

export default {
  components: {
    DxButton,
    DxCheckBox,
    DxDateBox,
    DxToolbar, DxItem,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem,
    DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, DxColumnChooser, DxGridToolbar, DxSummary, DxTotalItem,
    DxPopup,
    DxSelectBox,
    SearchButtonGroup,
  },
  setup() {
    const router = useRouter();
    const vars = {};
    vars.grid = {};
    vars.dateBox = {};

    vars.formData = {
      startDate: new Date(),
      endDate: new Date(),
    };
    const dataSource = new ArrayStore({ key: 'grid_id', data: [] })
    // vars.formData.startDate.setDate(vars.formData.startDate.getDate() - 7);
    vars.selectClientDialog = reactive({
      show: false,
      value: null,
      data: [],
      items: []
    })
    vars.filter = reactive({status: []});

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
        stateStore.bind(`purchase-receiving-${key}`, evt.component);

        // methods.initSorting();
        // methods.searchDateRange();
      },
      initSorting() {
        const columns = vars.grid['status'].getVisibleColumns();
        const col = columns.filter(item => item.sortOrder);
        if (col.length == 0) {
          const defaultName = 'receiving.receiving_date';
          const defaultSort = columns.filter(item => item.name == defaultName);
          if (defaultSort.length > 0) {
            vars.grid['status'].columnOption(defaultSort[0].index, 'sortOrder', 'desc');
          }
        }
      },
      goReceivingDetail({ data }) {
        router.push({ path: `/purchase/receiving/${data.receiving.id}` });
      },
      getParams () {
        return { 
          filter: [
            [
              'receiving.receiving_date', '>=',
              moment(vars.formData.startDate)
                .startOf('day')
                .format('YYYY-MM-DD 00:00:00'),
            ],
            'and',
            [
              'receiving.receiving_date', '<=',
              moment(vars.formData.endDate)
                .endOf('day')
                .format('YYYY-MM-DD 23:59:59'),
            ],
          ],
          sort: [
            {selector : 'receiving.receiving_date', desc: true}
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
        // const dateFilter = filter.find(v => typeof v === 'object' && v[0] === 'receiving.receiving_date')
        // if (dateFilter) dateFilter[2] = filterValue
        // else filter.push(['receiving.receiving_date', 'between', filterValue])

        // vars.grid['status'].option('filterValue', filter)
          try{
          dataSource.clear()
          vars.grid['status'].beginCustomLoading('데이터를 집계중입니다')
          const params = methods.getParams(); 
      
          const { data } = await purchaseReceivingItem.load(params);

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
        purchaseReceivingItem.exportData(evt.component, '입고현황', `입고현황_${Date.now()}.xlsx`)
        evt.cancel = true
      },
      async printDocument () {
        vars.selectClientDialog.show = false

        const mutateItem = (item) => {
          item.unit_price = parseFloat(item.unit_price)
          item.receiving_quantity = parseInt(item.receiving_quantity, 10)
          item.supply_price = parseFloat(item.supply_price)
          item.price = Math.round(item.unit_price * item.receiving_quantity)

          item.unit_price_s = numeral(item.unit_price).format('0,0.0000')
          item.receiving_quantity_s = numeral(item.receiving_quantity).format('0,0')
          item.supply_price_s = numeral(item.supply_price).format('0,0.00')
          item.price_s = numeral(item.price).format('0,0')
          return item
        }

        const reduceItem = (list) => {
          const reducedValue = list.reduce(
            (t, i) => {
              t.receiving_quantity += i.receiving_quantity
              t.supply_price += i.supply_price
              t.price += Math.floor(i.price.toFixed(5))
              return t
            }, 
            {
              receiving_quantity: 0,
              supply_price: 0,
              price: 0
            }
          )
          reducedValue.receiving_quantity = numeral(reducedValue.receiving_quantity).format('0,0')
          reducedValue.supply_price = numeral(reducedValue.supply_price).format('0,0.00')
          reducedValue.price = numeral(reducedValue.price).format('0,0')
          return reducedValue
        }

        const data = vars.selectClientDialog.data.filter(v => v.receiving.client_company === vars.selectClientDialog.value)
        
        const params = {
          info: {
            startDate: moment(vars.formData.startDate).format('YYYY-MM-DD'),
            endDate: moment(vars.formData.endDate).format('YYYY-MM-DD')
          },
          list: [],
          summary: {}
        }

        for (const item of data) {
          const exists = params.list.find(v => v.client_company === item.receiving.client_company && v.date === item.receiving.receiving_date)
          if (exists) exists.list.push(mutateItem(item))
          else {
            params.list.push({
              client_company: item.receiving.client_company,
              date: item.receiving.receiving_date,
              dateStr: moment(item.receiving.receiving_date).format('YYYY-MM-DD'),
              summary: {},
              list: [mutateItem(item)]
            })
          }
        }
        
        for (const item of params.list) {
          item.summary = reduceItem(item.list)
        }
        params.summary = reduceItem(data)
        params.list = orderBy(params.list, ['date'], ['asc'])
        await printDocument('purchasehistory', params)
      },
      async openClientDialog () {
        const {data} = await purchaseReceivingItem.load({
          filter: [
            [
              'receiving.receiving_date',
              '>=',
              moment(vars.formData.startDate).startOf('day').format('YYYY-MM-DD 00:00:00'),
            ],
            'and',
            [
              'receiving.receiving_date',
              '<=',
              moment(vars.formData.endDate).endOf('day').format('YYYY-MM-DD 23:59:59'),
            ],
          ],
          skip: 0,
          take: 3000
        })

        const grouped = groupBy(data, 'receiving.client_company')
        vars.selectClientDialog.data = data
        vars.selectClientDialog.items = Object.keys(grouped)
        vars.selectClientDialog.value = vars.selectClientDialog.items.length ? vars.selectClientDialog.items[0] : null;
        vars.selectClientDialog.show = true
      }
    };

    return { vars, methods, purchaseReceivingItem, dataSource };
  },
};
</script>

<style lang="scss" scoped>
.dialog-button-container {
  margin-top: 10px;
  text-align: center;
}
</style>