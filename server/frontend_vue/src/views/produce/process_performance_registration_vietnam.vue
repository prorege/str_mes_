<script setup>
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar'
import {
  DxForm,
  DxLabel,
  DxGroupItem,
  DxSimpleItem,
  DxEmptyItem,
  DxButtonItem
} from 'devextreme-vue/form'
import { 
  DxDataGrid, 
  DxColumn, 
  DxPaging, 
  DxEditing,
  DxToolbar as DxGridToolbar
} from 'devextreme-vue/data-grid'
import { DxPopup, DxPosition, DxToolbarItem } from 'devextreme-vue/popup'
import { DxLoadPanel } from 'devextreme-vue/load-panel'

import {projectRegistration} from '@/data-source/project'
import {
  baseBom, 
  baseBomProcess, 
  baseBomLink,
  baseCode
} from '@/data-source/base'
import {
  processPerformanceRegistration, 
  performance, 
  performanceItem1,
  produceWorkOrderItem2,
  processMaterialConsumption
} from '@/data-source/produce'
import DataGridWorkOrderItem from '@/components/produce/data-work-order-item-vietnam.vue'
import DataGridProcPermReg from '@/components/produce/data-process-performance-registration-vietnam.vue'
import { generateItemButtonOption } from '@/utils/util'
import { notifyInfo, notifyError } from '@/utils/notify'

import authService from '@/auth'
import moment from 'moment'
import {ref, reactive, nextTick, onBeforeUnmount} from 'vue'
import numeral from 'numeral'

const formState = ref('read')
const loading = ref(false)
const popup = ref({show: false, type: 'work', filter: null})
const confirm = ref({show: false})
const popupRefreshId = ref(Date.now())
const processRenderKey = ref(`pr-${Date.now()}`)
const components = reactive({ form: null, grid: null, add: null })
const materialOptions = reactive({ key: 'value', data: [], items: [] })

document.body.style.zoom = '1.5'

const formData = ref({
  work_order: null,
  project: null,
  performance: {
    fk_manager_id: authService.user.emp_name
  }
})

const workList = ref([])

const numpad = ref({
  visible: false,
  value: '0',
  key1: null,
  key2: null
})

const consume = ref({
  lot_number: '',
  quantity: 0,
  item_code: ''
})

const itemList = ref(null)
const progressItems = ref(null)
const employeeList = ref([])
const progressItemCount = {}

// token 기간 늘리기
let authtoken = null
const tmk = setInterval(() => { authtoken = authService.token }, 60 * 1000)
onBeforeUnmount(() => { clearInterval(tmk) })
loadManager()

document.body.classList.add('kiosk-view')
function initializeGridComponent (component) {
  components.grid = component
  component.filter(['process_number', '=', ''])
}

async function loadManager () {
  const {data: parentItem} = await baseCode.load({filter: [
    ['code_name', '=', '현장공정담당자'], 
    ['fk_company_id', '=', authService.getCompanyId()]
  ]})
  if (!parentItem.length) return
  const parentId = parentItem[0].id

  const {data: codes} = await baseCode.load({filter: ['parent_code_id', '=', parentId]})
  employeeList.value = codes
}

function checkState (flags) {
  return flags.includes(formState.value)
}

function addItem () {
  clearForm()
  formData.value.performance.created = new Date()
  formData.value.performance.work_start_time = formData.value.performance.work_end_time = new Date()
  formData.value.performance.work_rest_time = '00:00'
  formData.value.performance.work_duration = '00:00'
  formState.value = 'add'
}

async function getDupItem (params) {
  const {data: resp} = await processPerformanceRegistration.load({filter: [
    ['order_number', '=', params.order_number],
    ['fk_company_id', '=', params.fk_company_id],
    ['fk_process_id', '=', params.fk_process_id],
    ['fk_work_order_item', '=', params.fk_work_order_item]
  ]})
  return resp
}

async function editItem () {
  if (!formData.value.performance) return
  formState.value = 'edit'
}

