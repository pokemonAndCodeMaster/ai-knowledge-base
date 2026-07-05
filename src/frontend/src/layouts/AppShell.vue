<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar">
      <div class="brand"><span>QC</span><strong>质检一站式平台</strong></div>
      <nav aria-label="主导航">
        <p>人工质检</p>
        <RouterLink to="/manual-qc/acceptance">验收中心</RouterLink>
      </nav>
    </aside>
    <main class="app-main">
      <header class="topbar"><span>人工质检 / 验收中心</span><strong>当前用户：王敏</strong></header>
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.app-shell { min-height: 100vh; background: var(--color-bg); }
.sidebar { position: fixed; inset: 0 auto 0 0; width: 232px; padding: 18px 14px; border-right: 1px solid var(--color-line); background: #eef1f4; }
.brand { display: flex; align-items: center; gap: 10px; padding-bottom: 20px; }
.brand span { display: grid; width: 34px; height: 34px; place-items: center; border-radius: 6px; background: #172434; color: white; font-weight: 800; }
nav p { margin: 18px 8px 6px; color: var(--color-muted); font-size: 12px; }
nav a { display: block; padding: 10px 12px; border-radius: 5px; text-decoration: none; }
nav a.router-link-active { color: var(--color-blue); background: var(--color-blue-soft); font-weight: 750; }
.app-main { margin-left: 232px; }
.topbar { display: flex; height: 64px; align-items: center; justify-content: space-between; padding: 0 28px; border-bottom: 1px solid var(--color-line); background: white; color: var(--color-muted); }
@media (max-width: 760px) { .sidebar { position: static; width: auto; } .app-main { margin-left: 0; } }
</style>
