# app.py

from flask import Flask, render_template, request
from models import PopulationModel, MentalHealthModel, CarePathwaysModel, CrisisImpactModel, MetricsCalculator
from config import MENTAL_HEALTH_INCIDENT_RATE

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 获取用户输入的参数
        initial_population = int(request.form.get('initial_population', 1000000))
        years = int(request.form.get('years', 1))
        crisis_scenario = request.form.get('crisis_scenario', 'pandemic')

        # 人口模型
        population_model = PopulationModel(initial_population)
        projected_population = population_model.project_population(years=years)

        # 心理健康模型
        mental_health_model = MentalHealthModel(projected_population)
        base_prevalence = mental_health_model.calculate_prevalence()

        # 危机影响
        crisis_model = CrisisImpactModel(crisis_scenario=crisis_scenario)
        adjusted_incident_rate = crisis_model.adjust_incident_rate(MENTAL_HEALTH_INCIDENT_RATE)
        adjusted_prevalence = mental_health_model.calculate_prevalence(adjusted_incident_rate)

        # 模拟疾病进展
        cases = mental_health_model.simulate_progression(adjusted_prevalence)

        # 护理路径和资源分配
        care_model = CarePathwaysModel()
        resources = care_model.allocate_resources(cases)

        # 计算指标
        metrics_calculator = MetricsCalculator()
        total_resources = sum(resources.values())
        total_demand = sum(cases.values())
        waiting_time = metrics_calculator.calculate_waiting_time(resources=total_resources, demand=total_demand)
        waiting_list_length = metrics_calculator.calculate_waiting_list_length(demand=total_demand, service_rate=total_resources)
        severe_cases = metrics_calculator.calculate_severe_cases(cases)
        relapse_cases = metrics_calculator.calculate_relapse_rate(cases)

        # 将结果传递给前端
        results = {
            'waiting_time': f"{waiting_time:.2f}",
            'waiting_list_length': f"{waiting_list_length:.0f}",
            'severe_cases': f"{severe_cases:.0f}",
            'relapse_cases': f"{relapse_cases:.0f}"
        }

        return render_template('index.html', results=results)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
