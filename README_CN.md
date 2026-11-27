# 欢迎来到 NHK：Naive Harness Kit

[English](README.md) | **中文**

NHK 是一个 prompt-first 的懒人包：帮你把 Codex 或 Claude Code 的 workspace 搭起来、维护好，让你把注意力留给真正的项目。

你不需要先修一门“Agent harness engineering”再开工。NHK 会替你做几个合理的默认决定，把它们写在你和 agent 都看得见的地方，遇到你应该拍板的事就停下来问。它不会魔法，更像那个帮你搬家、还坚持给每个箱子贴标签的朋友：有点碎嘴，但未来的你回头看时，不用对着一堆 agent 的即兴发挥考古。

## 30 秒看懂

用 coding agent 用得认真一点，很快就会反复碰到下面 5 类事，NHK 就是来接手它们的：

- 识别项目采用的工作流，接上它的工单或计划
- 给当前的 agent 初始化合适的指令文件（`AGENTS.md` 或 `CLAUDE.md`），懒一点，但不乱来
- 让指路、规划、派工、恢复和文档管理这几份说明，始终跟得上项目的真实情况
- 判断一个 workstream 该继续保持 active，还是该进入 archive
- 整个过程靠明确的 prompt 驱动，而不是靠看不见的 hooks 偷偷做事

它是给新手、懒人，以及宁愿先把东西做出来、也不想从零手搓 harness 的人准备的。大佬当然也欢迎，这里不查段位。

## 快速开始

