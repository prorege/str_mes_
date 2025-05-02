import axios from 'axios';
import notify from 'devextreme/ui/notify';
import authService from '../auth';

export default class ApiService {
  constructor(baseURL) {
    this.q = axios.create({ baseURL });
    this.get = this.q.get;
    this.post = this.q.post;
    this.put = this.q.put;
    this.patch = this.q.patch;
    this.delete = this.q.delete;
    this.q.interceptors.request.use(this.beforeRequestProcessor.bind(this));
    this.q.interceptors.response.use(
      this.responseSuccessProcessor.bind(this),
      this.responseErrorProcessor.bind(this)
    );
  }

  beforeRequestProcessor(config) {
    config.headers.token = authService.token;
    return config;
  }

  responseSuccessProcessor(response) {
    return response;
  }

  responseErrorProcessor(error) {
    let msg = '';
    if (error.response.status === 411) {
      //notify('인증이 만료되었습니다', 'error', 2000);
      alert('다른 곳에서 동일한 계정으로 로그인하여 로그아웃합니다.');
      authService.logOut();

      setTimeout(() => {
        location.href = '/';
      }, 1000);
    } else if (error.response.status === 403) {
      if (error.response.config.method === 'post') msg = '생성 권한이 없습니다';
      else if (error.response.config.method === 'patch')  msg = '수정 권한이 없습니다';
      else if (error.response.config.method === 'delete') msg = '삭제 권한이 없습니다';
      notify(msg, 'error', 2000);
    } else if (error.response.status === 412) {
         msg = '권한이 없습니다';
         notify(msg, 'error', 2000);
    } else if (error.response.status === 404) {
        // msg = '데이터가 없습니다.'
        // notify(msg, 'error', 2000);
    } 
    return Promise.reject(error);
  }

  setAuthHeader(token) {
    this.q.defaults.headers.common['token'] = token;
  }

  unsetAuthHeader() {
    this.q.defaults.headers.common['token'] = '';
    delete this.q.defaults.headers.common['token'];
  }

  getFilterFromRequest(req) {
    // req[0] // column name
    // req[1] // op (contains, notcontains, startswith, endswith, =, <>)
    // req[2] // value
    let add = { name: req[0] };
    switch (req[1]) {
      case 'has': {
        add.op = 'has';
        add.val = req[2];
        break;
      }
      case 'any': {
        add.op = 'any';
        add.val = req[2];
        break;
      }
      case 'contain': {
        add.op = 'like';
        add.val = `%${req[2]}%`;
        break;
      }
      case 'contains': {
        add.op = 'like';
        add.val = `%${req[2]}%`;
        break;
      }
      case 'notcontains': {
        add.op = 'like';
        add.val = `%${req[2]}%`;
        break;
      }
      case 'startswith': {
        add.op = 'like';
        add.val = `${req[2]}%`;
        break;
      }
      case 'endswith': {
        add.op = 'like';
        add.val = `%${req[2]}`;
        break;
      }
      case '=': {
        if (req[2] === null) {
          add.op = 'is_null';
        } else {
          add.op = 'eq';
          add.val = req[2];
        }
        break;
      }
      case '>': {
        add.op = 'gt';
        add.val = req[2];
        break;
      }
      case '>=': {
        add.op = 'gte';
        add.val = req[2];
        break;
      }
      case '<': {
        add.op = 'lt';
        add.val = req[2];
        break;
      }
      case '<=': {
        add.op = 'lte';
        add.val = req[2];
        break;
      }
      case '<>': {
        if (req[2] === null) {
          add.op = 'is_not_null';
        } else {
          add.op = 'neq';
          add.val = req[2];
        }
        break;
      }
      default: {
        console.log(`Unknown operation: ${req[0]} / ${req[1]} / ${req[2]}`);
        return null;
      }
    }

    if (add.name.includes('.')) {
      let splited_adds = add.name.split('.');
      let new_add = {
        name: splited_adds[0],
        op: 'has',
        val: {
          name: splited_adds[1],
          op: add.op,
          val: add.val,
        },
      };
      return new_add;
    }
    return add;
  }

  parseParameter(filter, obj) {
    if (typeof filter[0] === 'string') {
      const add = this.getFilterFromRequest(filter);
      if (add) obj.push(add)
    }
    else {
      for (let ft of filter) {
        if (typeof ft === 'string') continue;
        this.parseParameter(ft, obj)
      }
    }
  }

  getParamsForRestless(options, defs) {
    let params = {},
      q = {};
    // let {skip, take, requireTotalCount, requireGroupCount, sort, filter, totalSummary, group, groupSummary} = options
    let { skip, take, sort, filter } = options;
    // 일단 and 만...
    if (filter) {
      q.filters = [];
      this.parseParameter(filter, q.filters)
    }

    if (defs && defs.length) {
      if (!q.filters) q.filters = [];
      if (!q.filters.length) q.filters = defs;
      else q.filters = [...q.filters, ...defs];
    }

    if (typeof skip === 'number' && typeof take === 'number') {
      params.results_per_page = take;
      params.page = Math.floor(skip / take) + 1;
    }

    if (sort) {
      q.order_by = sort
        .filter((v) => typeof v.selector === 'string')
        .map((v) => ({
          field: v.selector.replace('.', '__'),
          direction: v.desc ? 'desc' : 'asc',
        }));
    }

    if (Object.keys(q).length) params.q = JSON.stringify(q);
    return params;
  }

  getParamsForRestless2(options, defaultFilter, defaultSort) {
    let params = {},
      q = {};

    // let {skip, take, requireTotalCount, requireGroupCount, sort, filter, totalSummary, group, groupSummary} = options
    let { skip, take, sort, filter } = options;

    // 일단 and 만...
    if (filter) {
      q.filters = [];
      this.parseParameter(filter, q.filters)
    }

    if (typeof skip === 'number' && typeof take === 'number') {
      params.results_per_page = take;
      params.page = Math.floor(skip / take) + 1;
    }

    if (sort) {
      q.order_by = sort.map((v) => ({
        field: v.selector,
        direction: v.desc ? 'desc' : 'asc',
      }));
    }

    if (defaultFilter && defaultFilter.length) {
      if (!q.filters) q.filters = [];
      if (!q.filters.length) q.filters = defaultFilter;
      else q.filters = [...q.filters, ...defaultFilter];
    }
    if (defaultSort && defaultSort.length) {
      let order_by = defaultSort.map((v) => ({
        field: v.selector,
        direction: v.desc ? 'desc' : 'asc',
      }));

      if (!q.order_by) q.order_by = [];
      if (!q.order_by.length) q.order_by = order_by;
      else q.order_by = [...q.order_by, ...order_by];
    }

    if (Object.keys(q).length) params.q = JSON.stringify(q);
    return params;
  }
}