async function updateItem () {
  loading.value = true
  if (formState.value === 'add') {
    if (formData.value.performance.work_order_item.required_quantity < formData.value.performance.process_quantity) {
      notifyInfo('완료수량이 작지수량보다 클수 없습니다', {position: 'top left'})
      loading.value = false
      return
    }
    try {
      const params = Object.assign({}, formData.value.performance)
      // const worker = employeeList.value.find(v => v.code_name === params.fk_manager_id)
      params.worker = params.worker.join(',')
      params.order_number = formData.value.work_order.number
      params.created = moment().format('YYYY-MM-DD HH:mm:ss')
      params.fk_company_id = authService.getCompanyId()
      if (params.work_start_time instanceof Date) params.work_start_time = moment(params.work_start_time).format('HH:mm')
      if (params.work_end_time instanceof Date) params.work_end_time = moment(params.work_end_time).format('HH:mm')
      if (params.work_rest_time instanceof Date) params.work_rest_time = moment(params.work_rest_time).format('HH:mm')
      const good_quantity = params.good_quantity
      delete params.fk_manager_id
      delete params.work_order_item
      delete params.good_quantity
      delete params.item
      delete params.work_duration

      const dupItems = await getDupItem(params)
      const totalProcQty = dupItems.reduce((t, i) => (t + i.process_quantity), 0)
      console.log(`작지수량: ${formData.value.performance.work_order_item.required_quantity}, 기완료수량: ${totalProcQty}, 추가완료수량: ${params.process_quantity}`)
      if (formData.value.performance.work_order_item.required_quantity < (params.process_quantity + totalProcQty)) {
        notifyInfo(`완료수량이 작지수량보다 클수 없습니다. 이미 완료한 이력을 확인해 주세요. [${dupItems.map(v => `${v.number}: ${v.process_quantity}`).join(',')}]`, {position: 'top left'})
        loading.value = false
        return
      }
      
      if (isLastProcess()) {
        notifyInfo('생산입고로 자동 등록 처리 됩니다', {position: 'top left'})
        let { data: newPerm } = await performance.insert({
          target_date: params.created,
          department: authService.user.department.department_name,
          manager: authService.user.user_name,
          // department: formData.value.work_order.department,
          // manager: formData.value.work_order.manager,
          etc: '',
          fk_company_id: authService.getCompanyId()
        })
        await performanceItem1.insert({
          item_code: params.item_code,
          production_receiving_quantity: params.process_quantity,
          check_quantity: params.process_quantity,
          work_order_number: params.order_number,
          bad_quantity: params.bad_quantity,
          action_quantity: 0,
          good_quantity: good_quantity,
          check_yn: true,
          lot: formData.value.performance.process_tag,
          unit_price: formData.value.performance.item.purchase_price,
          request_delivery_date: formData.value.performance.work_order_item.request_delivery_date,
          order_number: formData.value.performance.work_order_item.order_number,
          fk_project_management_id: formData.value.performance.work_order_item.fk_project_management_id,
          client_company: formData.value.performance.work_order_item.client_company,
          client_item_number: formData.value.performance.work_order_item.client_item_number,
          end_user: formData.value.performance.work_order_item.end_user,
          fk_performance_registration_id: newPerm.id,
          fk_work_order_item: formData.value.performance.work_order_item.id,
          warehouse_code: authService.user.department.wh_code
        })
        console.log(`생산입고 등록 완료: ${newPerm.id}`)
      }

      const { data } = await processPerformanceRegistration.insert(params)
      formData.value.performance.id = data.id
      formData.value.performance.number = data.number
      await updateConsumeItem()

      notifyInfo('저장되었습니다', {position: 'top left'})
      clearForm()
      formState.value = 'read'
    }
    catch (ex) {
      console.error(ex)
      notifyError('저장에 실패하였습니다', {position: 'top left'})
    }
    finally {
      loading.value = false
    }
  }
  else {
    try {
      const params = {
        worker: formData.value.performance.worker.join(','), 
        process_quantity: formData.value.performance.process_quantity,
        bad_quantity: formData.value.performance.bad_quantity,
        work_start_time: formData.value.performance.work_start_time,
        work_end_time: formData.value.performance.work_end_time,
        work_rest_time: formData.value.performance.work_rest_time,
        fk_process_id: formData.value.performance.fk_process_id,
        process_tag: formData.value.performance.process_tag
      }

      if (isLastProcess()) {
        const {data: perfItem} = await performanceItem1.load({filter: [
          ['fk_work_order_item', '=', formData.value.performance.work_order_item.id],
          ['work_order_number', '=', formData.value.work_order.number],
          ['item_code', '=', formData.value.performance.item_code]
        ]})

        if (perfItem.length) {
          await performanceItem1.update(perfItem[0].id, {
            production_receiving_quantity: params.process_quantity,
            check_quantity: params.process_quantity,
            bad_quantity: params.bad_quantity,
            good_quantity: formData.value.performance.good_quantity
          })
          notifyInfo('생산입고가 수정되었습니다', {position: 'top left'})
        }
      }

      await processPerformanceRegistration.update(formData.value.performance.number, params)
      await updateConsumeItem()

      notifyInfo('저장되었습니다', {position: 'top left'})
      clearForm()
      formState.value = 'read'
    }
    catch (ex) {
      console.error(ex)
      notifyError('저장에 실패하였습니다', {position: 'top left'})
    }
    finally {
      loading.value = false
    }
  }
}

async function updateConsumeItem () {
  if (!components.grid || !components.grid.hasEditData()) return
  await components.grid.saveEditData()
}

async function onConsumeSaving ({changes}) {
  for (const item of changes) {
    switch (item.type) {
      case 'insert': {
        item.data.process_number = formData.value.performance.number
        break
      }
    }
  }
}

