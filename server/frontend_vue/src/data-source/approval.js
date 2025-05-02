import RestlessStore from './restless-store';

const approvalManagement = new RestlessStore('/api/mes/v1/approval/management');

const getApprovalManagement = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/approval/management');
  instance.defaultFilters = defaultFilters;
  return instance;
};

export {
  approvalManagement,
  getApprovalManagement,
};


