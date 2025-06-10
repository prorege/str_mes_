import defaultLayout from '@/layouts/side-nav-outer-toolbar';
import code from '@/views/base/code';
import employee from '@/views/base/employee';
import warehouse from '@/views/base/warehouse';
import client from '@/views/base/client';
import item from '@/views/base/item';
import process from '@/views/base/process';
import bom from '@/views/base/bom';
import bank from '@/views/base/bank';

export default [
  {
    path: '/base/code',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: code,
  },
  {
    path: '/base/employee',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: employee,
  },
  {
    path: '/base/warehouse',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: warehouse,
  },
  {
    path: '/base/client',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: client
  },
  {
    path: '/base/item',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: item,
  },
  {
    path: '/base/process',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: process,
  },
  {
    path: '/base/bom',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: bom,
  },
  {
    path: '/base/bank',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: bank,
  },
];
