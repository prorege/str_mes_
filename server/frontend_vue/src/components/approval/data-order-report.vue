<template>
  <div class="order-report dx-card responsive-paddings back-colored">
    <div class="content-header">
      <div class="content-header-container">
        <div class="content-header-title">
          <h2>수주사항보고서</h2>
        </div>
        <div class="content-header-line">
          <div class="content-header-approval-line">
            <table class="approval-line-table">
              <colgroup>
                <col style="width:28px"/>
                <col style="width:46px"/>
                <col style="width:46px"/>
                <col style="width:46px"/>
                <col style="width:46px"/>
                <col style="width:46px"/>
                <col style="width:46px"/>
                <col style="width:46px"/>
                <col style="width:46px"/>
                <col style="width:46px"/>
                <col style="width:46px"/>
              </colgroup>
              <tr>
                <td rowspan="3" style="font-weight: bold;">결제</td>
                <th>사원 및<br>계장</th>
                <th>대리</th>
                <th>과장</th>
                <th>차장</th>
                <th>부장</th>
                <th>이사</th>
                <th>상무</th>
                <th>전무</th>
                <th>대표이사</th>
                <th>회장</th>
              </tr>
              <tr style="height: 30px;">
                <td v-for="i in 11" :key="i">
                    <div class="approval-sign-box">
                    </div>
                </td>
              </tr>
              <tr style="height: 15px;">
                <td v-for="i in 11" :key="i"></td>
              </tr>
            </table>
          </div>
        </div>
    
      </div>
    </div>
    <div class="content-body">
      <div class="content-body-container">
        <div class="content-body-form dx-card responsive-paddings back-colored">
          <dx-form :form-data="vars.formData">
            <dx-group-item :col-count="4">
              <dx-group-item>
                  <dx-simple-item
                    data-field="business_number"
                    :editor-options="{
                      ...vars.formState,
                    }"
                  >
                    <dx-label text="영업 건 번호" :show-colon="false" />
                  </dx-simple-item>

                  <dx-simple-item data-field="business_date" editor-type="dxDateBox" :editor-options="{ 
                    dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss', 
                    ...vars.formState
                  }">
                    <dx-label text="영업일자" :show-colon="false"/>
                  </dx-simple-item>

                  <dx-simple-item data-field="business_name" :editor-options="{
                    ...vars.formState }">
                    <dx-label text="영업 건 명" :show-colon="false" />
                    <dx-required-rule message="영업명을 입력하세요" />
                  </dx-simple-item>
                  <dx-simple-item data-field="client_company"
                  :editor-options="{
                    ...vars.formState,
                  }"
                >
                    <dx-label text="계약상대자" :show-colon="false" />
                    <dx-required-rule message="계약상대자를 선택하세요" />
                  </dx-simple-item>
                  <dx-simple-item data-field="contract_company"
                  :editor-options="{
                    ...vars.formState,
                  }"
                >
                  <dx-label text="수요기관" :show-colon="false" />
                </dx-simple-item>
              </dx-group-item>
              <dx-group-item>
                  <dx-simple-item data-field="business_department" :editor-options="{
                      ...vars.formState,
                    }">
                    <dx-label text="담당부서" :show-colon="false" />
                  </dx-simple-item>

                  <dx-simple-item data-field="business_manager" :editor-options="{
                    ...vars.formState,
                  }">
                    <dx-label text="당사담당자" :show-colon="false" />
                  </dx-simple-item>

                  <dx-simple-item data-field="business_amount" editor-type="dxNumberBox" :editor-options="{
                    format: '₩,##0',
                    ...vars.formState
                  }">
                    <dx-label text="영업금액" :show-colon="false" />
                  </dx-simple-item>
                  <dx-simple-item 
                  data-field="client_manager" 
                  :editor-options="{
                    ...vars.formState
                }">
                  <dx-label text="업체담당자" :show-colon="false" />
                </dx-simple-item>
                <dx-simple-item data-field="completion_date" editor-type="dxDateBox" :editor-options="{
                    dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                    ...vars.formState
                  }">
                    <dx-label text="준공일자" :show-colon="false" />
                  </dx-simple-item>
              </dx-group-item>
              <dx-group-item>
                  <dx-simple-item data-field="business_type" :editor-options="{
                    ...vars.formState,
                  }">
                    <dx-label text="영업구분" :show-colon="false" />
                  </dx-simple-item>
                  <dx-simple-item data-field="classification" :editor-options="{
                    ...vars.formState,
                  }">
                    <dx-label text="종목" :show-colon="false" />
                  </dx-simple-item>
                  <dx-simple-item data-field="location" :editor-options="{
                    ...vars.formState,
                  }">
                    <dx-label text="현장지역" :show-colon="false" />
                  </dx-simple-item>
                  <dx-simple-item data-field="registration_closing_date" editor-type="dxDateBox" :editor-options="{ 
                    dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                    type: 'datetime',
                    displayFormat: 'yyyy-MM-dd HH:mm',
                    pickerType: 'calendar',
                    ...vars.formState
                  }">
                    <dx-label text="등록마감" :show-colon="false"/>
                  </dx-simple-item>
                  <dx-simple-item data-field="bid_closing_date" editor-type="dxDateBox" :editor-options="{ 
                    dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                    type: 'datetime',
                    displayFormat: 'yyyy-MM-dd HH:mm',
                    pickerType: 'calendar',
                    ...vars.formState
                  }">
                    <dx-label text="투찰마감" :show-colon="false"/>
                  </dx-simple-item>
              </dx-group-item>
              <dx-group-item>
                  <dx-simple-item data-field="business_progress" :editor-options="{
                    ...vars.formState,
                  }">
                    <dx-label text="진행현황" :show-colon="false" />
                  </dx-simple-item>
                  <dx-simple-item data-field="project.project_number" :editor-options="{
                    ...vars.formState,
                  }">
                    <dx-label text="연결 프로젝트" :show-colon="false" />
                  </dx-simple-item>
                  <dx-simple-item data-field="contract_type" :editor-options="{
                    ...vars.formState,
                  }">
                    <dx-label text="계약유형" :show-colon="false" />
                  </dx-simple-item>
                  <dx-group-item :col-count="2" css-class="form-group">
                    <dx-simple-item data-field="gross_profit" editor-type="dxNumberBox" :editor-options="{
                    readOnly: true,
                    format: '₩,##0',
                    }">
                    <dx-label text="매출총이익" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item data-field="gross_profit_rate" editor-type="dxNumberBox" :editor-options="{
                      readOnly: true,
                      format: '#0.00%'
                      }">
                      <dx-label text="GM" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item data-field="operating_profit" editor-type="dxNumberBox" :editor-options="{
                        readOnly: true,
                        format: '₩,##0',
                        }">
                        <dx-label text="순수익" :show-colon="false" />
                      </dx-simple-item>
                    
                      <dx-simple-item data-field="operating_profit_rate" editor-type="dxNumberBox" :editor-options="{
                      readOnly: true,
                      format: '#0.00%'
                      }">
                      <dx-label text="OP" :show-colon="false" />
                    </dx-simple-item>
                </dx-group-item>
              </dx-group-item>
            </dx-group-item>
          </dx-form>
        </div>
        <div class="content-body-line">
          <h2>원 가 내 역</h2>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive } from 'vue';
