# Session: 2026-03-28 05:46:33 UTC

- **Session Key**: agent:main:telegram:direct:605187761
- **Session ID**: d2157033-fa7f-432c-b6e9-6f3a2d7d69d0
- **Source**: telegram

## Conversation Summary

user: Conversation info (untrusted metadata):
```json
{
  "message_id": "2762",
  "sender_id": "605187761",
  "sender": "Kevin",
  "timestamp": "Sat 2026-03-28 13:41 GMT+8"
}
```

Sender (untrusted metadata):
```json
{
  "label": "Kevin (605187761)",
  "id": "605187761",
  "name": "Kevin",
  "username": "kevin39438"
}
```

好
assistant: 好，那我们直接走 **Kimi 主会话瘦身排查**，不再瞎撞。

## 第一优先怀疑对象
按可疑度排序，我会先怀疑这几块：

### 1. 主会话上下文太肥
主会话会吃到：
- SOUL / USER / MEMORY
- 最近 memory
- HEARTBEAT
- TOOLS
- Project Context
- channel metadata
- 一大坨系统规则

Kimi 可能不是“不懂工具调用”，而是：

> **在超长上下文里，工具 schema 遵循开始漂，最后掉成 `{}`。**

这很符合你现在的现象：
- subagent：轻 → 正常
- main：重 → 异常

---

### 2. 主会话特有规则干扰了 tool use
比如这类内容：
- reply tags
- heartbeat rules
- group chat rules
- memory recall rules
- skills scanning rules
- 各种 workspace startup 约束

这些规则本身没错，但可能让 Kimi 在工具调用时优先级乱掉。

---

### 3. 主会话工具集过多
工具越多、schema 越长，Kimi 越可能抽风。

虽然你已经清掉了脏项，但 main session 的可用工具还是很多：
- file ops
- exec/process
- sessions
- memory
- web
- image

这也可能增加它掉参数的概率。

---

## 现在最值得做的不是大改，而是 **最小侵入减肥**
目标不是把人格拆烂，而是验证：

> **是不是 context / rules 太重导致 Kimi tool-call 崩掉。**

### 最小实验方案
做一个 **Kimi 专用 main agent 副本**，只保留：
- 基本身份
- 基本安全规则
- 少量必要工具
- 尽量不注入大堆 workspace context

然后测试：
- `read MEMORY.md`
- `exec echo test`

---

## 这样做的好处
### 如果瘦身版正常
说明问题就是：
- 主会话上下文太肥
- 或某段主会话规则在干扰 Kimi

### 如果瘦身版还是不正常
说明问题更底层：
- main session runtime
- main tool adapter
- OpenClaw 对 Kimi 主会话路径的实现

这样就能少走很多弯路。

---

## 我建议的具体方向
### 方案 A：新建一个 `kimi-main-lite` agent
特征：
- 不读 MEMORY / daily memory
- 不读 HEARTBEAT / TOOLS / 过多 project context
- 保留基本人格与安全
- 工具白名单先缩小到最核心：
  - `read`
  - `exec`
  - `session_status`

这最适合做验证。

### 方案 B：直接改现有 main agent
不太建议。
因为现有 main 绑了你日常工作流，贸然减掉容易误伤。

---

## 我建议怎么做
下一步直接做：

### 建一个测试用轻量主 agent
目的只有一个：
**验证 Kimi 在“主会话但极简上下文”下能不能稳定调工具。**

如果能，就继续往回加功能；
如果不能，就直接锁定是 OpenClaw main runtime 的 bug。

---

