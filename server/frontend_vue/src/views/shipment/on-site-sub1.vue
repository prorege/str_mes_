<script setup>
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar'
import {
  DxForm,
  DxLabel,
  DxSimpleItem,
} from 'devextreme-vue/form'
import { DxPopup } from 'devextreme-vue/popup'
import { DxLoadPanel } from 'devextreme-vue/load-panel'
import DataGridWorkOrderItem from '@/components/produce/data-work-order-item'
import DataGridRelease from '@/components/shipment/data-release.vue'
import { baseEmployee } from '@/data-source/base'
import { projectRegistration } from '@/data-source/project'
import { produceWorkOrderItem1 } from '@/data-source/produce'
import { shipmentRelease, shipmentOrder, shipmentReleaseItem, shipmentOrderItem } from '@/data-source/shipment'
import QrReader from '@/components/qr/reader'
import {
  generateItemButtonOption
} from '@/utils/util'
import authService from '@/auth'
import { notifyInfo, notifyError } from '@/utils/notify'
import {ref, nextTick, onBeforeUnmount} from 'vue'
import moment from 'moment'

const loading = ref(false)
const showQrReader = ref(false)
const popup = ref({show: false, type: 'order', filter: null})
const employeeList = ref([])
const projectList = ref([])
const formState = ref('init')
const formData = ref({
  order: null,
  project: null, 
  work_order: null,
  release_manager_id: authService.user.id,
  item_code: null,
  release: null,
  release_quantity: null
})
const todayText = moment().format('YYYY-MM-DD')
let employee = authService.user

// token 기간 늘리기
let authtoken = null
const tmk = setInterval(() => { authtoken = authService.token }, 60 * 1000)
onBeforeUnmount(() => { clearInterval(tmk) })

baseEmployee.load({filter: [['fk_company_id', '=', authService.getCompanyId()]], skip: 0, take: 1000})
  .then(({data}) => employeeList.value = data)
  .then(setDefaultManager)
  .then(() => projectRegistration.load({filter: ['fk_company_id', '=', authService.getCompanyId()], skip: 0, take: 1000}))
  .then(({data}) => (projectList.value = data))

function setDefaultManager () {
  const emp = employeeList.value.find(item => item.emp_code === authService.user.user_id)
  if (emp) {
    formData.value.release_manager_id = emp.id
  }
}

function getPopupCb (name, filter = null) {
  return (evt) => {
    evt.event.stopPropagation()
    evt.event.preventDefault()
    popup.value.type = name
    popup.value.show = true
    popup.value.filter = filter
  }
}

function newItem () {
  formState.value = 'new'
}

function editItem () {
  formState.value = 'edit'
}

async function updateItem () {
  loading.value = true

  try {
    if (!formData.value.release) {
      const { data: insertedData } = await shipmentRelease.insert({
        release_date: moment().format('YYYY-MM-DD HH:mm:ss'),
        client_company: formData.value.order.client_company,
        client_manager: formData.value.order.client_manager,
        release_department: formData.value.order.order_department,
        release_manager: formData.value.order.work_order.manager,
        release_type: formData.value.order.order_type,
        vat_type: formData.value.order.vat_type,
        payment_terms: formData.value.order.payment_terms,
        delivery_date: formData.value.order.delivery_date,
        delivery_place: formData.value.order.delivery_place,
        client_order_number: formData.value.order.client_order_number,
        fk_project_management_id: formData.value.order.fk_project_management_id,
        end_user: formData.value.order.end_user,
        note: formData.value.order.note,
        etc: formData.value.order.etc,
        supply_price: formData.value.order.supply_price,
        vat: formData.value.order.vat,
        total_price: formData.value.order.total_price,
        confirmed: false,
        fk_company_id: authService.getCompanyId()
      })
      formData.value.release = insertedData

      await shipmentReleaseItem.insert({
        item_code: formData.value.item_code,
        order_quantity: formData.value.order_item.order_quantity,
        release_quantity: formData.value.release_quantity,
        unit_price: formData.value.order_item.unit_price,
        supply_price: formData.value.order_item.supply_price,
        request_delivery_date: formData.value.order_item.request_delivery_date,
        non_invoice: formData.value.release_quantity,
        warehouse_code: formData.value.order_item.warehouse_code,
        order_number: formData.value.order.order_number,
        client_item_number: formData.value.order_item.client_item_number,
        note: formData.value.order_item.note,
        closing_yn: 0,
        fk_project_management_id: formData.value.order_item.fk_project_management_id,
        fk_release_id: formData.value.release.id,
        fk_order_item_id: formData.value.order_item.id
      })
    }
    else {
      await shipmentReleaseItem.update(formData.value.order_item.id, {
        release_quantity: formData.value.release_quantity
      })
    }

    notifyInfo('저장되었습니다')
    clearForm()
  }
  catch (ex) {
    console.error(ex)
    notifyError('저장 중 문제가 발생하였습니다')
  }
  finally {
    loading.value = false
  }
}

