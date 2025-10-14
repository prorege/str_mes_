import RestlessStore from './restless-store';

const asReceipt = new RestlessStore('/api/mes/v1/as/receipt');

const asReceiptItem = new RestlessStore('/api/mes/v1/as/receipt-item');

const asResult = new RestlessStore('/api/mes/v1/as/result');

const asResultItem = new RestlessStore('/api/mes/v1/as/result-item');

const asResultAttachment = new RestlessStore('/api/mes/v1/as/result-attachment');

const asResultExpense = new RestlessStore('/api/mes/v1/as/result-expense');

const asReceiptResultStatus = new RestlessStore('/api/mes/v1/as/receipt-result-status');  

const getAsReceipt = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/as/receipt');
  instance.defaultFilters = defaultFilters; 
  return instance;
};

const getAsReceiptItem = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/as/receipt-item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getAsResult = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/as/result');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getAsResultItem = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/as/result-item');
  instance.defaultFilters = defaultFilters;
  return instance;
};


const getAsResultAttachment = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/as/result-attachment');
  instance.defaultFilters = defaultFilters;
  return instance;
};


const getAsResultExpense = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/as/result-expense');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getAsReceiptResultStatus = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/as/receipt-result-status', {}, 'processed', 'receipt_id');
  instance.defaultFilters = defaultFilters;
  return instance;
};


export { 
    asReceipt, 
    asReceiptItem,
    asResult,
    asResultItem,
    asResultAttachment,
    asResultExpense,
    asReceiptResultStatus,
    getAsReceipt,
    getAsReceiptItem,
    getAsResult,
    getAsResultItem,
    getAsResultAttachment,
    getAsResultExpense,
    getAsReceiptResultStatus
};
