# models/metrics.py

class MetricsCalculator:
    def calculate_waiting_time(self, resources, demand):
        """计算平均等待时间。
        需要根据实际的服务率和等待时间模型调整此方法。
        """
        # 防止除以零
        if resources == 0:
            return float('inf')
        return demand / resources

    def calculate_waiting_list_length(self, demand, service_rate):
        """计算等待名单长度。
        需要根据实际的服务率和等待名单模型调整此方法。
        """
        return max(demand - service_rate, 0)

    def calculate_severe_cases(self, cases):
        """返回重度病例数。"""
        return cases['severe']

    def calculate_relapse_rate(self, cases):
        """计算复发率（占位符方法）。
        需要根据实际的复发率数据调整。
        """
        relapse_rate = 0.1  # 假设复发率为10%，需要根据实际数据调整
        return relapse_rate * sum(cases.values())
