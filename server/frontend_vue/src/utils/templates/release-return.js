export default `
<style>
body { margin: 0; padding: 0;  }
@media print {
  @page { size: portrait }
  .page { border: 0; }
}
.page { width: 210mm; height: 297mm; border: 1px solid #ebebeb; box-sizing: border-box; padding: 8mm; }
.page2 { width: 210mm; height: 297mm; border: 1px solid #ebebeb; box-sizing: border-box; padding: 1mm; }
.page th, .page td { font-size: 13px; font-weight: bold; }
.release-subtitle { text-align: center; text-align-last: center; white-space: nowrap; font-size: 16px; margin-top: -18px; font-weight: normal; }
.release-client-name { font-size: 22px !important; }
.release-right-col { text-align: right; text-align-last: right; }
.item-table-wrap { height: 558px; border-top: 2px solid black; border-right: 2px solid black; border-left: 2px solid black; }
.item-table th { letter-spacing: 10px; text-align: center; text-align-last: center;}
.item-table td { height: 41px; }
.dense-row table { border-top: 0; }
.dense-row > td { padding-top: 0; padding-bottom: 0; }
.summary-table table { height: 60px; }

.border-0-top { border-top-width: 0 !important; }
.border-0-bottom { border-bottom-width: 0 !important; }
.border-0-right { border-right-width: 0 !important; }
.border-0-left { border-left-width: 0 !important; }

.border-1-top { border-top: 1px solid black !important; }
.border-1-bottom { border-bottom: 1px solid black !important; }
.border-1-right { border-right: 1px solid black !important; }
.border-1-left { border-left: 1px solid black !important; }

.border-2-top { border-top: 2px solid black !important; }
.border-2-bottom { border-bottom: 2px solid black !important; }
.border-2-right { border-right: 2px solid black !important; }
.border-2-left { border-left: 2px solid black !important; }

</style>
<!-- PAGE START -->
<% if (caps) { %>
<% _.forEach(pages, function(items) { %>
<div class="page2">
<table class="print-document">
  <colgroup>
    <col style="width:40%"/>
    <col style="width:60%"/>
  </colgroup>
  <thead>
    <tr>
      <th colspan="2">
        <div class="title"><%= title %></div>
        <div class="release-subtitle">( 공급자 보관용 )</div>
        <img src="<%= _host %>/img/stech.png" style="position:absolute;top:0;right:20px;height:65px;width:140px;object-fit:contain;"/>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <table>
          <tr>
            <td class="release-client-name"><%= client_company %></td>
          </tr>
          <tr>
            <td>귀하</td>
          </tr>
        </table>
      </td>
      <td>
        <table>
          <tr>
            <td class="release-right-col">일련번호</td>
            <td>:</td>
            <td><%= return_number %></td>
          </tr>
          <tr>
            <td class="release-right-col">거래일자</td>
            <td>:</td>
            <td><%= return_date %></td>
          </tr>
          <tr>
            <td class="release-right-col">영업담당</td>
            <td>:</td>
            <td><%= return_manager %></td>
          </tr>
        </table>
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
            <th>E-mail</th>
            <td colspan="3"><%= _company.bill_email %></td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
      <td colspan="2">
        아래와 같이 (명세)합니다.
      </td>
    </tr>

    <tr class="dense-row">
      <td colspan="2">
      <div class="item-table-wrap">
        <table class="lined-all item-table">
          <colgroup>
            <col style="width:20px"/>
            <col style="width:20px"/>
            <col style=""/>
            <col style=""/>
            <col style="width:40px"/>
            <col style="width:20px"/>
            <col style="width:30px"/>
            <col style="width:30px"/>
            <col style=""/>
          </colgroup>
          <thead>
            <tr>
              <th class="border-0-top border-0-left">&nbsp;</th>
              <th class="border-0-top" style="letter-spacing: 2px;">P/O NO.</th>
              <th class="border-0-top">품목코드</th>
              <th class="border-0-top">품명 및 규격</th>
              <th class="border-0-top">수량</th>
              <th class="border-0-top">단위</th>
              <th class="border-0-top">단가</th>
              <th class="border-0-top">금액</th>
              <th class="border-0-top border-0-right">비고</th>
            </tr>
          </thead>
          <tbody>
            <% _.forEach(items, function(item, index) { %>
            <tr>
              <td class="align-center border-0-left"><%= item.index %></td>
              <td>&nbsp;</td>
              <td><%= item.item.item_code %></td>
              <td><%= item.item.item_name %> <% if (item.item.item_standard) { %> / <%= item.item.item_standard %> <% } %></td>
              <td class="align-right"><%= numeral(item.return_quantity).format('0,0') %></td>
              <td><%= item.item.unit %></td>
              <td class="align-right"><%= item.unit_price %></td>
              <td class="align-right"><%= item.supply_price %></td>
              <td class="text-ellipsis border-0-right"><%= item.note %></td>
            </tr>
            <% }); %>
          </tbody>
        </table>
        </div>
      </td>
    </tr>

    <tr class="dense-row summary-table">
      <td style="padding-right: 0;">
        <table class="lined-all">
          <colgroup>
            <col style="width:20px"/>
            <col />
            <col style="width:20px"/>
          </colgroup>
          <tr>
            <td class="border-2-bottom border-2-left">비고</td>
            <td class="border-2-bottom"><%= etc %></td>
            <td class="border-2-bottom border-0-right">합계</td>
          </tr>
        </table>
      </td>
      <td style="padding-left: 0;">
        <table class="lined-all" style="border-left: 0;">
          <tr>
            <th>공 급 가 액</th>
            <th>부 가 세</th>
            <th class="border-2-right">총 합 계</th>
          </tr>
          <tr>
            <td class="align-center border-2-bottom"><%= supply_price %></td>
            <td class="align-center border-2-bottom"><%= vat %></td>
            <td class="align-center border-2-bottom border-2-right"><%= total_price %></td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
      <td>
        본 물건을 받으시면. 동봉하여 드린 거래명세서(인수자)란에 회수 담당자 확인(사인) 후 FAX(본사) 부탁드립니다.
        원본(공급자 보관용) 은 우편발송 요청드립니다.
      </td>
      <td>
        <table class="lined-all" style="border-left: 0;">
          <tr>
            <th>담 당</th>
            <th>출 고 자</th>
            <th>인 수 자</th>
          </tr>
          <tr>
            <td class="align-center"><%= return_manager %></td>
            <td class="align-center"><%= return_manager %></td>
            <td class="align-center">&nbsp;</td>
          </tr>
        </table>
      </td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td colspan="2" class="align-right">
        일련번호: <%= return_number %>
      </td>
    </tr>
  </tfoot>
</table>
</div>
<% }) %>
<% _.forEach(pages, function(items) { %>
  <div class="page2">
  <table class="print-document">
    <colgroup>
      <col style="width:40%"/>
      <col style="width:60%"/>
    </colgroup>
    <thead>
      <tr>
        <th colspan="2">
          <div class="title"><%= title %></div>
          <div class="release-subtitle">( 공급받는자 보관용 )</div>
          <img src="<%= _host %>/img/stech.png" style="position:absolute;top:0;right:20px;height:65px;width:140px;object-fit:contain;"/>
        </th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>
          <table>
            <tr>
              <td class="release-client-name"><%= client_company %></td>
            </tr>
            <tr>
              <td>귀하</td>
            </tr>
          </table>
        </td>
        <td>
          <table>
            <tr>
              <td class="release-right-col">일련번호</td>
              <td>:</td>
              <td><%= return_number %></td>
            </tr>
            <tr>
              <td class="release-right-col">거래일자</td>
              <td>:</td>
              <td><%= return_date %></td>
            </tr>
            <tr>
              <td class="release-right-col">영업담당</td>
              <td>:</td>
              <td><%= return_manager %></td>
            </tr>
          </table>
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
              <th>E-mail</th>
              <td colspan="3"><%= _company.bill_email %></td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td colspan="2">
          아래와 같이 (명세)합니다.
        </td>
      </tr>
  
      <tr class="dense-row">
        <td colspan="2">
        <div class="item-table-wrap">
          <table class="lined-all item-table">
            <colgroup>
              <col style="width:20px"/>
              <col style="width:20px"/>
              <col style=""/>
              <col style=""/>
              <col style="width:40px"/>
              <col style="width:20px"/>
              <col style="width:30px"/>
              <col style="width:30px"/>
              <col style=""/>
            </colgroup>
            <thead>
              <tr>
                <th class="border-0-top border-0-left">&nbsp;</th>
                <th class="border-0-top" style="letter-spacing: 2px;">P/O NO.</th>
                <th class="border-0-top">품목코드</th>
                <th class="border-0-top">품명 및 규격</th>
                <th class="border-0-top">수량</th>
                <th class="border-0-top">단위</th>
                <th class="border-0-top">단가</th>
                <th class="border-0-top">금액</th>
                <th class="border-0-top border-0-right">비고</th>
              </tr>
            </thead>
            <tbody>
              <% _.forEach(items, function(item, index) { %>
              <tr>
                <td class="align-center border-0-left"><%= item.index %></td>
                <td>&nbsp;</td>
                <td><%= item.item.item_code %></td>
                <td><%= item.item.item_name %> <% if (item.item.item_standard) { %> / <%= item.item.item_standard %> <% } %></td>
                <td class="align-right"><%= numeral(item.return_quantity).format('0,0') %></td>
                <td><%= item.item.unit %></td>
                <td class="align-right"><%= item.unit_price %></td>
                <td class="align-right"><%= item.supply_price %></td>
                <td class="text-ellipsis border-0-right"><%= item.note %></td>
              </tr>
              <% }); %>
            </tbody>
          </table>
          </div>
        </td>
      </tr>
  
      <tr class="dense-row summary-table">
        <td style="padding-right: 0;">
          <table class="lined-all">
            <colgroup>
              <col style="width:20px"/>
              <col />
              <col style="width:20px"/>
            </colgroup>
            <tr>
              <td class="border-2-bottom border-2-left">비고</td>
              <td class="border-2-bottom"><%= etc %></td>
              <td class="border-2-bottom border-0-right">합계</td>
            </tr>
          </table>
        </td>
        <td style="padding-left: 0;">
          <table class="lined-all" style="border-left: 0;">
            <tr>
              <th>공 급 가 액</th>
              <th>부 가 세</th>
              <th class="border-2-right">총 합 계</th>
            </tr>
            <tr>
              <td class="align-center border-2-bottom"><%= supply_price %></td>
              <td class="align-center border-2-bottom"><%= vat %></td>
              <td class="align-center border-2-bottom border-2-right"><%= total_price %></td>
            </tr>
          </table>
        </td>
      </tr>
      <tr>
        <td>
          본 물건을 받으시면. 동봉하여 드린 거래명세서(인수자)란에 회수 담당자 확인(사인) 후 FAX(본사) 부탁드립니다.
          원본(공급자 보관용) 은 우편발송 요청드립니다.
        </td>
        <td>
          <table class="lined-all" style="border-left: 0;">
            <tr>
              <th>담 당</th>
              <th>출 고 자</th>
              <th>인 수 자</th>
            </tr>
            <tr>
              <td class="align-center"><%= return_manager %></td>
              <td class="align-center"><%= return_manager %></td>
              <td class="align-center">&nbsp;</td>
            </tr>
          </table>
        </td>
      </tr>
    </tbody>
    <tfoot>
      <tr>
        <td colspan="2" class="align-right">
          일련번호: <%= return_number %>
        </td>
      </tr>
    </tfoot>
  </table>
  </div>
  <% }) %>
<% } else { %>
<!-- PAGE START -->
<% _.forEach(pages, function(items) { %>
<div class="page">
<table class="print-document">
  <colgroup>
    <col style="width:40%"/>
    <col style="width:60%"/>
  </colgroup>
  <thead>
    <tr>
      <th colspan="2">
        <div class="title"><%= title %></div>
        <div class="release-subtitle">( 공급자 보관용 )</div>
        <img src="<%= _host %>/img/stech.png" style="position:absolute;top:0;right:20px;height:60px;"/>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <table>
          <tr>
            <td class="release-client-name"><%= client_company %></td>
          </tr>
          <tr>
            <td>귀하</td>
          </tr>
        </table>
      </td>
      <td>
        <table>
          <tr>
            <td class="release-right-col">일련번호</td>
            <td>:</td>
            <td><%= return_number %></td>
          </tr>
          <tr>
            <td class="release-right-col">거래일자</td>
            <td>:</td>
            <td><%= return_date %></td>
          </tr>
          <tr>
            <td class="release-right-col">영업담당</td>
            <td>:</td>
            <td><%= return_manager %></td>
          </tr>
        </table>
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
            <th>E-mail</th>
            <td colspan="3"><%= _company.bill_email %></td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
      <td colspan="2">
        아래와 같이 (명세)합니다.
      </td>
    </tr>

    <tr class="dense-row">
      <td colspan="2">
      <div class="item-table-wrap">
        <table class="lined-all item-table" style="table-layout:fixed">
          <colgroup>
            <col style="width:24px" />
            <col style="" />
            <col style="width:76px" />
            <col style="width:48px" />
            <col style="width:120px" />
            <col style="width:100px" />
          </colgroup>
          <thead>
            <tr>
              <th class="border-0-top border-0-left">&nbsp;</th>
              <th class="border-0-top">품명 및 규격</th>
              <th class="border-0-top">수량</th>
              <th class="border-0-top">단위</th>
              <th class="border-0-top">금액</th>
              <th class="border-0-top border-0-right">비고</th>
            </tr>
          </thead>
          <tbody>
            <% _.forEach(items, function(item, index) { %>
            <tr>
              <td class="align-center border-0-left"><%= item.index %></td>
              <td><%= item.item.item_name %> <% if (item.item.item_standard) { %> / <%= item.item.item_standard %> <% } %></td>
              <td class="align-right"><%= numeral(item.return_quantity).format('0,0') %></td>
              <td><%= item.item.unit %></td>
              <td class="align-right"><%= item.supply_price %></td>
              <td class="text-ellipsis border-0-right"><%= item.note %></td> 
            </tr>
            <% }); %>
          </tbody>
        </table>
        </div>
      </td>
    </tr>

    <tr class="dense-row summary-table">
      <td style="padding-right: 0;">
        <table class="lined-all">
          <colgroup>
            <col style="width:20px"/>
            <col />
            <col style="width:20px"/>
          </colgroup>
          <tr>
            <td class="border-2-bottom border-2-left">비고</td>
            <td class="border-2-bottom"><%= etc %></td>
            <td class="border-2-bottom border-0-right">합계</td>
          </tr>
        </table>
      </td>
      <td style="padding-left: 0;">
        <table class="lined-all" style="border-left: 0;">
          <tr>
            <th>공 급 가 액</th>
            <th>부 가 세</th>
            <th class="border-2-right">총 합 계</th>
          </tr>
          <tr>
            <td class="align-center border-2-bottom"><%= supply_price %></td>
            <td class="align-center border-2-bottom"><%= vat %></td>
            <td class="align-center border-2-bottom border-2-right"><%= total_price %></td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
      <td>
        본 물건을 받으시면. 동봉하여 드린 거래명세서(인수자)란에 회수 담당자 확인(사인) 후 FAX(본사) 부탁드립니다.
        원본(공급자 보관용) 은 우편발송 요청드립니다.
      </td>
      <td>
        <table class="lined-all" style="border-left: 0;">
          <tr>
            <th>담 당</th>
            <th>출 고 자</th>
            <th>인 수 자</th>
          </tr>
          <tr>
            <td class="align-center"><%= return_manager %></td>
            <td class="align-center"><%= return_manager %></td>
            <td class="align-center">&nbsp;</td>
          </tr>
        </table>
      </td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td colspan="2" class="align-right">
        일련번호: <%= return_number %>
      </td>
    </tr>
  </tfoot>
</table>
</div>
<% }) %>
<!-- PAGE START --> 
<% _.forEach(pages, function(items) { %>
<div class="page">
<table class="print-document">
  <colgroup>
    <col style="width:40%"/>
    <col style="width:60%"/>
  </colgroup>
  <thead>
    <tr>
      <th colspan="2">
        <div class="title"><%= title %></div>
        <div class="release-subtitle">( 공급받는자 보관용 )</div>
        <img src="<%= _host %>/img/onetech_.png" style="position:absolute;top:0;right:20px;height:60px;"/>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
        <table>
          <tr>
            <td class="release-client-name"><%= client_company %></td>
          </tr>
          <tr>
            <td>귀하</td>
          </tr>
        </table>
      </td>
      <td>
        <table>
          <tr>
            <td class="release-right-col">일련번호</td>
            <td>:</td>
            <td><%= return_number %></td>
          </tr>
          <tr>
            <td class="release-right-col">거래일자</td>
            <td>:</td>
            <td><%= return_date %></td>
          </tr>
          <tr>
            <td class="release-right-col">영업담당</td>
            <td>:</td>
            <td><%= return_manager %></td>
          </tr>
        </table>
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
            <th>E-mail</th>
            <td colspan="3"><%= _company.bill_email %></td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
      <td colspan="2">
        아래와 같이 (명세)합니다.
      </td>
    </tr>

    <tr class="dense-row">
      <td colspan="2">
      <div class="item-table-wrap">
        <table class="lined-all item-table" style="table-layout:fixed">
          <colgroup>
            <col style="width:24px" />
            <col style="" />
            <col style="width:76px" />
            <col style="width:48px" />
            <col style="width:120px" />
            <col style="width:100px" />
          </colgroup>
          <thead>
            <tr>
              <th class="border-0-top border-0-left">&nbsp;</th>
              <th class="border-0-top">품명 및 규격</th>
              <th class="border-0-top">수량</th>
              <th class="border-0-top">단위</th>
              <th class="border-0-top">금액</th>
              <th class="border-0-top border-0-right">비고</th>
            </tr>
          </thead>
          <tbody>
            <% _.forEach(items, function(item, index) { %>
            <tr>
              <td class="align-center border-0-left"><%= item.index %></td>
              <td><%= item.item.item_name %> <% if (item.item.item_standard) { %> / <%= item.item.item_standard %> <% } %></td>
              <td class="align-right"><%= numeral(item.return_quantity).format('0,0') %></td>
              <td><%= item.item.unit %></td>
              <td class="align-right"><%= item.supply_price %></td>
              <td class="text-ellipsis border-0-right"><%= item.note %></td> 
            </tr>
            <% }); %>
          </tbody>
        </table>
        </div>
      </td>
    </tr>

    <tr class="dense-row summary-table">
      <td style="padding-right: 0;">
        <table class="lined-all">
          <colgroup>
            <col style="width:20px"/>
            <col />
            <col style="width:20px"/>
          </colgroup>
          <tr>
            <td class="border-2-bottom border-2-left">비고</td>
            <td class="border-2-bottom"><%= etc %></td>
            <td class="border-2-bottom border-0-right">합계</td>
          </tr>
        </table>
      </td>
      <td style="padding-left: 0;">
        <table class="lined-all" style="border-left: 0;">
          <tr>
            <th>공 급 가 액</th>
            <th>부 가 세</th>
            <th class="border-2-right">총 합 계</th>
          </tr>
          <tr>
            <td class="align-center border-2-bottom"><%= supply_price %></td>
            <td class="align-center border-2-bottom"><%= vat %></td>
            <td class="align-center border-2-bottom border-2-right"><%= total_price %></td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
      <td>
        본 물건을 받으시면. 동봉하여 드린 거래명세서(인수자)란에 회수 담당자 확인(사인) 후 FAX(본사) 부탁드립니다.
        원본(공급자 보관용) 은 우편발송 요청드립니다.
      </td>
      <td>
        <table class="lined-all" style="border-left: 0;">
          <tr>
            <th>담 당</th>
            <th>출 고 자</th>
            <th>인 수 자</th>
          </tr>
          <tr>
            <td class="align-center"><%= return_manager %></td>
            <td class="align-center"><%= return_manager %></td>
            <td class="align-center">&nbsp;</td>
          </tr>
        </table>
      </td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td colspan="2" class="align-right">
        일련번호: <%= return_number %>
      </td>
    </tr>
  </tfoot>
</table>
</div>
<% }) %>
<% } %>
`