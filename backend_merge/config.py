# config.py

# 人口配置
POPULATION_GROWTH_RATE = 0.01  # 人口年增长率，需要根据实际数据调整

# 心理健康配置
MENTAL_HEALTH_INCIDENT_RATE = 0.15  # 心理健康问题的年发生率，需要根据实际数据调整
PROGRESSION_RATES = {
    'mild_to_moderate': 0.1,   # 轻度到中度的进展率，需要根据实际数据调整
    'moderate_to_severe': 0.05  # 中度到重度的进展率，需要根据实际数据调整
}

# 资源配置
RESOURCE_ALLOCATION = {
    'mild': 0.4,      # 分配给轻度疾病治疗的资源比例，需要根据实际数据调整
    'moderate': 0.35, # 分配给中度疾病治疗的资源比例，需要根据实际数据调整
    'severe': 0.25    # 分配给重度疾病治疗的资源比例，需要根据实际数据调整
}

# 危机影响配置
CRISIS_FACTORS = {
    'unemployment_rise': 0.2,  # 失业率上升对心理健康的影响系数，需要根据实际数据调整
    'poverty_increase': 0.15,  # 贫困增加的影响系数，需要根据实际数据调整
    'refugee_influx': 0.1,     # 难民涌入的影响系数，需要根据实际数据调整
    'natural_disaster': 0.05,  # 自然灾害的影响系数，需要根据实际数据调整
    'pandemic': 0.3            # 疫情的影响系数，需要根据实际数据调整
}
