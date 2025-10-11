`uv` 是由 Astral（Ruff 的开发团队）推出的一个超高速 Python 包安装器和解析器，旨在替代 `pip`、`pip-tools`、`virtualenv` 等工具。它使用 Rust 编写，性能远超现有工具，同时保持与现有生态的兼容性。

## 1. 安装 uv
### 支持的操作系统
+ Windows
+ macOS
+ Linux

### 安装方法
#### 使用 pip 安装
```bash
pip install uv
```

#### 使用官方安装脚本
```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex
```

#### 使用包管理器
```bash
# Homebrew (macOS/Linux)
brew install uv

# Scoop (Windows)
scoop install uv

# Arch Linux
yay -S uv
```

安装完成后，将 uv 添加到 PATH：

```bash
# Linux/macOS
source ~/.cargo/env
# 或者重启终端
```

## 2. 基本概念
### uv 的核心功能
+ **包安装**：替代 `pip install`
+ **虚拟环境管理**：替代 `python -m venv` 和 `virtualenv`
+ **依赖解析**：替代 `pip-tools`
+ **项目管理**：类似 `poetry` 和 `pipenv` 的功能
+ **Python 版本管理**：内置 Python 版本发现和管理

### 与现有工具的关系
```plain
uv = pip + pip-tools + virtualenv + poetry (部分功能)
```

## 3. 虚拟环境管理
### 创建虚拟环境
```bash
# 创建名为 .venv 的虚拟环境（默认名称）
uv venv

# 指定虚拟环境名称
uv venv myenv

# 指定 Python 版本
uv venv --python 3.11
uv venv --python python3.11

# 指定虚拟环境路径
uv venv /path/to/venv
```

### 激活虚拟环境
```bash
# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 删除虚拟环境
```bash
# 直接删除目录
rm -rf .venv
# 或
rmdir /s .venv  # Windows
```

### 查看 Python 版本信息
```bash
# 查看可用的 Python 版本
uv python list

# 查看当前使用的 Python
uv python find
```

## 4. 包管理
### 安装包
```bash
# 安装单个包
uv pip install requests

# 安装多个包
uv pip install requests flask django

# 从 requirements.txt 安装
uv pip install -r requirements.txt

# 安装特定版本
uv pip install requests==2.28.0

# 安装兼容版本
uv pip install "requests>=2.25.0,<3.0.0"

# 从 Git 安装
uv pip install git+https://github.com/psf/requests.git

# 从本地路径安装
uv pip install ./my-package
```

### 卸载包
```bash
# 卸载单个包
uv pip uninstall requests

# 卸载多个包
uv pip uninstall requests flask
```

### 列出已安装的包
```bash
# 列出所有包
uv pip list

# 列出过时的包
uv pip list --outdated

# 以 freeze 格式输出
uv pip freeze
```

### 显示包信息
```bash
# 显示包详细信息
uv pip show requests

# 显示依赖树
uv pip show --tree requests
```

## 5. 依赖解析和锁定
### 生成 requirements.txt
```bash
# 从 pyproject.toml 生成
uv pip compile pyproject.toml

# 从 requirements.in 生成锁定文件
uv pip compile requirements.in

# 生成到指定文件
uv pip compile requirements.in -o requirements.txt

# 指定 Python 版本
uv pip compile --python-version 3.11 requirements.in

# 包含开发依赖
uv pip compile --all-extras requirements.in
```

### 同步依赖
```bash
# 根据 requirements.txt 同步环境
uv pip sync requirements.txt

# 同步并删除未在 requirements.txt 中的包
uv pip sync requirements.txt

# 同步到指定虚拟环境
uv pip sync --python /path/to/python requirements.txt
```

## 6. 项目管理
### 初始化项目
```bash
# 创建新的 Python 项目
uv init my-project
cd my-project

# 初始化当前目录
uv init .
```

生成的项目结构：

```plain
my-project/
├── pyproject.toml
├── README.md
└── src/
    └── my_project/
        └── __init__.py
```

### 添加依赖
```bash
# 添加运行时依赖
uv add requests

# 添加开发依赖
uv add --dev pytest black

# 添加可选依赖（extras）
uv add --optional dev pytest
```

### 移除依赖
```bash
# 移除依赖
uv remove requests

# 移除开发依赖
uv remove --dev pytest
```

### 安装项目依赖
```bash
# 安装所有依赖（包括可选依赖）
uv sync

# 安装时不包括可选依赖
uv sync --no-all-extras

# 安装特定的可选依赖
uv sync --extra dev
```

## 7. 高级功能
### 并行安装
uv 默认使用并行安装，大幅提升安装速度：

```bash
# 显式指定并发数
uv pip install --concurrent-downloads 10 requests
```

### 缓存管理
```bash
# 查看缓存信息
uv cache dir

# 清理缓存
uv cache clean

# 清理特定包的缓存
uv cache clean requests
```

### 离线模式
```bash
# 离线安装（使用缓存）
uv pip install --offline requests
```

### 自定义索引源
```bash
# 使用自定义 PyPI 源
uv pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple requests

# 添加额外索引源
uv pip install --extra-index-url https://pypi.org/simple requests
```

### 环境变量配置
```bash
# 设置缓存目录
export UV_CACHE_DIR=/path/to/cache

# 设置默认索引源
export UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple

# 设置并发下载数
export UV_CONCURRENT_DOWNLOADS=20
```

## 8. 性能对比
### 安装速度测试
```bash
# 测试安装 Django 及其依赖
time pip install django
time uv pip install django

