export default `
<style>
  body { margin: 0; padding: 0; width: 297mm; }
  @media print {
    @page { size: landscape }
    .print-document { margin-top: 0px !important; }
  }
  .print-document { margin-top: 60px; padding: 0px 20px 20px 20px; }
  .print-document > tbody > tr > td { vertical-align: top; }
  .headline { font-size: 16px; font-weight: bold; letter-spacing: -0.5px; margin: 14px 0 10px; }
  
  .sheet th, sheet td { text-align-last: auto; }
  .sheet th { text-align: center; }
  .underline { border-width: 0; border-bottom-width: 1px; border-color: #d7d7d7; }
  .underline.dashed { border-style: dashed; }
  .underline.solid { border-style: solid; }
  .underline.solid-lg { border-style: solid; border-bottom-width: 3px; }

  .upperline { border-width: 0; border-top-width: 3px; border-color: #d7d7d7; border-style: solid; }
</style>
<div class="print-document">
<table class="sheet">
  <colgroup>
    <col style="width:30px" />
    <col />
    <col />
    <col />
    <col />
    <col />
    <col />
    <col />
    <col />
    <col />
  </colgroup>
  <thead>
    <tr>
      <th colspan="10" class="align-center" style="font-size: 28px;">수입원가 리스트</th>
    </tr>
    <tr>
      <th colspan="10" class="align-center" style="font-size: 18px; font-weight: normal;">( 통관번호별 )</th>
    </tr>
    <tr>
      <th colspan="10">&nbsp;</th>
    </tr>
    <tr>
      <th colspan="2">통관번호: <%= clearance_number %></th>
      <th>통관일자: <%= moment(clearance_date).format('YYYY-MM-DD') %></th>
      <th>공급자: <%= supplier %></th>
      <th colspan="7"></th>
    </tr>
    <tr>
      <th class="underline solid-lg" colspan="2"></th>
      <th class="underline solid-lg" colspan="5">
        Invoice No.: <%= clearance_number %> &nbsp;&nbsp;&nbsp;
        B/L결제시의 환율: 1<%= currency %>당 ₩<%= numeral(ex_rate).format('0,0.00') %>
      </th>
      <th class="underline solid-lg" colspan="3" class="align-right">(수입원가는 VAT 별도금액임)</th>
    </tr>
    <tr>
      <th class="underline solid">일련번호</th>
      <th class="underline solid" colspan="2">오더번호/바이어명/품명</th>
      <th class="underline solid">통관수량</th>
      <th class="underline solid">단가(외환)</th>
      <th class="underline solid">수입금액(외환)</th>
      <th class="underline solid">수입금액(₩)</th>
      <th class="underline solid">환산단가(₩)</th>
      <th class="underline solid">수입원가(₩)</th>
      <th class="underline solid">비용부가율</th>
    </tr>
  </thead>
  <tbody>
    <% _.forEach(list, function(item, index) { %>
    <tr>
      <td class="underline dashed align-center" rowspan="2"><%= index + 1 %></td>
      <td><%= clearance_number %></td>
      <td><%= buyer %></td>
      <td colspan="6"></td>
    </tr>
    <tr>
      <td class="underline dashed" colspan="2"><%= item.item.item_name %></td>
      <td class="underline dashed align-right"><%= numeral(item.qty).format('0,0') %></td>
      <td class="underline dashed align-right"><%= numeral(item.import_price).format('0,0.0000') %></td>
      <td class="underline dashed align-right"><%= numeral(item.amount).format('0,0.0000') %></td>
      <td class="underline dashed align-right"><%= numeral(item.won_amount).format('0,0.00') %></td>
      <td class="underline dashed align-right"><%= numeral(item.won_price).format('0,0') %></td>
      <td class="underline dashed align-right"><%= numeral(item.cost_price).format('0,0') %></td>
      <td class="underline dashed align-right"><%= numeral(item.cost_rate).format('0,0.00') %></td>
    </tr>
    <% }); %>
    </tbody>
    <tfoot>
      <tr>
        <td class="upperline align-center" colspan="3">합 계</td>
        <td class="upperline align-right"><%= numeral(list.reduce((t, a) => t += a.qty, 0)).format('0,0') %></td>
        <td class="upperline align-right"></td>
        <td class="upperline align-right"><%= numeral(list.reduce((t, a) => t += Number(a.amount), 0)).format('0,0.0000') %></td>
        <td class="upperline align-right"><%= numeral(list.reduce((t, a) => t += a.won_amount, 0)).format('0,0.00') %></td>
        <td class="upperline align-right"></td>
        <td class="upperline align-right"><%= numeral(total_price_cost).format('0,0') %></td>
        <td class="upperline align-right"><%= numeral(list.reduce((t, a) => t += Number(a.cost_rate), 0)).format('0,0.00') %></td>
      </tr>
    </tfoot>
</table>
</div>
`