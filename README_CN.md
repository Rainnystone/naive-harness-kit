# 欢迎来到 NHK：Naive Harness Kit

[English](README.md) | **中文**

NHK 是一个面向 Codex 和 Claude Code 的 prompt-first 懒人包，专门给那些不想先修 "Agent harness engineering" 再开工的人。

它的气质是：稍微自嘲一点，稍微谦卑一点，但尽量务实。目标不是显得很厉害，而是先把好用的工具安上、把它们合理串起来，然后尽量少折腾、少拍脑袋，把一个 agent workspace 的指令系统搭起来、维持住、别养歪。

## NHK 是什么

NHK 主要解决几类很快就会反复出现的问题：

- 先把真正有用的工作流工具接进来，尤其是 `superpowers` 和 `planning-with-files`
- 在当前环境里懒一点但别乱来地初始化 `AGENTS.md` 还是 `CLAUDE.md`
- 怎么让 `coding-agent-guide.md` 和 `documentation-governance.md` 始终和真实状态一致
- 一个 workstream 到底该继续保持 active，还是该正式进入 archive
- 整个过程尽量靠明确 prompt 驱动，而不是靠不透明的 hooks 偷偷做事

换句话说，NHK 不是要假装自己会魔法，而是想当那个有点碎嘴但还算靠谱的朋友：可以偷懒，但别糊弄；可以简化，但要把规则写下来，免得未来的你回头看时像在考古。

这套东西就是给新手、小白、懒得自己从零搭 harness 的人准备的。大佬当然可以全手搓，但 NHK 的定位本来就不是考大家是不是大佬。

## 包里有什么

NHK 自带 4 个核心 skill：

- `welcome-to-nhk`：总入口路由
- `nhk-bootstrap`：首次初始化
- `nhk-upkeep`：日常维护
- `nhk-archive`：用户确认后的归档交接

另外还带了几份冻结的本地 reference：

- `AGENTS-template.md`
- `CLAUDE-template.md`
- `coding-agent-guide-template.md`
- `documentation-governance-template.md`
- `archive-readme-template.md`
- `dependency-setup.md`
- `validation-scenarios.md`

## 文档管理逻辑

NHK 是刻意把“写给人看”和“写给 agent 看”的文档拆开的：

- `README.md` 是 GitHub 默认首页，写给人看
- `README_CN.md` 是中文配套页，写给人看
- `AGENTS.md` 是给 Codex 一类 agent 维护这个仓库时看的
- `CLAUDE.md` 是给 Claude Code 看的，并导入共享仓库规则
- 四个 skill 文件夹定义 NHK 的实际行为
- `references/` 里放的是技能会引用的冻结草稿资产和验证材料

这个拆分不是形式主义。README 负责解释 NHK 是什么、怎么安装、怎么用；`AGENTS.md` 和 `CLAUDE.md` 不负责当教程，它们的职责是告诉 coding agent 在维护 NHK 这个仓库本身时该怎么做，避免把“维护 skill 仓库”和“使用 skill”混成一团。

对于一个真正由 NHK 管理的 workspace，文档体系应该是分层的：

| 层 | 文件 | 作用 |
| --- | --- | --- |
| 指令层 | `AGENTS.md` 或 `CLAUDE.md` | 稳定执行规则、验证纪律、协作规则 |
| 路由层 | `coding-agent-guide.md` | 快速任务分流、入口文件、packet 落点、第一轮验证 |
| 治理层 | `documentation-governance.md` | active/archive 规则、命名规则、加载顺序、归档转换规则 |
| 活跃工作层 | active `specs/`、active `plans/`，以及按需启用的根目录 `task_plan.md` / `progress.md` / `findings.md` | 只放正在进行的工作 |
| 归档层 | `archive/` 加根级 `archive/README.md` | 已完成的 spec、plan、tracking，以及历史参考材料 |

NHK 在这里是故意有主张的：

- 每个 NHK-managed workspace 都应该至少有指令层、路由层、治理层
- 根目录 tracking 文件是按需启用，不是默认永远存在
- active 文档和 archive 文档不能混着放
- archive 转换必须有人类确认
- 已归档 workstream 应通过根级 `archive/README.md` 保持可检索

