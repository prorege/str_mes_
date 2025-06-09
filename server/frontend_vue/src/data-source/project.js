import RestlessStore from './restless-store';

const projectRegistration = new RestlessStore(
  '/api/mes/v1/project/project_management'
);
const projectItem = new RestlessStore('/api/mes/v1/project/project_item');

const projectParticipant = new RestlessStore('/api/mes/v1/project/project_participant');

const projectCompany = new RestlessStore('/api/mes/v1/project/project_company');

const projectDocument = new RestlessStore('/api/mes/v1/project/project_document');

const projectReceipt = new RestlessStore('/api/mes/v1/project/project_receipt');

const projectNotice = new RestlessStore('/api/mes/v1/project/project_notice');

const projectSchedule = new RestlessStore(
  '/api/mes/v1/project/project_schedule'
);

const projectBusiness = new RestlessStore(
  '/api/mes/v1/project/project_business'
);

const projectBusinessNote = new RestlessStore(
  '/api/mes/v1/project/project_business_note'
);

const projectBusinessProgress = new RestlessStore(
  '/api/mes/v1/project/project_business_progress'
);
const projectExcutionPlan = new RestlessStore(
  '/api/mes/v1/project/excution_plan'
);

const projectExcutionPlanItem = new RestlessStore(
  '/api/mes/v1/project/excution_plan_item'
);

const projectExcutionPlanSubcontract = new RestlessStore(
  '/api/mes/v1/project/excution_plan_subcontract'
);

const projectExcutionPlanExpense = new RestlessStore(
  '/api/mes/v1/project/excution_plan_expense'
);

const projectBusinessTripLog = new RestlessStore(
  '/api/mes/v1/project/business_trip_log'
);

const projectHappyCall = new RestlessStore(
  '/api/mes/v1/project/happy_call'
);

const projectDailyLog = new RestlessStore(
  '/api/mes/v1/project/daily_log'
);

const projectCostLog = new RestlessStore(
  '/api/mes/v1/project/cost_log'
);

const projectCompletion = new RestlessStore(
  '/api/mes/v1/project/completion'
);

const projectCustomerInformation = new RestlessStore(
  '/api/mes/v1/project/customer_information'
);

const projectCustomerHistory = new RestlessStore(
  '/api/mes/v1/project/customer_history'
);

const projectBusinessQuote = new RestlessStore(
  '/api/mes/v1/project/business_quote'
);

const projectBusinessCost = new RestlessStore(
  '/api/mes/v1/project/business_cost'
);

const projectBusinessBasic = new RestlessStore(
  '/api/mes/v1/project/business_basic'
);

const getProjectRegistration = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/project_management');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getProjectItem = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/project_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getProjectParticipant = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/project_participant');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getProjectCompany = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/project_company');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getProjectDocument = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/project_document');
  instance.defaultFilters = defaultFilters;
  return instance;
};
const getProjectReceipt = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/project_receipt');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getProjectBusiness = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/project_business');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getProjectBusinessNote = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/project_business_note');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getProjectBusinessProgress = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/project_business_progress');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getProjectExcutionPlan = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/excution_plan');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getProjectExcutionPlanItem = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/excution_plan_item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getProjectExcutionPlanSubcontract = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/excution_plan_subcontract');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getProjectExcutionPlanExpense = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/excution_plan_expense');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getProjectBusinessTripLog = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/business_trip_log');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getProjectHappyCall = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/happy_call');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getProjectDailyLog = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/daily_log');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getProjectCostLog = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/cost_log');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getProjectCompletion = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/completion');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getProjectCustomerInformation = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/customer_information');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getProjectCustomerHistory = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/customer_history');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getProjectBusinessQuote = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/business_quote');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getProjectBusinessCost = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/business_cost');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getProjectBusinessBasic = defaultFilters => {
  const instance = new RestlessStore('/api/mes/v1/project/business_basic');
  instance.defaultFilters = defaultFilters;
  return instance;
};

export {
  projectRegistration,
  projectItem,
  projectParticipant,
  projectCompany,
  projectDocument,
  projectReceipt,
  projectSchedule,
  projectNotice,
  projectBusiness,
  projectBusinessNote,
  projectBusinessProgress,
  projectExcutionPlan,
  projectExcutionPlanItem,
  projectExcutionPlanSubcontract,
  projectExcutionPlanExpense,
  projectBusinessTripLog,
  projectHappyCall,
  projectDailyLog,
  projectCostLog,
  projectCompletion,
  projectCustomerInformation,
  projectCustomerHistory,
  projectBusinessQuote,
  projectBusinessCost,
  projectBusinessBasic,
  getProjectRegistration,
  getProjectItem,
  getProjectParticipant,
  getProjectCompany,
  getProjectDocument,
  getProjectReceipt,
  getProjectBusiness,
  getProjectBusinessNote,
  getProjectBusinessProgress,
  getProjectExcutionPlan,
  getProjectExcutionPlanItem,
  getProjectExcutionPlanSubcontract,
  getProjectExcutionPlanExpense,
  getProjectBusinessTripLog,
  getProjectHappyCall,
  getProjectDailyLog,
  getProjectCostLog,
  getProjectCompletion,
  getProjectCustomerInformation,
  getProjectCustomerHistory,
  getProjectBusinessQuote,
  getProjectBusinessCost,
  getProjectBusinessBasic
};
