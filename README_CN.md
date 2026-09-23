# 欢迎来到 NHK：Naive Harness Kit

[English](README.md) | **中文**

NHK 是一个面向 Codex 和 Claude Code 的 prompt-first 懒人包，专门给那些不想先修 "Agent harness engineering" 再开工的人。

它的气质是：稍微自嘲一点，稍微谦卑一点，但尽量务实。目标不是显得很厉害，而是先把好用的工具安上、把它们合理串起来，然后尽量少折腾、少拍脑袋，把一个 agent workspace 的指令系统搭起来、维持住、别养歪。

## NHK 是什么

NHK 主要解决下面 5 类很快就会反复出现的问题：

- 先把真正有用的工作流工具接进来，尤其是 `superpowers` 和 `planning-with-files`
- 在当前环境里懒一点但别乱来地初始化 `AGENTS.md` 还是 `CLAUDE.md`
- 让指路、规划、派工、恢复和文档管理这几份说明，始终跟得上项目的真实情况
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

另外还带了十个受控 reference：

- `AGENTS-template.md`
- `CLAUDE-template.md`
- `coding-agent-guide-template.md`
- `implementation-planning-template.md`
- `worker-policy-template.md`
- `execution-recovery-template.md`
- `documentation-governance-template.md`
- `archive-readme-template.md`
- `dependency-setup.md`
- `validation-scenarios.md`

其中 instruction template 更像生成契约，不是复制粘贴小零食。它会告诉 agent 哪些必须留下、哪些必须按项目改写、哪些只是在生成阶段帮忙，到了最终 `AGENTS.md` 或 `CLAUDE.md` 里就该安静退场。

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
| 指令层 | canonical `AGENTS.md` 或 standalone `CLAUDE.md`，可再带一个 thin Claude adapter | 稳定执行规则、验证纪律、协作规则 |
| 路由层 | `coding-agent-guide.md` | 从任务或症状找到首读文件、可能修改面和针对性验证 |
| 规划层 | `implementation-planning.md` | 按需加载的 Superpowers-compatible task sizing、依赖边和 wide-change 结构 |
| 派工与恢复层 | `worker-policy.md`、`execution-recovery.md` | 怎么选帮手、检查成果，以及反复修不好时该怎样停下来判断 |
| 治理层 | `documentation-governance.md` | 文档角色、active/archive surfaces、命名与加载、归档不变量 |
| 活跃工作层 | active `specs/`、active `plans/`，以及按需启用的根目录 `task_plan.md` / `progress.md` / `findings.md` | 只放正在进行的工作 |
| 归档层 | `archive/` 加根级 `archive/README.md` | 已完成的 spec、plan、tracking，以及历史参考材料 |

NHK 在这里是故意有主张的：

- 主指令文件确定后，NHK 会备齐七项基础内容：指路、规划、派工、恢复和文档管理这五份说明，加上 `archive/` 和 `archive/README.md`
- 根目录 tracking 文件是按需启用，不是默认永远存在
- active 文档和 archive 文档不能混着放
- archive 转换必须有人类确认
- 已归档 workstream 应通过根级 `archive/README.md` 保持可检索

对 NHK 面向的新手项目来说，路由表就是新手需要的浅层 code map。再另做一张 codemap，多半只是让第一次进仓库的人同时迷路在两张地图里，未免有点用力过猛。

治理层的直接依据就是 `references/documentation-governance-template.md`。NHK 不认为文档生命周期应该靠默认脑补解决，而是要求这些规则在目标 workspace 里明确写出来。

`implementation-planning.md` 是编写、批准或实质修改计划前才加载的 Superpowers overlay。默认一个 Task 交付一个 Module：责任、前置依赖、接口和完整验收明确的一组相关工作。同一能力的实现、测试、配置、迁移和文档一起交付，保留具体内部步骤与及时验证。只有结果无关、权限不同、跨模块依赖未解决，或范围超出一位实现者与审查者能可靠掌握时才拆分；文件数、提交数、耗时或内部结果可单独测试本身都不够。独立派发的机械工作是明确例外。Superpowers 继续提供 Files、Interfaces、TDD steps、命令、预期结果、必要代码和审查提示；冲突时 NHK 的模块大小、角色路由、复用与等待规则优先。NHK 不修改插件。

`worker-policy.md` 管的是“这活交给谁、要交代清楚什么、谁来检查”。需要安排子代理干活或检查它们的成果时，才读它。`execution-recovery.md` 则在修复开始打转时出场：同一个任务或同一个问题五轮还没解决，或者更早发现设计可能有问题，就先按它的说明重新判断。平时不用把两份文件都摊在桌上。

缺哪份，`nhk-bootstrap` 就按对应的[派工模板](references/worker-policy-template.md)或[恢复模板](references/execution-recovery-template.md)补哪份，已有的项目内容会留下。如果主指令文件里还放着旧版 NHK 的规则，bootstrap 或 upkeep 只把这些过时段落换成指向配套文件的说明。项目事实和你明确批准过的例外也会保留。

