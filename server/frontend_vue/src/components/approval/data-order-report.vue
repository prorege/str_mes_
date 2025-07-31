<template>
  <div class="order-report dx-card responsive-paddings">
    <div class="content-header">
      <div class="content-header-container">
        <div class="content-header-title">
          <h1>수주사항보고서</h1>
        </div>
        <div class="content-header-line">
          <div class="content-header-approval-line">
            <table class="approval-line-table">
              <colgroup>
                <col style="width:30px"/>
                <col style="width:50px"/>
                <col style="width:50px"/>
                <col style="width:50px"/>
                <col style="width:50px"/>
                <col style="width:50px"/>
                <col style="width:50px"/>
                <col style="width:50px"/>
                <col style="width:50px"/>
                <col style="width:50px"/>
                <col style="width:50px"/>
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
              <tr style="height: 45px;">
                <td v-for="i in 11" :key="i">
                    <div class="approval-sign-box">
                    </div>
                </td>
              </tr>
              <tr style="height: 20px;">
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
        <h2 style="text-align: center; background-color: #f0f0f0; height: 60px; line-height: 60px;">원 가 내 역</h2>
        <div class="content-body-item">
          <div class="item-total-supply">
            <table>
              <colgroup>
                <col style="width: auto;" />
                <col style="width: 15px;" /> 
                <col style="width: 200px;" /> 
                <col style="width: auto;" /> 
                <col style="width: 15px;" /> 
                <col style="width: 200px;" /> 
              </colgroup>
              <tr>
                <th>&nbsp;&nbsp;&nbsp;구 매 합 계 </th>
                <th style="text-align: center;">:</th>
                <th style="text-align: left;">{{ vars.formData.purchase_supply_price.toLocaleString() +" 원"}}</th>
                <th>견 적 합 계 </th>
                <th style="text-align: center;">:</th>
                <th style="text-align: left;">{{ vars.formData.quote_supply_price.toLocaleString() +" 원"}}</th>
              </tr>
            </table>
          </div>
          <div class="item-list">
            <dx-data-grid
                class="fixed-header-table"
                column-resizing-mode="widget"
                :show-borders="true"
                :remote-operations="false"
                :column-auto-width="true"
                :allow-column-resizing="false"
                :allow-column-reordering="true"
                :select-text-onedit-start="true"
                :sorting="{ mode: 'none' }"
                :data-source="vars.dataSource.cost"
                >
                <dx-column caption="구분" data-field="type" :cell-template="methods.itemTypeTemplate" />
                <dx-column caption="품목코드" data-field="item_code" :allow-editing="false" />
                <dx-column caption="품명" data-field="item.item_name" :allow-editing="false"  />
                <dx-column caption="규격" data-field="item.item_standard" :allow-editing="false"  />
                <dx-column caption="단위" data-field="item.unit" :allow-editing="false" />
                <dx-column caption="견적수량" data-field="quote_quantity"  data-type="number" format=",###.#"  />
                <dx-column caption="견적단가" data-field="quote_unit_price"  data-type="number" format="currency"  />
                <dx-column caption="견적금액" data-field="quote_supply_price" data-type="number" format="currency"  />
                <dx-column caption="구매단가" data-field="purchase_unit_price" data-type="number" format="currency"  />
                <dx-column caption="구매금액" data-field="purchase_supply_price" data-type="number" format="currency" />
                <dx-column caption="DC Rate" data-field="dc_rate" data-type="number" format="percent" :visible="false" />
                <dx-summary :recalculate-while-editing="true" :calculate-custom-summary="methods.calculateCustomSummary">
                    <dx-total-item name="quote_supply_price" summary-type="custom" />
                    <dx-total-item name="purchase_supply_price" summary-type="custom" />
                </dx-summary>
                <dx-paging :enabled="false" />
            
            </dx-data-grid>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { reactive, onMounted } from 'vue';
