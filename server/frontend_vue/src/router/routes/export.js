import defaultLayout from '@/layouts/side-nav-outer-toolbar';

import salesOrder from '@/views/export/sales-order';
import salesOrderStatus from '@/views/export/sales-order-status';
import commInvoice from '@/views/export/comm-invoice';
import commInvoiceStatus from '@/views/export/comm-invoice-status';

export default [
  {
    path: '/export/sales-order',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: salesOrder,
  },
  {
    path: '/export/sales-order/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: salesOrder,
    props: true,
  },
  {
    path: '/export/sales-order/status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: salesOrderStatus,
  },
  {
    path: '/export/comm-invoice',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: commInvoice,
  },
  {
    path: '/export/comm-invoice/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: commInvoice,
    props: true,
  },
  {
    path: '/export/comm-invoice/status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: commInvoiceStatus,
  },
];
