<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings">
        <div class="content-header">
          <dx-toolbar>
            <dx-item location="before">
              <div class="content-title">검사기준등록</div>
            </dx-item>
          </dx-toolbar>
        </div>
        <div class="standard-code-container">
          <div class="standard-code-body">
            <div class="standard-code-item">
              <dx-data-grid
                class="scrollable-grid"
                height="calc(100vh - 200px)"
                :data-source="baseItem"
                :column-auto-width="true"
                :show-borders="true"
                :show-row-lines="true"
                :focused-row-enabled="true"
                :remote-operations="true"
                :scrolling="{ mode: 'virtual', rowRenderingMode: 'virtual' }"
                :on-initialized="
                  evt => methods.onGridInitialized(evt, 'base-code-1dep')
                "
                @focused-row-changed="methods.onFocusedRowChanged(0, $event)"
              >
                <dx-editing
                  mode="cell"
                  :allow-adding="false"
                  :allow-updating="false"
                  :allow-deleting="false"
                  :use-icons="true"
                />
                <dx-paging :page-size="1000" />

                <dx-column
                  data-field="id"
                  caption="품목 ID"
                  :visible="false"
                  :allow-sorting="false"
                >
                </dx-column>
                <dx-column
                  data-field="created"
                  caption="생성일"
                  :visible="false"
                  :allow-sorting="false"
                >
                </dx-column>
                <dx-column
                  data-field="item_code"
                  caption="품목코드"
                  :allow-sorting="false"
                />
                <dx-column
                  data-field="item_name"
                  caption="품명"
                  :allow-sorting="false"
                  :visible="true"
                />
                <dx-column
                  data-field="item_standard"
                  caption="규격"
                  :visible="true"
                />
              </dx-data-grid>
            </div>

            <div
              class="standard-code-item standard-code-child"
              v-for="(col, idx) in vars.childGrid"
              :key="col.parent.id"
            >
              <dx-data-grid
                class="scrollable-grid"
                height="calc(100vh - 200px)"
                :data-source="col.dataSource"
                :column-auto-width="true"
                :show-borders="true"
                :show-row-lines="true"
                :focused-row-enabled="true"
                :on-initialized="
                  evt =>
                    methods.onGridInitialized(evt, `base-code-child-${idx}`)
                "
              >
                <dx-editing
                  mode="cell"
                  :allow-adding="true"
                  :allow-updating="true"
                  :allow-deleting="true"
                  :use-icons="true"
                />
                <dx-paging :enabled="true" :page-size="1000" />
                <dx-column
                  data-field="id"
                  caption="검사기준 ID"
                  :visible="false"
                  :allow-sorting="false"
                >
                </dx-column>
                <dx-column
                  data-field="created"
                  caption="생성일"
                  :visible="false"
                  :allow-sorting="false"
                >
                </dx-column>
                <dx-column
                  data-field="qa_type"
                  caption="검사구분"
                  :allow-sorting="false"
                >
                  <dx-lookup
                    :data-source="vars.dataSource.qa_types"
                    value-expr="code_name"
                    display-expr="code_name"
                  />
                </dx-column>
                <dx-column
                  data-field="qa_item"
                  caption="검사항목"
                  :allow-sorting="false"
                  :visible="true"
                >
                  <dx-lookup
                    :data-source="vars.dataSource.qa_items"
                    value-expr="code_name"
                    display-expr="code_name"
                  />
                </dx-column>
                <dx-column
                  data-field="qa_standard"
                  caption="검사규격"
                  :visible="true"
                />
                <dx-column
                  data-field="measurement_unit"
                  caption="측정단위"
                  :visible="true"
                >
                  <dx-lookup
                    :data-source="vars.dataSource.qa_units"
                    value-expr="code_name"
                    display-expr="code_name"
                  />
                </dx-column>
                <dx-column
                  data-field="tolerance_plus"
                  caption="공차(+)"
                  :visible="true"
                />
                <dx-column
                  data-field="tolerance_minus"
                  caption="공차(-)"
                  :visible="true"
                />
                <dx-column
                  data-field="qa_method"
                  caption="검사방법"
                  :visible="true"
                >
                  <dx-lookup
                    :data-source="vars.dataSource.qa_methods"
                    value-expr="code_name"
                    display-expr="code_name"
                  />
                </dx-column>
                <dx-column
                  data-field="input_type"
                  caption="입력구분"
                  :visible="true"
                >
                  <dx-lookup
                    :data-source="vars.dataSource.qa_inputs"
                    value-expr="code_name"
                    display-expr="code_name"
                  />
                </dx-column>
                <dx-column
                  data-field="qa_count"
                  caption="검사횟수"
                  :visible="true"
                />
                <!-- dx-column type="buttons" :width="110"
                  ><dx-button
                    hint="Image"
                    icon="image"
                    :visible="true"
                    @click="methods.onUploadImage"
                  /><dx-button name="delete" />
                </dx-column -->
              </dx-data-grid>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import {
  DxDataGrid,
  DxColumn,
  DxEditing,
  DxPaging,
  DxButton,
  DxLookup,
} from 'devextreme-vue/data-grid';
import { baseCode, baseItem } from '../../data-source/base';
import { qualityQAStandard } from '../../data-source/quality';
import { onMounted, ref, reactive, computed, watch, nextTick } from 'vue';
import { baseCodeLoader } from '../../data-source/base';

