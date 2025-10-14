import defaultLayout from '@/layouts/side-nav-outer-toolbar';
import receipt from '@/views/as/receipt';
import result from '@/views/as/result';
import receiptResultStatus from '@/views/as/receipt-result-status';

export default [
  {
    path: '/as/receipt',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: receipt,
  },
  {
    path: '/as/receipt/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: receipt,
    props: true,
  },
  {
    path: '/as/result',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: result,
  },
  {
    path: '/as/result/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: result,
    props: true,
  },
  {
    path: '/as/receipt-result-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: receiptResultStatus,
  },
];