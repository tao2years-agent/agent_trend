# 企业研发的组织级上下文与团队记忆

[离线研究报告](outputs/report.html) · [Markdown 全文](outputs/report.md) · [专题 Wiki](wiki/index.md) · [覆盖与限制](state/checkpoint.md)

研究版本 2026-11-18。知识条目、证据、发布事件与候选实验一同维护。报告 HTML 可单文件分享和离线阅读，在线引用指向原始来源；要在离线环境同时打开“本地证据”，需保留本目录结构。

## Ingest / Query / Lint

- 查询先读 `wiki/index.md`，按问题进入来源、学术证据或实验页；`corpus/screened-papers.json` 为合并人工核对后的筛查表。
- `raw/sources/2026-11-18` 是原网页／正文／API字节与哈希元数据，`raw/git` 是选定提交的源码，`raw/web` 是本轮检索或分页摘录。目录名是研究版本，抓取元数据另记 UTC。文献检索未解决的条目仍保留。
- 来源入口见 `corpus/sources.tsv` 和 `corpus/papers.tsv`；本版采集器 `scripts/capture.py` 从各表生成同名 JSON。固定提交发现器是 `scripts/inspect_source.py`。另取的修订正文及调用点各有独立 URL 和哈希元数据。刷新时新建日期目录并更新该版脚本常量，保留旧字节。
- 编辑 `research/` 的主体与 `corpus/` 的产品、机会、正文阅读卡及复核记录，随后在本目录运行 `python scripts/build.py`、`python scripts/render_html.py`、`python scripts/check_reader.py`、`python scripts/lint.py`。依赖 Python、BeautifulSoup、Markdown、websocket-client 和本机 Chrome；本版脚本针对 Windows。
- `python scripts/check_cutoff.py` 重跑历史Git隔离反例，`bun scripts/check_jit.ts` 重跑 Gemini CLI 原版适配函数的受控试验。它们都不调用语言模型。
