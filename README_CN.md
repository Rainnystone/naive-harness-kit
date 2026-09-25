# 欢迎来到 NHK：Naive Harness Kit

[English](README.md) | **中文**

NHK 是一个 prompt-first 的懒人包：帮你把 Codex 或 Claude Code 的 workspace 搭起来、维护好，让你把注意力留给真正的项目。

你不需要先修一门“Agent harness engineering”再开工。NHK 会替你做几个合理的默认决定，把它们写在你和 agent 都看得见的地方，遇到你应该拍板的事就停下来问。它不会魔法，更像那个帮你搬家、还坚持给每个箱子贴标签的朋友：有点碎嘴，但未来的你回头看时，不用对着一堆 agent 的即兴发挥考古。

## 30 秒看懂

用 coding agent 用得认真一点，很快就会反复碰到下面 5 类事，NHK 就是来接手它们的：

- 先把真正有用的工作流工具接进来，尤其是 `superpowers` 和 `planning-with-files`
- 给当前的 agent 初始化合适的指令文件（`AGENTS.md` 或 `CLAUDE.md`），懒一点，但不乱来
- 让指路、规划、派工、恢复和文档管理这几份说明，始终跟得上项目的真实情况
- 判断一个 workstream 该继续保持 active，还是该进入 archive
- 整个过程靠明确的 prompt 驱动，而不是靠看不见的 hooks 偷偷做事

它是给新手、懒人，以及宁愿先把东西做出来、也不想从零手搓 harness 的人准备的。大佬当然也欢迎，这里不查段位。

## 快速开始