export default {
  components: {
    DxDataGrid,
    DxColumn,
    DxEditing,
    DxPaging,
    DxToolbar,
    DxItem,
    DxButton,
    DxLookup,
  },
  setup() {
    const vars = {}, methods = {};

    // Vars
    vars.dataGridInstance = {};
    vars.selected = reactive({ 0: null, 1: null, 2: null });
    vars.childGrid = reactive([]);
    vars.dataSource = reactive({
      qa_types: [],
      qa_items: [],
      qa_units: [],
      qa_methods: [],
      qa_inputs: [],
    })

    qualityQAStandard.defaultFilters = [
      { name: 'fk_base_item_id', op: 'is_null', val: null },
    ];

    vars.secondDepthBaseCode = qualityQAStandard.clone();
    vars.secondDepthBaseCode.defaultFilters = [
      { name: 'parent_code_id', op: 'eq', val: 0 },
    ];

    onMounted(async () => {
      await methods.loadBaseCode();
    });

    // Methods
    const onDragRow = async (depth, evt) => {
      if (evt.fromIndex === evt.toIndex) return;
      console.log(`onDragRow: ${depth}`);
      const dataSource = vars.childGrid[depth].dataSource;
      const visibleRows = evt.component.getVisibleRows();

      const moveRow = visibleRows.splice(evt.fromIndex, 1);
      visibleRows.splice(evt.toIndex, 0, moveRow[0]);

      let start = evt.fromIndex,
        end = evt.toIndex;
      if (evt.fromIndex > evt.toIndex) {
        start = evt.toIndex;
        end = evt.fromIndex;
      }

      for (let i = start; i <= end; i++) {
        let data = visibleRows[i].data;
        console.log(data.id);
        await dataSource.update(data.id, { code_order: i + 1 });
      }
      await evt.component.refresh();
    };

    methods.onGridInitialized = (evt, key) => {
      vars.dataGridInstance[key] = evt.component;
    };

    methods.onFocusedRowChanged = (depth, evt) => {
      console.log(`onFocusedRowChanged: ${depth}`);
      vars.childGrid.splice(depth, vars.childGrid.length);

      const dataSource = qualityQAStandard.clone();
      dataSource.defaultFilters = [
        { name: 'fk_base_item_id', op: 'eq', val: evt.row.data.id },
      ];
      dataSource.on('inserting', params => {
        params.fk_base_item_id = evt.row.data.id;
      });

      vars.childGrid.push({
        parent: evt.row.data,
        dataSource,
      });

      // vars.secondDepthBaseCode.defaultFilters = [{name: 'parent_code_id', op: 'eq', val: evt.row.data.id}]
      // vars.selected[0] = evt.row.data

      // if (vars.dataGridInstance['base-code-2dep']) {
      //   vars.dataGridInstance['base-code-2dep'].refresh()
      // }
    };

    methods.onDragRow = depth => {
      return evt => {
        evt.promise = onDragRow(depth, evt);
      };
    };

    methods.onUploadImage = () => {};

    methods.loadBaseCode = () => {
      return baseCodeLoader([
        '검사구분',
        '검사항목',
        '측정단위',
        '검사방법',
        '입력구분',
      ])
      .then(response => {
        vars.dataSource.qa_types = response['검사구분'];
        vars.dataSource.qa_items = response['검사항목'];
        vars.dataSource.qa_units = response['측정단위'];
        vars.dataSource.qa_methods = response['검사방법'];
        vars.dataSource.qa_inputs = response['입력구분'];
      })
      .then(() => (vars.init.value = true));
    };

    return {
      vars,
      methods,
      baseCode,
      baseItem,
    };
  },
};
</script>

<style lang="scss" scoped>
.standard-code-body {
  display: flex;
  flex-wrap: nowrap;
}
.standard-code-item {
  flex: 0 0 250px;
  &:not(.standard-code-child) {
    padding-top: 46px;
  }
}
.standard-code-child {
  margin-left: 10px;
}
.scrollable-grid {
  height: calc(100vh - 300px);
}
</style>
