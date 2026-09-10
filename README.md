# Game Template

Svelte 5 + Vite + PixiJS 游戏模板，内置 Lingui 本地化与可选设计系统。

## 开始新项目

复制本目录（或 clone 后删除 `.git`），在项目根目录运行：

```sh
python setup.py
```

交互式完成：

1. 项目重命名（`package.json` name 与 `index.html` title）
2. 删除 `.git/` 并重新 `git init`（主分支 `main`）
3. 可选生成 `AGENTS.md`（含本地化方案使用说明）
4. 可选移除内置设计系统 `src/lib/style/`

支持非交互：`python setup.py --name my-game --yes`。

## 常用命令

```sh
pnpm dev        # 开发
pnpm build      # 构建产物到 dist/
pnpm check      # svelte-check + tsc 类型检查
pnpm lint       # oxlint
pnpm fmt        # oxfmt

pnpm i18n:extract    # 提取文案到 src/locales/<locale>/messages.po
pnpm i18n:compile    # 编译 PO 为 messages.mjs
```

## 本地化

基于 [lingui-for-svelte](https://github.com/lingui/lingui-for-svelte)（Lingui v6），
源语言为 `zh-Hans`，源码字符串直接写中文：

```svelte
<script lang="ts">
    import { t } from "lingui-for-svelte/macro"
</script>

<span>{$t`中文文案`}</span>
```

流程：改文案 → `pnpm extract` → 翻译各语言 PO → `pnpm compile`。
新增语言需在 `lingui.config.ts` 的 `locales` 中登记，并在
`src/locales/catalog.ts` 注册编译产物；详见模板生成的 `AGENTS.md`。
