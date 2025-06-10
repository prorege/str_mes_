export default `
<style>
body { margin: 0; padding: 0;  }
@media print {
  @page { size: portrait }
  .page { border: 0; }
}
.page { width: 210mm; height: 297mm; border: 1px solid #ebebeb; box-sizing: border-box; padding: 5mm; }
.page th, .page td { font-size: 13px; font-weight: bold; }
.release-subtitle { text-align: center; text-align-last: center; white-space: nowrap; font-size: 16px; margin-top: -18px; font-weight: normal; }
.release-client-name { font-size: 22px !important; }
.release-right-col { text-align: right; text-align-last: right; }
.item-table-wrap { height: 558px; border-top: 3px solid black; border-right: 3px solid black; border-left: 3px solid black; }
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

.border-3-top { border-top: 3px solid black !important; }
.border-3-bottom { border-bottom: 3px solid black !important; }
.border-3-right { border-right: 3px solid black !important; }
.border-3-left { border-left: 3px solid black !important; }

</style>
<!-- PAGE START -->
<% _.forEach(pages, function(items) { %>
<div class="page">
    <table>
      <tbody>
        <tr>
          <td colspan="2" style="font-size: 24px; border-bottom: 3px solid black !important;">에스텍아이앤씨(주)</td>
        </tr>
        <tr>
          <td><%= _company.address %> / 우) 43182</td>
          <td>본사 : TEL : <%= _company.phone %> / FAX : <%= _company.fax %></td>
        </tr>
        <tr>
          <td colspan="2">E-Mail : <%= _company.bill_email %></td>
        </tr>
      </tbody>
    </table>
    <table class="print-document">
      <colgroup>
        <col style="width:40%"/>
        <col style="width:60%"/>
      </colgroup>
      <thead>
        <tr>
          <th colspan="2">
            <div class="" style="border: 1px solid black; text-align: center; text-align-last: center; font-size: 35px; max-width: 420px; margin: 15px auto;">인수증 명세서</div>
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
              <colgroup>
                <col style="width:230px"/>
                <col/>
              </colgroup>
              <tr>
                <td class="release-right-col">일련번호 :</td>
                <td ><%= release_number %></td>
              </tr>
              <tr>
                <td class="release-right-col">거래일자 :</td>
                <td><%= release_date %></td>
              </tr>
              <tr>
                <td class="release-right-col">영업담당 :</td>
                <td><%= release_manager %></td>
              </tr>
            </table>
            <table class="lined-all" style="border: 3px solid black;">
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
                <th>성 명</th>
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
                <th>종 목</th>
                <td><%= _company.business_sector %></td>
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
                <col style="width:26px" />
                <col style="" />
                <col style="width:74px" />
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
                  <td class="align-left border-0-left"><%= item.index %></td>
                  <td><%= item.item.item_name %> <% if (item.item.item_standard) { %> / <%= item.item.item_standard %> <% } %></td>
                  <td class="align-right"><%= numeral(item.release_quantity).format('0,0') %></td>
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
                <td class="border-3-bottom border-3-left">비고</td>
                <td class="border-3-bottom"><%= etc %></td>
                <td class="border-3-bottom border-0-right">합계</td>
              </tr>
            </table>
          </td>
          <td style="padding-left: 0;">
            <table class="lined-all" style="border-left: 0;">
              <tr>
                <th>공 급 가 액</th>
                <th>부 가 세</th>
                <th class="border-3-right">총 합 계</th>
              </tr>
              <tr>
                <td class="align-center border-3-bottom"><%= supply_price %></td>
                <td class="align-center border-3-bottom"><%= vat %></td>
                <td class="align-center border-3-bottom border-3-right"><%= total_price %></td>
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
                <td class="align-center"><%= release_manager %></td>
                <td class="align-center"><%= release_manager %></td>
                <td class="align-center">&nbsp;</td>
              </tr>
            </table>
          </td>
        </tr>
      </tbody>
    </table>
    </div>
    <% }) %>
    <!-- PAGE START --> 
    <% _.forEach(pages, function(items) { %>
      <div class="page">
        <table>
          <tbody>
            <tr>
              <td colspan="2" style="font-size: 24px; border-bottom: 3px solid black !important;">에스텍아이앤씨(주)</td>
            </tr>
            <tr>
              <td>경기도 안양시 안양구 진파로 30, 624호 / 우) 43182</td>
              <td>본사 : TEL : <%= _company.phone %> / FAX : <%= _company.fax %></td>
            </tr>
            <tr>
              <td colspan="2">E-Mail : <%= _company.bill_email %></td>
            </tr>
          </tbody>
        </table>
        <table class="print-document">
          <colgroup>
            <col style="width:40%"/>
            <col style="width:60%"/>
          </colgroup>
          <thead>
            <tr>
              <th colspan="2">
                <div class="" style="border: 1px solid black; text-align: center; text-align-last: center; font-size: 35px; max-width: 420px; margin: 15px auto;">인수증 명세서</div>
                <div class="release-subtitle">( 공급자받는자 보관용 )</div>
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
                    <colgroup>
                        <col style="width:230px"/>
                        <col/>
                    </colgroup>
                    <tr>
                        <td class="release-right-col">일련번호 :</td>
                        <td ><%= release_number %></td>
                    </tr>
                    <tr>
                        <td class="release-right-col">거래일자 :</td>
                        <td><%= release_date %></td>
                    </tr>
                    <tr>
                        <td class="release-right-col">영업담당 :</td>
                        <td><%= release_manager %></td>
                    </tr>
                </table>
                <table class="lined-all" style="border: 3px solid black;">
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
                    <th>성 명</th>
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
                    <th>종 목</th>
                    <td><%= _company.business_sector %></td>
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
                    <col style="width:26px" />
                    <col style="" />
                    <col style="width:74px" />
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
                      <td class="align-left border-0-left"><%= item.index %></td>
                      <td><%= item.item.item_name %> <% if (item.item.item_standard) { %> / <%= item.item.item_standard %> <% } %></td>
                      <td class="align-right"><%= numeral(item.release_quantity).format('0,0') %></td>
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
                    <td class="border-3-bottom border-3-left">비고</td>
                    <td class="border-3-bottom"><%= etc %></td>
                    <td class="border-3-bottom border-0-right">합계</td>
                  </tr>
                </table>
              </td>
              <td style="padding-left: 0;">
                <table class="lined-all" style="border-left: 0;">
                  <tr>
                    <th>공 급 가 액</th>
                    <th>부 가 세</th>
                    <th class="border-3-right">총 합 계</th>
                  </tr>
                  <tr>
                    <td class="align-center border-3-bottom"><%= supply_price %></td>
                    <td class="align-center border-3-bottom"><%= vat %></td>
                    <td class="align-center border-3-bottom border-3-right"><%= total_price %></td>
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
                    <td class="align-center"><%= release_manager %></td>
                    <td class="align-center"><%= release_manager %></td>
                    <td class="align-center">&nbsp;</td>
                  </tr>
                </table>
              </td>
            </tr>
          </tbody>
        </table>
        </div>
      <% }) %>
      `