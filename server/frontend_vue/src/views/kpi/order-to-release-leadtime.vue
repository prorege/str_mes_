<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">수주 출하 리드타임</div>
            </dx-item>
          </dx-toolbar>
        </div>
        <div>
          <div class="search-status">
            <span class="search-title">수주일자</span>
            <dx-date-box v-model:value="vars.formData.startDate" />
            <span class="search-bar">~</span>
            <dx-date-box v-model:value="vars.formData.endDate" />
            <span class="search-tab"></span>
            <dx-button text="검색" icon="search" @click="methods.loadItem()" />
          </div>
        </div>
      </div>
      <div class="dx-card responsive-paddings mt-1">
        <dx-data-grid
          height="calc(100vh - 230px)"
          date-serialization-format="yyyy-MM-ddTHH:mm:ss"
          :on-initialized="evt => methods.onGridInitialized(evt, 'status')"
          :data-source="vars.dataSource.item"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="false"
          :allow-column-reordering="true"
          :allow-column-resizing="true"
          @exporting="methods.onExporting"
        >
          <dx-column caption="수주번호" data-field="order_number" />
          <dx-column caption="수주일자" data-field="order_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="고객업체" data-field="client_company" />
          <dx-column caption="출고번호" data-field="release_number" />
          <dx-column caption="출고일자" data-field="release_date" data-type="date" format="yyyy-MM-dd" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item_name" />
          <dx-column caption="규격" data-field="item_standard" />
          <dx-column caption="리드타임" data-field="leadtime" data-type="number" format="fixedPoint"/>

          <!-- dx-export :enabled="true" / -->
          <dx-paging :page-size="20" />
          <dx-sorting mode="single" />
          <dx-filter-row :visible="true" />
        </dx-data-grid>

        <div class="mt-2">
          <table class="summary-table">
            <tr>
              <th>평균 리드타임</th>
              <td>{{ vars.summary.average }}</td>
            </tr>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment';

import { useRouter } from 'vue-router';
import { reactive, onMounted } from 'vue';

import DxButton from 'devextreme-vue/button';
import DxCheckBox from 'devextreme-vue/check-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow } from 'devextreme-vue/data-grid';

import stateStore from '@/utils/state-store';
import ApiService from '../../utils/api-service';
import { shipmentQuoteItem } from '../../data-source/shipment';

export default {
  components: {
    DxButton,
    DxCheckBox,
    DxDateBox,
    DxToolbar, DxItem,
    DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow,
  },
  setup() {
    const router = useRouter();
    const api = new ApiService('/api/mes/v1/shipment/leadtime');
    const vars = {};
    vars.grid = {};
    vars.formData = reactive({
      startDate: new Date(),
      endDate: new Date(),
    });
    vars.formData.startDate.setDate(vars.formData.startDate.getDate() - 7);
    vars.dataSource = reactive({ item: [] })
    vars.summary = reactive({ average: 0 })

    onMounted(async () => {
      await methods.loadItem();
    });

    const methods = {
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`shipment-leadtime-${key}`, evt.component);
      },
      onExporting (evt) {
        shipmentQuoteItem.exportData(evt.component, '견적현황', `견적현황_${Date.now()}.xlsx`)
        evt.cancel = true
      },
      async loadItem() {
        const params = {
          'start_date': moment(vars.formData.startDate).startOf('day').format('YYYY-MM-DD 00:00:00'),
          'end_date': moment(vars.formData.endDate).endOf('day').format('YYYY-MM-DD 23:59:59'),
        }
        const { data } = await api.post('', params);
        vars.dataSource.item = [...data.data];
        if ( vars.grid.status) {
          vars.grid.status.refresh();
        }
        vars.summary.average = data.average;
      },
    };

    return { vars, methods, shipmentQuoteItem };
  },
};
</script>
