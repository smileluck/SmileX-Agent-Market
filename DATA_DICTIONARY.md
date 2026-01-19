# 运营增长Agent系统 - 数据字典

## 1. 数据库概述

本系统使用SQLite数据库存储数据，数据库文件位于 `data/smilex_agent.db`。系统包含4个主要表，用于存储爬虫数据、搜索任务和AI评估结果。

## 2. 表结构详解

### 2.1 zhihu_questions - 知乎问题表

**表名**：zhihu_questions  
**描述**：存储从知乎爬取的热门问题数据  
**主键**：id  
**索引**：question_id (唯一索引)

| 字段名 | 数据类型 | 长度 | 约束 | 描述 | 示例值 |
|-------|---------|------|------|------|--------|
| id | Integer | - | PRIMARY KEY, AUTOINCREMENT | 自增主键ID | 1 |
| question_id | String | 50 | UNIQUE, NOT NULL | 知乎问题ID | 123456789 |
| title | String | 500 | NOT NULL | 问题标题 | 如何提高Python编程效率？ |
| title_raw | Text | - | - | 问题标题原始HTML | `<h1 class="QuestionHeader-title">如何提高Python编程效率？</h1>` |
| url | String | 500 | NOT NULL | 问题链接 | https://www.zhihu.com/question/123456789 |
| rank | Integer | - | DEFAULT 0 | 热门排名 | 5 |
| rank_raw | Text | - | - | 排名原始HTML | `<span class="HotList-itemIndex">5</span>` |
| metrics | String | 100 | - | 热度指标 | 10.2万热度 |
| metrics_raw | Text | - | - | 热度指标原始HTML | `<div class="HotList-itemMetrics">10.2万热度</div>` |
| excerpt | Text | - | - | 问题描述 | 作为一名Python开发者，我想提高自己的编程效率... |
| excerpt_raw | Text | - | - | 问题描述原始HTML | `<p class="HotList-itemExcerpt">作为一名Python开发者，我想提高自己的编程效率...</p>` |
| search_task_id | Integer | - | - | 关联的搜索任务ID | 1 |
| crawl_time | DateTime | - | DEFAULT CURRENT_TIMESTAMP | 爬取时间 | 2026-01-19 12:34:56 |
| created_at | DateTime | - | DEFAULT CURRENT_TIMESTAMP | 记录创建时间 | 2026-01-19 12:34:56 |
| updated_at | DateTime | - | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 记录更新时间 | 2026-01-19 12:34:56 |

### 2.2 zhihu_answers - 知乎回答表

**表名**：zhihu_answers  
**描述**：存储从知乎爬取的回答数据  
**主键**：id  
**索引**：answer_id (唯一索引)

| 字段名 | 数据类型 | 长度 | 约束 | 描述 | 示例值 |
|-------|---------|------|------|------|--------|
| id | Integer | - | PRIMARY KEY, AUTOINCREMENT | 自增主键ID | 1 |
| answer_id | String | 50 | UNIQUE, NOT NULL | 知乎回答ID | 987654321 |
| question_id | String | 50 | NOT NULL | 关联的问题ID | 123456789 |
| title | String | 500 | - | 回答标题 | 提高Python编程效率的10个技巧 |
| title_raw | Text | - | - | 回答标题原始HTML | `<h2>提高Python编程效率的10个技巧</h2>` |
| author | String | 200 | - | 回答作者 | Python爱好者 |
| content | Text | - | - | 回答内容 | 1. 使用列表推导式<br>2. 掌握装饰器<br>3. 合理使用生成器... |
| content_raw | Text | - | - | 回答内容原始HTML | `<div class="RichContent-inner">1. 使用列表推导式<br>2. 掌握装饰器<br>3. 合理使用生成器...</div>` |
| url | String | 500 | - | 回答链接 | https://www.zhihu.com/question/123456789/answer/987654321 |
| question_url | String | 500 | - | 问题链接 | https://www.zhihu.com/question/123456789 |
| vote_up | Integer | - | DEFAULT 0 | 点赞数 | 1234 |
| comment_count | Integer | - | DEFAULT 0 | 评论数 | 56 |
| create_time | DateTime | - | - | 知乎回答原始创建时间 | 2026-01-18 10:20:30 |
| search_task_id | Integer | - | - | 关联的搜索任务ID | 1 |
| crawl_time | DateTime | - | DEFAULT CURRENT_TIMESTAMP | 爬取时间 | 2026-01-19 12:34:56 |
| created_at | DateTime | - | DEFAULT CURRENT_TIMESTAMP | 记录创建时间 | 2026-01-19 12:34:56 |
| updated_at | DateTime | - | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 记录更新时间 | 2026-01-19 12:34:56 |

