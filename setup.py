#!/usr/bin/env python3
"""交互式 setup 脚本：把这份模板变成一个新的游戏项目。

用法（在模板副本的根目录执行）：

    python setup.py

也可以非交互式运行：

    python setup.py --name my-game --yes

功能：
    1. 重命名项目（package.json name + index.html title）
    2. 删除 .git/ 并重新 git init，主分支为 main
    3. 可选生成 AGENTS.md（含本地化方案使用说明）
    4. 可选移除自带设计系统（src/lib/style/）
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GIT_DIR = ROOT / ".git"
PACKAGE_JSON = ROOT / "package.json"
INDEX_HTML = ROOT / "index.html"
APP_CSS = ROOT / "src" / "app.css"
STYLE_DIR = ROOT / "src" / "style"

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


def normalize_name(raw: str) -> str:
    name = raw.strip().lower().replace(" ", "-")
    return re.sub(r"[^a-z0-9._-]+", "-", name).strip("-") or "my-game"


def ask(prompt: str, default: bool) -> bool:
    hint = "[Y/n]" if default else "[y/N]"
    while True:
        try:
            answer = input(f"{prompt} {hint}: ").strip().lower()
        except EOFError:
            return default
        if not answer:
            return default
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  请输入 y 或 n")


def ask_text(prompt: str, default: str) -> str:
    suffix = f" [{default}]" if default else ""
    try:
        answer = input(f"{prompt}{suffix}: ").strip()
    except EOFError:
        return default
    return answer or default


# ---------------------------------------------------------------- rename


def rename_project(new_name: str) -> None:
    with open(PACKAGE_JSON, encoding="utf-8") as f:
        pkg = json.load(f)

    old_name = pkg.get("name", "")
    pkg["name"] = new_name
    with open(PACKAGE_JSON, "w", encoding="utf-8") as f:
        json.dump(pkg, f, indent=4, ensure_ascii=False)
        f.write("\n")
    print(f"  package.json: name {old_name!r} -> {new_name!r}")

    html = INDEX_HTML.read_text(encoding="utf-8")
    new_html, count = re.subn(
        r"(<title>)[^<]*(</title>)", rf"\g<1>{new_name}\g<2>", html, count=1
    )
    if count:
        INDEX_HTML.write_text(new_html, encoding="utf-8")
        print(f"  index.html:   title -> {new_name!r}")
    else:
        print("  index.html:   未找到 <title>，跳过")


# ---------------------------------------------------------------- git


def reinit_git() -> None:
    if GIT_DIR.exists():
        shutil.rmtree(GIT_DIR)
        print("  已删除旧 .git/")
    if shutil.which("git") is None:
        print("  错误：未找到 git，跳过仓库初始化")
        return
    subprocess.run(["git", "init", "-b", "main"], cwd=ROOT, check=True)
    print("  已初始化新仓库，主分支为 main")


# ---------------------------------------------------------------- AGENTS.md


AGENTS_TEMPLATE = """\
# AGENTS.md

__PROJECT_NAME__ 的开发约定与工具链说明。

## 常用命令

| 命令 | 说明 |
| --- | --- |
| `pnpm dev` | 启动开发服务器 |
| `pnpm build` | 生产构建 |
| `pnpm check` | svelte-check + tsc 类型检查 |
| `pnpm lint` / `pnpm lint:fix` | oxlint 检查 / 自动修复 |
| `pnpm fmt` | oxfmt 格式化 |
| `pnpm i18n:extract` / `pnpm i18n:compile` | 提取 / 编译多语言目录 |

## 本地化方案（Lingui + lingui-for-svelte）

- 技术栈：`@lingui/core` v6 + `lingui-for-svelte`，**源语言为 zh-Hans**，
  源码中的字符串直接写中文。
- Svelte 组件中：

  ```svelte
  <script lang="ts">
      import { t } from "lingui-for-svelte/macro"
  </script>

  <span>{$t`中文文案`}</span>
  <span>{$t`还有 ${count} 个未完成`}</span><!-- 插值 -->
  ```

- 普通 `.ts` 数据模块中用 `msg` 宏（由 `unplugin-lingui-macro` 处理），
  先把 `msg\\`...\\`` 存进数据结构，渲染时再经 `$t(...)` 翻译：

  ```ts
  import { msg } from "@lingui/core/macro"

  export const label = msg`开始游戏`
  ```

### 工作流

1. 改动文案后在项目根目录执行 `pnpm extract`，扫描 `src/` 更新
   `src/locales/<locale>/messages.po`；
2. 翻译各语言 PO 文件里的 `msgstr`（zh-Hans 是源语言，无需翻译）；
3. 执行 `pnpm compile` 把 PO 编译成 `messages.mjs`
   （`src/locales/catalog.ts` 静态引用这些产物）。

### 新增语言

1. 在 `lingui.config.ts` 的 `locales` 数组中加入 BCP-47 语言代码（如 `ja`）；
2. `pnpm extract` 生成对应 PO，翻译后 `pnpm compile`；
3. 在 `src/locales/catalog.ts` 中注册该语言的编译产物。

### 注意事项

