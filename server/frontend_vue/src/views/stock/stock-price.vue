<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before"
              ><div class="content-title">재고금액</div></dx-item
            >
          </dx-toolbar>
        </div>
        <div>
          <div class="search-status">
            <span class="search-bar">창고선택</span>
            <dx-lookup
              value-expr="wh_code"
              display-expr="wh_name"  
              v-model:value="vars.filter.warehouse"
              :data-source="vars.dataSource.warehouse"
            />

            <span class="search-bar">자산구분</span>
            <dx-lookup
              value-expr="code_name"
              display-expr="code_name"  
              v-model:value="vars.filter.assetType"
              :data-source="vars.dataSource.assetType"
            />

            <span class="search-bar">품목대분류</span>
            <dx-lookup
              :search-enabled=true
              search-mode="contains"
              value-expr="code_name"
              display-expr="code_name"  
              v-model:value="vars.filter.category"
              :data-source="vars.dataSource.category"
            />

            <span class="search-tab"></span>
            <dx-button
              text="검색"
              icon="search"
              @click="methods.searchStock()"
            />
          </div>
        </div>
      </div>

      <div class="dx-card responsive-paddings mt-1">
        <dx-tree-list
          id="id"
          key-expr="id"
          parent-id-expr="parent_id"
          height="calc(100vh - 200px)"
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :focused-row-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :data-source="vars.stock.item"
          :on-initialized="evt => methods.onGridInitialized(evt, 'stock-list')"
        >
          <dx-column caption="창고구분" data-field="warehouse" :filter-operations="['contains', '=']" />
          <dx-column caption="자산구분" data-field="item.asset_type" :filter-operations="['contains', '=']" />
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="규격" data-field="item.item_standard" />
          <dx-column caption="현재고" data-field="current_stock" data-type="number" />
          <dx-column caption="단가" data-field="item.purchase_price" data-type="number" format="₩,##0" />
          <dx-column caption="금액" data-type="number" format="₩,##0" :calculate-cell-value="methods.calculateTotalPrice" />

          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
        </dx-tree-list>
      </div>

      <div class="mt-2">
          <table class="summary-table">
            <tr>
              <th>합계금액:</th>
              <td>{{ vars.summary.total_price.value }}</td>
            </tr>
          </table>
        </div>
    </div>
  </div>
</template>

<script>
import numeral from 'numeral';

import { useRouter } from 'vue-router';
import { reactive, onMounted, computed } from 'vue';

import DxButton from 'devextreme-vue/button';
import DxLookup from 'devextreme-vue/select-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxTreeList, DxColumn, DxPaging, DxFilterRow, DxColumnChooser } from 'devextreme-vue/tree-list';

import authService from '../../auth';
import ApiService from '../../utils/api-service';
import { baseCodeLoader } from '../../data-source/base';
import { loadWarehouse } from '../../utils/data-loader';

export default {
  components: {
    DxButton,
    DxLookup,
    DxDateBox,
    DxToolbar, DxItem,
    DxTreeList, DxColumn, DxPaging, DxFilterRow, DxColumnChooser,
  },
  setup() {
    const api = new ApiService('/api/mes/v1/stock/price');
    const router = useRouter();
    const vars = {};
    let targetdate = new Date();
    targetdate.setDate(targetdate.getDate());
    vars.filter = reactive({
      assetType: '',
      warehouse: '',
      category: '',
    });
    vars.stock = reactive({
      grid: null,
      selectedCell: null,
      totalPrice: 0,
      item: [],
      filter: [],
    });
    vars.dataSource = reactive({
      targetdate: targetdate,
      warehouse: [],
      assetType: [],
      category: [],
    });
    vars.grid = {};
    vars.summary = {};
    vars.summary.total_price = computed(() => '₩' + numeral(vars.stock.totalPrice).format('0,0'));

    onMounted(async () => {
      await methods.loadBaseCode();
      await loadWarehouse(vars.dataSource);
      vars.dataSource.warehouse.unshift({ wh_name: '전체', wh_code: '전체' });
      vars.filter.warehouse = vars.dataSource.warehouse[0].wh_code;
      vars.filter.assetType = vars.dataSource.assetType[0].code_name;
      vars.filter.category = vars.dataSource.category[0].code_name;
    });

    const methods = {
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
      },
      async searchStock() {
        vars.stock.filter = [];
        vars.stock.filter.push({
          name: 'fk_company_id',
          op: 'eq',
          val: authService._user.fk_company_id || 0,
        });

        if (
          vars.filter.warehouse &&
          vars.filter.warehouse != '전체' &&
          vars.filter.warehouse != ''
        ) {
          vars.stock.filter.push({
            name: 'wh_code',
            op: 'eq',
            val: vars.filter.warehouse,
          });
        }

        if (
          vars.filter.assetType &&
          vars.filter.assetType != '전체' &&
          vars.filter.assetType != ''
        ) {
          vars.stock.filter.push({
            name: 'item',
            op: 'has',
            val: {
              name: 'asset_type',
              op: 'eq',
              val: vars.filter.assetType,
            },
          });
        }
        if (
          vars.filter.category &&
          vars.filter.category != '전체' &&
          vars.filter.category != ''
        ) {
          vars.stock.filter.push({
            name: 'item',
            op: 'has',
            val: {
              name: 'main_category',
              op: 'eq',
              val: vars.filter.category,
            },
          });
        }

        //vars.stock.item = getSetupBasicStock(vars.stock.filter);
        const params = {
          warehouse: vars.filter.warehouse,
          asset_type: vars.filter.assetType,
          category: vars.filter.category,
        };
        const { data } = await api.post('', params);
        vars.stock.item = [...data.data];
        vars.stock.totalPrice = data.totalPrice;
      },
      loadBaseCode() {
        return baseCodeLoader(['자산구분', '품목분류'], authService.getCompanyId()).then(
          response => {
            vars.dataSource.assetType = response['자산구분'];
            vars.dataSource.assetType.unshift({ code_name: '전체' });

            vars.dataSource.category = response['품목분류'];
            vars.dataSource.category.sort(function(a, b) {
              const upperA = a.code_name.toUpperCase();
              const upperB = b.code_name.toUpperCase();

              if (upperA > upperB) return 1;
              if (upperA < upperB) return -1;
              if (upperA == upperB) return 0;
            });
            vars.dataSource.category.unshift({ code_name: '전체' });
          }
        );
      },
      calculateTotalPrice(rowData) {
        const totalPrice = rowData.current_stock * rowData.item.purchase_price;
        return totalPrice ? totalPrice : 0;
      }
    };

    return { vars, methods };
  },
};
</script>
