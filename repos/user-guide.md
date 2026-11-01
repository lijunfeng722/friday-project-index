# Friday 用户手册

面向家庭使用者的图文手册、GitHub Pages 与可下载的部署维护脚本。

- [代码或文档仓库](https://github.com/lijunfeng722/friday-user-guide)
- 类型：独立文档。
- 使用关系：使用与部署维护。

## 怎样使用这个仓库

静态站点，不连接家庭账号或设备。

[在线手册](https://lijunfeng722.github.io/friday-user-guide/)按入门、操作指南、参考、说明和常见问题组织。源内容为 Markdown，使用 MkDocs Material 构建；推送 main 后由 GitHub Actions 发布。

[公开脚本目录](https://github.com/lijunfeng722/friday-user-guide/tree/main/docs/assets/scripts)提供启停管理程序、停止与重新启动入口、依赖安装升级工具的下载副本及校验清单。安装器源码和回归测试已同步到 [Friday 主仓](friday.md)。脚本由使用者下载后在部署电脑运行；私有服务清单不上传。操作与版本说明见[部署维护总览](../docs/operations.md)。

## 与其他仓库的关系

参见[整体架构](../docs/architecture.md)，或[返回总索引](../README.md)。
