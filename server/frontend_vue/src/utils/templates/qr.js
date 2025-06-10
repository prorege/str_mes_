export default `
<style>
body { margin: 0; padding: 0; }
.print-document {
  box-sizing: border-box;
}
.section {
  display: flex;
  align-items: center;
  page-break-before:always;
}

.label {
  margin: 0cm;
  font-size: 0;
}
.label.left {
  margin-left: 3mm;
  margin-right: 8mm;
}
.label img { 
  width: 100%; height: 100%;
}
.p50x24 { width: 50mm; height: 24mm; }
.s47x26 { width: 4.7cm; height: 2.69cm; }
.s2x2 { width: 2cm; height: 2cm; }
</style>
<div class="print-document">
<% _.chain(items).chunk(2).value().forEach(function(item, index) { %>
  <div class="section p50x24">
    <div class="label left s<%=label%>">
      <img src="<%= item[0].qr %>"/>
    </div>
    <% if (item[1]) { %>
    <div class="label s<%=label%>">
      <img src="<%= item[1].qr %>"/>
    </div>
    <% } %>
  </div>
<% }); %>
</div>
`