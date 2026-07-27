# 欢迎来到 NHK：Naive Harness Kit

[English](README.md) | **中文**

NHK 是一个面向 Codex 和 Claude Code 的 prompt-first 懒人包，专门给那些不想先修 "Agent harness engineering" 再开工的人。

它的气质是：稍微自嘲一点，稍微谦卑一点，但尽量务实。目标不是显得很厉害，而是先把好用的工具安上、把它们合理串起来，然后尽量少折腾、少拍脑袋，把一个 agent workspace 的指令系统搭起来、维持住、别养歪。

## NHK 是什么

NHK 主要解决下面 5 类很快就会反复出现的问题：

- 先把真正有用的工作流工具接进来，尤其是 `superpowers` 和 `planning-with-files`
- 在当前环境里懒一点但别乱来地初始化 `AGENTS.md` 还是 `CLAUDE.md`
- 怎么让路由、implementation planning 和 documentation governance 三份 companion 始终和真实状态一致
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

另外还带了八个受控 reference：

- `AGENTS-template.md`
- `CLAUDE-template.md`
- `coding-agent-guide-template.md`
- `implementation-planning-template.md`
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
| 治理层 | `documentation-governance.md` | 文档角色、active/archive surfaces、命名与加载、归档不变量 |
| 活跃工作层 | active `specs/`、active `plans/`，以及按需启用的根目录 `task_plan.md` / `progress.md` / `findings.md` | 只放正在进行的工作 |
| 归档层 | `archive/` 加根级 `archive/README.md` | 已完成的 spec、plan、tracking，以及历史参考材料 |

NHK 在这里是故意有主张的：

- canonical instruction 确定后，每个 NHK-managed workspace 都有五个强制 foundation surface：路由、implementation planning、governance、`archive/` 和 `archive/README.md`
- 根目录 tracking 文件是按需启用，不是默认永远存在
- active 文档和 archive 文档不能混着放
- archive 转换必须有人类确认
- 已归档 workstream 应通过根级 `archive/README.md` 保持可检索

对 NHK 面向的新手项目来说，路由表就是新手需要的浅层 code map。再另做一张 codemap，多半只是让第一次进仓库的人同时迷路在两张地图里，未免有点用力过猛。

治理层的直接依据就是 `references/documentation-governance-template.md`。NHK 不认为文档生命周期应该靠默认脑补解决，而是要求这些规则在目标 workspace 里明确写出来。

`implementation-planning.md` 的职责刻意更窄：它只是 Superpowers overlay，不是来抢班夺权的第二套 planner。只有在编写、批准或实质修改 implementation plan 前才加载；普通编码、review 和 debug 不用读。它保留 Superpowers 要求的精确文件、接口、TDD steps、命令、预期结果与必要代码，只增加 `Delivers`、`Blocked by` 和 `Worker class`，把每个 task 收到一个 fresh implementer context 和一个 reviewer gate 能稳妥接住的大小。NHK 只通过 workspace 文档做这层改良，不去 patch Superpowers 插件。

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

维护者也可以检查生成后的 companion docs，但这不会把 validator 变成运行时依赖：

```bash
python3 -B scripts/validate_nhk.py --final <coding-agent-guide.md> --kind coding-guide
python3 -B scripts/validate_nhk.py --final <implementation-planning.md> --kind planning-guide
python3 -B scripts/validate_nhk.py --final <documentation-governance.md> --kind doc-governance
```

如果你是第一次配这种环境，不确定依赖有没有装好，这非常正常。NHK 的设计本来就是在这种地方先停下来问，而不是装懂。

## 怎么用

最短路径其实很简单：

