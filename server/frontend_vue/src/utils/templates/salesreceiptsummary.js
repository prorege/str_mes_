export default `
<style>
body { margin: 0; padding: 0; width: 210mm; }
.dotted { border-bottom: 1px dotted black; }
.dotted-top { border-top: 1px dotted black; }
.dotted-bottom { border-bottom: 1px dotted black; }
.lined-top { border-top: 1px solid black; }
.lined-bottom { border-bottom: 1px solid black; }
</style>
<table class="print-document">
  <thead>
    <tr>
      <th colspan="2">
        <div class="title">
          매 출 원 장
        </div>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <span style="font-weight:bold;">업체:</span> <%= client.name %> &nbsp;&nbsp;&nbsp;
        <span style="font-weight:bold;">사업자번호:</span> <%= String(client.business_number).replace(/(\\d{3})(\\d{2})(\\d{5})/, '$1-$2-$3') %></td>
      <td class="align-right"><%= info.startDate %> ~ <%= info.endDate %></td>
    </tr>
    <tr>
      <td colspan="2">
        <table class="lined-all">
          <colgroup>
            <col style="width:82px">
            <col style="width:94px">
            <col>
            <col>
            <col>
            <col>
            <col>
            <col>
          </colgroup>
          <thead>
            <tr>
              <th>일 자</th>
              <th>거 래 구 분</th>
              <th>품 명 및 규 격</th>
              <th>수 량</th>
              <th>단 가</th>
              <th>금 액</th>
              <th>잔 액</th>
              <th>참 고 사 항</th>
            </tr>
          </thead>
          <tbody>
            <% _.forEach(past_balance, function(item, index) { %>
              <tr>
                <td><%= moment(item.action_date).format('YYYY-MM-DD') %></td>
                <td><%= item.action_type %></td>
                <td><%= item.item_code %></td>
                <td class="align-right"><%= numeral(item.qty).format('0,0') %></td>
                <td class="align-right"><%= numeral(item.unit_price).format('0,0') %></td>
                <td class="align-right"><%= numeral(item.amount).format('0,0') %></td>
                <td class="align-right"><%= numeral(item.balance).format('0,0') %></td>
                <td class="align-right"></td>
              </tr>
            <% }); %>
            <% _.forEach(month_group, function(month, key) { %>
              <% _.forEach(month.list, function(item, index) { %>
                <tr>
                  <td><%= moment(item.action_date).format('YYYY-MM-DD') %></td>
                  <td><%= item.action_type %></td>
                  <td><%= item.item_code %></td>
                  <td class="align-right"><%= numeral(item.qty).format('0,0') %></td>
                  <td class="align-right"><%= numeral(item.unit_price).format('0,0') %></td>
                  <td class="align-right"><%= numeral(item.amount).format('0,0') %></td>
                  <td class="align-right"><%= numeral(item.balance).format('0,0') %></td>
                  <td><%= item.note %></td>
                </tr>
              <% }); %>
              <tr class="acc-month">
                <td colspan="8" style="padding:0">
                  <table>
                    <colgroup>
                      <col style="width:81px">
                      <col>
                      <col>
                      <col>
                      <col>
                    </colgroup>
                    <tr>
                      <td rowspan="2"><%= month.month %></td>
                      <td>수량합계: <%= numeral(month.monthSumQty).format('0,0') %></td>
                      <td>매출합계: <%= numeral(month.monthSumPrice).format('0,0') %></td>
                      <td>세액합계: <%= numeral(month.monthSumVat).format('0,0') %></td>
                      <td>입금합계: <%= numeral(month.monthSumDep).format('0,0') %></td>
                    </tr>
                    <tr>
                      <td>수량누계: <%= numeral(month.accSumQty).format('0,0') %></td>
                      <td>매출누계: <%= numeral(month.accSumPrice).format('0,0') %></td>
                      <td>세액누계: <%= numeral(month.accSumVat).format('0,0') %></td>
                      <td>입금누계: <%= numeral(month.accSumDep).format('0,0') %></td>
                    </tr>
                  </table>
                </td>
              </tr>
              <tr>
                <td style="border: 0">&nbsp;</td>
              </tr>
            <% }); %>
          </tbody>
        </table>
      </td>
    </tr>
    <tr>
      <td>&nbsp;</td>
      <td>
        <table style="margin-top:20px;">
          <colgroup>
            <col style="width:100px">
            <col style="">
          </colgroup>
          <tr>
            <th class="lined-bottom">일자</th>
            <td class="lined-bottom align-right">금액</td>
          </tr>
          <% _.forEach(day_group, function(item, index) { %>
            <tr>
              <th class="dotted-bottom"><%= item.date %></th>
              <td class="dotted-bottom align-right"><%= numeral(item.price).format('0,0') %></td>
            </tr>
          <% }); %>
          <tr>
            <th class="lined-top lined-bottom">합계금액</th>
            <td class="lined-top lined-bottom align-right"><%= numeral(day_group.reduce((t, i) => t += i.price, 0)).format('0,0') %></td>
          </tr>
        </table>
      </td>
    </tr>
  </tbody>
</table>
`