治理层的直接依据就是 `references/documentation-governance-template.md`。NHK 不认为文档生命周期应该靠默认脑补解决，而是要求这些规则在目标 workspace 里明确写出来。

## 依赖

NHK 默认把下面两个工作流系统视为并列依赖：

- [`superpowers`](https://github.com/obra/superpowers)：负责流程纪律、skill-first 路由、brainstorm/spec/plan 这套方法
- [`planning-with-files`](https://github.com/othmanadi/planning-with-files)：负责外部 tracking、恢复、跨轮连续性

这两个东西搭配起来的意义很大。

`superpowers` 好用，是因为它会给 agent 工作一个比较清楚的形状，不至于一路滑向“先随便做点什么再说”的即兴表演。它能帮助模型选 workflow、走 brainstorm/spec/plan 这类更稳的路径，也减少模型隔一会儿就重新发明一套方法论的冲动。

`planning-with-files` 则正好补上另一块：Codex 和 Claude Code 在长期记忆管理这件事上，实际表现都偏模糊。把任务状态、发现、进度放进外部文件，虽然不酷，但比把一切都押在模型“应该还记得吧”上可靠得多。它很适合拿来维持外部记忆，避免 agent 忘记哪个 workstream 还 active、哪些验证已经跑过、哪些事情只是看起来做完了。

合在一起看：
- `superpowers` 给流程形状
- `planning-with-files` 给记忆一个落在模型外部的稳定位置
- NHK 则用这两者去把 `AGENTS.md` / `CLAUDE.md` 初始化、日常维护、active/archive 判断这几件事做得更不拍脑袋

如果缺了其中一个，NHK 不应该装作没事继续跑，而是应该停下来问你：是要安装、启用，还是只是手动 adopt 它的工作流约定。对应说明在 [`references/dependency-setup.md`](references/dependency-setup.md)。

## 怎么安装

NHK 本质上是一个文件型 skill bundle，没有什么要编译的东西。

1. 把整个 `nhk/` 目录复制到你当前 agent 环境使用的本地 skills 目录里。
2. 保持目录结构原样，不要把 `references/` 和各个 skill 文件夹拆散。
3. 确保 `superpowers` 和 `planning-with-files` 可用；如果暂时不可用，也至少知道自己是要安装、启用，还是手动 adopt。
4. 到目标 workspace 里，从 `welcome-to-nhk` 开始，让 NHK 懒一点但别瞎猜地初始化 `AGENTS.md` 或 `CLAUDE.md`。

如果你是第一次配这种环境，不确定依赖有没有装好，这非常正常。NHK 的设计本来就是在这种地方先停下来问，而不是装懂。

## 怎么用

最短路径其实很简单：

1. 先从 `welcome-to-nhk` 开始。
2. 让它判断现在应该进入 `nhk-bootstrap`、`nhk-upkeep` 还是 `nhk-archive`。
3. 用 `nhk-bootstrap` 去建立或适配主 instruction file、两个强制 companion docs，以及根级 archive surface（`archive/` 加 `archive/README.md`）。
4. 正常开发周期走完后，用 `nhk-upkeep` 修正漂移，并确认当前 workstream 还该不该继续保持 active。
5. 只有在用户明确说“这个 workstream 完成了，可以归档”之后，才进入 `nhk-archive`。

如果你完全不知道先点哪个 skill，NHK 的态度是故意有点专断的：先走 `welcome-to-nhk`，让入口路由来当现场最清醒的那个人。

## Codex 和 Claude Code

NHK 同时兼容这两个方向：

- Codex 型 workspace 通常以 `AGENTS.md` 为核心
- Claude Code 型 workspace 通常以 `CLAUDE.md` 为核心

NHK 不会在这件事上瞎猜。如果仓库里已经有其中一个，就保留它；如果两个都有，就问人类谁才是 active，而不是擅自当皇帝判案。

## 仓库自身的维护

这个仓库本身也带了 `AGENTS.md` 和 `CLAUDE.md`。

这里的分工是：

- `AGENTS.md` 作为 coding agent 的共享仓库维护规范
- `CLAUDE.md` 导入 `AGENTS.md`，只补少量 Claude 专属说明

这样 human-facing 的 README 和 agent-facing 的工作规则就分开了。没那么花哨，但通常也更不容易出事。
