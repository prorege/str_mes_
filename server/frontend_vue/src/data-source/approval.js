import RestlessStore from './restless-store';

const approvalManagement = new RestlessStore('/api/mes/v1/approval/management');
const approval = new RestlessStore('/api/mes/v1/approval/approval');
const approvalLine = new RestlessStore('/api/mes/v1/approval/approval-line');
const approvalLineResult = new RestlessStore('/api/mes/v1/approval/approval-line-result');
const approvalDocument = new RestlessStore('/api/mes/v1/approval/approval-document');
const approvalAttachment = new RestlessStore('/api/mes/v1/approval/approval-attachment');
const approvalDocumentStatus = new RestlessStore('/api/mes/v1/approval/document-status');

const getApprovalManagement = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/approval/management');
  instance.defaultFilters = defaultFilters;
  return instance;
};


const getApproval = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/approval/approval');
  instance.defaultFilters = defaultFilters; 
  return instance;
};

const getApprovalDocumentStatus = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/approval/document-status');
  instance.defaultFilters = defaultFilters; 
  return instance;
};

const getApprovalLine = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/approval/approval-line');
  instance.defaultFilters = defaultFilters; 
  return instance;
};  

const getApprovalLineResult = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/approval/approval-line-result');
  instance.defaultFilters = defaultFilters; 
  return instance;
};

const getApprovalDocument = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/approval/approval-document');
  instance.defaultFilters = defaultFilters; 
  return instance;
};

const getApprovalAttachment = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/approval/approval-attachment');
  instance.defaultFilters = defaultFilters; 
  return instance;
};

export {
  approvalManagement,
  approval,
  approvalDocumentStatus,
  approvalLine,
  approvalLineResult,
  approvalDocument,
  approvalAttachment,
  getApprovalManagement,
  getApproval,
  getApprovalDocument,
  getApprovalDocumentStatus,
  getApprovalLine,
  getApprovalLineResult,
  getApprovalAttachment,
};


