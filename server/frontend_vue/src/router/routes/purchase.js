import defaultLayout from '@/layouts/side-nav-outer-toolbar';

import orderPlan from '@/views/purchase/order-plan';
import order from '@/views/purchase/order';
import preReceiving from '@/views/purchase/pre-receiving';
import receiving from '@/views/purchase/receiving';
import receivingReturn from '@/views/purchase/receiving-return';
import orderPlanStatus from '@/views/purchase/order-plan-status';
import orderStatus from '@/views/purchase/order-status';
import preReceivingStatus from '@/views/purchase/pre-receiving-status';
import receivingStatus from '@/views/purchase/receiving-status';
import receivingReturnStatus from '@/views/purchase/receiving-return-status';
import orderReceivingStatus from '@/views/purchase/order-receiving-status';
import orderReceivingStatus_ from '@/views/purchase/order-receiving-status_';
import orderPrereceivingStatus from '@/views/purchase/order-to-prereceiving-status';
import prereceivingReceivingStatus from '@/views/purchase/prereceiving-to-receiving-status';
import statement from '@/views/purchase/statement';
import payment from '@/views/purchase/payment';
import balanceItemStatus from '@/views/purchase/balance-item-status';
import balanceStatus from '@/views/purchase/balance-status';

export default [
  {
    path: '/purchase/order-plan',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: orderPlan,
  },
  {
    path: '/purchase/order-plan/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: orderPlan,
    props: true,
  },
  {
    path: '/purchase/order',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: order,
  },
  {
    path: '/purchase/order/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: order,
    props: true,
  },
  {
    path: '/purchase/pre-receiving',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: preReceiving,
  },
  {
    path: '/purchase/pre-receiving/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: preReceiving,
    props: true,
  },
  {
    path: '/purchase/receiving',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: receiving,
  },
  {
    path: '/purchase/receiving/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: receiving,
    props: true,
  },
  {
    path: '/purchase/receiving-return',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: receivingReturn,
  },
  {
    path: '/purchase/receiving-return/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: receivingReturn,
    props: true,
  },
  {
    path: '/purchase/order-plan-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: orderPlanStatus,
  },
  {
    path: '/purchase/order-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: orderStatus,
  },
  {
    path: '/purchase/pre-receiving-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: preReceivingStatus,
  },
  {
    path: '/purchase/receiving-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: receivingStatus,
  },
  {
    path: '/purchase/receiving-return-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: receivingReturnStatus,
  },
  {
    path: '/purchase/order-receiving-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: orderReceivingStatus,
  },
  {
    path: '/purchase/order-receiving-status_',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: orderReceivingStatus_,
  },
  {
    path: '/purchase/order-to-prereceiving-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: orderPrereceivingStatus,
  },
  {
    path: '/purchase/prereceiving-to-receiving-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: prereceivingReceivingStatus,
  },
  {
    path: '/purchase/statement',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: statement,
  },
  {
    path: '/purchase/statement/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: statement,
    props: true,
  },
  {
    path: '/purchase/payment',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: payment,
  },
  {
    path: '/purchase/payment/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: payment,
    props: true,
  },
  {
    path: '/purchase/balance-item-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: balanceItemStatus,
  },
  {
    path: '/purchase/balance-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: balanceStatus,
  },
];

