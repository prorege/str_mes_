import ApiService from './utils/api-service';
import store from '@/utils/store'

const apiService = new ApiService('/api/monitor/v1');
// const menuService = new ApiService('/api/mes/v1/setup/')

const cookieOptions = {expires: 1}
const getExpire = () => Date.now() + (3 * 60 * 60 * 1000)

const authService = {
  _user: null,
  _logo: null,
  _token: null,
  _menu: [],
  loggedIn() {
    return !!this._user;
  },

  get user() {
    return this._user;
  },

  get token () {
    const t = store.get('token')
    if (t) {
      store.set('token', t, getExpire())
      return t
    }
    else return null
  },

  async logIn(user_id, user_pw) {
    try {
      // Send request
      let { data } = await apiService.post('login', { user_id, user_pw });
      if (!data.status) throw Error(data.reason);

      this._user = data.user;
      data.user.department = data.department;
      this._logo = data.logo;
      this._token = data.user.token;
      this._menu = data.menu;

      const expired = getExpire()
      store.set('token', data.user.token, expired)
      store.set('auth', JSON.stringify(data.user), expired);
      store.set('menu', JSON.stringify(data.menu), expired);
      store.set('logo', data.logo || '', expired);

      return {
        isOk: true,
        data: this._user,
      };
    } catch {
      return {
        isOk: false,
        message: 'Authentication failed',
      };
    }
  },

  async logOut() {
    this._user = null;
    this._token = null;
    store.remove('token');
    store.remove('auth');
    store.remove('logo');
    store.remove('menu');
  },

  async getUser() {
    try {
      // Send request

      return {
        isOk: true,
        data: this._user,
        logo: this._logo,
      };
    } catch {
      return {
        isOk: false,
      };
    }
  },

  getCompanyId() {
    return this._user.fk_company_id;
  },
  getDepartmentName() {
    return this._user.department.department_name;
  },
  getUserName() {
    return this._user.user_name;
  },
  getWarehouseCode() {
    return authService._user.department.wh_code;
  },
  getMenu() {
    return this._menu;
  },
  checkAvailMenu(path) {
    return !!this._menu.find(v => v.path === path);
  },
  async resetPassword(email) {
    try {
      // Send request
      console.log(email);

      return {
        isOk: true,
      };
    } catch {
      return {
        isOk: false,
        message: 'Failed to reset password',
      };
    }
  },

  async changePassword(email, recoveryCode) {
    try {
      // Send request
      console.log(email, recoveryCode);

      return {
        isOk: true,
      };
    } catch {
      return {
        isOk: false,
        message: 'Failed to change password',
      };
    }
  },

  async createAccount(email, password) {
    try {
      // Send request
      console.log(email, password);

      return {
        isOk: true,
      };
    } catch {
      return {
        isOk: false,
        message: 'Failed to create account',
      };
    }
  },
};

const onCreatedAuthController = () => {
  try {
    let k = store.get('token');
    let s = store.get('auth');
    let l = store.get('logo');
    let m = store.get('menu');
    if (s) {
      authService._user = JSON.parse(s);
      authService._menu = JSON.parse(m);
      authService._logo = l;
      authService._token = k;
    }
  } catch (ex) {
    console.error(ex.message);
  }
};

onCreatedAuthController();

export default authService;
