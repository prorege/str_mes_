import defaultLayout from '@/layouts/side-nav-outer-toolbar';
import testRegistration from '@/views/quality/test-registration';
import testRegistrationStatus from '@/views/quality/test-registration-status';
import testRegistrationStatus_ from '@/views/quality/test-registration-status_';
import nonconformanceAction from '@/views/quality/nonconformance-action';
import nonconformanceActionStatus from '@/views/quality/nonconformance-action-status';
import measuringEquipment from '@/views/quality/measuring-equipment';
import qaStandard from '@/views/quality/qa-standard';
import E7 from '@/views/quality/7';
import E8 from '@/views/quality/8';

export default [
  {
    path: '/quality/test-registration',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: testRegistration,
  },
  {
    path: '/quality/test-registration/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: testRegistration,
    props: true,
  },
  {
    path: '/quality/test-registration-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: testRegistrationStatus,
  },
  {
    path: '/quality/test-registration-status_',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: testRegistrationStatus_,
  },
  {
    path: '/quality/nonconformance-action',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: nonconformanceAction,
  },
  {
    path: '/quality/nonconformance-action-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: nonconformanceActionStatus,
  },
  {
    path: '/quality/measuring-equipment',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: measuringEquipment,
  },
  {
    path: '/quality/qa-standard',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: qaStandard,
  },
  {
    path: '/quality/7',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: E7,
  },
  {
    path: '/quality/8',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: E8,
  },
];
