import defaultLayout from '@/layouts/side-nav-outer-toolbar';

import Etc from '@/views/stock/etc';
import Etc_ from '@/views/stock/etc_';
import EtcStatus from '@/views/stock/etc-status';
import EtcStatus_ from '@/views/stock/etc_-status';
import MoveRequest from '@/views/stock/move-request';
import MoveRequestStatus from '@/views/stock/move-request-status';
import StockStatus from '@/views/stock/stock-status';
import StockPrice from '@/views/stock/stock-price';
import ReceivePaymentStatus from '@/views/stock/receive-payment-status';
import MoveRelease from '@/views/stock/move-release';
import MoveReleaseStatus from '@/views/stock/move-release-status';
import StockCorrection from '@/views/stock/stock-correction';
import StockCorrectionStatus from '@/views/stock/stock-correction-status';
import StockItemStatus from '@/views/stock/stock-item-status';

export default [
  {
    path: '/stock/etc',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: Etc,
  },
  {
    path: '/stock/etc/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: Etc,
    props: true
  },
  {
    path: '/stock/etc_',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: Etc_,
  },
  {
    path: '/stock/etc_/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: Etc_,
    props: true
  },
  {
    path: '/stock/etc_-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: EtcStatus_,
  },
  {
    path: '/stock/etc-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: EtcStatus,
  },
  {
    path: '/stock/move-request',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: MoveRequest,
  },
  {
    path: '/stock/move-request/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: MoveRequest,
    props: true
  },
  {
    path: '/stock/move-request-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: MoveRequestStatus,
  },
  {
    path: '/stock/move-release',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: MoveRelease,
  },
  {
    path: '/stock/move-release/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: MoveRelease,
    props: true
  },
  {
    path: '/stock/move-release-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: MoveReleaseStatus,
  },
  {
    path: '/stock/stock-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: StockStatus,
  },
  {
    path: '/stock/stock-price',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: StockPrice,
  },
  {
    path: '/stock/receive-payment-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: ReceivePaymentStatus,
  },
  {
    path: '/stock/stock-correction',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: StockCorrection,
  },
  {
    path: '/stock/stock-correction/:id',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: StockCorrection,
    props: true
  },
  {
    path: '/stock/stock-correction-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: StockCorrectionStatus,
  },
  {
    path: '/stock/stock-item-status',
    meta: { requiresAuth: true, layout: defaultLayout },
    component: StockItemStatus,
  },
];
