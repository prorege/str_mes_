export default `
<style>
  body { margin: 0; padding: 0;  }
  @media print {
    @page { size: portrait }
    .page { border: 0; }
  }
  .page { width: 210mm; height: 297mm; box-sizing: border-box; position:relative; }
  .approval_title { font-size: 36px; width: 100%; margin: 20px auto; display:flex; flex-wrap: nowrap; justify-content: space-between;}
  .font-size-12 td { font-size: 12px; font-weight: bold; !important }
  .font-size-17 { font-size: 20px; font-weight: bold; !important }
  .page th,
  .page th, td { 
    font-size:15px; font-weight: bold; 
    !important;
  }
  .approval_table th,
  .approval_table td {
     font-size: 13px; 
  }
</style>
<div class="page">
  <table class="print-document">
    <colgroup>
      <col style="width:50%"/>
      <col style="width:50%"/>
    </colgroup>
    <thead>
      <tr>
        <th colspan="2">
          <div class="approval_title">
            <div style="width: 33.33%;">&nbsp;</div>
            <div style="width: 33.33%;">품 의 서</div>
            <div style="width: 33.33%; font-size: 28px; display: flex; justify-content: flex-end; align-items: flex-end;">(<%= order_type %>)</div>
          </div>
        </th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>
          <table>
            <tr style="padding-bottom: 10px;">
              <td class="font-size-17" style="width:80px;">품의번호</td>
              <td style="width:0px; padding:0">:</td>
              <td colspan="3" class="font-size-17"><%= order_number %></td>
            </tr>
            <tr style="padding-bottom: 10px;">
              <td class="font-size-17" style="width:80px;">업 체 명</td>
              <td style="width:0px; padding:0">:</td>
              <td colspan="3" class="font-size-17"><%= client_company %></td>
            </tr>
            <tr style="padding-bottom: 10px;">
              <td class="" style="width:80px;">발주담당</td>
              <td style="width:0px; padding:0">:</td>
              <td colspan="3" class="">
                <% if (order_manager) { %>
                <%= order_manager.emp_name %>
                <% } %>
              </td>
            </tr>
            <tr style="">
              <td class="" style=" width:80px;">발 주 일</td>
              <td style="width:0px; padding:0">:</td>
              <td colspan="3" class=""><%= order_date %></td>
            </tr>
          </table>
        </td>
        <td>
          <div style="padding: 10px;">
            <div class="font-size-17" style="padding-bottom: 10px;"><%= _company.name %></div>
            <div style="padding: 4px 0;" class="font-size-14"><%= _company.address %></div>
          </div>
          <table class="lined-all fixed approval_table">
            <colgroup>
              <col style="width:20px"/>
              <col style="width:45px"/>
              <col style="width:45px"/>
              <col style="width:45px"/>
              <col style="width:45px"/>
              <col style="width:45px"/>
              <col style="width:45px"/>
            </colgroup>
            <tr>
              <td rowspan="3" style="" class="align-center">결재</td>
              <th>사 장</th>
              <th>전 무</th>
              <th>팀 장</th>
              <th>부 장</th>
              <th>계 장</th>
              <th>담 당</th>
            </tr>
            <tr style="height: 46px;" class="align-center">
              <td class="">
                <% if (approve_manager) { %>
                <%= approve_manager %>
                <% } %>
              </td>
              <td>&nbsp;</td>
              <td class="">
                <% if (confirmed_manager) { %>
                <%= confirmed_manager %>
                <% } %>
              </td>
              <td>&nbsp;</td>
              <td>&nbsp;</td>
              <td class=""><%= order_manager.emp_name %></td>
            </tr>
            <tr style="" class="align-center font-size-12">
              <td class="">
                  <% if (approve_date) { %>
                  <%= moment(approve_date).format('YYMMDD') %>
                  <% } %>
              </td>
              <td>&nbsp;</td>
              <td class="">
                  <% if (confirmed_date) { %>
                  <%= moment(confirmed_date).format('YYMMDD') %>
                  <% } %>
              </td>
              <td>&nbsp;</td>
              <td>&nbsp;</td>
              <td class=""><%= order_date_short %></td>
            </tr>
          </table>
        </td>
      </tr>
      <tr><td colspan="2">&nbsp;</td></tr>
      <tr>
        <td colspan="2" class="align-left" style="padding-bottom: 10px;">
          1. 하기 품목을 (외주, 구입)코저 하오니 재가하여 주시기 바랍니다.
        </td>
      </tr>
      <tr>
        <td colspan="2" class="align-left font-size-17" style="padding-bottom: 15px;">
          합계금액: WON <%= numeral(total_price).format('0,0') %>
        </td>
      </tr>
      <tr>
        <td colspan="2">
          <table class="lined-all">
            <colgroup>
              <col style="width:40px">
              <col>
              <col>
              <col>
              <col>
              <col style="width:100px">
              <col style="width:40px">
            </colgroup>
            <thead>
              <tr>
                <th>번 호</th>
                <th>품 명</th>
                <th>규 격</th>
                <th>수 량</th>
                <th>단 가</th>
                <th>금 액</th>
                <th>요 청 납 기</th>
              </tr>
            </thead>
            <tbody>
              <% _.forEach(items, function(item, index) { %>
              <tr>
                <td><%= index + 1 %></td>
                <td>
                  <%= item.item.item_name %>
                  <% if (item.note) { %>
                    <div class="caption">(<%= item.note %>)</div>
                  <% } %>
                </td>
                <td><%= item.item.item_standard %></td>
                <td class="align-right"><%= item.order_quantity %> <%= item.item.unit %></td>
                <td class="align-right"><%= item.unit_price %></td>
                <td class="align-right"><%= numeral(item.supply_price).format('0,0') %></td>
                <td><%= item.request_delivery_date  %></td>
              </tr>
              <% }); %>
            </tbody>
            <tfoot>
              <tr>
                <td colspan="5" class="align-center"><b>공 급 가&nbsp;&nbsp;합 계</b></td>
                <td class="align-right"><%= numeral(supply_price).format('0,0') %></td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td colspan="5" class="align-center"><b>부 가 세</b></td>
                <td class="align-right"><%= numeral(tax_price).format('0,0') %></td>
                <td>&nbsp;</td>
              </tr>
              <tr>
                <td colspan="5" class="align-center"><b>합 계 금 액</b></td>
                <td class="align-right"><%= numeral(total_price).format('0,0') %></td>
                <td>&nbsp;</td>
              </tr>
            </tfoot>
          </table>
        </td>
      </tr>
      <tr><td>&nbsp;</td></tr>
      <tr>
        <td colspan="2" >
          <div class="align-left" style="display: flex; align-items: flex-start;">
            <span>비고</span>
            <span>&nbsp;&nbsp;:&nbsp;&nbsp;</span>
            <span style="white-space: pre-line; display: inline-block"><%= etc %></span>
           </div>
        </td>
      </tr>
    </tbody>
  </table>
  <div style="border-top: 2px solid #000000; padding-top:3px; padding-bottom: 3px; font-weight: bold; position: absolute; bottom: 0; width: 210mm; box-sizing: border-box;">품의번호: <%= order_number %></div>
</div>
`