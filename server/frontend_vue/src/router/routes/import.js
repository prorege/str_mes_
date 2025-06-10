import defaultLayout from '@/layouts/side-nav-outer-toolbar';

import purchaseOrder from '@/views/import/purchase-order';
import shipment from '@/views/import/shipment';
import clearance from '@/views/import/clearance';
import credit from '@/views/import/credit';
import approval from '@/views/import/approval';
import approvalCost from '@/views/import/approval-cost';
import clearanceCost from '@/views/import/clearance-cost';

export default [
  {
    path: '/import/purchase-order',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: purchaseOrder,
  },
  {
    path: '/import/purchase-order/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: purchaseOrder,
    props: true,
  },
  {
    path: '/import/shipment',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: shipment,
  },
  {
    path: '/import/shipment/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: shipment,
    props: true,
  },
  {
    path: '/import/clearance',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: clearance,
  },
  {
    path: '/import/clearance/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: clearance,
    props: true,
  },
  {
    path: '/import/credit',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: credit,
  },
  {
    path: '/import/credit/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: credit,
    props: true,
  },
  {
    path: '/import/approval',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: approval,
  },
  {
    path: '/import/approval/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: approval,
    props: true,
  },
  {
    path: '/import/approval-cost',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: approvalCost,
  },
  {
    path: '/import/approval-cost/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: approvalCost,
    props: true,
  },
  {
    path: '/import/clearance-cost',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: clearanceCost,
  },
  {
    path: '/import/clearance-cost/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: clearanceCost,
    props: true,
  },
];
