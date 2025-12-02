<template>
  <div>
    <div class="content-block">
      <div class="dx-card responsive-paddings back-colored">
        
        <div class="content-header">
          <dx-toolbar class="back-colored">
            <dx-item location="before">
              <div class="content-title">M/D 관리 현황</div>
            </dx-item>
          </dx-toolbar>
        </div>

        <div class="search-row">
          <div class="search-item">
            <span class="search-label">등록일자</span>
            <div class="search-input-group">
              <dx-date-box v-model:value="vars.formData.startDate" type="date" display-format="yyyy-MM-dd" width="120" />
              <span class="tilde">~</span>
              <dx-date-box v-model:value="vars.formData.endDate" type="date" display-format="yyyy-MM-dd" width="120" />
            </div>
            <SearchButtonGroup class="ml-2" @change="({startDate, endDate}) => { vars.formData.startDate = startDate; vars.formData.endDate = endDate; }" />
          </div>
        </div>

        <div class="search-row mt-2">
          <div class="search-item">
            <span class="search-label">담당자</span>
            <dx-select-box 
              width="150"
              placeholder="선택..."
              value-expr="emp_name"
              display-expr="emp_name"
              v-model:value="vars.formData.employee"
              :data-source="vars.dataSource.employee"
              :show-clear-button="true"
            />
          </div>

          <div class="search-item ml-3">
            <span class="search-label" style="background-color: #666; color: white; padding: 4px 8px; border-radius: 4px;">프로젝트 명</span>
            <dx-select-box 
              width="250"
              placeholder="선택..."
              value-expr="project_name"
              display-expr="project_name"
              v-model:value="vars.formData.project"
              :data-source="vars.dataSource.projects"
              :search-enabled="true"
              :show-clear-button="true"
              @value-changed="methods.onProjectChanged"
            />
          </div>

          <div class="search-item ml-4">
            <dx-radio-group
              layout="horizontal"
              :items="vars.viewModes"
              v-model:value="vars.formData.viewMode"
              value-expr="value"
              display-expr="text"
              @value-changed="methods.onViewModeChanged"
            />
          </div>

          <div class="search-item ml-auto">
            <dx-button text="검색" icon="search" type="default" styling-mode="contained" @click="methods.searchDateRange()" />
          </div>
        </div>
      </div>

      <div class="dx-card responsive-paddings mt-2">
        <dx-data-grid
          height="calc(100vh - 280px)"
          column-resizing-mode="widget"
          :show-borders="true"
          :column-auto-width="true"
          :show-row-lines="true"
          :focused-row-enabled="true"
          :allow-column-resizing="true"
          :allow-column-reordering="true"
          :row-alternation-enabled="true"
          :data-source="dataSource"
          :on-initialized="evt => methods.onGridInitialized(evt, 'md-registration-status')"
          @exporting="methods.onExporting"
        >
          <dx-group-panel :visible="vars.formData.viewMode === 'project'" />
          
          <dx-column caption="담당자" data-field="manager" width="100" alignment="center" />
          
          <dx-column 
            caption="프로젝트명" 
            data-field="project_name" 
            min-width="250" 
            :group-index="vars.formData.viewMode === 'project' ? 0 : undefined" 
          />

          <dx-column caption="총 M/D" alignment="center">
            <dx-column caption="일" data-field="total_md_day" data-type="number" format="#,##0.0" width="60" />
            <dx-column caption="시간" data-field="total_md_hour" data-type="number" format="#,##0" width="60" />
          </dx-column>

          <dx-column caption="누적사용 M/D" alignment="center">
             <dx-column caption="일" data-field="used_md_day" data-type="number" format="#,##0.0" width="60" />
            <dx-column caption="시간" data-field="used_md_hour" data-type="number" format="#,##0" width="60" />
          </dx-column>

          <dx-column caption="등록일자" data-field="created" data-type="date" format="yyyy-MM-dd" width="100" alignment="center" />
          
          <dx-column caption="사용 M/D(시간)" data-field="used_md_hour_input" data-type="number" format="#,##0" width="120" css-class="highlight-column" />

          <dx-column caption="구분" data-field="position_type" width="80" alignment="center">
            <dx-lookup :data-source="vars.dataSource.position_type" value-expr="code_name" display-expr="code_name" />
          </dx-column>

          <dx-column caption="업무 내용" data-field="note" />

          <dx-sorting mode="multiple" />
          <dx-export :enabled="true" />
          <dx-paging :page-size="20" />
          <dx-filter-row :visible="true" />
          
          <dx-summary>
            <dx-group-item column="used_md_hour_input" summary-type="sum" display-format="{0} 시간" align-by-column="true" />
            
            <dx-total-item column="used_md_hour_input" summary-type="sum" display-format="총합: {0} 시간" />
          </dx-summary>

        </dx-data-grid>
      </div>
    </div>
  </div>
