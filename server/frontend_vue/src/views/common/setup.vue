<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings">
        
        <div class="content-header">
          <dx-toolbar>
            <dx-item location="before">
              <div class="content-title">셋업관리</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <dx-tab-panel>
          <dx-item title="사용자관리" icon="user">
            <template #default>
              <div class="tab-setup">
                <setup-user />
              </div>
            </template>
          </dx-item>
          <dx-item title="기초재고관리" icon="cart">
            <template #default>
              <div class="tab-setup">
                <setup-stock />
              </div>
            </template>
          </dx-item>
          <dx-item title="기초잔액관리" icon="money">
            <template #default>
              <div class="tab-setup">
                <setup-balance />
              </div>
            </template>
          </dx-item>
          <dx-item title="자동채번관리" icon="bulletlist">
            <template #default>
              <div class="tab-setup">
                <setup-numbering />
              </div>
            </template>
          </dx-item>
          <dx-item title="년도별 원가 구성 요율관리" icon="percent">
            <template #default>
              <div class="tab-setup">
                <setup-produce-cost />
              </div>
            </template>
          </dx-item>
          <dx-item title="통제관리" icon="toolbox">
            <template #default>
              <div class="tab-setup">
                <setup-control />
              </div>
            </template>
          </dx-item>
          <dx-item title="판관비관리" icon="percent">
            <template #default>
              <div class="tab-setup">
                <setup-sga-expense />
              </div>
            </template>
          </dx-item>
        </dx-tab-panel>

      </div>
    </div>
  </div>
</template>

<script>
import DxTabPanel, { DxItem } from 'devextreme-vue/tab-panel';
import DxToolbar from 'devextreme-vue/toolbar';

import SetupUser from './setup-user.vue';
import SetupStock from './setup-stock.vue';
import SetupBalance from './setup-balance.vue';
import SetupNumbering from './setup-numbering.vue';
import setupProduceCost from './setup-produce-cost.vue';
import setupControl from './setup-control.vue';
import setupSgaExpense from './setup-sga-expense.vue';

export default {
  components: {
    DxTabPanel,
    DxItem,
    DxToolbar,
    SetupUser,
    SetupStock,
    SetupBalance,
    SetupNumbering,
    setupProduceCost,
    setupControl,
    setupSgaExpense
  },
  setup() {
    return {};
  },
};
</script>

<style>
.tab-setup {
  padding: 8px;
}
</style>
