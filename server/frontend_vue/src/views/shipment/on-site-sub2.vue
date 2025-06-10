<script setup>
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar'
import {
  DxForm,
  DxLabel,
  DxSimpleItem,
} from 'devextreme-vue/form'
import { DxPopup } from 'devextreme-vue/popup'
import { DxLoadPanel } from 'devextreme-vue/load-panel'
import DataItem from '@/components/base/data-item.vue'
import DataLend from '@/components/shipment/data-lend.vue'
import { baseEmployee, baseItem } from '@/data-source/base'
import { shipmentLend } from '@/data-source/shipment'
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
const components = {}
const popup = ref({show: false, type: 'lend', filter: null})
const employeeList = ref([])
const formState = ref('init')
const formData = ref({
  id: null,
  created: null,
  lend_number: null,
  lend_date: null,
  lend_manager: null,
  item_code: null,
  quantity: null,
  not_retrieved_quantity: null,
  client_company: null,
  note: null,
  etc: null,
  fk_company_id: null,
  item: null
})
const todayText = moment().format('YYYY-MM-DD')

// token 기간 늘리기
let authtoken = null
const tmk = setInterval(() => { authtoken = authService.token }, 60 * 1000)
onBeforeUnmount(() => { clearInterval(tmk) })

baseEmployee.load({filter: [['fk_company_id', '=', authService.getCompanyId()]], skip: 0, take: 1000})
  .then(({data}) => employeeList.value = data)
  .then(setDefaultManager)

function initialized (key, {component}) {
  components[key] = component
}

function setDefaultManager () {
  const emp = employeeList.value.find(item => item.emp_code === authService.user.user_id)
  if (emp) formData.value.lend_manager = emp.emp_name
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
  formData.value.quantity = 0
  formData.value.not_retrieved_quantity = 0
  formState.value = 'new'
}

function editItem () {
  formState.value = 'edit'
}

async function updateItem () {
  loading.value = true

  try {
    if (!formData.value.id) {
      const updateData = Object.assign({}, formData.value)
      delete updateData.id
      delete updateData.created
      delete updateData.item
      updateData.lend_date = moment().format('YYYY-MM-DD HH:mm:ss')
      updateData.fk_company_id = authService.getCompanyId()
      await shipmentLend.insert(updateData)
      // const { data: insertedData } = await shipmentLend.insert(updateData)
      // formData.value = insertedData
    }
    else {
      await shipmentLend.update(formData.value.id, {
        quantity: formData.value.quantity,
        not_retrieved_quantity: formData.value.not_retrieved_quantity
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

async function removeItem () {
  loading.value = true
  await shipmentLend.remove(formData.value.id)

  clearForm()
  loading.value = false
}

function clearForm () {
  for (const key in formData.value) {
    formData.value[key] = null
  }
  setDefaultManager()
  formState.value = 'init'
}

async function loadItem (item) {
  if (popup.value.type === 'lend') {
    formData.value = item
    formState.value = 'new'
  }
  else if (popup.value.type === 'item') {
    components['form'].beginUpdate()
    clearForm()
    formData.value.item_code = item.item_code
    formData.value.item = item
    components['form'].updateData(formData.value)
    components['form'].endUpdate()
  }
  popup.value.show = false
}

function onPasteHandler ({event}) {
  try {
    const text = event.originalEvent.clipboardData.getData('text')
    const list = text.split('|')
    loadItemData(list[0])
  }
  catch (ex) {
    console.error(ex)
    notifyError('QR정보를 읽어오는데 실패했습니다');
  }
}

function onReadQrData (data) {
  showQrReader.value = false;
  if (!data) notifyError('스캔이 취소됬습니다');
  else {
    const list = data.data.split('|')
    loadItemData(list[0])
  }
}

async function loadItemData (itemCode) {
  const {data: itemData} = await baseItem.load({filter: ['item_code', '=', itemCode]})
  if (itemData.length) {
    components['form'].beginUpdate()
    clearForm()
    formData.value.item_code = itemData[0].item_code
    formData.value.item = itemData[0]
    components['form'].updateData(formData.value)
    components['form'].endUpdate()
    notifyInfo(`${itemCode}를 불러옵니다`);
    newItem()
  }
  else {
    notifyError('품목번호를 조회할 수 없습니다');
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
          disabled: formData.id || formState === 'new',
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
          disabled: !formData.id || formState === 'edit',
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
          disabled: !formData.id,
          onClick: removeItem,
        }"
      />
    </dx-toolbar>
    <dx-form 
      class="form-style"
      :form-data="formData" 
      :show-colon-after-label="false"
      @initialized="(evt) => initialized('form', evt)">
      <dx-simple-item
        css-class="autofill-input"
        data-field="lend_number"
        :editor-options="{
          placeholder: '(자동 채번)',
          ...generateItemButtonOption('search', getPopupCb('lend'))
        }">
        <dx-label text="가출고번호" />
      </dx-simple-item>
      <dx-simple-item
        css-class="autofill-input"
        data-field="lend_date"
        editor-type="dxDateBox"
        :editor-options="{readOnly: true, placeholder: todayText}">
        <dx-label text="가출고일자" />
      </dx-simple-item>
      <dx-simple-item
        css-class="autofill-input"
        data-field="lend_manager"
        editor-type="dxSelectBox"
        :editor-options="{
          dataSource: employeeList,
          displayExpr: 'emp_name',
          valueExpr: 'emp_name',
          readOnly: !formData.order
        }">
        <dx-label text="담당자" />
      </dx-simple-item>
      <dx-simple-item
        data-field="item_code"
        :editor-options="{
          onPaste: onPasteHandler,
          placeholder: '(QR 코드 스캔 or 찾기)',
          buttons: [
            {name: 'qr', location: 'after', options: { stylingMode: 'text', icon: 'photo', onClick: () => showQrReader = true}},
            {name: 'search', location: 'after', options: { stylingMode: 'text', icon: 'search', onClick: getPopupCb('item')}}
          ]
        }">
        <dx-label text="품목번호" />
      </dx-simple-item>
      <dx-simple-item
        css-class="autofill-input"
        data-field="item.item_name"
        :editor-options="{readOnly: true}">
        <dx-label text="출고품목" />
      </dx-simple-item>
      <dx-simple-item
        css-class="autofill-input"
        data-field="item.item_standard"
        :editor-options="{readOnly: true}">
        <dx-label text="규격" />
      </dx-simple-item>
      <dx-simple-item
        data-field="quantity"
        editor-type="dxNumberBox"
        :editor-options="{
          showSpinButtons: true,
          readOnly: formState !== 'new' && formState !== 'edit'
        }">
        <dx-label text="가출고수량" />
      </dx-simple-item>

    </dx-form>

    <dx-popup
      v-model:visible="popup.show"
      content-template="popup-content"
      title="검색"
      :close-on-outside-click="true"
      :resize-enabled="true">
      <template #popup-content>
        <DataLend v-show="popup.type === 'lend'" @change="loadItem" />
        <DataItem v-show="popup.type === 'item'" @change="loadItem" />
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
:deep(.autofill-input) {
  .dx-texteditor-input-container,
  .dx-textbox {
    background-color: #ebebeb;
  }
}
</style>