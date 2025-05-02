<script setup>
import QrScanner from 'qr-scanner'
import { ref, onMounted, defineEmits } from 'vue'

const player = ref()
const decoded = ref('')
const emit = defineEmits(['read'])
let scanner = undefined

onMounted(() => {
  console.log('scanner on mounted')
  const options = {
    highlightScanRegion: true,
    highlightCodeOutline: true,
    returnDetailedScanResult: true,
    maxScansPerSecond: 60
  }
  scanner = new QrScanner(player.value, resolveResult, options)
  scanner.start()
})

function resolveResult (result) {
  decoded.value = result
  emit('read', result)
  scanner.stop()
}
</script>

<template>
  <div class="scanner-bg">
    <div class="">
      <video ref="player" class="player"></video>
      <div class="button-container"><button type="button" @click="resolveResult('')">취소</button></div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.scanner-bg {
  position: fixed; top: 0; left: 0;
  width: 100vw; height: 100vh;
  z-index: 9000;
  background-color: white;

  display: flex;
  justify-content: center;
  align-items: center;
}

.player {
  width: 400px;
  background-color: #606060;
}
.button-container {
  display: flex;
  justify-content: center;
}
button {
  border: 1px solid #a0a0a0;
  background-color: #ebebeb;
  width: 130px;
  height: 40px;
  font-size: 18px;
}
</style>