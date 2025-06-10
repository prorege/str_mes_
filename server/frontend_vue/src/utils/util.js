import { confirm } from 'devextreme/ui/dialog'

const generateItemButtonOption = (
  icon,
  callback,
  location = 'after',
  options = {},
  btnOpts = {}
) => {
  let buttonOptions = { stylingMode: 'text', icon, onClick: callback, ...btnOpts };
  return {
    ...options,
    buttons: [{ name: icon, location, options: buttonOptions }],
  };
};

const sumSupplyPrice = (grid, quantityName, priceName) => {
  let total = 0;
  if (grid) {
    const rows = grid.getVisibleRows();
    if (rows.length > 0) {
      rows.forEach(elem => {
        if (elem.removed) return
        total += elem.data[quantityName] * elem.data[priceName];
      });
    }
  }
  return total;
};

const calcPriceSummary = (vat_type, total) => {
  let supply_price = 0;
  let vat = 0;
  let total_price = 0;

  switch (vat_type) {
    case '별도': {
      supply_price = total;
      vat = Math.floor(Math.abs(total) * 0.1) * (total >= 0 ? 1 : -1);
      total_price = total + vat;
      break;
    }
    case '포함': {
      total_price = total;
      supply_price = Math.round((total * 10) / 11);
      vat = total_price - supply_price;
      break;
    }
    case '영세': {
      total_price = total;
      vat = 0;
      supply_price = total;
      break;
    }
    default: {
      total_price = total;
      vat = 0;
      supply_price = total;
    }
  }
  return { supply_price, vat, total_price };
};

const getFirstCodeNameInBaseCodeList = (baseCodeList) => {
  if (!baseCodeList || baseCodeList.length <= 0) { return ''; }
  return baseCodeList[0].code_name;
};

const humanize = (n) => {
  const runit = ['','십','백','천']
  const aunit = ['','만','억','조']
  const nunit = {'1':'일','2':'이','3':'삼','4':'사','5':'오','6':'육','7':'칠','8':'팔','9':'구'}
  const a = String(n).split('')
  let cursor = 0, result = ''
  while (a.length) {
    const i = cursor % 4
    if (i === 0) result = aunit[cursor / 4] + result
    const r = nunit[a.pop()]
    if (r) result = r + runit[i] + result
    cursor++
  }
  return result
}

const businessNumberFormat = (n) => {
  try {
    const a = String(n).replace(/-/g, '').split('')
    a.splice(3, 0, '-')
    a.splice(6, 0, '-')
    return a.join('')
  }
  catch (ex) {
    console.error(ex)
    return n
  }
}

const currentDateTime = () => {
  const today = new Date();
  return `${today.getFullYear()}-${("00"+(today.getMonth() + 1)).slice(-2)}-${("00"+today.getDate()).slice(-2)}T${("00"+today.getHours()).slice(-2)}:${("00"+today.getMinutes()).slice(-2)}:${("00"+today.getSeconds()).slice(-2)}`
}

const beforeExitConfirm = (function () {
  console.info('저장확인기능 초기화')
  const message = '저장하지 않은 내용이 있습니다.\n이동하시겠습니까?'
  
  let checkContentChangeFn = undefined

  function clear () {
    console.info('저장확인기능: 해제')
    checkContentChangeFn = undefined
    window.removeEventListener('beforeunload', onBeforeUnloadHandler)
  }

  function onBeforeUnloadHandler (evt) {
    console.info('저장확인기능: 페이지 이탈')
    evt.preventDefault()
    if (checkContentChangeFn()) evt.returnValue = message
    return
  }

  return {
    clear,
    check (fn) {
      clear()
      console.info('저장확인기능: 등록')
      if (typeof fn !== 'function') return 
      checkContentChangeFn = fn
      window.addEventListener('beforeunload', onBeforeUnloadHandler)
    },
    setRouter (router) {
      router.beforeEach(async (to, from, next) => {
        if (typeof checkContentChangeFn === 'function' && checkContentChangeFn()) {
          try {
            const r = await confirm(message, '알림')
            if (r) {
              clear()
              console.info('저장확인기능: 사용자선택으로 강제이동')
              next()
            }
            else {
              console.info('저장확인기능: 사용자선택으로 이동취소')
              next(false)
            }
          }
          catch (ex) {
            console.info(`저장확인기능: 예외(${ex})`)
            next(false)
          }
        }
        else {
          clear()
          next()
        }
      })
    }
  }
})()

export { 
  generateItemButtonOption, 
  sumSupplyPrice, 
  calcPriceSummary,
  getFirstCodeNameInBaseCodeList,
  humanize, 
  businessNumberFormat, 
  currentDateTime,
  beforeExitConfirm,
};
