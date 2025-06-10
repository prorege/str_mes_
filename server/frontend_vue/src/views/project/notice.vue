<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings">
        <div class="content-header">
          <dx-toolbar>
            <dx-item location="before">
              <div class="content-title">공지사항</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <dx-data-grid
          class="fixed-header-table" height="calc(100vh - 150px)"
          date-serialization-format="yyyy-MM-ddTHH:mm:ss"
          :data-source="store.projectNotice"
          :show-borders="true"
          :allow-column-reordering="true"
          :allow-column-resizing="true"
          :column-auto-width="true"
          :remote-operations="true"
          @initialized="evt => methods.initialized(evt, 'notice-grid')"
          @init-new-row="methods.initNewRow"
          @cell-click="methods.cellClick"
          @edit-canceled="methods.editCanceled"
          @editing-start="methods.editingStart">
          <!--dx-column data-field="id" caption="번호" sort-order="desc" :width="60" /-->
          <dx-column data-field="created" caption="생성시간" data-type="date" format="yyyy-MM-dd" :allow-editing="false" :visible="false" :width="120" />
          <dx-column data-field="important" caption="중요여부" data-type="boolean" :width="80" />
          <dx-column data-field="title" caption="제목">
            <dx-required-rule message="제목을 입력하세요" />
          </dx-column>
          <dx-column data-field="start_date" caption="공지시작일" data-type="date" format="yyyy-MM-dd" :width="100" />
          <dx-column data-field="end_date" caption="공지종료일" data-type="date" format="yyyy-MM-dd" :width="100" />
          <dx-column data-field="content_html" caption="내용" :visible="false" />
          <dx-column data-field="register_id" caption="최초등록자" :allow-editing="false" :width="100" />
          <dx-column data-field="fk_company_id" caption="회사" :allow-editing="false" :visible="false" />
          <dx-filter-row :visible="true"/>
          <dx-paging :page-size="20" />
          <dx-editing :allow-adding="vars.editable.value" :allow-updating="vars.editable.value" :allow-deleting="vars.editable.value" mode="popup" :use-icons="true">
            <dx-grid-popup
              :show-title="true"
              :width="840" :height="700"
              :resize-enabled="true"
              title="공지사항">
            </dx-grid-popup>
            <dx-form :col-count="1" :show-colon-after-label="false">
              <dx-group-item :col-count="2">
                <dx-simple-item data-field="title"/>
                <dx-simple-item data-field="important"/>
              </dx-group-item>
              <dx-group-item :col-count="2">
                <dx-simple-item data-field="start_date"/>
                <dx-simple-item data-field="end_date"/>
              </dx-group-item>
              <dx-simple-item 
                data-field="content_html" 
                editor-type="dxHtmlEditor" 
                :label="{visible: false}"
                :editor-options="vars.htmlEditorOptions"
              />
            </dx-form>
          </dx-editing>
        </dx-data-grid>
      </div>
    </div>

    <dx-popup
      v-model:visible="vars.noticeDetail.visible"
      :title="vars.noticeDetail.title"
      :drag-enabled="true"
      :close-on-outside-click="true"
      :show-close-button="true"
      :resize-enabled="true"
      :width="740"
      :height="540"
      @initialized="evt => methods.initialized(evt, 'notice-detail')"
      @hiding="methods.popupClose">
      <div class="popup-notice" v-html="vars.noticeDetail.context"></div>
    </dx-popup>
  </div>
</template>

<script>
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar'
import {DxDataGrid, DxColumn, DxEditing, DxPaging, DxPopup as DxGridPopup, DxForm, DxFilterRow, DxRequiredRule} from 'devextreme-vue/data-grid'
import {DxGroupItem, DxSimpleItem} from 'devextreme-vue/form'
import { DxPopup } from 'devextreme-vue/popup'
import {DxHtmlEditor} from 'devextreme-vue/html-editor'
import { ref, reactive } from 'vue'
import {projectNotice} from '../../data-source/project'
import authService from '../../auth'
import stateStore from '@/utils/state-store'

export default {
  components: {
    DxToolbar, DxItem, DxPopup,
    DxGroupItem, DxSimpleItem,
    DxDataGrid, DxColumn, DxEditing, DxPaging, DxGridPopup, DxForm, DxFilterRow, DxRequiredRule,
    DxHtmlEditor
  },
  setup() {
    const vars = {}, methods = {}, store = {projectNotice}
    
    // Vars
    vars.components = {}
    vars.edit = {}
    vars.editable = ref(true)
    vars.noticeDetail = reactive({
      visible: false,
      title: '',
      context: ''
    })
    vars.htmlEditorOptions = {
      height: 'calc(100vh - 350px)',
      toolbar: {
        items: [
          'undo', 'redo',
          'separator',
          {name: 'size', acceptedValues: ['8pt', '10pt', '12pt', '14pt', '18pt', '24pt', '36pt']},
          {name: 'font', acceptedValues: ['Arial', 'Courier New', 'Georgia', 'Impact', 'Lucida Console', 'Tahoma', 'Times New Roman', 'Verdana']},
          'bold', 'italic', 'strike', 'underline',
          'separator',
          'color', 'background', 
          'separator',
          'link', 'image'
        ],
        multiline: false
      }
    }
    store.projectNotice.defaultFilters = {name: 'fk_company_id', op: 'eq', val: authService.getCompanyId()}

    // Methods
    methods.initialized = (evt, key) => {
      vars.components[key] = evt.component
      stateStore.bind(key, evt.component)
    }

    methods.initNewRow = (evt) => {
      // console.log(evt)
      evt.data.fk_company_id = authService.getCompanyId()
      evt.data.important = false
      evt.data.start_date = new Date()
      evt.data.end_date = new Date()
      evt.data.register_id = authService.user.user_id
      vars.edit.data = evt.data
      vars.edit.key = null
    }

    methods.editingStart = (evt) => {
      console.log('editingStart')
      vars.edit.data = evt.data
      vars.edit.key = evt.key
    }

    methods.cellClick = (evt) => {
      // evt.component.editRow(evt.rowIndex)
      vars.noticeDetail.title = evt.data.title
      vars.noticeDetail.context = evt.data.content_html
      vars.noticeDetail.visible = true
    }

    methods.popupClose = () => {
      vars.noticeDetail.title = ''
      vars.noticeDetail.context = ''
    }

    methods.log = (evt) => {
      console.log(evt)
    }

    return {vars, methods, store}
  },
}
</script>
