<template>
    <div>
        <dx-load-panel v-model:visible="loading" :show-pane="true" />
        <div class="content-block" v-if="loaded">
            <div class="dx-card responsive-paddings back-colored">
                <div class="content-header">
                <dx-toolbar class="back-colored">
                    <dx-item location="before">
                    <div class="content-title">외근-출장현황</div>
                    </dx-item>
                    <dx-item
                    location="after"
                    widget="dxButton"
                    :options="{
                        text: '전체화면',
                        type: 'normal',
                        onClick: setFullscreen,
                    }"
                    />
                </dx-toolbar>
                </div>
        
                <div :key="refreshKey" ref="viewer" class="fullscreen-content">
                <dx-data-grid
                    width="100%"
                    height="100%"
                    class="custom-grid"
                    column-resizing-mode="widget"
                    :data-source="dataSource"
                    :show-borders="true"
                    :row-alternation-enabled="true"
                    :allow-column-reordering="true"
                    :allow-column-resizing="true"
                    :column-auto-width="true"
                    :remote-operations="true"
                    :sorting="{ mode: 'none' }"
                    @toolbar-preparing="onGrid1ToolbarPreparing"
                    :on-initialized="evt => onGridInitialized(evt, 'status')"
                >
                    <dx-grid-toolbar>
                    <dx-item location="before" template="day-tmpl" />
                    <dx-item location="center" template="title-tmpl" />
                    <dx-item location="after" template="date-tmpl" />
                    </dx-grid-toolbar>
                    <template #day-tmpl>
                    <div class="status-menu" style="margin-left: 20px;">{{ currentDay }}</div>
                    </template>
        
                    <template #title-tmpl>
                    <div class="status-title-xxlarge">
                        외근 / 출장 현황
                    </div>
                    </template>
        
                    <template #date-tmpl>
                    <div class="status-menu" style="margin-right: 20px;">{{ currentTime }}</div>
                    </template>
        
                    
                    <dx-column
                    data-field="manager"
                    caption="담당자"
                    css-class="column-dark"
                    alignment='center'
                    width="100"
                    />
                    <dx-column
                    data-field="companion"
                    caption="동행자"
                    css-class="column-dark"
                    alignment='center'
                    />
                    <dx-column
                    data-field="trip_type"
                    caption="구분"
                    css-class="column-dark"
                    alignment='center'
                    width="70"
                    />
                    <dx-column
                    caption="기간"
                    cell-template="period-template"
                    css-class="column-dark"
                    width="150"
                    alignment='center'
                    />
                    <dx-column
                    data-field="project_name"
                    caption="프로젝트명"
                    css-class="column-dark"
                    alignment='center'
                    />
                    <dx-column
                    data-field="note"
                    caption="업무 내용"
                    css-class="column-dark"
                    alignment='center'
                    />
                    <dx-column
                    data-field="stopover"
                    caption="경유지"
                    css-class="column-dark"
                    alignment='center'
                    />
                    <dx-column
                    data-field="vehicle"
                    caption="운행차량"
                    css-class="column-dark"
                    alignment='center'
                    width="110"
                    />
                    <template #period-template="{data}">
                        <div class="period_container">
                            <span>
                                <div class="period_date">{{ (moment(data.data['trip_start_date']).format('MM-DD')) }}</div>
                                <div class="period_hour">{{ (moment(data.data['trip_start_date']).format('HH:mm')) }}</div>
                            </span>
                            <span>~</span>
                            <span>
                                <div class="period_date">{{ (moment(data.data['trip_end_date']).format('MM-DD')) }}</div>
                                <div class="period_hour">{{ (moment(data.data['trip_end_date']).format('HH:mm')) }}</div>
                            </span>
                        </div>
                    </template>
                    <!-- dx-scrolling mode="infinite" / -->
                    <dx-paging :page-size="vars.setting.page" />
                </dx-data-grid>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script setup>
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
DxLookup,
DxToolbar as DxGridToolbar,
DxItem as DxGridItem,
DxRequiredRule as DxGridRequiredRule,
} from 'devextreme-vue/data-grid';
import { DxSelectBox } from 'devextreme-vue/select-box';
import { projectBusinessTripLog } from '@/data-source/project';
import {
performanceItem1,
getPerformanceItem1,
processPerformanceRegistration,
} from '@/data-source/produce';
import { setupControl } from '@/data-source/setup';
import moment from 'moment';
import { onMounted, ref, reactive, onBeforeUnmount } from 'vue';
import authService from '../../auth';
import { useRoute } from 'vue-router'
moment.locale('ko');
//document.body.style.zoom = '1.8';
const vars = { dlg: {} };
const loading = ref(false);
const loaded = ref(false);
const viewer = ref(null);
const route = useRoute()
const refreshKey = ref(Date.now());
vars.grid = { status: null };
vars.setting = reactive({
page: 10,
});
let timerId = null;

const dataSource = ref([])
const currentDate = moment().format('YYYY-MM-DD');
const currentDay = moment().format('MMMM Do (ddd)');
const currentTime = ref(moment().format('HH:mm:ss'));

const timerId2 = setInterval(() => {
currentTime.value = moment().format('HH:mm:ss');
}, 1000);

let timerId3


dataRefresh()


async function dataRefresh () {
    clearTimeout(timerId3)

    const params = {
        skip: 0, 
        take: 3000, 
        sort: [{ selector: 'trip_start_date', desc: false }], // 🔥 시작날짜 오름차순 정렬 추가
        filter: [
        ['trip_end_date', '>=', currentDate],
        ]
    }


    const {data} = await projectBusinessTripLog.load(params);
    console.log("data : ", data)
    dataSource.value = data;
    loaded.value = true

    if (route.path === "/monitoring/trip-log-status") timerId3 = setTimeout(() => dataRefresh(), 5 * 1000)
}

document.onfullscreenchange = () => {
if (!document.fullscreenElement) {
    // if (timerId) clearTimeout(timerId);
    // timerId = setTimeout(() => {
    //   refreshKey.value = Date.now();
    //   timerId = null;
    // }, 1000);
}
};

function onGrid1ToolbarPreparing(e){
    e.toolbarOptions.elementAttr = {
        class : 'toolbar-css'
    }
}

onMounted(async () => {
const { data } = await setupControl.load({
    filter: [['fk_company_id', '=', authService.getCompanyId()]],
    take: 1,
    skip: 0,
});
if (data.length > 0) {
    //document.body.style.zoom = data[0].monitoring_zoom;
    vars.setting.page = data[0].monitoring_page;
}
});

onBeforeUnmount(() => {
if (timerId) clearTimeout(timerId);
document.onfullscreenchange = null;
//document.body.style.zoom = '1.0';
clearInterval(timerId2);
clearTimeout(timerId3);
});

function onGridInitialized(evt, key) {
vars.grid[key] = evt.component;
}

function setFullscreen() {
if (!viewer.value) return;
viewer.value.requestFullscreen();
}

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
.custom-grid{
    font-size: 22px;
    font-weight: 700;
}

.status-title-xxlarge {
    font-size: 48px;
    font-weight: 700;
}
::v-deep .dx-toolbar-items-container{
    height: 76px;
}
.status-menu{
    font-size: 30px;
    font-weight: 700;
}
.period_container{
    display: flex;
    justify-content: space-around;
    align-items: center;
}

.period_date{
    color: #ffa500;
    font-size: 22px;
    font-weight: 600;
    text-align: center;
}
.period_hour{
    text-align: center;
    font-size: 19px;
}
::v-deep .dx-datagrid-content .dx-datagrid-table .dx-row > td{
    vertical-align: middle;
}

</style>
