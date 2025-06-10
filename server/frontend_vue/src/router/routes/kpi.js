import defaultLayout from "@/layouts/side-nav-outer-toolbar"
import defectiveRateStatus from '@/views/kpi/defective-rate-status'
import orderToReleaseLeadtime from '@/views/kpi/order-to-release-leadtime'
import produceLeadtime from '@/views/kpi/produce-leadtime'
import productCost from '@/views/kpi/product-cost'
import claim from '@/views/kpi/claim'
import orderToReleaseLeadtimeChart from '@/views/kpi/order-to-release-leadtime-chart'

export default [
  {
    path: "/kpi/defective-rate-status",
    meta: { requiresAuth: true, layout: defaultLayout },
    component: defectiveRateStatus
  },
  {
    path: "/kpi/order-to-release-leadtime",
    meta: { requiresAuth: true, layout: defaultLayout },
    component: orderToReleaseLeadtime
  },
  {
    path: "/kpi/produce-leadtime",
    meta: { requiresAuth: true, layout: defaultLayout },
    component: produceLeadtime
  },
  {
    path: "/kpi/product-cost",
    meta: { requiresAuth: true, layout: defaultLayout },
    component: productCost
  },
  {
    path: "/kpi/claim",
    meta: { requiresAuth: true, layout: defaultLayout },
    component: claim
  },
  {
    path: "/kpi/order-to-release-leadtime-chart",
    meta: { requiresAuth: true, layout: defaultLayout },
    component: orderToReleaseLeadtimeChart
  },
]