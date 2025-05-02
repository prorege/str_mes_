<template>
  <div>
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">원가마감</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div>
          <div class="search-status search-line">
            <span class="search-title">기간</span>

            <dx-date-box v-model:value="vars.formData.startDate" />
            <span class="search-bar">~</span>
            <dx-date-box v-model:value="vars.formData.endDate" />
            <span class="search-tab"></span>

            <span class="search-title">마감창고</span>
            <dx-select-box
              value-expr="wh_code"
              display-expr="wh_name"  
              v-model:value="vars.formData.warehouseCode"
              :data-source="vars.dataSource.warehouse"
            />
            <span class="search-tab"></span>

            <span class="search-title">품목코드</span>
            <dx-text-box v-model:value="vars.formData.itemCode">
              <dx-text-box-button name="search2" location="after"
                :options="{ icon: 'clear', stylingMode: 'text', onClick: () => (vars.formData.itemCode = null) }"
              />
              <dx-text-box-button name="search" location="after"
                :options="{ icon: 'search', stylingMode: 'text', onClick: () => (vars.dlg.findItem.show = true) }"
              />
            </dx-text-box>
          </div>

          <div class="search-status">
            <dx-button text="입고단가 누락 조회" icon="search" @click="methods.searchMissingCost()" />
            <span class="search-tab"></span>
            <dx-check-box text="" v-model:value="vars.formData.searchComplete" />

            <span class="search-tab"></span>
            <span class="search-tab"></span>

            <dx-button text="원가마감 산정 및 적용" icon="money" @click="methods.closeCost()" />
            <span class="search-tab"></span>
            <dx-check-box text="" v-model:value="vars.formData.closingComplete" :read-only="true" />

            <span class="search-tab"></span>
            <span class="search-tab"></span>

            <dx-button text="출고원가 누락 조회" icon="search" @click="methods.searchMissingReleaseCost()" />

            <span class="search-tab"></span>
            <span class="search-tab"></span>

            <dx-button text="마감재고 원가 적용" icon="check" @click="methods.applyCost()" />
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
          :data-source="costClosing"
          :on-initialized="evt => methods.onGridInitialized(evt, 'history')"
        >
          <dx-column caption="마감처리일자" data-field="created" data-type="datetime" format="yyyy-MM-dd HH:mm:ss" :sort-index="1" sort-order="desc" />
          <dx-column caption="마감창고" data-field="warehouse.wh_name" data-type="string" />
          <dx-column caption="마감기간(시작)" data-field="start_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="마감기간(종료)" data-field="end_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="마감담당자" data-field="manager" data-type="string" />
          <dx-column caption="원가마감 적용" data-field="closed" data-type="boolean" />
          <dx-column caption="마감재고 적용" data-field="applied" data-type="boolean" />

          <dx-sorting mode="single" />
          <dx-export :enabled="true" />
          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-column-chooser mode="select" :enabled="true" />
        </dx-data-grid>
      </div>

      <dx-popup
        title="입고단가 누락"
        content-template="popup-content"
        v-model:visible="vars.dlg.missingCostItem.show"
        :width="1200"
        :height="800"
        :resize-enabled="true"
        :close-on-outside-click="true"
        @initialized="evt => methods.onGridInitialized(evt, 'item-popup')"
      >
        <template #popup-content>
          <dx-scroll-view>

            <div class="dx-card responsive-paddings back-colored">
              <div class="content-header">
                <dx-toolbar class="back-colored">
                  <dx-item location="before">
                    <div class="content-title">입고</div>
                  </dx-item>
                </dx-toolbar>
              </div>

              <dx-data-grid
                column-resizing-mode="widget"
                :show-borders="true"
                :column-auto-width="true"
                :remote-operations="true"
                :allow-column-resizing="true"
                :allow-column-reordering="true"
                :data-source="vars.dataSource.purchaseReceivingItem"
                :on-initialized="evt => methods.onGridInitialized(evt, 'purchaseReceivingItem')"
              >
                <dx-column caption="입고번호" data-field="receiving.receiving_number" />
                <dx-column caption="입고일자" data-field="receiving.receiving_date2" data-type="date" format="yyyy-MM-dd" />
                <dx-column caption="품목코드" data-field="item_code" />
                <dx-column caption="품명" data-field="item.item_name" />

                <dx-paging :page-size="20" />
                <dx-filter-row :visible="true" />
              </dx-data-grid>
            </div>

            <div class="dx-card responsive-paddings back-colored mt-1">
              <div class="content-header">
                <dx-toolbar class="back-colored">
                  <dx-item location="before">
                    <div class="content-title">기타입고</div>
                  </dx-item>
                </dx-toolbar>
              </div>

              <dx-data-grid
                column-resizing-mode="widget"
                :show-borders="true"
                :column-auto-width="true"
                :remote-operations="true"
                :allow-column-resizing="true"
                :allow-column-reordering="true"
                :data-source="vars.dataSource.stockEtcItem"
                :on-initialized="evt => methods.onGridInitialized(evt, 'stockEtcItem')"
              >
                <dx-column caption="입고번호" data-field="stock_etc.number" />
                <dx-column caption="입고일자" data-field="stock_etc.target_date" data-type="date" format="yyyy-MM-dd" />
                <dx-column caption="품목코드" data-field="item_code" />
                <dx-column caption="품명" data-field="item.item_name" />

                <dx-paging :page-size="20" />
                <dx-filter-row :visible="true" />
              </dx-data-grid>
            </div>

            <div class="dx-card responsive-paddings back-colored mt-1">
              <div class="content-header">
                <dx-toolbar class="back-colored">
                  <dx-item location="before">
                    <div class="content-title">재고이동입고</div>
                  </dx-item>
                </dx-toolbar>
              </div>

              <dx-data-grid
                column-resizing-mode="widget"
                :show-borders="true"
                :column-auto-width="true"
                :remote-operations="true"
                :allow-column-resizing="true"
                :allow-column-reordering="true"
                :data-source="vars.dataSource.stockMoveReleaseItem"
                :on-initialized="evt => methods.onGridInitialized(evt, 'stockMoveReleaseItem')"
              >
                <dx-column caption="입고번호" data-field="stock_move_release.number" />
                <dx-column caption="입고일자" data-field="stock_move_release.target_date" data-type="date" format="yyyy-MM-dd" />
                <dx-column caption="품목코드" data-field="item_code" />
                <dx-column caption="품명" data-field="item.item_name" />

                <dx-paging :page-size="20" />
                <dx-filter-row :visible="true" />
              </dx-data-grid>
            </div>

            <div class="dx-card responsive-paddings back-colored mt-1">
              <div class="content-header">
                <dx-toolbar class="back-colored">
                  <dx-item location="before">
                    <div class="content-title">생산입고</div>
                  </dx-item>
                </dx-toolbar>
              </div>

              <dx-data-grid
                column-resizing-mode="widget"
                :show-borders="true"
                :column-auto-width="true"
                :remote-operations="true"
                :allow-column-resizing="true"
                :allow-column-reordering="true"
                :data-source="vars.dataSource.performanceRegistrationItem"
                :on-initialized="evt => methods.onGridInitialized(evt, 'performanceRegistrationItem')"
              >
                <dx-column caption="입고번호" data-field="performance_registration.number" />
                <dx-column caption="입고일자" data-field="performance_registration.target_date" data-type="date" format="yyyy-MM-dd" />
                <dx-column caption="품목코드" data-field="item_code" />
                <dx-column caption="품명" data-field="item.item_name" />

                <dx-paging :page-size="20" />
                <dx-filter-row :visible="true" />
              </dx-data-grid>
            </div>

            <div class="dx-card responsive-paddings back-colored mt-1">
              <div class="content-header">
                <dx-toolbar class="back-colored">
                  <dx-item location="before">
                    <div class="content-title">출고반품</div>
                  </dx-item>
                </dx-toolbar>
              </div>

              <dx-data-grid
                column-resizing-mode="widget"
                :show-borders="true"
                :column-auto-width="true"
                :remote-operations="true"
                :allow-column-resizing="true"
                :allow-column-reordering="true"
                :data-source="vars.dataSource.shipmentReleaseReturnItem"
                :on-initialized="evt => methods.onGridInitialized(evt, 'shipmentReleaseReturnItem')"
              >
                <dx-column caption="반품번호" data-field="release_return.return_number" />
                <dx-column caption="반품일자" data-field="release_return.return_date" data-type="date" format="yyyy-MM-dd" />
                <dx-column caption="품목코드" data-field="item_code" />
                <dx-column caption="품명" data-field="item.item_name" />

                <dx-paging :page-size="20" />
                <dx-filter-row :visible="true" />
              </dx-data-grid>
            </div>

            <div class="dx-card responsive-paddings back-colored mt-1">
              <div class="content-header">
                <dx-toolbar class="back-colored">
                  <dx-item location="before">
                    <div class="content-title">통관</div>
                  </dx-item>
                </dx-toolbar>
              </div>

              <dx-data-grid
                column-resizing-mode="widget"
                :show-borders="true"
                :column-auto-width="true"
                :remote-operations="true"
                :allow-column-resizing="true"
                :allow-column-reordering="true"
                :data-source="vars.dataSource.importClearanceItem"
                :on-initialized="evt => methods.onGridInitialized(evt, 'importClearanceItem')"
              >
                <dx-column caption="통관번호" data-field="import_clearance.clearance_number" />
                <dx-column caption="통관일자" data-field="import_clearance.clearance_date" data-type="date" format="yyyy-MM-dd" />
                <dx-column caption="품목코드" data-field="item_code" />
                <dx-column caption="품명" data-field="item.item_name" />

                <dx-paging :page-size="20" />
                <dx-filter-row :visible="true" />
              </dx-data-grid>
            </div>

          </dx-scroll-view>
        </template>
      </dx-popup>

      <dx-popup
        title="출고원가 누락"
        content-template="popup-content"
        v-model:visible="vars.dlg.missingReleaseCostItem.show"
        :width="1200"
        :height="800"
        :resize-enabled="true"
        :close-on-outside-click="true"
        @initialized="evt => methods.onGridInitialized(evt, 'item-popup')"
      >
        <template #popup-content>
          <dx-scroll-view>

            <div class="dx-card responsive-paddings back-colored">
              <div class="content-header">
                <dx-toolbar class="back-colored">
                  <dx-item location="before">
                    <div class="content-title">출고</div>
                  </dx-item>
                </dx-toolbar>
              </div>

              <dx-data-grid
                column-resizing-mode="widget"
                :show-borders="true"
                :column-auto-width="true"
                :remote-operations="true"
                :allow-column-resizing="true"
                :allow-column-reordering="true"
                :data-source="vars.dataSource.shipmentReleaseItem"
                :on-initialized="evt => methods.onGridInitialized(evt, 'shipmentReleaseItem')"
              >
                <dx-column caption="입고번호" data-field="release.release_number" />
                <dx-column caption="입고일자" data-field="release.release_date" data-type="date" format="yyyy-MM-dd" />
                <dx-column caption="품목코드" data-field="item_code" />
                <dx-column caption="품명" data-field="item.item_name" />

                <dx-paging :page-size="20" />
                <dx-filter-row :visible="true" />
              </dx-data-grid>
            </div>

            <div class="dx-card responsive-paddings back-colored mt-1">
              <div class="content-header">
                <dx-toolbar class="back-colored">
                  <dx-item location="before">
                    <div class="content-title">기타출고</div>
                  </dx-item>
                </dx-toolbar>
              </div>

              <dx-data-grid
                column-resizing-mode="widget"
                :show-borders="true"
                :column-auto-width="true"
                :remote-operations="true"
                :allow-column-resizing="true"
                :allow-column-reordering="true"
                :data-source="vars.dataSource.stockEtcReleaseItem"
                :on-initialized="evt => methods.onGridInitialized(evt, 'stockEtcReleaseItem')"
              >
                <dx-column caption="입고번호" data-field="stock_etc.number" />
                <dx-column caption="입고일자" data-field="stock_etc.target_date" data-type="date" format="yyyy-MM-dd" />
                <dx-column caption="품목코드" data-field="item_code" />
                <dx-column caption="품명" data-field="item.item_name" />

                <dx-paging :page-size="20" />
                <dx-filter-row :visible="true" />
              </dx-data-grid>
            </div>

            <div class="dx-card responsive-paddings back-colored mt-1">
              <div class="content-header">
                <dx-toolbar class="back-colored">
                  <dx-item location="before">
                    <div class="content-title">재고이동출고</div>
                  </dx-item>
                </dx-toolbar>
              </div>

              <dx-data-grid
                column-resizing-mode="widget"
                :show-borders="true"
                :column-auto-width="true"
                :remote-operations="true"
                :allow-column-resizing="true"
                :allow-column-reordering="true"
                :data-source="vars.dataSource.stockMoveReleaseReleaseItem"
                :on-initialized="evt => methods.onGridInitialized(evt, 'stockMoveReleaseReleaseItem')"
              >
                <dx-column caption="입고번호" data-field="stock_move_release.number" />
                <dx-column caption="입고일자" data-field="stock_move_release.target_date" data-type="date" format="yyyy-MM-dd" />
                <dx-column caption="품목코드" data-field="item_code" />
                <dx-column caption="품명" data-field="item.item_name" />

                <dx-paging :page-size="20" />
                <dx-filter-row :visible="true" />
              </dx-data-grid>
            </div>

            <div class="dx-card responsive-paddings back-colored mt-1">
              <div class="content-header">
                <dx-toolbar class="back-colored">
                  <dx-item location="before">
                    <div class="content-title">자재소모</div>
                  </dx-item>
                </dx-toolbar>
              </div>

              <dx-data-grid
                column-resizing-mode="widget"
                :show-borders="true"
                :column-auto-width="true"
                :remote-operations="true"
                :allow-column-resizing="true"
                :allow-column-reordering="true"
                :data-source="vars.dataSource.materialConsumeItem"
                :on-initialized="evt => methods.onGridInitialized(evt, 'materialConsumeItem')"
              >
                <dx-column caption="입고번호" data-field="performance_registration.number" />
                <dx-column caption="입고일자" data-field="performance_registration.target_date" data-type="date" format="yyyy-MM-dd" />
                <dx-column caption="품목코드" data-field="item_code" />
                <dx-column caption="품명" data-field="item.item_name" />

                <dx-paging :page-size="20" />
                <dx-filter-row :visible="true" />
              </dx-data-grid>
            </div>

            <div class="dx-card responsive-paddings back-colored mt-1">
              <div class="content-header">
                <dx-toolbar class="back-colored">
                  <dx-item location="before">
                    <div class="content-title">입고반품</div>
                  </dx-item>
                </dx-toolbar>
              </div>

              <dx-data-grid
                column-resizing-mode="widget"
                :show-borders="true"
                :column-auto-width="true"
                :remote-operations="true"
                :allow-column-resizing="true"
                :allow-column-reordering="true"
                :data-source="vars.dataSource.purchaseReceivingReturnItem"
                :on-initialized="evt => methods.onGridInitialized(evt, 'purchaseReceivingReturnItem')"
              >
                <dx-column caption="반품번호" data-field="receiving_return.return_number" />
                <dx-column caption="반품일자" data-field="receiving_return.return_date" data-type="date" format="yyyy-MM-dd" />
                <dx-column caption="품목코드" data-field="item_code" />
                <dx-column caption="품명" data-field="item.item_name" />

                <dx-paging :page-size="20" />
                <dx-filter-row :visible="true" />
              </dx-data-grid>
            </div>

            <div class="dx-card responsive-paddings back-colored mt-1">
              <div class="content-header">
                <dx-toolbar class="back-colored">
                  <dx-item location="before">
                    <div class="content-title">수출</div>
                  </dx-item>
                </dx-toolbar>
              </div>

              <dx-data-grid
                column-resizing-mode="widget"
                :show-borders="true"
                :column-auto-width="true"
                :remote-operations="true"
                :allow-column-resizing="true"
                :allow-column-reordering="true"
                :data-source="vars.dataSource.exportCommInvoiceItem"
                :on-initialized="evt => methods.onGridInitialized(evt, 'exportCommInvoiceItem')"
              >
                <dx-column caption="통관번호" data-field="export_comm_invoice.invoice_number" />
                <dx-column caption="통관일자" data-field="export_comm_invoice.invoice_date" data-type="date" format="yyyy-MM-dd" />
                <dx-column caption="품목코드" data-field="item_code" />
                <dx-column caption="품명" data-field="item.item_name" />

                <dx-paging :page-size="20" />
                <dx-filter-row :visible="true" />
              </dx-data-grid>
            </div>

          </dx-scroll-view>
        </template>
      </dx-popup>

      <dx-popup
      title="품목찾기"  
      content-template="popup-content"
      v-model:visible="vars.dlg.findItem.show"
      :width="680"
      :height="460"
      :resize-enabled="true"
      :close-on-outside-click="true"
      @initialized="evt => methods.onGridInitialized(evt, 'find-item-popup')"
    >
      <template #popup-content>
        <dx-data-grid
          column-resizing-mode="widget"
          :show-borders="true"
          :remote-operations="true"
          :column-auto-width="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="vars.dataSource.baseItem"
          :on-initialized="evt => methods.onGridInitialized(evt, 'baseItem')"
          @selection-changed="methods.selectItem"
        >
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item_name" />
          <dx-column caption="규격" data-field="item_standard" />
          <dx-column caption="자산구분" data-field="asset_type" />

          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          <dx-selection mode="single" select-all-mode="page" show-check-boxes-mode="onClick"/>
        </dx-data-grid>
      </template>
    </dx-popup>

    </div>
  </div>
