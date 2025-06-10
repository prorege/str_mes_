<script setup>
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar'
import {
  DxForm,
  DxLabel,
  DxSimpleItem,
} from 'devextreme-vue/form'
import { DxDataGrid, DxColumn, DxPaging, DxFilterRow } from 'devextreme-vue/data-grid'
import { DxPopup } from 'devextreme-vue/popup'
import { DxLoadPanel } from 'devextreme-vue/load-panel'
import { getShipmentReleaseItem } from '@/data-source/shipment'
import {
  generateItemButtonOption
} from '@/utils/util'
import authService from '@/auth'
import { notifyInfo, notifyError } from '@/utils/notify'
import {ref, onBeforeUnmount} from 'vue'
import moment from 'moment'

const loading = ref(false)
const components = {}
const shipmentReleaseItem = getShipmentReleaseItem()
const popup = ref({show: false, type: 'lend', filter: null})
const formState = ref('init')
const formData = ref({ id: null, lot_number: null })
const todayText = moment().format('YYYY-MM-DD')
let empInfo = undefined

// token 기간 늘리기
let authtoken = null
const tmk = setInterval(() => { authtoken = authService.token }, 60 * 1000)
onBeforeUnmount(() => { clearInterval(tmk) })

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

async function onRowClick ({ data }) {
  popup.value.show = false
  formData.value.id = data.id
  components['form'].updateData('release.release_number', data.release.release_number)
  components['form'].updateData('release.release_date', data.release.release_date)
  components['form'].updateData('release.client_company', data.release.client_company)
  components['form'].updateData('item_code', data.item_code)
  components['form'].updateData('item.item_name', data.item.item_name)
  components['form'].updateData('release_quantity', data.release_quantity)
  components['form'].updateData('lot_number', data.lot_number)

  const elm = document.querySelector('#lot-number-input input')
  if (elm) {
    elm.focus()
    elm.select()
  }
}

async function updateItem () {
  if (!formData.value.id) {
    notifyError('출고 품목을 선택해 주세요')
    return
  }

  if (!formData.value.lot_number) {
    notifyError('생산주차를 적어주세요')
    return
  }

  notifyInfo(`ID: ${formData.value.id}, 생산주차: ${formData.value.lot_number}`)

  try {
    await shipmentReleaseItem.update(formData.value.id, {
      lot_number: formData.value.lot_number
    })

    notifyInfo('저장되었습니다')
    clearForm()
  }
  catch (ex) {
    console.error(ex)
    notifyError('저장 중 문제가 발생하였습니다')
  }
}

function clearForm () {
  for (const key in formData.value) {
    formData.value[key] = null
  }
  if (components['form']) components['form'].resetValues()
  if (components['grid']) components['grid'].refresh()
  formState.value = 'init'
}

function onPasteHandler ({event}) {
  try {
    const text = event.originalEvent.clipboardData.getData('text')
    event.preventDefault()
    const list = text.split('|')
    if (!list[2]) return
    let value = formData.value.lot_number || ''
    value += list[2]
    components['form'].updateData('lot_number', value)
  }
  catch (ex) {
    console.error(ex)
    notifyError('QR정보를 읽어오는데 실패했습니다');
  }
}

function onTextBoxInput(e){
    const currentInput = e.event.target.value;
    if(!currentInput) return
    components['form'].updateData('lot_number', currentInput)
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
          text: '저장',
          type: 'success',
          disabled: !formData.id || !formData.lot_number,
          onClick: updateItem,
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
        data-field="release.release_number"
        :editor-options="{
          readOnly: true,
          ...generateItemButtonOption('search', getPopupCb('stock'), 'after', {}, { disabled: false })
        }">
        <dx-label text="출고번호" />
      </dx-simple-item>
      <dx-simple-item
        css-class="autofill-input"
        data-field="release.release_date"
        editor-type="dxDateBox"
        :editor-options="{readOnly: true, placeholder: todayText}">
        <dx-label text="출고일자" />
      </dx-simple-item>
      <dx-simple-item
        css-class="autofill-input"
        data-field="release.client_company"
        :editor-options="{
          readOnly: true
        }">
        <dx-label text="고객업체" />
      </dx-simple-item>
      <dx-simple-item
        data-field="item_code"
        :editor-options="{
          readOnly: true
        }">
        <dx-label text="품목번호" />
      </dx-simple-item>
      <dx-simple-item
        css-class="autofill-input"
        data-field="item.item_name"
        :editor-options="{readOnly: true}">
        <dx-label text="품명" />
      </dx-simple-item>
      
      <dx-simple-item
        data-field="release_quantity"
        editor-type="dxNumberBox"
        :editor-options="{
          format: ',##0.###',
          readOnly: true
        }">
        <dx-label text="출고수량" />
      </dx-simple-item>

      <dx-simple-item
        data-field="lot_number"
        :editor-options="{
          readOnly: !formData.id,
          elementAttr: { id: 'lot-number-input' },
          showClearButton: true,
          onPaste: onPasteHandler,
          onInput: onTextBoxInput,
        }">
        <dx-label text="생산주차" />
      </dx-simple-item>
    </dx-form>

    <dx-popup
      v-model:visible="popup.show"
      content-template="popup-content"
      title="검색"
      :close-on-outside-click="true"
      :resize-enabled="true">
      <template #popup-content>
        <dx-data-grid
          :data-source="shipmentReleaseItem"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          @initialized="(evt) => initialized('grid', evt)"
          @row-click="onRowClick"
        >
          <dx-column caption="출고번호" data-field="release.release_number" :sort-index="1" sort-order="desc" />
          <dx-column caption="출고일자" data-field="release.release_date" data-type="date" format="yyyy-MM-dd" :sort-index="0" sort-order="desc" />
          <dx-column caption="고객업체" data-field="release.client_company" />
          <dx-column caption="품명" data-field="item.item_name" />
          <dx-column caption="출고수량" data-field="release_quantity" data-type="number" />

          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
        </dx-data-grid>
      </template>
    </dx-popup>
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