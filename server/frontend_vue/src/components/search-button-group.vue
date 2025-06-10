<script setup>
import DxButton from 'devextreme-vue/button';
import moment from 'moment';
import { ref, defineEmits } from 'vue';

const emit = defineEmits(['change']);
const state = ref();

function getStateName(name) {
  return state.value === name ? 'default' : 'normal';
}

function searchToday() {
  const dt = moment();
  state.value = '0D';
  emit('change', {
    startDate: dt.startOf('D').toDate(),
    endDate: dt.endOf('D').toDate(),
  });
}
function searchYesterday() {
  const dt = moment().add(-1, 'day');
  state.value = '1D';
  emit('change', {
    startDate: dt.startOf('day').toDate(),
    endDate: dt.endOf('day').toDate(),
  });
}
function searchCurrentMonth() {
  const dt = moment();
  state.value = '0M';
  emit('change', {
    startDate: dt.startOf('month').toDate(),
    endDate: dt.endOf('month').toDate(),
  });
}
function searchPreviousMonth() {
  const dt = moment().add(-1, 'month');
  state.value = '1M';
  emit('change', {
    startDate: dt.startOf('month').toDate(),
    endDate: dt.endOf('month').toDate(),
  });
}
function searchCurrentYear() {
  const dt = moment();
  state.value = '0Y';
  emit('change', {
    startDate: dt.startOf('year').toDate(),
    endDate: dt.endOf('year').toDate(),
  });
}
function searchPreviousYear() {
  const dt = moment().add(-1, 'year');
  state.value = '1Y';
  emit('change', {
    startDate: dt.startOf('year').toDate(),
    endDate: dt.endOf('year').toDate(),
  });
}
function searchAll() {
  const dt = moment();
  state.value = 'AL';
  emit('change', {
    endDate: dt.endOf('year').toDate(),
    startDate: dt.add(-100, 'year').startOf('year').toDate(),
  });
}
</script>

<template>
  <dx-button text="당일" :type="getStateName('0D')" @click="searchToday()" />
  <dx-button
    text="전일"
    :type="getStateName('1D')"
    @click="searchYesterday()"
  />
  <dx-button
    text="당월"
    :type="getStateName('0M')"
    @click="searchCurrentMonth()"
  />
  <dx-button
    text="전월"
    :type="getStateName('1M')"
    @click="searchPreviousMonth()"
  />
  <dx-button
    text="금년"
    :type="getStateName('0Y')"
    @click="searchCurrentYear()"
  />
  <dx-button
    text="전년"
    :type="getStateName('1Y')"
    @click="searchPreviousYear()"
  />
  <dx-button text="전체" :type="getStateName('AL')" @click="searchAll()" />
</template>
