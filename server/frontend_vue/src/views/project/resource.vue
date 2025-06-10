<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings">
        <div class="content-header">
          <dx-toolbar>
            <dx-item location="before">
              <div class="content-title">자료등록</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <dx-file-manager
          :file-system-provider="ds.remoteProvider"
          :on-selected-file-opened="vars.displayImagePopup"
          height="calc(100vh - 148px)">
          <dx-permissions
            :create="true"
            :copy="true"
            :move="true"
            :delete="true"
            :rename="true"
            :upload="true"
            :download="true"
          />

          <dx-file-toolbar>
            <dx-file-item name="create" text="새폴더" />
            <dx-file-item name="upload" text="업로드" />
            <dx-file-item name="refresh" text="새로고침" />
            <dx-file-selection-item name="download" text="다운로드" />
            <dx-file-selection-item name="separator" />
            <dx-file-selection-item name="move" text="이동" />
            <dx-file-selection-item name="copy" text="복사" />
            <dx-file-selection-item name="rename" text="이름변경" />
            <dx-file-selection-item name="delete" text="삭제" />
            <dx-file-selection-item name="clearSelection" text="선택취소" />
          </dx-file-toolbar>

          <dx-item-view>
            <dx-details>
              <dx-column data-field="name" caption="파일명"/>
              <dx-column data-field="dateModified" caption="최종수정일"/>
              <dx-column data-field="size" caption="크기"/>
            </dx-details>
          </dx-item-view>
        </dx-file-manager>

      </div>
    </div>

    <dx-popup
      :close-on-outside-click="true"
      v-model:visible="vars.popupVisible"
      v-model:title="vars.imageItemToDisplay.name"
      max-height="600"
      class="photo-popup-content">
      <img
        :src="vars.imageItemToDisplay.url"
        class="photo-popup-image"
      />
    </dx-popup>

  </div>
</template>

<script>
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxFileManager, DxPermissions, DxToolbar as DxFileToolbar, DxItem as DxFileItem, DxFileSelectionItem, DxItemView, DxDetails, DxColumn, } from 'devextreme-vue/file-manager';
import { DxPopup } from 'devextreme-vue/popup';
import RemoteFileSystemProvider from 'devextreme/file_management/remote_provider';

const remoteProvider = new RemoteFileSystemProvider({
  endpointUrl: '/api/mes/v1/project/file_manager'
});

export default {
  components: {
    DxToolbar, DxItem, 
    DxFileManager, DxPermissions, DxFileToolbar, DxFileItem, DxFileSelectionItem,
    DxItemView, DxDetails, DxColumn,
    DxPopup
  },
  setup() {
    const vars = {}, methods = {}, ds = {}

    // Vars
    vars.components = {}
    vars.imageItemToDisplay = {}
    vars.popupVisible = false

    // DataSources
    ds.remoteProvider = remoteProvider

    methods.displayImagePopup = (evt) => {
      vars.imageItemToDisplay = {
        name: evt.file.name,
        url: evt.file.dataItem.url,
      };
      vars.popupVisible = true
    }

    return {
      vars, methods, ds
    };
  },
};
</script>