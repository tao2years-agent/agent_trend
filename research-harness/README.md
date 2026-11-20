# 组织级研发自动化 · 2026-11-20

<!-- second-edition -->
**2026-11-20 决策版**　[深度分析](outputs/deep-report-v2.html) · [四页决策稿](outputs/insights-decision.html) · [分享 PDF](outputs/insights-decision.pdf) · [复核 Wiki](round2/index.md)。下方早期交付与当时覆盖数保留供追溯。
<!-- /second-edition -->

[分享洞察 PDF](outputs/insights.pdf) · [可检索的离线洞察](outputs/insights.html) · [深度报告](outputs/deep-report.html) · [Markdown 全文](outputs/deep-report.md) · [产品矩阵](outputs/product-matrix.csv) · [Wiki](wiki/index.md)

## 从哪查

按场景找机制，可先在任一 HTML 的证据索引输入“批准”“重放”“归因”或产品名称。HTML 单文件即可离线转发，点击编号会展开本条机制、证据及限制，原始来源需要联网。PDF 中的编号链接到原始来源。CSV 包含逐项机制、版本变化和选型实验。Wiki 与 Markdown 支持定位本地快照。

## 如何维护

- 产品事实源是六个 lanes 下的 cases.json。每组均保存官方源码或文档、版本证据及方法说明。更新先读对应目录的 README.md 或 method.md，新增日期/内容哈希快照，校对变更事件与实现修订，再改案例字段。不要把滚动发布订阅当作历史全库。
- 学术与工程材料从 corpus/reading-seeds.tsv 和 field-seeds.tsv 出发，运行 `python -X utf8 scripts/ingest.py reading` 或 `field`。该脚本的日期目录固定为本次基线，下一轮需新建日期目录和审核清单，保留旧结果。raw/web 中为带来源定位的浏览文本。OpenAlex 和 Crossref 只用于书目与作者摘要；capture 中即使失败，已改走会议页的记录仍可在统一来源表查到。
- 研究者在 corpus/paper-notes.tsv、field-notes.tsv 记录结论、边界和具体定位；research/ 存合成判断与试点提案。report 和 Wiki 不单独手改。
- 从专题目录依次运行 `python -X utf8 scripts/build.py`、`python -X utf8 scripts/share_pdf.py`、`python -X utf8 scripts/check_reader.py`、`python -X utf8 scripts/audit.py`。HTML 使用 Python-Markdown，PDF 使用 ReportLab 和嵌入的 Windows 等线字体，浏览器验证使用本机 Chrome/CDP；细节见脚本。必要时使用 pdftoppm 渲染每页复查。
- [研究协议](research/protocol.md) · [覆盖与未决问题](state/checkpoint.md) · [审计结果](state/audit.json) · [操作记录](state/log.md)。
