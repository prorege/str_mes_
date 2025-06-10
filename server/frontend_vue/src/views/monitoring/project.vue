<template>
  <dx-load-panel v-model:visible="vars.loading.value" :show-pane="true" />
  <div class="content-block">
    <div class="dx-card responsive-paddings back-colored">
      <div class="content-header">
        <dx-toolbar class="back-colored">
          <dx-item location="before">
            <div class="content-title">프로젝트현황</div>
          </dx-item>
          <dx-item
            location="after"
            widget="dxButton"
            :options="{
              text: '전체화면',
              type: 'normal',
              onClick: methods.setFullscreen,
            }"
          />
        </dx-toolbar>
      </div>

      <div ref="viewer" class="content-wrapper">
        <div>
          <div class="project-title">
            프로젝트 현황
          </div>
          <div class="project-date">
            일 시 : {{ currentDate }} {{ currentTime }}
          </div>
        </div>

        <div :key="refreshKey" class="fullscreen-content">
          <div class="chart-item">
            <div class="chart-title">
              <MARQUEE>
                <div class="item-info">
                  {{ vars.data.project[0].project_name }}
                </div>
              </MARQUEE>
              <div class="work-info"></div>
            </div>
            <div class="chart-content">
              <monitoring-chart
                :color="vars.data.project[0].color"
                track="#252c40"
                :value="vars.data.project[0].total_progress"
              />
            </div>
            <div v-if="vars.data.project[0].contract_end_date" class="chart-content-left">종료일 : {{ vars.data.project[0].contract_end_date }}</div>
            <div v-if="vars.data.project[0].sum_of_quantity" class="chart-content-right">주문수량 : {{ vars.data.project[0].sum_of_quantity }}</div>
            
          </div>

          <div class="chart-item">
            <div class="chart-title">
              <MARQUEE>
                <div class="item-info">
                  {{ vars.data.project[1].project_name }}
                </div>
              </MARQUEE>
              <div class="work-info"></div>
            </div>
            <div class="chart-content">
              <monitoring-chart
                :color="vars.data.project[1].color"
                track="#252c40"
                :value="vars.data.project[1].total_progress"
              />
            </div>
            <div v-if="vars.data.project[1].contract_end_date" class="chart-content-left">종료일 : {{ vars.data.project[1].contract_end_date }}</div>
            <div v-if="vars.data.project[1].sum_of_quantity" class="chart-content-right">주문수량 : {{ vars.data.project[1].sum_of_quantity }}</div>
          </div>

          <div class="chart-item">
            <div class="chart-title">
              <MARQUEE>
                <div class="item-info">
                  {{ vars.data.project[2].project_name }}
                </div>
              </MARQUEE>
              <div class="work-info"></div>
            </div>
            <div class="chart-content">
              <monitoring-chart
                :color="vars.data.project[2].color"
                track="#252c40"
                :value="vars.data.project[2].total_progress"
              />
            </div>
            <div v-if="vars.data.project[2].contract_end_date" class="chart-content-left">종료일 : {{ vars.data.project[2].contract_end_date }}</div>
            <div v-if="vars.data.project[2].sum_of_quantity" class="chart-content-right">주문수량 : {{ vars.data.project[2].sum_of_quantity }}</div>
          </div>

          <div class="chart-item">
            <div class="chart-title">
              <MARQUEE>
                <div class="item-info">
                  {{ vars.data.project[3].project_name }}
                </div>
              </MARQUEE>
              <div class="work-info"></div>
            </div>
            <div class="chart-content">
              <monitoring-chart
                :color="vars.data.project[3].color"
                track="#252c40"
                :value="vars.data.project[3].total_progress"
              />
            </div>
            <div v-if="vars.data.project[3].contract_end_date" class="chart-content-left">종료일 : {{ vars.data.project[3].contract_end_date }}</div>
            <div v-if="vars.data.project[3].sum_of_quantity" class="chart-content-right">주문수량 : {{ vars.data.project[3].sum_of_quantity }}</div>
          </div>

          <div class="chart-item">
            <div class="chart-title">
              <MARQUEE>
                <div class="item-info">
                  {{ vars.data.project[4].project_name }}
                </div>
              </MARQUEE>
              <div class="work-info"></div>
            </div>
            <div class="chart-content">
              <monitoring-chart
                :color="vars.data.project[4].color"
                track="#252c40"
                :value="vars.data.project[4].total_progress"
              />
            </div>
            <div v-if="vars.data.project[4].contract_end_date" class="chart-content-left">종료일 : {{ vars.data.project[4].contract_end_date }}</div>
            <div v-if="vars.data.project[4].sum_of_quantity" class="chart-content-right">주문수량 : {{ vars.data.project[4].sum_of_quantity }}</div>
          </div>

          <div class="chart-item">
            <div class="chart-title">
              <MARQUEE> 
                <div class="item-info">
                {{ vars.data.project[5].project_name }}
                </div>
              </MARQUEE>
              <div class="work-info"></div>
            </div>
            <div class="chart-content">
              <monitoring-chart
                :color="vars.data.project[5].color"
                track="#252c40"
                :value="vars.data.project[5].total_progress"
              />
            </div>
            <div v-if="vars.data.project[5].contract_end_date" class="chart-content-left">종료일 : {{ vars.data.project[5].contract_end_date }}</div>
            <div v-if="vars.data.project[5].sum_of_quantity" class="chart-content-right">주문수량 : {{ vars.data.project[5].sum_of_quantity }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { DxLoadPanel } from 'devextreme-vue/load-panel';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';

import MonitoringChart from '@/components/monitoring/monitoring-chart';
import { ref, reactive, computed, onBeforeMount, onMounted, onBeforeUnmount } from 'vue';
import moment from 'moment';
import ApiService from '../../utils/api-service';

export default {
  components: {
    DxLoadPanel,
    DxToolbar,
    DxItem,
    MonitoringChart,
  },
  props: {
    id: [String, Number],
  },
  setup(props) {
    const vars = { dlg: {} };
    const viewer = ref(null);
    const refreshKey = ref(Date.now());
    const apiService = new ApiService('/api/mes/v1/project/monitoring');
    vars.loading = ref(false);
    const currentDate = moment().format('YYYY-MM-DD');
    const currentTime = ref(moment().format('HH:mm'));
    vars.timerId3 = setInterval(() => {
      currentTime.value = moment().format('HH:mm');
    }, 60 * 1000);
    vars.timerId = null;
    vars.timerId2 = null;
    vars.total = 100;
    vars.page = 1;
    vars.data = reactive({
      project: [
        {
          project_name: '',
          color: '#62cd14',
          total_progress: 0,
        },
        {
          project_name: '',
          color: '#62cd14',
          total_progress: 0,
        },
        {
          project_name: '',
          color: '#62cd14',
          total_progress: 0,
        },
        {
          project_name: '',
          color: '#62cd14',
          total_progress: 0,
        },
        {
          project_name: '',
          color: '#62cd14',
          total_progress: 0,
        },
        {
          project_name: '',
          color: '#62cd14',
          total_progress: 0,
        },
      ],
    });

    document.onfullscreenchange = () => {
      if (!document.fullscreenElement) {
        if (vars.timerId) clearTimeout(vars.timerId);
        vars.timerId = setTimeout(() => {
          methods.refresh();
        }, 10);
      }
    };

    onBeforeMount(async () => {
      methods.reload();

      vars.timerId2 = setInterval(() => {
        vars.page += 1;
        if (vars.page > vars.total) {
          vars.page = 1;
        }

        methods.reload();
      }, 5000);
    });

    onMounted(async () => {
      methods.refresh();
    });

    onBeforeUnmount(async () => {
      if (vars.timerId) clearTimeout(vars.timerId);
      if (vars.timerId2) clearInterval(vars.timerId2);
      if (vars.timerId3) clearInterval(vars.timerId3);
      document.onfullscreenchange = null;
    });

    const methods = {
      setFullscreen() {
        if (!viewer.value) return;
        viewer.value.requestFullscreen();
      },
      refresh() {
        refreshKey.value = Date.now();
        vars.timerId = null;
      },
      async reload() {
        const response = await apiService.post('', { page: vars.page });
        if (response && response['status'] == 200) {
          vars.total = response['data']['total'];
          const dataList = response['data']['data'];
          dataList.forEach(v => v.color = getGraphColor(v.total_progress))
          vars.data.project = [...dataList];
          if (vars.data.project.length < 6) {
            const limit = 6 - vars.data.project.length;
            for (let i = 0; i < limit; ++i) {
              vars.data.project.push({
                project_name: '',
                total_progress: 0,
                color: '#FFFFFF'
              });
            }
          }
        }
      },
    };

    function getGraphColor (progress) {
      if (progress == 100) return '#ff6f00'
      if (progress > 80) return '#62cd14'
      if (progress > 60) return '#00e582'
      if (progress > 40) return '#adcc00'
      if (progress > 20) return '#005aff'
      return '#00aeff'
    }

    return {
      vars,
      viewer,
      refreshKey,
      currentDate,
      currentTime,
      methods,
    };
  },
};
</script>

<style lang="scss" scoped>
.dx-card {
  width: 100%;
}

.project-title {
  font-size: 46px;
  font-weight: 700;
  margin-top: 20px;
  color:#FFFFFF;
}

.project-date {
  font-size: 24px;
  font-weight: 500;
  float: right;
  padding-right: 20px;
  color:#d7d7d7;
}

.content-wrapper {
  text-align: center;

  border: 1px solid #834a4a;
  border-radius: 4px;

  box-sizing: border-box;
  background: #1e2635;  
}

.fullscreen-content {
  position: relative;
  width: 100%;
  height: calc(100vh - 150px);
  margin-top: 10px;
  padding: 12px;

  display: grid;
  gap: 10px 10px;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  grid-auto-flow: dense;

  overflow: hidden;
}

.chart-item {
  width: 100%;
  height: 100%;
  padding: 10px;
  box-sizing: border-box;
  border-radius: 12px;
  background-color: #0f121a;
  .chart-title {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: bold;
    color: #FFF;
    font-size: 55px;
    height: 20%;
    align-items: flex-start;
    .item-info {
    }
    .work-info {
    }
  }
  .chart-content {
    width: calc(100% - 20px);
    height: 70%;
    padding: 10px;
    margin-left: 10px;
    box-sizing: border-box;
  }
  .chart-content-left {
    font-size:30px;
    float: left;
    font-weight: 1000;
    color: #ff875e;
  }
  .chart-content-right {
    font-size:30px;
    float: right;
    font-weight: 1000;
    color:#b2fff1;
  }
}
</style>
