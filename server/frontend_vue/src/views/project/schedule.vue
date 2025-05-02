<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings">
        <div class="content-header">
          <dx-toolbar>
            <dx-item location="before">
              <div class="content-title">일정관리</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <dx-form 
          :form-data="vars.formData"
          @initialized="(evt) => methods.initialized(evt, 'project-schdule-form')">
          <dx-group-item :col-count="3">
            <dx-group-item :col-span="2">
              <dx-group-item :col-count="2">
                <dx-simple-item 
                  data-field="project_number"
                  :editor-options="{
                    placeholder: '프로젝트를 선택해 주세요',
                    buttons: [
                      {name: 'search', location: 'after', options: {stylingMode: 'text', icon: 'search', onClick: methods.openProjectDialog}}
                    ]
                  }">
                  <dx-label text="프로젝트번호" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item
                  data-field="contract_begin_date"
                  editor-type="dxDateBox"
                  :editor-options="{readOnly: true}">
                  <dx-label text="계약시작일" :show-colon="false" />
                </dx-simple-item>
              </dx-group-item>
              <dx-simple-item
                data-field="project_name"
                :editor-options="{readOnly: true}">
                <dx-label text="프로젝트명" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
            <dx-group-item>
              <dx-simple-item
                data-field="contract_end_date"
                editor-type="dxDateBox"
                :editor-options="{readOnly: true}">
                <dx-label text="계약종료일" :show-colon="false" />
              </dx-simple-item>
              <dx-simple-item
                data-field="total_progress"
                template="progress">
                <dx-label text="진행률" :show-colon="false" />
              </dx-simple-item>
            </dx-group-item>
          </dx-group-item>

          <template #progress="{}">
            <div style="height: 34px">
              <dx-progress-bar
                :value="vars.formData.value.total_progress"
                :show-status="false"
              />
            </div>
          </template>
        </dx-form>
        
        <div style="height: 16px"></div>
        <dx-gantt
          :task-list-width="400"
          :disabled="!vars.formData.id"
          height="calc(100vh - 250px)"
          scale-type="weeks"
          @initialized="(evt) => methods.initialized(evt, 'project-gantt')"
          @task-inserting="methods.taskInserting"
          @task-updating="methods.taskUpdating">

          <dx-tasks 
            :data-source="ds.projectSchedule" 
            title-expr="title" 
            start-expr="start_date" 
            end-expr="end_date" 
            progress-expr="progress_percent" 
          />

          <dx-gantt-toolbar>
            <dx-gantt-item name="undo"/>
            <dx-gantt-item name="redo"/>
            <dx-gantt-item name="separator"/>
            <dx-gantt-item name="addTask"/>
            <dx-gantt-item name="deleteTask"/>
            <dx-gantt-item name="separator"/>
            <dx-gantt-item name="zoomIn"/>
            <dx-gantt-item name="zoomOut"/>
          </dx-gantt-toolbar>

          <dx-editing :enabled="true"/>

          <dx-column data-field="title" caption="일정" />
          <dx-column data-field="progress_percent" caption="비율(%)" :width="62" />
          <dx-column data-field="start_date" caption="시작" data-type="date" format="yyyy-MM-dd" :width="90" />
          <dx-column data-field="end_date" caption="종료" data-type="date" format="yyyy-MM-dd" :width="90" />

        </dx-gantt>
      </div>
    </div>

    <dx-popup 
      v-model:visible="vars.status.dlgProject"
      content-template="popup-content"
      title="프로젝트 선택"
      :close-on-outside-click="true"
      :width="680" :height="460"
      :resize-enabled="true"
      @initialized="(evt) => methods.initialized(evt, 'scehdule-popup')">

      <template #popup-content>
        <dx-data-grid
          :data-source="ds.projectRegistration"
          :show-borders="true"
          :allow-column-reordering="true"
          :allow-column-resizing="true"
          :column-auto-width="true"
          :remote-operations="true"
          @initialized="(evt) => methods.initialized(evt, 'project-table')"
          @row-click="methods.projectClickHandler">
          <dx-grid-column data-field="project_number" caption="프로젝트번호" />
          <dx-grid-column data-field="project_name" caption="프로젝트명" />
          <dx-grid-column data-field="contract_date" caption="계약일자" data-type="date" format="yyyy-MM-dd" />
          <dx-grid-column data-field="contract_begin_date" caption="계약기간(시작)" data-type="date" format="yyyy-MM-dd" />
          <dx-grid-column data-field="contract_end_date" caption="계약기간(종료)" data-type="date" format="yyyy-MM-dd" />
          <dx-grid-column data-field="contract_amount" caption="계약금액" :format="{ type: 'fixedPoint', precision: 2 }" />
          <dx-paging :page-size="20"/>
          <dx-filter-row :visible="true"/>
        </dx-data-grid>
      </template>
    </dx-popup>

  </div>
</template>

