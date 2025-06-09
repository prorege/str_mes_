import defaultLayout from '@/layouts/side-nav-outer-toolbar';
import registration from '@/views/project/registration';
import status from '@/views/project/status';
import notice from '@/views/project/notice';
import schedule from '@/views/project/schedule';
import resource from '@/views/project/resource';
import business from '@/views/project/business';
import businessStatus from '@/views/project/business-status'
import excutionPlan from '@/views/project/excution-plan';
import excutionPlanStatus from '@/views/project/excution-plan-status';
import businessTripLog from '@/views/project/business-trip-log';
import businessTripLogStatus from '@/views/project/business-trip-log-status';
import excutionPlanToOrder from '@/views/project/excution-plan-to-order';
import happyCall from '@/views/project/happy-call';
import mdRegistration from '@/views/project/md-registration';
import mdStatus from '@/views/project/md-status';

export default [
  {
    path: '/project/registration',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: registration,
  },
  {
    path: '/project/registration/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: registration,
    props: true,
  },
  {
    path: '/project/registration/business/:business_id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: registration,
    props: true,
  },
  {
    path: '/project/status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: status,
  },
  {
    path: '/project/notice',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: notice,
  },
  {
    path: '/project/schedule',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: schedule,
  },
  {
    path: '/project/resource',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: resource,
  },
  {
    path: '/project/business',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: business,
  },
  {
    path: '/project/business/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: business,
    props: true,
  },
  {
    path: '/project/business-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: businessStatus,
  },
  {
    path: '/project/excution-plan',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: excutionPlan,
  },
  {
    path: '/project/excution-plan/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: excutionPlan,
    props: true,
  },
  {
    path: '/project/excution-plan/project/:project_id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: excutionPlan,
    props: true,
  },
  {
    path: '/project/excution-plan-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: excutionPlanStatus,
  },
  {
    path: '/project/business-trip-log',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: businessTripLog,
  },
  {
    path: '/project/business-trip-log-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: businessTripLogStatus,
  },
  {
    path: '/project/excution-plan-to-order',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: excutionPlanToOrder,
  },
  {
    path: '/project/happy-call',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: happyCall,
  },
  {
    path: '/project/md-registration',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: mdRegistration,
  },
  {
    path: '/project/md-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: mdStatus,
  }
];
