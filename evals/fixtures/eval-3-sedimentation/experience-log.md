# Experience Log

## 2026-08-08 — tRPC 迁移踩坑 | Tags: [migration, trpc]

### 踩坑
批量替换 REST 时漏了旧挂载点，回归测试没覆盖。

### 根因
全局搜索只搜了 `app.use`，没搜 `import` 引用。

### 下次怎么做
迁移类任务先 Grep 全引用再动手。

> 注：本条目已出现 3 次同类（pathlib 迁移、axios 迁移），满足「毕业判据」的反复出现 ≥3 次条件。