**1. 装好 NHK 依赖的两个工具。** 分别是 [`superpowers`](https://github.com/obra/superpowers) 和 [`planning-with-files`](https://github.com/othmanadi/planning-with-files)。不确定装没装？没关系，NHK 会先检查，缺了就停下来问你，不会装作一切就绪。

**2. 把 NHK 复制到 agent 的 skills 目录。** 没有任何要编译的东西。四个 skill 目录和 `references/` 并排放：

```text
<skills-root>/
├── welcome-to-nhk/
├── nhk-bootstrap/
├── nhk-upkeep/
├── nhk-archive/
└── references/
```

在这个 repo 里执行：

```bash
cp -R welcome-to-nhk nhk-bootstrap nhk-upkeep nhk-archive references <skills-root>/
```

把 `<skills-root>` 换成你的 agent 实际使用的 skills 目录（Claude Code 通常是 `~/.claude/skills/`）。这五个目录必须直接并排，外面再套一层 `nhk/`，agent 就找不到它们了。

**3. 刷新 agent 会话**，确认四个 skill 都可发现。

**4. 打开你的项目，从 `welcome-to-nhk` 开始。** 它会看一圈现场，再把你交给下一步该用的 skill。日常用法真的就这么多。

<details>
<summary>可选：用 Python 再核对一次安装</summary>

如果本机刚好有 Python 3，可以用这个零第三方依赖的 validator 检查文件布局：

```bash
python3 -B scripts/validate_nhk.py --install-root <skills-root>
```

它只能核对文件和版本，不能替平台确认 skill 真的被发现了，所以第 3 步的刷新不能省。Repo 里的 `scripts/` 和 `tests/` 是维护者工具，不属于运行时安装内容；Python 也不是 NHK 的依赖。

</details>

## 四个 skill

| Skill | 什么时候出场 | 做什么 |
| --- | --- | --- |
| `welcome-to-nhk` | 永远第一个 | 总入口。检查依赖和指令文件，然后从下面三个里选一个。拿不准的时候就从这里开始，让它当现场最清醒的那个人。 |
| `nhk-bootstrap` | 第一次初始化，或者缺了必需的部分 | 写好主指令文件、五份配套说明，以及存放已完成工作的地方。你负责看，不用从空白文档开始写。 |
| `nhk-upkeep` | 一个开发周期结束后，或者更新 NHK 之后 | 修正文档和当前 NHK 规则之间的漂移。只有某个 workstream 有明确的完成证据时，才会问你要不要归档。 |
| `nhk-archive` | 只在你确认某个 workstream 完成之后 | 把这个完成的 workstream 移进 `archive/`，并保证索引找得到它。 |

更新了本机的 NHK？在已有项目里从 `welcome-to-nhk` 开始，要求做一次 upkeep。就算文档看起来还挺整齐，它也会对照新模板检查一遍；项目事实和你批准过的例外会保留，缺少基础文件则先走 bootstrap。只更新安装包，不会顺手改写各个项目的文档。

## 你的项目里会多出什么

主指令文件确定后，NHK 会备齐七项基础内容：指路、规划、派工、恢复和文档管理这五份说明，加上 `archive/` 和 `archive/README.md`。它们的分工是这样的：

| 层 | 文件 | 作用 |
| --- | --- | --- |
| 指令层 | canonical `AGENTS.md` 或 standalone `CLAUDE.md`，可再带一个 thin Claude adapter | 稳定的执行规则、验证纪律、协作规则 |
| 路由层 | `coding-agent-guide.md` | 从任务或症状出发：先读什么、大概改哪里、怎么验证 |
| 规划层 | `implementation-planning.md` | 任务大小、依赖关系和大范围改动的结构，只在做计划时加载 |
| 派工与恢复层 | `worker-policy.md`、`execution-recovery.md`，以及可选的 Claude `.claude/agents/nhk-*.md` | 怎么选帮手、检查成果，以及反复修不好时该怎样停下来判断 |
| 治理层 | `documentation-governance.md` | 文档角色、active 与已归档材料的区分、命名和加载 |
| 活跃工作层 | active 的 `specs/`、`plans/`，以及按需启用的根目录 `task_plan.md` / `progress.md` / `findings.md` | 只放正在进行的工作 |
| 归档层 | `archive/` 加根级 `archive/README.md` | 已完成的 spec、plan 和 tracking，留作参考 |

有几条主张是故意内置的：

- 根目录 tracking 文件按需出现，不是默认永远存在。
- active 文档和归档文档分开放，归档一定等你确认。
- 对 NHK 面向的新手项目来说，路由表就是新手需要的浅层 code map。再另做一张 codemap，多半只是让第一次进仓库的人同时迷路在两张地图里。
- 文档的生命周期要明确写下来，依据是 `references/documentation-governance-template.md`，不靠脑补。

配套说明平时不占地方：写或改计划时才拿出 `implementation-planning.md`，把活交给帮手时才拿出 `worker-policy.md`，修复开始打转时才拿出 `execution-recovery.md`。大多数时候，它们都不用摊在桌上。

## 为什么这样设计

NHK 的每个选择，都来自对 coding agent 实际表现的几条朴素观察：

- **靠 prompt，不靠 hook。** 每一步都是你读得懂的 prompt，没有东西在背后偷偷运行；出了问题，你能看到是哪条指令导致的。这也让 NHK 在 Codex 和 Claude Code 里表现一致。
- **常驻指令要短，细节按需加载。** agent 会反复读取主指令文件，每读一次都要花 token 和注意力。所以主指令文件只放稳定规则和指路，配套说明等任务真的需要时再加载。
- **写下来，比指望它记得靠谱。** agent 跨会话会忘，有时同一个会话里也会忘，文件不会。这就是 NHK 搭配 `planning-with-files`，并把路由、规划和归档规则写进文档的原因。
- **难以撤回的决定留给你。** 归档、最高档模式、帮手再找帮手，以及任何有歧义的情况，都要等你明确点头。NHK 宁可多问一句，也不替你猜错。
- **帮手的强度跟着任务走。** 每派一个帮手都要花时间和 token，所以默认选够用的那一档，要升档就得说出理由。难度可以换来更强的帮手，习惯不行。
- **反复失败，需要的是新解释。** 修复一直撞在同一堵墙上时，再打一个补丁很少有用。NHK 会给循环设上限，要求先换个角度重新看问题。
- **故意保持新手尺寸。** 对 NHK 面向的项目，一套固定的小型基础文档加一张路由表已经够用。结构再多，主要就是多了要同步维护的东西。

## 为什么是这两个依赖

- `superpowers` 给 agent 的工作一个形状：先 brainstorm、spec、plan，再动手，而不是一路滑向“先随便做点什么再说”，隔二十分钟就重新发明一套方法论。
- `planning-with-files` 给记忆一个落在模型外部的稳定位置。Codex 和 Claude Code 在长期记忆这件事上都偏模糊，几份朴素的 tracking 文件，比指望模型记得哪些验证跑过、哪个 workstream 还 active 可靠得多。

NHK 用这两者，让指令初始化、日常维护和归档判断不再拍脑袋。缺了其中一个，NHK 会停下来问你：安装、启用，还是只在本次运行里手动 adopt 它的约定。Adopt 不会安装任何东西，也不会延续到下一次运行，NHK 会如实说明。具体边界见 [`references/dependency-setup.md`](references/dependency-setup.md)。

## Codex 还是 Claude Code？

两边都能用。共通的规则（审查、等待、恢复，以及需要你批准的事项）完全一样，不同的是各个平台给 NHK 的控制手段：

| | Codex | Claude Code |
| --- | --- | --- |
| 主指令文件 | `AGENTS.md` | standalone `CLAUDE.md`，或 import `AGENTS.md` 的 thin `CLAUDE.md` |
| 配套说明 | 需要时按文件路径读取 | 同左；绝不用 `@` 导入 |
| 帮手型号 | 四个能力档位，每档对应[派工模板](references/worker-policy-template.md)里的一个预设 | 只用 Opus；light 与 standard 共用一份定义，另有 deep 和只读的 audit |
| 帮手的 effort 怎么设 | 派发每个帮手时直接选 | 通过 bootstrap 提议的可选 `.claude/agents/nhk-*.md` 文件；不装就跟随你的会话设置 |
| 需要你明确批准 | Ultra，以及帮手再找帮手 | 主线程使用 Fable，以及帮手再找帮手 |

为什么不一样？两个平台共用同样的四个档位和同样的权限，差别只在映射。Codex 允许主线程在派发每个帮手时同时选型号和 effort，所以每个档位对应一个预设。Claude Code 可以按次选帮手的型号，但 effort 只能写在 agent 定义文件里。所以 NHK 准备了三份现成的定义，只用一个足够强的型号系列，各份之间只调整思考的力度；light 档的活由 standard 定义承担。

**哪个指令文件说了算。** NHK 不会在这件事上瞎猜。如果两个文件都在，而 `CLAUDE.md` 在正文里有一行严格等于 `@AGENTS.md` 或 `@./AGENTS.md` 的真实 import，AGENTS 就是 canonical，不必多问。只有导入行却没有 AGENTS 的 CLAUDE 是 broken adapter；两个互相独立的文件才是真歧义，这时 NHK 会请你来选。

thin CLAUDE 只 import AGENTS。五份 companion docs 始终使用反引号普通路径并按需读取；如果用 `@` 把它们展开，每次会话都得先把整套说明背一遍，再看看今天到底用不用得上。

**主线程用什么型号？** 两个平台各给一条建议：

对于实施阶段的 Codex 主线程，建议使用 GPT-6 Sol xhigh。长期运行的主线程会反复读取自己的上下文，Sol 的 cache read 比更强的 Astra 系列便宜得多。这只是给使用者的建议：主线程型号和 effort 由你选择，NHK 的 worker 权限不依赖该选择。当前选项可参阅 [OpenAI 模型说明](https://learn.chatgpt.com/docs/models)。

对于实施阶段的 Claude Code 主线程，建议使用 Opus high，比默认 effort 高一档，因为协调工作压在主线程上。它和上面一样只是建议，不是规则；无论你怎么选，帮手的档位都不变。当前选项可参阅 [Anthropic effort 说明](https://platform.claude.com/docs/en/build-with-claude/effort)。

## 帮手、审查，以及什么时候该停

不读这一节也能正常使用 NHK。写在这里，是为了让你知道 agent 把活交给帮手时，都在按什么规矩办事。

简单版：

- **帮手按任务匹配。** 日常工作用合理的默认档，明确、低风险的小任务可以轻一点，真正困难的活才用重档，而且要把难点写清楚。
- **派出去的任务有独立检查。** SDD 按原子任务审查；native 保留自己的验证和一次独立终审。需求与质量两个结论都要通过。
- **主线程耐心等待。** 不会每隔几分钟就去催帮手。
- **修复打转就先重新思考。** 同一个问题修到第五轮，下一步是给出更好的解释，而不是第六个补丁。
- **大权限留在你手里。** 最高档模式、帮手再找帮手、归档，都需要你明确同意。

<details>
<summary>细则，给好奇的你</summary>

### 能力档位

**怎么挑帮手。** NHK 把帮手的工作分成四个能力档位，权限按工作角色确定，两个平台共用同一份定义。`standard` 是常规实施、局部设计、集成、排错、独立调查和任务初审的默认档。`light` 可以完整实现并测试明确、低风险的小功能，也可以处理机械工作：行为与接口明确、有既定做法、验证可靠、影响局部可控；计划不必给出完整实现代码。涉及安全、数据完整性或隐蔽的跨任务影响时，即使代码很短也需要更多判断。选择 `deep` 前先检查范围、接口和上下文；只有剩余推理难点或 `standard` 能力不足的证据才支持升级，并在派工说明中写明难点。`deep` 是实施的能力上限。只读的 `audit` 档负责独立诊断和复杂计划的整体终审，从不做实施。架构标签和较后的修复轮次不自动触发升档。局部修复与限定复审只有在原因、行为、方案、影响和验证清楚，且无需设计或跨任务判断时，才可用 `light`。你的预算仍然有效。

[派工模板](references/worker-policy-template.md)定义这些档位、把它们映射到各个平台，并生成项目的 `worker-policy.md`。优化的是正确交付的总成本：规划、上下文交接、实施、审查和返工。原子边界应让明确工作适合 `light`，让剩余判断落在 `standard` 能处理的范围内。大量任务需要 `deep` 时回看计划，不设模型使用比例配额。失败后先分类原因，再判断是否升级；配置不可用时明确报告，不静默换档，也不回退旧型号。在 `deep` 仍无法收敛、出现更早的停滞证据或达到五轮上限时，进入执行恢复。

### 仅 Codex

**各档预设。** 日常的 `standard` 档用 Sol xhigh，只花更强系列一小部分的价格，就能完成大多数切分合理的原子任务。`deep` 换到 Astra medium：比 Sol xhigh 更强，同时仍是实施上限。`audit` 用 Astra xhigh，只做只读工作；max 不再是 worker 预设。`light` 继续用 Luna。精确预设以模板为准。

### 仅 Claude Code

**各档定义。** Claude 的帮手全部使用 Opus。Claude Code 只能通过 agent 定义文件设置帮手的 effort，所以在 Claude Code workspace 里，`nhk-bootstrap` 会按 [agent 定义模板](references/claude-agents-template.md) 提议在 `.claude/agents/` 下添加三个可选文件：`nhk-standard` 使用 Opus 的默认 effort，同时承担 `light` 和 `standard`；`nhk-deep` 想得更深；只读的 `nhk-audit` 想得最深。之所以没有单独的 light 定义，是因为默认 effort 的 Opus 做小活已经足够经济；以后可以换一个更轻的型号系列来占这个位置，而不用改任何档位规则。我们建议接受；如果拒绝，帮手仍然使用 Opus，effort 跟随你的会话设置。新建的 `.claude/agents/` 目录要开一个新会话，Claude Code 才能发现。Fable 留在主线程，而且要由你选择或同意。

### 两个平台通用

**特殊授权。** 在提供 Ultra 的平台上，使用 Ultra 和让帮手继续找帮手是两件分别需要授权的事：都要针对当前这次运行里的具体任务，由你明确批准。

**帮手复用。** 普通修复优先交回原实现者，限定复审优先交回原独立审查者。允许用便宜配置不代表必须换人；只有独立完整的修复交接连同总开销都划算时，才换新帮手，并把合适的意见合并成一个修复包。

**审查。** SDD 为每个原子任务或符合条件的机械批次安排一位独立只读审查者，分别给出需求符合度与实现质量结论，两项都要通过。初审默认使用 `standard`，只有审查本身确实困难才用 `deep`。整体终审使用 `deep`，复杂计划的整体终审使用 `audit`。内部步骤不单独派审查者。审查依据固定版本、约束、实际 diff 与测试证据。只有单任务、非复杂计划，已通过的 SDD 任务审查在相同最终范围、版本和证据上覆盖全部要求与改动时，才能兼作终审；任何变化都要重新判断。多任务和复杂计划保留整体终审。Native 执行保留自己的逐任务验证和一次独立整体终审，不增加逐任务子代理审查。合并审查不增加修复或恢复次数。

**等待。** 派发或恢复后，以及两次主动进度检查之间，主线程至少等待 30 分钟；在工具限制和更高优先级指令允许时使用较长的事件等待，同时立即响应完成、提问、具体失败和你的消息。空等待返回或沉默，都不构成查状态、催促、中断、换人或重复调查的理由。这不是超时、定时轮询、缓存 TTL 或运行时设置。规则更新保留已完成和执行中任务的身份与进度；尚未开始的工作按原子任务契约重新评估，不重派已完成工作，也不重置恢复计数。

**你已经做过的决定。** 已有的人类决定可以在 `worker-policy.md` 中保留为范围明确的普通派工例外。[派工模板](references/worker-policy-template.md)规定用一条 JSON 列表记录，写明目标、仓库相对路径范围、角色、一个 `light`、`standard` 或 `deep` 预设，以及具体批准依据。Bootstrap 和 upkeep 必须核对这个决定及其边界，不能编造授权。正常规则和型号目录仍然保留，记录只改变完全匹配范围内的预设选择；它不能豁免 worker class、审查要求、预算、`audit` 档、Ultra 或递归授权。可选的 validator 只检查记录结构，不证明你真的同意过；未记录的冲突，以及格式错误或范围笼统的记录仍会失败。

**规划。** `implementation-planning.md` 是编写、批准或实质修改计划前才加载的 Superpowers overlay。两平台统一使用原子任务：能够独立测试、值得独立审查的最小交付。如果审查者可以接受一个结果、拒绝相邻结果，就可以拆开，即使它们属于同一功能。每项任务保留完整的实现、测试和必要的配置、迁移、文档；任务可以跨文件，功能可以跨任务。紧密耦合的事务、权限判断和恢复路径保持完整。内部执行步骤留在任务中；同形机械修改可按明确文件清单与共用验证组成一个批次。调查只有能交付可验证结论、接口契约或可复用决策时才单独拆出，普通的局部理解留给实施者。

计划保留 Files、Interfaces、具体 TDD steps、边界样例、命令、预期结果和必要代码范例；局部实现交给 worker，不要求主线程先写完整实现代码。Worker class 描述工作性质，不等于模型档位。SDD 每个任务或合格批次使用新的实施上下文，并保持实施串行；native 是独立的执行选择。沿用上游 brief、report、diff package 和 ledger 文件；即使提取工具只取得任务段落，交接也必须带上绑定的全局约束和相关接口。NHK 的原子粒度、规划详细度、角色路由、复用与等待规则覆盖冲突的上游默认，但不修改插件。规划字段保留为活跃文本。

**更新旧项目。** Upkeep 将 NHK 自有的完整模块默认规则改为原子任务契约，保留项目事实和已批准例外。旧 `module-implementation` / `initial-module-review` 记录只有仍指向同一个任务、相同范围和已确认批准依据时，才改为 `task-implementation` / `initial-task-review`。旧模块拆成多个任务或对应关系不明确时，报告给人决定，不把授权自动复制到新任务。旧版本按 Band 划分的路由改为档位规则；例外记录只有在其预设仍是该角色允许的 `light`、`standard` 或 `deep` 预设时才保留，其余情况等你决定。在 Claude Code 中，upkeep 会在已退役的 `nhk-diagnosis` 旁补上 `nhk-audit`，并请你删除退役的 `nhk-light` 和 `nhk-diagnosis` 文件，因为 upkeep 自己从不删除文件。仅更新安装包不会自动改写项目文件。

**修复开始打转时。** 普通 bug 继续用 Superpowers 的系统性调试流程。同一个问题熬过了第五轮，NHK 会让主线程先重看自己的判断，再伸手去拿第六个补丁。每项任务最多五轮普通修复与复审；跨任务遇到同一个未解决的问题，次数也接着算，换个任务名不会清零。次数记在当前工作流已有的记录里。

如果新的因果证据能解释前面为什么没修好，才允许一轮恢复修正和一次复审。解释存在分歧时，最多进行一次全新上下文的只读诊断，使用 `audit` 档；诊断会区分观察事实与旧假设，返回证据或能区分几种解释的实验。修复与复审按各自角色选配置。五轮是上限：三次修复失败后的架构检查，以及更早出现的停滞迹象，仍然有效。证据还是说不清，或者恢复失败时，接下来由你决定。[恢复模板](references/execution-recovery-template.md)规定了证据要求与停止规则。

**配套说明缺失或过时。** 缺哪份配套说明，`nhk-bootstrap` 就按对应模板补哪份，已有的项目内容会留下。如果主指令文件里还放着旧版 NHK 的规则，bootstrap 或 upkeep 只把这些过时段落换成指向配套说明的链接。项目事实和你明确批准过的例外都会保留。

</details>

## 这个 repo 里有什么

四个 skill，各占一个目录：`welcome-to-nhk`、`nhk-bootstrap`、`nhk-upkeep` 和 `nhk-archive`。

另外还带了十一个受控 reference，skill 需要时才会读取：

- `AGENTS-template.md` 和 `CLAUDE-template.md`：怎么生成主指令文件
- `coding-agent-guide-template.md`、`implementation-planning-template.md`、`worker-policy-template.md`、`execution-recovery-template.md`、`documentation-governance-template.md`：五份配套说明
- `archive-readme-template.md`：归档索引
- `claude-agents-template.md`：可选的 Claude Code 帮手定义
- `dependency-setup.md`：缺依赖时怎么办
- `validation-scenarios.md`：NHK 用来自检的场景

其中 instruction template 更像生成契约，不是复制粘贴小零食。它会告诉 agent 哪些必须留下、哪些必须按项目改写、哪些只在生成阶段帮忙，到了最终的 `AGENTS.md` 或 `CLAUDE.md` 里就该安静退场。

写给人看的文档和写给 agent 看的文档是刻意分开的。`README.md` 和 `README_CN.md` 写给人看；`AGENTS.md` 写给维护这个仓库的 coding agent，`CLAUDE.md` 为 Claude Code 导入它。四个 skill 目录定义 NHK 的实际行为，`references/` 放它们用到的冻结模板和验证材料。

## 维护 NHK 本身

这一节写给修改 NHK 的人，不是写给使用 NHK 的人。仓库自带 `AGENTS.md`（共享的维护规范）和一个 thin `CLAUDE.md`，后者导入前者，只补少量 Claude 专属说明。这样工作规则就不会混进 README。没那么花哨，但通常也更不容易出事。

可选的 validator 也能检查生成后的配套文档：

```bash
python3 -B scripts/validate_nhk.py --final <coding-agent-guide.md> --kind coding-guide
python3 -B scripts/validate_nhk.py --final <implementation-planning.md> --kind planning-guide
python3 -B scripts/validate_nhk.py --final <worker-policy.md> --kind worker-policy
python3 -B scripts/validate_nhk.py --final <execution-recovery.md> --kind execution-recovery
python3 -B scripts/validate_nhk.py --final <documentation-governance.md> --kind doc-governance
```

篇幅测试会用相同的项目事实生成 `AGENTS.md` 和 standalone `CLAUDE.md` 示例，与细则拆到配套文件之前的基线比较。两者每轮加载的英文词数都要至少减少 20%，挪几个换行不算。这是在检查指令有没有真正变短，不是给实际费用打包票；也是维护者的检查，不是安装 NHK 要交的作业。