function isLastProcess () {
  if (!progressItems.value) return true
  if (progressItems.value.length <= 1) return true
  const selected = progressItems.value.findIndex(v => v.id === formData.value.performance.fk_process_id)

  if (selected < 0) {
    console.info('공정을 찾을수 없음')
    console.info(progressItems.value)
    console.info(formData.value.performance.fk_process_id)
    return false
  }

  return selected >= (progressItems.value.length - 1)
}

async function clearForm () {
  consume.value.item_code = ''
  consume.value.lot_number = ''
  consume.value.quantity = 0
  components.grid.filter(['process_number', '=', ''])
  components.grid.cancelEditData()

  components.form.beginUpdate()
  formData.value.work_order = null
  formData.value.project = null
  formData.value.performance = {fk_manager_id: authService.user.emp_name}
  popupRefreshId.value = Date.now()
  components.form.endUpdate()
  setProgressCount([])
  workList.value = []
  numpad.value.visible = false
  numpad.value.value = '0'
  numpad.value.key1 = null
  numpad.value.key2 = null
  itemList.value = undefined;
  progressItems.value = []
  for (const key of Object.keys(progressItemCount)) {
    delete progressItemCount[key]
  }
  await nextTick()
}

function removeItem () {
  if (formData.value.performance.number) {
    confirm.value.show = true
  }
  else {
    clearForm()
    formState.value = 'read'
  }
}

async function removeItemExec () {
  try {
    if (isLastProcess()) {
      const {data: perfItem} = await performanceItem1.load({filter: [
        ['fk_work_order_item', '=', formData.value.performance.work_order_item.id],
        ['work_order_number', '=', formData.value.work_order.number],
        ['item_code', '=', formData.value.performance.item_code]
      ]})

      if (perfItem.length) {
        notifyInfo('생산입고가 삭제되었습니다', {position: 'top left'})
        await performanceItem1.remove(perfItem[0].id)
        await performance.remove(perfItem[0].fk_performance_registration_id)
      }
    }

    if (components.grid) {
      const rows = components.grid.getVisibleRows()
      rows.forEach(({rowIndex}) => components.grid.deleteRow(rowIndex))
      await components.grid.saveEditData()
    }

    await processPerformanceRegistration.remove(formData.value.performance.number)
    notifyInfo('삭제되었습니다', {position: 'top left'})
    clearForm()
    formState.value = 'read'
  }
  catch (ex) {
    console.error(ex)
    notifyError('삭제에 실패하였습니다', {position: 'top left'})
  }
  finally {
    confirm.value.show = false
  }
}

function getPopupCb (name) {
  return () => {
    // if (name === 'perm') {
    //   popup.value.filter = [
    //     ['created', '>=', moment().startOf('d').format('YYYY-MM-DD HH:mm:ss')]
    //   ]
    // }
    // else {
    //   popup.value.filter = null
    // }
    popup.value.filter = null
    popup.value.type = name
    popup.value.show = true
  }
}

function setProgressCount (progress) {
  for (const key in progressItemCount) {
    delete progressItemCount[key]
  }
  for (const prc of progress) {
    if (progressItemCount[prc.fk_process_id] === undefined) progressItemCount[prc.fk_process_id] = 0
    progressItemCount[prc.fk_process_id] += prc.process_quantity
  }
  processRenderKey.value = `pr-${Date.now()}`
}

async function loadItem (item) {
  await clearForm()
  if (popup.value.type === 'work') {
    formData.value.work_order = item.work_order
    formData.value.performance.item_code = item.item_code
    itemList.value = [item]
  }
  else if (popup.value.type === 'perm') {
    // setProgressCount([item])
    item.worker = item.worker.split(',')
    formData.value.work_order = { number: item.order_number }
    formData.value.performance = item
    itemList.value = [item]
  }
  
  popup.value.show = false
  popup.value.type = null
}

function progressItemColor (idx = 0) {
  const colors = [
    '#4572A7', '#AA4643', '#89A54E', '#80699B', '#3D96AE',
    '#DB843D', '#92A8CD', '#A47D7C', '#B5CA92']

  return {'backgroundColor': colors[idx % 9]}
}

