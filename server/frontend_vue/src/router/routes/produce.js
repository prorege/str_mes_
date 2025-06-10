import defaultLayout from '@/layouts/side-nav-outer-toolbar';
import mobileLayout from '@/layouts/mobile';
import plan from '@/views/produce/plan';
import meqsureRequirement from '@/views/produce/measure-requirement';
import workOrder from '@/views/produce/work-order';
import performanceRegistration from '@/views/produce/performance-registration';
import planStatus from '@/views/produce/plan-status';
import workOrderStatus from '@/views/produce/work-order-status';
import performanceRegistrationStatus from '@/views/produce/performance-registration-status';
import workOrderReceivingStatus from '@/views/produce/work-order-receiving-status';
import processPerformanceRegistration from '@/views/produce/process_performance_registration';
import processPerformanceRegistrationVietnam from '@/views/produce/process_performance_registration_vietnam';
import processPerformanceStatus from '@/views/produce/process_performance_status'

export default [
  {
    path: '/produce/plan',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: plan,
  },
  {
    path: '/produce/plan/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: plan,
    props: true,
  },
  {
    path: '/produce/measure-requirement',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: meqsureRequirement,
  },
  {
    path: '/produce/measure-requirement/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: meqsureRequirement,
    props: true,
  },
  {
    path: '/produce/work-order',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: workOrder,
  },
  {
    path: '/produce/work-order/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: workOrder,
    props: true
  },
  {
    path: '/produce/performance-registration',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: performanceRegistration,
  },
  {
    path: '/produce/performance-registration/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: performanceRegistration,
    props: true
  },
  {
    path: '/produce/plan-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: planStatus,
  },
  {
    path: '/produce/work-order-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: workOrderStatus,
  },
  {
    path: '/produce/performance-registration-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: performanceRegistrationStatus,
  },
  {
    path: '/produce/work-order-receiving-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: workOrderReceivingStatus,
  },
  {
    path: '/produce/process-performance-registration',
    meta: { requiresAuth: true, layout: mobileLayout },
    component: processPerformanceRegistration,
  },
  {
    path: '/produce/process_performance_registration_vietnam',
    meta: { requiresAuth: true, layout: mobileLayout },
    component: processPerformanceRegistrationVietnam,
  },
  {
    path: '/produce/process-performance-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: processPerformanceStatus
  },
];
