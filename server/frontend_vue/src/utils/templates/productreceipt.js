export default `
<style>
  body { margin: 0; padding: 0; width: 210mm; }
  @media print {
    @page { size: portrait }
    .print-document { margin-top: 0px !important; }
  }
  .print-document { margin-top: 60px; }
  .print-document > tbody > tr > td { vertical-align: top; }
  .bom-title { text-align-last: left; font-size: 24px; }
  .headline { font-size: 16px; font-weight: bold; letter-spacing: -0.5px; margin: 14px 0 10px; }
  .bom-table { }
  .bom-table th, .bom-table td { border: 1px solid black; }
  .border-box { border: 1px solid black; padding: 12px; box-sizing: border-box; }
  .no-border { border: 0 !important; }

  .sign { float: right; border: 3px solid black; display: flex; align-items: center; font-size: 13px; }
  .sign-label { padding: 10px 20px; border-right: 3px solid black; }
  .sign-blank { padding: 10px; width: 100px; text-align: right; }
</style>
<table class="print-document">
  <colgroup>
    <col style="width:40%"/>
    <col style="width:60%"/>
  </colgroup>
  <thead>
    <tr>
      <th colspan="2">
        <div class="bom-title">제품입고증</div>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <div class="headline"><%= target_date %></div>
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
            <col style="width:54px"/>
          </colgroup>
          <tr>
            <td rowspan="3" style="font-weight: bold;">결제</td>
            <th>사 장</th>
            <th>전 무</th>
            <th>팀 장</th>
            <th>부 장</th>
            <th>계 장</th>
            <th>담 당</th>
          </tr>
          <tr style="height: 46px;">
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
            <td>&nbsp;</td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
      <td colspan="2">
        <table class="bom-table">
          <tr>
            <th>작지번호</th>
            <th>품 명</th>
            <th>단 위</th>
            <th>입 고 량</th>
            <th>입고단가</th>
            <th>입고금액</th>
            <th>비 고</th>
          </tr>
          <% _.forEach(item1, function(part, index) { %>
            <tr>
              <td><%= part.work_order_number %></td>
              <td><%= part.item.item_name %></td>
              <td><%= part.item.unit %></td>
              <td class="align-right"><%= part.production_receiving_quantity %></td>
              <td class="align-right"><%= part.unit_price %></td>
              <td class="align-right"><%= part.total_price %></td>
              <td><%= part.note %></td>
            </tr>
          <% }); %>
          <tr>
            <td colspan="3">합 계 : </td>
            <td class="align-right"><%= total_quantity %></td>
            <td>&nbsp;</td>
            <td class="align-right"><%= total_price %></td>
            <td>&nbsp;</td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
      <td colspan="2">
        <div class="sign">
          <div class="sign-label">창고담당</div>
          <div class="sign-blank text-right">(인)</div>
        </div>
      </td>
    </tr>
  </tbody>
</table>
`