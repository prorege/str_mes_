<template>
  <div class="content-block">
    <div class="dx-card responsive-paddings back-colored">
      <div class="content-header">
        <dx-toolbar class="back-colored">
          <dx-item location="before">
            <div class="content-title">안전재고 현황</div>
          </dx-item>
          <dx-item
            location="after"
            widget="dxButton"
            :options="{
              text: '전체화면',
              type: 'normal',
              onClick: methods.setFullscreen,
            }"
          />
        </dx-toolbar>
      </div>

      <div>
        <div class="search-status">
          <span class="search-bar">창고선택</span>
          <dx-lookup
            v-model:value="vars.filter.warehouse"
            :data-source="vars.dataSource.warehouse"
            value-expr="wh_code"
            display-expr="wh_name"
          />

          <span class="search-bar">자산구분</span>
          <dx-lookup
            v-model:value="vars.filter.assetType"
            :data-source="vars.dataSource.assetType"
            value-expr="code_name"
            display-expr="code_name"
          />
          <span class="search-tab"></span>
          <dx-button
            text="검색"
            icon="search"
            @click="methods.searchStock()"
          />
        </div>
      </div>

      <div :key="refreshKey" ref="viewer" class="fullscreen-content">
        <dx-data-grid
          width="100%"
          height="100%"
          column-resizing-mode="widget"
          :on-initialized="evt => methods.onInitialized(evt, 'status')"
          :data-source="vars.dataSource.stock"
          :show-borders="true"
          :row-alternation-enabled="true"
          :allow-column-reordering="true"
          :allow-column-resizing="true"
          :column-auto-width="true"
          :remote-operations="true"
        >
          <dx-grid-toolbar>
            <dx-item location="center" template="title" />
            <dx-item location="after" template="date" />
          </dx-grid-toolbar>

          <template #title>
            <div class="status-title">
              안전재고 현황 모니터링
            </div>
          </template>

          <template #date>
            <div>일 시 : {{ vars.currentDate }} {{ vars.currentTime.value }}</div>
          </template>

          <dx-column
            data-field="item_code"
            caption="품목코드"
            css-class="column-dark"
          />
          <dx-column
            data-field="item.item_name"
            caption="품명"
            css-class="column-dark"
          />
          <dx-column
            data-field="item.item_standard"
            caption="규격"
            css-class="column-dark"
          />
          <dx-column
            data-field="current_stock"
            caption="현재고"
            data-type="number"
            format="fixedPoint"
            css-class="column-green"
          />
          <dx-column
            data-field="assign_stock"
            caption="할당재고"
            data-type="number"
            format="fixedPoint"
            css-class="column-green"
            :calculate-display-value="methods.assignStock"
          />
          <dx-column
            data-field="available_stock"
            caption="가용재고"
            data-type="number"
            format="fixedPoint"
            css-class="column-green"
          />
          <dx-column
            data-field="item.safety_stock"
            caption="안전재고"
            data-type="number"
            format="fixedPoint"
            css-class="column-green"
          />
          <dx-column
            data-field="diff"
            caption="가용재고 - 안전재고"
            data-type="number"
            format="fixedPoint"
            css-class="column-green"
            sort-order="desc"
          />
          <dx-paging :page-size="vars.setting.page" />
        </dx-data-grid>
      </div>
    </div>
  </div>
</template>

<script>
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import {
  DxDataGrid,
  DxColumn,
  DxSelection,
  DxEditing,
  DxPaging,
  DxFilterRow,
  DxScrolling,
  DxColumnChooser,
  DxToolbar as DxGridToolbar,
  DxItem as DxGridItem,
  DxRequiredRule as DxGridRequiredRule,
} from 'devextreme-vue/data-grid';
import DxLookup from 'devextreme-vue/select-box';
import DxButton from 'devextreme-vue/button';
import { baseWarehouse } from '@/data-source/base';
import moment from 'moment';
import { onMounted, ref, reactive, onBeforeUnmount } from 'vue';
import ApiService from '../../utils/api-service';
import { notifyError } from '../../utils/notify';
import authService from '../../auth';
import { baseCodeLoader } from '../../data-source/base';

