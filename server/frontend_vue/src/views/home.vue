<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings fit-height-content">
        <div class="standard-code-container">
          <div class="standard-code-body">

            <div class="standard-code-item pr pb">
              <div class="content-header">
                <dx-toolbar>
                  <dx-item location="before">
                    <div class="content-title">공지사항</div>
                  </dx-item>
                </dx-toolbar>
              </div>

              <dx-data-grid
                class="fixed-header-table"
                height="calc(100% - 40px)"
                :show-borders="true"
                :column-auto-width="true"
                :remote-operations="true"
                :allow-column-resizing="true"
                :hover-state-enabled="true"
                :allow-column-reordering="true"
                :data-source="store.projectNotice"
                @row-click="methods.rowClick"
                @initialized="evt => methods.initialized(evt, 'notice-grid')"
              >
                <dx-column caption="생성시간" data-field="created" data-type="date" format="yyyy-MM-dd" :allow-editing="false" :visible="false" :width="120" />
                <dx-column caption="중요여부" data-field="important" data-type="boolean" :width="80" />
                <dx-column caption="제목" data-field="title" />
                <dx-column caption="공지시작일" data-field="start_date" data-type="date" format="yyyy-MM-dd" :width="100" />
                <dx-column caption="공지종료일" data-field="end_date" data-type="date" format="yyyy-MM-dd" :width="100" />
                <dx-column caption="내용" data-field="content_html" :visible="false" />
                <dx-column caption="최초등록자" data-field="user.user_name" :allow-editing="false" :width="100" />
                <dx-column caption="회사" data-field="fk_company_id" :allow-editing="false" :visible="false" />

                <dx-filter-row :visible="false" />
                <dx-paging :page-size="20" />
              </dx-data-grid>
            </div>

            <div class="standard-code-item pl pb">
              <div class="content-header">
                <dx-toolbar>
                  <dx-item location="before">
                    <div class="content-title">수주 미확정 현황</div>
                  </dx-item>
                </dx-toolbar>
              </div>

              <dx-data-grid
                class="fixed-header-table"
                height="calc(100% - 40px)"
                :show-borders="true"
                :column-auto-width="true"
                :remote-operations="true"
                :hover-state-enabled="true"
                :allow-column-resizing="true"
                :allow-column-reordering="true"
                :data-source="store.orderNotConfirmedItem"
                @cell-dbl-click="methods.orderItemDblClk"
                @initialized="evt => methods.initialized(evt, 'dashboard-not-confirmed-item-grid')"
              >
                <dx-column caption="수주번호" data-field="order.order_number" />
                <dx-column caption="수주일자" data-field="order.order_date" data-type="date" format="yyyy-MM-dd" />
                <dx-column caption="담당자" data-field="order.order_manager" />
                <dx-column caption="품목코드" data-field="item_code" />
                <dx-column caption="품명" data-field="item.item_name" />
                <dx-column caption="수주수량" data-field="order_quantity" data-type="number" format="fixedPoint" />
                <dx-column caption="할당수량" data-field="assign_quantity" data-type="number" format="fixedPoint" />
                <dx-column caption="프로젝트번호" data-field="project_management.project_number" />

                <dx-filter-row :visible="false" />
                <dx-paging :page-size="20" />
              </dx-data-grid>
            </div>
          </div>

          <div class="standard-code-body">
            <div class="standard-code-item pr pt">
              <div class="content-header">
                <dx-toolbar>
                  <dx-item location="before">
                    <div class="content-title">출고요청 미확인 현황</div>
                  </dx-item>
                </dx-toolbar>
              </div>

              <dx-data-grid
                class="fixed-header-table"
                height="calc(100% - 40px)"
                :show-borders="true"
                :column-auto-width="true"
                :remote-operations="true"
                :hover-state-enabled="true"
                :allow-column-resizing="true"
                :allow-column-reordering="true"
                :data-source="store.purchaseOrderPlanItem"
                @cell-dbl-click="methods.purchaseOrderPlanItemDblClk"
                @initialized="evt => methods.initialized(evt,'dashboard-purhcase-order-plan-item-grid')"
              >
                <dx-column caption="생성시간" data-field="created" data-type="date" format="yyyy-MM-dd" :allow-editing="false" :visible="false" />
                <dx-column caption="발주계획번호" data-field="order_plan.order_plan_number" />
                <dx-column caption="계획일자" data-field="order_plan.order_plan_date" data-type="date" format="yyyy-MM-dd" />
                <dx-column caption="담당자" data-field="order_plan.order_plan_manager" />
                <dx-column caption="품목코드" data-field="item_code" />
                <dx-column caption="품명" data-field="item.item_name" />
                <dx-column caption="수량" data-field="order_plan_quantity" data-type="number" format="fixedPoint" />
                <dx-column caption="미발주수량" data-field="unordered_quantity" data-type="number" format="fixedPoint" />
                <dx-column caption="프로젝트번호" data-field="project_management.project_number" />
                <dx-column caption="회사" data-field="fk_company_id" :allow-editing="false" :visible="false" />

                <dx-filter-row :visible="false" />
                <dx-paging :page-size="20" />
              </dx-data-grid>
            </div>

            <div class="standard-code-item pl pt">
              <div class="content-header">
                <dx-toolbar>
                  <dx-item location="before">
                    <div class="content-title">미출고 현황</div>
                  </dx-item>
                </dx-toolbar>
              </div>

              <dx-data-grid
                class="fixed-header-table"
                height="calc(100% - 40px)"
                :show-borders="true"
                :column-auto-width="true"
                :remote-operations="true"
                :hover-state-enabled="true"
                :allow-column-resizing="true"
                :allow-column-reordering="true"
                :data-source="store.orderNotReleaseItem"
                @cell-dbl-click="methods.orderItemDblClk"
                @initialized="evt => methods.initialized(evt,'dashboard-not-release-item-grid')"
              >
                <dx-column caption="수주번호" data-field="order.order_number" />
                <dx-column caption="수주일자" data-field="order.order_date" data-type="date" format="yyyy-MM-dd" />
                <dx-column caption="담당자" data-field="order.order_manager" />
                <dx-column caption="품목코드" data-field="item_code" />
                <dx-column caption="품명" data-field="item.item_name" />
                <dx-column caption="수주수량" data-field="order_quantity" data-type="number" format="fixedPoint" />
                <dx-column caption="미출고수량" data-field="not_shipped" data-type="number" format="fixedPoint" />
                <dx-column caption="프로젝트번호" data-field="project_management.project_number" />

                <dx-filter-row :visible="false" />
                <dx-paging :page-size="20" />
              </dx-data-grid>
            </div>

          </div>
        </div>
      </div>
    </div>

    <dx-popup
      v-model:visible="vars.noticeDetail.visible"
      :width="740"
      :height="540"
      :title="vars.noticeDetail.title"
      :drag-enabled="true"
      :resize-enabled="true"
      :show-close-button="true"
      :close-on-outside-click="true"
      @hiding="methods.popupClose"
      @initialized="evt => methods.initialized(evt, 'notice-detail')"
    >
     <dx-scroll-view width="100%" height="100%">
      <div class="popup-notice" v-html="vars.noticeDetail.context"></div>
    </dx-scroll-view>
    </dx-popup>
  </div>
