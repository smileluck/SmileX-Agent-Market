"""
图表生成模块，用于生成各种数据可视化图表
"""
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.logger import setup_logger
from config.settings import PROJECT_ROOT

logger = setup_logger(__name__)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


class ChartGenerator:
    """
    图表生成器，用于生成各种数据可视化图表
    """
    
    def __init__(self):
        """
        初始化图表生成器
        """
        # 创建图表输出目录
        self.output_dir = os.path.join(PROJECT_ROOT, 'data', 'visualization')
        os.makedirs(self.output_dir, exist_ok=True)
        
        logger.info(f"图表生成器初始化成功，输出目录: {self.output_dir}")
    
    def generate_bar_chart(self, data: pd.DataFrame, x_col: str, y_col: str, 
                          title: str, filename: str, xlabel: str = None, 
                          ylabel: str = None, color: str = '#3498db') -> str:
        """
        生成柱状图
        
        Args:
            data (pd.DataFrame): 数据
            x_col (str): X轴列名
            y_col (str): Y轴列名
            title (str): 图表标题
            filename (str): 输出文件名
            xlabel (str, optional): X轴标签. Defaults to None.
            ylabel (str, optional): Y轴标签. Defaults to None.
            color (str, optional): 柱子颜色. Defaults to '#3498db'.
        
        Returns:
            str: 图表文件路径
        """
        try:
            plt.figure(figsize=(10, 6))
            plt.bar(data[x_col], data[y_col], color=color)
            plt.title(title, fontsize=14)
            plt.xlabel(xlabel if xlabel else x_col, fontsize=12)
            plt.ylabel(ylabel if ylabel else y_col, fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # 保存图表
            output_path = os.path.join(self.output_dir, filename)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"柱状图生成成功: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"生成柱状图失败，错误: {str(e)}")
            raise
    
    def generate_line_chart(self, data: pd.DataFrame, x_col: str, y_col: str, 
                           title: str, filename: str, xlabel: str = None, 
                           ylabel: str = None, color: str = '#e74c3c') -> str:
        """
        生成折线图
        
        Args:
            data (pd.DataFrame): 数据
            x_col (str): X轴列名
            y_col (str): Y轴列名
            title (str): 图表标题
            filename (str): 输出文件名
            xlabel (str, optional): X轴标签. Defaults to None.
            ylabel (str, optional): Y轴标签. Defaults to None.
            color (str, optional): 线条颜色. Defaults to '#e74c3c'.
        
        Returns:
            str: 图表文件路径
        """
        try:
            plt.figure(figsize=(10, 6))
            plt.plot(data[x_col], data[y_col], marker='o', color=color, linewidth=2)
            plt.title(title, fontsize=14)
            plt.xlabel(xlabel if xlabel else x_col, fontsize=12)
            plt.ylabel(ylabel if ylabel else y_col, fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            # 保存图表
            output_path = os.path.join(self.output_dir, filename)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"折线图生成成功: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"生成折线图失败，错误: {str(e)}")
            raise
    
    def generate_heatmap(self, data: pd.DataFrame, title: str, 
                        filename: str, annot: bool = True) -> str:
        """
        生成热力图
        
        Args:
            data (pd.DataFrame): 数据
            title (str): 图表标题
            filename (str): 输出文件名
            annot (bool, optional): 是否显示数值. Defaults to True.
        
        Returns:
            str: 图表文件路径
        """
        try:
            plt.figure(figsize=(10, 8))
            sns.heatmap(data, annot=annot, cmap='YlGnBu', fmt='.2f')
            plt.title(title, fontsize=14)
            plt.tight_layout()
            
            # 保存图表
            output_path = os.path.join(self.output_dir, filename)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"热力图生成成功: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"生成热力图失败，错误: {str(e)}")
            raise
    
    def generate_pie_chart(self, data: pd.DataFrame, values_col: str, 
                          names_col: str, title: str, filename: str) -> str:
        """
        生成饼图
        
        Args:
            data (pd.DataFrame): 数据
            values_col (str): 数值列名
            names_col (str): 名称列名
            title (str): 图表标题
            filename (str): 输出文件名
        
        Returns:
            str: 图表文件路径
        """
        try:
            plt.figure(figsize=(8, 8))
            plt.pie(data[values_col], labels=data[names_col], autopct='%1.1f%%', 
                   startangle=90, shadow=True)
            plt.title(title, fontsize=14)
            plt.axis('equal')
            plt.tight_layout()
            
            # 保存图表
            output_path = os.path.join(self.output_dir, filename)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"饼图生成成功: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"生成饼图失败，错误: {str(e)}")
            raise
    
    def generate_scatter_plot(self, data: pd.DataFrame, x_col: str, y_col: str, 
                            title: str, filename: str, xlabel: str = None, 
                            ylabel: str = None, color_col: str = None) -> str:
        """
        生成散点图
        
        Args:
            data (pd.DataFrame): 数据
            x_col (str): X轴列名
            y_col (str): Y轴列名
            title (str): 图表标题
            filename (str): 输出文件名
            xlabel (str, optional): X轴标签. Defaults to None.
            ylabel (str, optional): Y轴标签. Defaults to None.
            color_col (str, optional): 颜色分组列名. Defaults to None.
        
        Returns:
            str: 图表文件路径
        """
        try:
            plt.figure(figsize=(10, 6))
            
            if color_col:
                unique_colors = data[color_col].unique()
                colors = plt.cm.rainbow(range(len(unique_colors)))
                
                for i, color_value in enumerate(unique_colors):
                    subset = data[data[color_col] == color_value]
                    plt.scatter(subset[x_col], subset[y_col], color=colors[i], 
                               label=color_value, alpha=0.7)
                plt.legend()
            else:
                plt.scatter(data[x_col], data[y_col], color='#2ecc71', alpha=0.7)
            
            plt.title(title, fontsize=14)
            plt.xlabel(xlabel if xlabel else x_col, fontsize=12)
            plt.ylabel(ylabel if ylabel else y_col, fontsize=12)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            # 保存图表
            output_path = os.path.join(self.output_dir, filename)
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"散点图生成成功: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"生成散点图失败，错误: {str(e)}")
            raise
    
    def generate_interactive_bar_chart(self, data: pd.DataFrame, x_col: str, 
                                      y_col: str, title: str, filename: str) -> str:
        """
        生成交互式柱状图
        
        Args:
            data (pd.DataFrame): 数据
            x_col (str): X轴列名
            y_col (str): Y轴列名
            title (str): 图表标题
            filename (str): 输出文件名
        
        Returns:
            str: 图表文件路径
        """
        try:
            fig = px.bar(data, x=x_col, y=y_col, title=title)
            fig.update_layout(xaxis_tickangle=-45)
            
            # 保存图表
            output_path = os.path.join(self.output_dir, filename)
            fig.write_html(output_path)
            
            logger.info(f"交互式柱状图生成成功: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"生成交互式柱状图失败，错误: {str(e)}")
            raise
    
    def generate_radar_chart(self, data: pd.DataFrame, categories: list, 
                            values: list, title: str, filename: str) -> str:
        """
        生成雷达图
        
        Args:
            data (pd.DataFrame): 数据
            categories (list): 雷达图维度
            values (list): 对应维度的值
            title (str): 图表标题
            filename (str): 输出文件名
        
        Returns:
            str: 图表文件路径
        """
        try:
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name='评估值'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 10]
                    )),
                showlegend=True,
                title=title
            )
            
            # 保存图表
            output_path = os.path.join(self.output_dir, filename)
            fig.write_html(output_path)
            
            logger.info(f"雷达图生成成功: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"生成雷达图失败，错误: {str(e)}")
            raise