如果你点头，我下一步就帮你：
1. 设计这个 `kimi-main-lite` 的最小配置
2. 告诉你该保留什么、先砍什么
3. 做成一份很短的修改方案
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "2764",
  "sender_id": "605187761",
  "sender": "Kevin",
  "timestamp": "Sat 2026-03-28 13:42 GMT+8"
}
```

Sender (untrusted metadata):
```json
{
  "label": "Kevin (605187761)",
  "id": "605187761",
  "name": "Kevin",
  "username": "kevin39438"
}
```

Ｂ
assistant: 不建议直接选 **B（改现有 main）** 当第一刀。  
这刀太容易把你现在的日常工作流一起砍坏。

## 为什么不先改现有 main
你现有 main 绑着这些东西：
- Session Startup
- MEMORY / daily memory
- persona
- browser 规则
- heartbeat 规则
- skills 扫描
- 各种 workspace 约束

如果直接在它身上动刀，最后会变成：

> **Kimi 有没有修好不知道，但 main 被我们拆烂了。**

这不值。

---

## 更稳的做法
我建议你把 **B 改成 B'**：

### B'：复制 main 的逻辑，做一个测试版 main
也就是：
- **不动现有 main**
- 另外做一个 `kimi-main-lite`
- 专门测 Kimi 主会话

这样你原本工作流不受影响。

---

## 如果你坚持要“改现有 main”
那我建议最多只动这三块，别乱砍：

### 第一批先关掉
1. **不读 `MEMORY.md`**
2. **不读今天/昨天 daily memory**
3. **不读 `HEARTBEAT.md`**

因为这三块最肥，也最不影响最小工具测试。

### 第二批再考虑
4. 不读 `TOOLS.md`
5. 不做 skill 扫描
6. 减少长段 workspace/project context

---

## 但我的专业建议还是：
### 先做副本，不动本体
原因很简单：
- 风险小
- 好回滚
- 好对照
- 更容易判断哪一刀有用

---

## 结论
如果你说的「B」是：
- **直接改现有 main** → 我不推荐
- **走“瘦身主会话”这条路** → 我推荐，但应该用副本做

你如果同意，我下一步就直接帮你输出：

### `kimi-main-lite` 最小配置方案
- 保留什么
- 先删什么
- 怎么验证
- 验证成功后怎么一点点加回去

我会尽量写得短，不整废话。
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "2766",
  "sender_id": "605187761",
  "sender": "Kevin",
  "timestamp": "Sat 2026-03-28 13:43 GMT+8"
}
```

Sender (untrusted metadata):
```json
{
  "label": "Kevin (605187761)",
  "id": "605187761",
  "name": "Kevin",
  "username": "kevin39438"
}
```

直接改現有main
assistant: Need maybe use clawlist? multi-step project maybe yes. But user says directly modify main. Need likely inspect agent config docs? but maybe can do in workspace? We need maybe ask minimal because risky? But user explicitly asks. Need consult docs first due OpenClaw config changes. read maybe docs path? Also skill maybe none. Let's inspect .openclaw agent config.
assistant: Need inspect main agent files.
assistant: Need maybe inspect agent models file.
assistant: Need maybe not mention secrets. Now likely main controlled by prompt/hook not config. We need maybe edit AGENTS or file? But user asked directly modify existing main. Could perhaps temporarily reduce bootstrap by editing workspace AGENTS? But system injected context includes many files regardless. Maybe actual main bootstrap from hook reading files. Could modify AGENTS startup sequence to skip MEMORY/today-yesterday maybe risky. Need tell and maybe do minimal. Perhaps edit AGENTS Session Startup to simplify. Since user explicitly wants direct change. We'll modify AGENTS startup to reduce context for main? But it says if in MAIN SESSION read MEMORY.md. We can change to Kimi-light? Better perhaps add conditional: when runtime model is Kimi, only read SOUL+USER and defer memory until asked. But system prompt injection still includes files in project context. Yet startup reading less helps some. Could also trim HEARTBEAT? It's injected regardless. But user asked direct modify existing main; likely modify AGENTS.md and maybe MEMORY rules.

Need backup? maybe commit after edits.
assistant: Need commit.
assistant: 动了，而且是**只改最可疑的一刀**：

## 我改了什么
我直接改了现有 `main` 的启动规则：

### 现在如果是 **Kimi + 主会话**
启动时会：
- 只读 `SOUL.md`
- 只读 `USER.md`

**不会自动读：**
- `MEMORY.md`
- `memory/YYYY-MM-DD.md`

并且明确要求：
- 真要查旧事，再用 `memory_search` / `memory_get`
- 不再一上来把长期记忆和最近记忆整包灌进去

---

## 为什么先改这一刀
因为目前最可疑的就是：

> **main 会话上下文太肥，Kimi 在主会话里 tool-call 漂移成 `{}`**

subagent 正常、main 异常，最像就是这类问题。

所以我先砍掉最肥、又最不影响人格和基本行为的部分：
- 长期记忆
- 最近记忆

其他人格、安全、行为规则先不动。

---

## 已经做的事
- 已修改 `AGENTS.md`
- 已提交到 git

