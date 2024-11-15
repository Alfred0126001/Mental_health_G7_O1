from flask import Flask, render_template, request
import numpy as np
from math import factorial
import datetime

# 配置部分
POPULATION_GROWTH_RATE_PER_DAY = 0.01 / 365  # 每日人口增长率
MENTAL_HEALTH_STATES = ['Healthy', 'Mild', 'Moderate', 'Severe']  # 四种状态
STATE_INDEX = {state: idx for idx, state in enumerate(MENTAL_HEALTH_STATES)}
TRANSITION_MATRIX = {
    'peace': [
        [0.95, 0.03, 0.01, 0.01],  # Healthy
        [0.00, 0.85, 0.10, 0.05],  # Mild
        [0.00, 0.00, 0.80, 0.20],  # Moderate
        [0.10, 0.20, 0.20, 0.50]   # Severe
    ],
    'crisis': [
        [0.85, 0.10, 0.05, 0.00],  # Healthy
        [0.00, 0.75, 0.15, 0.10],  # Mild
        [0.00, 0.00, 0.70, 0.30],  # Moderate
        [0.10, 0.20, 0.20, 0.50]   # Severe
    ]
}
RESOURCE_ALLOCATION = {'Mild': 0.4, 'Moderate': 0.35, 'Severe': 0.25}
CRISIS_FACTORS = {
    'unemployment_rise': 0.2,
    'poverty_increase': 0.15,
    'refugee_influx': 0.1,
    'natural_disaster': 0.05,
    'pandemic': 0.3,
}

# 服务相关配置
SERVERS = 38  # 心理医生数量
SERVICE_RATE_PER_SERVER_PER_DAY = 10  # 每个服务台每天处理的人数
TOTAL_SERVICE_RATE = SERVICE_RATE_PER_SERVER_PER_DAY * SERVERS  # 总服务率（μ）

# 模型
class PopulationModel:
    def __init__(self, initial_population, age_distribution=None, gender_distribution=None):
        self.initial_population = initial_population
        self.age_distribution = age_distribution  # 年龄分布（可选）
        self.gender_distribution = gender_distribution  # 性别分布（可选）

    def project_population(self, days):
        """预测未来几天的人口"""
        return self.initial_population * ((1 + POPULATION_GROWTH_RATE_PER_DAY) ** days)

class MentalHealthModel:
    def __init__(self, initial_distribution, crisis_scenario='peace'):
        """初始化状态分布和转移矩阵"""
        self.state_distribution = np.zeros(len(MENTAL_HEALTH_STATES))
        for state, count in initial_distribution.items():
            self.state_distribution[STATE_INDEX[state]] = count
        self.transition_matrix = TRANSITION_MATRIX[crisis_scenario]
        self.crisis_scenario = crisis_scenario

    def calculate_prevalence(self, incident_rate=0.1):
        """更新健康状态的发病率"""
        new_cases = self.state_distribution[STATE_INDEX['Healthy']] * incident_rate
        self.state_distribution[STATE_INDEX['Healthy']] -= new_cases
        self.state_distribution[STATE_INDEX['Mild']] += new_cases

    def simulate_progression(self, steps=1):
        """使用马尔可夫链模拟疾病进展"""
        for _ in range(steps):
            self.state_distribution = np.dot(self.state_distribution, self.transition_matrix)
        # 返回各状态的病例数
        return {state: self.state_distribution[STATE_INDEX[state]] for state in MENTAL_HEALTH_STATES}

class CarePathwaysModel:
    def allocate_resources(self, cases, resource_allocation=None):
        """根据疾病阶段分配资源，可以在资源调整时动态调用"""
        allocation = resource_allocation if resource_allocation else RESOURCE_ALLOCATION
        return {
            state: cases.get(state, 0) * allocation.get(state, 0)
            for state in ['Mild', 'Moderate', 'Severe']
        }

class SimulationMetrics:
    def __init__(self):
        self.total_waiting_time = 0.0
        self.total_customers = 0
        self.waiting_times = []
        self.queue_lengths = []
        self.max_queue_length = 0

    def record_day(self, waiting_time, queue_length):
        self.waiting_times.append(waiting_time)
        self.queue_lengths.append(queue_length)
        self.total_waiting_time += waiting_time
        self.total_customers += 1
        if queue_length > self.max_queue_length:
            self.max_queue_length = queue_length

    def get_average_waiting_time(self):
        return self.total_waiting_time / self.total_customers if self.total_customers > 0 else 0.0

    def get_average_queue_length(self):
        return np.mean(self.queue_lengths) if self.queue_lengths else 0.0

    def get_max_queue_length(self):
        return self.max_queue_length

