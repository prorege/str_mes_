<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        <div class="content-header">
          <T.DxToolbar class="back-colored">
            <T.DxItem location="before">
              <div class="content-title">측정장비등록</div>
            </T.DxItem>
          </T.DxToolbar>
        </div>
      </div>

      <div class="dx-card responsive-paddings mt-1">
        <G.DxDataGrid
          height="calc(100vh - 200px)"
          column-resizing-mode="widget"
          :data-source="qualityMeasuringEquipment"
          :show-borders="true"
          :column-auto-width="true"
          :remote-operations="true"
          :allow-column-reordering="true"
          :allow-column-resizing="true"
          :row-alternation-enabled="true"
          @initialized="evt => initialized(evt, 'status-list')"
          @init-new-row="editingStart"
          @editing-start="editingStart"
          @edit-canceled="editCanceled"
          @saving="saving"
          @saved="saved"
        >
          <G.DxColumn caption="장비코드" data-field="equipment_code" :filter-operations="['contains', '=']">
            <G.DxRequiredRule message="장비코드를 입력해 주세요" />
            <G.DxAsyncRule :validation-callback="checkEquipmentCode" />
          </G.DxColumn>
          <G.DxColumn caption="장비명" data-field="equipment_name" />
          <G.DxColumn caption="제조원" data-field="manufacturer" />
          <G.DxColumn caption="구입일자" data-field="purchase_date" data-type="date" format="yyyy-MM-dd" sort-order="desc" />
          <G.DxColumn caption="교정기한" data-field="correction_date" data-type="date" format="yyyy-MM-dd" />
          <G.DxColumn caption="교정주기" data-field="correction_interval" />
          <G.DxColumn caption="알람기준일" data-field="alarm_date" />
          <G.DxColumn caption="모델명" data-field="model_name" />
          <G.DxColumn caption="시리얼번호" data-field="serial_number" />
          <G.DxColumn caption="적요" data-field="note" />

          <G.DxColumn caption="첨부파일" name="file_attachments" cell-template="fileUpload" />
          <G.DxColumn caption="교정성적서" name="file_correction" cell-template="fileUpload" />
          <G.DxColumn caption="구매증빙서" name="file_receipt" cell-template="fileUpload" />

          <G.DxEditing mode="row"
            :use-icons="true"
            :allow-updating="true"
            :allow-adding="true"
            :allow-deleting="true"
            v-model:edit-row-key="editRowKey"
          />
          <G.DxPaging :page-size="20" />
          <G.DxFilterRow :visible="true" />

          <template #fileUpload="{data}">
            <div class="file-upload-wrap">
              <a href="javascript:void(0)" @click="uploadAttachments(data)" v-if="data.key === editRowKey">업로드</a>
              <a href="javascript:void(0)" :class="{disabled: !data.data[data.column.name]}" @click="downloadAttachments(data)" v-else>다운로드</a>
            </div>
          </template>
        </G.DxDataGrid>
      </div>
    </div>
    <input type="file" ref="fileInput" @change="fileChangeHandler" />
  </div>
</template>

<script setup>
import * as G from 'devextreme-vue/data-grid';
import * as T from 'devextreme-vue/toolbar';
import {downloadFile} from '../../utils/download-file'
import ApiService from '../../utils/api-service';
import {qualityMeasuringEquipment} from '../../data-source/quality';
import {ref} from 'vue'
import { notifyInfo } from '../../utils/notify';

const components = {};
const fileInput = ref();
const editRowKey = ref();
const fileUploadService = new ApiService('/api/mes/v1/quality/measuring_equipment_upload');
const uploadFiles = {}
let uploadClickedContent = null

function initialized (evt, key) {
  components[key] = evt.component;
}

async function checkEquipmentCode ({value}) {
  const {totalCount} = await qualityMeasuringEquipment.load({filter: ['equipment_code', '=', value]})
  if (totalCount) throw Error('존재하는 장비코드 입니다')
  return
}

function editingStart ({component, data}) {
  if (data.id) component.columnOption('equipment_code', 'allowEditing', false)
  else component.columnOption('equipment_code', 'allowEditing', true)
}

function editCanceled () {
  uploadClickedContent = null
  for (const key in uploadFiles) {
    uploadFiles[key] = null
    delete uploadFiles[key]
  }
}

function saving (evt) {
  const uploadFileKeys = Object.keys(uploadFiles)
  if (evt.changes.length && evt.changes[0].type === 'remove') {
    evt.promise = new Promise((resolve, reject) => {
      const formData = new FormData()
      formData.append('key', evt.changes[0].key)
      formData.append('type', 'remove')
      fileUploadService.post('', formData)
        .then(() => resolve(false))
        .catch((err) => reject(err))
    })
  }
  if (uploadFileKeys.length) {
    evt.promise = new Promise((resolve, reject) => {
      const formData = new FormData()

      if (!evt.changes.length) {
        evt.changes.push({data: {}, key: editRowKey.value, type: 'update'})
      }

      if (evt.changes[0].type !== 'insert') formData.append('key', evt.changes[0].key)
      formData.append('type', evt.changes[0].type)

      for (const key of uploadFileKeys) {
        formData.append(key, uploadFiles[key])
      }

      fileUploadService.post('', formData)
        .then(({data}) => {
          for (const key in data) evt.changes[0].data[key] = data[key]
          console.log(evt.changes[0])
          resolve(false)
        })
        .catch((err) => reject(err))
    })
  }
}

function saved (evt) {
  editCanceled()
}

function downloadAttachments ({column, data}) {
  if (!data[column.name]) return
  downloadFile(
    `/api/mes/v1/quality/quality_management_download/${data[column.name]}`
  );
}

function uploadAttachments ({column}) {
  uploadClickedContent = column.name
  fileInput.value.value = ''
  fileInput.value.click()
}

async function fileChangeHandler ({target}) {
  if (!uploadClickedContent) {
    fileInput.value.value = ''
    return
  }
  
  if (target.files[0]) {
    uploadFiles[uploadClickedContent] = target.files[0]
    notifyInfo(`${target.files[0].name} 파일이 선택되었습니다`)
  }
  else if (uploadFiles[uploadClickedContent]) {
    notifyInfo(`${uploadFiles[uploadClickedContent].name} 파일이 취소되었습니다`)
    uploadFiles[uploadClickedContent] = null
    delete uploadFiles[uploadClickedContent]
  }
}

</script>

<style lang="scss" scoped>
.file-upload-wrap {
  text-align: center;
  > a {
    display: inline-block;
    font-size: 12px;
    text-decoration: none;
    padding: 0 10px;
    border: 1px solid #337ab7;
    &:hover:not(.disabled) { 
      color: white;
      background-color: #337ab7; 
    }
    &.disabled {
      opacity: 0.4;
      cursor: not-allowed;
    }
  }
}
</style>