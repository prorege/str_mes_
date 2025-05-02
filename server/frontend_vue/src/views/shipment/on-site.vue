<script setup>
import OnSiteSub1 from './on-site-sub1.vue'
import OnSiteSub2 from './on-site-sub2.vue'
import OnSiteSub4 from './on-site-sub4.vue'
import {ref} from 'vue'
const tab = ref(0)
</script>

<template>
  <div class="mobile-nav">
    <button type="button" :class="{active: tab === 3}" @click="tab = 3">출고LOT 등록</button>
    <button type="button" :class="{active: tab === 0}" @click="tab = 0">출하등록</button>
    <!-- button type="button" :class="{active: tab === 1}" @click="tab = 1">가출고등록</button -->
    <button type="button" :class="{active: tab === 2}" @click="tab = 2">기타출고등록</button>
  </div>
  <div class="">
    <OnSiteSub1 v-if="tab === 0" />
    <OnSiteSub2 v-if="tab === 1" />
    <OnSiteSub4 v-if="tab === 3" />
  </div>
</template>

<style lang="scss" scoped>
.mobile-nav {
  padding: 12px 12px 0px 12px;
  display: flex;
  justify-content: space-between;

  button {
    width: 45%; height: 40px;
    border: 1px solid #d7d7d7;
    background-color: white;
    &.active {
      background-color: #337ab7;
      color: white;
      font-weight: bold;
    }
  }
}
</style>