# Jev 导航站 · Jev Directory

TypeSafe AI System One 决策模型 **Jev** 的生态看板：X 爆款推文、开源项目、Skills / 工具、官方资源。中 / 英双语，静态站，无需构建。

- 国内：https://guuur45juj0j7.space.mcode.cn （`#lang=en` 打开英文）
- 海外：https://4o1a732ukzj0n.space.minimax.io （相同内容，支持中英切换；独立站点 `443814152761464`）
- 文件：`index.html`（页面 + 逻辑，ECharts 无关，纯原生 JS）、`data.js`（全部数据，`window.JEV_DATA`）
- `scripts/scrape_usecases.py`：从 madewithjev.com 八个 use-case 分类抓取 X 渠道案例（标题 / 作者 / 点赞 / 帖子文本 / 缩略图 / GitHub 链接），输出 `mwj_builds.json`，再合并进 `data.js`
- 交互：总览保留带排名的原版网格卡片，分类页采用侧栏与信息流卡片；八项数据统计独立展示。默认显示 X 帖子，支持类型筛选、搜索、排序与中英切换。手机端通过「分类」菜单切换，搜索始终可用。
- 分类直达：`#lang=zh&cat=games-realtime&kind=x`；八个应用分类之外单列「官方与资源」。
- 分类名称、案例摘要与非仓库标题随中英界面切换；仓库名、产品名和技术标签保留原名，X 帖子原文可展开查看。

## 数据口径

- 推文浏览量只按推文去重统计，数据栏拆为「官方发布贴（3 条）」与「社区案例」；GitHub 卡片不重复计入。缺失浏览数的帖子不计入浏览量合计。
- 热度分 = 点赞 + Star×3 + 浏览/400；Jev 原生项目排在集成 Jev 的大框架之前
- 数据快照 2026-09-19；所有耗时 / 成本 / 准确率均为作者自述
- 812 条原始记录全部保留；跨类型重复资源不重复展示，页面显示 797 条（543 个开源项目、173 条推文及 81 条其他资源）。

## 本地运行

直接双击 `index.html`，或 `python3 -m http.server` 后打开。

## 更新数据

```bash
python3 scripts/scrape_usecases.py   # 生成 mwj_builds.json
# 按 tweet id 去重后合并进 data.js（见 git log 中的合并脚本）
```
