import defaultLayout from '@/layouts/side-nav-outer-toolbar';
import setup from '@/views/common/setup';
import menu from '@/views/common/menu';
import authGroup from '@/views/common/auth-group';
import menuGroup from '@/views/common/menu-group'
import code from '@/views/common/code';
import control from '@/views/common/control';

export default [
  {
    path: '/common/setup',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: setup,
  },
  {
    path: '/common/menu',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: menu,
  },
  {
    path: '/common/group/auth',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: authGroup,
  },
  {
    path: '/common/group/menu',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: menuGroup,
  },
  {
    path: '/common/code',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: code,
  },
  {
    path: '/common/control',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: control,
  },
];
