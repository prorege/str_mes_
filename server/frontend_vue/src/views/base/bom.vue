<template>
  <div>
    <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
    <div class="content-block">
      <div class="dx-card responsive-paddings">
        <div class="content-header">
          <dx-toolbar>
            <dx-item location="before">
              <div class="content-title">
                BOM 관리
                <button type="button" class="sidebar-btn" @click="methods.toggleSidebar()">
                  품목 리스트 {{vars.sidebar.value ? '숨기기' : '보기'}}
                </button>
              </div>
            </dx-item>
            <dx-item location="after">
              <dx-button text="저장" icon="xlsxfile" type="default" :visible="vars.printDoc.value" @click="methods.saveBomSheet" />
            </dx-item>
            <dx-item location="after">
              <dx-button text="출력" icon="print" type="default" :visible="vars.printDoc.value" @click="methods.printBomSheet" />
            </dx-item>
            <dx-item location="after">
              <DxButtonGroup
                :items="[
                  { icon: 'import', text: '엑셀로 추가', value: 'upload' },
                  { icon: 'attach', text: '샘플', value: 'download' }
                ]"
                :visible="vars.printDoc.value"
                styling-mode="default"
                key-expr="value"
                @item-click="({itemData}) => methods.excelButtonClick(itemData.value)"
              />
            </dx-item>
          </dx-toolbar>
        </div>
        <div class="standard-code-container">
          <div class="standard-code-body">
            <div class="standard-code-item" v-show="vars.sidebar.value">
              <dx-data-grid
                height="calc(100vh - 150px)"
                :show-borders="true"
                :show-row-lines="true"
                :remote-operations="true"
                :column-auto-width="true"
                :focused-row-enabled="true"
                :data-source="baseItem"
                :on-initialized="evt => methods.onGridInitialized(evt, 'base-bom')"
              >
                <dx-editing
                  :use-icons="true"  
                  :allow-adding="false"
                  :allow-updating="false"
                  :allow-deleting="false"
                />
                <dx-filter-row :visible="true" />
                <dx-paging :page-size="20" />
                <dx-row-dragging
                  group="bom"  
                  :show-drag-icons="false"
                  :allow-reordering="false"
                  :allow-drop-inside-item="false"
                />

                <dx-column caption="ITEM ID" data-field="id" :visible="false" :allow-sorting="false" />
                <dx-column caption="생성일" data-field="created" :visible="false" />
                <dx-column caption="품목코드" data-field="item_code" :allow-sorting="false" />
                <dx-column caption="품명" data-field="item_name" :allow-sorting="false" />
                <dx-column caption="규격" data-field="item_standard" />
              </dx-data-grid>
            </div>
            <div class="bom-editor">
              <!-- 버튼 -->
              <div class=""></div>

              <!-- BOM 정보 -->
              <div class="">
                <dx-form
                  :form-data="vars.formData"
                  @field-data-changed="methods.onFieldDataChanged"
                  @initialized="evt => methods.onGridInitialized(evt, 'base-bom-form')"
                >
                  <dx-group-item :col-count="2">
                    <dx-simple-item
                      data-field="item.item_code"
                      :editor-options="{
                        buttons: [
                          {
                            name: 'search',
                            location: 'after',
                            options: {
                              stylingMode: 'text',
                              icon: 'search',
                              onClick: () => (vars.dlg.addItem.show = true),
                            },
                          },
                        ],
                      }"
                    >
                      <dx-label text="품목코드" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item
                      data-field="bom_depth"
                      editor-type="dxSelectBox"
                      :editor-options="{
                        dataSource: [
                          { value: 0, text: '사용안함' },
                          { value: 1, text: '사용함' },
                        ],
                        displayExpr: 'text',
                        valueExpr: 'value',
                        readOnly: !vars.formData.id,
                      }"
                    >
                      <dx-label text="자재 계산 시 반제품 사용여부" :show-colon="false" />
                    </dx-simple-item>
                  </dx-group-item>
                  <dx-group-item :col-count="3">
                    <dx-simple-item data-field="item.item_name" :editor-options="{ readOnly: true }">
                      <dx-label text="품명" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item data-field="item.item_standard" :editor-options="{ readOnly: true }">
                      <dx-label text="규격" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item data-field="item.asset_type" :editor-options="{ readOnly: true }">
                      <dx-label text="자산구분" :show-colon="false" />
                    </dx-simple-item>
                  </dx-group-item>
                </dx-form>
              </div>

              <!-- 품목 정보 -->
              <div class="bom-tree">
                <dx-tree-list
                  key-expr="treekey"
                  items-expr="children"
                  data-structure="tree"
                  height="calc(100vh - 500px)"
                  :show-borders="true"
                  :auto-expand-all="true"
                  :column-auto-width="true"
                  :focused-row-enabled="true"
                  :editing="{
                    mode: 'row',
                    useIcons: true,
                    allowUpdating: true,
                    allowDeleting: true,
                  }"
                  :columns="vars.bomTreeColumns"
                  :data-source="vars.bomTreeList"
                  :on-initialized="evt => methods.onGridInitialized(evt, 'base-bom-tree')"
                  @editing-start="methods.editingStart"
                  @row-updating="methods.rowUpdating"
                  @row-updated="methods.rowUpdated"
                  @row-removing="methods.rowRemoving"
                  @row-removed="methods.rowRemoved"
                  @cell-click="methods.onCellClick"
                  @cell-dbl-click="methods.itemPopupClick"
                  @focused-row-changed="methods.onFocusedRowChanged"
                >
                  <dx-row-dragging
                    group="bom"  
                    :show-drag-icons="false"
                    :allow-reordering="false"
                    :allow-drop-inside-item="true"
                    :on-add="methods.onAddItemToBom"
                  />
                </dx-tree-list>
              </div>

              <!-- 공정관리 -->
              <div class="bom-process-grid">
                <dx-data-grid
                  height="228px"
                  :show-borders="true"
                  :show-row-lines="true"
                  :column-auto-width="true"
                  :remote-operations="true"
                  :data-source="baseBomProcess"
                  :on-initialized="evt => methods.onGridInitialized(evt, 'base-bom-process')"
                >
                  <dx-grid-toolbar>
                    <dx-grid-item template="addButton" :visible="vars.common.selectedBomId !== 0" />
                    <dx-grid-item name="saveButton" :visible="vars.common.selectedBomId !== 0" />
                    <dx-grid-item name="revertButton" :visible="vars.common.selectedBomId !== 0" />
                  </dx-grid-toolbar>
                  <template #addButton>
                    <dx-button icon="add" @click="() => vars.process.visible = true" />
                  </template>
                  <dx-editing mode="batch"
                    :use-icons="true"
                    :allow-adding="true"
                    :allow-updating="true"
                    :allow-deleting="true"
                  />
                  <dx-paging :enabled="true" :page-size="1000" />

                  <dx-column caption="BOM ID" data-field="bom_id" :visible="false" />
                  <dx-column caption="공정코드" data-field="process.process_code" :allow-editing="false" />
                  <dx-column caption="공정명" data-field="process_id" :allow-editing="true" :set-cell-value="methods.setBomProcessItem">
                    <dx-lookup display-expr="process_name" value-expr="id" :data-source="vars.common.process" />
                  </dx-column>
                  <dx-column caption="C/T" data-field="ct" />
                  <dx-column caption="단위" data-field="process.unit" :allow-editing="false" />
                  <dx-column caption="단가" data-field="price" data-type="number" :format="{ type: 'fixedPoint', precision: 2 }" />
                  <dx-column caption="검사여부" data-field="check_yn" data-type="boolean" :allow-editing="true" />
                  <dx-column caption="외주발주여부" data-field="outsource_yn" data-type="boolean" :allow-editing="true" />
                  <dx-column caption="공정순서" data-field="order" data-type="number" :allow-editing="true" :sort-index="0" sort-order="asc" />
                </dx-data-grid>
              </div>

              <!-- 작업내역 -->
              <div class="bom-process-grid">
                <dx-data-grid
                  height="228px"
                  :show-borders="true"
                  :show-row-lines="true"
                  :remote-operations="true"
                  :column-auto-width="true"
                  :focused-row-enabled="true"
                  :editing="{
                    mode: 'row',
                    useIcons: true,
                    allowAdding: false,
                    allowUpdating: false,
                    allowDeleting: false,
                  }"
                  :data-source="baseBomHistory"
                  :on-initialized="evt => methods.onGridInitialized(evt, 'base-bom-history')"
                  @init-new-row="methods.newBomHistory"
                >
                  <dx-grid-toolbar>
                    <dx-grid-item name="addRowButton" :visible="vars.common.selectedBomId !== 0" />
                    <dx-grid-item name="saveButton" :visible="vars.common.selectedBomId !== 0" />
                    <dx-grid-item name="revertButton" :visible="vars.common.selectedBomId !== 0" />
                  </dx-grid-toolbar>
                  <dx-editing mode="batch"
                    :use-icons="true"
                    :allow-adding="true"
                    :allow-updating="true"
                    :allow-deleting="true"
                  />
                  <dx-column caption="입력일" data-field="created" data-type="date" :allow-editing="false" :sort-index="0" sort-order="desc" />
                  <dx-column caption="입력사원" data-field="manager" data-type="string" :allow-editing="true" />
                  <dx-column caption="사유(내용)" data-field="detail" data-type="string" :allow-editing="true" />
                  <dx-column caption="중요" data-field="important_yn" data-type="boolean" :allow-editing="true" />

                  <dx-paging :enabled="true" :page-size="4" />
                </dx-data-grid>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <dx-popup
      title="주공급업체 설정"  
      content-template="popup-content"
      v-model:visible="vars.dlg.supplier.show"
      :width="360"
      :height="460"
      :close-on-outside-click="true"
    >
      <template #popup-content>
        <dx-data-grid
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :hover-state-enabled="true"
          :data-source="vars.dlg.supplier.dataSource"
          @row-click="methods.selectMainSupplier"
          @initialized="evt => methods.onGridInitialized(evt, 'supplier')"
        >
          <dx-column caption="업체약칭" data-field="client.alias" />
          <dx-column caption="업체명" data-field="client.name" />

          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
        </dx-data-grid>
      </template>
    </dx-popup>

    <dx-popup
      title="품목선택"
      content-template="popup-content"
      v-model:visible="vars.dlg.addItem.show"
      :width="680"
      :height="460"
      :resize-enabled="true"
      :close-on-outside-click="true"
    >
      <template #popup-content>
        <dx-data-grid
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :hover-state-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :data-source="vars.dlg.addItem.dataSource"
          :on-initialized="evt => methods.onGridInitialized(evt, 'base_bom_item_in_popup')"
          @row-click="methods.selectBaseItem"
        >
          <dx-column caption="품목코드" data-field="item_code" />
          <dx-column caption="품명" data-field="item_name" />
          <dx-column caption="규격" data-field="item_standard" />
          <dx-column caption="자산구분" data-field="asset_type" />

          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
        </dx-data-grid>
      </template>
    </dx-popup>

    <popup-item-detail v-model:visible="vars.itemDetail.visible" :item-id="vars.itemDetail.id" />
    <popup-process v-model:visible="vars.process.visible" @selected="methods.addSelectedProcess" />

    <input hidden
      type="file"
      ref="excelRef"
      accept=".xlsx,.xls"
      @change="methods.excelFileChange"
    />
  </div>
