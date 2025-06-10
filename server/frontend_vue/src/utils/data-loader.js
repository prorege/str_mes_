import authService from '../auth';
import {
  baseDepartment,
  baseEmployee,
  baseClient,
  baseClientManager,
  baseWarehouse,
  baseBank,
} from '../data-source/base';

const loadDepartment = (dataSource) => {
  return baseDepartment
    .load({
      filter: [['fk_company_id', '=', authService.getCompanyId()]],
      take: 10000000,
      skip: 0,
    })
    .then(({ data }) => {
      dataSource.department = data;
    });
};

const loadEmployee = (dataSource, departmentId) => {
  return baseEmployee
    .load({
      filter: departmentId ? [['fk_department_id', '=', departmentId]] : [],
      take: 10000000,
      skip: 0,
    })
    .then(({ data }) => {
      dataSource.employee = data;
    });
};

const loadClient = (dataSource) => {
  return baseClient
    .load({
      filter: [['fk_company_id', '=', authService.getCompanyId()]],
      take: 10000000,
      skip: 0,
    })
    .then(({ data }) => {
      dataSource.client_company = data;
    });
};

const loadClientManager = (dataSource, clientName) => {
  return baseClient
    .load({
      filter: [['name', '=', clientName]],
    })
    .then(({ data }) => {
      if (data.length > 0) {
        baseClientManager
          .load({
            filter: [['fk_client_id', '=', data[0].id]],
            take: 10000000,
            skip: 0,
          })
          .then(({ data }) => {
            dataSource.client_manager = data;
          });
      }
    });
};

const loadWarehouse = (dataSource) => {
  return baseWarehouse
    .load({
      filter: [['fk_company_id', '=', authService._user.fk_company_id]],
      take: 10000000,
      skip: 0,
      sort: [{ selector: 'wh_order', desc: false }],
    })
    .then(({ data }) => {
      dataSource.warehouse = data;
    });
};

const loadBank = (dataSource) => {
  return baseBank
    .load({
      filter: [['fk_company_id', '=', authService.getCompanyId()]],
      take: 10000000,
      skip: 0,
    })
    .then(({ data }) => {
      dataSource.bank = data;
    });
};

export {
  loadDepartment,
  loadEmployee,
  loadClient,
  loadClientManager,
  loadWarehouse,
  loadBank,
};
