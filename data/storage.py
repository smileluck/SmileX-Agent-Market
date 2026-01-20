"""
数据存储管理模块，处理数据库连接和数据操作
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Dict, Any, Type, Optional
from datetime import datetime
from data.models import Base, ZhihuQuestion, ZhihuAnswer, ContentScore, SearchTask
from config.settings import DATABASE_URL
from utils.logger import setup_logger

logger = setup_logger(__name__)


class DataStorage:
    """
    数据存储管理类，负责数据库连接和数据操作
    """
    
    def __init__(self, db_url: str = DATABASE_URL):
        """
        初始化数据存储
        
        Args:
            db_url (str, optional): 数据库连接URL. Defaults to DATABASE_URL.
        """
        self.db_url = db_url
        self.engine = None
        self.SessionLocal = None
        
        # 初始化数据库连接
        self._init_db()
    
    def _init_db(self):
        """
        初始化数据库连接和表结构
        """
        try:
            # 创建数据库引擎
            self.engine = create_engine(self.db_url, echo=False)
            
            # 创建表结构
            Base.metadata.create_all(bind=self.engine)
            
            # 创建Session工厂
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            logger.info(f"数据库初始化成功，连接URL: {self.db_url}")
        except Exception as e:
            logger.error(f"数据库初始化失败，错误: {str(e)}")
            raise
    
    def get_db(self) -> Session:
        """
        获取数据库会话
        
        Returns:
            Session: 数据库会话对象
        """
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    def save_zhihu_questions(self, questions: List[Dict[str, Any]], search_task_id: int = None) -> int:
        """
        保存知乎问题列表到数据库
        
        Args:
            questions (List[Dict[str, Any]]): 知乎问题列表
            search_task_id (int, optional): 关联的搜索任务ID. Defaults to None.
        
        Returns:
            int: 成功保存的问题数量
        """
        if not questions:
            return 0
        
        db = next(self.get_db())
        saved_count = 0
        duplicate_count = 0
        
        try:
            for question_data in questions:
                # 处理crawl_time字段，确保是datetime对象
                crawl_time = question_data.get('crawl_time')
                if crawl_time is not None:
                    if isinstance(crawl_time, str):
                        try:
                            question_data['crawl_time'] = datetime.strptime(crawl_time, '%Y-%m-%d %H:%M:%S')
                        except Exception as e:
                            logger.warning(f"解析crawl_time字符串失败: {str(e)}，使用当前时间")
                            question_data['crawl_time'] = datetime.now()
                    elif not isinstance(crawl_time, datetime):
                        logger.warning(f"crawl_time类型不支持: {type(crawl_time)}，使用当前时间")
                        question_data['crawl_time'] = datetime.now()
                else:
                    question_data['crawl_time'] = datetime.now()
                
                # 添加搜索任务ID
                if search_task_id:
                    question_data['search_task_id'] = search_task_id
                
                # 检查问题是否已存在（去重逻辑）
                existing = db.query(ZhihuQuestion).filter(
                    ZhihuQuestion.question_id == question_data['question_id']
                ).first()
                
                if existing:
                    # 已存在，跳过保存
                    duplicate_count += 1
                    logger.debug(f"问题已存在，跳过保存: {question_data['question_id']}")
                    continue
                
                # 创建新问题
                question = ZhihuQuestion(**question_data)
                db.add(question)
                logger.debug(f"新增知乎问题: {question_data['title']}")
                saved_count += 1
            
            db.commit()
            logger.info(f"成功保存 {saved_count} 个知乎问题，跳过 {duplicate_count} 个重复问题")
            return saved_count
        except Exception as e:
            db.rollback()
            logger.error(f"保存知乎问题失败，错误: {str(e)}")
            return 0
        finally:
            db.close()
    
    def save_zhihu_answers(self, answers: List[Dict[str, Any]], search_task_id: int = None) -> int:
        """
        保存知乎回答列表到数据库
        
        Args:
            answers (List[Dict[str, Any]]): 知乎回答列表
            search_task_id (int, optional): 关联的搜索任务ID. Defaults to None.
        
        Returns:
            int: 成功保存的回答数量
        """
        if not answers:
            return 0
        
        db = next(self.get_db())
        saved_count = 0
        duplicate_count = 0
        
        try:
            for answer_data in answers:
                # 从URL中提取answer_id
                url = answer_data.get('url', '')
                answer_id = ''
                if url:
                    try:
                        answer_id = url.split('/')[-1].split('?')[0]
                    except Exception:
                        pass
                
                if not answer_id:
                    logger.warning(f"无法从URL提取answer_id，跳过该条记录")
                    continue
                
                # 检查回答是否已存在（去重逻辑）
                existing = db.query(ZhihuAnswer).filter(
                    ZhihuAnswer.answer_id == answer_id
                ).first()
                
                if existing:
                    # 已存在，跳过保存
                    duplicate_count += 1
                    logger.debug(f"回答已存在，跳过保存: {answer_id}")
                    continue
                
                # 构建保存数据
                save_data = {
                    'answer_id': answer_id,
                    'question_id': answer_data.get('question_id', ''),
                    'title': answer_data.get('title', ''),
                    'title_raw': answer_data.get('title_raw', ''),
                    'author': answer_data.get('author', ''),
                    'content': answer_data.get('content', ''),
                    'content_raw': answer_data.get('content_raw', ''),
                    'url': url,
                    'question_url': answer_data.get('question_url', ''),
                    'vote_up': answer_data.get('vote_up_count', 0),
                    'comment_count': answer_data.get('comment_count', 0),
                    'search_task_id': search_task_id
                }
                
                # 处理create_time字段，确保是datetime对象
                create_time = answer_data.get('create_time')
                if create_time is not None:
                    if isinstance(create_time, str):
                        try:
                            save_data['create_time'] = datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')
                        except Exception:
                            try:
                                from dateutil import parser
                                save_data['create_time'] = parser.parse(create_time)
                            except Exception as e:
                                logger.warning(f"解析create_time字符串失败: {str(e)}，不设置create_time")
                    elif isinstance(create_time, datetime):
                        save_data['create_time'] = create_time
                    else:
                        logger.warning(f"create_time类型不支持: {type(create_time)}，不设置create_time")
                
                # 处理crawl_time字段，确保是datetime对象
                crawl_time = answer_data.get('crawl_time')
                if crawl_time is not None:
                    if isinstance(crawl_time, str):
                        try:
                            save_data['crawl_time'] = datetime.strptime(crawl_time, '%Y-%m-%d %H:%M:%S')
                        except Exception as e:
                            logger.warning(f"解析crawl_time字符串失败: {str(e)}，使用当前时间")
                            save_data['crawl_time'] = datetime.now()
                    elif isinstance(crawl_time, datetime):
                        save_data['crawl_time'] = crawl_time
                    else:
                        logger.warning(f"crawl_time类型不支持: {type(crawl_time)}，使用当前时间")
                        save_data['crawl_time'] = datetime.now()
                else:
                    save_data['crawl_time'] = datetime.now()
                
                # 创建新回答
                answer = ZhihuAnswer(**save_data)
                db.add(answer)
                logger.debug(f"新增知乎回答: {answer_id}")
                saved_count += 1
            
            db.commit()
            logger.info(f"成功保存 {saved_count} 个知乎回答，跳过 {duplicate_count} 个重复回答")
            return saved_count
        except Exception as e:
            db.rollback()
            logger.error(f"保存知乎回答失败，错误: {str(e)}")
            return 0
        finally:
            db.close()
    
    def save_search_task(self, keyword: str, page_count: int = 0, total_results: int = 0) -> int:
        """
        保存搜索任务到数据库
        
        Args:
            keyword (str): 搜索关键词
            page_count (int, optional): 爬取页数. Defaults to 0.
            total_results (int, optional): 总结果数. Defaults to 0.
        
        Returns:
            int: 搜索任务ID
        """
        db = next(self.get_db())
        
        try:
            # 创建搜索任务
            search_task = SearchTask(
                keyword=keyword,
                page_count=page_count,
                total_results=total_results
            )
            
            db.add(search_task)
            db.commit()
            
            logger.info(f"成功保存搜索任务，关键词: {keyword}，任务ID: {search_task.id}")
            return search_task.id
        except Exception as e:
            db.rollback()
            logger.error(f"保存搜索任务失败，错误: {str(e)}")
            return 0
        finally:
            db.close()
    
    def save_content_score(self, score_data: Dict[str, Any]) -> bool:
        """
        保存内容评分到数据库
        
        Args:
            score_data (Dict[str, Any]): 内容评分数据
        
        Returns:
            bool: 是否保存成功
        """
        db = next(self.get_db())
        
        try:
            # 检查评分是否已存在
            existing = db.query(ContentScore).filter(
                ContentScore.content_id == score_data['content_id'],
                ContentScore.content_type == score_data['content_type']
            ).first()
            
            if existing:
                # 更新现有评分
                for key, value in score_data.items():
                    if hasattr(existing, key):
                        setattr(existing, key, value)
                logger.debug(f"更新内容评分: {score_data['content_id']}")
            else:
                # 创建新评分
                score = ContentScore(**score_data)
                db.add(score)
                logger.debug(f"新增内容评分: {score_data['content_id']}")
            
            db.commit()
            logger.info(f"成功保存内容评分: {score_data['content_id']}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"保存内容评分失败，错误: {str(e)}")
            return False
        finally:
            db.close()
    
    def get_zhihu_questions(self, limit: int = 100, offset: int = 0) -> List[ZhihuQuestion]:
        """
        获取知乎问题列表
        
        Args:
            limit (int, optional): 返回数量限制. Defaults to 100.
            offset (int, optional): 偏移量. Defaults to 0.
        
        Returns:
            List[ZhihuQuestion]: 知乎问题列表
        """
        db = next(self.get_db())
        
        try:
            questions = db.query(ZhihuQuestion).order_by(
                ZhihuQuestion.created_at.desc()
            ).limit(limit).offset(offset).all()
            
            logger.info(f"获取到 {len(questions)} 个知乎问题")
            return questions
        except Exception as e:
            logger.error(f"获取知乎问题失败，错误: {str(e)}")
            return []
        finally:
            db.close()
    
    def get_zhihu_question_by_id(self, question_id: str) -> Optional[ZhihuQuestion]:
        """
        根据ID获取知乎问题
        
        Args:
            question_id (str): 知乎问题ID
        
        Returns:
            Optional[ZhihuQuestion]: 知乎问题对象，不存在则返回None
        """
        db = next(self.get_db())
        
        try:
            question = db.query(ZhihuQuestion).filter(
                ZhihuQuestion.question_id == question_id
            ).first()
            
            if question:
                logger.info(f"获取到知乎问题: {question.title}")
            else:
                logger.info(f"未找到知乎问题，ID: {question_id}")
            
            return question
        except Exception as e:
            logger.error(f"获取知乎问题失败，错误: {str(e)}")
            return None
        finally:
            db.close()
    
    def get_zhihu_answers(self, limit: int = 100, offset: int = 0) -> List[ZhihuAnswer]:
        """
        获取知乎回答列表
        
        Args:
            limit (int, optional): 返回数量限制. Defaults to 100.
            offset (int, optional): 偏移量. Defaults to 0.
        
        Returns:
            List[ZhihuAnswer]: 知乎回答列表
        """
        db = next(self.get_db())
        
        try:
            answers = db.query(ZhihuAnswer).order_by(
                ZhihuAnswer.crawl_time.desc()
            ).limit(limit).offset(offset).all()
            
            logger.info(f"获取到 {len(answers)} 个知乎回答")
            return answers
        except Exception as e:
            logger.error(f"获取知乎回答失败，错误: {str(e)}")
            return []
        finally:
            db.close()
    
    def get_zhihu_answer_by_id(self, answer_id: str) -> Optional[ZhihuAnswer]:
        """
        根据ID获取知乎回答
        
        Args:
            answer_id (str): 知乎回答ID
        
        Returns:
            Optional[ZhihuAnswer]: 知乎回答对象，不存在则返回None
        """
        db = next(self.get_db())
        
        try:
            answer = db.query(ZhihuAnswer).filter(
                ZhihuAnswer.answer_id == answer_id
            ).first()
            
            if answer:
                logger.info(f"获取到知乎回答: {answer.answer_id}")
            else:
                logger.info(f"未找到知乎回答，ID: {answer_id}")
            
            return answer
        except Exception as e:
            logger.error(f"获取知乎回答失败，错误: {str(e)}")
            return None
        finally:
            db.close()
    
    def get_content_scores(self, content_type: str = None, 
                          limit: int = 100, offset: int = 0) -> List[ContentScore]:
        """
        获取内容评分列表
        
        Args:
            content_type (str, optional): 内容类型，如'question'或'answer'. Defaults to None.
            limit (int, optional): 返回数量限制. Defaults to 100.
            offset (int, optional): 偏移量. Defaults to 0.
        
        Returns:
            List[ContentScore]: 内容评分列表
        """
        db = next(self.get_db())
        
        try:
            query = db.query(ContentScore).order_by(ContentScore.total_score.desc())
            
            if content_type:
                query = query.filter(ContentScore.content_type == content_type)
            
            scores = query.limit(limit).offset(offset).all()
            
            logger.info(f"获取到 {len(scores)} 个内容评分")
            return scores
        except Exception as e:
            logger.error(f"获取内容评分失败，错误: {str(e)}")
            return []
        finally:
            db.close()


# 创建全局数据存储实例
data_storage = DataStorage()
