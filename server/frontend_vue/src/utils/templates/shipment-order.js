export default `<style>
  body { margin: 0; padding: 0; }
  @media print {
    @page { size: portrait }
    .print-document { margin-top: 0px !important; }
  }
  .page2 { width: 210mm; height: 297mm; position: relative; }
  .print-document > tbody > tr > td { vertical-align: top; }
  .print-document th, .print-document td { font-size: 14px }
  .subtitle { text-align: center; text-align-last: center; white-space: nowrap; font-size: 16px; margin: -15px 0px 14px 8px; letter-spacing: 12px; font-weight: normal; }
  .headline { font-size: 16px; font-weight: bold; letter-spacing: -0.5px; margin: -15px 0px 14px 8px; letter-spacing: 12px; }
  .border-box { border: 1px solid black; padding: 12px; box-sizing: border-box; }
  .no-border { border: 0 !important; }
  .no-border-right { border-right: 0 !important; }
  .no-border-left { border-left: 0 !important; }
  .no-border-x { border-right: 0 !important; border-left: 0 !important; }

  .sign { float: right; border: 3px solid black; display: flex; align-items: center; font-size: 13px; }
  .sign-label { padding: 10px 20px; border-right: 3px solid black; }
  .sign-blank { padding: 10px; width: 100px; text-align: right; }
  .bottom-sheet { position: absolute; bottom: 6px; left: 8px; right: 8px; }
  .item-table-wrap { height: 560px; }
  .item-table td { height: 41px; }
</style>
<% _.forEach(pages, function(items) { %>
<div class="page2">
<table class="print-document">
  <colgroup>
    <col style=""/>
    <col style="width:310px"/>
  </colgroup>
  <thead>
    <tr>
      <th colspan="2">
        <div class="title">주 문 서</div>
        <div class="subtitle">(<%= order_type %>)</div>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <table class="fixed">
          <colgroup>
            <col style="width:80px"/>
            <col style="width:20px"/>
            <col style=""/>
          </colgroup>
          <tr>
            <th>수 신</th>
            <td>:</td>
            <td style="font-size:18px"><%= client_company %></td>
          </tr>
          <tr>
            <th>전 화 번 호</th>
            <td>:</td>
            <td><%= client_manager_phone %></td>
          </tr>
          <tr>
            <th>운 송 구 분</th>
            <td>:</td>
            <td><%= transport %></td>
          </tr>
          <tr>
            <th>수 취 담 당</th>
            <td>:</td>
            <td><%= client_manager %></td>
          </tr>
          <tr>
            <th>납 품 주 소</th>
            <td>:</td>
            <td><%= delivery_place %></td>
          </tr>
          <tr>
            <th>발 주 번 호</th>
            <td>:</td>
            <td><%= client_order_number %></td>
          </tr>
        </table>
      </td>
      <td>
        <table class="lined-all fixed" style="width:auto;float:right;border:2px solid black;">
          <colgroup>
            <col style="width:30px"/>
            <col style="width:54px"/>
            <col style="width:54px"/>
            <col style="width:54px"/>
            <col style="width:54px"/>
            <col style="width:54px"/>
          </colgroup>
          <tr>
            <td rowspan="3" style="font-weight: bold;">결제</td>
            <th>담 당</th>
            <th>검 토</th>
            <th>확 인 1</th>
            <th>확 인 2</th>
            <th>승 인</th>
          </tr>
          <tr style="height: 46px;">
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td style="padding:0;text-align:center;"><%= _company.ceo_name %></td>
          </tr>
          <tr style="height: 20px;">
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td style="font-size:10px;padding:0;text-align:center;"><%= procDateShort %></td>
          </tr>
        </table>
        <table class="fixed">
          <colgroup>
            <col style="width:80px"/>
            <col style="width:20px"/>
            <col style=""/>
          </colgroup>
          <tr>
            <th>수 주 번 호</th>
            <td>:</td>
            <td><%= order_number %></td>
          </tr>
          <tr>
            <th>작 성 일</th>
            <td>:</td>
            <td><%= moment(created).format('YYYY년 MM월 DD일') %></td>
          </tr>
          <tr>
            <th>작 성 자</th>
            <td>:</td>
            <td><%= order_manager %></td>
          </tr>
          <tr>
            <th>담 당 자</th>
            <td>:</td>
            <td><%= order_manager %></td>
          </tr>
          <tr>
            <th>전 결 일 자</th>
            <td>:</td>
            <td></td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
      <td colspan="2">
        다음의 내역과 같이 (정기, 수시) 주문합니다.
      </td>
    </tr>
    <tr>
      <td colspan="2">
      <div class="item-table-wrap">
        <table class="lined-all item-table">
          <colgroup>
            <col style="width:40px">
            <col>
            <col>
            <col>
            <col>
            <col style="width:100px">
            <col style="width:80px">
          </colgroup>
          <thead>
            <tr>
              <th>번 호</th>
              <th>품 명</th>
              <th>수 량</th>
              <th>단 가</th>
              <th>금 액</th>
              <th>출 하 예 정 일</th>
              <th>참 고</th>
            </tr>
          </thead>
          <tbody>
            <% _.forEach(items, function(item, index) { %>
              <tr>
                <td><%= item.index %></td>
                <td>
                  <%= item.item.item_name %>
                  <% if (item.note) { %>
                    <div class="caption">(<%= item.note %>)</div>
                  <% } %>
                </td>
                <td class="align-right">
                  <%= numeral(item.order_quantity).format('0,0') %>
                  &nbsp;<%= item.item.unit %>
                </td>
                <td class="align-right"><%= numeral(item.unit_price).format('0,0') %></td>
                <td class="align-right"><%= numeral(item.supply_price).format('0,0') %></td>
                <td>
                  <%= item.request_delivery_date && moment(item.request_delivery_date).format('YYYY-MM-DD') %>
                </td>
                <td><%= item.note %></td>
              </tr>
            <% }); %>
          </tbody>
          <tfoot>
          <% if(items['total_supply_price']) { %>
            <tr>
              <td colspan="3" class="align-right no-border-right"><b>합 계 금 액 :</b></td>
              <td colspan="2" class="align-right no-border-x">
                <%= items['total_supply_price'] %>
              </td>
              <td colspan="2" class="no-border-left">&nbsp;</td>
            </tr>
            <% } %>
            <tr>
            <td colspan="7" class="">&nbsp;</td>
           </tr>
           <tr>
            <td class="" style="">비고</td> 
            <td colspan="6" class="" style=""><%= etc %></td>
           </tr>
          </tfoot>
        </table>
        </div>
      </td>
    </tr>
  </tbody>
</table>

<div class="bottom-sheet">
  <div style="display:flex; justify-content: space-between; align-items: flex-end;">
    <table class="lined-all" style="width:220px;">
      <colgroup>
        <col style="width:97px;"/>
        <col />
      </colgroup>
      <tr>
        <th>전월말 미수금액</th>
        <td class="align-right"><%= numeral(balance.receivable_balance).format('0,0') %></td>
      </tr>
      <tr>
        <th>당 월 매출 금액</th>
        <td class="align-right"><%= numeral(balance.release_balance).format('0,0') %></td>
      </tr>
      <tr>
        <th>당 월 수금 금액</th>
        <td class="align-right"><%= numeral(balance.deposit_balance).format('0,0') %></td>
      </tr>
      <tr>
        <th>현 미수금</th>
        <td class="align-right"><%= numeral(balance.current_balance).format('0,0') %></td>
      </tr>
    </table>
    <div style="font-size: 12px;">
      [출력시간: <%= moment().format('YYYY-MM-DD HH:mm:ss') %>]
    </div>
  </div>
  <hr />
  <div style="display:flex; justify-content: space-between; font-size: 12px;">
    <div>수주번호: <%= order_number %> &nbsp;&nbsp;&nbsp; 업체명: <%= client_company %></div>
    <div><%= _company.name %></div>
  </div>
</div>
</div>
<% }) %>
`