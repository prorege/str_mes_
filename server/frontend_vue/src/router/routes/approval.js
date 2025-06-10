import defaultLayout from '@/layouts/side-nav-outer-toolbar';
import approvalManagement from '@/views/approval/management';

export default [
  {
    path: '/approval/management',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: approvalManagement,
  },
];