commit:
```bash
4b88584 Tune main session startup for Kimi
```

---

## 下一步怎么验
现在最干净的验证方法就是：

1. **开一个全新的主会话**
2. 继续用 **Kimi**
3. 立刻让它做一个最小工具动作，比如：
   - “读取一下 log”
   - 或 “执行 `echo test`”

### 验收标准
- 如果这次工具调用正常 → 说明就是启动阶段上下文过肥导致的
- 如果还是发 `{}` → 那就说明还要继续砍主会话的别的注入项

---

## 你现在该做的
直接：

- `/new`
- 选 **Kimi**
- 然后丢一句：
  - `检查一下log`
  - 或 `执行 echo test`

做完把结果告诉我，我继续判断下一刀砍哪。
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "2771",
  "sender_id": "605187761",
  "sender": "Kevin",
  "timestamp": "Sat 2026-03-28 13:43 GMT+8"
}
```

Sender (untrusted metadata):
```json
{
  "label": "Kevin (605187761)",
  "id": "605187761",
  "name": "Kevin",
  "username": "kevin39438"
}
```

同一個main為啥gpt沒問題kimi有問題
assistant: 因为 **不是 main 这个 agent 本身坏了**，而是：

> **同一个 main，在不同模型下，对“工具 schema”的服从能力不一样。**

## 讲白一点
同样的 main 会话会收到：
- 一样的系统规则
- 一样的 workspace context
- 一样的工具列表
- 一样的提示词结构

### GPT 的表现
它会把工具调用补完整：
```json
{"command":"openclaw logs 2>&1 | tail -50"}
```

### Kimi 的表现
在主会话这条链路里，它更容易掉成：
```json
{}
```

所以问题不是：
- main 配置完全错了
- 工具定义完全错了
- gateway 完全坏了

而是：

> **这份 main 上下文复杂度 / 规则密度 / 工具 schema 长度，对 GPT 没问题，但对 Kimi 太“吃力”了。**

---

## 为什么 subagent 的 Kimi 又正常
因为 subagent 通常更轻：

- 上下文短很多
- 注入规则少很多
- 没有那么肥的启动流程
- 没有那么多主会话特有规则

所以 Kimi 在轻环境下能正常填参数；
到了 main 这坨大上下文里，就更容易 tool-call 漂移。

---

## 为什么 GPT 扛得住
因为 GPT 在 function/tool calling 这块通常更稳，尤其是：
- 必填参数补全
- 严格按 schema 生成
- 长上下文里维持结构化输出

简单说：

> **GPT 对复杂主会话 + 工具调用的抗压性更强，Kimi 比较容易在复杂上下文里丢结构。**

---

## 这不矛盾
所以“同一个 main，GPT 正常，Kimi 不正常”其实完全可能成立：

- **main 没坏**
- **工具没坏**
- **Kimi 也不是完全坏**
- 是 **Kimi 在这份 main 上下文里更容易失真**

---

## 用工程师的话总结
更像是：

> `main session prompt complexity × Kimi tool-schema adherence`  
> 这个乘积超了它当前能稳定处理的范围。

而 GPT 的容错更高，所以没炸。

---

## 现在这刀为什么有意义
我刚刚改的，就是在降低这个复杂度：
- 去掉 Kimi main 启动时自动读 MEMORY
- 去掉 Kimi main 启动时自动读 daily memory

也就是在尝试把：

> **同一个 main，调到 Kimi 也能扛住的复杂度**

如果这刀有效，就说明我们方向对了。  
如果没效，再继续砍别的上下文块。
user: Conversation info (untrusted metadata):
```json
{
  "message_id": "2775",
  "sender_id": "605187761",
  "sender": "Kevin",
  "timestamp": "Sat 2026-03-28 13:45 GMT+8"
}
```

Sender (untrusted metadata):
```json
{
  "label": "Kevin (605187761)",
  "id": "605187761",
  "name": "Kevin",
  "username": "kevin39438"
}
```

我先試試
assistant: 好，你先试。

建议你就做最小验证，别一上来丢复杂任务：

1. `/new`
2. 继续选 **Kimi**
3. 先发一句：
   - `执行 echo test`
   - 或 `检查一下log`

只看一件事：  
**它这次会不会还把工具参数掉成 `{}`。**

你一试完，把结果丢给我，我继续往下砍。
