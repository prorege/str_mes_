<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings">
        <div class="content-header">
          <dx-toolbar>
            <dx-item location="before">
              <div class="content-title">기준코드</div>
            </dx-item>
          </dx-toolbar>
        </div>
        <div class="standard-code-container">

          <div class="standard-code-body">
            <div class="standard-code-item">
              <dx-data-grid
                class="scrollable-grid"
                height="calc(100vh - 194px)"
                :show-borders="true"
                :show-row-lines="true"
                :remote-operations="true"
                :column-auto-width="true"
                :focused-row-enabled="true"
                :data-source="baseCode"
                :scrolling="{mode: 'virtual', rowRenderingMode: 'virtual'}"
                :on-initialized="(evt) => methods.onGridInitialized(evt, 'base-code-1dep')"
                @focused-row-changed="methods.onFocusedRowChanged(0, $event)"
              >
                <dx-column caption="코드 ID" data-field="id" :visible="false" :allow-sorting="false" />
                <dx-column caption="생성일" data-field="created" :visible="false" :allow-sorting="false" />
                <dx-column caption="코드분류" data-field="code_name" :visible="true" :allow-sorting="true" sort-order="asc" />
                <dx-column caption="설명" data-field="code_class_detail" :visible="true" :allow-sorting="false" />
                <dx-column caption="상위코드" data-field="parent_code_id" :visible="false" />
                <dx-column caption="순서" data-field="code_order" :visible="false" />
                <dx-column caption="깊이" data-field="code_depth" :visible="false" />

                <dx-sorting mode="single"/>
                <dx-paging :page-size="1000"/>
                <dx-editing mode="cell"
                  :use-icons="true"  
                  :allow-adding="false"
                  :allow-updating="false"
                  :allow-deleting="false"
                />
                <dx-filter-row :visible="true" />
              </dx-data-grid>
            </div>

            <div class="standard-code-item standard-code-child" v-for="(col, idx) in vars.childGrid" :key="col.parent.id">
              <dx-data-grid
                class="scrollable-grid"
                height="calc(100vh - 148px)"
                :show-borders="true"
                :show-row-lines="true"
                :remote-operations="true"
                :column-auto-width="true"
                :focused-row-enabled="true"
                :data-source="col.dataSource"
                :on-initialized="(evt) => methods.onGridInitialized(evt, `base-code-child-${idx}`)"
                @init-new-row="methods.initNewRow(idx, $event)"
                @focused-row-changed="methods.onFocusedRowChanged(idx + 1, $event)"
              >
                <dx-column caption="코드 ID" data-field="id" :visible="false" :allow-sorting="false" />
                <dx-column caption="생성일" data-field="created" :visible="false" :allow-sorting="false" />
                <dx-column caption="코드분류" data-field="code_name" :allow-sorting="false">
                  <dx-async-rule message="코드분류는 중복될 수 없습니다" :validation-callback="methods.validationUniqueCodeName" />
                </dx-column>
                <dx-column caption="설명" data-field="code_class_detail" :visible="true" :allow-sorting="false" />
                <dx-column caption="상위코드" data-field="parent_code_id" :visible="false" />
                <dx-column caption="순서" data-field="code_order" :visible="true" sort-order="asc" />
                <dx-column caption="깊이" data-field="code_depth" :visible="false" sort-order="asc" />
                
                <dx-paging :page-size="1000"/>
                <dx-editing mode="row"
                  :use-icons="true"  
                  :allow-adding="true"
                  :allow-updating="true"
                  :allow-deleting="true"
                />
                <dx-row-dragging
                  drop-feedback-mode="push"  
                  :allow-reordering="true"
                  :on-reorder="methods.onDragRow(idx + 1)"
                />
              </dx-data-grid>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar'
import { DxDataGrid, DxColumn, DxPaging, DxEditing, DxSorting, DxAsyncRule, DxFilterRow, DxRowDragging } from 'devextreme-vue/data-grid'
import { baseCode } from '../../data-source/base'
import { reactive } from '@vue/reactivity'

export default {
  components: {
    DxToolbar, DxItem,
    DxDataGrid, DxColumn, DxPaging, DxEditing, DxSorting, DxAsyncRule, DxFilterRow, DxRowDragging,
  },
  setup() {
    const vars = {}, methods = {}, validationStore = baseCode.clone()

    // Vars
    vars.dataGridInstance = {}
    vars.max_depth = 0
    vars.childGrid = reactive([])
    baseCode.defaultFilters = [{name: 'parent_code_id', op: 'is_null', val: null}]

    // Methods
    const onDragRow = async (depth, evt) => {
      if (evt.fromIndex === evt.toIndex) return
      console.log(`onDragRow: ${depth}`)
      const dataSource = vars.childGrid[depth].dataSource
      const visibleRows = evt.component.getVisibleRows()

      const moveRow = visibleRows.splice(evt.fromIndex, 1)
      visibleRows.splice(evt.toIndex, 0, moveRow[0])

      let start = evt.fromIndex, end = evt.toIndex
      if (evt.fromIndex > evt.toIndex) {
        start = evt.toIndex
        end = evt.fromIndex
      }

      for (let i=start; i<=end; i++) {
        let data = visibleRows[i].data
        console.log(data.id)
        await dataSource.update(data.id, { code_order: i + 1 })
      }
      await evt.component.refresh()
    }

    methods.onGridInitialized = (evt, key) => {
      vars.dataGridInstance[key] = evt.component
    }

    methods.onFocusedRowChanged = (depth, evt) => {
      if (depth === 0) vars.max_depth = evt.row.data.max_depth - 1
      console.log(`depth: ${depth} / ${vars.max_depth}`)
      vars.childGrid.splice(depth, vars.childGrid.length)

      if (depth < vars.max_depth) {
        const dataSource = baseCode.clone()
        dataSource.defaultFilters = [{name: 'parent_code_id', op: 'eq', val: evt.row.data.id}]
        dataSource.on('inserting', (params) => {
          params.parent_code_id = evt.row.data.id
        })

        vars.childGrid.push({
          parent: evt.row.data,
          dataSource
        })
      }
    }

    methods.onDragRow = (depth) => {
      return (evt) => {
        evt.promise = onDragRow(depth, evt)
      }
    }

    methods.initNewRow = (depth, evt) => {
      evt.data.parent_code_id = vars.childGrid[depth].parent.id
      evt.data.fk_company_id = vars.childGrid[depth].parent.fk_company_id
    }

    methods.validationUniqueCodeName = async ({data, value}) => {
      let filter = [
        ['code_name', '=', value], 
        'and', ['parent_code_id', '=', data.parent_code_id],
        'and', ['fk_company_id', '=', data.fk_company_id]
      ]
      if (data.id) {
        filter.push('and')
        filter.push(['id', '<>', data.id])
      }
      const resp = await validationStore.load({filter})
      return !resp.totalCount
    }

    return {
      vars, methods,
      baseCode
    };
  },
};
</script>

<style lang="scss" scoped>
.standard-code-container {
  // height: calc(100vh - 254px);
}
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
