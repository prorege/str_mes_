import defaultLayout from '@/layouts/side-nav-outer-toolbar';
import approvalManagement from '@/views/approval/management';
import document from '@/views/approval/document.vue';
import request from '@/views/approval/request.vue';
import approval from '@/views/approval/approval.vue';

export default [
  {
    path: '/approval/management',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: approvalManagement,
  },
  {
    path: '/approval/document',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: document,
  },
  {
    path: '/approval/approval',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: approval,
  },
  {
    path: '/approval/request',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: request,
  },
];

