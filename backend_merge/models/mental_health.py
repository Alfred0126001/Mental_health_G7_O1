# models/mental_health.py

from config import MENTAL_HEALTH_INCIDENT_RATE, PROGRESSION_RATES

class MentalHealthModel:
    def __init__(self, population):
        self.population = population

    def calculate_prevalence(self, incident_rate=None):
        """计算心理健康问题的患病人数。"""
        if incident_rate is None:
            incident_rate = MENTAL_HEALTH_INCIDENT_RATE
        return self.population * incident_rate

    def simulate_progression(self, prevalence):
        """模拟疾病在不同严重程度之间的进展。
        返回一个字典，包括轻度、中度和重度病例数。
        """
        mild = prevalence * (1 - PROGRESSION_RATES['mild_to_moderate'])
        moderate = prevalence * PROGRESSION_RATES['mild_to_moderate'] * (1 - PROGRESSION_RATES['moderate_to_severe'])
        severe = prevalence * PROGRESSION_RATES['moderate_to_severe']
        return {'mild': mild, 'moderate': moderate, 'severe': severe}
