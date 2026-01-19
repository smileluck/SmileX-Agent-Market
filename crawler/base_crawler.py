"""
基础爬虫类，定义通用爬虫功能
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from utils.logger import setup_logger

logger = setup_logger(__name__)


class BaseCrawler:
    """
    基础爬虫类，提供通用的爬虫功能
    """
    
    def __init__(self, base_url: str, user_agent: str, cookie: str, max_retries: int = 3,
                 timeout: int = 10, download_delay: float = 1.0):
        """
        初始化基础爬虫
        
        Args:
            base_url (str): 基础URL
            user_agent (str): User-Agent
            cookie (str): Cookie
            max_retries (int, optional): 最大重试次数. Defaults to 3.
            timeout (int, optional): 请求超时时间. Defaults to 10.
            download_delay (float, optional): 下载延迟. Defaults to 1.0.
        """
        self.base_url = base_url
        self.user_agent = user_agent
        self.cookie = cookie
        self.max_retries = max_retries
        self.timeout = timeout
        self.download_delay = download_delay
        
        # 初始化session
        self.session = self._init_session()
    
    def _init_session(self) -> requests.Session:
        """
        初始化requests session，配置重试机制和headers
        
        Returns:
            requests.Session: 配置好的session实例
        """
        session = requests.Session()
        
        # 配置重试策略
        retry_strategy = Retry(
            total=self.max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1,
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        
        # 设置默认headers
        session.headers.update({
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": self.cookie
        })
        
        return session
    
    def get(self, url: str, params: dict = None, headers: dict = None,
           **kwargs) -> requests.Response:
        """
        发送GET请求
        
        Args:
            url (str): 请求URL
            params (dict, optional): 请求参数. Defaults to None.
            headers (dict, optional): 请求头. Defaults to None.
            **kwargs: 其他请求参数
        
        Returns:
            requests.Response: 请求响应
        
        Raises:
            requests.exceptions.RequestException: 请求异常
        """
        try:
            response = self.session.get(
                url, params=params, headers=headers, timeout=self.timeout, **kwargs
            )
            response.raise_for_status()
            logger.info(f"GET请求成功: {url}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"GET请求失败: {url}, 错误: {str(e)}")
            raise
    
    def post(self, url: str, data: dict = None, json: dict = None,
            headers: dict = None, **kwargs) -> requests.Response:
        """
        发送POST请求
        
        Args:
            url (str): 请求URL
            data (dict, optional): 请求数据. Defaults to None.
            json (dict, optional): JSON数据. Defaults to None.
            headers (dict, optional): 请求头. Defaults to None.
            **kwargs: 其他请求参数
        
        Returns:
            requests.Response: 请求响应
        
        Raises:
            requests.exceptions.RequestException: 请求异常
        """
        try:
            response = self.session.post(
                url, data=data, json=json, headers=headers, timeout=self.timeout, **kwargs
            )
            response.raise_for_status()
            logger.info(f"POST请求成功: {url}")
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"POST请求失败: {url}, 错误: {str(e)}")
            raise
    
    def close(self):
        """
        关闭session
        """
        self.session.close()
        logger.info("Session已关闭")
