import defaultLayout from '@/layouts/side-nav-outer-toolbar';
import mobileLayout from '@/layouts/mobile';

import Quote from '@/views/shipment/quote';
import QuoteManual from '@/views/shipment/quote-manual';
import Order from '@/views/shipment/order';
import Release from '@/views/shipment/release';
import ReleaseReturn from '@/views/shipment/release-return';
import Lend from '@/views/shipment/lend';
import Retrieve from '@/views/shipment/retrieve';
import OnSite from '@/views/shipment/on-site';
import SalesStatement from '@/views/shipment/sales-statement';
import Deposit from '@/views/shipment/deposit';
import EstimateStatus from '@/views/shipment/quote-status';
import OrderStatus from '@/views/shipment/order-status';
import OrderAdminStatus from '@/views/shipment/order-admin-status';
import ReleaseStatus from '@/views/shipment/release-status';
import ReleaseReturnStatus from '@/views/shipment/release-return-status';
import ReleaseRequestStatus from '@/views/shipment/release-request-status';
import OrderToReleaseStatus from '@/views/shipment/order-to-release-status';
import SalesStatementStatus from '@/views/shipment/sales-statement-status';
import DepositStatus from '@/views/shipment/deposit-status';
import QuoteToOrderStatus from '@/views/shipment/quote-to-order-status';
import ReleaseToSalesStatus from '@/views/shipment/release-to-sales-status';
import SalesToDepositStatus from '@/views/shipment/sales-to-deposit-status';
import SalesBalanceStatus from '@/views/shipment/sales-balance-status';
import SalesBalanceItemStatus from '@/views/shipment/sales-balance-item-status';

export default [
  {
    path: '/shipment/quote',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: Quote,
  },
  {
    path: '/shipment/quote/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: Quote,
    props: true,
  },
  {
    path: '/shipment/quote/business/:business_id/',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: Quote,
    props: true,
  },
  {
    path: '/shipment/quote-manual',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: QuoteManual,
  },
  {
    path: '/shipment/quote-manual/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: QuoteManual,
    props: true,
  },
  {
    path: '/shipment/order',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: Order,
  },
  {
    path: '/shipment/order/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: Order,
    props: true,
  },
  {
    path: '/shipment/release',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: Release,
  },
  {
    path: '/shipment/release/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: Release,
    props: true,
  },
  {
    path: '/shipment/release-return',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: ReleaseReturn,
  },
  {
    path: '/shipment/release-return/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: ReleaseReturn,
    props: true,
  },
  {
    path: '/shipment/lend',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: Lend,
  },
  {
    path: '/shipment/retrieve',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: Retrieve,
  },
  {
    path: '/shipment/sales-statement',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: SalesStatement,
  },
  {
    path: '/shipment/sales-statement/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: SalesStatement,
    props: true,
  },
  {
    path: '/shipment/deposit',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: Deposit,
  },
  {
    path: '/shipment/deposit/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: Deposit,
    props: true,
  },
  {
    path: '/shipment/on-site',
    meta: { requiresAuth: true, layout: mobileLayout, title: 'PDA' },
    component: OnSite,
  },
  {
    path: '/shipment/quote/status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: EstimateStatus,
  },
  {
    path: '/shipment/order/status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: OrderStatus,
  },
  {
    path: '/shipment/order-admin/status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: OrderAdminStatus,
  },
  {
    path: '/shipment/release/status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: ReleaseStatus,
  },
  {
    path: '/shipment/release-return/status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: ReleaseReturnStatus,
  },
  {
    path: '/shipment/release-request/status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: ReleaseRequestStatus,
  },
  {
    path: '/shipment/order-to-release/status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: OrderToReleaseStatus,
  },
  {
    path: '/shipment/sales-statement/status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: SalesStatementStatus,
  },
  {
    path: '/shipment/deposit/status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: DepositStatus,
  },
  {
    path: '/shipment/quote-to-order/status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: QuoteToOrderStatus,
  },
  {
    path: '/shipment/release-to-sales/status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: ReleaseToSalesStatus,
  },
  {
    path: '/shipment/sales-to-deposit/status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: SalesToDepositStatus,
  },
  {
    path: '/shipment/sales-balance/status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: SalesBalanceStatus,
  },
  {
    path: '/shipment/sales-balance-item/status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: SalesBalanceItemStatus,
  },
];
