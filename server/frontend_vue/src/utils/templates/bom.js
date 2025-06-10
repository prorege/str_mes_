export default `
<style>
  body { margin: 0; padding: 0; width: 297mm; }
  @media print {
    @page { size: landscape }
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

  .t-bold { border-top-width: 3px !important; }
  .l-bold { border-left-width: 3px !important; }
  .r-bold { border-right-width: 3px !important; }
  .b-bold { border-bottom-width: 3px !important; }
</style>
<table class="print-document">
  <colgroup>
    <col style="width:40%"/>
    <col style="width:60%"/>
  </colgroup>
  <thead>
    <tr>
      <th colspan="2">
        <div class="bom-title">Part List ( BOM )</div>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <div class="headline">생산품목: <%= item.item_code %> * <%= item.item_name %> *</div>
        <table class="bom-table">
          <tr>
            <th class="t-bold l-bold">구분</th><th class="t-bold r-bold">금액(원)</th>
          </tr>
          <tr>
            <th class="l-bold">자재원가</th><td class="r-bold align-right"><%= costs.partCost %></td>
          </tr>
          <tr>
            <th class="l-bold">노무비</th><td class="r-bold align-right"><%= costs.laborCost %></td>
          </tr>
          <tr>
            <th class="l-bold b-bold">제조경비+감가비</th><td class="b-bold r-bold align-right"><%= costs.produceCost %></td>
          </tr>
          <tr>
            <th>외주가공비</th><td class="align-right"><%= costs.outSourceCost %></td>
          </tr>
          <tr>
            <th>제조원가</th><td class="align-right"><%= costs.produceTotalCost %></td>
          </tr>
          <tr>
            <th>판관비</th><td class="align-right"><%= costs.operatingCost %></td>
          </tr>
          <tr>
            <th class="t-bold l-bold b-bold">매출원가</th>
            <td class="t-bold r-bold b-bold align-right"><%= costs.salesPrice %></td>
          </tr>
        </table>
      </td>
      <td>
        <div class="headline">[실제 정전개 공정 절차표]</div>
        <table class="bom-table">
          <tr>
            <th>생산공정/품목</th><th>공임가(원)</th><th>공임액(원)</th><th>작업시간(분)</th>
          </tr>
          <% _.forEach(processList, function(prc, index) { %>
            <tr>
              <td><%= prc.title %></td>
              <td class="align-right"><%= prc.price_humanize %></td>
              <td class="align-right"><%= prc.price_total_humanize %></td>
              <td class="align-right"><%= prc.ct %></td>
            </tr>
          <% }); %>
        </table>
      </td>
    </tr>
    <tr>
      <td colspan="2">
        <div class="headline">[ Part List ]</div>
        <table class="bom-table">
          <tr>
            <th>자재코드</th>
            <th>품 명</th>
            <th>재 질</th>
            <th>순소요량</th>
            <th>손실율</th>
            <th>소요량</th>
            <th>자재가(원)</th>
            <th>자재금액(원)</th>
            <th>주공급원</th>
          </tr>

          <% _.forEach(partList, function(part, index) { %>
            <tr>
              <td><%= part.item.item_code %></td>
              <td><%= part.item.item_name %></td>
              <td><%= part.item.item_standard %></td>
              <td><%= part.requirement %></td>
              <td><%= part.lrate %>%</td>
              <td><%= part.requirement + part.requirement * (part.lrate / 100.0) %></td>
              <td class="align-right"><%= part.purchase_price_humanize %></td>
              <td class="align-right"><%= part.purchase_price_total_humanize %></td>
              <td><%= part.client_company %></td>
            </tr>

            <% if (part.children && part.children.length) _.forEach(part.children, function(childPart, index) { %>
              <tr>
                <td><%= childPart.item.item_code %></td>
                <td><%= childPart.item.item_name %></td>
                <td><%= childPart.item.item_standard %></td>
                <td><%= childPart.requirement %></td>
                <td><%= childPart.lrate %>%</td>
                <td><%= childPart.requirement + childPart.requirement * (childPart.lrate / 100.0) %></td>
                <td class="align-right"><%= childPart.purchase_price_humanize %></td>
                <td class="align-right"><%= childPart.purchase_price_total_humanize %></td>
                <td><%= childPart.client_company %></td>
              </tr>
            <% }) %>
          <% }); %>
        </table>
      </td>
    </tr>
    <tr>
      <td colspan="2">
        <div class="headline">[ History 관리 내역 ]</div>
        <table class="bom-table">
          <tr>
            <th>입력일</th>
            <th>입력사원</th>
            <th>사유(내용)</th>
            <th>중요</th>
          </tr>

          <% _.forEach(historyList, function(item, index) { %>
            <tr>
              <td><%= item.created %></td>
              <td><%= item.manager %></td>
              <td><%= item.detail %></td>
              <td><%= item.important_yn %></td>
            </tr>
          <% }); %>
        </table>
      </td>
    </tr>
  </tbody>
</table>
`