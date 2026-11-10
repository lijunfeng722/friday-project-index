# Friday

家庭产品主仓：设备、手势、回看、KTV 与可选 ARL/API 智能通道。

- [代码或文档仓库](https://github.com/Geeprox/Friday)
- 类型：主项目。
- 使用关系：核心。

## 怎样使用这个仓库

独立运行；本地视觉属于本仓库，不是 Miloco 内置手势。

从产品 README 和部署指南开始；修改用户可见行为后，同步用户手册对应任务页和截图。摄像头、音频、云台、自动化及设备操作分别配置，不由一个连接成功推定全部开通。

已有环境的启动、正常停止、重新启动、依赖升级与现场验收入口统一列在[部署维护总览](../docs/operations.md)。安装器的 Xiaomi Home v0.5.0 固定版本、来源校验及离线升级修复已推送到本仓库 `main`，提交为 [4ecf56c](https://github.com/Geeprox/Friday/commit/4ecf56c6a515f1fe1d6494e3632a2257490353ad)。日常启停源码移至元仓库根目录，用户手册保留工具下载副本；使用时核对源码和工具版本。

多人镜头中，另一人持续比 OK 不能接管已有操作者的问题已由 [5961567](https://github.com/Geeprox/Friday/commit/5961567d3ed897eed20fb161be6dfa49d522df3d)修复；107 项相关回归通过。用户手册安装基线已更新至该公开提交，具体选择与验证步骤见部署维护总览。

## 与其他仓库的关系

ARL · Codex 与 OpenAI API 是可选文字智能通道，使用不同凭据与用量。Friday 主仓维护 Responses 语义解释、Decisions 影子建议、Realtime 主动输入和 Image API 歌曲背景，以及本机预算、故障暂停和 ARL/本地降级。设备范围、任务确认及媒体票据仍由原业务链路管理。

本机 API 配置与背景库属于私有运行数据，不进入仓库或可清理构建目录。用户手册维护开关、上限、隐私范围与示例截图；接口和数据流见[主仓智能通道说明](https://github.com/Geeprox/Friday/blob/main/docs/intelligence.md)。软件回归不替代真实 API 账户、麦克风和电视验收。

参见[整体架构](../docs/architecture.md)，或[返回总索引](../README.md)。
