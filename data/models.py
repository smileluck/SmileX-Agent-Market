"""
数据模型模块，定义数据库表结构
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# 创建基础模型类
Base = declarative_base()


class ZhihuQuestion(Base):
    """
    知乎问题数据模型
    """
    __tablename__ = 'zhihu_questions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(String(50), unique=True, nullable=False, comment='知乎问题ID')
    title = Column(String(500), nullable=False, comment='问题标题')
    title_raw = Column(Text, comment='问题标题原始HTML')
    url = Column(String(500), nullable=False, comment='问题链接')
    rank = Column(Integer, default=0, comment='热门排名')
    rank_raw = Column(Text, comment='排名原始HTML')
    metrics = Column(String(100), comment='热度指标')
    metrics_raw = Column(Text, comment='热度指标原始HTML')
    excerpt = Column(Text, comment='问题描述')
    excerpt_raw = Column(Text, comment='问题描述原始HTML')
    search_task_id = Column(Integer, comment='关联的搜索任务ID')
    crawl_time = Column(DateTime, default=func.now(), comment='爬取时间')
    created_at = Column(DateTime, default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment='更新时间')
    
    def __repr__(self):
        return f"<ZhihuQuestion(question_id='{self.question_id}', title='{self.title[:30]}...')>"


class ZhihuAnswer(Base):
    """
    知乎回答数据模型
    """
    __tablename__ = 'zhihu_answers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    answer_id = Column(String(50), unique=True, nullable=False, comment='知乎回答ID')
    question_id = Column(String(50), nullable=False, comment='关联的问题ID')
    title = Column(String(500), comment='回答标题')
    title_raw = Column(Text, comment='回答标题原始HTML')
    author = Column(String(200), comment='回答作者')
    content = Column(Text, comment='回答内容')
    content_raw = Column(Text, comment='回答内容原始HTML')
    url = Column(String(500), comment='回答链接')
    question_url = Column(String(500), comment='问题链接')
    vote_up = Column(Integer, default=0, comment='点赞数')
    comment_count = Column(Integer, default=0, comment='评论数')
    create_time = Column(DateTime, comment='知乎回答原始创建时间')
    search_task_id = Column(Integer, comment='关联的搜索任务ID')
    crawl_time = Column(DateTime, default=func.now(), comment='爬取时间')
    created_at = Column(DateTime, default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment='更新时间')
    
    def __repr__(self):
        return f"<ZhihuAnswer(answer_id='{self.answer_id}', author='{self.author}')>"


class SearchTask(Base):
    """
    搜索任务数据模型，用于存储关键词搜索任务信息
    """
    __tablename__ = 'search_tasks'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    keyword = Column(String(200), nullable=False, comment='搜索关键词')
    crawl_time = Column(DateTime, default=func.now(), comment='爬取时间')
    page_count = Column(Integer, default=0, comment='爬取页数')
    total_results = Column(Integer, default=0, comment='总结果数')
    created_at = Column(DateTime, default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment='更新时间')
    
    def __repr__(self):
        return f"<SearchTask(keyword='{self.keyword}', crawl_time='{self.crawl_time}')>"


class ContentScore(Base):
    """
    内容评分数据模型，用于存储Agent对内容的评估结果
    """
    __tablename__ = 'content_scores'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    content_id = Column(String(50), nullable=False, comment='内容ID')
    content_type = Column(String(20), nullable=False, comment='内容类型(question/answer)')
    quality_score = Column(Float, default=0.0, comment='质量评分')
    spread_score = Column(Float, default=0.0, comment='传播潜力评分')
    operation_score = Column(Float, default=0.0, comment='运营价值评分')
    total_score = Column(Float, default=0.0, comment='总评分')
    evaluation_time = Column(DateTime, default=func.now(), comment='评估时间')
    evaluation_details = Column(Text, comment='评估详情')
    created_at = Column(DateTime, default=func.now(), comment='创建时间')
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), comment='更新时间')
    
    def __repr__(self):
        return f"<ContentScore(content_id='{self.content_id}', total_score={self.total_score})>"
