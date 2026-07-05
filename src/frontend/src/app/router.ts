import { createRouter, createWebHistory } from 'vue-router'

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/manual-qc/acceptance' },
    {
      path: '/manual-qc/acceptance',
      name: 'manual-qc-acceptance',
      component: () => import('@/features/manual-qc/acceptance/views/AcceptanceQueueView.vue'),
      meta: { title: '验收中心' },
    },
  ],
})
