import defaultLayout from "@/layouts/side-nav-outer-toolbar"

import production from '@/views/eis/production'
import project from '@/views/eis/project'
import sales from '@/views/eis/sales'
import purchase from '@/views/eis/purchase'

export default [
  {
    path: "/eis/production",
    meta: { requiresAuth: true, layout: defaultLayout },
    component: production
  },
  {
    path: "/eis/project",
    meta: { requiresAuth: true, layout: defaultLayout },
    component: project
  },
  {
    path: "/eis/sales",
    meta: { requiresAuth: true, layout: defaultLayout },
    component: sales
  },
  {
    path: "/eis/purchase",
    meta: { requiresAuth: true, layout: defaultLayout },
    component: purchase
  }
]