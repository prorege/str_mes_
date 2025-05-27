import RestlessStore from './restless-store';

const setupBasicStock = new RestlessStore('/api/mes/v1/setup/basic_stock');
const setupBasicBalance = new RestlessStore('/api/mes/v1/setup/basic_balance');
const setupGroup = new RestlessStore('/api/mes/v1/setup/group');
const setupGroupAuth = new RestlessStore('/api/mes/v1/setup/group_auth');
const setupCodeChangeHistory = new RestlessStore(
  '/api/mes/v1/setup/code_change_history'
);
const setupMenu = new RestlessStore('/api/mes/v1/setup/menu');
const setupControl = new RestlessStore('/api/mes/v1/setup/control');
const setupProduceCost = new RestlessStore(
  '/api/mes/v1/setup/produce_cost',
  {},
  'processed',
  ['year', 'subfix', 'fk_company_id']
);
const setupSgaExpense = new RestlessStore('/api/mes/v1/setup/sga_expense');
const setupMD = new RestlessStore('/api/mes/v1/setup/md');

const getSetupBasicStock = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/setup/basic_stock');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getSetupBasicBalance = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/setup/basic_balance');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getStock = async (itemCode, warehouseCode) => {
  let currentStock = 0;
  let availableStock = 0;
  const stock = getSetupBasicStock([
    { name: 'item_code', op: 'eq', val: itemCode },
    { name: 'wh_code', op: 'eq', val: warehouseCode },
  ]);
  const { data } = await stock.load();
  if (data.length > 0) {
    currentStock = data[0].current_stock;
    availableStock = data[0].available_stock;
    return {
      basicStock: data[0],
      currentStock: currentStock,
      availableStock: availableStock,
    };
  }
  return {
    basicStock: {
      current_stock: 0,
      available_stock: 0,
    },
    currentStock: currentStock,
    availableStock: availableStock,
  };
};

const getSetupControl = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/setup/control');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getSetupCodeChangeHistory = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/setup/code_change_history');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getSetupMenu = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/setup/menu');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getSetupSgaExpense = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/setup/sga_expense');
  instance.defaultFilters = defaultFilters;
  return instance;
};

const getSetupMD = (defaultFilters) => {
  const instance = new RestlessStore('/api/mes/v1/setup/md');
  instance.defaultFilters = defaultFilters;
  return instance;
};

// 데이터 변경
// const setupMenu = new RestlessStore(
//   '/api/mes/v1/setup/menu',
//   (options) => {
//     let baseLoad = options.load
//     options.load = (loadOptions) => {
//       // 필요한 필터 추가
//       return baseLoad(loadOptions).then(response => {
//         // 필요에 따라 데이터 변경
//         return response.data.map(v => {
//           return {
//             id: v.id,
//             parentId: v.menu_depth, // 현재 메뉴 상위키 컬럼이 없음
//             path: v.etc, // 메뉴에 대한 링크 필요

//             isDirectory: v.menu_depth < 0,
//             text: v.menu_name,
//             menu_enable: v.menu_enable,

//           }
//         })
//       })
//     }
//   }
// )

export {
  setupMenu,
  setupBasicStock,
  setupBasicBalance,
  setupGroup,
  setupGroupAuth,
  setupCodeChangeHistory,
  setupControl,
  setupProduceCost,
  setupSgaExpense,
  setupMD,
  getSetupBasicStock,
  getSetupBasicBalance,
  getStock,
  getSetupControl,
  getSetupCodeChangeHistory,
  getSetupMenu,
  getSetupSgaExpense,
  getSetupMD,
};