export default {
  components: {
    DxLoadPanel,
    DxToolbar,
    DxItem,
    DxDataGrid,
    DxColumn,
    DxSelection,
    DxEditing,
    DxPaging,
    DxFilterRow,
    DxScrolling,
    DxColumnChooser,
    DxLookup,
    DxGridToolbar,
    DxGridItem,
    DxGridRequiredRule,
    DxButton,
  },
  setup() {
    const api = new ApiService('/api/mes/v1/setup/store-status');
    const vars = { dlg: {} };
    const viewer = ref(null);
    const refreshKey = ref(Date.now());
    vars.grid = { status: null };
    vars.dataSource = reactive({
      stock: [],
      warehouse: [],
      assetType: [],
    });
    vars.filter = reactive({
      stock: [],
      assetType: '',
      warehouse: '',
    })

    vars.warehouse = reactive({
      name: '',
      code: '',
      index: 0,
    });
    vars.setting = reactive({
      page: 10,
    });

    vars.currentDate = moment().format('YYYY-MM-DD');
    vars.currentTime = ref(moment().format('HH:mm'));

    vars.timer = {
      zoom: null,
      page: null,
    }
    vars.timer.page = setInterval(() => {
      if (vars.grid.status) {
        const pageCount = vars.grid.status.pageCount();
        let pageIndex = vars.grid.status.pageIndex();
        if (pageIndex >= pageCount - 1) {
          pageIndex = -1;
        }
        vars.grid.status.pageIndex(pageIndex + 1);
      }
    }, 5 * 1000);

    document.onfullscreenchange = () => {
      if (!document.fullscreenElement) {
        if (vars.timer.zoom) clearTimeout(vars.timer.zoom);
        vars.timer.zoom = setTimeout(() => {
          refreshKey.value = Date.now();
          vars.timer.zoom = null;
        }, 1000);
      }
    };

    onMounted(async () => {
      await methods.loadBaseCode();
      await methods.loadWarehouse();
      vars.dataSource.warehouse.unshift({ wh_name: '전체', wh_code: '전체' });
      vars.filter.warehouse = vars.dataSource.warehouse[0].wh_code;
      vars.filter.assetType = vars.dataSource.assetType[0].code_name;

      await methods.searchStock();
    });

    onBeforeUnmount(() => {
      if (vars.timer.zoom) clearTimeout(vars.timer.zoom);
      document.onfullscreenchange = null;
      clearInterval(vars.timer.page);
    });

    const methods = {
      onInitialized(evt, key) {
        vars.grid[key] = evt.component;
      },
      setFullscreen() {
        if (!viewer.value) return;
        viewer.value.requestFullscreen();
      },
      assignStock(rowData) {
        return rowData.current_stock - rowData.available_stock;
      },
      async loadWarehouse() {
        const { data } = await baseWarehouse.load({skip: 0, take: 1000});
        vars.dataSource.warehouse = [...data];
        vars.warehouse.name = vars.dataSource.warehouse[vars.warehouse.index].wh_name;
        vars.warehouse.code = vars.dataSource.warehouse[vars.warehouse.index].wh_code;
      },
      
      loadBaseCode() {
        return baseCodeLoader(['자산구분'], authService.getCompanyId()).then(
          response => {
            vars.dataSource.assetType = response['자산구분'];
            vars.dataSource.assetType.unshift({ code_name: '전체' });
          }
        );
      },
      async searchStock() {
        const params = {
          warehouse: vars.filter.warehouse,
          asset_type: vars.filter.assetType,
        };
        console.log(params);
        const { data } = await api.post('', params);
        vars.dataSource.stock = [...data.data];
        vars.grid.status.refresh();
      },
    };

    return { 
      vars, 
      viewer,
      refreshKey,
      methods
    };
  },
};
</script>

<style lang="scss" scoped>
.dx-card {
  width: 100%;
}
.fullscreen-content {
  position: relative;
  width: 100%;
  height: calc(100vh - 160px);
  margin-top: 10px;
  padding: 12px;
  border: 1px solid #d7d7d7;
  border-radius: 4px;

  box-sizing: border-box;
  background-color: white;
}
</style>
