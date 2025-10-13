import auth from '@/auth';
import { createRouter, createWebHistory } from 'vue-router';

import Home from '@/views/home';
import Profile from '@/views/profile';
import Tasks from '@/views/tasks';
import defaultLayout from '@/layouts/side-nav-outer-toolbar';
import simpleLayout from '@/layouts/single-card';

import RtQr from './routes/qr';
import RtShipment from './routes/shipment';
import RtPurchase from './routes/purchase';
import RtStock from './routes/stock';
import RtQuality from './routes/quality';
import RtProduce from './routes/produce';
import RtProject from './routes/project';
import RtMonitoring from './routes/monitoring';
import RtBase from './routes/base';
import RtCommon from './routes/common';
import RtEis from './routes/eis';
import RtKpi from './routes/kpi';
import RtCost from './routes/cost';
import RtImport from './routes/import';
import RtExport from './routes/export';
import RtApproval from './routes/approval';
import RtAs from './routes/as';

function loadView(view) {
  return () => import(/* webpackChunkName: "login" */ `../views/${view}.vue`);
}

const router = new createRouter({
  routes: [
    ...RtQr,
    ...RtShipment,
    ...RtPurchase,
    ...RtStock,
    ...RtQuality,
    ...RtProduce,
    ...RtProject,
    ...RtMonitoring,
    ...RtBase,
    ...RtCommon,
    ...RtEis,
    ...RtKpi,
    ...RtCost,
    ...RtImport,
    ...RtExport,
    ...RtApproval,
    ...RtAs,
    {
      path: '/home',
      name: 'home',
      meta: {
        requiresAuth: true,
        layout: defaultLayout,
      },
      component: Home,
    },
    {
      path: '/profile',
      name: 'profile',
      meta: {
        requiresAuth: true,
        layout: defaultLayout,
      },
      component: Profile,
    },
    {
      path: '/tasks',
      name: 'tasks',
      meta: {
        requiresAuth: true,
        layout: defaultLayout,
      },
      component: Tasks,
    },
    {
      path: '/login-form',
      name: 'login-form',
      meta: {
        requiresAuth: false,
        layout: simpleLayout,
        title: '로그인',
      },
      component: loadView('login-form'),
    },
    {
      path: '/reset-password',
      name: 'reset-password',
      meta: {
        requiresAuth: false,
        layout: simpleLayout,
        title: '패스워드 재설정',
        description:
          '등록에 사용한 이메일 주소를 입력해 주시면 이메일을 통해 비밀번호 재설정 링크를 보내드립니다.',
      },
      component: loadView('reset-password-form'),
    },
    {
      path: '/create-account',
      name: 'create-account',
      meta: {
        requiresAuth: false,
        layout: simpleLayout,
        title: '가입하기',
      },
      component: loadView('create-account-form'),
    },
    {
      path: '/change-password/:recoveryCode',
      name: 'change-password',
      meta: {
        requiresAuth: false,
        layout: simpleLayout,
        title: '비밀번호 변경',
      },
      component: loadView('change-password-form'),
    },
    {
      path: '/',
      redirect: '/home',
    },
    {
      path: '/recovery',
      redirect: '/home',
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/home',
    },
  ],
  history: createWebHistory(),
});

router.beforeEach((to, from, next) => {
  if (to.name === 'login-form' && auth.loggedIn()) {
    next({ name: 'home' });
  }

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!auth.loggedIn()) {
      next({
        name: 'login-form',
        query: { redirect: to.fullPath },
      });
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
