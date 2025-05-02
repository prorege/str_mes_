export default `
<style>
.acc-month td { background-color: #c7c7c7; }
tr.lined-outer { border: 1px solid #000; }
</style>
<table class="print-document" style="width: 210mm;">
  <colgroup>
    <col style="width:40%"/>
    <col style="width:60%"/>
  </colgroup>
  <thead>
    <tr>
      <th colspan="2">
        <div class="title">견 적 서</div>
        <img src="<%= _host %>/img/stech.png" style="position:absolute;top:0;right:20px;height:60px;"/>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <table>
          <colgroup>
            <col style="width:35%"/>
            <col style="width:5%"/>
            <col style="width:60%"/>
          </colgroup>
          <tr>
            <th>수 신</th>
            <td>:</td>
            <td><%= client_company %></td>
          </tr>
          <tr>
            <th>참 조</th>
            <td>:</td>
            <td><%= client_manager.name %> <%= client_manager.position %> 님</td>
          </tr>
          <tr>
            <th>T E L</th>
            <td>:</td>
            <td><%= client_manager.mobile %></td>
          </tr>
          <tr>
            <th>F A X</th>
            <td>:</td>
            <td><%= client_manager.fax %></td>
          </tr>
          <tr>
            <th>견 적 유 효 기 간</th>
            <td>:</td>
            <td><%= validity_period %></td>
          </tr>
          <tr>
            <th>품 질 보 증 기 간</th>
            <td>:</td>
            <td><%= warranty_period %></td>
          </tr>
          <tr>
            <th>인 도 조 건</th>
            <td>:</td>
            <td><%= delivery_terms %></td>
          </tr>
        </table>
      </td>
      <td>
        <table class="lined-all">
          <colgroup>
            <col style="width:20px"/>
            <col/>
            <col/>
            <col/>
            <col/>
          </colgroup>
          <tr>
            <td rowspan="7" class="">공급자</td>
            <th>등 록 번 호</th>
            <td colspan="3"><%= _company.business_number %></td>
          </tr>
          <tr>
            <th>상 호</th>
            <td><%= _company.name %></td>
            <th>대 표 자</th>
            <td style="position:relative;">
              <%= _company.ceo_name %>
              <img src="<%= _host %>/img/stamp.png" style="position:absolute;top:-34px;right:-10px;height:100px;"/>
            </td>
          </tr>
          <tr>
            <th>주 소</th>
            <td colspan="3"><%= _company.address %></td>
          </tr>
          <tr>
            <th>업 태</th>
            <td><%= _company.business_status %></td>
            <th>업 종</th>
            <td><%= _company.business_sector %></td>
          </tr>
          <tr>
            <th>T E L</th>
            <td><%= _company.phone %></td>
            <th>F A X</th>
            <td><%= _company.fax %></td>
          </tr>
          <tr>
            <th>담 당</th>
            <td><%= quote_manager.emp_name %> <%= quote_manager.emp_position %></td>
            <th>연 락 처</th>
            <td><%= quote_manager.emp_mobile %></td>
          </tr>
          <tr>
            <th>E-mail</th>
            <td colspan="3"><%= quote_manager.emp_email %></td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
      <td colspan="2">
      <table>
          <tr class="lined-outer">
            <th>제&nbsp;&nbsp;&nbsp;&nbsp;목 : </th> 
            <td colspan="2"><%= business_name %></td>
          </tr>
          <tr class="lined-outer">
            <th>견 적 금 액 :</th>
            <td>일금<%= supply_price_humanize %>원정 (₩<%= supply_price %>)</td>
            <td>[V.A.T. <%= vat_type %>]</td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
      <td colspan="2" class="align-center">
        아래와 같이 견적서를 제출합니다.
      </td>
    </tr>
    <tr>
      <td colspan="2">&nbsp;</td>
    </tr>

    <tr>
      <td colspan="2">
        <table class="lined-all">
          <colgroup>
            <col style="width:25px"/>
            <col/>
            <col/>
            <col/>
            <col/>
            <col/>
            <col/>
          </colgroup>
          <thead>
            <tr>
              <th>No.</th>
              <th>항 목</th>
              <th>규 격</th>
              <th>수 량</th>
              <th>단 가</th>
              <th>금 액</th>
              <th>비 고</th>
            </tr>
          </thead>
          <tbody>
            <% _.forEach(items, function(item, index) { %>
            <tr class="acc-month">
              <td><%= item.index %></td>
              <td><%= item.item.item_name %></td>
              <td><%= item.item.item_standard %></td>
              <td class="align-right"><%= item.quote_quantity %></td>
              <td class="align-right">₩<%= item.unit_price %></td>
              <td class="align-right">₩<%= item.supply_price %></td>
              <td><%= item.note %></td>
            </tr>
              <% if(item.children && item.children.length) _.forEach(item.children, function(child, index) { %>
                <tr>
                  <td>&nbsp;&nbsp;<%= child.index %>)</td>
                  <td><%= child.item.item_name %></td>
                  <td><%= child.item.item_standard %></td>
                  <td class="align-right"><%= child.quote_quantity %></td>
                  <td class="align-right">₩<%= child.unit_price %></td>
                  <td class="align-right">₩<%= child.supply_price %></td>
                  <td><%= child.note %></td>
                </tr>
              <% }) %>
            <% }); %>
          </tbody>
        </table>
      </td>
    </tr>

    <tr>
      <td colspan="2" class="align-center">------------- 이 하 여 백 -------------</td>
    </tr>

    <tr>
      <td colspan="2">
        <table class="lined-outer">
          <tr>
            <td>총 액</td>
            <td>₩<%= supply_price %></td>
          </tr>
        </table>
      </td>
    </tr>

    <tr>
      <td colspan="2">
        <table class="lined-all">
          <colgroup>
            <col style="width:20px"/>
            <col/>
          </colgroup>
          <td>MEMO</td>
          <td>
            <pre><%= etc %></pre>
          </td>
        </table>
      </td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td colspan="2">
        <table>
          <tr>
            <td>견적번호: <%= quote_number %></td>
            <td class="align-right">견적일자: <%= quote_date %></td>
          </tr>
        </table>
      </td>
    </tr>
  </tfoot>
</table>`