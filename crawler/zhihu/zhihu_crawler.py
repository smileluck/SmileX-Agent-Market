"""
知乎爬虫类，实现知乎数据的爬取
"""
import time
import json
from datetime import datetime
from typing import List, Dict, Any
from bs4 import BeautifulSoup
from crawler.base_crawler import BaseCrawler
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ZhihuCrawler(BaseCrawler):
    """
    知乎爬虫类，用于爬取知乎热门问题、回答等数据
    """
    
    def __init__(self, **kwargs):
        """
        初始化知乎爬虫
        
        Args:
            **kwargs: 基础爬虫的配置参数
        """
        from config.settings import CRAWLER_CONFIG
        zhihu_config = CRAWLER_CONFIG['ZHIHU']
        
        super().__init__(
            base_url=zhihu_config['BASE_URL'],
            user_agent=zhihu_config['USER_AGENT'],
            max_retries=zhihu_config['MAX_RETRIES'],
            download_delay=zhihu_config['DOWNLOAD_DELAY'],
            cookie=zhihu_config['COOKIE']
        )
        
        # 知乎热门问题URL
        self.hot_list_url = f"{self.base_url}/hot"
    
    def _clean_html_content(self, html_content: str) -> str:
        """
        清理HTML标签，提取纯文本内容
        
        Args:
            html_content (str): 包含HTML标签的内容
        
        Returns:
            str: 清理后的纯文本内容
        """
        if not html_content:
            return ""
        
        try:
            # 使用BeautifulSoup解析HTML并提取纯文本
            soup = BeautifulSoup(html_content, 'lxml')
            text = soup.get_text(separator=' ', strip=True)
            
            # 清理多余的空白字符
            import re
            text = re.sub(r'\s+', ' ', text).strip()
            
            return text
        except Exception as e:
            logger.error(f"清理HTML内容失败，错误: {str(e)}")
            return html_content
    
    def get_hot_questions(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        获取知乎热门问题列表
        
        Args:
            limit (int, optional): 返回的问题数量限制. Defaults to 50.
        
        Returns:
            List[Dict[str, Any]]: 热门问题列表，每个问题包含标题、链接、热度等信息
        """
        logger.info(f"开始爬取知乎热门问题，限制数量: {limit}")
        
        try:
            # 请求热门问题页面
            response = self.get(self.hot_list_url)
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 解析热门问题列表
            hot_items = soup.find_all('section', class_='HotItem')
            questions = []
            
            for i, item in enumerate(hot_items):
                if i >= limit:
                    break
                
                try:
                    # 提取问题信息
                    question = self._parse_hot_item(item)
                    if question:
                        questions.append(question)
                        logger.info(f"成功解析热门问题: {question['title']}")
                    
                    # 添加下载延迟
                    time.sleep(self.download_delay)
                except Exception as e:
                    logger.error(f"解析热门问题失败，索引: {i}, 错误: {str(e)}")
                    continue
            
            logger.info(f"成功爬取 {len(questions)} 个知乎热门问题")
            return questions
        except Exception as e:
            logger.error(f"爬取知乎热门问题失败，错误: {str(e)}")
            return []
    
    def _parse_hot_item(self, item: BeautifulSoup) -> Dict[str, Any]:
        """
        解析单个热门问题项
        
        Args:
            item (BeautifulSoup): 热门问题的BeautifulSoup对象
        
        Returns:
            Dict[str, Any]: 解析后的问题信息，包含原始HTML和清理后的文本
        """
        question = {}
        
        try:
            # 排名
            rank_tag = item.find('div', class_='HotItem-rank')
            rank_text = rank_tag.text.strip() if rank_tag else '0'
            question['rank'] = int(rank_text)
            question['rank_raw'] = str(rank_tag) if rank_tag else ''
            
            # 问题链接和标题
            title_tag = item.find('h2', class_='HotItem-title')
            if title_tag and title_tag.a:
                title_text = title_tag.a.text.strip()
                question['title'] = title_text
                question['title_raw'] = str(title_tag.a)
                question['url'] = title_tag.a['href']
                
                # 提取问题ID
                question_id = question['url'].split('/')[-1].split('?')[0]
                question['question_id'] = question_id
            
            # 热度
            metrics_tag = item.find('div', class_='HotItem-metrics')
            if metrics_tag:
                metrics_text = metrics_tag.text.strip()
                question['metrics'] = metrics_text
                question['metrics_raw'] = str(metrics_tag)
            
            # 问题描述
            excerpt_tag = item.find('p', class_='HotItem-excerpt')
            if excerpt_tag:
                excerpt_text = excerpt_tag.text.strip()
                question['excerpt'] = excerpt_text
                question['excerpt_raw'] = str(excerpt_tag)
            
            # 标记爬取时间（使用datetime对象）
            question['crawl_time'] = datetime.now()
            
            return question
        except Exception as e:
            logger.error(f"解析热门问题项失败，错误: {str(e)}")
            return {}
    
    def get_question_answers(self, question_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        获取问题的回答列表
        
        Args:
            question_id (str): 问题ID
            limit (int, optional): 返回的回答数量限制. Defaults to 20.
        
        Returns:
            List[Dict[str, Any]]: 回答列表，每个回答包含作者、内容、点赞数等信息
        """
        logger.info(f"开始爬取问题回答，问题ID: {question_id}，限制数量: {limit}")
        
        try:
            # 知乎问题回答API (实际中需要找到正确的API或使用Selenium)
            # 这里使用问题页面URL作为示例
            question_url = f"{self.base_url}/question/{question_id}"
            response = self.get(question_url)
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 解析回答列表（实际中知乎回答是动态加载的，需要使用Selenium或API）
            answers = []
            
            # TODO: 实现知乎回答的动态加载和解析
            # 这里返回空列表，后续需要完善
            logger.warning(f"知乎回答爬取功能待完善，问题ID: {question_id}")
            
            return answers
        except Exception as e:
            logger.error(f"爬取问题回答失败，问题ID: {question_id}，错误: {str(e)}")
            return []
    
    def get_answer_details(self, answer_id: str) -> Dict[str, Any]:
        """
        获取单个回答的详细信息
        
        Args:
            answer_id (str): 回答ID
        
        Returns:
            Dict[str, Any]: 回答的详细信息
        """
        logger.info(f"开始爬取回答详情，回答ID: {answer_id}")
        
        try:
            answer_url = f"{self.base_url}/answer/{answer_id}"
            response = self.get(answer_url)
            
            # TODO: 实现回答详情的解析
            # 这里返回空字典，后续需要完善
            logger.warning(f"知乎回答详情爬取功能待完善，回答ID: {answer_id}")
            
            return {}
        except Exception as e:
            logger.error(f"爬取回答详情失败，回答ID: {answer_id}，错误: {str(e)}")
            return {}
    
    def search_content(self, query: str, max_pages: int = 10, limit: int = 20) -> List[Dict[str, Any]]:
        """
        搜索知乎内容
        
        Args:
            query (str): 搜索关键词，支持多关键词查询
            max_pages (int, optional): 最大爬取页数. Defaults to 10.
            limit (int, optional): 每页返回数量限制. Defaults to 20.
        
        Returns:
            List[Dict[str, Any]]: 搜索结果列表，每个结果包含标题、内容、链接等信息
        """
        logger.info(f"开始搜索知乎内容，关键词: {query}，最大页数: {max_pages}，每页限制: {limit}")
        
        all_results = []
        current_page = 0
        is_end = False
        next_url = None
        
        try:
            while current_page < max_pages and not is_end:
                try:
                    # 构建请求URL
                    if next_url:
                        search_url = next_url
                    else:
                        search_url = f"{self.base_url}/api/v4/search_v3"
                        params = {
                            'gk_version': 'gz-gaokao',
                            't': 'general',
                            'q': query,
                            'correction': 1,
                            'offset': current_page * limit,
                            'limit': limit,
                            'filter_fields': '',
                            'lc_idx': 0,
                            'show_all_topics': 0,
                            'search_source': 'Filter',
                            'sort': 'created_time'
                        }
                    
                    logger.info(f"正在爬取第 {current_page + 1} 页...")
                    
                    # 发送请求
                    if next_url:
                        response = self.get(next_url)
                    else:
                        response = self.get(search_url, params=params)
                    
                    # 解析JSON响应
                    response_data = response.json()
                    
                    # 解析搜索结果
                    page_results = self._parse_search_results(response_data)
                    
                    if page_results:
                        all_results.extend(page_results)
                        logger.info(f"第 {current_page + 1} 页成功获取 {len(page_results)} 条结果")
                    else:
                        logger.warning(f"第 {current_page + 1} 页未获取到有效结果")
                    
                    # 检查分页信息
                    paging = response_data.get('paging', {})
                    is_end = paging.get('is_end', False)
                    next_url = paging.get('next')
                    
                    current_page += 1
                    
                    # 添加下载延迟
                    if current_page < max_pages and not is_end:
                        time.sleep(self.download_delay)
                        
                except json.JSONDecodeError as e:
                    logger.error(f"解析JSON响应失败，页码: {current_page + 1}，错误: {str(e)}")
                    break
                except Exception as e:
                    logger.error(f"爬取第 {current_page + 1} 页失败，错误: {str(e)}")
                    break
            
            logger.info(f"搜索完成，共获取 {len(all_results)} 条结果")
            return all_results
            
        except Exception as e:
            logger.error(f"搜索知乎内容失败，错误: {str(e)}")
            return all_results
    
    def _parse_search_results(self, response_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        解析搜索结果
        
        Args:
            response_data (Dict[str, Any]): API响应数据
        
        Returns:
            List[Dict[str, Any]]: 解析后的搜索结果列表
        """
        results = []
        
        try:
            data_list = response_data.get('data', [])
            
            for item in data_list:
                # 只处理类型为search_result的条目
                if item.get('type') != 'search_result':
                    continue
                
                try:
                    object_data = item.get('object', {})
                    
                    # 提取标题
                    title = object_data.get('title', '')
                    
                    # 提取内容（原始HTML）
                    content = object_data.get('content', '')
                    
                    # 提取答案链接
                    url = object_data.get('url', '')
                    
                    # 提取问题链接
                    question_data = object_data.get('question', {})
                    question_url = question_data.get('url', '') if question_data else ''
                    
                    # 提取问题ID
                    question_id = ''
                    if question_url:
                        try:
                            question_id = question_url.split('/')[-1].split('?')[0]
                        except Exception:
                            pass
                    
                    # 提取作者信息
                    author_data = object_data.get('author', {})
                    author_name = author_data.get('name', '') if author_data else ''
                    
                    # 提取点赞数
                    vote_up_count = object_data.get('voteup_count', 0)
                    
                    # 提取评论数
                    comment_count = object_data.get('comment_count', 0)
                    
                    # 提取创建时间
                    create_time = None
                    raw_create_time = object_data.get('created_time') or object_data.get('created')
                    if raw_create_time:
                        try:
                            # 尝试将时间戳转换为datetime对象
                            if isinstance(raw_create_time, (int, float)):
                                create_time = datetime.fromtimestamp(raw_create_time)
                            elif isinstance(raw_create_time, str):
                                # 尝试解析ISO格式的时间字符串
                                try:
                                    from dateutil import parser
                                    create_time = parser.parse(raw_create_time)
                                except Exception:
                                    # 如果解析失败，尝试其他格式
                                    try:
                                        create_time = datetime.strptime(raw_create_time, '%Y-%m-%d %H:%M:%S')
                                    except Exception:
                                        create_time = None
                        except Exception as e:
                            logger.warning(f"解析create_time失败: {str(e)}，使用当前时间")
                            create_time = None
                    
                    # 如果没有获取到create_time，使用当前时间
                    if not create_time:
                        create_time = datetime.now()
                    
                    # 清理HTML标签，提取纯文本
                    title_clean = self._clean_html_content(title)
                    content_clean = self._clean_html_content(content)
                    
                    # 构建结果字典，包含原始数据和清理后的文本
                    result = {
                        'title': title_clean,
                        'title_raw': title,
                        'content': content_clean,
                        'content_raw': content,
                        'url': url,
                        'question_url': question_url,
                        'question_id': question_id,
                        'author': author_name,
                        'vote_up_count': vote_up_count,
                        'comment_count': comment_count,
                        'crawl_time': datetime.now(),
                        'create_time': create_time
                    }
                    
                    results.append(result)
                    logger.debug(f"成功解析搜索结果: {title[:50]}...")
                    
                except Exception as e:
                    logger.error(f"解析单个搜索结果失败，错误: {str(e)}")
                    continue
            
            return results
            
        except Exception as e:
            logger.error(f"解析搜索结果失败，错误: {str(e)}")
            return results
