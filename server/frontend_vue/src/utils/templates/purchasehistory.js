export default `
<style>
  .text-top-right { position: absolute; top: 0px; right: 0px; }
  .dotted { border-bottom: 1px dotted black; }
  .dotted-top { border-top: 1px dotted black; }
  .subtitle2 { font-size: 14px; }
  .lined-top { border-top: 1px solid black; }
  .lined-bottom { border-bottom: 1px solid black; }
</style>
<table class="print-document">
  <thead>
    <tr>
      <th>
        <div class="title">
          매 입 일 보
          <div class="subtitle2">(공급업체 / 매입일자별)</div>
        </div>
        <div class="text-top-right">(부가세별도 금액임)</div>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>매입 기간: <%= info.startDate %> ~ <%= info.endDate %></td>
      <td class="text-right">&nbsp;</td>
    </tr>
    <tr>
      <td colspan="2">
        <table class="lined-top lined-bottom">
          <colgroup>
            <col>
            <col>
            <col style="width:120px">
            <col style="width:84px">
            <col>
            <col>
            <col>
            <col>
            <col>
            <col>
          </colgroup>
          <thead>
            <tr>
              <th>공급업체</th>
              <th>매입일자</th>
              <th colspan="4">&nbsp;</th>
            </tr>
            <tr>
              <th class="lined-bottom">거래구분/발주번호/품번</th>
              <th class="lined-bottom">품명</th>
              <th class="lined-bottom">규격</th>
              <th class="lined-bottom align-right" style="width:100px;">매입수량</th>
              <th class="lined-bottom align-right">매입가</th>
              <th class="lined-bottom align-right">금액</th>
            </tr>
          </thead>
          <tbody>
            <% _.forEach(list, function(group, index) { %>
              <tr>
                <td class="dotted"><%= group.client_company %></td>
                <td class="dotted"><%= group.dateStr %></td>
                <td class="dotted" colspan="4">&nbsp;</td>
              </tr>
              <% _.forEach(group.list, function(item, index) { %>
                <tr>
                  <td><%= item.receiving.receiving_type %> <% if (item.order_number) { %>/ <%= item.order_number %><% } %> / <%= item.item.item_code %></td>
                  <td><%= item.item.item_name %></td>
                  <td><%= item.item.item_standard %></td>
                  <td class="align-right"><%= item.receiving_quantity_s %> <%= item.item.unit %></td>
                  <td class="align-right"><%= item.unit_price_s %></td>
                  <td class="align-right"><%= item.price_s %></td>
                </tr>
              <% }); %>
              <tr>
                <td class="dotted-top" colspan="3">고객합산</td>
                <td class="dotted-top align-right"><%= group.summary.receiving_quantity %> EA</td>
                <td class="dotted-top align-right" colspan="2"><%= group.summary.price %></td>
              </tr>
              <tr>
                <td colspan="5">&nbsp;</td>
              </tr>
            <% }); %>
            <tr>
              <td class="lined-top" colspan="3">전체합산</td>
              <td class="lined-top align-right"><%= summary.receiving_quantity %> EA</td>
              <td class="lined-top align-right" colspan="2"><%= summary.price %></td>
            </tr>
          </tbody>
        </table>
      </td>
    </tr>
  </tbody>
</table>
`