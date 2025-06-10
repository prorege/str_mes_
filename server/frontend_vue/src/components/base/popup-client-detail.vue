<template>
    <dx-scroll-view width="100%" height="100%">
    <dx-form
        :col-count="1"
        :form-data="vars.clientFormData"
        :show-colon-after-label="false"
        :read-only="true"
        >
        <dx-group-item :col-count="2" css-class="pa-4">
            <dx-simple-item data-field="alias">
            <dx-label text="업체약칭" />
            </dx-simple-item>
            <dx-simple-item data-field="corp_number" :editor-options="{ mask: '000000 - 0000000' }">
            <dx-label text="법인번호" />
            </dx-simple-item>

            <dx-simple-item data-field="name">
            <dx-label text="정식상호" />
            </dx-simple-item>
            <dx-group-item :col-count="5">
            <dx-simple-item :col-span="4" data-field="business_number" :editor-options="{ mask: '000 - 00 - 00000' }">
                <dx-label text="사업자번호" />
            </dx-simple-item>
            <dx-simple-item :col-span="1" data-field="zero_tax_rate_yn">
                <dx-label text="영세율" />
            </dx-simple-item>
            </dx-group-item>

            <dx-simple-item data-field="address">
            <dx-label text="주소" />
            </dx-simple-item>
            <dx-simple-item data-field="ceo_name">
            <dx-label text="대표자명" />
            </dx-simple-item>

            <dx-group-item :col-count="2">
            <dx-simple-item data-field="address_detail">
                <dx-label text="상세주소" />
            </dx-simple-item>
            <dx-simple-item data-field="zip_code">
                <dx-label text="우편번호" />
            </dx-simple-item>
            </dx-group-item>
            <dx-simple-item data-field="business_status">
            <dx-label text="업태" />
            </dx-simple-item>

            <dx-simple-item data-field="phone">
            <dx-label text="대표전화번호" />
            </dx-simple-item>
            <dx-simple-item data-field="business_sector">
            <dx-label text="종목" />
            </dx-simple-item>

            <dx-simple-item data-field="fax">
            <dx-label text="팩스번호" />
            </dx-simple-item>
            <dx-simple-item data-field="name_en">
            <dx-label text="업체명(영문)" />
            </dx-simple-item>

            <dx-simple-item data-field="email">
            <dx-label text="대표 이메일" />
            </dx-simple-item>
            <dx-simple-item data-field="ceo_name_en">
            <dx-label text="대표자명(영문)" />
            </dx-simple-item>

            <dx-simple-item data-field="homepage">
            <dx-label text="홈페이지" />
            </dx-simple-item>
            <dx-simple-item data-field="phone_en">
            <dx-label text="전화번호(국제)" />
            </dx-simple-item>

            <dx-simple-item data-field="bill_manager">
            <dx-label text="계산서 담당자" />
            </dx-simple-item>
            <dx-simple-item data-field="fax_en">
            <dx-label text="팩스번호(국제)" />
            </dx-simple-item>

            <dx-simple-item data-field="bill_email">
            <dx-label text="계산서 이메일" />
            </dx-simple-item>
            <dx-simple-item data-field="address_en">
            <dx-label text="주소(영문)" />
            </dx-simple-item>

            <dx-group-item :col-count="2">
            <dx-simple-item data-field="client_type">
                <dx-label text="업체분류" />
            </dx-simple-item>
            <dx-simple-item data-field="district_type">
                <dx-label text="지역구분" />
            </dx-simple-item>
            </dx-group-item>
            <dx-simple-item data-field="etc" 
            :editor-options="generateItemButtonOption(
                'rename',
                methods.createPopupFn('etc', '비고')
            )">
            <dx-label text="비고" />
            </dx-simple-item>

            <dx-group-item :col-count="2">
            <dx-simple-item data-field="manager">
                <dx-label text="당사담당자" />
            </dx-simple-item>
            <dx-simple-item data-field="trade_yn">
                <dx-label text="거래중지" />
            </dx-simple-item>
            </dx-group-item>
            <dx-group-item :col-count="2">
            <dx-simple-item data-field="register_id">
                <dx-label text="최초등록자" />
            </dx-simple-item>
            <dx-simple-item data-field="created">
                <dx-label text="최초등록일자" />
            </dx-simple-item>
            </dx-group-item>

            <dx-group-item :col-count="2">
            <dx-simple-item data-field="before_alias">
                <dx-label text="변경전 업체약칭" />
            </dx-simple-item>
            <dx-simple-item data-field="after_alias">
                <dx-label text="변경후 업체약칭" />
            </dx-simple-item>
            </dx-group-item>
            <dx-group-item :col-count="2">
            <dx-simple-item data-field="modify_id">
                <dx-label text="최종수정자" />
            </dx-simple-item>
            <dx-simple-item data-field="last_updated_date">
                <dx-label text="최종수정일자" />
            </dx-simple-item>
            </dx-group-item>
            <dx-group-item :col-span="2">
                <dx-data-grid
                class="fixed-header-table"
                height="100%"
                column-resizing-mode="widget"
                :data-source="vars.clientManager"
                :remote-operations="true"
                :show-borders="true"
                :allow-column-resizing="true"
                :column-auto-width="true"
                :select-text-on-edit-start="true"
                @initialized="evt => methods.initialized(evt, 'popup-client-manager')"
              >
                <dx-column caption="거래처담당자" data-field="name"  :visible="true" />
                <dx-column caption="부서" data-field="department"  :visible="true" />
                <dx-column caption="직급" data-field="position"  :visible="true" />
                <dx-column caption="휴대폰번호" data-field="mobile"  :visible="true" />
                <dx-column caption="이메일주소" data-field="email"  :visible="true" />
                <dx-column caption="직통전화번호" data-field="direct_phone"  :visible="true" />
                <dx-column caption="내선번호" data-field="ext_phone" :visible="true" />
                <dx-column caption="비고" data-field="etc"  :visible="true" />
                <dx-column caption="거래처 ID" data-field="fk_client_id" :visible="false" />
                <dx-paging :page-size="20" />
              </dx-data-grid>
            </dx-group-item>
        </dx-group-item>
     </dx-form>
    </dx-scroll-view> 
    
