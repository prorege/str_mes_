import defaultLayout from "@/layouts/side-nav-outer-toolbar"

import qr from '@/views/qr/qr'
import lot from '@/views/qr/lot'

export default [
  {
    path: "/qr/qr",
    meta: { requiresAuth: true, layout: defaultLayout },
    component: qr
  },
  {
    path: "/qr/lot",
    meta: { requiresAuth: true, layout: defaultLayout },
    component: lot
  }
]