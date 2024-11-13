# models/crisis_impact.py

from config import CRISIS_FACTORS

class CrisisImpactModel:
    def __init__(self, crisis_scenario):
        self.crisis_scenario = crisis_scenario

    def adjust_incident_rate(self, base_rate):
        """根据危机情景调整发生率。
        需要根据实际数据调整危机影响系数。
        """
        impact_factor = CRISIS_FACTORS.get(self.crisis_scenario, 0)
        return base_rate * (1 + impact_factor)
