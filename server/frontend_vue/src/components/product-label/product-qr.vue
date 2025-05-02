<template>
  <div>
    <canvas ref="canvas"></canvas>
    <div v-if="error">{{error}}</div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

import QRCode from 'qrcode'

export default {
  props: {
    code: String
  },
  setup(props) {
    const canvas = ref(null)
    let error = null

    onMounted(() => {
      try {
        QRCode.toCanvas(canvas.value, props.code, {margin: 0})
      }
      catch (ex) {
        console.log(ex)
        error = ex.message
      }
    })

    return { canvas, error }
  },
}
</script>