</template>
<script>
import { DxPopup } from 'devextreme-vue/popup';
import { DxScrollView } from 'devextreme-vue/scroll-view';
import {
  DxForm,
  DxTab,
  DxLabel,
  DxGroupItem,
  DxSimpleItem,
  DxTabbedItem,
  DxTabPanelOptions,
} from 'devextreme-vue/form';
import {
  DxDataGrid,
  DxColumn,
  DxPaging,
  DxExport,
  DxColumnChooser,
  DxFilterRow,
  DxEditing,
} from 'devextreme-vue/data-grid';
import { DxButton } from 'devextreme-vue/button';
import { baseClient, getBaseClientManager } from '@/data-source/base';
import authService from '../../auth';
import ApiService from '../../utils/api-service';
import { notifyError } from '../../utils/notify';
import stateStore from '@/utils/state-store';
import { ref, reactive, nextTick, watch, onMounted } from 'vue';
import { generateItemButtonOption } from '../../utils/util';
export default {
    components: {
        DxPopup,
        DxScrollView,
        DxForm,
        DxTab,
        DxLabel,
        DxGroupItem,
        DxSimpleItem,
        DxTabbedItem,
        DxTabPanelOptions,
        DxDataGrid,
        DxColumn,
        DxPaging,
        DxExport,
        DxColumnChooser,
        DxFilterRow,
        DxEditing,
    },
    props: {
        clientName: [String],
    },
    setup(props){
        onMounted(async () => {
            methods.initById(props.clientName);
        });
        const vars = {};

        vars.clientFormData = reactive({});

        vars.clientManager = getBaseClientManager([{ name: 'fk_client_id', op: 'eq', val: 0 }])
        const components = {};

        const methods = {
            async initById(clientName){
                if (!clientName) return;
                const { data } = await baseClient.load({
                    filter: [
                        ['name', '=', clientName]
                    ],
                });
                Object.assign(vars.clientFormData, data[0]);
        
                vars.clientManager.defaultFilters[0].val = data[0].id;
      
                if (components['popup-client-manager']) components['popup-client-manager'].refresh();
                
            },
            initialized(evt, key){
                components[key] = evt.component;
            },
            createPopupFn(key, title, data = null) {
                const _key = key, _title = title, _data = data;
                return () => {
                    vars.dlg.key = _key;
                    vars.dlg.data = _data;
                    vars.dlg.title = _title;
                    vars.dlg.show = true;
                };
            },
        }
        watch(
            () => props.clientName,
            () => methods.initById(props.clientName)
        );

        return {
            vars, methods, generateItemButtonOption, 
        }
    }
}
</script>