### 2.3 search_tasks - 搜索任务表

**表名**：search_tasks  
**描述**：存储关键词搜索任务信息  
**主键**：id

| 字段名 | 数据类型 | 长度 | 约束 | 描述 | 示例值 |
|-------|---------|------|------|------|--------|
| id | Integer | - | PRIMARY KEY, AUTOINCREMENT | 自增主键ID | 1 |
| keyword | String | 200 | NOT NULL | 搜索关键词 | Python编程效率 |
| crawl_time | DateTime | - | DEFAULT CURRENT_TIMESTAMP | 爬取时间 | 2026-01-19 12:34:56 |
| page_count | Integer | - | DEFAULT 0 | 爬取页数 | 5 |
| total_results | Integer | - | DEFAULT 0 | 总结果数 | 100 |
| created_at | DateTime | - | DEFAULT CURRENT_TIMESTAMP | 记录创建时间 | 2026-01-19 12:34:56 |
| updated_at | DateTime | - | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 记录更新时间 | 2026-01-19 12:34:56 |

### 2.4 content_scores - 内容评分表

**表名**：content_scores  
**描述**：存储AI对内容的评估结果  
**主键**：id  
**索引**：content_id + content_type (组合索引)

| 字段名 | 数据类型 | 长度 | 约束 | 描述 | 示例值 |
|-------|---------|------|------|------|--------|
| id | Integer | - | PRIMARY KEY, AUTOINCREMENT | 自增主键ID | 1 |
| content_id | String | 50 | NOT NULL | 内容ID（对应question_id或answer_id） | 123456789 |
| content_type | String | 20 | NOT NULL | 内容类型 | question |
| quality_score | Float | - | DEFAULT 0.0 | 质量评分（0-10分） | 8.5 |
| spread_score | Float | - | DEFAULT 0.0 | 传播潜力评分（0-10分） | 7.2 |
| operation_score | Float | - | DEFAULT 0.0 | 运营价值评分（0-10分） | 9.0 |
| total_score | Float | - | DEFAULT 0.0 | 总评分（0-10分） | 8.2 |
| evaluation_time | DateTime | - | DEFAULT CURRENT_TIMESTAMP | 评估时间 | 2026-01-19 12:34:56 |
| evaluation_details | Text | - | - | 评估详情（JSON格式） | {"quality_analysis": "内容结构清晰，实用性强", "spread_analysis": "话题热度高，潜在传播性好"} |
| created_at | DateTime | - | DEFAULT CURRENT_TIMESTAMP | 记录创建时间 | 2026-01-19 12:34:56 |
| updated_at | DateTime | - | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 记录更新时间 | 2026-01-19 12:34:56 |

## 3. 数据关系图

```
+----------------+     +----------------+     +----------------+     +----------------+
| zhihu_answers  |     | zhihu_questions|     | content_scores |     | search_tasks   |
+----------------+     +----------------+     +----------------+     +----------------+
| id             |     | id             |     | id             |     | id             |
| answer_id      |     | question_id    |     | content_id     |     | keyword        |
| question_id    |---->| url            |     | content_type   |<----| page_count     |
| author         |     | title          |     | quality_score  |     | total_results  |
| content        |     | metrics        |     | spread_score   |     |                |
| vote_up        |     | crawl_time     |     | operation_score|     |                |
| comment_count  |     | search_task_id |---->| total_score    |     |                |
| search_task_id |     |                |     | evaluation_time|     |                |
+----------------+     +----------------+     +----------------+     +----------------+
```

## 4. 数据流向

1. **爬虫数据采集**：
   - 系统通过 `ZhihuCrawler` 爬取知乎热门问题
   - 爬取的数据首先存储到 `zhihu_questions` 表
   - 可选择爬取问题的回答，存储到 `zhihu_answers` 表

