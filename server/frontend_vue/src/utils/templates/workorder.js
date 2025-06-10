export default `
<style>
  body { margin: 0; padding: 0;  }
  @media print {
    @page { size: portrait }
    .page { border: 0; }
  }
  .page { width: 210mm; height: 297mm; border: 1px solid #ebebeb; box-sizing: border-box; padding: 8mm; }
  .release-subtitle { text-align: center; text-align-last: center; white-space: nowrap; font-size: 16px; margin-top: -18px; font-weight: normal; }
  .release-client-name { font-size: 22px; }
  .release-right-col { text-align: right; text-align-last: right; }
  .item-table th { letter-spacing: 10px; text-align: center; text-align-last: center;}
  .summary-table table { height: 60px; }
  .lined-box { border: 1px solid #000; }
  .bottom-dotted-line { border-bottom: 1px dotted #000; }
  .bottom-solid-line { border-bottom: 1px solid #000; }
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
          <div class="title">자 재 출 고 의 뢰 서</div>
        </th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td colspan="2">
          <table>
            <colgroup>
              <col style="width: 10%;">
              <col style="width: 5%;">
              <col style="width: 35%;">
              <col style="width: 10%;">
              <col style="width: 5%;">
              <col style="width: 35%;">
            </colgroup>
            <tr>
              <th>거래처</th>
              <td>:</td>
              <td><%= client_company %></td>
              <th>작지일자</th>
              <td>:</td>
              <td><%= target_date %></td>
            </tr>
            <tr>
              <th>출고처</th>
              <td>:</td>
              <td><%= outcome_warehouse %></td>
              <th>작지번호</th>
              <td>:</td>
              <td><%= number %></td>
            </tr>
            <tr>
              <th>입고처</th>
              <td>:</td>
              <td><%= income_warehouse %></td>
              <th>출고주문번호</th>
              <td>:</td>
              <td><%= number %></td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td colspan="2">
          다음과 같이 자재출고를 의회 하오니 하기 자재를 출고하여 주시기 바랍니다.
        </td>
      </tr>
      <tr>
        <td colspan="2">
          <table class="lined-all item-table">
            <colgroup>
              <col style="width:35px" />
              <col style="" />
              <col style="" />
              <col style="" />
              <col style="width:40px" />
            </colgroup>
            <thead>
              <tr>
                <th>NO.</th>
                <th>품번</th>
                <th>품명</th>
                <th>목표량</th>
                <th>단위</th>
              </tr>
            </thead>
            <tbody>
              <% _.forEach(item1, function(item, index) { %>
              <tr>
                <td><%= index + 1 %></td>
                <td><%= item.item.item_code %></td>
                <td><%= item.item.item_name %></td>
                <td class="align-right"><%= item.required_quantity %></td>
                <td><%= item.item.unit %></td>
              </tr>
              <% }); %>
            </tbody>
          </table>
        </td>
      </tr>

      <tr>
        <td colspan="2">
          자재투입내역
        </td>
      </tr>
      <tr>
        <td colspan="2">
          <table class="lined-box item-table">
            <thead>
              <tr>
                <th class="bottom-solid-line">자재코드 / 품명 / 규격</th>
                <th class="align-right bottom-solid-line">현재고</th>
                <th class="align-right bottom-solid-line">자재투입량</th>
              </tr>
            </thead>
            <tbody>
              <% _.forEach(item2, function(item, index) { %>
              <tr>
                <td class="bottom-dotted-line">
                  <%= index + 1 %>. <%= item.item.item_code %>,
                  <%= item.item.item_name %>, 
                  <%= item.item.item_standard %>
                </td>
                <td class="align-right bottom-dotted-line"><%= numeral(parseFloat(item.basic_stock.current_stock)).format('0,0') %></td>
                <td class="align-right bottom-dotted-line"><%= numeral(parseFloat(item.required_quantity)).format('0,0') %> <%= item.item.unit %></td>
              </tr>
              <% }); %>
            </tbody>
          </table>
        </td>
      </tr>
      <tr>
        <td colspan="2">
          <%= etc %>
        </td>
      </tr>
    </tbody>
    <tfoot>
      <tr>
        <td colspan="2" class="align-right">
          작지번호: <%= number %>
        </td>
      </tr>
    </tfoot>
  </table>
  </div>
`