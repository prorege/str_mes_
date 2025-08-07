<template>
  <div class="order-report dx-card responsive-paddings">
    <div class="buttons">
        <dx-button text="인쇄" icon="print" @click="methods.printPopup" />
    </div>
    <div class="content-header">
      <div class="content-header-container">
        <div class="content-header-title">
          <h1>수주사항보고서</h1>
        </div>
        <div class="content-header-line">
          <div class="empty-space"></div>
          <div class="business-name"><h4>사업명 : {{ vars.formData.business_name }}</h4></div>
          <div class="content-header-approval-line">
            <table class="approval-line-table">
              <colgroup>
                <col style="width:30px"/>
                <col style="width:65px"/>
                <col style="width:65px"/>
                <col style="width:65px"/>
                <col style="width:65px"/>
                <col style="width:65px"/>
              </colgroup>
              <tr style="height: 20px;">
                <td rowspan="3" style="font-weight: bold;">결제</td>
                <th>기안</th>
                <th>팀장</th>
                <th>PM검토</th>
                <th>PE검토</th>
                <th>대표이사</th>
              </tr>
              <tr style="height: 45px;">
                <td v-for="i in 6" :key="i">
                    <div class="approval-sign-box">
                    </div>
                </td>
              </tr>
              <tr style="height: 20px;">
                <td v-for="i in 6" :key="i"></td>
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
            <dx-group-item :col-count="19">
              <dx-group-item :col-span="7">
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
              <dx-group-item :col-span="5">
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
                  <dx-simple-item data-field="completion_date" editor-type="dxDateBox" :editor-options="{
                    dateSerializationFormat: 'yyyy-MM-ddTHH:mm:ss',
                    ...vars.formState
                  }">
                    <dx-label text="준공예정일" :show-colon="false" />
                  </dx-simple-item>
              </dx-group-item>
              <dx-group-item :col-span="7">
                  <dx-group-item :col-count="2">
                    <dx-simple-item data-field="business_progress" :editor-options="{
                      ...vars.formState,
                    }">
                      <dx-label text="진행현황" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item data-field="contract_type" :editor-options="{
                    ...vars.formState,
                  }">
                    <dx-label text="계약유형" :show-colon="false" />
                  </dx-simple-item>
                  </dx-group-item>
                  <dx-group-item :col-count=2>
                    <dx-simple-item data-field="project.project_number" :editor-options="{
                    ...vars.formState,
                  }">
                      <dx-label text="연결 프로젝트" :show-colon="false" />
                    </dx-simple-item>
                    <dx-simple-item data-field="business_type" :editor-options="{
                    ...vars.formState,
                  }">
                      <dx-label text="영업구분" :show-colon="false" />
                    </dx-simple-item>
                  </dx-group-item>
                  <dx-simple-item data-field="business_amount" editor-type="dxNumberBox" :editor-options="{
                    format: '₩,##0',
                    ...vars.formState
                  }">
                    <dx-label text="영업금액" :show-colon="false" />
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
import { reactive, onMounted, watch } from 'vue';
import { DxForm, DxGroupItem, DxSimpleItem, DxLabel, DxRequiredRule } from 'devextreme-vue/form';
import { DxNumberBox } from 'devextreme-vue/number-box'
import { DxDataGrid, DxColumn, DxScrolling, DxPaging, DxSummary, DxTotalItem, } from 'devextreme-vue/data-grid';
import { DxButton } from 'devextreme-vue/button';
import { getProjectBusinessCost, projectBusiness } from '../../data-source/project';
import { approvalDocumentStatus, approvalLine } from '../../data-source/approval';
import ArrayStore from 'devextreme/data/array_store';
import authService from '@/auth';
import { groupBy, sortBy } from 'lodash';
import html2canvas from 'html2canvas';
import { filter } from 'lodash';
export default {
  components: {
    DxForm, DxGroupItem, DxSimpleItem, DxLabel, DxRequiredRule, DxNumberBox, DxDataGrid, DxColumn, DxScrolling, DxPaging, DxSummary, DxTotalItem, DxButton,
  },
  props: {
    fk_business_id: {
      type: Number,
      default: null
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
      completion_date: '',
      business_type: '',
      classification: '',
      location: '',
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
      cost : new ArrayStore({ key: 'item_code', data: [] }),
      approvalLine : [],
      approvalLineResult : [],
    });
    vars.formState = reactive({
      readOnly: true,
    });
    const methods = {
      async initById(id){
        try {
          const response = await approvalDocumentStatus.load({
            filter: ['manager', '=', authService.getUserName()]
          });
          if (response.data) {
            const document = response.data.find(item => item.document_name === '수주사항보고서')
            if (document) {
              const { data : approvalLineData } = await approvalLine.load({
                filter: ['fk_document_id', '=', document.id]
              });
              vars.dataSource.approvalLine = approvalLineData;
            }
          }
          
          if (id) {
            const { data : businessData } = await projectBusiness.load({
              filter: ['id', '=', id]
            });
            Object.assign(vars.formData, businessData[0]);

            if (vars.formData.id){
              const { data : costData } = await getProjectBusinessCost([{ name: 'fk_business_id', op: 'eq', val: vars.formData.id }]).load();
            
              const groupedData = groupBy(costData, 'item.main_category');
              
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
          }
        } catch (error) {
          console.error('DataOrderReport mounted error:', error);
        }
      },
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
      },
      async printPopup() {
        if(!vars.formData.id) return;
        const popup = document.querySelector('.order-report');
        
        if (!popup) return;
        const popupParent = popup.parentElement;

        const clone = popup.cloneNode(true);

        clone.style.width = '1400px';
        clone.style.margin = '0 auto';
        clone.style.position = 'fixed';
        clone.style.zIndex = '-9999';
        clone.classList.add('print-mode');

        
        // 버튼 숨기기
        const buttonsElement = clone.querySelector('.buttons');
        if (buttonsElement) {
          buttonsElement.style.display = 'none';
        }
        
        popupParent.appendChild(clone);
        
        try {
          const canvas = await html2canvas(clone, { 
            backgroundColor: '#fff', 
            scale: 2,
            useCORS: true,
            allowTaint: true
          });
          
          const imgData = canvas.toDataURL('image/png');
          popupParent.removeChild(clone);
          
          const printWindow = window.open('', '_blank', 'width=900,height=1200');
          printWindow.document.write(`
              <html>
                <head>
                  <title>인쇄</title>
                  <meta charset="utf-8">
                  <style>
                    @page { 
                      size: A4; 
                      margin: 0; 
                    }
                    html { 
                      margin: 0; 
                      padding: 0; 
                    }
                    body { 
                      margin: 0; 
                      padding: 0;
                    }
                    .print-container {
                      text-align: center;
                    }
                    img { 
                      max-width: 210mm; 
                      max-height: 297mm; 
                      padding: 10px;
                      display: block;
                      margin: 0 auto;
                    }
                  </style>
                </head>
                <body>
                  <div class="print-container">
                    <img src="${imgData}" />
                  </div>
                </body>
              </html>
            `);
          printWindow.document.close();
          printWindow.focus();
          setTimeout(() => {
            printWindow.print();
            printWindow.close();
          }, 1000);
        } catch (error) {
          console.error('Print error:', error);
      
        }
        if (popupParent.contains(clone)) {
          popupParent.removeChild(clone);
        }
      },
    }
    
    onMounted(async () => {
      
    });

    watch(
      () => props.fk_business_id,
      () => methods.initById(props.fk_business_id),
      { immediate: true }
    )
    
    return { vars, methods };
  }
}
</script>

<style lang="scss">
.print-mode {
  h1 {
    font-size: 2.5em !important;
  }
  .business-name > h4{
    font-size: 1.2em !important;
  }
  .approval-line-table > tr > th, td {
    font-size: 0.9em !important;
  }
  .dx-field-item-label-content {
    font-size: 1.3em !important;
  }
  
  .dx-texteditor-input {
    font-size: 1.25em !important;
  }
  
  .dx-datagrid-headers .dx-header-row {
    font-size: 1.3em !important;
  }
  
  .dx-datagrid-rowsview .dx-row {
    font-size: 1.3em !important;
  }
}
.order-report {
 
  padding: 20px;
  height: 100%;
  font-size: 1.2em !important;
  // max-height: calc(100vh - 250px);
  .buttons {
    position: fixed;
    top: 80px;
    left: 40px;
    z-index: 1000;
  }
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
        justify-content: space-between;
        width: 100%;
        margin-bottom: 20px;
        .empty-space {
          width: 25%;
        }
        .business-name {
          margin-top: 0px;
          width: 50%;
          text-align: center;
          h4 {
            font-weight: bold;
          }
        }

        .content-header-approval-line {
          width: 25%;
          display: flex;
          justify-content: flex-end;
          
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