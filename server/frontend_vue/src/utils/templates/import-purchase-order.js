export default `
<style>
  body { margin: 0; padding: 0; width: 210mm; }
  @media print {
    @page { size: portrait }
    .page { border: 0; }
    .print-document { margin-top: 0px !important; }
  }
  .v-bottom td { font-size: 15px; font-weight: bold; }
  .print-document { margin-top: 60px; padding: 10px; }
  .between { display: flex; justify-content: space-between; }
  .normal-size { font-size: 12px; }
  .v-top td { vertical-align: top; font-size: 18px; font-weight: bold; }
  .table-head td { border-top: 1px solid black; border-bottom: 1px solid black; }
  .table-footer td { border-top: 1px dotted black; border-bottom: 1px solid black; }
  ._height_40 {
    height: 40px;
  }
  .border_none {
    border : none;
  }
</style>
<div class="print-document page">
    <div style="max-width: 500px; font-weight: bold; font-size: 48px;">
      NEW ORDER ENTRY
    </div>
  
    <table class="v-top">
      <br>
      <br>
      <tr>
        <td colspan="8" style="max-width: 210mm;">
          **********************************************************************************************
        </td>
      </tr>
      <tr class="_height_40">
        <td style="width:40px;">FROM</td>
        <td colspan="3">: <%= buyer_name_en %> </td>
        <td style="width:80px;">P/O NO.</td>
        <td colspan="3">: <%= order_number %> </td>
      </tr>
      <tr class="_height_40">
        <td>TO</td>
        <td colspan="3">: <%= supplier %> </td>
        <td>DATE</td>
        <td colspan="3">: <%= order_date %> </td>
      </tr>
      <tr class="_height_40">
        <td>ATTN</td>
        <td colspan="3">: <%= supplier_contact %> </td>
        <td colspan="2" style="width:140px;">TERMS OF PAYMENT</td>
        <td colspan="2">: <%= payment %> </td>
      </tr>
      <tr class="_height_40">
        <td colspan="2" style="padding-right: 0px !important; max-width:90px;">CUSTOMER</td>
        <td colspan="2">: <%= buyer_name_en %> </td>
        <td>
        <td>
        <td>
        <td>
        <td>
      </tr>
      <tr>
        <td colspan="8" style="max-width: 210mm;">
          **********************************************************************************************
        </td>
      </tr>
    </table>
  
    <div style="height: 20px;">&nbsp;</div>
  
    <table class="v-bottom">
      <tr class="table-head">
        <td colspan="2" class="align-center">ITEMS</td>
        <td class="align-center">QUANTITY</td>
        <td class="align-center">UNIT PRICE <br>( <%= currency %> )</td>
        <td class="align-center">REQUIRED <br>DELIVERY</td>
      </tr>
      <% _.forEach(items, function(item, index) { %>
      <tr>
        <td colspan="2" class="align-left" style="padding-left : 20px"><%= index + 1 %>. <%= item.item.item_name %></td>
        <td class="align-center"> <%= numeral(item.qty).format('0,0') %> <%= item.item.unit %> </td>
        <td class="align-center"> <%= numeral(item.import_price).format('0,0.0000') %> </td>
        <td class="align-center"><% if (item.req_date) { %> <%= moment(item.req_date).format('YYYY-MM-DD') %> <% } %> </td>
      </tr>
      <% }); %>
      <tr class="table-footer">
        <td colspan="2" class="align-left" style="padding-left : 20px">Total :</td>
        <td class="align-center"> <%= numeral(items.reduce((t, a) => t += a.qty, 0)).format('0,0') %> <%= items[0].item.unit %> </td>
        <td class="align-center"></td>
        <td class="_height_40" style="text-align: right;"><%= currency %> <%= numeral(total_price).format('0,0.00') %> </td>
      </tr>
      <tr class="border_none" style="height: 200px;" ><td>&nbsp;<td><tr>
      <tr class="_height_40" border=1>
        <td style="width: 70px; vertical-align: top;">Remarks : </td>
        <td colspan="4"> <%= remark %> </td>
      </tr>
    </table>
    
  </div>
`