async function onFormDataChange (evt) {
  // console.log('필드업데이트:', evt.dataField)
  switch (evt.dataField) {
    case 'performance.item_code': {
      if (formData.value.performance && formData.value.performance.item_code) {
        let itemId = null

        if (!formData.value.performance.number) {
          const item = itemList.value.find(v => v.item_code === formData.value.performance.item_code)
          const {data: project} = await projectRegistration.load({filter: ['id', '=', item.fk_project_management_id]})
          formData.value.project = project.length ? project[0] : null

          const {data: pastData} = await processPerformanceRegistration.load({
            filter: [
              ['order_number', '=', formData.value.work_order.number],
              ['fk_work_order_item', '=', item.id]
            ]
          })
          setProgressCount(pastData)

          formData.value.performance.work_order_item = item
          formData.value.performance.fk_work_order_item = item.id
          formData.value.performance.fk_project_management_id = item.fk_project_management_id
          formData.value.performance.process_quantity = item.required_quantity
          formData.value.performance.item = item.item

          itemId = item.item.id
        }
        else {
          const {data: project} = await projectRegistration.load({filter: ['id', '=', formData.value.performance.fk_project_management_id]})
          formData.value.project = project.length ? project[0] : null
          itemId = formData.value.performance.item.id

          const {data: pastData} = await processPerformanceRegistration.load({
            filter: [
              ['order_number', '=', formData.value.performance.order_number],
              ['fk_work_order_item', '=', formData.value.performance.fk_work_order_item]
            ]
          })
          setProgressCount(pastData)

          if (components.grid) {
            components.grid.filter([
              ['process_number', '=', formData.value.performance.number],
              ['item.lot_check', '=', true]
            ])
          }
        }

        const {data: bom} = await baseBom.load({
            filter: [
              ['item_id', '=', itemId], 
              'and', ['fk_company_id', '=', authService.getCompanyId()]
            ]
        })

        if (bom.length) {
          const {data: itemProcess} = await baseBomProcess.load({filter: ['bom_id', '=', bom[0].id], sort: [{ selector : 'order', desc : false}]})
          
          progressItems.value = itemProcess.map(v => v.process)
        }
        
        const {data} = await produceWorkOrderItem2.load({ filter: [
          ['work_order.number', '=', formData.value.work_order.number],
          ['item.lot_check', '=', true]
        ]})

        materialOptions.items = data
        materialOptions.data = data.map(v => {
          const text = [v.item.item_code, v.item.item_name]
          if (v.item.item_standard) text.push(v.item.item_standard)
          return {
            text: text.join('/'),
            value: v.item.item_code
          }
        })
      }
      else {
        formData.value.project = null
      }
      break
    }
    case 'performance.process_quantity':
    case 'performance.bad_quantity': {
      if (!formData.value.performance.bad_quantity) formData.value.performance.bad_quantity = 0
      formData.value.performance.good_quantity = formData.value.performance.process_quantity - formData.value.performance.bad_quantity
      break
    }
    case 'performance.work_start_time':
    case 'performance.work_end_time':
    case 'performance.work_rest_time': {
      if (!formData.value.performance.work_start_time || !formData.value.performance.work_end_time) break
      const start = moment(formData.value.performance.work_start_time, 'HH:mm')
      const end = moment(formData.value.performance.work_end_time, 'HH:mm')

      let rest = 0
      if (formData.value.performance.work_rest_time) {
        const today = moment().startOf('D')
        if (formData.value.performance.work_rest_time instanceof Date) rest = moment(formData.value.performance.work_rest_time).diff(today, 'minute')
        else rest = moment(formData.value.performance.work_rest_time, 'HH:mm').diff(today, 'minute')
      }

      const min = end.diff(start, 'minute') - rest
      if (min < 0) {
        notifyError('작업시간이 0보다 작습니다', {position: 'top left'})
      }
      else {
        formData.value.performance.work_duration = `${String(Math.floor(min / 60)).padStart(2, '0')}:${String(min % 60).padStart(2, '0')}`
      }
      break
    }
  }
}

async function addConsumeRow () {
  if (!components.grid) return

  if (!consume.value.item_code) {
    notifyError('품목을 선택해 주세요', {position: 'top left'})
    return
  }

  if (!consume.value.lot_number) {
    notifyError('LOT번호를 적어주세요', {position: 'top left'})
    return
  }

  if (isNaN(consume.value.quantity)) {
    notifyError('투입수량을 적어주세요', {position: 'top left'})
    return
  }

  await components.grid.addRow()
  components.grid.cellValue(0, 'item_code', consume.value.item_code)
  components.grid.cellValue(0, 'lot_number', consume.value.lot_number)
  components.grid.cellValue(0, 'quantity', consume.value.quantity)
}