function removeItem () {
  loading.value = true
  clearForm()
  loading.value = false
}

function clearForm () {
  formData.value.order = null
  formData.value.items = null
  formData.value.project = null 
  formData.value.order_item = null
  formData.value.release = null
  formData.value.item_code = null
  formData.value.release_quantity = null
  formState.value = 'init'

  setDefaultManager()
}

async function loadItem (item) {
  clearForm()
  await nextTick()
  if (popup.value.type === 'work-order') {
    formData.value.work_order = item
    if (item.order_number) {
      const {data: order} = await shipmentOrder.load({filter: ['order_number', '=', item.order_number]})
      formData.value.order = order[0]
    }
    if (item.fk_project_management_id) {
      const {data: project} = await projectRegistration.load({filter: ['id', '=', item.fk_project_management_id]})
      formData.value.project = project[0]
    }
    else {
      formData.value.project = null
    }
    newItem()
  }
  else if (popup.value.type === 'release') {
    formData.value.release = item
    const {data: releaseItems} = await shipmentReleaseItem.load({filter: ['fk_release_id', '=', item.id]})
    if (releaseItems.length) {
      formData.value.items = releaseItems
      await nextTick()
      formData.value.item_code = releaseItems[0].item_code
    }
  }
  popup.value.show = false
}

function onPasteHandler ({event}) {
  try {
    const text = event.originalEvent.clipboardData.getData('text')
    const list = text.split('|')
    if (list.length !== 4) throw Error('QR코드 형식이 맞지 않습니다')
    loadOrderData(list[0], list[2])
  }
  catch (ex) {
    console.error(ex)
    notifyError('QR정보를 읽어오는데 실패했습니다');
  }
}

async function onFormDataChange (evt) {
  if (evt.dataField === 'item_code') {
    if (formData.value.item_code) {
      const item = formData.value.items.find(v => v.item_code === formData.value.item_code)
      formData.value.order_item = item.order_item ? item.order_item : item

      if (item.fk_release_id) {
        // 출고품목일 경우
        const {data: orderData} = await shipmentOrder.load({filter: ['order_number', '=', item.order_number]})
        if (orderData.length) {
          formData.value.order = orderData[0]
          formData.value.release_quantity = item.release_quantity
        }
      }
    }
  }
}

function onReadQrData (data) {
  showQrReader.value = false;
  if (!data) notifyError('스캔이 취소됬습니다');
  else {
    const list = data.data.split('|')
    loadOrderData(list[0], list[3])
  }
}

async function loadOrderData (orderNumber, itemCode, quantity) {
  const params = {
    filter: [
      ['work_order.number', '=', orderNumber],
      'and',
      ['item_code', '=', itemCode]
    ]
  }
  const {data: orderData} = await produceWorkOrderItem1.load(params)
  if (orderData.length) {
    if (!orderData[0].unproduced_quantity) {
      notifyError('미입고수량이 0인 항목입니다');
      return
    }

    popup.value.type = 'work-order'
    await loadItem(orderData[0])
    await nextTick()
    formData.value.item_code = itemCode
    notifyInfo(`${orderNumber}를 불러옵니다`);
  }
  else {
    notifyError('수주번호를 조회할 수 없습니다');
  }
}
</script>