import { DxForm, DxGroupItem, DxSimpleItem, DxLabel, DxRequiredRule } from 'devextreme-vue/form';
import { DxNumberBox } from 'devextreme-vue/number-box'
import { DxDataGrid, DxColumn, DxScrolling, DxPaging, DxSummary, DxTotalItem, } from 'devextreme-vue/data-grid';
import { getProjectBusinessCost } from '../../data-source/project';
import ArrayStore from 'devextreme/data/array_store';
import { groupBy, sortBy } from 'lodash';
export default {
  components: {
    DxForm, DxGroupItem, DxSimpleItem, DxLabel, DxRequiredRule, DxNumberBox, DxDataGrid, DxColumn, DxScrolling, DxPaging, DxSummary, DxTotalItem,
  },
  props: {
    businessId: {
      type: [String, Number],
      default: null
    },
    formData: {
      type: Object,
      default: () => ({})
    }
  },
  setup(props) {
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
      quote_supply_price: 0,
      purchase_supply_price: 0,
    });
    vars.dataSource = reactive({
      cost : new ArrayStore({ key: 'item_code', data: [] })
    });
    vars.formState = reactive({
      readOnly: true,
    });
    
    const methods = {
      itemTypeTemplate(e, v) {
        if (v.data.isGroupHeader) {
          e.style.backgroundColor = '#f0f0f0';
          e.style.fontWeight = 'bold';
          e.style.textAlign = 'center';
          e.textContent = v.data.type;
        } else if (!v.data.isEmptyRow) {
          e.textContent = "";
        }
      },
      calculateCustomSummary(options) {
        if (options.name === 'purchase_supply_price'){
          if (options.summaryProcess === 'start'){
            options.totalValue = 0;
          } else if (options.summaryProcess === 'calculate'){
            if (typeof options.value.purchase_supply_price === 'number'){
              options.totalValue += options.value.purchase_supply_price;
            } 
          } else if (options.summaryProcess === 'finalize'){
            vars.formData.purchase_supply_price = options.totalValue;
          }
        } else if (options.name === 'quote_supply_price'){
          if (options.summaryProcess === 'start'){
            options.totalValue = 0;
          } else if (options.summaryProcess === 'calculate'){
            if (typeof options.value.quote_supply_price === 'number'){
              options.totalValue += options.value.quote_supply_price;
            }
          } else if (options.summaryProcess === 'finalize'){
            vars.formData.quote_supply_price = options.totalValue;
          }
        }
      }
    }
    
    onMounted(async () => {
      try {
        if (props.formData) {
          Object.assign(vars.formData, props.formData);
        }
        if (props.businessId) {
          const { data } = await getProjectBusinessCost([{ name: 'fk_business_id', op: 'eq', val: props.businessId }]).load();
          
          const groupedData = groupBy(data, 'item.main_category');
          
          const processedData = [];
          const categories = Object.keys(groupedData);
          
          categories.forEach((category, categoryIndex) => {

            const firstItem = sortBy(groupedData[category], 'item_order')[0];
            if (firstItem) {
              processedData.push({
                type: category,
                ...firstItem,
                isGroupHeader: true
              });
            }
            
            const sortedItems = sortBy(groupedData[category], 'item_order');
            sortedItems.slice(1).forEach(item => {
              processedData.push({
                ...item,
                isGroupHeader: false
              });
            });
            
            if (categoryIndex < categories.length - 1) {
              processedData.push({
                item_order: '',
                item_code: '',
                item_name: '',
                item_standard: '',
                unit: '',
                quote_quantity: '',
                quote_unit_price: '',
                quote_supply_price: '',
                purchase_unit_price: '',
                purchase_supply_price: '',
                dc_rate: '',
                isGroupHeader: false,
                isEmptyRow: true
              });
            }
          });
 
          vars.dataSource.cost = new ArrayStore({ 
            key: 'item_code', 
            data: processedData 
          });
        }
      } catch (error) {
        console.error('DataOrderReport mounted error:', error);
      }
    });
    
    return { vars, methods };
  }
}
</script>

<style lang="scss">
.order-report {
  padding: 20px;
  height: 100%;
  // max-height: calc(100vh - 250px);

  .content-header {
    .content-header-container {
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;

      .content-header-title {
        h1 {
          font-weight: bold;
          margin-bottom: 0;
        }
      }
      .content-header-line {
        display: flex;
        justify-content: flex-end;
        width: 100%;
        margin-bottom: 20px;

        .content-header-approval-line {
        .approval-line-table th,
        .approval-line-table td {
          font-size: 0.8rem;
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
      h2 {
          font-weight: bold;
      }
      .content-body-item {
        display: flex;
        flex-direction: column;
        width: 100%;
        // border: 1px solid #dddddd;
        
        
        .item-total-supply {

        }
        .item-list {
          .dx-row.dx-column-lines.dx-header-row {
            background-color: #ffffff !important;
            font-weight: bold !important;
          }
          .dx-datagrid-headers .dx-header-row {
            background-color: #ffffff !important;
            font-weight: bold !important;
          }
        }
        
      }
    }
  }
}
</style>