</template>

<script>
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import {
  DxForm,
  DxLabel,
  DxGroupItem,
  DxSimpleItem,
} from 'devextreme-vue/form';
import DxButton from 'devextreme-vue/button'
import DxButtonGroup, { DxButtonGroupItem } from 'devextreme-vue/button-group';
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import {
  DxDataGrid,
  DxColumn,
  DxEditing,
  DxPaging,
  DxFilterRow,
  DxRowDragging,
  DxLookup,
  DxToolbar as DxGridToolbar,
  DxItem as DxGridItem,
} from 'devextreme-vue/data-grid';
import { DxTreeList } from 'devextreme-vue/tree-list';
import { DxPopup } from 'devextreme-vue/popup';
import notify from 'devextreme/ui/notify';
import authService from '@/auth';
import ApiService from '@/utils/api-service';
import { notifyError } from '@/utils/notify';
import {
  baseItem,
  baseBom,
  baseBomLink,
  baseBomProcess,
  baseProcess,
  baseBomHistory,
  baseClientItem,
  getBaseBomProcess,
} from '@/data-source/base';
import { ref, reactive } from '@vue/reactivity';
import numeral from 'numeral';
import moment from 'moment';
import printDocument from '@/utils/print-document';
import PopupItemDetail from '@/components/base/popup-item-detail';
import PopupProcess from '@/components/base/popup-process.vue';
import { setupProduceCost } from '@/data-source/setup'
import ExcelJS from 'exceljs';
import { saveAs } from 'file-saver';
import Decimal from 'decimal.js';

