<template>
  <dx-scroll-view height="100%" width="100%" class="single-card">
    <slot></slot>
  </dx-scroll-view>
</template>

<script>
import DxScrollView from "devextreme-vue/scroll-view"

export default {
  components: {
    DxScrollView
  },
  setup() {

  }
};
</script>

<style lang="scss" scoped>
@import "../themes/generated/variables.base.scss";

.single-card {
  width: 100%;
  height: 100%;
}
</style>
