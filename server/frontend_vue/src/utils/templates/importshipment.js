export default `
<style>
  body { margin: 0; padding: 0; width: 210mm; }
  @media print {
    @page { size: portrait }
    .page { border: 0; }
    .print-document { margin-top: 0px !important; }
  }
  .page th, .page td { font-size: 15px; font-weight: bold; }
  .print-document { margin-top: 60px; padding: 10px; }
  .between { display: flex; justify-content: space-between; }
  .normal-size { font-size: 12px; }
  .v-top td { vertical-align: top; }
  .table-head td { border-top: 1px solid black; border-bottom: 1px solid black; }
  .table-footer td { border-top: 1px dotted black; }
</style>
<div class="print-document page">
  <div class="between normal-size">
    <div>
      <%= _company.name_en %>
    </div>
    <div>
      TEL: <%= _company.phone_en %><br>
      FAX: <%= _company.fax_en %>
    </div>
  </div>
  
  <div class="align-center" style="max-width: 260px; margin: 20px auto; font-weight: bold; font-size: 25px;">
    <%= _company.name_en %><br>
    &lt; OFFER &gt;
  </div>

  <table class="v-top">
    <tr>
      <td>SERIAL NO.</td>
      <td>:</td>
      <td>
        <div class="between">
          <div><%= shipment_number %></div>
          <div>DATE : <%= shipment_date %></div>
        </div>    
      </td>
    </tr>
    <tr>
      <td colspan="3" class="align-center">
        We Hereby import under the following terms and conditions
      </td>
    </tr>
    <tr>
      <td>ORIGIN</td>
      <td>:</td>
      <td><%= origin %></td>
    </tr>
    <tr>
      <td>BENEFICIARY</td>
      <td>:</td>
      <td>
        <div style="">
          <%= supplier.name %><br>
          <%= supplier.address_en %>
        </div>
      </td>
    </tr>
    <tr>
      <td>PAYMENT</td>
      <td>:</td>
      <td>
        <div>
          <%= payment %>
        </div>
      </td>
    </tr>
    <tr>
      <td>ADVISING BANK</td>
      <td>:</td>
      <td><%= adv_bank_info.bank_name %> <%= adv_bank_info.bank_address %></td>
    </tr>
    <tr>
      <td>ACCOUNT NO.</td>
      <td>:</td>
      <td><%= adv_bank_info.account_number %> <% if (adv_bank_info.swift_code) { %>(Swift code: <%= adv_bank_info.swift_code %>)<% } %></td>
    </tr>
    <tr>
      <td>DISPATCH</td>
      <td>:</td>
      <td><%= delivery %></td>
    </tr>
    <tr>
      <td>PACKING</td>
      <td>:</td>
      <td><%= packing %></td>
    </tr>
    <tr>
      <td>INSPECTION</td>
      <td>:</td>
      <td><%= inspection %></td>
    </tr>
    <tr>
      <td>VALIDITY</td>
      <td>:</td>
      <td><%= validity %></td>
    </tr>
    <tr>
      <td>REMARKS</td>
      <td>:</td>
      <td><%= remark %></td>
    </tr>
  </table>

  <div style="height: 20px;">&nbsp;</div>

  <table>
    <tr class="table-head">
      <td>DESCRIPTION</td>
      <td class="align-right">QUANTITY</td>
      <td class="align-right">UNIT PRICE(<%= currency %>)</td>
      <td class="align-right">AMOUNT(<%= currency %>)</td>
    </tr>
    <tr>
      <td colspan="4" class="align-center">F.O.B. <%= destination %></td>
    </tr>
    <% _.forEach(grouped, function(itemGroupList, hsCode) { %>
      <tr>
        <td colspan="4" style="font-weight: bold;">HSK NO : <%= hsCode %></td>
      </tr>
      <% _.forEach(itemGroupList, function(list, itemGroup) { %>
        <tr>
          <td colspan="4"  style="font-weight: bold;"><%= itemGroup %></td>
        </tr>
      <% _.forEach(list, function(item, index) { %>
        <tr>
          <td><%= item.item.item_name %> <% if (item.item.item_standard) { %>[<%= item.item.item_standard %>]<% } %></td>
          <td class="align-right"><%= item.qty_str %> <%= item.item.unit %></td>
          <td class="align-right"><%= item.import_price_str %></td>
          <td class="align-right"><%= item.amount_str %></td>
        </tr>
      <% }) %>
      <% }) %>
    <% }) %>
    <tr class="table-footer">
      <td>Total:</td>
      <td class="align-right"><%= total_qty_str %> <%= unit %></td>
      <td class="align-right">&nbsp;</td>
      <td class="align-right"><%= currency %> <%= total_price_str %></td>
    </tr>
  </table>
  
</div>
`