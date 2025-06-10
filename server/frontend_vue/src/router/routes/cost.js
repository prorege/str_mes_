import defaultLayout from '@/layouts/side-nav-outer-toolbar';
import closing from '@/views/cost/closing';
import closingReceivePaymentStatus from '@/views/cost/closing-receive-payment-status';
import stockItemStatus from '@/views/cost/stock-item-status';
import closingStockStatus from '@/views/cost/closing-stock-status';
import closingStockGroupStatus from '@/views/cost/closing-stock-group-status';
import profitStatus from '@/views/cost/profit-status';
import profitStockStatus from '@/views/cost/profit-stock-status';
import produceSalesCostStatus from '@/views/cost/produce-sales-cost-status';
import correction from '@/views/cost/correction';


export default [
  {
    path: '/cost/closing',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: closing,
  },
  {
    path: '/cost/closing-receive-payment-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: closingReceivePaymentStatus,
  },
  {
    path: '/cost/stock-item-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: stockItemStatus,
  },
  {
    path: '/cost/produce-sales-cost-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: produceSalesCostStatus,
  },
  {
    path: '/cost/closing-stock-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: closingStockStatus,
  },
  {
    path: '/cost/closing-stock-group-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: closingStockGroupStatus,
  },
  {
    path: '/cost/profit-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: profitStatus,
  },{
    path: '/cost/profit-stock-status',
    meta: { requiresAuth: true, layout: defaultLayout},
    component: profitStockStatus,
  },
  {
    path: '/cost/correction',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: correction,
  },
];