- **不要手动编辑** `src/locales/*/messages.mjs`，那是编译产物，一切以 `.po` 为准；
- 运行时切换语言调用 `src/i18n.ts` 中的 `changeLanguage(locale)`；
- 提交代码时 `.po` 与 `.mjs` 都要入库，保证克隆后可直接构建。
"""

STYLE_SECTION = """
## 设计系统

`src/style/` 提供基于 Tailwind CSS v4 的主题令牌与组件类：

- 入口为 `src/app.css` 中的 `@import "./lib/style/index.css"`；
- 颜色令牌定义在 `colors.css`（`--color-primary`、`--color-base-100` 等，
  通过 `.dark` 类支持暗色模式）；
- 组件类包括 `btn`、`card`、`modal`、`input`、`toggle`、`badge`、`kbd` 等，
  用法同 DaisyUI 风格：`class="btn btn-primary btn-sm"`。
"""


def write_agents_md(project_name: str, include_style: bool) -> None:
    content = AGENTS_TEMPLATE.replace("__PROJECT_NAME__", project_name)
    if include_style:
        content += STYLE_SECTION
    path = ROOT / "AGENTS.md"
    path.write_text(content, encoding="utf-8")
    print(f"  已生成 {path.name}")


# ---------------------------------------------------------------- style


def remove_style() -> None:
    if STYLE_DIR.exists():
        shutil.rmtree(STYLE_DIR)
        print("  已删除 src/style/")
    css = APP_CSS.read_text(encoding="utf-8")
    cleaned = "\n".join(
        line for line in css.splitlines() if "./style/index.css" not in line
    )
    APP_CSS.write_text(cleaned.rstrip() + "\n", encoding="utf-8")
    print(f"  已从 {APP_CSS.relative_to(ROOT)} 移除样式导入")


# ---------------------------------------------------------------- main


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="交互式初始化新的游戏项目")
    parser.add_argument("--name", help="新项目名称（跳过重命名提问）")
    parser.add_argument(
        "--git",
        dest="git",
        action="store_true",
        default=None,
        help="重建 git 仓库（默认询问）",
    )
    parser.add_argument(
        "--no-git", dest="git", action="store_false", help="不重建 git 仓库"
    )
    parser.add_argument(
        "--agents",
        dest="agents",
        action="store_true",
        default=None,
        help="生成 AGENTS.md（默认询问）",
    )
    parser.add_argument(
        "--no-agents", dest="agents", action="store_false", help="不生成 AGENTS.md"
    )
    parser.add_argument(
        "--style",
        dest="style",
        action="store_true",
        default=None,
        help="保留设计系统（默认询问）",
    )
    parser.add_argument(
        "--no-style", dest="style", action="store_false", help="移除设计系统"
    )
    parser.add_argument(
        "-y", "--yes", action="store_true", help="全部采用默认值，不再询问"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    with open(PACKAGE_JSON, encoding="utf-8") as f:
        current_name = json.load(f).get("name", "")

    # ---- 项目名
    if args.name is not None:
        new_name = normalize_name(args.name)
    elif args.yes:
        new_name = current_name
    else:
        print("=" * 46)
        print(" 游戏模板初始化")
        print("=" * 46)
        while True:
            raw = ask_text("新项目名称（回车保持当前名称）", current_name)
            candidate = normalize_name(raw) if raw else raw
            if not candidate or NAME_RE.match(candidate):
                new_name = candidate
                break
            suggestion = normalize_name(raw)
            print(f"  名称不合法（仅限小写字母、数字、. _ -），建议：{suggestion}")
            raw = ask_text("请重试", suggestion)
            candidate = normalize_name(raw) if raw else raw
            if candidate and NAME_RE.match(candidate):
                new_name = candidate
                break
            print("  已使用建议名称")

    do_git = (
        args.git
        if args.git is not None
        else (
            True
            if args.yes
            else ask("重建 git 仓库（删除 .git 后重新 init，主分支 main）？", True)
        )
    )
    do_agents = (
        args.agents
        if args.agents is not None
        else (True if args.yes else ask("生成 AGENTS.md（含本地化使用说明）？", True))
    )
    keep_style = (
        args.style
        if args.style is not None
        else (True if args.yes else ask("保留内置设计系统（src/style/）？", True))
    )

    print("\n即将执行：")
    print(
        f"  1. 项目名称     : {'保持 ' + current_name if new_name == current_name else current_name + ' -> ' + new_name}"
    )
    print(f"  2. 重建 git 仓库: {'是' if do_git else '否'}")
    print(f"  3. 生成 AGENTS.md: {'是' if do_agents else '否'}")
    print(f"  4. 设计系统     : {'保留' if keep_style else '移除'}")
    if not args.yes:
        if not ask("\n确认执行？", True):
            print("已取消。")
            return 1

    print()

    if new_name != current_name:
        rename_project(new_name)
    else:
        print("  项目名称未变化，跳过重命名")

    if do_git:
        reinit_git()

    if do_agents:
        write_agents_md(new_name or current_name, include_style=keep_style)

    if not keep_style:
        remove_style()

    print("\n完成。接下来可以运行：\n  pnpm install\n  pnpm dev")
    return 0


if __name__ == "__main__":
    sys.exit(main())
