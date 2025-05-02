import defaultLayout from "@/layouts/side-nav-outer-toolbar"
import produceprogress from '@/views/monitoring/produce-progress'
import storeStatus from '@/views/monitoring/store-status'
import project from '@/views/monitoring/project'
import quality from '@/views/monitoring/quality'
import tripLogStatus from '@/views/monitoring/trip-log-status'

export default [
  {
    path: "/monitoring/produce-progress",
    meta: { requiresAuth: true, layout: defaultLayout },
    component: produceprogress
  },
  {
    path: "/monitoring/store-status",
    meta: { requiresAuth: true, layout: defaultLayout },
    component: storeStatus
  },
  {
    path: "/monitoring/project",
    meta: { requiresAuth: true, layout: defaultLayout },
    component: project
  },
  {
    path: "/monitoring/quality",
    meta: { requiresAuth: true, layout: defaultLayout },
    component: quality
  },
  {
    path: "/monitoring/trip-log-status",
    meta: { requiresAuth: true, layout: defaultLayout },
    component: tripLogStatus
  },
]