export default {
  components: {
    DxToolbar,
    DxItem,
    DxButton,
    DxButtonGroup,
    DxButtonGroupItem,
    DxTreeList,
    DxPopup,
    DxForm,
    DxLabel,
    DxGroupItem,
    DxSimpleItem,
    DxDataGrid,
    DxColumn,
    DxEditing,
    DxPaging,
    DxFilterRow,
    DxRowDragging,
    DxLookup,
    DxGridToolbar,
    DxGridItem,
    DxLoadPanel,
    PopupItemDetail,
    PopupProcess,
  },
  setup() {
    const vars = {},
      methods = {};
    baseItem.defaultFilters = [
      { name: 'fk_company_id', op: 'eq', val: authService.getCompanyId() },
    ];
    baseBom.defaultFilters = [
      { name: 'fk_company_id', op: 'eq', val: authService.getCompanyId() },
    ];

    // Vars
    vars.dataGridInstance = {};
    vars.loading = ref(false);
    vars.sidebar = ref(false)
    vars.printDoc = ref(false)

    vars.dlg = {};
    vars.dlg.addItem = reactive({ show: false, dataSource: baseItem.clone() });
    vars.dlg.supplier = reactive({ show: false, dataSource: baseClientItem.clone() });
    vars.formData = reactive({
      id: null,
    });
    vars.itemDetail = reactive({ visible: false, id: 0 });
    vars.process = reactive({ visible: false });
    vars.bomTreeList = reactive([]);
    vars.common = reactive({ process: [], selectedBomId: 0 });
    vars.bomTreeColumns = [
      { caption: 'BOM ID', dataField: 'id', visible: false, allowEditing: false },
      { caption: '순번', dataField: 'indexNumber', allowEditing: false },
      { caption: '품목코드', dataField: 'item.item_code', allowEditing: false },
      { caption: '품명', dataField: 'item.item_name', allowEditing: false },
      { caption: '규격', dataField: 'item.item_standard', allowEditing: false },
      { caption: '주공급업체', dataField: 'client_company', allowEditing: false },
      { caption: 'L/Rate', dataField: 'lrate', dataType: 'number' },
      { caption: '소요량', dataField: 'requirement', dataType: 'number' },
      { caption: '총소요량', dataType: 'number', allowEditing: false,
        calculateCellValue: row => {
          if (!('lrate' in row)) return '';
          if (row.lrate == 0) {
            return row.requirement;
          } else {
            return row.requirement + row.requirement * (row.lrate / 100.0);
          }
        },
      },
      { caption: '단가', dataField: 'item.purchase_price', dataType: 'number', format: {type: 'currency', precision: 2}, allowEditing: false },
      { caption: '금액', dataType: 'number', format: "₩,##0.00", allowEditing: false,
        calculateCellValue: row => {
          if (!row.item) return 0;
          if (!('requirement' in row)) return row.item.purchase_price;
          if (row.lrate == 0) {
            return row.item.purchase_price * row.requirement;
          } else {
            return (
              row.item.purchase_price *
              (row.requirement + row.requirement * (row.lrate / 100.0))
            );
          }
        },
      },
    ];
    const excelRef = ref()

    baseProcess
      .load()
      .then(response => (vars.common.process = response.data))
      .catch(ex => console.error(ex.message));

    // vars.baseBomItem = baseBom.clone()
    // vars.baseBomItem.defaultFilters = [{name: 'parent_item_id', op: 'is_null'}]
    // vars.baseBomItem.load().then(result => { console.log(result) })

    // Methods
    methods.onGridInitialized = (evt, key) => {
      vars.dataGridInstance[key] = evt.component;
      if (key === 'base-bom-process') evt.component.filter(['bom_id', '=', vars.common.selectedBomId])
      else if (key === 'base-bom-history') evt.component.filter(['bom_id', '=', vars.common.selectedBomId])
    };

    methods.getChildBom = async (parent, parentKeys, prevTreekey) => {
      const result = await baseBomLink.load({
        filter: ['parent_id', '=', parent.id],
        skip: 0,
        take: 1000,
      });
      if (result.data.length) {
        parentKeys.push(parent.id);
        if (!prevTreekey) prevTreekey = String(parent.id);
        parent.children = result.data
          .filter(v => {
            if (prevTreekey.split('-').includes(String(v.child_id))) {
              notify(
                `포함될 수 없는 항목이 있습니다(${v.child_id})`,
                'warning'
              );
              return false;
            }
            return true;
          })
          .map((v, index) => ({
            indexNumber: (index + 1),
            id: v.child_id,
            treekey: `${prevTreekey}-${v.child_id}`,
            link_id: v.link_id,
            lrate: v.lrate,
            requirement: v.requirement,
            client_company: v.client_company
          }))

        for (let child of parent.children) {
          let { data } = await baseBom.byKey(child.id);
          data.item.purchase_price = parseFloat(data.item.purchase_price)
          Object.assign(child, data);
          console.debug(
            `tree - parent: ${parent.id}, child: ${child.id}, treekey: ${child.treekey}`
          );
          await methods.getChildBom(child, parentKeys, child.treekey);
        }
      }
    };

    methods.selectBomByItemId = async data => {
      let result = await baseBom.load({ filter: ['item_id', '=', data.id] });
      if (!result.data.length) {
        await baseBom.insert({
          item_id: data.id,
          bom_depth: 0,
          fk_company_id: authService.getCompanyId(),
        });
        result = await baseBom.load({ filter: ['item_id', '=', data.id] });
      }
      result.data.forEach(data => data.item.purchase_price = parseFloat(data.item.purchase_price))
      return result;
    };

    methods.selectBaseItem = async evt => {
      const data = evt.data;
      vars.dataGridInstance['base-bom-tree'].beginCustomLoading();
      vars.dataGridInstance['base-bom-tree'].beginUpdate();
      vars.dataGridInstance['base-bom-tree'].option('focusedRowIndex', -1);
      const result = await methods.selectBomByItemId(data);
      result.treekey = result.id;
      const parentKeys = [];
      result.data[0].treekey = result.data[0].id.toString();
      vars.bomTreeList = result.data;
      vars.bomTreeList[0].indexNumber = '1';

      const {data: supplier} = await baseClientItem.load({filter: [
        ['item_code', '=', vars.bomTreeList[0].item.item_code],
        ['main_supplier', '=', true]
      ]})
      if (supplier.length) {
        vars.bomTreeList[0].client_company = supplier[0].client.name
      }

      if (vars.bomTreeList.length) {
        vars.formData = vars.bomTreeList[0];
        if (!evt.key) {
          vars.dataGridInstance['base-bom-form'].beginUpdate();
          vars.dataGridInstance['base-bom-form'].updateData(vars.formData);
          vars.dataGridInstance['base-bom-form'].endUpdate();
        }
        await methods.getChildBom(vars.bomTreeList[0], parentKeys);
      }

      vars.dataGridInstance['base-bom-tree'].endUpdate();
      vars.dataGridInstance['base-bom-tree'].option(
        'dataSource',
        vars.bomTreeList
      );
      // await?
      for (let key of parentKeys)
        vars.dataGridInstance['base-bom-tree'].expandRow(key);
      vars.dlg.addItem.show = false;
      vars.dataGridInstance['base-bom-tree'].endCustomLoading();
      vars.printDoc.value = true
    };

    methods.onAddItemToBom = async ({
      dropInsideItem,
      itemData,
      toComponent,
      toIndex,
    }) => {
      if (toIndex === null) return console.warn('toIndex is null');

      if (toIndex === 0 && !vars.formData.id) {
        console.log('item set root');
        methods.selectBaseItem({ data: itemData });
        return;
      }

      let bom = await methods.selectBomByItemId(itemData);
      let bomId = bom.data[0].id;

      if (dropInsideItem) {
        let key = toComponent.getKeyByRowIndex(toIndex);
        if (!key)
          return console.warn(
            `key: ${typeof key}(${key}), toIndex: ${typeof toIndex}(${toIndex})`
          );

        const { data: toData, children: toChildren } = toComponent.getNodeByKey(
          key
        );
        if (key.split('-').includes(String(bomId))) {
          notify('상위에 있는 항목을 하위에 포함할 수 없습니다', 'warning');
          return;
        }

        if (toChildren.map(v => v.data.id).includes(bomId)) {
          notify('동일한 항목을 추가할 수 없습니다', 'warning');
          return;
        }

        console.log(
          `dropInsideItem: ${dropInsideItem}, key: ${key}, parent_id: ${toData.id}, bom: ${bomId}`
        );
        await baseBomLink.insert({
          parent_id: toData.id,
          child_id: bomId,
          root_id: vars.formData.id,
          lrate: 0,
          requirement: 1,
          client_company: itemData.client_company
        });
      } else {
        toIndex = toIndex === 0 ? toIndex : toIndex - 1;
        let key = toComponent.getKeyByRowIndex(toIndex);
        let toData = null,
          toChildren = null;
        if (key) {
          const node = toComponent.getNodeByKey(key);
          if (node.parent.data) {
            toData = node.parent.data;
            toChildren = node.parent.children;
          } else {
            toData = node.data;
            toChildren = node.children;
          }

          if (key.split('-').includes(String(bomId))) {
            notify('상위에 있는 항목을 하위에 포함할 수 없습니다', 'warning');
            return;
          }

          if (toChildren.map(v => v.data.id).includes(bomId)) {
            notify('동일한 항목을 추가할 수 없습니다', 'warning');
            return;
          }
        } else {
          notify('다시 한 번 품목을 드롭해 주세요', 'warning');
          return;
        }

        await baseBomLink.insert({
          parent_id: toData.id,
          child_id: bomId,
          root_id: vars.formData.id,
          lrate: 0,
          requirement: 1,
          client_company: itemData.client_company
        });
      }
      methods.selectBaseItem({ data: vars.formData.item });
    };

    methods.onFocusedRowChanged = async evt => {
      if (!evt.row) vars.common.selectedBomId = 0
      else {
        const row = evt.row;
        vars.common.selectedBomId = row.data.id
      }
      vars.dataGridInstance['base-bom-process'].filter(['bom_id', '=', vars.common.selectedBomId])
      vars.dataGridInstance['base-bom-process'].refresh()
      vars.dataGridInstance['base-bom-history'].filter(['bom_id', '=', vars.common.selectedBomId])
      vars.dataGridInstance['base-bom-history'].refresh()
    };

    methods.onCellClick = (evt) => {
      if (!evt.column) return
      if (evt.column.dataField === 'client_company') {
        vars.dlg.supplier.dataSource.defaultFilters = [{name: 'item_code', op: 'eq', val: evt.data.item.item_code}]
        vars.dlg.supplier.show = true
        if (vars.dataGridInstance['supplier']) vars.dataGridInstance['supplier'].refresh()
      }
    }

    methods.selectMainSupplier = async (evt) => {
      if (evt.data.main_supplier) {
        vars.dlg.supplier.show = false
        return
      }
      vars.dataGridInstance['supplier'].beginCustomLoading()
      const rows = evt.component.getVisibleRows()
      const supplier = rows.find(v => v.data.main_supplier)
      if (supplier) {
        await baseClientItem.update(supplier.id, { main_supplier: false })
      }
      await baseClientItem.update(evt.data.id, { main_supplier: true })
      vars.dataGridInstance['supplier'].endCustomLoading()
      vars.dlg.supplier.show = false
    }

    methods.editingStart = evt => {
      if (vars.formData.id === evt.data.id) {
        evt.cancel = true;
        notify('최상위 품목은 수정할 수 없습니다.', 'warning');
      }
    };

    methods.rowUpdating = async evt => {
      // TODO:
      // items-expr을 이용하는 tree-list에서 업데이트 시 store의 byKey에서 에러가 발생하는 문제가 있음
      // parent-id-expr을 이용하거나 custom arraystore를 만들어서 해결해야 될 것 같으나 추후 개선
      // 임시로 업데이트 상태를 취소하고 새로 불러오는 걸로 조치
      evt.cancel = true;
      evt.component.cancelEditData();

      console.log('rowUpdating');
      await baseBomLink.update(evt.oldData.link_id, evt.newData);
      methods.selectBaseItem({ data: vars.formData.item });
    };

    methods.rowUpdated = evt => {
      console.log('rowUpdated');
      console.log(evt);
    };

    methods.rowRemoving = evt => {
      if (vars.formData.id === evt.data.id) {
        evt.cancel = true;
        notify('최상위 품목은 삭제할 수 없습니다.', 'warning');
      } else {
        const isCanceled = new Promise((resolve, reject) => {
          baseBomLink
            .remove(evt.data.link_id)
            .then(() => {
              resolve(false);
            })
            .catch(err => {
              reject(err);
            });
        });
        evt.cancel = isCanceled;
      }
    };

    methods.rowRemoved = async ({ key }) => {
      console.log(`${key} removed`);
      methods.selectBaseItem({ data: vars.formData.item });
    };

    methods.newBomProcess = evt => {
      evt.data.bom_id = baseBomProcess.defaultFilters[0].val;
      evt.data.process_id = null;
      evt.data.process = {};
    };

    methods.setBomProcessItem = (newData, value) => {
      const process = vars.common.process.find(v => v.id === value);
      newData.process_id = process.id;
      newData.process = process;
    };

    methods.newBomHistory = evt => {
      evt.data.created = new Date()
      evt.data.manager = authService.user.user_name
      evt.data.bom_id = vars.common.selectedBomId;
      evt.data.important_yn = false
    };

    methods.onFieldDataChanged = async ({ dataField, value }) => {
      if (dataField !== 'bom_depth' || !vars.formData.id) return;
      vars.loading.value = true;
      await baseBom.update(vars.formData.id, { bom_depth: value });
      vars.loading.value = false;
    };

    methods.toggleSidebar = () => {
      vars.sidebar.value = !vars.sidebar.value
    };

    methods.saveBomSheet = async () => {
      const partList = vars.bomTreeList[0].children || []
      partList.forEach(p => {
        const price = Number(p.item.purchase_price) || 0
        p.purchase_price_total = price * p.requirement
        p.purchase_price_humanize = numeral(price).format('0,0.00')
        p.purchase_price_total_humanize = numeral(p.purchase_price_total).format('0,0.00')
      })

      const workbook = new ExcelJS.Workbook()
      workbook.creator = 'MEC'
      workbook.created = new Date()
      const sheet = workbook.addWorksheet('Part List')
      let index = 1
      const row = sheet.getRow(index++)
      row.getCell(1).value = '자재코드'
      row.getCell(2).value = '품명'
      row.getCell(3).value = '재질'
      row.getCell(4).value = '순소요량'
      row.getCell(5).value = '손실율'
      row.getCell(6).value = '소요량'
      row.getCell(7).value = '자재가(원)'
      row.getCell(8).value = '자재금액(원)'
      row.getCell(9).value = '주공급원'

      for (const part of partList) {
        const row = sheet.getRow(index++)
        row.getCell(1).value = part.item.item_code
        row.getCell(2).value = part.item.item_name
        row.getCell(3).value = part.item.item_standard
        row.getCell(4).value = part.requirement
        row.getCell(5).value = part.lrate
        row.getCell(6).value = part.requirement + part.requirement * (part.lrate / 100.0)
        row.getCell(7).value = part.purchase_price_humanize
        row.getCell(8).value = part.purchase_price_total_humanize
        row.getCell(9).value = part.client_company
      }

      const filename = `${vars.formData.item.item_code}(${moment().format('YYYYMMDDHHmmss')}).xlsx`
      const mimeType = { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' };
      const buffer = await workbook.xlsx.writeBuffer()
      const blob = new Blob([buffer], mimeType)
      saveAs(blob, decodeURIComponent(filename));
    }

    methods.printBomSheet = async () => {
      const productList = [{id: vars.formData.id, item: vars.formData.item}]
      const params = {}
      params.item = vars.formData.item
      params.partList = vars.bomTreeList[0].children || []
      params.processList = []

      params.partList.forEach(p => {
        const price = Number(p.item.purchase_price) || 0
        p.purchase_price_total = price * p.requirement
        p.purchase_price_humanize = numeral(price).format('0,0.00')
        p.purchase_price_total_humanize = numeral(p.purchase_price_total).format('0,0.00')

        if (p.children && p.children.length) {
          productList.push({id: p.id, item: p.item})
          p.children.forEach(c => {
            const price = Number(c.item.purchase_price) || 0
            c.purchase_price_total = price * c.requirement
            c.purchase_price_humanize = numeral(price).format('0,0.00')
            c.purchase_price_total_humanize = numeral(c.purchase_price_total).format('0,0.00')
          })
        }
      })
      
      const subfix = (/\/(C|HS|MO|O|V)$/.exec(vars.formData.item.item_code) || [''])[0]
      const {data: costInfo} = await setupProduceCost.load({filter: [
        ['year', '=', String(new Date().getFullYear())],
        ['subfix', '=', subfix],
        ['fk_company_id', '=', authService.getCompanyId()]
      ]})

      baseBomHistory.defaultFilters = [{ name: 'bom_id', op: 'eq', val: vars.formData.id }];
      const {data: historyList} = await baseBomHistory.load({ sort: [{selector: 'created', desc: true}] })
      params.historyList = historyList.map(item => {
        item.created = moment(item.created).format('YYYY-MM-DD')
        item.important_yn = item.important_yn ? '✓' : ''
        return item
      })

      const bomProcess = getBaseBomProcess({})
      for (const m of productList) {
        const {data: plist} = await bomProcess.load({filter: ['bom_id', '=', m.id]})
        plist.forEach((p) => {
          if (!p.ct) return

          const price = new Decimal(p.price);
          const ct = new Decimal(p.ct)

          let price_total = params.item.item_code === m.item.item_code
            ? price.times(ct)
            : m.item.asset_type === '제품' ? price.times(ct) : new Decimal(0);

          params.processList.push({
            title: `${p.process.process_name}/${m.item.item_code}`,
            price: p.price,
            ct: p.ct,
            price_total: Number(price_total),
            price_humanize: numeral(p.price).format('0,0.00'),
            price_total_humanize: numeral(price_total).format('0,0.00'),
          });
        });
      }

      params.costs = {};
      params.costs.partCost = params.partList.reduce(
        (t, i) => Number((new Decimal(t)).plus((new Decimal(i.item.purchase_price)).times(i.requirement))),
        0
      );
      params.costs.partCost = Number((new Decimal(params.costs.partCost)).times(100).floor().dividedBy(100));
      
      params.costs.laborCost = params.processList.reduce(
        (t, i) => Number((new Decimal(t)).plus(i.price_total).times(100).floor().dividedBy(100)),
        0
      );

      if (subfix === '/HS') {
        const laborCost = new Decimal(params.costs.laborCost);
        const costRate = new Decimal(costInfo[0].produce_cost_rate);

        params.costs.produceCost = Number(laborCost.times(costRate).dividedBy(100).times(100).floor().dividedBy(100));
      } else {
        const partCost = new Decimal(params.costs.partCost);
        const laborCost = new Decimal(params.costs.laborCost);
        const costRate = new Decimal(costInfo[0].produce_cost_rate);

        params.costs.produceCost = Number(partCost.plus(laborCost).times(costRate.dividedBy(100)).times(100).floor().dividedBy(100));
      }

      const partCost = new Decimal(params.costs.partCost);
      const laborCost = new Decimal(params.costs.laborCost);
      const produceCost = new Decimal(params.costs.produceCost);
      const operatingCostRate = new Decimal(costInfo[0].operating_cost_rate);

      params.costs.produceTotalCost = Number(partCost.plus(laborCost).plus(produceCost));

      const produceTotalCost = new Decimal(params.costs.produceTotalCost);
      params.costs.operatingCost = Number(produceTotalCost.times(operatingCostRate.dividedBy(100)));

      const operatingCost = new Decimal(params.costs.operatingCost);
      params.costs.salesPrice = Number(produceTotalCost.plus(operatingCost));
      params.costs.outSourceCost = 0;

      for (const key in params.costs) {
        params.costs[key] = numeral(params.costs[key]).format('0,0.00');
      }

      // 제조원가
      // console.info(`${params.costs.partCost} + $params.costs.laborCost} + ${params.costs.produceCost}`)
      // console.info(`${params.costs.produceTotalCost}`)

      await printDocument('bom', params);
    };

    methods.floor = (value, fixed) => {
      const fixedValue = 10 ** fixed;
      return Math.floor((value) * fixedValue) / fixedValue
    }

    methods.itemPopupClick = ({ column, data }) => {
      if (column.name === 'item.item_code') {
        vars.itemDetail.id = data.item.id;
        vars.itemDetail.visible = true;
      }
    };

    methods.excelFileChange = async ({ target }) => {
      if (!target.files.length) return;
      if (!vars.bomTreeList[0]) return;

      vars.dataGridInstance['base-bom-tree'].beginCustomLoading('엑셀 데이터를 읽고 있습니다');
      const api = new ApiService('/api/mes/v1/excel/base/bom');
      const fd = new FormData();
      fd.append('file', target.files[0]);
      fd.append('root_id', vars.bomTreeList[0].id);

      try {
        await api.post('', fd);
        const item = await baseItem.byKey(vars.formData.item_id)
        await methods.selectBaseItem(item)
      }
      catch (ex) {
        console.error(ex)
        vars.dataGridInstance['base-bom-tree'].endCustomLoading()
        notifyError(`데이터 추가에 실패했습니다`);
      }
      finally {
        target.value = ''
      }
    }

    methods.excelButtonClick = (type) => {
      if (type === 'upload') excelRef.value.click()
      else if (type === 'download') saveAs('/api/mes/v1/excel/base/bom', 'sample.xlsx');
    }

    methods.addSelectedProcess = async (rows) => {
      if (!vars.dataGridInstance['base-bom-process']) return
      const grid = vars.dataGridInstance['base-bom-process']
      const exists = grid.getVisibleRows().map(v => v.data.process_id)
      
      for (const row of rows) {
        if (exists.includes(row.id)) continue
        await grid.addRow()
        grid.cellValue(0, 'bom_id', vars.common.selectedBomId);
        grid.cellValue(0, 'process_id', row.id);
        grid.cellValue(0, 'process', row);
      }
    }

    return {
      vars,
      methods,
      baseItem,
      baseBom,
      baseBomProcess,
      baseBomHistory,
      excelRef
    };
  },
};
</script>

<style lang="scss" scoped>
.sidebar-btn {
  border: 0;
  background-color: transparent;
  color: #355cd1;
  text-decoration: underline;
}
.standard-code-container {
}
.standard-code-body {
  height: auto;
}
.standard-code-item {
  width: 350px;
  flex: 0 0 350px;
  &.hidden {
    display: none;
  }
}
.standard-code-child {
  margin-left: 10px;
}
.bom-editor {
  width: 400px;
  flex: 1 1 auto;
  padding-left: 24px;
  height: calc(100vh - 110px);
  overflow-y: auto;
}
.bom-tree {
  margin-top: 20px;
}
.bom-process-grid {
  margin-top: 20px;
}
</style>
