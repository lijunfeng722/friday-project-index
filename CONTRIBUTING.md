# 参与 Friday 跨仓库开发

先阅读 [开发规范](docs/development.md)、[仓库索引](README.md)与目标仓库自己的 AGENTS.md。元仓库的公共规范、各仓库入口和 Friday 开发 Skill 一起维护，变更应按实际影响分配到对应仓库。

在元仓库运行：

```sh
python3 scripts/check_index.py
python3 scripts/check_dev_policy.py check
python3 scripts/test_dev_policy.py
```

应看到索引与约定检查通过、测试成功。修改公共约定后，按开发规范中的 `sync` 与 `sync --check` 示例同步相关克隆，再分别提交。

PR 使用中文说明变更与验证，填写用户文档、技术文档和顶级索引的影响。公开资料只包含可公开的代码、示例与验证结论，原始家庭证据留在本机私有目录。普通开发检查不启动真实服务、摄像头或设备动作。
