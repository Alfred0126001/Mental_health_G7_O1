# models/population.py

from config import POPULATION_GROWTH_RATE

class PopulationModel:
    def __init__(self, initial_population):
        self.initial_population = initial_population

    def project_population(self, years):
        """预测未来几年的人口数量。"""
        return self.initial_population * ((1 + POPULATION_GROWTH_RATE) ** years)

    def get_demographics(self):
        """返回人口统计学信息（占位符方法）。
        需要使用实际的人口统计数据替换此方法的实现。
        """
        demographics = {
            'age_distribution': None,
            'gender_distribution': None,
            'socioeconomic_status': None
        }
        return demographics