</template>

<script>
import moment from 'moment';
import { reactive, onMounted } from 'vue';
import { alert } from 'devextreme/ui/dialog';
import DxButton from 'devextreme-vue/button';
import { DxDateBox } from 'devextreme-vue/date-box';
import DxSelectBox from 'devextreme-vue/select-box'; // Lookup 대신 SelectBox 사용
import DxRadioGroup from 'devextreme-vue/radio-group';
import DxToolbar, { DxItem } from 'devextreme-vue/toolbar';
import { 
  DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, 
  DxSummary, DxTotalItem, DxGroupItem, DxGroupPanel, DxLookup 
} from 'devextreme-vue/data-grid';

import SearchButtonGroup from '../../components/search-button-group.vue';
import ArrayStore from 'devextreme/data/array_store';
import stateStore from '@/utils/state-store';

import { projectMdRegistration, getProjectRegistration } from '../../data-source/project'; 
import { loadEmployee } from '../../utils/data-loader';
import { baseCodeLoader } from '../../data-source/base';

export default {
  components: {
    DxButton,
    DxDateBox,
    DxSelectBox,
    DxRadioGroup,
    DxToolbar, DxItem,
    DxDataGrid, DxColumn, DxPaging, DxExport, DxSorting, DxFilterRow, 
    DxSummary, DxTotalItem, DxGroupItem, DxGroupPanel, DxLookup,
    SearchButtonGroup,
  },
  setup() {
    const vars = {};
    vars.grid = {};
    
    // 라디오 버튼 옵션
    vars.viewModes = [
      { text: '날짜별 사용 M/D', value: 'date' },
      { text: '프로젝트별 사용 M/D', value: 'project' }
    ];

    vars.formData = reactive({
      startDate: new Date(),
      endDate: new Date(),
      employee: null,
      project: null,
      viewMode: 'date', // 기본값: 날짜별
    });

    vars.dataSource = reactive({
      employee: null,
      projects: [],
      position_type: [], // 구분(PM/PE)
    })
    
    const dataSource = new ArrayStore({ key: 'grid_id', data: [] })
    
    onMounted(async () => {
      await loadEmployee(vars.dataSource);
      await methods.loadProjects();
      await methods.loadBaseCode();
    })
    
    const methods = {
      onGridInitialized(evt, key) {
        vars.grid[key] = evt.component;
        stateStore.bind(`project-md-status-${key}`, evt.component);
      },

// 프로젝트 목록 조회 (콤보박스용) - M/D 내역이 있는 것만 중복제거하여 표시
    async loadProjects() {
      try {
        // 1. M/D 등록 테이블 조회
        const result = await projectMdRegistration.load(); 
        const allRows = Array.isArray(result) ? result : (result.data || []);
             
        // 2. 프로젝트명 기준으로 중복 제거 (Set 자료구조 사용)
        const uniqueProjects = [];
        const seenNames = new Set();
          
        allRows.forEach(row => {
          // 프로젝트명이 있고, 아직 목록에 넣지 않은 이름이라면 추가
            if (row.project_name && !seenNames.has(row.project_name)) {
              seenNames.add(row.project_name);
              uniqueProjects.push({ project_name: row.project_name });
            }
        });

        // 3. 가나다순 정렬 (찾기 편하게)
        uniqueProjects.sort((a, b) => a.project_name.localeCompare(b.project_name));

        vars.dataSource.projects = uniqueProjects;

      } catch (e) {
        console.error("프로젝트 목록 로드 실패", e);
      }
    },

       // 기초코드(직책구분) 조회
      async loadBaseCode(){
          return baseCodeLoader(['직책구분']).then(response =>{
              vars.dataSource.position_type = response['직책구분']
          });
      },

      // [요구사항] 프로젝트 선택 시 -> 날짜별 모드로 변경
      onProjectChanged(e) {
        if (e.value) {
            vars.formData.viewMode = 'date';
        }
      },

      // [요구사항] 보기 모드 변경 시 로직
      onViewModeChanged(e) {
        if (e.value === 'project') {
            // 프로젝트별 보기 선택 시 -> 프로젝트 선택값 초기화
            vars.formData.project = null;
        }
        // 모드가 바뀌면 그리드 리프레시를 위해 검색 재실행 권장 (선택사항)
        methods.searchDateRange();
      },

      getParams () {
        const startDate = moment(vars.formData.startDate).startOf('day').format('YYYY-MM-DD 00:00:00');
        const endDate = moment(vars.formData.endDate).endOf('day').format('YYYY-MM-DD 23:59:59');

        // 기본 필터: 날짜 범위
        const filter = [
            ['trip_start_date', '>=', startDate],
            'and',
            ['trip_start_date', '<=', endDate],
        ];

        // 담당자 필터
        if (vars.formData.employee) {
            filter.push('and', ['manager', '=', vars.formData.employee]);
        }

        // 프로젝트 필터
        if (vars.formData.project) {
             filter.push('and', ['project_name', '=', vars.formData.project]);
        }

        const params = {
            filter: filter,
            sort: [{ selector: 'trip_start_date', desc: true }], // 최신순 정렬
            skip: 0,
            take: 10000,
        };

        return params;
      },

      async searchDateRange() {
        if (vars.formData.startDate > vars.formData.endDate) {
          await alert('조회 일자가 잘못 되었습니다', '조회');
          return;
        }

        try{
          dataSource.clear()
          const gridKey = 'md-registration-status';
          if(vars.grid[gridKey]) vars.grid[gridKey].beginCustomLoading('데이터를 조회 중입니다...');
          
          const params = methods.getParams(); 

          // [수정 포인트 1] 결과를 변수(result)로 전체를 받습니다.
          const result = await projectMdRegistration.load(params);
          
          // [수정 포인트 2] 결과가 배열인지 객체인지 확인하여 안전하게 리스트 추출
          // RestlessStore 설정에 따라 배열([..])로 오거나, 객체({data:[..]})로 올 수 있음
          let rows = [];
          if (Array.isArray(result)) {
              rows = result;
          } else if (result && result.data && Array.isArray(result.data)) {
              rows = result.data;
          } else if (result && result.objects && Array.isArray(result.objects)) {
              rows = result.objects; // flask-restless 기본 포맷 대비
          }

          console.log("조회된 데이터:", rows); // F12 콘솔에서 확인용

          let i = 1;
          rows.forEach((v) => {
            v.grid_id = i++
            dataSource.insert(v);
          });

        } catch(ex){
          console.error("데이터 조회 실패:", ex)
        } finally{
          const gridKey = 'md-registration-status';
          if(vars.grid[gridKey]) vars.grid[gridKey].endCustomLoading();
        }
        const gridKey = 'md-registration-status';
        if(vars.grid[gridKey]) vars.grid[gridKey].refresh(); 
      },
      
      onExporting(evt) {
        projectMdRegistration.exportData(evt.component, 'MD관리현황', `MD관리현황_${Date.now()}.xlsx`);
        evt.cancel = true;
      },
      
    };

    return { vars, methods, dataSource };
  },
};
</script>

<style scoped>
/* 레이아웃 스타일링 */
.search-row {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.search-item {
  display: flex;
  align-items: center;
  margin-right: 10px;
}

.search-label {
  font-weight: 500;
  margin-right: 8px;
  white-space: nowrap;
}

.search-input-group {
  display: flex;
  align-items: center;
}

.tilde {
  margin: 0 8px;
}

.ml-2 { margin-left: 8px; }
.ml-3 { margin-left: 16px; }
.ml-4 { margin-left: 24px; }
.ml-auto { margin-left: auto; }
.mt-2 { margin-top: 8px; }

/* 그리드 내 강조 컬럼 스타일 (사용 M/D) */
:deep(.highlight-column) {
  background-color: #f0f0f0; 
  font-weight: bold;
}
</style>