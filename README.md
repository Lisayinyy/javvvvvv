# Jev 导航站 · Jev Directory

TypeSafe AI System One 决策模型 **Jev** 的生态看板：X 爆款推文、开源项目、Skills / 工具、官方资源。中 / 英双语，静态站，无需构建。

- 线上：https://guuur45juj0j7.space.mcode.cn （`#lang=en` 打开英文）
- 文件：`index.html`（页面 + 逻辑，ECharts 无关，纯原生 JS）、`data.js`（全部数据，`window.JEV_DATA`）
- `scripts/scrape_usecases.py`：从 madewithjev.com 八个 use-case 分类抓取 X 渠道案例（标题 / 作者 / 点赞 / 帖子文本 / 缩略图 / GitHub 链接），输出 `mwj_builds.json`，再合并进 `data.js`

## 数据口径

- 推文浏览量只按推文去重统计，拆为「官方发布贴（3 条��」与「社区案例」两栏；GitHub 卡片不重复计入
- 热度分 = 点赞 + Star×3 + 浏览/400；Jev 原生项目排在集成 Jev 的大框架之前
- 数据快照 2026-09-19；所有耗时 / 成本 / 准确率均为作者自述

## 本地运行

直接双击 `index.html`，或 `python3 -m http.server` 后打开。

## 更新数据

```bash
python3 scripts/scrape_usecases.py   # 生成 mwj_builds.json
# 按 tweet id 去重后合并进 data.js（见 git log 中的合并脚本）
```