**1. 选择这个项目用的工作流。** 新项目推荐 [Matt Pocock Skills](https://github.com/mattpocock/skills)，也完整支持 [Superpowers](https://github.com/obra/superpowers)。已有的 Superpowers 项目升级时继续沿用原流程。NHK 按项目实际需要检查相应能力。

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
| `welcome-to-nhk` | 总入口 | 识别主指令、工作流和当前操作所需的能力，再选择下一步。 |
| `nhk-bootstrap` | 初次设置或缺少必需文件 | 接好主指令、五份配套说明和所选工作流的记录。 |
| `nhk-upkeep` | 一个开发周期结束后，或者更新 NHK 之后 | 修正文档和当前 NHK 规则之间的漂移。只有某个 workstream 有明确的完成证据时，才会问你要不要归档。 |
| `nhk-archive` | 你明确同意归档一项已完成的工作 | 索引仍由原处管理的记录，需要移动的本地材料先复制再核验。 |

更新了本机的 NHK？在已有项目里从 `welcome-to-nhk` 开始，要求做一次 upkeep。就算文档看起来还挺整齐，它也会对照新模板检查一遍；项目事实和你批准过的例外会保留，缺少基础文件则先走 bootstrap。只更新安装包，不会顺手改写各个项目的文档。

## 你的项目里会多出什么

确定主指令后，NHK 接好五份配套说明。Superpowers 项目在初始化时建立 `archive/` 及索引；Matt 项目在第一次确认归档时建立。Matt 的工单和领域文档约定由 `docs/agents/` 管理。

| 层 | 文件 | 作用 |
| --- | --- | --- |
| 指令层 | canonical `AGENTS.md` 或 standalone `CLAUDE.md`，可再带一个 thin Claude adapter | 稳定的执行规则、验证纪律、协作规则 |
| 路由层 | `coding-agent-guide.md` | 从任务或症状出发：先读什么、大概改哪里、怎么验证 |
| 规划层 | `implementation-planning.md` | 任务大小、依赖关系和大范围改动的结构，只在做计划时加载 |
| 派工与恢复层 | `worker-policy.md`、`execution-recovery.md`，以及可选的 Claude `.claude/agents/nhk-*.md` | 怎么选帮手、检查成果，以及反复修不好时该怎样停下来判断 |
| 治理层 | `documentation-governance.md` | 文档角色、active 与已归档材料的区分、命名和加载 |
| 正在进行的工作 | Matt 在选定的 tracker 里保存 spec 和工单；Superpowers 使用 spec、plan 和执行记录 | 验收、依赖、证据和剩余工作 |
| 归档 | `archive/README.md` | 指向已核验的本地材料或原始工单 |

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
- **从工作记录接续。** 下一次会话直接读工单或执行记录里的进度与验证结果。需要额外跟踪、现有记录又不足时，才启用 `planning-with-files`。
- **批准实施后，主线程持续推进。** 范围内可逆的工程选择由它决定，失败由它排查，必要检查由它收尾。剩余动作需要新权限、改变目标，或已用尽恢复机会且没有可行路径时，才需要你决定。归档、递归派工和 Claude 主线程使用 Fable 仍按各自的授权规则处理。
- **帮手的强度跟着任务走。** 每派一个帮手都要花时间和 token，所以默认选够用的那一档，要升档就得说出理由。难度可以换来更强的帮手，习惯不行。
- **反复失败，需要的是新解释。** 修复一直撞在同一堵墙上时，再打一个补丁很少有用。NHK 会给循环设上限，要求先换个角度重新看问题。
- **故意保持新手尺寸。** 对 NHK 面向的项目，一套固定的小型基础文档加一张路由表已经够用。结构再多，主要就是多了要同步维护的东西。

## 两套工作流怎样选、怎样搭配

- **Matt。** 缺少工单或领域配置时使用 Matt 的项目 setup。主指令中的 `## Agent skills` 导航指向 `docs/agents/issue-tracker.md`、`docs/agents/domain.md`；配置了 triage 才加入 `docs/agents/triage-labels.md`。双入口项目把这节放在 `AGENTS.md`，薄 `CLAUDE.md` 只负责导入。本地 tracker 使用 `.scratch/<feature>/spec.md` 和 `issues/` 下每票一份文件；远程 tracker 保留原编号、讨论和依赖。
- **Superpowers。** 这项工作的需求、计划和进度由它的 spec、plan 和执行记录管理。项目也可以用 Matt 的 `GLOSSARY.md`、`GLOSSARY-MAP.md` 和架构决策记录（ADR）。这些知识按需建立，功能完成后仍留在项目里。旧项目中的 `CONTEXT.md` 先核实内容，再决定是否按旧版词表迁移。

把默认选择记在 `documentation-governance.md` 的 `Workflow: Matt` 或 `Workflow: Superpowers` 一行。每项工作有一个负责的流程、一处权威进度。更换默认值用于新工作，进行中的工作仍从原记录接续。缺少当前操作必需的能力时，可以安装、启用，或明确选择只在这次手动遵循其约定。[依赖设置](references/dependency-setup.md) · [可选的 planning-with-files](https://github.com/othmanadi/planning-with-files)

## Codex 还是 Claude Code？

两边都能用。共通的规则（审查、等待、恢复，以及需要你批准的事项）完全一样，不同的是各个平台给 NHK 的控制手段：

| | Codex | Claude Code |
| --- | --- | --- |
| 主指令文件 | `AGENTS.md` | standalone `CLAUDE.md`，或 import `AGENTS.md` 的 thin `CLAUDE.md` |
| 配套说明 | 需要时按文件路径读取 | 同左；绝不用 `@` 导入 |
| 帮手型号 | 四个能力档位，每档对应[派工模板](references/worker-policy-template.md)里的一个预设 | 每个档位一份定义：light 用 Haiku，standard、deep 和只读的 audit 用 Opus |
| 帮手的 effort 怎么设 | 派发每个帮手时直接选 | 通过 bootstrap 提议的可选 `.claude/agents/nhk-*.md` 文件；不装就跟随你的会话设置 |
| 需要你明确批准 | 帮手再找帮手 | 主线程使用 Fable，以及帮手再找帮手 |

为什么不一样？两个平台共用同样的四个档位和同样的权限，差别只在映射。Codex 允许主线程在派发每个帮手时同时选型号和 effort，所以每个档位对应一个预设。Claude Code 可以按次选帮手的型号，但 effort 只能写在 agent 定义文件里。所以 NHK 准备了四份现成的定义，每个档位一份：light 档的活交给小而便宜的 Haiku 系列，并用它的最高 effort；其余三份使用 Opus，各份之间只调整思考的力度。

**哪个指令文件说了算。** NHK 不会在这件事上瞎猜。如果两个文件都在，而 `CLAUDE.md` 在正文里有一行严格等于 `@AGENTS.md` 或 `@./AGENTS.md` 的真实 import，AGENTS 就是 canonical，不必多问。只有导入行却没有 AGENTS 的 CLAUDE 是 broken adapter；两个互相独立的文件才是真歧义，这时 NHK 会请你来选。

thin CLAUDE 只 import AGENTS。五份 companion docs 始终使用反引号普通路径并按需读取；如果用 `@` 把它们展开，每次会话都得先把整套说明背一遍，再看看今天到底用不用得上。

**主线程用什么型号？** 两个平台各给一条建议：

对于实施阶段的 Codex 主线程，建议使用 GPT-6.2 Astra xhigh，负责跨任务取舍、集成和交付。这只是给使用者的建议，主线程型号和 effort 由你选择，NHK 的 worker 权限不依赖该选择。[OpenAI 模型说明](https://learn.chatgpt.com/docs/models)

对于实施阶段的 Claude Code 主线程，建议使用 Opus high，比默认 effort 高一档，因为协调工作压在主线程上。它和上面一样只是建议，不是规则；无论你怎么选，帮手的档位都不变。当前选项可参阅 [Anthropic effort 说明](https://platform.claude.com/docs/en/build-with-claude/effort)。

## 帮手、审查，以及什么时候该停

不读这一节也能正常使用 NHK。写在这里，是为了让你知道 agent 把活交给帮手时，都在按什么规矩办事。

简单版：

- **帮手按任务匹配。** 日常工作用合理的默认档，明确、低风险的小任务可以轻一点，真正困难的活才用重档，而且要把难点写清楚。
- **审查跟随实施流程。** Superpowers SDD 逐项审查，native 执行保留独立终审。Matt 对集成结果做项目规范和原始需求两方面的审查。
- **主线程耐心等待。** 不会每隔几分钟就去催帮手。
- **修复打转就先重新思考。** 同一个问题修到第五轮，下一步是给出更好的解释，而不是第六个补丁。
- **重要权限由你掌握。** 归档、递归派工和 Claude 主线程使用 Fable 需要明确批准。实施期间，一次只读独立咨询已有授权。

<details>
<summary>细则，给好奇的你</summary>

### 能力档位

**怎么挑帮手。** NHK 把帮手的工作分成四个能力档位，权限按工作角色确定，两个平台共用同一份定义。`standard` 是常规实施、局部设计、集成、排错、独立调查和任务初审的默认档。`light` 可以完整实现并测试明确、低风险的小功能，也可以处理机械工作：行为与接口明确、有既定做法、验证可靠、影响局部可控；计划不必给出完整实现代码。涉及安全、数据完整性或隐蔽的跨任务影响时，即使代码很短也需要更多判断。选择 `deep` 前先检查范围、接口和上下文；只有剩余推理难点或 `standard` 能力不足的证据才支持升级，并在派工说明中写明难点。`deep` 是实施的能力上限。只读的 `audit` 档负责独立诊断和复杂计划的整体终审，从不做实施。架构标签和较后的修复轮次不自动触发升档。局部修复与限定复审只有在原因、行为、方案、影响和验证清楚，且无需设计或跨任务判断时，才可用 `light`。你的预算仍然有效。

[派工模板](references/worker-policy-template.md)定义这些档位、把它们映射到各个平台，并生成项目的 `worker-policy.md`。优化的是正确交付的总成本：规划、上下文交接、实施、审查和返工。原子边界应让明确工作适合 `light`，让剩余判断落在 `standard` 能处理的范围内。大量任务需要 `deep` 时回看计划，不设模型使用比例配额。失败后先分类原因，再判断是否升级；配置不可用时明确报告，不静默换档，也不回退旧型号。在 `deep` 仍无法收敛、出现更早的停滞证据或达到五轮上限时，进入执行恢复。

### 仅 Codex

**各档预设。** `light` 使用 Terra xhigh。`standard`、`deep` 和只读 `audit` 使用 Sol xhigh。影响实现的重要问题经过调查仍拿不准时，主线程可另请一名 Astra xhigh 在全新上下文里给出独立意见。这位咨询者只读，不承担实施、审查和派工。[派工模板](references/worker-policy-template.md)列有精确型号。

### 仅 Claude Code

**各档定义。** Claude 的 light 帮手使用 Haiku，其余帮手全部使用 Opus。Claude Code 只能通过 agent 定义文件设置帮手的 effort，所以在 Claude Code workspace 里，`nhk-bootstrap` 会按 [agent 定义模板](references/claude-agents-template.md) 提议在 `.claude/agents/` 下添加四个可选文件：`nhk-light` 以 max effort 运行 Haiku 5.5，承担 `light`；`nhk-standard` 以默认的 medium effort 运行 Opus，承担 `standard`；`nhk-deep` 想得更深；只读的 `nhk-audit` 想得最深。Haiku 5.5 的定价远低于 Opus，即使开到最高 effort，用它做 `light` 允许的小而清晰的活也很经济；档位规则本身不变。我们建议接受；如果拒绝，所有帮手都使用 Opus，effort 跟随你的会话设置。新建的 `.claude/agents/` 目录要开一个新会话，Claude Code 才能发现。Fable 留在主线程，而且要由你选择或同意。恢复阶段的诊断会交给一个可以续跑的帮手，而不是一次性的内置探索 agent，这样唯一允许的那次追问才能回到同一个帮手；如果那个帮手已经无法续跑，这次追问就作废，不会转交给新的帮手。

### 两个平台通用

**特殊授权。** 递归派工要针对本次运行的具体任务另行批准。Astra 咨询与恢复诊断共用同一次机会，按任务和持续存在的同一验收缺口记账。它不会增加修复次数，也不能用作后备型号或替代终审。

**帮手复用。** 普通修复优先交回原实现者，限定复审优先交回原独立审查者。允许用便宜配置不代表必须换人；只有独立完整的修复交接连同总开销都划算时，才换新帮手，并把合适的意见合并成一个修复包。

**审查。** SDD 为每个原子任务或符合条件的机械批次安排一位独立只读审查者，分别给出需求符合度与实现质量结论，两项都要通过。初审默认使用 `standard`，只有审查本身确实困难才用 `deep`。整体终审使用 `deep`，复杂计划的整体终审使用 `audit`。内部步骤不单独派审查者。审查依据固定版本、约束、实际 diff 与测试证据。只有单任务、非复杂计划，已通过的 SDD 任务审查在相同最终范围、版本和证据上覆盖全部要求与改动时，才能兼作终审；任何变化都要重新判断。多任务和复杂计划保留整体终审。Native 执行保留自己的逐任务验证和一次独立整体终审，不增加逐任务子代理审查。合并审查不增加修复或恢复次数。

**等待。** Superpowers SDD 的帮手派出或恢复后，以及两次主动进度检查之间，至少留 30 分钟。收到完成、提问、具体失败或你的消息时立即处理。恢复执行时沿用任务身份、证据与修复次数。

**你已经做过的决定。** 已有的人类决定可以在 `worker-policy.md` 中保留为范围明确的普通派工例外。[派工模板](references/worker-policy-template.md)规定用一条 JSON 列表记录，写明目标、仓库相对路径范围、角色、一个 `light`、`standard` 或 `deep` 预设，以及具体批准依据。Bootstrap 和 upkeep 必须核对这个决定及其边界，不能编造授权。正常规则和型号目录仍然保留，记录只改变完全匹配范围内的预设选择；它不能豁免 worker class、审查要求、预算、`audit` 档或递归授权。可选的 validator 只检查记录结构，不证明你真的同意过；未记录的冲突，以及格式错误或范围笼统的记录仍会失败。

**规划。** `implementation-planning.md` 跟随当前工作的归属。Superpowers overlay 把计划拆成能够独立测试、值得独立审查的最小交付。Matt 在 tracker 里记录可独立验证的纵向切片、验收和依赖；`implement-spec` 可在隔离工作树中并行处理已就绪的独立工单，集成后对照项目规范和原始需求审查。更换项目默认值后，进行中的计划仍沿用原流程。

Superpowers 计划保留 Files、Interfaces、具体 TDD steps、边界样例、命令、预期结果和必要代码范例；局部实现交给 worker，不要求主线程先写完整实现代码。Worker class 描述工作性质，不等于模型档位。SDD 每个任务或合格批次使用新的实施上下文，并保持实施串行；native 是独立的执行选择。沿用上游 brief、report、diff package 和 ledger 文件；即使提取工具只取得任务段落，交接也必须带上绑定的全局约束和相关接口。NHK 的原子粒度、规划详细度、角色路由、复用与等待规则覆盖冲突的上游默认，但不修改插件。规划字段保留为活跃文本。

**更新旧项目。** Upkeep 将 NHK 自有的完整模块默认规则改为原子任务契约，保留项目事实和已批准例外。旧 `module-implementation` / `initial-module-review` 记录只有仍指向同一个任务、相同范围和已确认批准依据时，才改为 `task-implementation` / `initial-task-review`。旧模块拆成多个任务或对应关系不明确时，报告给人决定，不把授权自动复制到新任务。旧版本按 Band 划分的路由改为档位规则；例外记录只有在其预设仍是该角色允许的 `light`、`standard` 或 `deep` 预设时才保留，其余情况等你决定。在 Claude Code 中，upkeep 会把旧的 `nhk-light` 定义改为 Haiku，补上缺失的当前定义（例如在已退役的 `nhk-diagnosis` 旁补上 `nhk-audit`），并请你删除退役的 `nhk-diagnosis` 文件，因为 upkeep 自己从不删除文件。仅更新安装包不会自动改写项目文件。

**修复开始打转时。** 按所选工作流排错。每项任务最多五轮普通修复与复审；跨任务遇到同一个未解决的问题，仍累计计算。把尝试与结果记在原工单或执行记录。达到上限时重新诊断原因，同时推进不受影响的工作。

两套工作流遇到影响实现而尚无定论的问题时，都可在全新上下文中做一次只读咨询。Codex 使用专门的 Astra xhigh 咨询配置，Claude 使用已有的可续跑诊断角色。向它提供验收条件、事实、反证和具体问题。前期已用过的咨询，进入恢复后仍算同一次额度。

咨询者核查原始证据，形成自己的解释，再与主线程的判断比较。它可以支持或推翻原判断，返回能解释历史失败的证据，或能区分不同解释的实验及预期结果。报告后，可以向同一咨询者进行一次定点追问，仅澄清原问题的证据、遗漏或分歧；追问计入同一次诊断，不扩展调查范围。诊断和追问的使用情况同时归属于任务和同一个持续验收问题，记入已有执行记录；换人、换会话、换模型、换提交、改任务名或重排计划都不清零。

主线程核查证据，自行决定并继续实施。如果新证据解释了前几次失败，可以进行一轮恢复修正和一次复审。Superpowers 保留三次修复失败后的架构检查。只有剩余动作需要新授权、改变验收，或恢复已用尽且没有可行路径时，才由你决定。[恢复模板](references/execution-recovery-template.md)

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