</template>

<script>
import { reactive } from 'vue';
import { useRouter } from 'vue-router';

import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { DxPopup, DxToolbarItem } from 'devextreme-vue/popup';
import { DxDataGrid, DxColumn, DxPaging, DxFilterRow } from 'devextreme-vue/data-grid';
import { DxScrollView } from 'devextreme-vue/scroll-view';
import { projectNotice } from '@/data-source/project';
import { getShipmentOrderItem } from '@/data-source/shipment';
import { getPurchaseOrderPlanItem } from '@/data-source/purchase';

import authService from '@/auth';
import stateStore from '@/utils/state-store';


export default {
  components: {
    DxToolbar, DxItem,
    DxPopup, DxToolbarItem,
    DxDataGrid, DxColumn, DxPaging, DxFilterRow, DxScrollView,
  },
  setup() {
    const router = useRouter();
    const vars = {},
      store = {},
      methods = {};
    var todayDate = new Date().toISOString().slice(0, 10);
    console.log(todayDate);

    projectNotice.defaultFilters = [
      { name: 'fk_company_id', op: 'eq', val: authService.getCompanyId() },
      { name: 'end_date', op: '>=', val: todayDate },
    ];
    store.projectNotice = projectNotice;

    store.orderNotConfirmedItem = getShipmentOrderItem([
      //{ name: 'order_confirmed', op: 'eq', val: 0 },
      {
        name: 'order',
        op: 'has',
        val: {
          name: 'confirmed',
          op: 'eq',
          val: 0,
        },
      },
    ]);
    store.orderNotReleaseItem = getShipmentOrderItem([
      { name: 'not_shipped', op: 'gt', val: 0 },
    ]);

    store.purchaseOrderPlanItem = getPurchaseOrderPlanItem([
      {
        name: 'order_plan',
        op: 'has',
        val: {
          name: 'fk_company_id',
          op: 'eq',
          val: authService.getCompanyId(),
        },
      },
      { name: 'unordered_quantity', op: 'gt', val: 0 },
    ]);

    vars.components = {};
    vars.noticeDetail = reactive({
      visible: false,
      title: '',
      context: '',
    });

    methods.initialized = (evt, key) => {
      vars.components[key] = evt.component;
      stateStore.bind(key, evt.component);
    };
    methods.rowClick = evt => {
      vars.noticeDetail.title = evt.data.title;
      vars.noticeDetail.context = evt.data.content_html;
      vars.noticeDetail.visible = true;
    };
    methods.popupClose = () => {
      vars.noticeDetail.title = '';
      vars.noticeDetail.context = '';
    };
    methods.orderItemDblClk = ({ column, data }) => {
      router.replace({
        path: `/shipment/order/${data.order.id}`,
      });
    };
    methods.purchaseOrderPlanItemDblClk = ({ column, data }) => {
      router.replace({ path: `/purchase/order-plan/${data.order_plan.id}` });
    };

    return { vars, store, methods };
  },
};
</script>

<style lang="scss">
.standard-code-container {
  height: calc(100vh - 120px);
}
.standard-code-body {
  display: flex;
  flex-wrap: nowrap;
  height: 50%;
}
.standard-code-item {
  width: 50%;
}
.pl {
  padding-left: 10px;
}
.pr {
  padding-right: 10px;
}
.pt {
  padding-top: 10px;
}
.pb {
  padding-bottom: 10px;
}
</style>
