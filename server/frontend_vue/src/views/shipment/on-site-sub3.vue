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
import DataStockEtcItem from '@/components/stock/data-stock-etc-item.vue'
import { baseEmployee, baseItem, baseWarehouse, baseDepartment } from '@/data-source/base'
import { stockEtc, stockEtcItem } from '@/data-source/stock';
import { projectRegistration } from '@/data-source/project';
import QrReader from '@/components/qr/reader'
import {
  generateItemButtonOption
} from '@/utils/util'
import authService from '@/auth'
import { notifyInfo, notifyError } from '@/utils/notify'
import {ref, onBeforeUnmount} from 'vue'
import moment from 'moment'

const loading = ref(true)
const showQrReader = ref(false)
const components = {}
const userName = authService.user.user_name
const popup = ref({show: false, type: 'lend', filter: null})
const warehouseList = ref([])
const projectList = ref([])
const formState = ref('init')
const formData = ref({
  id: null,
  created: null,
  type: null,
  item_code: null,
  quantity: null,
  unit_price: null,
  supply_price: null,
  warehouse_code: null,
  inout_type: null,
  project_number: null,
  note: null,
  fk_stock_etc_id: null,
  stock_etc: { manager: userName },
  item: null,
  warehouse: null,
  basic_stock: null
})
const todayText = moment().format('YYYY-MM-DD')
let empInfo = undefined

// token 기간 늘리기
let authtoken = null
const tmk = setInterval(() => { authtoken = authService.token }, 60 * 1000)
onBeforeUnmount(() => { clearInterval(tmk) })

const options = {skip: 0, take: 1,
  filter: [
    ['emp_code', '=', authService.user.user_id],
    'and',
    ['fk_company_id', '=', authService.getCompanyId()]
  ]
}

baseEmployee.load(options)
  .then(({data}) => {
    if (data.length) empInfo = data[0]
    else return Promise.reject()
  })
  .then(() => baseDepartment.byKey(empInfo.fk_department_id))
  .then(({data}) =>  empInfo.department = data)
  .then(() => baseWarehouse.load({filter: ['fk_company_id', '=', authService.getCompanyId()], skip: 0, take: 1000}))
  .then(({data}) => (warehouseList.value = data))
  .then(() => projectRegistration.load({filter: ['fk_company_id', '=', authService.getCompanyId()], skip: 0, take: 1000}))
  .then(({data}) => (projectList.value = data))
  .then(() => { loading.value = false })
  .catch(() => ( loading.value = false ))

function initialized (key, {component}) {
  components[key] = component
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
  formData.value.inout_type = '기타출고'
  formData.value.type = '출고'
  formData.value.quantity = 0
  formData.value.stock_etc = {
    manager: userName,
    department: empInfo
  }
  formState.value = 'new'
}

function editItem () {
  formState.value = 'edit'
}

async function updateItem () {
  if (!formData.value.item_code) {
    notifyError('품목을 선택해 주세요')
    return
  }

  components['form'].beginUpdate()
  try {
    if (!formData.value.id) {
      const {data: stockEtcData} = await stockEtc.insert({
        target_date: moment().format('YYYY-MM-DD HH:mm:ss'),
        department: empInfo.department.department_name,
        manager: formData.value.stock_etc.manager,
        note: '', etc: '',
        fk_company_id: authService.getCompanyId()
      })

      const updateData = Object.assign({}, formData.value)
      delete updateData.id
      delete updateData.created
      delete updateData.item
      delete updateData.stock_etc
      delete updateData.warehouse
      delete updateData.basic_stock
      updateData.fk_stock_etc_id = stockEtcData.id
      await stockEtcItem.insert(updateData)
    }
    else {
      await stockEtcItem.update(formData.value.id, {
        quantity: formData.value.quantity
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
    components['form'].endUpdate()
  }
}

async function removeItem () {
  loading.value = true
  await stockEtcItem.remove(formData.value.id)

  clearForm()
  loading.value = false
}

function clearForm () {
  for (const key in formData.value) {
    formData.value[key] = null
  }
  components['form'].resetValues()
  formState.value = 'init'
}

async function loadItem (item) {
  if (popup.value.type === 'stock') {
    formData.value = item
    formState.value = 'new'
  }
  else if (popup.value.type === 'item') {
    clearForm()
    formData.value.item_code = item.item_code
    formData.value.item = item
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
  <dx-load-panel v-model:visible="loading" :show-pane="true" />
  <div class="mobile-container back-colored" v-if="!loading">
    
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
        data-field="stock_etc.number"
        :editor-options="{
          placeholder: '(자동 채번)',
          ...generateItemButtonOption('search', getPopupCb('stock'))
        }">
        <dx-label text="기타출고번호" />
      </dx-simple-item>
      <dx-simple-item
        css-class="autofill-input"
        data-field="stock_etc.target_date"
        editor-type="dxDateBox"
        :editor-options="{readOnly: true, placeholder: todayText}">
        <dx-label text="기타출고일자" />
      </dx-simple-item>
      <dx-simple-item
        css-class="autofill-input"
        data-field="stock_etc.manager"
        :editor-options="{
          readOnly: true
        }">
        <dx-label text="담당자" />
      </dx-simple-item>
      <dx-simple-item
        data-field="warehouse_code"
        editor-type="dxSelectBox"
        :editor-options="{
          dataSource: warehouseList,
          displayExpr: 'wh_name',
          valueExpr: 'wh_code',
          readOnly: formState !== 'new' && formState !== 'edit'
        }">
        <dx-label text="출고창고" />
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
        <dx-label text="출고수량" />
      </dx-simple-item>
      <dx-simple-item
        data-field="fk_project_management_id"
        editor-type="dxSelectBox"
        :editor-options="{
          dataSource: projectList,
          displayExpr: 'project_number',
          valueExpr: 'id',
          readOnly: formState !== 'new' && formState !== 'edit'
        }">
        <dx-label text="프로젝트번호" />
      </dx-simple-item>
      <dx-simple-item
        css-class="autofill-input"
        data-field="inout_type"
        :editor-options="{readOnly: true}">
        <dx-label text="입출고유형" />
      </dx-simple-item>
      <dx-simple-item
        css-class="autofill-input"
        data-field="type"
        :editor-options="{readOnly: true}">
        <dx-label text="입출고구분" />
      </dx-simple-item>

    </dx-form>

    <dx-popup
      v-model:visible="popup.show"
      content-template="popup-content"
      title="검색"
      :close-on-outside-click="true"
      :resize-enabled="true">
      <template #popup-content>
        <DataStockEtcItem v-show="popup.type === 'stock'" :filter="[{name: 'inout_type', op: 'eq', val: '기타출고'},{name: 'type', op: 'eq', val: '출고'}]" @change="loadItem" />
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