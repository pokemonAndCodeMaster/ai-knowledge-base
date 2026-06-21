# 前端模块占位

这里保留 Vue3 + TypeScript + Vite 前端工程的边界。后续正式初始化前端时，保持以下约定：

- 页面放在 `src/frontend/src/views/<module>/`。
- 后端 API 调用放在 `src/frontend/src/api/`。
- TypeScript 类型放在 `src/frontend/src/types/`。
- 跨模块组件放在 `src/frontend/src/components/`。
- 路由配置是侧边菜单的唯一事实源。