import { DxForm, DxGroupItem, DxSimpleItem, DxLabel, DxRequiredRule } from 'devextreme-vue/form';

export default {
  components: {
    DxForm, DxGroupItem, DxSimpleItem, DxLabel, DxRequiredRule
  },
  setup() {
    const vars = reactive({});  
    vars.formData = reactive({
      business_number: '',
      business_date: '',
      business_name: '',
      client_company: '',
      contract_company: '',
      business_department: '',
      business_manager: '',
      business_amount: '',
      client_manager: '',
      completion_date: '',
      business_type: '',
      classification: '',
      location: '',
      registration_closing_date: '',
      bid_closing_date: '',
      business_progress: '',
      project_number: '',
      contract_type: '',
      gross_profit: '',
      gross_profit_rate: '',
      operating_profit: '',
      operating_profit_rate: '',
    });
    vars.formState = reactive({
      readOnly: true,
    });
    return { vars };
  }
}
</script>

<style lang="scss" scoped>
.order-report {
  padding: 20px;
  overflow-y: auto;
  scrollbar-width: thin;

  .content-header {
    .content-header-container {
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;

      .content-header-title {
        h2 {
          font-weight: bold;
        }
      }
      .content-header-line {
        display: flex;
        justify-content: flex-end;
        width: 100%;

        .content-header-approval-line {
        .approval-line-table th,
        .approval-line-table td {
          font-size: 0.7rem;
          border: 1px solid #dddddd;
          padding: 0;
          text-align: center;
          vertical-align: middle;
          background-color: #ffffff;
        }
        .approval-line-table {
        border-collapse: collapse;  

        }
      }
      }
      
    }
  }
  .content-body {
    .content-body-container {
      .content-body-form {

      }
      .content-body-line {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        h2 {
          font-weight: bold;
        }
      }
    }
  }
}
</style>