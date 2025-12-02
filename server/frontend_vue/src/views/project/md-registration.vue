<template>
        <div>
            <div class="content-block">
                <div class="dx-card responsive-paddings">
                    <div class="content-header">
                        <dx-toolbar>
                        <dx-item location="before">
                            <div class="content-title">M/D 관리</div>
                        </dx-item>
                        </dx-toolbar>
                    </div>
                    <div>
                        <dx-data-grid
                            column-resizing-mode="widget"
                            height="calc(100vh - 150px)"
                            :data-source="vars.dataSource.projectMdRegistration"
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
                            @initialized="(evt) => methods.onGridInitialized(evt, 'project-md-registration')"

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
                            <dx-column
                                data-field="project_name"
                                caption="프로젝트명"
                                :allow-editing="true"
                                :editor-options="{ ...generateItemButtonOption('search', methods.createFindPopupFn('project', '프로젝트 조회')) }"
                                >
                            </dx-column>                            
                            
                            <dx-column data-field="position_type" caption="업무형태">
                                <dx-lookup
                                :data-source="vars.dataSource.position_type"
                                value-expr="code_name"
                                display-expr="code_name"
                            />
                            </dx-column>
                            <!-- 총 M/D 일 -->
                            <dx-column 
                                data-field="total_md_day"
                                caption="총 M/D(일)"
                                data-type="number"
                                :allow-editing="false"
                            />

                            <!-- 총 M/D 시간 -->
                            <dx-column 
                                data-field="total_md_hour"
                                caption="총 M/D(시간)"
                                data-type="number"
                                :allow-editing="false"
                            />

                            <!-- 누적사용 M/D 일 -->
                            <dx-column 
                                data-field="used_md_day"
                                caption="누적사용 M/D(일)"
                                data-type="number"
                                :allow-editing="false"
                            />

                            <!-- 누적사용 M/D 시간 -->
                            <dx-column 
                                data-field="used_md_hour"
                                caption="누적사용 M/D(시간)"
                                data-type="number"
                                :allow-editing="false"
                            />

                            <!-- 사용 M/D(시간) 입력 필드 -->
                            <dx-column 
                                data-field="used_md_hour_input"
                                caption="사용 M/D(시간)"
                                data-type="number"
                                :allow-sorting="false"
                            />


                            <dx-column 
                                data-field="note" 
                                caption="업무 내용" 
                                :allow-sorting="false"
                                :editor-options="{ ...generateItemButtonOption('rename', methods.createFindPopupFn('note', '업무 내용')),
                             }" />
                            
                            
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
import { projectMdRegistration, getProjectMdRegistration, getProjectExcutionPlan, getProjectExcutionPlanExpense } from '../../data-source/project';
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
            project_manday : [],
            position_type: [],
            vehicle: [],
        });
        vars.dataSource.projectMdRegistration = getProjectMdRegistration(
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
                const grid = vars.grid['project-md-registration'];
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
                return baseCodeLoader(['업무형태', '운행차량']).then(response =>{
                vars.dataSource.position_type = response['업무형태']
                vars.dataSource.vehicle = response['운행차량']
                });
            },

            async finderReturnHandler(data) {
                const grid = vars.grid['project-md-registration'];
                const rowIndex = vars.focus.value ? vars.focus.value.rowIndex : 0;

                switch (vars.dlg.finder.key) {
                    case 'project': {
                        console.log("=== [1] 프로젝트 선택 시작 ===");
                        console.log("선택된 프로젝트:", data);

                        // 기본 정보 바인딩
                        grid.cellValue(rowIndex, 'project_name', data.project_name);
                        grid.cellValue(rowIndex, 'fk_project_management_id', data.id); 
                        // if(data.project_manager) grid.cellValue(rowIndex, 'manager', data.project_manager);

                        try {
                            const projectId = data.id;
                            let totalMdDay = 0;
                            let totalMdHour = 0;
                            let usedMdDay = 0;
                            let usedMdHour = 0;

                            // ---------------------------------------------------------
                            // A. 실행계획 조회
                            // ---------------------------------------------------------
                            const planStore = getProjectExcutionPlan();
                            const plans = await planStore.load({ 
                                filter: ['fk_project_management_id', '=', projectId] 
                            });

                            console.log("=== [2] 실행계획 조회 결과 ===", plans);

                            // API 응답이 배열인지, 객체인지 확인을 위한 방어 코드
                            // (만약 plans.data 로 들어오는 구조라면 여기서 캐치됨)
                            const planList = Array.isArray(plans) ? plans : (plans.data || []);

                            if (planList.length > 0) {
                                const planId = planList[0].id;
                                console.log("찾은 실행계획 ID:", planId);

                                const expenseStore = getProjectExcutionPlanExpense();
                                const expenses = await expenseStore.load({ 
                                    filter: ['fk_project_excution_plan_id', '=', planId] 
                                });

                                console.log("=== [3] 경비 내역 조회 결과 ===", expenses);
                                const expenseList = Array.isArray(expenses) ? expenses : (expenses.data || []);

                                expenseList.forEach((ex, index) => {
                                    // 공백 확인을 위해 대괄호로 감싸서 로그 출력
                                    console.log(`[${index}] 항목명: [${ex.expense_description}], Day: ${ex.day_amount}, Time: ${ex.time_amount}`);
                                    
                                    // "PM, PE M/D" 비교 (공백 제거 후 비교 등 유연성 추가 가능)
                                    // 혹시 모를 공백 제거를 위해 trim() 사용 추천
                                    const desc = ex.expense_description ? ex.expense_description.trim() : '';
                                    
                                    if (desc === 'PM, PE M/D') {
                                        console.log("👉 조건 일치! 합산합니다.");
                                        totalMdDay += (ex.day_amount || 0);
                                        totalMdHour += (ex.time_amount || 0);
                                    }
                                });
                            } else {
                                console.warn("⚠️ 이 프로젝트에 연결된 실행계획이 없습니다.");
                            }

                            // ---------------------------------------------------------
                            // B. 누적 사용 M/D 조회
                            // ---------------------------------------------------------
                            const mdStore = getProjectMdRegistration();
                            const prevMds = await mdStore.load({ 
                                filter: ['fk_project_management_id', '=', projectId] 
                            });
                            
                            console.log("=== [4] 기존 M/D 등록 내역 ===", prevMds);
                            const prevMdList = Array.isArray(prevMds) ? prevMds : (prevMds.data || []);

                            if (prevMdList.length > 0) {
                                const totalUsedHours = prevMdList.reduce((acc, curr) => acc + (curr.used_md_hour_input || 0), 0);
                                usedMdHour = totalUsedHours;
                                usedMdDay = parseFloat((totalUsedHours / 8).toFixed(1)); 
                            }

                            console.log(`=== [5] 최종 결과 === TotalDay: ${totalMdDay}, UsedDay: ${usedMdDay}`);

                            // 그리드 적용
                            grid.cellValue(rowIndex, 'total_md_day', totalMdDay);
                            grid.cellValue(rowIndex, 'total_md_hour', totalMdHour);
                            grid.cellValue(rowIndex, 'used_md_day', usedMdDay);
                            grid.cellValue(rowIndex, 'used_md_hour', usedMdHour);

                        } catch (error) {
                            console.error("❌ 에러 발생:", error);
                        }
                        
                        break;
                    }
                    // ... (companion, note 케이스는 기존과 동일)
                    case 'companion': {
                        if (Array.isArray(data)) {
                             grid.cellValue(rowIndex, 'companion', data.map(item=> item.emp_name).join(', '));
                        } else {
                             grid.cellValue(rowIndex, 'companion', data.emp_name);
                        }
                        break;
                    }
                    case 'note': {
                        grid.cellValue(rowIndex, 'note', vars.dlg.finder.data);
                        break;
                    }
                }
                vars.dlg.finder.show = false;
            },

            onGridInitialized(evt, key) {
                vars.grid[key] = evt.component;
                stateStore.bind(key, evt.component);
            },
            async addRowButton(){
                const grid = vars.grid['project-md-registration'];
                if(!grid) return;
                if(grid.hasEditData()){
                    await grid.saveEditData();
                }
                await grid.addRow();
                vars.focus.value = {rowIndex:0};
                await grid.option("focusedRowIndex", 0);
            },

            async saveRowButton(){
                const grid = vars.grid['project-md-registration'];
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