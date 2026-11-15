# Linux CPU 容器启动验证

此入口将本次 Friday 与 ARL 候选代码构建为 `linux/amd64` 镜像。默认启动 Friday 的明确模拟模式、ARL Linux 宿主和本机设置页，使用独立数据卷，不导入 Mac 家庭配置、账号或自动启动摄像头。它是部署基础与启动检查入口，不能把健康状态当成完整家庭功能或实物动作验收。

## 使用已发布镜像

发布流程成功后，镜像地址为 `ghcr.io/geeprox/friday-cpu`。`main` 指向最新通过验收的主干镜像，生产部署建议从 Actions 发布摘要复制 `@sha256:…` 固定版本；不要把本地构建或 PR 检查成功当成镜像已经发布。

在新部署使用配套 Compose，无需在本机编译源码或准备 SDK 文件：

```sh
FRIDAY_RUNTIME_IMAGE=ghcr.io/geeprox/friday-cpu:main docker compose -f docker/compose.yaml pull
FRIDAY_RUNTIME_IMAGE=ghcr.io/geeprox/friday-cpu:main docker compose -f docker/compose.yaml up -d --wait --wait-timeout 660
```

也可在本机私有 `.env` 中设置同一个 `FRIDAY_RUNTIME_IMAGE`，以后所有 Compose 命令复用该值。家庭覆盖文件使用同一变量，不会悄悄切回本地标签。已有部署先按备份和停止步骤规划升级；本页发布流程不会替换正在运行的容器。首次启动仅准备固定 SDK，模型、账号和家庭配置仍需单独完成。

## 构建和启动

三个配套仓库应并列放置：`project-index/`、`Friday/`、`ARL/`，均使用包含本次 Linux 适配的代码。在本索引仓库执行：

```sh
python3 scripts/build_linux_container.py
docker compose -f docker/compose.yaml up -d --wait --wait-timeout 660
docker compose -f docker/compose.yaml ps
python3 scripts/verify_linux_container.py --image friday-linux-cpu:local --output .artifacts/linux-container/verification.json
```

构建脚本从通过公开输入扫描的 Friday 快照和 ARL 运行文件创建临时上下文，不发送 Git 历史、忽略的数据目录、环境文件或本机凭据。仓库不并列时，用 `--friday`、`--arl` 指定目录。镜像实现统一位于 Friday 的 `docker/` 和 `scripts/build_linux_container.py`；本仓库脚本是兼容入口，只维护 Compose 和家庭部署说明。基础系统摘要和 Python 组件版本固定在 Friday 的 Dockerfile 与各组件锁文件中。需要 Docker BuildKit；不会切换当前 Docker context，也不会启动或停止其他项目的容器。

镜像包括 Web、ARL、CPU 视觉/语音依赖及独立的 ONNX 视觉、ONNX 分离环境。摄像头 SDK 在首次启动时从固定官方来源自动下载并校验，用户不需要手动取得 wheel 或重新构建；大型模型、账号、NAS 挂载和 Codex CLI 授权仍按配套技术文档准备，默认不下载或加载模型。本机 Docker 内存为 8 GiB 的环境不满足可选重型 CPU 画面复核的 24 GiB 主机准入，本镜像不安装该额外环境。

人体和手部已改用固定 OpenCV Zoo ONNX 模型，在当前无 AVX 的 amd64 模拟环境通过实际模型加载与推理。基础视觉不导入 MediaPipe 原生库；可选 YAMNet 环境声音分类仍受其 AVX 条件限制，实验性虹膜注视暂标为不支持。SenseVoice 和 KTV MDX 的 CPU 推理已分别实测。

Apple Silicon Mac 使用 amd64 模拟运行目标镜像，启动耗时不能作为 Intel/AMD 机器性能指标。默认容器预算 4 个 CPU、6 GiB 内存；没有 GPU、设备映射、特权模式或 Docker socket 挂载。

## 本机页面与状态

Friday 页面为 `http://127.0.0.1:8740`。ARL 设置的访问链接包含每次启动生成的令牌，只在本机终端读取：

