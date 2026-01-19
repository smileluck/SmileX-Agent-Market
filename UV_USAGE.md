# UV包管理工具使用指南

本项目已迁移到UV包管理工具，以下是使用说明。

## 安装UV

### Windows
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Linux/Mac
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 项目初始化

### 1. 同步依赖
```bash
uv sync
```

### 2. 安装开发依赖
```bash
uv sync --extra dev
```

## 常用命令

### 安装依赖
```bash
# 安装生产依赖
uv add package_name

# 安装开发依赖
uv add --dev package_name

# 从requirements.txt安装
uv pip install -r requirements.txt
```

### 运行脚本
```bash
# 在虚拟环境中运行Python脚本
uv run python script.py

# 运行测试
uv run pytest

# 运行代码格式化
uv run black .

# 运行代码检查
uv run flake8 .
```

### 管理依赖
```bash
# 更新依赖
uv lock --upgrade

# 移除依赖
uv remove package_name

# 查看已安装的包
uv pip list
```

## 项目结构

```
SmileX-Agent-Mark/
├── .venv/              # UV创建的虚拟环境
├── uv.lock             # UV锁文件（类似于package-lock.json）
├── pyproject.toml      # 项目配置和依赖定义
├── requirements.txt     # 保留的旧依赖文件（仅作参考）
└── ...
```

## 从pip迁移到UV

### 之前（使用pip）
```bash
pip install -r requirements.txt
python script.py
```

### 现在（使用UV）
```bash
uv sync
uv run python script.py
```

## 优势

1. **快速**: UV比pip快10-100倍
2. **可靠**: 使用锁文件确保依赖一致性
3. **简单**: 统一的依赖管理工具
4. **兼容**: 完全兼容pip和pyproject.toml

## 故障排除

### 如果遇到依赖冲突
```bash
uv lock --upgrade-package package_name
```

### 如果需要重新安装所有依赖
```bash
uv sync --reinstall
```

### 如果需要清理缓存
```bash
uv cache clean
```

## 注意事项

1. `requirements.txt`文件已保留，但不再作为主要依赖管理方式
2. 所有依赖定义都在`pyproject.toml`中
3. 使用`uv run`来运行脚本会自动激活虚拟环境
4. 虚拟环境位于`.venv`目录中