</template>

<script>
import moment from 'moment';

import { useRouter } from 'vue-router';
import { ref, reactive, onMounted } from 'vue';

import { alert, confirm } from 'devextreme/ui/dialog';
import DxButton from 'devextreme-vue/button';
import DxCheckBox from 'devextreme-vue/check-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxSelectBox from 'devextreme-vue/select-box';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import { DxScrollView } from 'devextreme-vue/scroll-view';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxTextBox, DxButton as DxTextBoxButton } from 'devextreme-vue/text-box';
import { DxForm, DxLabel, DxGroupItem, DxSimpleItem } from 'devextreme-vue/form';
import {DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxSelection, DxFilterRow, DxColumnChooser } from 'devextreme-vue/data-grid';

import stateStore from '@/utils/state-store';
import { costClosing } from '../../data-source/cost';
import { getBaseItem, getBaseWarehouse } from '../../data-source/base';
import { getPurchaseReceivingItem, getPurchaseReceivingReturnItem } from '../../data-source/purchase';
import { getStockEtcItem, getStockMoveReleaseItem } from '../../data-source/stock';
import { getPerformanceItem1, getPerformanceItem2 } from '../../data-source/produce';
import { getShipmentReleaseItem, getShipmentReleaseReturnItem } from '../../data-source/shipment';
import { getImportClearanceItem } from '../../data-source/import';
import { getCommInvoiceItem } from '../../data-source/export';

