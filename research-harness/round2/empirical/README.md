# AIDev 热门仓库子集的 PR 状态复算

从 [观察分析](result.md) 开始。数据为作者公开的 Hugging Face AIDev v5，固定 SHA b8dc67df93e7c11f6f20c84129db7232eb1ec253。预登记只依据数据字典与文件尾 schema，随后程序核对该登记文件的摘要。数据卡和三份 Parquet 原始 footer 在 raw/；range 清单列出每个下载区块的上下界与 SHA-256。HF 发布的整个 Parquet LFS 摘要可在 tree.json 查到；本项目验证所取区块，不声称已重新计算未下载的整体文件摘要。

## 离线核查

进入本目录，运行 python verify.py。项目内 tables/sample-minimal.csv 的每个 PR 在 7 日与 30 日各一行；按 pr_key 去重即可得到独立 PR 数量。个人账户的两类正式决定可能同时发生。窗口结局三列则互斥。按组校正后的比例使用合格总体规模乘组内比例求和，再除以 67,327。个体核对完毕可运行 python report.py 生成中文报告及 manifest.json。verify.py 只依赖标准库，report.py 还需要 pandas 与 pyarrow。

## 从公开源独立重算

所需 Python、pandas 与 PyArrow 实际版本详见 manifest.json，网络抓取还需 requests。不需要 token。请在独立目录运行；脚本从官方固定提交抓取并在自己的系统临时目录缓存必要列区块，不下载全部文件。

1. python discover.py 固定版本，访问 Hugging Face API 文件树及版本 README。
2. python columns.py 只取三个 Parquet 尾部的 schema/row group metadata。
3. python ingest.py 读所需 131 个列区块。每次检查 HTTP 206、Content-Range、长度及锁文件摘要；短暂 TLS 连接失败可以重试。在已有锁的快照上会逐项比较摘要。
4. python analyze.py 构建时间窗、去重与分层，加入草稿和人工评审标签，生成 tables 与 audit.json。
5. python verify.py 独立以标准库从最小样本复算主结果，python report.py 生成 result.md 和文件摘要。

数据正文和用户名不会进入项目成果。review 表的 user 列仅为识别 Bot 字段未覆盖的明显服务账号被选取，在临时原始区块中可能包含公开用户名；临时目录为系统 TEMP 中的 aidev-r2- 加固定 SHA。分析后可清理这个目录，保留项目内用于重新拉取的区块摘要。无线上变更、无外部回写。

## 字段的含义

- no_terminal_by_horizon 指在预设时间窗内从 merged_at / closed_at 未看到终止，含后来关闭的工作，不推断最终命运。
- draft_transition 表示来自 timeline 的正面证据，不能识别从创建就一直处于草稿又未转换的 PR。
- personal_decision 是该窗内至少一个符合个人账户筛选的 APPROVED 或 CHANGES_REQUESTED；不能证实真人身份或触发合并。
- repository_rank 是代理内同一仓库的散列顺序，用于限量敏感性分析。timeline_outcome 独立从带时间的事件序列重建；缺事件时保留 no_dated_transition。