更新本机安装的 NHK 后，可以在已有项目里从 `welcome-to-nhk` 开始，要求做一次 upkeep。它会对照当前安装的模板检查 NHK 规则，就算文档看起来还挺整齐，也不能因此跳过。项目事实和你明确批准过的例外会保留；缺少基础文件则先走 bootstrap。更新安装包本身不会顺手改写各个项目的文档。

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

如果缺了其中一个，NHK 不应该装作没事继续跑，而是应该停下来问你：是要安装、启用，还是明确授权只在本次 NHK 运行里手动 adopt 它的工作流约定。Adopt 不等于安装，也不会自动延续到下一次运行，最后应如实说明。对应边界在 [`references/dependency-setup.md`](references/dependency-setup.md)。

## 怎么安装

NHK 本质上是一个文件型 skill bundle，没有什么要编译的东西。

把四个 skill 目录和同级 `references/` 直接放进当前 agent 环境使用的 skills root：

```text
<skills-root>/
├── welcome-to-nhk/
├── nhk-bootstrap/
├── nhk-upkeep/
├── nhk-archive/
└── references/
```

从这个 repo 复制时，等价命令是：

```bash
cp -R welcome-to-nhk nhk-bootstrap nhk-upkeep nhk-archive references <skills-root>/
```

请把 `<skills-root>` 换成当前环境的真实 skills 路径，不要再额外套一层 `nhk/`。

Repo 里的 `scripts/` 和 `tests/` 只供维护者使用，不属于运行时安装内容；Python 也不是 NHK 依赖。这个零第三方依赖的 validator 是可选工具，本机刚好有 Python 3 时可以用它检查文件布局：

```bash
python3 -B scripts/validate_nhk.py --install-root <skills-root>
```

Validator 只能核对文件和版本，不能冒充平台的 skill discovery。复制和验证后仍要刷新 agent 会话，并确认四个 skill 都可发现，再到目标 workspace 里从 `welcome-to-nhk` 开始。

如果你是第一次配这种环境，不确定依赖有没有装好，这非常正常。NHK 的设计本来就是在这种地方先停下来问，而不是装懂。

## 怎么用

最短路径其实很简单：

1. 先从 `welcome-to-nhk` 开始。
2. 让它判断现在应该进入 `nhk-bootstrap`、`nhk-upkeep` 还是 `nhk-archive`。
3. 让 `nhk-bootstrap` 准备主指令文件、五份配套说明，以及存放已完成工作的地方（`archive/` 加 `archive/README.md`）。不用你从空白文档开始写。
4. 正常开发周期走完后，用 `nhk-upkeep` 修正漂移；只有一个具体 workstream 同时具备完成证据和相关材料时，它才会询问是否归档。
5. 只有在用户明确说“这个 workstream 完成了，可以归档”之后，才进入 `nhk-archive`。

如果你完全不知道先点哪个 skill，NHK 的态度是故意有点专断的：先走 `welcome-to-nhk`，让入口路由来当现场最清醒的那个人。

## Codex 和 Claude Code

NHK 同时兼容这两个方向：

- Codex 型 workspace 通常以 `AGENTS.md` 为核心
- Claude Code 型 workspace 可以使用 standalone `CLAUDE.md`，也可以用 thin `CLAUDE.md` 导入 canonical `AGENTS.md`

NHK 不会在这件事上瞎猜。如果两个文件都在，而 CLAUDE 在正文里有一行严格等于 `@AGENTS.md` 或 `@./AGENTS.md` 的真实 import，AGENTS 就是 canonical，不必多问。只有导入行却没有 AGENTS 的 CLAUDE 是 broken adapter；两个互相独立的文件才是真歧义，需要人来选。

thin CLAUDE 只 import AGENTS。五份 companion docs 始终使用反引号普通路径并按需读取；如果用 `@` 把它们展开，每次会话都得先把整套说明背一遍，再看看今天到底用不用得上。

## 怎么挑帮手，什么时候该停一停

NHK 使用三个 Codex 档位，权限按工作角色确定。完整模块默认使用 medium；独立、确定、规格清楚且低风险的机械工作可用较轻档位。选择高档位前，先检查范围、接口和上下文；只有检查后仍有具体推理难点，或已有证据表明 medium 能力不足，才使用高档位，并在派工说明中用一句话指出难点。已知困难任务可以直接从高档位开始。局部修复与限定复审，只有在原因、行为、方案、影响和验证清楚，且无需设计或跨模块判断时，才可用较轻档位。你的预算仍然有效。

精确型号名单与角色权限放在[派工模板](references/worker-policy-template.md)，再生成项目的 `worker-policy.md`。合理的模块边界应让大多数实施适合默认角色，同时避免交付碎片化或把全部设计工作转移给主线程。大量任务需要高档位时应重看计划；真正困难的工作不受比例配额限制。失败后先分类原因，再判断是否升级。型号不可用时明确报告，不静默换档或回退旧型号。在普通能力上限仍无法收敛、出现更早的停滞证据或达到五轮上限时，进入执行恢复。