<template>
  <div class="mobile-container back-colored">
    <dx-load-panel v-model:visible="loading" :show-pane="true" />
    <dx-toolbar class="back-colored">
      <dx-item
        location="after"
        locate-in-menu="auto"
        widget="dxButton"
        :options="{
          text: '신규',
          type: 'default',
          disabled: formData.release || formState === 'new',
          onClick: newItem,
        }"
      />
      <dx-item
        location="after"
        locate-in-menu="auto"
        widget="dxButton"
        :options="{
          text: '수정',
          type: 'normal',
          disabled: !formData.order || !formData.release || formState === 'edit',
          onClick: editItem,
        }"
      />
      <dx-item
        location="after"
        locate-in-menu="auto"
        widget="dxButton"
        :options="{
          text: '저장',
          type: 'success',
          disabled: formState !== 'new' && formState !== 'edit',
          onClick: updateItem,
        }"
      />
      <dx-item
        location="after"
        locate-in-menu="auto"
        widget="dxButton"
        :options="{
          text: '삭제',
          type: 'danger',
          disabled: !formData.order || !formData.release,
          onClick: removeItem,
        }"
      />
    </dx-toolbar>
    <dx-form 
      class="form-style"
      :form-data="formData" 
      :show-colon-after-label="false" 
      @field-data-changed="onFormDataChange">
      <dx-simple-item
        data-field="order.order_number"
        :editor-options="{
          onPaste: onPasteHandler,
          placeholder: '(QR 코드 스캔 or 찾기)',
          buttons: [
            {name: 'qr', location: 'after', options: { stylingMode: 'text', icon: 'photo', onClick: () => showQrReader = true}},
            {name: 'search', location: 'after', options: { stylingMode: 'text', icon: 'search', onClick: getPopupCb('work-order')}}
          ]
        }">
        <dx-label text="수주번호" />
      </dx-simple-item>
      <dx-simple-item
        css-class="autofill-input"
        data-field="release.release_number"
        :editor-options="{
          placeholder: '(자동 채번)',
          ...generateItemButtonOption('search', getPopupCb('release'))
        }">
        <dx-label text="출하번호" />
      </dx-simple-item>
      <dx-simple-item
        css-class="autofill-input"
        data-field="release.release_date"
        editor-type="dxDateBox"
        :editor-options="{readOnly: true, placeholder: todayText}">
        <dx-label text="출하일자" />
      </dx-simple-item>
      <dx-simple-item
        css-class="autofill-input"
        data-field="release_manager_id"
        editor-type="dxSelectBox"
        :editor-options="{
          dataSource: employeeList,
          displayExpr: 'emp_name',
          valueExpr: 'id',
          readOnly: !formData.order
        }">
        <dx-label text="출고담당자" />
      </dx-simple-item>
      <dx-simple-item
        css-class="autofill-input"
        data-field="work_order.item.item_name"
        :editor-options="{
          readOnly: true
        }">
        <dx-label text="출고품목" />
      </dx-simple-item>
      <dx-simple-item
        css-class="autofill-input"
        data-field="work_order.warehouse_code"
        :editor-options="{readOnly: true}">
        <dx-label text="출고창고" />
      </dx-simple-item>
      <dx-simple-item
        css-class="autofill-input"
        data-field="order.client_company"
        :editor-options="{readOnly: true}">
        <dx-label text="고객업체" />
      </dx-simple-item>
      <dx-simple-item
        css-class="autofill-input"
        data-field="project.project_name"
        :editor-options="{readOnly: true}">
        <dx-label text="프로젝트명" />
      </dx-simple-item>
      <dx-simple-item
        css-class="autofill-input"
        data-field="work_order.required_quantity"
        :editor-options="{readOnly: true}">
        <dx-label text="수주수량" />
      </dx-simple-item>
      <dx-simple-item
        css-class="autofill-input"
        data-field="work_order.request_delivery_date"
        editor-type="dxDateBox"
        :editor-options="{readOnly: true}">
        <dx-label text="요청납기" />
      </dx-simple-item>
      <dx-simple-item
        data-field="release_quantity"
        editor-type="dxNumberBox"
        :editor-options="{
          showSpinButtons: true,
          min: 0, max: formData.order ? formData.work_order.required_quantity : 0,
          readOnly: formState !== 'new' && formState !== 'edit'
        }">
        <dx-label text="출고수량" />
      </dx-simple-item>
    </dx-form>

    <dx-popup
      v-model:visible="popup.show"
      content-template="popup-content"
      title="검색"
      :close-on-outside-click="true"
      :resize-enabled="true">
      <template #popup-content>
        <data-grid-release v-show="popup.type === 'release'" @change="loadItem" />
        <data-grid-work-order-item v-show="popup.type === 'work-order'" :filters="['unproduced_quantity', '>', 0]" @change="loadItem" />
      </template>
    </dx-popup>

    <QrReader v-if="showQrReader" @read="onReadQrData" />
  </div>
</template>

<style lang="scss" scoped>
.mobile-container {
  padding: 10px; margin: 10px;
}
.form-style {
  margin: 10px 0 0;
}
:deep(.autofill-input) .dx-textbox {
  background-color: #ebebeb;
}
</style>