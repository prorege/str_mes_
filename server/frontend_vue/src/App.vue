<template>
  <div id="root">
    <div :class="cssClasses">
      <component
        :is="$route.meta.layout"
        :title="title"
        :is-x-small="screen.getScreenSizeInfo.isXSmall"
        :is-large="screen.getScreenSizeInfo.isLarge"
      >
        <div class="content">
          <router-view></router-view>
        </div>
      </component>
    </div>
  </div>
</template>

<script>
import { sizes, subscribe, unsubscribe } from './utils/media-query';
import {
  getCurrentInstance,
  reactive,
  onMounted,
  onBeforeUnmount,
  computed,
} from 'vue';

//Add the '.dx-swatch-additional' class to the container to apply swatch styles to its nested elements.

function getScreenSizeInfo() {
  const screenSizes = sizes();

  return {
    isXSmall: screenSizes['screen-x-small'],
    isLarge: screenSizes['screen-large'],
    cssClasses: Object.keys(screenSizes).filter(cl => screenSizes[cl]),
  };
}

export default {
  setup() {
    const vm = getCurrentInstance();

    const title = vm.proxy.$appInfo.title;
    const screen = reactive({ getScreenSizeInfo: {} });
    screen.getScreenSizeInfo = getScreenSizeInfo();

    function screenSizeChanged() {
      screen.getScreenSizeInfo = getScreenSizeInfo();
    }

    onMounted(() => {
      document.body.classList.remove('kiosk-view')
      subscribe(screenSizeChanged);
    });

    onBeforeUnmount(() => {
      unsubscribe(screenSizeChanged);
    });

    const cssClasses = computed(() => {
      return ['app'].concat(screen.getScreenSizeInfo.cssClasses);
    });

    return {
      title,
      screen,
      cssClasses,
    };
  },
};
</script>

<style lang="scss">
@import './dx-global.scss';

.app {
  @import './themes/generated/variables.base.scss';
  background-color: darken($base-bg, 5);
  display: flex;
  height: 100%;
  width: 100%;
}

.dx-row.dx-column-lines.dx-header-row {
  color: black;
  background-color: #e3fef9;
}

.dx-datagrid-headers .dx-header-row {
  color: black;
  background-color: #e3fef9;
}

.dx-toolbar .back-colored {
  background-color: #f7f7f7;
}

.back-colored {
  background-color: #f7f7f7;
}

.DxDataGrid {
  background-color: #f7f7f7;
}

.status-title {
  font-size: x-large;
  font-weight: 700;
}

.dx-header-row .column-dark {
  color: white;
  background-color: black;
}

.dx-header-row .column-green {
  color: white;
  background-color: #385723;
}

.dx-header-row .bullet {
  color: white;
  background-color: #385723;
}

.kiosk-view {
  .dx-popup-wrapper {
    .dx-overlay-content.dx-popup-normal.dx-resizable.dx-popup-inherit-height {
      transform: translate(50%, 50%) !important;
    }
  }
}
</style>