function addNumpad (value) {
  if (typeof value === 'string') {
    if (numpad.value.value === '0') numpad.value.value = value
    else numpad.value.value += value
  }
  else {
    if (value === -1) {
      if (numpad.value.value.length <= 1) numpad.value.value = '0'
      else numpad.value.value = numpad.value.value.slice(0, -1)
    }
    else if (value === null) numpad.value.value = '0'
  }
}
function openNumpad (key1, key2, e) {
  if (e.component.option('readOnly')) return
  if (key1 === 'consume') {
    numpad.value.value = String(consume.value[key2])
  }
  else {
    if (!key2) numpad.value.value = String(formData.value[key1] || '0')
    else numpad.value.value = String(formData.value[key1][key2] || '0')
  }
  
  numpad.value.key1 = key1
  numpad.value.key2 = key2
  numpad.value.visible = true
}
function closeNumpad () {
  numpad.value.visible = false
  numpad.value.key1 = null
  numpad.value.key2 = null
  numpad.value.origin = null
}
function submitNumpad () {
  const v = parseInt(numpad.value.value, 10)
  if (numpad.value.key1 === 'consume') {
    consume.value[numpad.value.key2] = v
  }
  else {
    if (!numpad.value.key2) formData.value[numpad.value.key1] = v
    else numpad.value.value = formData.value[numpad.value.key1][numpad.value.key2] = v
    
    if (!formData.value.performance.bad_quantity) formData.value.performance.bad_quantity = 0
    formData.value.performance.good_quantity = formData.value.performance.process_quantity - formData.value.performance.bad_quantity
  }

  closeNumpad()
}

function processFormat(value){
  if(!value) return ''
  switch(value.id){
    case 1:{
      return 'forming'
    }
    case 2:{
      return 'assembling'
    }
    case 3:{
      return 'line fix'
    }
    case 4: {
      return '1st molding'
    }
    case 5: {
      return '2nd molding'
    }
    case 6: {
      return 'visual inspection'
    }
    case 7: {
      return 'performance test'
    }
    case 8: {
      return 'packaging'
    }
    case 9:{
      return 'SMT process'
    }
    case 10:{
      return 'case lot marking'
    }
    case 11:{
      return 'harness work'
    }
    case 12:{
      return 'case + sticker'
    }
    case 13:{
      return '1st test'
    }
    case 14:{
      return 'bolt assembly'
    }
  }
  
}
function numberFormat(value, format) {
  return numeral(value).format(format)
}

async function onConsumeFormChanged ({component, dataField, value}) {
  component.beginUpdate()
  if (dataField === 'item_code') {
    consume.value.lot_number = ''
    const item = materialOptions.items.find(v => v.item_code === value)
    const qty = formData.value.performance.process_quantity || 1
    consume.value.quantity = qty
    if (item) {
      const { data: link } = await baseBomLink.load({filter: [
        ['child_bom.item_id', '=', item.item.id],
        ['parent_bom.item_id', '=', formData.value.performance.item.id]
      ]})
      if (link.length) {
        console.info(`투입수량: BOM찾음 ${qty} * ${link[0].requirement}`)
        consume.value.quantity = qty * link[0].requirement
      }
    }
    else {
      console.log(`옵션에 다음 항목 없음: ${value}`)
    }
  }
  component.endUpdate()
}

function logout () {
  authService.logOut()
  location.href = '/'
}
</script>

