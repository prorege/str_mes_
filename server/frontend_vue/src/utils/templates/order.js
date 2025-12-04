export default `
<style>
.env-table th { text-align: center; text-align-last: center; }
.caption { font-size: 60%; }
.font-size-18 { font-size: 15px; }
.font-size-18 td,
.font-size-18 th {
  font-size: 15px; font-weight: bold;
}
.font-size-13 {
  font-size: 13px; 
}
.font-size-13 td,
.font-size-13 th {
  font-size: 13px;
  font-weight: bold;
}
.header-color {
  background-color:rgb(190, 183, 230);
}
.font-size-12 {
  font-size: 12px;
}
.font-size-12 td,
.font-size-12 th {
  font-size: 12px;
  font-weight: bold;
}
</style>
<table class="print-document" style="width: 210mm;">
  <colgroup>
    <col style="width:50%"/>
    <col style="width:50%"/>
  </colgroup>
  <thead>
    <tr>
      <th colspan="2">
        <div class="title">발 주 서</div>
        <div style="display:flex;justify-content:center;margin-top:-15px;"><div style="font-size: 18px;" class="">( <%= order_type %> )</div></div>
        <img src="<%= _host %>/img/str.png" style="position:absolute;top:0;right:20px;height:65px;width:140px;object-fit:contain;"/>
      </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="width: 60%;">
        <table class="font-size-13">
          <colgroup>
            <col style="width:80px;"/>
            <col style="width:0px;"/>
            <col/>
            <col/>
            <col/>
          </colgroup>
          <tr>
            <td>수신</td>
            <td>:</td>
            <td colspan="3" class=""><%= client_company %></td>
          </tr>
          <tr>
            <td>발주번호</td>
            <td>:</td>
            <td colspan="3"><%= order_number %></td>
          </tr>
          <tr>
            <td>발주일자</td>
            <td>:</td>
            <td colspan="3"><%= order_date %></td>
          </tr>
          <tr>
            <td>사업명</td>
            <td>:</td>
            <td colspan="3">
              <% if (project_management) { %>
                <%= project_management.project_name %>
              <% } %>
            </td>
          </tr>
          <tr>
          <tr>
            <td>사업번호</td>
            <td>:</td>
            <td colspan="3">
              <% if (project_management) { %>
                <%= project_management.project_number %>
              <% } %>
            </td>
          </tr>
        </table>
      </td>
      <td style="width: 40%;">
        <table class="lined-all" style="text-align: center;">
          <colgroup>
            <col style="width:10%"/>
            <col style="width:30%"/>
            <col style="width:30%"/>
            <col style="width:30%"/>
          </colgroup>
          <tr>
            <td rowspan="2" style="writing-mode: vertical-rl; text-align: center; font-weight: bold;">결 재</td>
            <td style="font-weight: bold;">담 당</td>
            <td style="font-weight: bold;">실 장</td>
            <td style="font-weight: bold;">대 표 이 사</td>
          </tr>
          <tr>
            <td style="height: 100px;"></td>
            <td style="height: 100px;"></td>
            <td style="height: 100px;"></td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
      <td colspan="2">&nbsp;</td>
    </tr>

    <tr>
      <td colspan="2" class="align-left font-size-13" style="font-weight: bold;">
        1. 물품의표시.
      </td>
    </tr>
    
    <tr>
      <td colspan="2">
        <table class="lined-all">
          <colgroup>
            <col style="width:40px">
            <col>
            <col>
            <col style="width:40px">
            <col>
            <col>
            <col>
            <col style="width:100px">
          </colgroup>
          <thead>
            <tr class="header-color">
              <th>번 호</th>
              <td style="font-weight: bold; text-align: center;">품 명</td>
              <td style="font-weight: bold; text-align: center;">규 격</td>
              <th style="font-weight: bold;">단 위</th>
              <th style="font-weight: bold;">수 량</th>
              <th style="font-weight: bold;">단 가</th>
              <th style="font-weight: bold;">금 액</th>
              <th>요 청 납 기</th>
            </tr>
          </thead>
          <tbody>
            <% _.forEach(items, function(item, index) { %>
            <tr>
              <td><%= index + 1 %></td>
              <td>
                <%= item.item.item_name %>
                <% if (item.note) { %>
                  <div>(<%= item.note %>)</div>
                <% } %>
              </td>
              <td><%= item.item.item_standard %></td>
              <td><%= item.item.unit %></td>
              <td class="align-right"><%= item.order_quantity %></td>
              <td class="align-right"><%= item.unit_price %></td>
              <td class="align-right"><%= numeral(item.supply_price).format('0,0') %></td>
              <td><%= item.request_delivery_date  %></td>
            </tr>
            <% }); %>
            <% if (delivery_price > 0) { %>
            <tr>
              <td></td>
              <td>운송비</td>
              <td colspan="7"><%= numeral(delivery_price).format('0,0') %></td>
            </tr>
            <% } %>
            <% if (_note) { %>
            <tr>
              <td></td>
              <td>비고</td>
              <td colspan="7"><%= _note %></td>
            </tr>
            <% } %>
          </tbody>
          <tfoot>
            <tr>
              <td colspan="6" class="align-center"><b>공 급 가&nbsp;&nbsp;합 계</b></td>
              <td class="align-right"><%= numeral(supply_price).format('0,0') %></td>
              <td>&nbsp;</td>
            </tr>
            <tr>
              <td colspan="6" class="align-center"><b>부 가 세</b></td>
              <td class="align-right"><%= numeral(tax_price).format('0,0') %></td>
              <td>&nbsp;</td>
            </tr>
            <tr>
              <td colspan="6" class="align-center"><b>합 계 금 액</b></td>
              <td class="align-right"><%= numeral(total_price).format('0,0') %></td>
              <td>&nbsp;</td>
            </tr>
          </tfoot>
        </table>
      </td>
    </tr>
    <tr>
      <td colspan="2" class="align-left font-size-13" style="font-weight: bold;">
        2. 계약조건.
      </td>
    </tr>
    <tr>
      <td colspan="2" style="width: 100%; padding-bottom: 0;">
        <table class="font-size-13">
          <colgroup>
            <col style="width: 50%;">
            <col style="width: 50%;">
          </colgroup>
          <tr>
            <td style="padding: 0;">
              <table class="lined-outer" style="border-right: 0; text-align: center;">
                <tr>
                  <td>납품장소</td>
                  <td><% if (delivery_place) { %><%= delivery_place %><% } %></td>
                </tr>
                <tr>
                  <td>납품일자</td>
                  <td><% if (delivery_date) { %><%= delivery_date %><% } %></td>
                </tr>
                <tr>
                  <td>지불조건</td>
                  <td><% if (payment_terms) { %><%= payment_terms %><% } %></td>
                </tr>
                <tr>
                  <td>운임부담</td>
                  <td>계약자</td>
                </tr>
                <tr>
                  <td>&nbsp;</td>
                  <td>&nbsp;</td>
                </tr>
              </table>
            </td>
            <td style="padding: 0;">
              <table class="lined-outer" style="text-align: center;">
                <tr>
                  <td>검수방법</td>
                  <td>발주처 및 당사 담당자 확인</td>
                </tr>
                <tr>
                  <td>계약보증</td>
                  <td>증권</td>
                </tr>
                <tr>
                  <td>하자보증</td>
                  <td>증권</td>
                </tr>
                <tr>
                  <td>지체보상금</td>
                  <td>3/1000</td>
                </tr>
                <tr>
                  <td>하자기간</td>
                  <td><% if (ref_number) { %><%= ref_number %><% } %></td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </td>
    </tr>
    <tr>
     <td colspan="2" style="padding-top: 0; padding-bottom: 0;">
        <table class="lined-outer" style="border-top: 0; border-bottom: 0; ">
          <tr>
            <td>
              상기 조건에 명시되지 아니한 사항은 관례에 따르고 합의 계약사항에 이의가 있을 때에는 주문자의 해석에 따른다.
            </td>
          </tr>
          <tr>
            <td>
              특기사항 : 수신후 도장날인하여 회신 바랍니다.
            </td>
          </tr>
        </table>
      </td>
    </tr>
     <tr>
      <td colspan="2" style="width: 100%; padding-bottom: 0; padding-top: 0;">
        <table class="font-size-12">
          <colgroup>
            <col style="width: 50%;">
            <col style="width: 50%;">
          </colgroup>
          <tr>
            <td style="padding: 0;">
              <table class="lined-outer" style="border-right: 0; text-align: center;">
                <tr>
                  <td style="width: 20%; padding-right: 0;">주문자</td>
                  <td style="width: 35%; text-align: left; padding-left: 0; padding-right: 0;"><%= _company.name %></td>
                  <td style="width: 18%; padding-left: 0; padding-right: 0; text-align: left;">대표이사</td>
                  <td style="width: 27%; position:relative; text-align: left; padding-left: 0;"><%= _company.ceo_name %>  <img src="<%= _host %>/img/stamp.png" style="position:absolute;top:-34px;right:25px;height:80px;"/></td>
                </tr>
                <tr>
                  <td style="width: 20%; padding-right: 0;">담당자</td>
                  <td style="width: 35%; text-align: left; padding-left: 0; padding-right: 0;"><% if (project_management) { %><%= project_management.project_manager %>&nbsp;<%= project_management.project_manager_position %><% } %></td>
                  <td style="width: 18%; padding-left: 0; padding-right: 0; text-align: left;">이메일</td>
                  <td style="width: 27%; text-align: left; padding-left: 0;"><% if (project_management) { %><%= project_management.project_manager_email %><% } %></td>
                </tr>
                <tr>
                  <td style="width: 20%; padding-right: 0;">전&nbsp;&nbsp;&nbsp;화</td>
                  <td colspan="3" style="width: 80%; text-align: left; padding-left: 0;"><%= _company.phone %></td>
                </tr>
                <tr>
                  <td style="width: 20%; padding-right: 0;">팩&nbsp;&nbsp;&nbsp;스</td>
                  <td colspan="3" style="width: 80%; text-align: left; padding-left: 0;"><%= _company.fax %></td>
                </tr>
                <tr>
                  <td style="width: 20%; padding-right: 0;">핸드폰</td>
                  <td colspan="3" style="width: 80%; text-align: left; padding-left: 0;"><% if (project_management) { %><%= project_management.project_manager_mobile %><% } %></td>
                </tr>
              </table>
            </td>
            <td style="padding: 0;">
              <table class="lined-outer" style="text-align: center;">
                <tr>
                  <td style="width: 20%; padding-right: 0;">납품자</td>
                  <td style="width: 35%; text-align: left; padding-left: 0; padding-right: 0;"><%= client_company %></td>
                  <td style="width: 18%; padding-left: 0; padding-right: 0; text-align: left;">대표이사</td>
                  <td style="width: 27%; position:relative; text-align: left; padding-left: 0;">
                    <% if (client_manager) { %>
                      <%= client_manager.ceo_name %>
                    <% } %>
                  </td>
                </tr>
                <tr>
                  <td style="width: 20%; padding-right: 0;">담당자</td>
                  <td colspan="3" style="width: 80%; text-align: left; padding-left: 0;">
                    <% if (client_manager) { %>
                    <%= client_manager.name %> <%= client_manager.position %> 님
                    <% } %>
                  </td>
                </tr>
                <tr>
                  <td style="width: 20%; padding-right: 0;">전&nbsp;&nbsp;&nbsp;화</td>
                  <td colspan="3" style="width: 80%; text-align: left; padding-left: 0;"><% if (client_manager) { %><%= client_manager.mobile %><% } %></td>
                </tr>
                <tr>
                  <td style="width: 20%; padding-right: 0;">팩&nbsp;&nbsp;&nbsp;스</td>
                  <td colspan="3" style="width: 80%; text-align: left; padding-left: 0;"><% if (client_manager) { %><%= client_manager.fax %><% } %></td>
                </tr>
                <tr>
                  <td style="width: 20%; padding-right: 0;">이메일</td>
                  <td colspan="3" style="width: 80%; text-align: left; padding-left: 0;"><% if (client_manager) { %><%= client_manager.email %><% } %></td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </tbody>
  </table>
`