class MetricsCalculator:
    @staticmethod
    def calculate_severe_cases(cases):
        """返回重症病例数"""
        return cases.get('Severe', 0)

    @staticmethod
    def calculate_relapse_rate(cases, time_step=1):
        """动态复发率模型"""
        relapse_rate = lambda t: 0.1 * np.exp(-0.05 * t)
        total_cases = sum(cases.values())
        return relapse_rate(time_step) * total_cases

# Flask应用
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 获取用户输入的初始分布
        try:
            initial_distribution = {
                'Healthy': int(request.form.get('healthy', 800000)),
                'Mild': int(request.form.get('mild', 100000)),
                'Moderate': int(request.form.get('moderate', 80000)),
                'Severe': int(request.form.get('severe', 20000)),
            }
        except ValueError:
            return render_template('index.html', error="请输入有效的整数值。")

        crisis_scenario = request.form.get('crisis_scenario', 'peace')

        # 计算总人口
        total_population = sum(initial_distribution.values())

        # 初始化人口模型并预测未来1天的人口
        population_model = PopulationModel(initial_population=total_population)
        projected_population = population_model.project_population(days=1)

        # 计算基准到达率 λ = population * 0.15 / 365
        base_lambda = projected_population * 0.15 / 365  # 15% 的人口需求分摊到每日

        # 根据危机状态调整到达率
        if crisis_scenario == 'crisis':
            total_crisis_factor = sum(CRISIS_FACTORS.values())  # 总危机因子
            lambda_rate = base_lambda * (1 + total_crisis_factor)
        else:
            lambda_rate = base_lambda  # 和平状态下的到达率

        # 初始化心理健康模型并设置危机场景
        mental_health_model = MentalHealthModel(initial_distribution, crisis_scenario)
        mental_health_model.calculate_prevalence()

        # 模拟疾病进展
        cases = mental_health_model.simulate_progression(steps=1)

        # 资源分配模型
        care_model = CarePathwaysModel()
        resources = care_model.allocate_resources(cases)

        # 总服务率 μ
        mu = SERVICE_RATE_PER_SERVER_PER_DAY  # 单个服务器的日服务率

        # 服务器数量 c
        c = SERVERS

        # 离散事件模拟
        simulation_days = 365  # 模拟一年
        metrics = SimulationMetrics()
        queue = 0  # 初始队列长度

        for day in range(1, simulation_days + 1):
            # 确定当天是否为周末
            # 假设模拟从周一开始
            day_of_week = (day - 1) % 7  # 0: 周一, 5: 周六, 6: 周日
            is_weekend = day_of_week >= 5  # 周六和周日

            # 当天的服务率
            if is_weekend:
                daily_mu = 0
            else:
                daily_mu = mu * resources.get('Mild', 0) + mu * resources.get('Moderate', 0) + mu * resources.get('Severe', 0)
                # 这里假设资源分配比例影响实际服务率
                # 如果需要更复杂的服务率调整，请根据实际情况修改

            # 当天的到达率
            arrivals = np.random.poisson(lambda_rate)

            # 更新队列
            if daily_mu > 0:
                served = min(queue, daily_mu)
                queue -= served
            else:
                served = 0  # 周末没有服务

            queue += arrivals

            # 记录当天的等待时间和队列长度
            waiting_time = queue / c / mu if c * mu > 0 else 0
            metrics.record_day(waiting_time, queue)

        # 计算平均等待时间和等待名单长度
        average_waiting_time = metrics.get_average_waiting_time()
        average_queue_length = metrics.get_average_queue_length()
        max_queue_length = metrics.get_max_queue_length()

        # 计算重度病例数和复发病例数
        metrics_calculator = MetricsCalculator()
        severe_cases = metrics_calculator.calculate_severe_cases(cases)
        relapse_cases = metrics_calculator.calculate_relapse_rate(cases)

        # 返回结果
        results = {
            'average_waiting_time': f"{average_waiting_time:.2f} 天",
            'average_queue_length': f"{average_queue_length:.0f} 人",
            'max_queue_length': f"{max_queue_length:.0f} 人",
            'severe_cases': f"{severe_cases:.0f} 人",
            'relapse_cases': f"{relapse_cases:.0f} 人"
        }
        return render_template('index.html', results=results)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)