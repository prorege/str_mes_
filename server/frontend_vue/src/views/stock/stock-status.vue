<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">재고조회</div>
            </dx-item>
          </dx-toolbar>
        </div>
        <div>
          <div class="search-status">
            <!--span class="search-title">일자</span>
            <dx-date-box v-model:value="vars.dataSource.targetdate" /-->
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
            <span class="search-tab"></span>
            <dx-button text="검색" icon="search" @click="methods.searchStock()" />
            
            <dx-button
              text="Excel 저장"
              icon="xlsxfile"
              style="margin-left: auto;"
              :disabled="!vars.stock.item.length"
              @click="methods.excelExport()"
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
          <dx-column caption="현재고" data-field="current_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="할당재고" data-field="assign_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="가용재고" data-field="available_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="안전재고" data-field="item.safety_stock" data-type="number" format="fixedPoint" />
          <dx-column caption="품목대분류" data-field="item.main_category">
            <dx-grid-lookup value-expr="code_name" display-expr="code_name" :data-source="vars.dataSource.category" />
          </dx-column>
          <dx-column caption="품목중분류" data-field="item.middle_category" />
          <dx-column caption="품목소분류" data-field="item.sub_category" />

          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
        </dx-tree-list>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment';

import { useRouter } from 'vue-router';
import { reactive, onMounted } from 'vue';

import DxButton from 'devextreme-vue/button';
import DxLookup from 'devextreme-vue/select-box';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxTreeList, DxColumn, DxPaging, DxFilterRow, DxColumnChooser, DxLookup as DxGridLookup } from 'devextreme-vue/tree-list';

import { baseCodeLoader } from '../../data-source/base';

import saveAs from 'file-saver'
import { Workbook } from 'exceljs'
import authService from '../../auth';
import stateStore from '@/utils/state-store';
import ApiService from '../../utils/api-service';
import { loadWarehouse } from '../../utils/data-loader';

export default {
  components: {
    DxButton,
    DxLookup,
    DxDateBox,
    DxToolbar, DxItem,
    DxTreeList, DxColumn, DxPaging, DxFilterRow, DxColumnChooser, DxGridLookup,
  },
  setup() {
    const api = new ApiService('/api/mes/v1/stock/search');
    const router = useRouter();
    const vars = {};
    let targetdate = new Date();
    targetdate.setDate(targetdate.getDate());
    vars.filter = reactive({
      assetType: '',
      warehouse: '',
    });
    vars.stock = reactive({
      grid: null,
      selectedCell: null,
      item: [],
      filter: [],
    });
    vars.dataSource = reactive({
      targetdate: targetdate,
      warehouse: [],
      assetType: [],
      category: []
    });
    vars.grid = {};

    onMounted(async () => {
      await methods.loadBaseCode();
      await loadWarehouse(vars.dataSource);
      vars.dataSource.warehouse.unshift({ wh_name: '전체', wh_code: '전체' });
      vars.filter.warehouse = vars.dataSource.warehouse[0].wh_code;
      vars.filter.assetType = vars.dataSource.assetType[0].code_name;
    });

    const methods = {
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`stock-status-${key}`, evt.component);
        methods.initSorting();
      },
      initSorting() {
        const columns = vars.grid['stock-list'].getVisibleColumns();
        const col = columns.filter((item) => item.sortOrder);
        if (col.length == 0) {
          const defaultName = 'item_code';
          const defaultSort = columns.filter(
            (item) => item.name == defaultName
          );
          if (defaultSort.length > 0) {
            vars.grid['stock-list'].columnOption(
              defaultSort[0].index,
              'sortOrder',
              'asc'
            );
          }
        }
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

        //vars.stock.item = getSetupBasicStock(vars.stock.filter);
        const params = {
          warehouse: vars.filter.warehouse,
          asset_type: vars.filter.assetType,
        };
        const { data } = await api.post('', params);
        vars.stock.item = [...data.data];
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
          }
        );
      },
      async excelExport () {
        const today = new Date();
        const workbook = new Workbook();
        workbook.creator = 'Stock';
        workbook.created = today;
        workbook.lastPrinted = today;
        
        const worksheet = workbook.addWorksheet('Main sheet');
        const colnames = ['창고구분', '자산구분', '품목코드', '품명', '규격', '현재고', '할당재고', '가용재고', '안전재고', '품목대분류', '품목중분류', '품목소분류']
        const row = worksheet.getRow(1)

        for (let i=1; i<colnames.length; i++) {
          row.getCell(i).value = colnames[i - 1]
        }
        
        for (let i=0; i<vars.stock.item.length; i++) {
          const item = vars.stock.item[i]
          const row = worksheet.getRow(i + 2)
          row.getCell(1).value = item.warehouse
          row.getCell(2).value = item.item.asset_type
          row.getCell(3).value = item.item_code
          row.getCell(4).value = item.item.item_name
          row.getCell(5).value = item.item.item_standard
          row.getCell(6).value = item.current_stock
          row.getCell(7).value = item.assign_stock
          row.getCell(8).value = item.available_stock
          row.getCell(9).value = item.item.safety_stock
          row.getCell(10).value = item.item.main_category
          row.getCell(11).value = item.item.middle_category 
          row.getCell(12).value = item.item.sub_category
        }

        const blob = await workbook.xlsx.writeBuffer()
        saveAs(new Blob([blob], { type: 'application/octet-stream' }), `재고조회-${moment().format('YYYY-MM-DD HH:mm:ss')}.xlsx`);
      }
    };

    return { vars, methods };
  },
};
</script>