1. 先从 `welcome-to-nhk` 开始。
2. 让它判断现在应该进入 `nhk-bootstrap`、`nhk-upkeep` 还是 `nhk-archive`。
3. 用 `nhk-bootstrap` 去建立或适配主 instruction file、三个强制 companion docs，以及根级 archive surface（`archive/` 加 `archive/README.md`）。
4. 正常开发周期走完后，用 `nhk-upkeep` 修正漂移；只有一个具体 workstream 同时具备完成证据和相关材料时，它才会询问是否归档。
5. 只有在用户明确说“这个 workstream 完成了，可以归档”之后，才进入 `nhk-archive`。

如果你完全不知道先点哪个 skill，NHK 的态度是故意有点专断的：先走 `welcome-to-nhk`，让入口路由来当现场最清醒的那个人。

## Codex 和 Claude Code

NHK 同时兼容这两个方向：

- Codex 型 workspace 通常以 `AGENTS.md` 为核心
- Claude Code 型 workspace 可以使用 standalone `CLAUDE.md`，也可以用 thin `CLAUDE.md` 导入 canonical `AGENTS.md`

NHK 不会在这件事上瞎猜。如果两个文件都在，而 CLAUDE 在正文里有一行严格等于 `@AGENTS.md` 或 `@./AGENTS.md` 的真实 import，AGENTS 就是 canonical，不必多问。只有导入行却没有 AGENTS 的 CLAUDE 是 broken adapter；两个互相独立的文件才是真歧义，需要人来选。

thin CLAUDE 只 import AGENTS。三份 companion docs 始终使用反引号普通路径并按需读取；如果用 `@` 把它们展开，每次会话都得先把整套说明背一遍，再看看今天到底用不用得上。

## Worker 成本规则

如果所有 worker 都默认继承主线程顶配，最后很容易出现一种微妙局面：模型认真思考了半天，完成了一项本来只需要靠谱打字的工作。于是 NHK 改成三个实践型 Codex preset 档；它们是按 task fit 选择的候选集合，不是什么宇宙通用排行榜，同档内部也没有固定强弱顺序：

`Band 1: GPT-5.5 xhigh; GPT-5.6 Luna max; GPT-5.6 Terra high`
`Band 2: GPT-5.6 Terra xhigh; GPT-5.6 Terra max; GPT-5.6 Sol high`
`Band 3: GPT-5.6 Sol xhigh; GPT-5.6 Sol max`

机械任务、规格清楚的普通实现和 scoped review 使用 Band 1；多文件集成和困难但边界明确的任务使用 Band 2；架构判断、高不确定但仍有边界的任务和 final review 使用 Band 3，或者留在主线程。主线程先选档，再显式写出 model 和 effort，并在档内按 task fit 与预计总成本选择，而不是默认拿最高 effort。某个 preset 不可用时先在同档换选；只有 packet 已经正确拆小、但能力仍不足时才升一档。packet 太大仍然先拆。主线程 model 和 effort 继续作为每个 worker 的成本上限。Sol max 只要没越过这个上限就不用额外批准；越级则先问人。

Ultra 不在这三个档里。只有用户针对当前运行里的一个具体 packet 明确批准，并同时授权该 packet 内的递归派遣时，才可以下传。Claude standalone 沿用“满足任务的最低成本配置、越级先批准”的规则，但不随身背一张 OpenAI 型号表——毕竟它也不是来参观模型博物馆的。

## 修补开始原地打转时

大多数 gap 应该能在五轮认真的 fix–verify 或 fix–review 里收敛。如果同一个 gap 到第五轮还稳稳坐在那里，NHK 就不再假装“第六次说不定会灵光一现”：必须停手并调用或重启 `systematic-debugging`，把前五轮算作失败修复；根因和架构重新审视完成之前，不准再贴第六块补丁。

## 仓库自身的维护

这个仓库本身也带了 `AGENTS.md` 和 `CLAUDE.md`。

这里的分工是：

- `AGENTS.md` 作为 coding agent 的共享仓库维护规范
- `CLAUDE.md` 导入 `AGENTS.md`，只补少量 Claude 专属说明

这样 human-facing 的 README 和 agent-facing 的工作规则就分开了。没那么花哨，但通常也更不容易出事。