<template>
  <div class="mobile-container back-colored">
    <dx-load-panel v-model:visible="loading" :show-pane="true" />
    <dx-toolbar class="back-colored">
      <dx-item location="before">
        <div class="content-title" id="process-performance-registration">Process Performance registration</div>
      </dx-item>
      <dx-item
        location="after"
        locate-in-menu="auto"
        widget="dxButton"
        :options="{
          text: 'New',
          type: 'copy',
          disabled: checkState(['add', 'edit']),
          onClick: addItem,
        }"
      />
      <dx-item
        location="after"
        locate-in-menu="auto"
        widget="dxButton"
        :options="{
          text: 'Edit',
          type: 'normal',
          disabled: !formData.performance.number,
          onClick: editItem,
        }"
      />
      <dx-item
        location="after"
        locate-in-menu="auto"
        widget="dxButton"
        :options="{
          text: 'Save',
          type: 'success',
          disabled: checkState(['read']),
          onClick: updateItem,
        }"
      />
      <dx-item
        location="after"
        locate-in-menu="auto"
        widget="dxButton"
        :options="{
          text: checkState(['add']) ? 'Cancel' : 'Delete',
          type: 'danger',
          onClick: removeItem,
        }"
      />
      <dx-item
        location="after"
        locate-in-menu="auto"
        widget="dxButton"
        :options="{
          text: 'LogOut',
          type: 'default',
          onClick: logout,
        }"
      />
    </dx-toolbar>

    <div class="display-flex">
      <dx-form 
        :form-data="formData" 
        :show-colon-after-label="false" class="form-style" 
        :col-count="2"
        @initialized="({component}) => components.form = component"
        @field-data-changed="onFormDataChange">
        <dx-simple-item
          data-field="work_order.number"
          css-class="reg-form-input"
          :editor-options="{
            placeholder: '(Find)',
            readOnly: !checkState(['add']),
            ...generateItemButtonOption('search', getPopupCb('work'))
          }">
          <dx-label text="Work Order Number" />
        </dx-simple-item>
        <dx-empty-item />
        <dx-simple-item
          data-field="performance.number"
          css-class="reg-form-input"
          :editor-options="{
            placeholder: '(Automatic Number)', readOnly: checkState(['add']),
            ...generateItemButtonOption('search', getPopupCb('perm'))
          }">
          <dx-label text="Performance Number" />
        </dx-simple-item>
        <dx-simple-item
          data-field="performance.created"
          editor-type="dxDateBox"
          css-class="reg-form-input"
          :editor-options="{readOnly: true}">
          <dx-label text="Registration Date" />
        </dx-simple-item>

        <dx-simple-item
          data-field="performance.item_code"
          css-class="reg-form-input"
          editor-type="dxSelectBox"
          :editor-options="{
            dataSource: itemList, 
            displayExpr: 'item.item_name',
            valueExpr: 'item.item_code',
            readOnly: itemList === undefined
          }">
          <dx-label text="Item Name" />
        </dx-simple-item>
        <dx-simple-item
          data-field="performance.process_tag"
          css-class="reg-form-input"
          :editor-options="{
            readOnly: !checkState(['add', 'edit'])
          }">
          <dx-label text="Production Week" />
        </dx-simple-item>

        <dx-simple-item
          data-field="performance.item.item_code"
          css-class="reg-form-input"
          :editor-options="{readOnly: true}">
          <dx-label text="Item Code" />
        </dx-simple-item>
        <dx-simple-item
          data-field="performance.item.item_standard"
          css-class="reg-form-input"
          :editor-options="{readOnly: true}">
          <dx-label text="Item Standard" />
        </dx-simple-item>
        <dx-group-item :col-span="2" :col-count="4">
          <dx-simple-item
            data-field="performance.work_order_item.required_quantity"
            css-class="reg-form-input"
            editor-type="dxNumberBox"
            :editor-options="{readOnly: true, format: ',##0'}">
            <dx-label text="Required Quantity" />
          </dx-simple-item>
          <dx-simple-item
            data-field="performance.process_quantity"
            css-class="reg-form-input"
            editor-type="dxNumberBox"
            :editor-options="{
              readOnly: !checkState(['add', 'edit']),
              format: ',##0',
              onFocusIn: (e) => openNumpad('performance', 'process_quantity', e)
            }">
            <dx-label text="Completed Quantity" />
          </dx-simple-item>
          <dx-simple-item
            data-field="performance.bad_quantity"
            css-class="reg-form-input"
            editor-type="dxNumberBox"
            :editor-options="{
              readOnly: !checkState(['add', 'edit']),
              format: ',##0',
              onFocusIn: (e) => openNumpad('performance', 'bad_quantity', e)
            }">
            <dx-label text="Bad Quantity" />
          </dx-simple-item>
          <dx-simple-item
            data-field="performance.good_quantity"
            css-class="reg-form-input"
            editor-type="dxNumberBox"
            :editor-options="{
              readOnly: true,
              format: ',##0'
            }">
            <dx-label text="Good Quantity" />
          </dx-simple-item>
        </dx-group-item>
        <dx-simple-item
          data-field="performance.fk_process_id"
          css-class="reg-form-input"
          editor-type="dxSelectBox"
          :editor-options="{
            valueExpr: 'id',
            displayExpr: processFormat,
            acceptCustomValue: true,
            dataSource: progressItems,
            readOnly: !progressItems
          }">
          <dx-label text="Production Process" />
        </dx-simple-item>
        <dx-simple-item
          data-field="performance.worker"
          css-class="reg-form-input"
          editor-type="dxTagBox"
          :editor-options="{
            dropDownOptions: {
              height: 100,
            },
            dataSource: employeeList,
            displayExpr: 'code_name',
            valueExpr: 'code_name',
            readOnly: !checkState(['add', 'edit'])
          }">
          <dx-label text="Worker" />
        </dx-simple-item>
        <dx-group-item :col-span="2" :col-count="4">
          <dx-simple-item
            data-field="performance.work_start_time"
            css-class="reg-form-input"
            editor-type="dxDateBox"
            :editor-options="{
              type: 'time',
              pickerType: 'rollers',
              displayFormat: 'HH:mm',
              readOnly: !checkState(['add', 'edit'])
            }">
            <dx-label text="Work Start Time" />
          </dx-simple-item>
          <dx-simple-item
            data-field="performance.work_end_time"
            css-class="reg-form-input"
            editor-type="dxDateBox"
            :editor-options="{
              type: 'time',
              pickerType: 'rollers',
              displayFormat: 'HH:mm',
              readOnly: !checkState(['add', 'edit'])
            }">
            <dx-label text="Work End Time" />
          </dx-simple-item>
          <dx-simple-item
            data-field="performance.work_rest_time"
            css-class="reg-form-input"
            editor-type="dxDateBox"
            :editor-options="{
              type: 'time',
              pickerType: 'rollers',
              displayFormat: 'HH:mm',
              readOnly: !checkState(['add', 'edit'])
            }">
            <dx-label text="Rest Time" />
          </dx-simple-item>
          <dx-simple-item
            data-field="performance.work_duration"
            css-class="reg-form-input"
            editor-type="dxDateBox"
            :editor-options="{
              type: 'time',
              displayFormat: 'HH:mm',
              readOnly: true
            }">
            <dx-label text="Working Time" />
          </dx-simple-item>
        </dx-group-item>
      </dx-form>
      <div class="consume-table">
        <div class="">
          <dx-form 
            style="margin-bottom:10px"
            :form-data="consume" 
            :show-colon-after-label="false"
            @initialized="({component}) => components.add = component"
            @field-data-changed="onConsumeFormChanged">

            <dx-simple-item
              data-field="item_code"
              editor-type="dxSelectBox"
              :label="{text: 'Meterial'}"
              :editor-options="{
                dataSource: materialOptions.data,
                readOnly: !checkState(['add', 'edit']),
                displayExpr: 'text',
                valueExpr: 'value'
              }"
            />
            
            <dx-group-item :col-count="5">
              <dx-simple-item
                data-field="lot_number"
                :col-span="3"
                :label="{text: 'LOT Number'}"
                :editor-options="{
                  readOnly: !checkState(['add', 'edit']),
                  showClearButton: true
                }"
              />
              <dx-simple-item
                data-field="quantity"
                editor-type="dxNumberBox"
                :col-span="2"
                :label="{text: 'Quantity'}"
                :editor-options="{
                  readOnly: !checkState(['add', 'edit']),
                  format: ',##0',
                  onFocusIn: (e) => openNumpad('consume', 'quantity', e)
                }"
              />
            </dx-group-item>
            
            <dx-button-item 
              :button-options="{
                text: 'Add',
                type: 'success',
                disabled: !checkState(['add', 'edit']),
                onClick: addConsumeRow
              }"
            />
          </dx-form>
        </div>
        <dx-data-grid
          height="180px"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :focused-row-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :data-source="processMaterialConsumption"
          @initialized="({component}) => initializeGridComponent(component)"
          @saving="onConsumeSaving">

          <dx-column caption="ID" data-field="id" :visible="false" :allow-editing="false" sort-order="desc" :show-in-column-chooser="false" />
          <dx-column caption="Lot Number" data-field="lot_number" :allow-editing="false" />
          <dx-column caption="Item Code" data-field="item_code" :allow-editing="false" />
          <dx-column caption="Quantity" data-field="quantity" :allow-editing="false" />
          <dx-column caption="생성시간" data-field="created" :visible="false" :allow-editing="false" />
          <dx-column caption="생산실적번호" data-field="process_number" :visible="false" :allow-editing="false" :show-in-column-chooser="false" />

          <dx-grid-toolbar :visible="false" />
          <dx-paging :page-size="20"/>
          <dx-editing mode="batch" :use-icons="true" :allow-adding="true" :allow-deleting="true" />

        </dx-data-grid>
      </div>
    </div>

    <div class="progress-panel">
      <div class="progress-title">Entire Production Process Status</div>
      <div class="progress-item-wrap" v-if="progressItems" :key="processRenderKey">
        <div class="progress-item" :style="progressItemColor(idx)" v-for="(item, idx) in progressItems" :key="idx">
          <div class="progress-item-bar"></div>
          <div class="progress-item-name">
            <div>{{processFormat(item)}}</div>
            <div class="progress-item-count" v-if="progressItemCount[item.id]">
              ({{numberFormat(progressItemCount[item.id], '0,0')}})
            </div>
          </div>
        </div>
      </div>
      <div class="progress-item-wrap empty" v-else>
        선택된 작업이 없습니다
      </div>
    </div>

    <dx-popup
      v-model:visible="popup.show"
      content-template="popup-content"
      title="항목선택"
      position="left top"
      width="66vw" height="65vh"
      :fullscreen="true"
      :close-on-outside-click="true"
      :resize-enabled="true">
      <template #popup-content>
        <data-grid-work-order-item v-show="popup.type === 'work'"
          height="460px" 
          :key="`wo-${popupRefreshId}`" 
          :filters="[['unproduced_quantity', '>', 0], 'and', ['end_yn', '=', false], 'and', ['work_order.department', '=', '맥텍비나']]" 
          @change="loadItem" 
        />
        <data-grid-proc-perm-reg v-show="popup.type === 'perm'"
          height="460px" 
          :key="`pg-${popupRefreshId}`"  
          :filters="popup.filter" @change="loadItem" 
        />
      </template>
    </dx-popup>

    <dx-popup
      v-model:visible="confirm.show"
      content-template="popup-content"
      title="삭제 확인"
      width="14rem" height="10rem"
      :wrapper-attr="{class: 'delete-confirm'}"
      :close-on-outside-click="false"
      :show-close-button="false"
      :drag-enabled="false"
      :resize-enabled="false">
      <dx-position my="left top" of="#process-performance-registration" />
      <dx-toolbar-item widget="dxButton" toolbar="bottom" location="before" :options="{text: '닫기', onClick: () => { confirm.show = false }}" />
      <dx-toolbar-item widget="dxButton" toolbar="bottom" location="after" :options="{text: '삭제', onClick: removeItemExec}" />
      <template #popup-content>
        삭제하시겠습니까?
      </template>
    </dx-popup>

    <dx-popup
      content-template="popup-content"
      v-model:visible="numpad.visible"
      :close-on-outside-click="true"
      :show-close-button="false"
      :show-title="false"
      :width="300"
      :height="300"
      position="left top"
    >
      <template #popup-content>
        <div class="numpad">
          <div class="numpad-value">{{numpad.value}}</div>
          <div class="numpad-body">
            <div class="numpad-item" @click="addNumpad('1')">1</div>
            <div class="numpad-item" @click="addNumpad('2')">2</div>
            <div class="numpad-item" @click="addNumpad('3')">3</div>

            <div class="numpad-item" @click="addNumpad('4')">4</div>
            <div class="numpad-item" @click="addNumpad('5')">5</div>
            <div class="numpad-item" @click="addNumpad('6')">6</div>

            <div class="numpad-item" @click="addNumpad('7')">7</div>
            <div class="numpad-item" @click="addNumpad('8')">8</div>
            <div class="numpad-item" @click="addNumpad('9')">9</div>

            <div class="numpad-item" @click="addNumpad(-1)">◀</div>
            <div class="numpad-item" @click="addNumpad('0')">0</div>
            <div class="numpad-item" @click="addNumpad(null)">Clear</div>
          </div>
        </div>
      </template>
      <dx-toolbar-item location="after" widget="dxButton" :options="{icon: 'close', text: 'Cancel', onClick: closeNumpad}" />
      <dx-toolbar-item location="after" widget="dxButton" :options="{icon: 'print', text: 'Add', onClick: submitNumpad}" />
    </dx-popup>
  </div>
