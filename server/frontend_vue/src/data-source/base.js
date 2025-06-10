import RestlessStore from './restless-store';

const baseClient = new RestlessStore('/api/mes/v1/base/client');
const baseClientManager = new RestlessStore('/api/mes/v1/base/client-manager');
const baseClientItem = new RestlessStore('/api/mes/v1/base/client-item');
const baseDesign = new RestlessStore('/api/mes/v1/base/design');
const baseItem = new RestlessStore('/api/mes/v1/base/item');
const baseCode = new RestlessStore('/api/mes/v1/base/code');
const baseDepartment = new RestlessStore('/api/mes/v1/base/department');
const baseEmployee = new RestlessStore('/api/mes/v1/base/employee');
const baseWarehouse = new RestlessStore('/api/mes/v1/base/warehouse');
const baseProcess = new RestlessStore('/api/mes/v1/base/process');
const baseBom = new RestlessStore('/api/mes/v1/base/bom');
const baseBomLink = new RestlessStore('/api/mes/v1/base/bom-link');
const baseBomProcess = new RestlessStore('/api/mes/v1/base/bom-process');
const baseBomHistory = new RestlessStore('/api/mes/v1/base/bom-history');
const baseBank = new RestlessStore('/api/mes/v1/base/bank');

const baseEmployeeLookup = new RestlessStore(
  '/api/mes/v1/base/employee',
  (options) => {
    let baseLoad = options.load;
    options.byKey = async (key) => {
      return { emp_name: key };
    };
    options.load = (loadOptions) => {
      loadOptions.skip = 0;
      loadOptions.take = 1000;
      return baseLoad.call(baseEmployeeLookup, loadOptions);
    };
    return options;
  }
);

const getBaseClient = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/base/client');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getBaseClientManager = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/base/client-manager');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getBaseClientItem = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/base/client-item');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getBaseDesign = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/base/design');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getBaseItem = (defaultFilters, clientId, warehouseCode) => {
  const instance = new RestlessStore('/api/mes/v1/base/item', {
    onLoaded: function (result) {
      result.data.forEach((item) => {
        if (clientId) {
          let clientItem = null;
          if (item.client_item) {
            clientItem = item.client_item.filter(
              (client) => client.client_id == clientId
            );
          }
          item.client_item = clientItem ? clientItem[0] : null;
        }

        if (warehouseCode) {
          let basicStock = null;
          if (item.basic_stock) {
            if (Array.isArray(item.basic_stock)) {
              basicStock = item.basic_stock.filter(
                (stock) => stock.wh_code == warehouseCode
              );
            } else {
              if (item.basic_stock.wh_code == warehouseCode) {
                basicStock = [item.basic_stock];
              }
            }
          }
          item.basic_stock = basicStock ? basicStock[0] : null;
        }
      });
    },
  });
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getBaseBomProcess = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/base/bom-process');
  instance.defaultFilters = defaultFilters;
  return instance;
}

const getBaseDepartment = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/base/department');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getBaseEmployee = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/base/employee');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getBaseEmployeeByDepartmentId = async (departmentId) => {
  const { data } = await baseEmployee.load({
    filter: [['fk_department_id', '=', departmentId]],
  });
  return data;
};

const getBaseCode = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/base/code');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getBaseWarehouse = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/base/warehouse');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getBaseBom = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/base/bom');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const baseCodeLoader = async (codeNames, companyId) => {
  let response,
    result = {};
  for (let code of codeNames) {
    result[code] = [];
    if (companyId) {
      response = await baseCode.load({
        filter: [
          ['code_name', '=', code],
          ['fk_company_id', '=', companyId],
        ],
      });
    } else {
      response = await baseCode.load({ filter: ['code_name', '=', code] });
    }
    if (response.data[0] && response.data[0].items) {
      result[code] = response.data[0].items;
    }
  }
  return result;
};

const getClientByName = async (name) => {
  const api = getBaseClient()
  const {data: list} = await api.load({filter: ['name', '=', name]})
  if (!list.length) return undefined
  return list[0]
}

const getBaseBank = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/base/bank');
  instance.defaultFilters = defaultFilters;
  return instance;
};

export {
  baseClient,
  baseClientManager,
  baseClientItem,
  baseDesign,
  baseItem,
  baseCode,
  baseDepartment,
  baseEmployee,
  baseWarehouse,
  baseProcess,
  baseBom,
  baseBomLink,
  baseBomProcess,
  baseBomHistory,
  baseEmployeeLookup,
  baseBank,
  getBaseClient,
  getBaseClientManager,
  getBaseClientItem,
  getBaseDesign,
  getBaseItem,
  getBaseCode,
  getBaseBom,
  getBaseBomProcess,
  getBaseDepartment,
  getBaseEmployee,
  getBaseEmployeeByDepartmentId,
  getBaseWarehouse,
  baseCodeLoader,
  getClientByName,
  getBaseBank,
};
