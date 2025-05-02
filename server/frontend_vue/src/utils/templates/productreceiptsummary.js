export default `
<style>
.border-top { border-top: 1px solid #000; }
.border-bottom { border-bottom: 1px solid #000; }
.border-left { border-left: 1px solid #000; }
.border-right { border-right: 1px solid #000; }
.border-outline { border: 1px solid #000; }

.border2-top { border-top: 2px solid #000; }
.border2-bottom { border-bottom: 2px solid #000; }

.item-row td { border-bottom: 1px solid #dbdbdb; }
.acc-month td { background-color: #c7c7c7; }
.acc-total td { background-color: #202020; color: white; } 
</style>
<table class="print-document">
  <thead>
    <tr>
      <th>
        <div class="title">
          상 품 수 불 장
          <div style="font-size:12px">(<%= info.warehouseName %>)</div>
        </div>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="text-right">(<%= info.startDate %> ~ <%= info.endDate %>)</td>
    </tr>
    <tr>
      <td>
        품목: <%= item.item_code %> &nbsp;&nbsp;
        품명: <%= item.item_name %> &nbsp;&nbsp;
        규격: <%= item.item_standard %>
      </td>
    </tr>
    <tr>
      <td colspan="2">
        <table class="">
          <colgroup>
            <col style="width:82px">
            <col>
            <col style="width:90px">
            <col>
            <col>
            <col>
            <col>
            <col>
          </colgroup>
          <thead>
            <tr>
              <th class="border2-top border2-bottom">일 자</th>
              <th class="border2-top border2-bottom">전 표 번 호</th>
              <th class="border2-top border2-bottom">거 래 구 분</th>
              <th class="border2-top border2-bottom">업 체</th>
              <th class="border2-top border2-bottom">단 가</th>
              <th class="border2-top border2-bottom">입 고 수 량</th>
              <th class="border2-top border2-bottom">출 고 수 량</th>
              <th class="border2-top border2-bottom">재 고 수 량</th>
            </tr>
          </thead>
          <tbody>
            <% _.forEach(list, function(month, index) { %>
              <% _.forEach(month.list, function(item, index) { %>
                <tr class="item-row">
                  <td><%= item.action_date %></td>
                  <td><%= item.number %></td>
                  <td><%= item.inout_type %></td>
                  <td><%= item.company %></td>
                  <td class="align-right"><%= item.unit_price_str %></td>
                  <td class="align-right"><%= item.receiving_stock_str %></td>
                  <td class="align-right"><%= item.release_stock_str %></td>
                  <td class="align-right"><%= item.sum_by_case_str %></td>
                </tr>
              <% }); %>
              <tr class="acc-month">
                <td colspan="2" class="text-center"><%= month.month %>계</td>
                <td colspan="3">&nbsp;</td>
                <td class="align-right"><%= month.mon_input_str %></td>
                <td class="align-right"><%= month.mon_output_str %></td>
                <td>&nbsp;</td>
              </tr>
              <tr class="acc-total">
                <td colspan="2" class="text-center">누계</td>
                <td colspan="3">&nbsp;</td>
                <td class="align-right"><%= month.acc_input %></td>
                <td class="align-right"><%= month.acc_output %></td>
                <td class="align-right"><%= month.acc_stock %></td>
              </tr>
            <% }); %>
          </tbody>
        </table>
      </td>
    </tr>
  </tbody>
</table>
`