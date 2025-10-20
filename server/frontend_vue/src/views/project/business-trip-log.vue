<template>
        <div>
            <div class="content-block">
                <div class="dx-card responsive-paddings">
                    <div class="content-header">
                        <dx-toolbar>
                        <dx-item location="before"
                            ><div class="content-title">외근-출장관리</div></dx-item
                        >
                        </dx-toolbar>
                    </div>
                    <div>
                        <dx-data-grid
                            column-resizing-mode="widget"
                            height="calc(100vh - 150px)"
                            :data-source="vars.dataSource.projectBusinessTripLog"
                            :show-borders="true"
                            :show-row-lines="true"
                            :remote-operations="true"
                            :focused-row-enabled="true"
                            :allow-column-resizing="true"
                            :allow-column-reordering="true"
                            @saving="methods.onSaving"
                            @editing-start="methods.onEditingStart"
                            @init-new-row="methods.onRowAdded"
                            @row-updated="methods.onRowUpdated"
                            @focused-cell-changed="methods.onFocusedCellChanged"
                            @initialized="(evt) => methods.onGridInitialized(evt, 'project-business-trip-log')"
                        >
                            <dx-grid-toolbar>
                                <dx-grid-item template="addRowButton" location="before" :visible="true" />
                                <dx-grid-item template="saveRowButton" location="before" :visible="true" />
                                
                            </dx-grid-toolbar>
                            <template #addRowButton>
                                <dx-button text="추가" icon="add" @click="methods.addRowButton" />
                            </template>
                            <template #saveRowButton>
                                <dx-button text="저장" icon="save" @click="methods.saveRowButton" />
                            </template>
                            <dx-search-panel :visible="true" :width="240" placeholder="검색" />
                            <dx-selection mode="single"/>
                            <dx-editing
                            mode="row"
                            :allow-adding="true"
                            :allow-updating="true"
                            :allow-deleting="true"
                            :use-icons="true"
                            />
                            <dx-paging :page-size="20"/>
                            <dx-column type="buttons" />
                            <dx-column
                            data-field="manager"
                            caption="담당자">
                            <dx-required-rule message="담당자 입력하세요"/>
                            </dx-column>
                            <dx-column data-field="companion" caption="동행자"
                            :editor-options="{
                                ...generateItemButtonOption('search', methods.createFindPopupFn('companion', '동행자 조회'))
                            }" />
                            <dx-column data-field="trip_type" caption="구분">
                                <dx-lookup
                                :data-source="vars.dataSource.trip_type"
                                value-expr="code_name"
                                display-expr="code_name"
                            />
                            </dx-column>
                            <dx-column 
                                data-field="trip_start_date"
                                data-type="datetime"
                                format="yyyy-MM-dd HH:mm"
                                caption="시작일시"
                                :allow-sorting="true">
                            </dx-column>
                            <dx-column 
                                data-field="trip_end_date"
                                data-type="datetime" 
                                format="yyyy-MM-dd HH:mm"
                                caption="종료일시"
                                :allow-sorting="false">
                            </dx-column>
                            <dx-column
                                data-field="project_name"
                                caption="프로젝트명"
                                :allow-editing="true"
                                :editor-options="{ ...generateItemButtonOption('search', methods.createFindPopupFn('project', '프로젝트 조회')) }"
                                >
                            </dx-column>
                            <dx-column 
                                data-field="note" 
                                caption="업무 내용" 
                                :allow-sorting="false"
                                :editor-options="{ ...generateItemButtonOption('rename', methods.createFindPopupFn('note', '업무 내용')),
                             }" />
                            <dx-column
                                data-field="stopover"
                                caption="장소(시,군/업체명)" />
                            <!-- <dx-column data-field="vehicle" caption="운행차량">
                                <dx-lookup
                                    :data-source="vars.dataSource.vehicle"
                                    value-expr="code_name"
                                    display-expr="code_name"
                                />
                            </dx-column> -->
                            
                        </dx-data-grid>
                    </div>
                </div>
            </div>
            <dx-popup
            v-model:visible="vars.dlg.finder.show"
            content-template="popup-content"
            width="60%"
            height="60%"
            :title="vars.dlg.finder.title"
            :close-on-outside-click="true"
            :key="vars.dlg.finder.key"
            :resize-enabled="true"
            @initialized="evt => methods.onGridInitialized(evt, 'find-popup')"
            >
            <template #popup-content>
                <data-grid-project
                v-if="vars.dlg.finder.key === 'project'"
                :filters="vars.dlg.finder.data"
                @change="methods.finderReturnHandler"
                />
                <data-grid-employee-select v-else-if="vars.dlg.finder.key === 'companion'" :filters="vars.dlg.finder.data" @change="methods.finderReturnHandler" />
                <div v-else-if="vars.dlg.finder.key === 'note'">
                    <div class="mb-2">
                        <dx-text-area
                        :height="430"
                        :value="vars.dlg.finder.data"
                        @update:value="methods.updateNoteValue"
                        />
                    </div>
                    <dx-toolbar>
                        <dx-item
                        widget="dxButton"
                        toolbar="top"
                        location="after"
                        :options="{
                            icon: 'save',
                            text: '저장',
                            onClick: methods.finderReturnHandler,
                        }"
                        />
                    </dx-toolbar>
                </div>
            </template>
            </dx-popup>
        </div>
</template>

