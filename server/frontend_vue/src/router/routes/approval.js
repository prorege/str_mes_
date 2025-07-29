import defaultLayout from '@/layouts/side-nav-outer-toolbar';
import approvalManagement from '@/views/approval/management';
import document from '@/views/approval/document.vue';

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
];