</template>

<style lang="scss" scoped>

:deep(.mobile-container .delete-confirm .dx-popup-normal) {
  margin: 100px 0 0 0;
}
.dx-popup-wrapper {
  .dx-overlay-content.dx-popup-normal.dx-resizable.dx-popup-inherit-height {
    transform: translate(50%, 50%) !important;
  }
}
.mobile-container {
  padding: 10px; margin: 10px;
}
.form-style {
  margin: 10px 0 0;
}

.progress-panel {
  position: absolute;
  bottom: 14px; left: 14px; right: 14px;
  padding: 14px;
  background-color: #e3e3e3;
  border-radius: 10px;
}
.progress-title {
  font-size: 1.4em;
}
.progress-item-wrap {
  // width: 300px;
  display: flex;
  align-items: center;
  height: 100px;
  border: 1px dashed #c7c7c7;
  border-radius: 6px;

  &.empty {
    justify-content: center;
    align-items: center;
    font-size: 1.4em;
    color: #808080;
  }
}
.progress-item {
  height: 60px;
  flex: 1 1 auto;
  margin: 0 10px;
  border-radius: 5px;
  background-color: #f7f7f7;
  position: relative;
  overflow: hidden;

  color: white;
  border: 1px solid white;
  box-shadow: 0px 2px 4px rgb(0 0 0 / 40%);
}
.progress-item-bar {
  position: absolute;
  top: 0; bottom: 0; left: 0;
  background-color: #c2cf9f;
  z-index: 1;
}
.progress-item-name {
  position: absolute;
  top: 0; bottom: 0; left: 0; right: 0;
  display: flex; justify-content: center; align-items: center;
  text-align: center;
  z-index: 2;
}
.progress-item-count {
  color: #b4b4b4;
  margin-left: 4px;
}
.display-flex {
  display: flex;
}
.consume-table {
  width: 600px;
  padding: 10px;
  margin: 10px 0px 10px 10px;
  box-sizing: border-box;
  border: 1px solid #c7c7c7;
  border-radius: 5px;
}
.numpad {
  .numpad-value {
    border-radius: 4px;
    background-color: #ebebeb;
    padding: 5px 10px;
    text-align: right;
    font-size: 21px;
  }
  .numpad-body {
    border: 1px solid #e5e5e5;
    border-radius: 4px;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    margin-top: 6px;
    padding: 5px;
  }
  .numpad-item {
    margin: 4px 0;
    padding: 6px 0;
    border-radius: 4px;
    flex: 0 0 32.6%;
    text-align: center;
    color: white;
    background-color: #6e6b88;
    cursor: pointer;
    &:hover {
      background-color: #504d64;
    }
  }
}
</style>