# 测试从 requirements.txt 安装
time pip install -r requirements.txt
time uv pip install -r requirements.txt
```

典型性能提升：

+ 包安装：5-10 倍速度提升
+ 依赖解析：10-100 倍速度提升
+ 虚拟环境创建：2-5 倍速度提升

## 9. 实际使用示例
### 示例 1：快速开始新项目
```bash
# 1. 创建项目目录
mkdir my-fastapi-app
cd my-fastapi-app

# 2. 初始化项目
uv init .

# 3. 创建虚拟环境
uv venv

# 4. 激活虚拟环境
source .venv/bin/activate  # Linux/macOS

# 5. 添加依赖
uv add fastapi uvicorn[standard]

# 6. 添加开发依赖
uv add --dev pytest httpx

# 7. 运行应用
uv run uvicorn main:app --reload
```

### 示例 2：迁移现有项目
```bash
# 1. 在项目根目录创建虚拟环境
uv venv

# 2. 从 requirements.txt 安装依赖
uv pip install -r requirements.txt

# 3. 生成锁定文件（可选）
uv pip freeze > requirements.lock

# 4. 后续使用锁定文件同步
uv pip sync requirements.lock
```

### 示例 3：CI/CD 集成
```yaml
# GitHub Actions 示例
name: CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Install uv
      run: curl -LsSf https://astral.sh/uv/install.sh | sh
    - name: Setup Python
      run: uv python install 3.11
    - name: Create virtual environment
      run: uv venv --python 3.11
    - name: Install dependencies
      run: uv pip install -r requirements.txt
    - name: Run tests
      run: uv run pytest
```

## 10. 配置文件
### pyproject.toml 配置
```toml
[project]
name = "my-project"
version = "0.1.0"
description = "A sample project"
dependencies = [
    "requests>=2.25.0",
    "click>=8.0.0",
]
requires-python = ">=3.8"

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=22.0.0",
]
docs = [
    "sphinx>=4.0.0",
]

[tool.uv]
# uv 特定配置
index-url = "https://pypi.tuna.tsinghua.edu.cn/simple"
concurrent-downloads = 20
```

### 全局配置
创建 `~/.config/uv/uv.toml`：

```toml
[index]
url = "https://pypi.tuna.tsinghua.edu.cn/simple"

[install]
concurrent-downloads = 20
```

## 11. 常见问题和解决方案
### 问题 1：找不到 Python 解释器
```bash
# 解决方案：指定 Python 路径
uv venv --python /usr/bin/python3.11
```

### 问题 2：网络问题导致安装失败
```bash
# 解决方案：使用国内镜像源
uv pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple package-name
```

### 问题 3：依赖冲突
```bash
# 解决方案：使用更严格的版本约束
uv pip compile --generate-hashes requirements.in
```

### 问题 4：缓存问题
```bash
# 解决方案：清理缓存后重试
uv cache clean
uv pip install package-name
```

## 12. 最佳实践
### 1. 使用锁定文件
始终在生产环境中使用锁定文件确保依赖一致性：

```bash
uv pip compile requirements.in -o requirements.txt
uv pip sync requirements.txt
```

### 2. 分离开发和生产依赖
```bash
# 生产依赖
uv add fastapi uvicorn

# 开发依赖
uv add --dev pytest black mypy
```

### 3. 使用虚拟环境
每个项目都应该有自己的虚拟环境：

```bash
cd project-dir
uv venv
source .venv/bin/activate
```

### 4. 定期更新依赖
```bash
# 检查过时的包
uv pip list --outdated

# 更新锁定文件
uv pip compile --upgrade requirements.in
```

### 5. 利用缓存
在 CI/CD 中缓存 uv 缓存目录以加速构建：

```bash
# 缓存目录位置
uv cache dir
```

## 13. 与其他工具的对比
| 功能 | uv | pip + venv | poetry | pipenv |
| --- | --- | --- | --- | --- |
| 安装速度 | ⚡️ 极快 | 🐢 慢 | 🏃‍♂️ 中等 | 🏃‍♂️ 中等 |
| 依赖解析 | ⚡️ 极快 | 🐢 慢 | 🏃‍♂️ 中等 | 🐢 慢 |
| 虚拟环境 | ✅ 内置 | ✅ 需要额外命令 | ✅ 内置 | ✅ 内置 |
| 锁定文件 | ✅ 支持 | ✅ 需要 pip-tools | ✅ 内置 | ✅ 内置 |
| 项目初始化 | ✅ 支持 | ❌ 不支持 | ✅ 支持 | ✅ 支持 |
| 兼容性 | ✅ 完全兼容 | ✅ 标准 | ⚠️ 部分兼容 | ⚠️ 部分兼容 |


## 14. 总结
`uv` 是一个革命性的 Python 工具，它将多个工具的功能集成到一个高性能的解决方案中。主要优势包括：

+ **极致性能**：Rust 编写，速度远超现有工具
+ **完全兼容**：与现有 pip、requirements.txt 等完全兼容
+ **功能完整**：集成了包管理、虚拟环境、依赖解析等功能
+ **易于使用**：命令行接口直观，学习成本低
+ **活跃开发**：由 Ruff 团队维护，更新频繁

对于新项目，强烈推荐使用 `uv` 作为默认的 Python 开发工具。对于现有项目，可以逐步迁移到 `uv` 以获得性能提升。

### 快速开始命令汇总
```bash
# 安装 uv
pip install uv

# 创建项目
uv init my-project
cd my-project

# 创建虚拟环境
uv venv

# 激活虚拟环境
source .venv/bin/activate  # Linux/macOS

# 安装依赖
uv add requests
uv add --dev pytest

# 运行代码
uv run python main.py

# 同步依赖
uv sync
```

通过使用 `uv`，你可以显著提升 Python 开发体验，减少等待时间，提高开发效率。

