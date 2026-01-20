# 运营增长Agent系统

## 项目简介

运营增长Agent系统是一个基于Python的自动化运营工具，主要用于爬取知乎热门问题、评估内容质量、存储数据并生成可视化报告，帮助运营人员快速发现有价值的内容和趋势。

## 功能特性

1. **知乎热门内容爬取**：自动爬取知乎热门问题列表
2. **内容智能评估**：基于AI模型对内容进行质量、传播潜力和运营价值评估
3. **数据持久化存储**：使用SQLAlchemy和SQLite数据库存储爬取数据和评估结果
4. **可视化分析报告**：生成柱状图、热力图等可视化图表，直观展示数据趋势
5. **日志管理**：完善的日志系统，便于调试和监控
6. **模块化设计**：清晰的代码结构，便于扩展和维护

## 技术栈

- **开发语言**：Python 3.8+
- **Web框架**：无（命令行工具）
- **数据库**：SQLite（默认）
- **ORM框架**：SQLAlchemy
- **爬虫框架**：自定义爬虫（基于requests和BeautifulSoup）
- **可视化库**：matplotlib
- **AI模型**：OpenAI API（可选）
- **日志系统**：logging模块

## 项目结构

```
SmileX-Agent-Mark/
├── agent/                  # AI智能评估模块
│   └── evaluator.py        # 内容评估器
├── config/                 # 配置文件目录
│   └── settings.py         # 系统设置
├── crawler/                # 爬虫模块
│   └── zhihu/              # 知乎爬虫
│       └── zhihu_crawler.py
├── data/                   # 数据模块
│   ├── models.py           # 数据模型
│   └── storage.py          # 数据存储管理
├── logs/                   # 日志文件目录
├── utils/                  # 工具模块
│   └── logger.py           # 日志配置
├── visualization/          # 可视化模块
│   └── charts.py           # 图表生成器
├── main.py                 # 项目主入口
├── migrate_database.py     # 数据库迁移脚本
├── pyproject.toml          # 项目依赖配置
├── requirements.txt        # 依赖列表
├── run.bat                 # Windows启动脚本
└── run.sh                  # Linux/Mac启动脚本
```

## 安装部署

### 环境要求

- Python 3.8+
- pip 或 uv 包管理器

### 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/smileluck/SmileX-Agent-Market.git
   cd SmileX-Agent-Mark
   ```

2. **安装依赖**
   - 使用 uv（推荐）
     ```bash
     uv install
     ```
   - 使用 pip
     ```bash
     pip install -r requirements.txt
     ```

3. **配置环境变量**
   - 复制 `.env.example` 文件为 `.env`（如果存在）
   - 根据需要修改配置项，如OpenAI API密钥等

## 使用方法

### 启动系统

- Windows系统
  ```bash
  run.bat
  ```

- Linux/Mac系统
  ```bash
  chmod +x run.sh
  ./run.sh
  ```

- 直接运行Python脚本
  ```bash
  python main.py
  ```

### 主要功能说明

1. **爬取知乎热门问题**
   - 系统会自动爬取知乎热门问题列表
   - 默认爬取20个热门问题
   - 可通过修改代码中的`limit`参数调整爬取数量

2. **内容评估**
   - 系统会对爬取的问题进行智能评估
   - 评估维度包括：质量评分、传播潜力评分、运营价值评分
   - 总评分是三个维度的加权平均值
   - 需要配置OpenAI API密钥才能使用此功能

3. **数据存储**
   - 爬取的数据会存储到SQLite数据库中
   - 数据库文件位于 `data/smilex_agent.db`
   - 支持查询和导出数据

4. **可视化报告**
   - 系统会生成可视化图表
   - 图表文件位于 `visualization/output/` 目录下
   - 包括热门问题排名柱状图和评分相关性热力图

## 配置说明

主要配置文件位于 `config/settings.py`，包含以下核心配置项：

- **PROJECT_ROOT**：项目根目录路径
- **DATABASE_URL**：数据库连接URL
- **LOG_LEVEL**：日志级别
- **OPENAI_API_KEY**：OpenAI API密钥（可选）

## 数据字典

详细数据字典请参考 `DATA_DICTIONARY.md` 文件。

## 日志管理

- 日志文件存储在 `logs/` 目录下
- 日志级别可通过配置文件调整
- 支持按日期滚动日志

## 扩展开发

### 添加新的爬虫

1. 在 `crawler/` 目录下创建新的爬虫模块
2. 实现爬虫类，继承或参考现有的 `ZhihuCrawler`
3. 在 `main.py` 中集成新的爬虫

### 添加新的评估维度

1. 修改 `ContentScore` 数据模型，添加新的评分字段
2. 更新 `ContentEvaluator` 类，实现新维度的评估逻辑
3. 在 `main.py` 中集成新的评估维度

## 注意事项

1. **知乎Cookie配置（重要）**
   
   知乎爬虫需要登录状态才能正常工作，必须配置有效的知乎Cookie。获取方法如下：
   
   ### 方法一：浏览器开发者工具获取（推荐）
   
   1. 在浏览器中登录知乎账号
   2. 按 `F12` 打开开发者工具
   3. 点击 `Network`（网络）标签页
   4. 刷新页面或访问知乎任意页面
   5. 在请求列表中找到任意请求，点击查看详情
   6. 在 `Headers` 中找到 `Request Headers` 部分
   7. 复制 `Cookie` 字段的完整值
   
   ### 方法二：浏览器插件获取
   
   1. 安装Cookie管理插件（如EditThisCookie、Cookie-Editor等）
   2. 登录知乎账号
   3. 使用插件导出知乎的Cookie
   
   ### 配置Cookie
   
   将获取到的Cookie配置到环境变量中：
   
   - 在 `.env` 文件中添加：
     ```
     ZHIHU_COOKIE=你的知乎Cookie值
     ```
   
   - 或者在系统环境变量中设置 `ZHIHU_COOKIE`
   
   **注意事项：**
   - Cookie有时效性，失效后需要重新获取
   - Cookie包含敏感信息，请勿泄露给他人
   - 建议定期更新Cookie以保证爬虫正常运行
   - 未配置Cookie可能导致爬取失败或获取不到完整数据

2. 爬虫使用说明
   - 请遵守网站的 robots.txt 规则
   - 不要频繁爬取，避免给网站服务器造成压力
   - 建议设置合理的爬取间隔

3. AI评估使用说明
   - 需要配置有效的OpenAI API密钥
   - 评估功能会产生API调用费用
   - 建议根据实际需求调整评估频率

4. 数据存储说明
   - 默认使用SQLite数据库，适合小规模数据存储
   - 如需存储大量数据，建议迁移到MySQL或PostgreSQL

## 常见问题

1. **爬取失败**
   - 检查网络连接是否正常
   - 检查网站是否有防爬机制
   - 检查爬虫代码是否需要更新

2. **AI评估失败**
   - 检查OpenAI API密钥是否有效
   - 检查网络连接是否正常
   - 检查API调用频率是否超过限制

3. **可视化图表生成失败**
   - 检查matplotlib库是否正确安装
   - 检查输出目录是否存在且可写

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎联系项目团队。