```sh
docker compose -f docker/compose.yaml exec runtime python /opt/container/entrypoint.py settings-url
docker compose -f docker/compose.yaml exec runtime python /opt/container/entrypoint.py health
```

Compose 只向宿主的 `127.0.0.1` 发布 8740、18745。容器内部的专用转发保留 Host/Origin，并让原应用保持回环监听；不改为信任任意代理头。请使用配套 Compose 的独立网络，不把管理端口发布到公网或加入不可信容器网络。依据：[Docker 端口发布说明](https://docs.docker.com/engine/network/port-publishing/)。

健康检查分别访问 Friday 状态接口、带令牌的 ARL 设置 API 和 ARL Unix socket。`healthy` 证明这三条控制面链路可用；模拟数据、未配置模型、Apple 不支持仍明确保留。启动后可查看页面和配置，不会仅因容器启动就控制真实设备。

验证脚本要求明确的 `--image` 与 `--output`。它为本轮新建随机名称、随机本机端口和匿名数据卷的模拟容器，检查 HTTP、授权、三个 CPU 环境、正常重启、设置持久化和令牌轮换，结束后回收本轮资源。不会复用或重启当前家庭容器；旧的 `--restart`、`--expect-mode` 参数已移除。常规验收跳过 SDK 下载；追加 `--camera-sdk` 会实际访问官方发行地址并验证首次安装和重启复用，不登录供应商、不连接设备或执行模型推理。

数据分别保存在 Compose 管理的 `friday-data`、`friday-cache` 卷中。访问令牌文件仅当前容器账号可读；不写入构建层或容器日志。模型和服务账号以后由操作者按原入口单独准备，不能直接复制 macOS 虚拟环境、动态库和钥匙串。

## 正常停止和恢复

```sh
docker compose -f docker/compose.yaml stop
docker compose -f docker/compose.yaml start --wait
```

容器收到停止信号后通知三个服务和转发进程，等待退出；数据卷保留。子服务异常退出时整个容器失败，避免剩余页面仍被误判为健康。配套 Compose 不自动重启，便于验证失败原因。

本机原服务继续使用原配置的 `stop-friday.sh` / `start-friday.sh`。原停止脚本不会管理本页新增的 Compose 项目；恢复原 macOS 部署前先停止此容器，避免 8740 端口冲突。不要使用 `down -v` 作为日常停止方法。

## 接入已有家庭

需要真实家庭模式时，使用同一自动安装镜像构建独立标签；首次启动会完成 SDK 下载与校验：

```sh
python3 scripts/build_linux_container.py --tag friday-linux-cpu:household
docker compose -f docker/compose.yaml -f docker/compose.household.yaml up -d --wait --wait-timeout 660
docker compose -f docker/compose.yaml -f docker/compose.household.yaml exec runtime python /opt/container/entrypoint.py health
```

SDK 版本和两层摘要固定在 Friday 的 `docker/camera-sdk-lock.json`；配套依赖在构建时按 `docker/camera-constraints.txt` 固定，SDK 本体只在用户容器启动后安装到私有卷。不会把账号、模型或家庭数据打包进镜像。实际切换前，需要先停止原 Friday，再把私有状态副本导入已有数据卷：家庭设置、人物库和规则库位于 `data/household/`，HA 授权位于 `data/credentials/`，摄像头配置、原暂停标记与模型位于 `data/embodied/`。数据库使用停止后的完整快照，不复制运行中的数据库单文件、macOS 虚拟环境、旧进程号或锁。

迁移时核对容器能够访问同一个 HA 实例，保留实例标识，并将设置和授权文件中的 HA 地址一致地替换为其容器可达地址；不能把相同端口当成同一实例的证明。Docker Desktop 可访问宿主提供的入口，Linux Engine 应按实际网络配置地址。ARL 地址改为容器自己的状态目录。设置与凭据只在私有卷内调整，原配置保留用于回退。

家庭模式仅接受已导入的 `use-ha-source` 标记和有效授权。启动或健康检查发现真实来源不可用时失败，不静默切换为模拟家庭。导入时保留摄像头和语音的暂停意图；本次受控测试暂时关闭副本中的家庭动作联动，避免测试话语或动作触发其他家电。

摄像头授权、属性回读、UDP 探测、真实视频、模型识别与云台动作是不同检查。Mac 上的 Linux 虚拟网络可能影响 SDK 媒体连接；即使 HA 在线，也不能承诺摄像头能够出帧。不要取消来源、时效或云台会话检查来绕过失败。

### Docker Desktop 摄像头 UDP 返回路径

本轮实际发现：SDK 的局域网发现请求发往 UDP 32108，摄像头从另一个端口回复。宿主能收取回复，容器的直接路径收不到；只改成单播也不够。配套代码提供一个只监听宿主回环地址的 Python 网络转发器，不加载 Mac 摄像头 SDK、Apple Vision 或媒体模型。摄像头连接、解码、ONNX 识别和云台决策仍在 Linux 容器内运行。原生 Linux 网络若已能直接连接，无须启用转发。

在宿主的 Friday 源码目录，先把 `FRIDAY_EMBODIED_DATA` 指向包含本人登记摄像头配置的目录，再运行：

```sh
python3 -m homeplane.embodied.camera_udp_relay --state .artifacts/camera-udp-relay.json
```

该进程只输出固定就绪信息和数量统计。随机凭据、目标绑定写入权限为 0600 的状态文件，不能提交或分享。每个包都验证凭据，只能转发到所选摄像头；连接数和空闲存活时间有上限，不保存画面或原始包。重复启动同一私有状态文件会保留凭据，目标地址变化时拒绝复用。

在另一个终端，将状态文件导入容器的摄像头私有目录，保持文件名 `camera-udp-relay.json`、权限 0600、属主为容器运行用户。建议通过标准输入和 `tar --no-same-owner` 导入，避免 `docker cp` 保留 Mac 用户编号后使文件不可读。该文件只为匹配的登记摄像头启用适配；缺少它时仍使用直接连接。不要把整套宿主环境或凭据复制到镜像。

镜像在独立构建阶段编译 `camera_udp_tunnel.c`，运行镜像无需编译器。适配只注入摄像头子进程，并覆盖普通、批量及 glibc fortify 收包入口；不改 SDK 二进制、系统路由或其他应用的套接字。非 Docker 的 Linux 开发环境若需同一适配，可用 `cc -shared -fPIC -O2 -pthread native/PortableVision/camera_udp_tunnel.c -ldl -o "$FRIDAY_EMBODIED_DATA/bin/camera-udp-tunnel.so"` 编译。

停止时先正常停止容器，等待摄像头租约恢复，再在转发终端按 Ctrl+C。若使用日常启停脚本，应在**独立私有清单**中按“转发进程、家庭容器”的顺序登记；脚本停止时反向执行。不要把测试容器加入原 Mac 服务清单而造成两套摄像头所有者同时启动。

## 已执行的启动验证（2026-11-13）

在 Apple Silicon Mac 的 Docker Desktop 上成功构建 `linux/amd64` 镜像，并通过 Compose 启动和健康检查。主机侧 Friday 页面、ARL 设置授权、Unix socket、异源及错误 Host 拒绝、Apple 不支持标记，以及主运行环境、视觉环境、分离环境的依赖导入全部通过。

正常停止退出码为 0；重启后恢复健康，临时调度设置保留、旧访问令牌失效，随后已恢复测试前的调度值。此轮未加载模型、迁移家庭配置或连接真实设备，因此不证明云台动作、自动跟踪、语音识别和分离音质，也不代表原生 x86_64 Linux 的性能验收。镜像与代码均未推送到远端。

后续家庭实测已接入既有 HA，并完成真人浏览器语音识别和公开许可音乐的 CPU 分离，使用者分别确认识别正确、伴奏效果可用。采用上述 UDP 适配后，真实摄像头画面已持续进入 Docker，CPU 解码约 20 帧/秒；ONNX 视觉处理累计超过 800 帧，观测到人体，近期单帧推理约 90–130 毫秒。自动模式已产生左右短步进且 Linux SDK 回执成功；使用者随后现场确认镜头能左右跟随，停下后稳定，本次人体自动跟踪验收通过。此确认独立于 SDK 回执记录。

有界云台图像对照也确认了实际运动：右向与左向短步进后，内存中的背景匹配分别约左移 93、右移 93 像素，分别有 174、175 个几何内点，覆盖 9、8 个背景网格。只记录几何统计，不保存家庭画面；它证明这组短步进引起镜头运动；人体左右跟随及停止稳定性另由使用者现场确认通过。


### 摄像头语音与文本播报验证（2026-11-14）

真实摄像头麦克风音频已进入 Docker 的 SenseVoice CPU 模型，使用者确认识别正确。测试没有保存音频或转写文本，没有执行语音设备指令，结束后恢复识别与跟踪策略。家庭屏“播放文本”也已实际测试，使用者确认听到且内容清楚；原音量、静音与语音暂停状态已恢复，家庭联动保持暂停。

这项播报是使用者接受的例外：Docker 经既有 HA 通知实体发送文字，由 Mini 设备侧合成声音，不是 Docker CPU 合成音频。当前接入接口未提供本地音频文件入口，设备侧是否依赖云端未验证，不声称全离线。实体须从 HA 注册表选择，并使用“播放文本”而非“执行文本指令”；目标与授权存私有持久卷。Apple 专属服务仍不支持，原 macOS 配置保留。详细链路与验收边界见 Friday 的 `docs/linux-runtime.md`。


### 迁移后手势列表为空

核对家庭设置、OAuth 凭据和 `action-authority.json` 是否仍指向同一个 HA 地址与实例。Docker 可达地址与旧宿主回环地址不同，会使控制授权无法匹配，即使授权报告显示已启用也没有可选目标。确认同一实例后，在私有卷备份旧授权，只更新迁移后的地址，保留操作范围、设备范围、有效期和暂停意图；不要通过放宽校验来绕过来源匹配。

先暂停自动规则及手势执行，再检查 `/api/embodied/devices` 的候选设备及页面下拉框。播放器当前状态是只读信息，不要求授予播放或音量写权限；新版列表可以显示待机等状态，实际离线仍显示不可用。


## 自动构建与发布边界

Friday 的 GitHub Actions 先执行同一提交的源码、隐私和回归检查，再构建 amd64 镜像并做隔离验收。`docker/runtime-lock.json` 固定 ARL 提交及运行文件摘要；发布构建拒绝脏工作区和不匹配的来源。已验收镜像通过短期构建附件交给发布任务，发布任务不重新构建。每次成功主干运行使用包含完整 Git SHA、运行编号与尝试次数的标签，并记录镜像 digest；`main` 只是方便查看最新合格版本的可变别名。部署应固定 digest。

流水线不连接家庭服务，不执行自动部署，也不包含账号、家庭数据、模型权重或条件性的 Miloco 摄像头 SDK。公开镜像不含 SDK 本体，首次启动自动下载的范围已确定；不要把完成本地构建写成已在 GHCR 发布。现有家庭 SDK 镜像保持本地，SDK 许可边界见 [官方版本许可证](https://github.com/XiaoMi/xiaomi-miloco/blob/v2026.9.11/LICENSE.md)。


## 首次 SDK 安装与故障恢复

默认自动安装 v2026.9.11，日志显示 `downloading`、`installed_verified`；成功后的启动显示 `cached_verified`，无需再次下载。安装目录为数据卷中的 `camera-sdk/2026.9.11/`，保留 wheel、许可证、说明及校验清单。可用 `docker compose -f docker/compose.yaml exec runtime python /opt/container/entrypoint.py camera-sdk-status` 复核。下载中断时启动失败，恢复网络后重启会重试；校验不一致不会继续启动。缓存损坏需先停止对应容器，备份并移走该版本目录再重启，不能删除整个数据卷。

项目仅用于非商业用途；保留的 Xiaomi Miloco 许可证还限制使用范围。自动下载和非商业说明不代表取得额外授权。许可证位于镜像 `/opt/container/licenses/Xiaomi-Miloco-LICENSE.md` 及安装目录 `LICENSE.md`，授权边界写入 `NOTICE.txt`。新流程只用于新建或明确升级的容器，不会修改现有家庭镜像、卷或暂停状态。
