---
title: "质检一站式平台前端Demo设计规范"
domain: ["ai_dlc", "tooling", "agent_evaluation"]
type: "norm"
tags: ["质检平台", "前端Demo", "可访问性", "交互规范", "设计工程"]
created: 2026-07-04
updated: 2026-07-04
sources: 5
status: active
related_code: []
affects_path: ["demo/quality-check-platform.html"]
trigger_keywords: ["质检前端Demo规范", "可访问性", "动效", "Carbon", "HTML原型"]
---

# 质检一站式平台前端 Demo 设计规范

← [[质检一站式平台顶层架构]]。执行计划：[[质检一站式平台前端Demo设计计划]]。

## 设计定位

Reading this as: 面向质检运营负责人和模块管理员的企业级密集工作台，采用克制、清晰、可审计的设计语言，参考 Carbon 的信息密度与状态表达，用原生 HTML/CSS/JavaScript 实现可离线演示的定制原型。

这不是营销页。`taste-skill` 明确把 Dashboard、数据表、多步骤产品 UI 列为非适用范围，因此只使用其反模板化、主题一致性、形状一致性、真实状态和文案审查规则，不套用 Hero、Bento 或营销页结构。

## 设计拨盘

- `DESIGN_VARIANCE: 5`：允许模块脉络条和不等宽信息区，但操作区保持可预测。
- `MOTION_INTENSITY: 3`：高频工作台以即时反馈为主，不做自动编舞。
- `VISUAL_DENSITY: 8`：桌面展示高密度运营信息；数值使用等宽数字，减少无意义卡片盒。

## 视觉系统

- 主题：第一版固定浅色主题，深墨色导航，避免整页暗色造成长时间运营疲劳；后续再决定是否补暗色模式。
- 色彩：平台只有一套中性色和语义色。模块用侧边标识和脉络条区分，不改变成功、警告、失败语义。
- 形状：输入和按钮 6px，抽屉/弹窗 10px；表格和主区域以分隔线组织，不把每个指标包成卡片。
- 字体：中文优先使用系统无衬线栈；数字、任务 ID、时间和状态码使用系统等宽栈。Demo 默认零外部字体依赖。
- 图标：从 Tabler Icons 选取并内嵌同一套 SVG symbol sprite，保留来源与统一线宽；不得使用 Emoji 作为结构图标，不手绘装饰性假图标。
- 签名元素：质检脉络条。人工模块表达交付阶段，大模型模块表达六通道进度，点击节点筛选对应问题。

## 可访问性硬门槛

> 引用自 `web-design-guidelines`：`Accessibility is not optional.`

- 使用 `header/nav/main/aside/section/table/dialog` 等语义元素；禁止用 `div onclick` 模拟按钮。
- 提供跳到主内容链接；一个页面一个 `h1`，标题层级不跳级。
- 所有控件有可见标签；错误与字段通过 `aria-describedby` 或 `aria-errormessage` 关联。
- 所有功能可用键盘完成；弹窗锁定焦点并在关闭后归还触发按钮。
- `:focus-visible` 始终可见；普通文字对比度至少 4.5:1，组件边界至少 3:1。
- 状态变化通过 `aria-live="polite"` 或 `role="status"` 宣告；紧急失败才使用 `role="alert"`。
- 颜色不是唯一状态信号，必须同时有文字或图标。
- 320px 不产生整页横向滚动；表格只允许自身容器横向滚动；触控目标至少 44×44px。

## 动效硬门槛

依据 `emil-design-eng`：高频动作减少或取消动画；动效只解释空间、状态或反馈。

- 键盘触发的页面切换、筛选和列表导航不动画。
- 按钮按压 100-160ms，可使用 `scale(0.97)`，不得影响周围布局。
- Tooltip 125-180ms，抽屉/弹窗 180-260ms，Toast 180-240ms。
- 进入使用强 `ease-out`，位置迁移使用 `ease-in-out`；不使用 `ease-in`，不使用 `transition: all`。
- 弹出层从触发点出现；居中 Modal 保持中心原点。任何元素不得从 `scale(0)` 出现。
- 高频动态元素优先 CSS transition，动画只改 `transform` 和 `opacity`。
- `prefers-reduced-motion` 下取消位移动画，只保留必要的颜色/透明度反馈。

## 状态与文案

- 每个主要数据区必须具备 loading、empty、error、ready 四态。
- 异步业务额外具备 previewing、preview_ready、executing、partial_success、refreshing、settled。
- 按钮名称与完成反馈使用同一动词，例如“执行分配”完成后提示“分配已提交”。
- Mock 数字和姓名必须标明“示例数据”，不制造看似真实的精确业务指标。
- 页面可见文案不使用营销口号，不出现“无缝、赋能、下一代”等空泛词。
- 最终 HTML 的可见文案不使用 em dash 或 en dash 作为装饰分隔符。

## 实现与验收

- 计划产物：`demo/quality-check-platform.html`。
- 单文件、离线可开、Mock 数据内置；若用户允许 CDN，再单独放宽图标依赖。
- URL hash 或 query 反映模块、二级页和关键筛选，支持浏览器前进/后退。
- 验证宽度：320、375、768、1024、1440；验证键盘、焦点归还、reduced motion 和高对比模式。
- 交付前逐项执行 `web-design-guidelines` 检查和 `emil-design-eng` Before/After 评审表。