对于长期运行的 Codex 主线程，建议考虑 GPT-6 Sol，复杂协调可用 xhigh，需要更深推理时再用 max。这只是给使用者的建议：主线程型号和 effort 由你选择，NHK 的 worker 权限不依赖该选择。当前选项可参阅 [OpenAI 模型说明](https://learn.chatgpt.com/docs/models)。

普通修复优先交回原实现者，限定复审优先交回原独立审查者。允许便宜配置不代表必须换人；只有独立完整的修复交接连同总开销都值得，才换新帮手，并把合适的意见合并为一个修复包。

每个模块安排一位独立只读审查者，分别给出需求符合度与实现质量结论，两项都要通过。初审默认使用中间档位；审查本身符合困难条件时才用高档位。复杂计划整体终审使用高档位，需要更深推理时可用 max；除此之外，max 只用于独立诊断。内部步骤不单独派审查者。审查使用固定版本、约束、实际差异与测试证据。只有单模块且非复杂计划，已通过的模块审查覆盖全部需求、改动和证据，而且最终范围与版本完全相同时，才可兼作终审。范围、版本或证据变化后要重新判断；多模块和复杂计划仍做整体终审。合并审查不增加修复或恢复次数。

派发或恢复后，以及两次主动进度检查之间，主线程至少等待 30 分钟；在工具限制和更高优先级指令允许时使用较长的事件等待，同时立即响应完成、提问、具体失败和你的消息。空等待返回或沉默不构成查状态、催促、中断、换人或重复调查的理由。这不是超时、定时轮询、缓存 TTL 或运行时设置。规则更新保留活跃任务编号与进度，不自动重组正在执行的计划或重新派发已完成工作。

已有的人类决定可以在 `worker-policy.md` 中保留为范围明确的普通派工例外。[派工模板](references/worker-policy-template.md)规定一条 JSON 列表记录，写明目标、仓库相对路径范围、角色、普通预设和具体批准依据。Bootstrap/upkeep 必须核对既有决定及其边界，不能编造授权。正常规则和型号目录仍然保留，记录只改变完全匹配范围内的预设选择；不能豁免 worker class、审查要求、预算、特殊角色权限、Ultra 或递归授权。可选验证器只检查记录结构，不证明人类真的同意过；未记录的冲突，以及格式错误或范围笼统的记录仍会失败。规划文档的必需字段保持活跃文本，按模板生成时无需暗中删除代码围栏。

Claude 的帮手明确选用 Sonnet 或 Opus。Fable 留在主线程，而且要由你选择或同意。使用 Ultra，以及让帮手继续找帮手，是两件分别需要授权的事：都要针对当前这次运行里的具体任务，由你明确批准。

普通 bug 继续用 Superpowers 的系统性调试流程。同一个问题熬过了第五轮，NHK 会让主线程先重看自己的判断，再伸手去拿第六个补丁。每项任务最多五轮普通修复与复审；跨任务遇到同一个未解决的问题，次数也接着算，换个任务名不会清零。记录仍写在当前工作流已有的地方。

如果新的因果证据能解释前面为什么没修好，才允许一轮恢复修正和一次复审。解释存在分歧时，最多进行一次全新上下文的只读诊断，按难度使用高档配置或 max。诊断区分观察事实与旧假设，返回证据或能区分解释的实验；修复与复审按各自角色选配置。五轮是上限：三次修复失败后的架构检查和更早的停滞证据仍然有效。证据仍说不清或恢复失败时，接下来由你决定。[恢复模板](references/execution-recovery-template.md)规定证据要求与停止规则。

## 仓库自身的维护

这个仓库本身也带了 `AGENTS.md` 和 `CLAUDE.md`。

这里的分工是：

- `AGENTS.md` 作为 coding agent 的共享仓库维护规范
- `CLAUDE.md` 导入 `AGENTS.md`，只补少量 Claude 专属说明

这样 human-facing 的 README 和 agent-facing 的工作规则就分开了。没那么花哨，但通常也更不容易出事。

如果你是在维护 NHK 本身，还可以用可选的 validator 检查生成后的配套文档：

```bash
python3 -B scripts/validate_nhk.py --final <coding-agent-guide.md> --kind coding-guide
python3 -B scripts/validate_nhk.py --final <implementation-planning.md> --kind planning-guide
python3 -B scripts/validate_nhk.py --final <worker-policy.md> --kind worker-policy
python3 -B scripts/validate_nhk.py --final <execution-recovery.md> --kind execution-recovery
python3 -B scripts/validate_nhk.py --final <documentation-governance.md> --kind doc-governance
```

篇幅测试会用相同的项目事实生成 `AGENTS.md` 和 standalone `CLAUDE.md` 示例，与细则拆到配套文件之前的基线比较。两者每轮加载的英文词数都要至少减少 20%，挪几个换行不算。这是在检查指令有没有真正变短，不是给实际费用打包票；也是维护者的检查，不是安装 NHK 要交的作业。
