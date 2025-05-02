
<template>
  <table class="product-label">
    <tbody>
      <tr v-for="(row, i) in rows" :key="i">
        <th>{{row.name}}</th>
        <td>{{row.text}}</td>
      </tr>
      <tr>
        <td colspan="2">
          <div class="bottom-info">
            <div class="warning">
              <template v-if="warning">
                <div>- 주의사항 -</div>
                <div>{{warning}}</div>
              </template>
            </div>
            <product-qr v-if="itemcode" :code="itemcode" />
          </div>
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
import ProductQr from './product-qr.vue'

export default {
  props: {
    itemcode: { type: String },
    warning: { type: String },
    rows: { type: Array }
  },
  components: {
    ProductQr
  },
  setup(props) {
    console.log(props.itemcode)
  },
}
</script>

<style lang="scss" scoped>
$border-color: #a0a0a0;

.product-label {
  min-width: 6cm;
  border: 1px solid $border-color;
  border-collapse: collapse;

  th, td {
    font-size: 12px;
    border: 1px solid $border-color; 
    padding: 2px 8px;
  }

  td {
    text-align: center;
  }

  .bottom-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0;
    padding-top: 4px;
    padding-bottom: 4px;
  }

  .warning {
    flex: 1 1 auto;
    font-size: 10px;
    padding-right: 10px;
  }
}
</style>