<script>
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import {
DxDataGrid,
DxColumn,
DxEditing,
DxPaging,
DxRequiredRule,
DxSearchPanel,
DxHeaderFilter,
DxFilterRow,
DxLookup,
DxToolbar as DxGridToolbar,
DxItem as DxGridItem,
DxSelection,
} from 'devextreme-vue/data-grid';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import DxTextArea from 'devextreme-vue/text-area';
import { DxButton } from 'devextreme-vue/button';
import { DxDateBox } from 'devextreme-vue/date-box';
import { h, createApp } from 'vue';
import {
  baseCodeLoader,
} from '../../data-source/base';
import moment from 'moment';
import DataGridProject from '../../components/project/data-project.vue';
import DataGridEmployeeSelect from '../../components/base/data-employee-select.vue';
import { reactive, onMounted, ref, nextTick } from 'vue';
import { projectBusinessTripLog, getProjectBusinessTripLog, } from '../../data-source/project';
import { generateItemButtonOption, beforeExitConfirm} from '../../utils/util';
import { confirm, alert } from 'devextreme/ui/dialog';
import authService from '../../auth'
import stateStore from '@/utils/state-store';

export default {
    components: {
        DxSelection,
        DxDateBox,
        DxTextArea,
        DxButton,
        DxGridToolbar,
        DxGridItem,
        DxDataGrid,
        DxColumn,
        DxEditing,
        DxPaging,
        DxToolbar,
        DxItem,
        DxRequiredRule,
        DxSearchPanel,
        DxHeaderFilter,
        DxFilterRow,
        DxLookup,
        DxPopup,
        DxToolbarItem,
        DataGridProject,
        DataGridEmployeeSelect
    },
    setup() {
        const vars = { dlg: {} };
        vars.grid = {};
        vars.disabled = reactive({
            save: true
        });
        vars.dlg.finder = reactive({
            show: false,
            title: '',
            key: null,
            data: null,
        });
        vars.focus = ref();
        vars.dataSource = reactive({
            projectBusinessTripLog : [],
            trip_type: [],
            vehicle: [],
        });
        vars.dataSource.projectBusinessTripLog = getProjectBusinessTripLog(
            [{name:'trip_end_date', op: '>=', val: moment().format('YYYY-MM-DD')}]
        );

        onMounted(async () => {
            await methods.loadBaseCode();
        });

        const methods = {
            createFindPopupFn(key, title, data = null){
                const _key = key,
                _title = title,
                _data = data;
                return () => {
                    vars.dlg.finder.key = _key;
                    vars.dlg.finder.data = _data;
                    vars.dlg.finder.title = _title;
                    vars.dlg.finder.show = true;
                };
            },
            onSaving(e){
                vars.disabled.save = true;
                beforeExitConfirm.clear()
            },
            onEditingStart(e){
                vars.disabled.save = false;
                beforeExitConfirm.check(() => !vars.disabled.save);
            },
            
            onRowAdded(e){
                e.data.manager = authService.getUserName();
                e.data.trip_start_date = new Date();
                e.data.trip_end_date = new Date();
            },

            onRowUpdated(e){
                // console.log(e);
            },

            async onFocusedCellChanged(e){
                if(e.rowIndex === -1) return;
                if(!vars.focus.value) {
                    vars.focus.value = e;
                    return;
                }
                const grid = vars.grid['project-business-trip-log'];
                if(!grid) return;

                const isDifferentRow = e.rowIndex !== vars.focus.value.rowIndex;
                
                if (isDifferentRow && grid && grid.hasEditData()) {
                    const isSelect = await confirm('저장되지않은 항목이 있습니다.\n 수정 후 다음 항목으로 넘어가시겠습니까? ', '수정');
                    await grid.clearSelection();
                    if (isSelect) {
                        await grid.saveEditData();
                        if(e.columnIndex == 0){
                            await grid.editRow(e.rowIndex);
                        }else{
                            await grid.option("focusedRowIndex", e.rowIndex);
                        }
                        
                    } else {
                        await grid.option("focusedRowIndex", vars.focus.value.rowIndex);
                        return;
                    }
                }
                vars.focus.value = e;
            },

            async loadBaseCode(){
                return baseCodeLoader(['외근출장구분', '운행차량']).then(response =>{
                vars.dataSource.trip_type = response['외근출장구분']
                vars.dataSource.vehicle = response['운행차량']
                });
            },

            finderReturnHandler(data) {
                const grid = vars.grid['project-business-trip-log'];
                const rowIndex = vars.focus.value ? vars.focus.value.rowIndex : 0;
                switch (vars.dlg.finder.key) {
                    case 'project': {
                        grid.cellValue(rowIndex, 'project_name', data.project_name)
                        break;
                    }
                    case 'companion': {
                        grid.cellValue(rowIndex, 'companion', data.map(item=> item.emp_name).join(', '));
                        break
                    }
                    case 'note': {
                        grid.cellValue(rowIndex, 'note', vars.dlg.finder.data);
                        break
                    }
                }

                vars.dlg.finder.show = false;
                vars.dlg.finder.title = '';
                vars.dlg.finder.key = null;
                vars.dlg.finder.data = null;
            },

            onGridInitialized(evt, key) {
                vars.grid[key] = evt.component;
                stateStore.bind(key, evt.component);
            },
            async addRowButton(){
                const grid = vars.grid['project-business-trip-log'];
                if(!grid) return;
                if(grid.hasEditData()){
                    await grid.saveEditData();
                }
                await grid.addRow();
                vars.focus.value = {rowIndex:0};
                await grid.option("focusedRowIndex", 0);
            },

            async saveRowButton(){
                const grid = vars.grid['project-business-trip-log'];
                if(!grid) return;
                await grid.saveEditData();
            },

            updateNoteValue(v) {
                vars.dlg.finder.data = v;
            }, 
        }
        return {
            vars,
            methods,
            generateItemButtonOption,
        };
    },
};
</script>
<style scoped>

</style>