import authService from '../../auth';
import ApiService from '../../utils/api-service';

export default {
  components: {
    DxButton,
    DxCheckBox,
    DxDateBox,
    DxSelectBox,
    DxLoadPanel,
    DxScrollView,
    DxToolbar, DxItem,
    DxPopup, DxToolbarItem,
    DxTextBox, DxTextBoxButton,
    DxForm, DxLabel, DxGroupItem, DxSimpleItem,
    DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxSelection, DxFilterRow, DxColumnChooser,
  },
  setup() {
    const router = useRouter();
    const vars = {};
    vars.dlg = {};
    vars.dlg.missingCostItem = reactive({ show: false });
    vars.dlg.missingReleaseCostItem = reactive({ show: false });
    vars.dlg.findItem = reactive({ show: false });
    vars.loading = ref(false);
    vars.grid = {};
    vars.now = new Date();
    vars.formData = reactive({
      searchComplete: false,
      closingComplete: false,
      warehouseCode: null,
      startDate: new Date(vars.now.getFullYear(), vars.now.getMonth() - 1, 1),
      endDate: new Date(vars.now.getFullYear(), vars.now.getMonth(), 0),
      historyId: null,
      itemCode: null,
    });
    vars.filter = {
      purchaseReceivingItem: [
        {name: 'warehouse_code', op: 'eq', val: null},
        {name: 'receiving', op: 'has', val: {name: 'receiving_date2', op: 'gte', val: ''}},
        {name: 'receiving', op: 'has', val: {name: 'receiving_date2', op: 'lte', val: ''}},
        {'or': [{name: 'unit_price', op: 'eq', val: 0}, {name: 'unit_price', op: 'is_null', val: null}]},
      ],
      stockEtcItem: [
        {name: 'warehouse_code', op: 'eq', val: null},
        {name: 'stock_etc', op: 'has', val: {name: 'target_date', op: 'gte', val: ''}},
        {name: 'stock_etc', op: 'has', val: {name: 'target_date', op: 'lte', val: ''}},
        {name: 'inout_type', op: 'eq', val: '입고'},
        {'or': [{name: 'unit_price', op: 'eq', val: 0}, {name: 'unit_price', op: 'is_null', val: null}]},
      ],
      stockMoveReleaseItem: [
        {name: 'in_warehouse', op: 'eq', val: null},
        {name: 'stock_move_release', op: 'has', val: {name: 'target_date', op: 'gte', val: ''}},
        {name: 'stock_move_release', op: 'has', val: {name: 'target_date', op: 'lte', val: ''}},
        {name: 'in_warehouse', op: 'neq', val: '공장창고'},
        {'or': [{name: 'cost_price', op: 'eq', val: 0}, {name: 'cost_price', op: 'is_null', val: null}]},
      ],
      performanceRegistrationItem: [
        {name: 'warehouse_code', op: 'eq', val: null},
        {name: 'performance_registration', op: 'has', val: {name: 'target_date', op: 'gte', val: ''}},
        {name: 'performance_registration', op: 'has', val: {name: 'target_date', op: 'lte', val: ''}},
        {'or': [{name: 'unit_price', op: 'eq', val: 0}, {name: 'unit_price', op: 'is_null', val: null}]},
      ],
      shipmentReleaseReturnItem: [
        {name: 'warehouse_code', op: 'eq', val: null},
        {name: 'release_return', op: 'has', val: {name: 'return_date', op: 'gte', val: ''}},
        {name: 'release_return', op: 'has', val: {name: 'return_date', op: 'lte', val: ''}},
        {'or': [{
          name: 'release_item', op: 'has', val: {name: 'unit_price', op: 'eq', val: 0}
        }, {
          name: 'release_item', op: 'has', val: {name: 'unit_price', op: 'is_null', val: null}
        }]},
      ],
      importClearanceItem: [
        {name: 'warehouse_code', op: 'eq', val: null},
        {name: 'import_clearance', op: 'has', val: {name: 'clearance_date', op: 'gte', val: ''}},
        {name: 'import_clearance', op: 'has', val: {name: 'clearance_date', op: 'lte', val: ''}},
        {'or': [{name: 'won_price', op: 'eq', val: 0}, {name: 'won_price', op: 'is_null', val: null}]},
      ],
      shipmentReleaseItem: [
        {name: 'warehouse_code', op: 'eq', val: null},
        {name: 'release', op: 'has', val: {name: 'release_date', op: 'gte', val: ''}},
        {name: 'release', op: 'has', val: {name: 'release_date', op: 'lte', val: ''}},
        {name: 'cost_price', op: 'is_null', val: null}
      ],
      stockEtcReleaseItem: [
        {name: 'warehouse_code', op: 'eq', val: null},
        {name: 'stock_etc', op: 'has', val: {name: 'target_date', op: 'gte', val: ''}},
        {name: 'stock_etc', op: 'has', val: {name: 'target_date', op: 'lte', val: ''}},
        {name: 'inout_type', op: 'eq', val: '출고'},
        {name: 'cost_price', op: 'is_null', val: null}
      ],
      stockMoveReleaseReleaseItem: [
        {name: 'out_warehouse', op: 'eq', val: null},
        {name: 'stock_move_release', op: 'has', val: {name: 'target_date', op: 'gte', val: ''}},
        {name: 'stock_move_release', op: 'has', val: {name: 'target_date', op: 'lte', val: ''}},
        {name: 'cost_price', op: 'is_null', val: null}
      ],
      materialConsumeItem: [
        {name: 'warehouse_code', op: 'eq', val: null},
        {name: 'performance_registration', op: 'has', val: {name: 'target_date', op: 'gte', val: ''}},
        {name: 'performance_registration', op: 'has', val: {name: 'target_date', op: 'lte', val: ''}},
        {name: 'cost_price', op: 'is_null', val: null}
      ],
      purchaseReceivingReturnItem: [
        {name: 'warehouse_code', op: 'eq', val: null},
        {name: 'receiving_return', op: 'has', val: {name: 'return_date', op: 'gte', val: ''}},
        {name: 'receiving_return', op: 'has', val: {name: 'return_date', op: 'lte', val: ''}},
        {name: 'cost_price', op: 'is_null', val: null}
      ],
      exportCommInvoiceItem: [
        {name: 'warehouse_code', op: 'eq', val: null},
        {name: 'export_comm_invoice', op: 'has', val: {name: 'invoice_date', op: 'gte', val: ''}},
        {name: 'export_comm_invoice', op: 'has', val: {name: 'invoice_date', op: 'lte', val: ''}},
        {name: 'cost_price', op: 'is_null', val: null}
      ]
    };
    vars.dataSource = reactive({
      purchaseReceivingItem: getPurchaseReceivingItem(vars.filter.purchaseReceivingItem),
      stockEtcItem: getStockEtcItem(vars.filter.stockEtcItem),
      stockMoveReleaseItem: getStockMoveReleaseItem(vars.filter.stockMoveReleaseItem),
      performanceRegistrationItem: getPerformanceItem1(vars.filter.performanceRegistrationItem),
      shipmentReleaseReturnItem: getShipmentReleaseReturnItem(vars.filter.shipmentReleaseReturnItem),
      importClearanceItem: getImportClearanceItem(vars.filter.importClearanceItem),
      shipmentReleaseItem: getShipmentReleaseItem(vars.filter.shipmentReleaseItem),
      stockEtcReleaseItem: getStockEtcItem(vars.filter.stockEtcReleaseItem),
      stockMoveReleaseReleaseItem: getStockMoveReleaseItem(vars.filter.stockMoveReleaseReleaseItem),
      materialConsumeItem: getPerformanceItem2(vars.filter.materialConsumeItem),
      purchaseReceivingReturnItem: getPurchaseReceivingReturnItem(vars.filter.purchaseReceivingReturnItem),
      exportCommInvoiceItem: getCommInvoiceItem(vars.filter.exportCommInvoiceItem),
      warehouse: [],
      baseItem: [],
    });

    onMounted(async () => {
      const { data } = await getBaseWarehouse([
        { name: 'use_cost_closing', op: 'eq', val: 1 }
      ]).load({ 
        sort: [{ selector: 'wh_order', desc: false }] 
      });
      if (data.length > 0) {
        vars.dataSource.warehouse = [...data];
        vars.formData.warehouseCode = data[0].wh_code;
      }

      methods.loadBaseItem();
    });

    const methods = {
      onGridInitialized(evt, key) {
        methods.insertGrid(key, evt.component);
        methods.bindStateStore(key, evt.component);
      },
      async applyCost() {
        if (!vars.formData.closingComplete) {
          await alert('원가마감 산정 및 적용이 완료되지 않았습니다.', '원가 마감');
          return;
        }

        const result = await confirm('마감 원가를 매입가로 적용하시겠습니까?', '원가 마감');
        if (result) {
          methods.showLoading();

          const apiApplyCost = new ApiService('/api/mes/v2/apply_cost');
          const params = { 
            history_id: vars.formData.historyId,
            start_date: methods.getSearchStartDate(), 
            end_date: methods.getSearchEndDate(),
            manager: authService.getUserName(),
            company_id: authService.getCompanyId(),
            warehouse_code: vars.formData.warehouseCode,
            item_code: vars.formData.itemCode,
          };
          try {
            await apiApplyCost.post('', params);
            await alert('마감 원가가 매입가로 적용되었습니다.', '원가 마감');
            methods.refreshCostClosingHistoryGrid();
          } catch (ex) {
            console.log(ex);
          } finally {
            methods.hideLoading();
          }
        }
      },
      async closeCost() {
        if (!vars.formData.searchComplete) {
          await alert('입고 단가 누락 조회가 완료되지 않았습니다.', '원가 마감');
          return;
        }

        const result = await confirm('원가가 마감되었습니다. 마감 원가를 적용하시겠습니까?', '원가 마감');
        if (result) {
          methods.showLoading();

          const apiCloseCost = new ApiService('/api/mes/v2/close_cost');
          const params = { 
            start_date: methods.getSearchStartDate(), 
            end_date: methods.getSearchEndDate(),
            manager: authService.getUserName(),
            company_id: authService.getCompanyId(),
            warehouse_code: vars.formData.warehouseCode,
            item_code: vars.formData.itemCode,
          };
          try {
            const res = await apiCloseCost.post('', params);
            methods.refreshCostClosingHistoryGrid();
            methods.setClosingComplete(true);
            vars.formData.historyId = res.data.id;
            
            console.log(res.data.minus_cost_items);

          } catch (ex) {
            methods.setClosingComplete(false);
            console.log(ex);
          } finally {
            methods.hideLoading();
          }
        }
      },
      async searchMissingCost() {
        if (!methods.isValidSearchDate()) {
          await alert('원가 마감 기간 선택이 잘못되었습니다', '입고 단가 누락 조회');
          return;
        }

        methods.setMissingCostItemDefaultFilter();

        const isMissingCostExist = await methods.isMissingCostExist();
        if (isMissingCostExist) {
          await alert('입고 단가 누락 건이 있습니다. 확인하세요.', '입고 단가 누락 조회');

          methods.showMissingCostItemPopup();
          methods.refreshMissingCostGrid();
          methods.setSearchComplete(false);
        } else {
          await alert('입고 단가 누락 조회가 완료되었습니다.', '입고 단가 누락 조회');
          methods.setSearchComplete(true);
        }
      },
      async searchMissingReleaseCost() {
        if (!methods.isValidSearchDate()) {
          await alert('원가 마감 기간 선택이 잘못되었습니다', '출고 원가 누락 조회');
          return;
        }

        methods.setMissingReleaseCostItemDefaultFilter();

        const isMissingCostExist = await methods.isMissingReleaseCostExist();
        if (isMissingCostExist) {
          await alert('출고 원가 누락 건이 있습니다. 확인하세요.', '출고 원가 누락 조회');

          methods.showMissingReleaseCostItemPopup();
          methods.refreshMissingReleaseCostGrid();
        } else {
          await alert('출고 원가 누락 품목이 없습니다.', '출고 원가 누락 조회');
        }
      },
      loadBaseItem() {
        vars.dataSource.baseItem = getBaseItem(null, null, null);
      },
      selectItem(data) {
        if (data.selectedRowsData.length > 0) {
          const item = data.selectedRowsData[0];
          vars.formData.itemCode = item.item_code;
        }
        vars.dlg.findItem.show = false;
      },
      insertGrid(key, component) {
        vars.grid[key] = component;
      },
      bindStateStore(key, component) {
        stateStore.bind(`cost-closing-${key}`, component);
      },
      setSearchComplete(isSearchComplete) {
        vars.formData.searchComplete = isSearchComplete;
      },
      setClosingComplete(isClosed) {
        vars.formData.closingComplete = isClosed;
      },
      showMissingCostItemPopup() {
        vars.dlg.missingCostItem.show = true;
      },
      showMissingReleaseCostItemPopup() {
        vars.dlg.missingReleaseCostItem.show = true;
      },
      showLoading() {
        vars.loading.value = true;
      },
      hideLoading() {
        vars.loading.value = false;
      },
      async isMissingCostExist() {
        if (await methods.isPurchaseReceivingItemExist()) { return true; }
        if (await methods.isStockEtcItemExist()) { return true; }
        if (await methods.isStockMoveReleaseItemExist()) { return true; }
        if (await methods.isPerformanceRegistrationItemExist()) { return true; }
        if (await methods.isShipmentReleaseReturnItemExist()) { return true; }
        if (await methods.isImportClearanceItemExist()) { return true; }
        return false;
      },
      async isPurchaseReceivingItemExist() {
        return (await methods.getPurchaseReceivingItemCount() > 0);
      },
      async isStockEtcItemExist() {
        return (await methods.getStockEtcItemCount() > 0);
      },
      async isStockMoveReleaseItemExist() {
        return (await methods.getStockMoveReleaseCount() > 0);
      },
      async isPerformanceRegistrationItemExist() {
        return (await methods.getPerformanceRegistrationItemCount() > 0);
      },
      async isShipmentReleaseReturnItemExist() {
        return (await methods.getShipmentReleaseReturnItemCount() > 0);
      },
      async isImportClearanceItemExist() {
        return (await methods.getImportClearanceItemCount() > 0);
      },
      async getStockEtcItemCount() {
        return await methods.getItemCount(vars.dataSource.stockEtcItem);
      },
      async getStockMoveReleaseCount() {
        return await methods.getItemCount(vars.dataSource.stockMoveReleaseItem);
      },
      async getPerformanceRegistrationItemCount() {
        return await methods.getItemCount(vars.dataSource.performanceRegistrationItem);
      },
      async getShipmentReleaseReturnItemCount() {
        return await methods.getItemCount(vars.dataSource.shipmentReleaseReturnItem);
      },
      async getImportClearanceItemCount() {
        return await methods.getItemCount(vars.dataSource.importClearanceItem);
      },
      async isMissingReleaseCostExist() {
        if (await methods.isShipmentReleaseItemExist()) { return true; }
        if (await methods.isStockEtcReleaseItemExist()) { return true; }
        if (await methods.isStockMoveReleaseReleaseItemExist()) { return true; }
        if (await methods.isMaterialConsumeItemExist()) { return true; }
        if (await methods.isPurchaseReceivingReturnItemExist()) { return true; }
        if (await methods.isExportCommInvoiceItemExist()) { return true; }
        return false;
      },
      async isShipmentReleaseItemExist() {
        return (await methods.getShipmentReleaseItemCount() > 0);
      },
      async isStockEtcReleaseItemExist() {
        return (await methods.getStockEtcReleaseItemCount() > 0);
      },
      async isStockMoveReleaseReleaseItemExist() {
        return (await methods.getStockMoveReleaseReleaseItemCount() > 0);
      },
      async isMaterialConsumeItemExist() {
        return (await methods.getMaterialConsumeItemCount() > 0);
      },
      async isPurchaseReceivingReturnItemExist() {
        return (await methods.getPurchaseReceivingReturnItemCount() > 0);
      },
      async isExportCommInvoiceItemExist() {
        return (await methods.getExportCommInvoiceItemCount() > 0);
      },
      async getPurchaseReceivingItemCount() {
        return await methods.getItemCount(vars.dataSource.purchaseReceivingItem);
      },
      async getShipmentReleaseItemCount() {
        return await methods.getItemCount(vars.dataSource.shipmentReleaseItem);
      },
      async getStockEtcReleaseItemCount() {
        return await methods.getItemCount(vars.dataSource.stockEtcReleaseItem);
      },
      async getStockMoveReleaseReleaseItemCount() {
        return await methods.getItemCount(vars.dataSource.stockMoveReleaseReleaseItem);
      },
      async getMaterialConsumeItemCount() {
        return await methods.getItemCount(vars.dataSource.materialConsumeItem);
      },
      async getPurchaseReceivingReturnItemCount() {
        return await methods.getItemCount(vars.dataSource.purchaseReceivingReturnItem);
      },
      async getExportCommInvoiceItemCount() {
        return await methods.getItemCount(vars.dataSource.exportCommInvoiceItem);
      },
      async getItemCount(dataSource) {
        const response = await dataSource.load({ take: 1, skip: 0, });
        return response.totalCount;
      },
      isValidSearchDate() {
        return (vars.formData.startDate <= vars.formData.endDate);
      },
      setMissingCostItemDefaultFilter() {
        methods.setPurchaseReceivingItemDefaultFilter();
        methods.setStockEtcItemDefaultFilter();
        methods.setStockMoveReleaseItemDefaultFilter();
        methods.setPerformanceRegistrationItemDefaultFilter();
        methods.setShipmentReleaseReturnItemDefaultFilter();
        methods.setImportClearanceItemDefaultFilter();
      },
      setPurchaseReceivingItemDefaultFilter() {
        methods.setDefaultFilter(vars.filter.purchaseReceivingItem, vars.dataSource.purchaseReceivingItem);
      },
      setStockEtcItemDefaultFilter() {
        methods.setDefaultFilter(vars.filter.stockEtcItem, vars.dataSource.stockEtcItem);
      },
      setStockMoveReleaseItemDefaultFilter() {
        methods.setDefaultFilter(vars.filter.stockMoveReleaseItem, vars.dataSource.stockMoveReleaseItem);
      },
      setPerformanceRegistrationItemDefaultFilter() {
        methods.setDefaultFilter(vars.filter.performanceRegistrationItem, vars.dataSource.performanceRegistrationItem);
      },
      setShipmentReleaseReturnItemDefaultFilter() {
        methods.setDefaultFilter(vars.filter.shipmentReleaseReturnItem, vars.dataSource.shipmentReleaseReturnItem);
      },
      setImportClearanceItemDefaultFilter() {
        methods.setDefaultFilter(vars.filter.importClearanceItem, vars.dataSource.importClearanceItem);
      },
      setMissingReleaseCostItemDefaultFilter() {
        methods.setShipmentReleaseItemDefaultFilter();
        methods.setStockEtcReleaseItemDefaultFilter();
        methods.setStockMoveReleaseReleaseItemDefaultFilter();
        methods.setMaterialConsumeItemDefaultFilter();
        methods.setPurchaseReceivingReturnItemDefaultFilter();
        methods.setExportCommInvoiceItemDefaultFilter();
      },
      setShipmentReleaseItemDefaultFilter() {
        methods.setDefaultFilter(vars.filter.shipmentReleaseItem, vars.dataSource.shipmentReleaseItem);
      },
      setStockEtcReleaseItemDefaultFilter() {
        methods.setDefaultFilter(vars.filter.stockEtcReleaseItem, vars.dataSource.stockEtcReleaseItem);
      },
      setStockMoveReleaseReleaseItemDefaultFilter() {
        methods.setDefaultFilter(vars.filter.stockMoveReleaseReleaseItem, vars.dataSource.stockMoveReleaseReleaseItem);
      },
      setMaterialConsumeItemDefaultFilter() {
        methods.setDefaultFilter(vars.filter.materialConsumeItem, vars.dataSource.materialConsumeItem);
      },
      setPurchaseReceivingReturnItemDefaultFilter() {
        methods.setDefaultFilter(vars.filter.purchaseReceivingReturnItem, vars.dataSource.purchaseReceivingReturnItem);
      },
      setExportCommInvoiceItemDefaultFilter() {
        methods.setDefaultFilter(vars.filter.exportCommInvoiceItem, vars.dataSource.exportCommInvoiceItem);
      },
      setDefaultFilter(filter, dataSource) {
        filter[0].val = vars.formData.warehouseCode;
        filter[1].val.val = methods.getSearchStartDateFake();
        filter[2].val.val = methods.getSearchEndDate();
        dataSource.defaultFilters = filter;
      },
      getSearchStartDateFake() {
        return moment('2000-01-01 00:00:00').startOf('day').format('YYYY-MM-DD 00:00:00');
      },
      getSearchStartDate() {
        return moment(vars.formData.startDate).startOf('day').format('YYYY-MM-DD 00:00:00');
      },
      getSearchEndDate() {
        return moment(vars.formData.endDate).endOf('day').format('YYYY-MM-DD 23:59:59');
      },
      refreshMissingCostGrid() {
        methods.refreshPurchaseReceivingItemGrid();
        methods.refreshStockEtcItemGrid();
        methods.refreshStockMoveReleaseItemGrid();
        methods.refreshPerformanceRegistrationItemGrid();
        methods.refreshShipmentReleaseReturnItemGrid();
        methods.refreshImportClearanceItemGrid();
      },
      refreshPurchaseReceivingItemGrid() {
        methods.refreshGrid(vars.grid.purchaseReceivingItem);
      },
      refreshStockEtcItemGrid() {
        methods.refreshGrid(vars.grid.stockEtcItem);
      },
      refreshStockMoveReleaseItemGrid() {
        methods.refreshGrid(vars.grid.stockMoveReleaseItem);
      },
      refreshPerformanceRegistrationItemGrid() {
        methods.refreshGrid(vars.grid.performanceRegistrationItem);
      },
      refreshShipmentReleaseReturnItemGrid() {
        methods.refreshGrid(vars.grid.shipmentReleaseReturnItem);
      },
      refreshImportClearanceItemGrid() {
        methods.refreshGrid(vars.grid.importClearanceItem);
      },
      refreshMissingReleaseCostGrid() {
        methods.refreshShipmentReleaseItemGrid();
        methods.refreshStockEtcReleaseItemGrid();
        methods.refreshStockMoveReleaseReleaseItemGrid();
        methods.refreshMaterialConsumeItemGrid();
        methods.refreshExportCommInvoiceItemGrid();
        methods.refreshCostClosingHistoryGrid();
      },
      refreshShipmentReleaseItemGrid() {
        methods.refreshGrid(vars.grid.shipmentReleaseItem);
      },
      refreshStockEtcReleaseItemGrid() {
        methods.refreshGrid(vars.grid.stockEtcReleaseItem);
      },
      refreshStockMoveReleaseReleaseItemGrid() {
        methods.refreshGrid(vars.grid.stockMoveReleaseReleaseItem);
      },
      refreshMaterialConsumeItemGrid() {
        methods.refreshGrid(vars.grid.materialConsumeItem);
      },
      refreshPurchaseReceivingReturnItemGrid() {
        methods.refreshGrid(vars.grid.purchaseReceivingReturnItem);
      },
      refreshExportCommInvoiceItemGrid() {
        methods.refreshGrid(vars.grid.exportCommInvoiceItem);
      },
      refreshCostClosingHistoryGrid() {
        methods.refreshGrid(vars.grid.history);
      },
      refreshGrid(grid) {
        if (grid) { grid.refresh(); }
      },
    };

    return { 
      vars, 
      methods, 
      costClosing, 
    };
  },
};
</script>
