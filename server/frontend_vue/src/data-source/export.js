import RestlessStore from './restless-store';

const salesOrder = new RestlessStore('/api/mes/v1/export/sales_order');
const salesOrderItem = new RestlessStore('/api/mes/v1/export/sales_order_item');
const commInvoice = new RestlessStore('/api/mes/v1/export/comm_invoice');

const getSalesOrderItem = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/export/sales_order_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getCommInvoiceItem = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/export/comm_invoice_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

export {
  salesOrder,
  salesOrderItem,
  commInvoice,
  getSalesOrderItem,
  getCommInvoiceItem,
};