<script>
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import {DxGantt, DxTasks, DxColumn, DxEditing, DxToolbar as DxGanttToolbar, DxItem as DxGanttItem
  // DxDependencies,
  // DxResourceAssignments,
  // DxValidation,
  // DxItem as DxGanttItem
} from 'devextreme-vue/gantt';
import {DxForm, DxLabel, DxGroupItem, DxSimpleItem} from 'devextreme-vue/form'
import {DxDataGrid, DxColumn as DxGridColumn, DxPaging, DxFilterRow} from 'devextreme-vue/data-grid'
import {DxPopup} from 'devextreme-vue/popup'

import { reactive, ref } from 'vue';
import { projectRegistration, projectSchedule } from '../../data-source/project';
import { DxProgressBar } from 'devextreme-vue/progress-bar'
import authService from '../../auth'
import moment from 'moment'

export default {
  components: {
    DxToolbar, DxItem, 
    DxForm, DxLabel, DxGroupItem, DxSimpleItem,
    DxProgressBar,
    DxPopup,
    DxDataGrid, DxGridColumn, DxPaging, DxFilterRow, DxGanttToolbar, DxEditing, DxGanttItem,
    DxGantt, DxTasks, DxColumn
    // DxValidation, DxDependencies, DxResourceAssignments
  },
  setup() {
    const vars = {}, methods = {}, ds = reactive({})

    // Vars
    vars.components = {}
    vars.formData = ref({
      id: null,
      project_number: null,
      project_name: null,
      contract_begin_date: null,
      contract_end_date: null,
      total_progress: 0
    })
    vars.status = reactive({
      dlgProject: false
    })

    // DataSources
    projectRegistration.defaultFilters = [{name: 'fk_company_id', op: 'eq', val: authService.getCompanyId()}]
    ds.projectRegistration = projectRegistration

    projectSchedule.defaultFilters = [{name: 'fk_project_management_id', op: 'eq', val: 0}]
    ds.projectSchedule = projectSchedule

    projectSchedule.on('loaded', ({data, totalCount}) => {
      if (!data.length) {
        vars.formData.value.total_progress = 0
        return
      }
      const sum = data.reduce((t, i) => t += i.progress_percent || 0, 0)
      const avg = Math.floor(sum / totalCount)
      vars.formData.value.total_progress = avg
    })

    methods.initialized = (evt, name) => {
      vars.components[name] = evt.component
    }

    methods.openProjectDialog = () => {
      vars.status.dlgProject = true
      if (vars.components['project-table']) vars.components['project-table'].refresh()
    }

    methods.projectClickHandler = (evt) =>{
      /*
      allocation_amount: null
      business_department: null
      business_manager: null
      contract_begin_date: "2022-01-18T22:26:21"
      contract_date: "2022-01-18T22:26:21"
      contract_end_date: "2022-02-17T22:26:21"
      contract_item: null
      project_name: "프로젝트 001"
      contract_amount: 27848
      contract_type: null
      created: "2022-01-19T23:03:13"
      fk_company_id: 1
      id: 1
      note: null
      order_company: null
      project_number: "PROJ-001"
      register_date: null
      register_department: null
      register_manager: null
      sales_department: null
      sales_manager: null
      site_address: null
      total_progress: null
      use_date: null
      use_department: null
      use_price: null
      */
     vars.formData.value = evt.data
      if (!vars.formData.value.total_progress) vars.formData.value.total_progress = 0
      vars.components['project-schdule-form'].beginUpdate()
      vars.components['project-schdule-form'].updateData(vars.formData.value)
      vars.components['project-schdule-form'].endUpdate()
      methods.loadSchedule()
      vars.status.dlgProject = false
    }

    methods.loadSchedule = async () => {
      projectSchedule.defaultFilters = [{name: 'fk_project_management_id', op: 'eq', val: vars.formData.value.id}]
      vars.components['project-gantt'].refresh()
    }

    methods.taskInserting = (evt) => {
      console.log(evt)
      
      const isCancel = new Promise((resolve, reject) => {
        projectSchedule.insert({
          title: '새 일정',
          start_date: moment(evt.values.start_date).add(9, 'hours').toDate(),
          end_date: moment(evt.values.end_date).add(9, 'hours').toDate(),
          progress_percent: evt.values.progress_percent,
          fk_project_management_id: vars.formData.value.id
        })
        .then(() => {
          vars.components['project-gantt'].refresh()
          resolve(false)
        })
        .catch((ex) => {
          reject(ex)
        })
      })
      
      evt.cancel = isCancel
    }

    methods.taskUpdating = (evt) => {
      console.log(evt)
      if (evt.newValues.start_date) {
        evt.newValues.start_date = moment(evt.newValues.start_date).add(9, 'hours').toDate()
      }
      if (evt.newValues.end_date) {
        evt.newValues.end_date = moment(evt.newValues.end_date).add(9, 'hours').toDate()
      }
    }

    return {
      vars, methods, ds
    };
  },
};
</script>

<style lang="scss" scoped>
:deep(.content-block .dx-gantt .dx-gantt-taskWrapper .dx-gantt-task .dx-gantt-tPrg) {
  background-color: #47b8bd;
}
</style>