2. **搜索任务管理**：
   - 每次搜索操作会创建一条 `search_task` 记录
   - 爬虫数据会关联到对应的搜索任务ID

3. **AI内容评估**：
   - 系统使用 `ContentEvaluator` 对爬取的内容进行评估
   - 评估结果存储到 `content_scores` 表
   - 每个内容（问题或回答）对应一条或多条评分记录

4. **数据可视化**：
   - 系统从数据库读取数据，生成可视化图表
   - 图表包括热门问题排名、评分相关性等

## 5. 数据类型说明

- **Integer**：整数类型，用于存储计数、ID等
- **String**：字符串类型，用于存储较短的文本数据
- **Text**：长文本类型，用于存储HTML内容、回答正文等
- **DateTime**：日期时间类型，用于存储时间戳
- **Float**：浮点类型，用于存储评分等小数数据

## 6. 索引策略

- **唯一索引**：`question_id`、`answer_id` 字段使用唯一索引，确保数据唯一性
- **组合索引**：`content_id` + `content_type` 组合索引，提高评分查询效率
- **外键关系**：搜索任务ID与爬虫数据之间建立逻辑关联，便于数据追溯

## 7. 数据生命周期

- **爬虫数据**：长期保存，可定期清理过期数据
- **搜索任务**：长期保存，用于历史任务查询
- **AI评估结果**：长期保存，支持趋势分析

## 8. 数据安全

- 数据库文件权限设置为只读（除系统进程外）
- 敏感数据（如API密钥）不存储在数据库中
- 定期备份数据库文件，防止数据丢失

## 9. 数据迁移

系统提供数据库迁移脚本 `migrate_database.py`，用于：
- 创建初始表结构
- 更新表结构
- 数据备份和恢复

## 10. 常见查询示例

### 10.1 查询热门问题TOP10

```sql
SELECT title, metrics, rank 
FROM zhihu_questions 
ORDER BY rank ASC 
LIMIT 10;
```

### 10.2 查询高评分问题

```sql
SELECT q.title, s.total_score, s.quality_score, s.spread_score, s.operation_score 
FROM zhihu_questions q 
JOIN content_scores s ON q.question_id = s.content_id 
WHERE s.content_type = 'question' 
ORDER BY s.total_score DESC 
LIMIT 10;
```

### 10.3 查询搜索任务历史

```sql
SELECT keyword, crawl_time, page_count, total_results 
FROM search_tasks 
ORDER BY crawl_time DESC;
```

## 11. 数据库维护

### 11.1 定期清理

建议定期清理过期数据，特别是爬虫数据：

```sql
-- 删除30天前的爬虫数据
DELETE FROM zhihu_questions WHERE crawl_time < datetime('now', '-30 days');
DELETE FROM zhihu_answers WHERE crawl_time < datetime('now', '-30 days');
```

### 11.2 数据备份

定期备份数据库文件：

```bash
# Linux/Mac
echo "数据库备份开始..."
date
cp data/smilex_agent.db data/backup/smilex_agent_$(date +%Y%m%d_%H%M%S).db
echo "数据库备份完成！"

# Windows
echo 数据库备份开始...
date /t
time /t
copy data\smilex_agent.db data\backup\smilex_agent_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%.db
echo 数据库备份完成！
```

## 12. 性能优化建议

1. **索引优化**：根据实际查询需求调整索引
2. **批量操作**：爬虫数据采用批量插入，提高效率
3. **分页查询**：大数据量查询时使用分页
4. **定期清理**：删除无用数据，减少数据库大小
5. **连接池**：高并发场景下使用连接池管理数据库连接

## 13. 未来扩展

1. **支持多数据库**：扩展支持MySQL、PostgreSQL等关系型数据库
2. **数据仓库**：添加数据仓库模块，支持大数据分析
3. **实时数据**：添加实时数据处理能力，支持流式数据
4. **数据加密**：对敏感数据进行加密存储
5. **数据脱敏**：实现数据脱敏功能，保护用户隐私

## 14. 数据字典维护

- 数据字典由开发人员维护，与代码同步更新
- 每次表结构变更后，需及时更新数据字典
- 数据字典版本与系统版本保持一致
