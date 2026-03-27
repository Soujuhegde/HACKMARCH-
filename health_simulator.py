"""
THE TIME MACHINE — Health Future Simulator
Projects health score and risk trajectories over 10 years.
"""

from biological_age import calculate_biological_age, simulate_optimized_age

def project_health_trajectory(metrics: dict, years: int = 10) -> dict:
    """
    Project health score trajectory for current vs optimized path.
    Returns data for Plotly charts.
    """
    current_result = calculate_biological_age(metrics)
    
    # Determine best single habit improvement
    best_habit, optimized_metrics = find_best_single_improvement(metrics)
    optimized_result = simulate_optimized_age(metrics, best_habit)
    
    year_labels = list(range(0, years + 1))
    
    # Current path: bio age grows faster than chronological due to habits
    current_bio_ages = []
    optimized_bio_ages = []
    current_cardio = []
    optimized_cardio = []
    
    for y in range(years + 1):
        # Current path: penalty compounds slightly each year
        growth_factor = 1 + (current_result["age_delta"] / 100)
        current_bio_age = current_result["biological_age"] + (y * growth_factor * 0.85)
        current_bio_ages.append(round(current_bio_age, 1))
        
        # Optimized path: improvement takes effect
        improvement = (current_result["biological_age"] - optimized_result["biological_age"])
        optim_bio_age = optimized_result["biological_age"] + (y * 0.75) - (improvement * min(y / 3, 1))
        optimized_bio_ages.append(round(optim_bio_age, 1))
        
        # Risk trajectories
        cardio_growth = 1 + (current_result["cardio_risk"] / 1000)
        current_cardio.append(min(100, round(current_result["cardio_risk"] * (cardio_growth ** y), 1)))
        optimized_cardio.append(min(100, round(current_result["cardio_risk"] * 0.75 * (1.008 ** y), 1)))
    
    return {
        "years": year_labels,
        "current_bio_ages": current_bio_ages,
        "optimized_bio_ages": optimized_bio_ages,
        "current_cardio_risk": current_cardio,
        "optimized_cardio_risk": optimized_cardio,
        "best_habit_change": best_habit,
        "best_habit_label": optimized_metrics,
        "age_savings": round(current_bio_ages[-1] - optimized_bio_ages[-1], 1),
        "cardio_risk_reduction": round(current_cardio[-1] - optimized_cardio[-1], 1),
        "current_result": current_result,
        "optimized_result": optimized_result,
    }

def find_best_single_improvement(metrics: dict) -> tuple:
    """Find the single habit change with biggest biological age improvement."""
    current = calculate_biological_age(metrics)
    current_bio = current["biological_age"]
    
    candidates = [
        ({"sleep_hours": 8}, "Sleep 8 hours/night"),
        ({"steps_per_day": 10000}, "Walk 10,000 steps/day"),
        ({"stress_level": 4}, "Reduce stress to moderate"),
        ({"exercise_min_week": 150}, "Exercise 150 min/week"),
        ({"diet_quality": 8}, "Improve diet quality"),
        ({"alcohol_units_week": 3}, "Reduce alcohol intake"),
    ]
    
    best_change = None
    best_label = ""
    best_improvement = 0
    
    for change, label in candidates:
        # Only suggest change if it's actually an improvement
        current_val = metrics.get(list(change.keys())[0])
        new_val = list(change.values())[0]
        
        result = simulate_optimized_age(metrics, change)
        improvement = current_bio - result["biological_age"]
        
        if improvement > best_improvement:
            best_improvement = improvement
            best_change = change
            best_label = label
    
    return best_change or {"sleep_hours": 8}, best_label or "Sleep 8 hours/night"

def calculate_life_expectancy_bonus(metrics: dict) -> dict:
    """Estimate potential life years gained from habit optimization."""
    current = calculate_biological_age(metrics)
    best_habit, _ = find_best_single_improvement(metrics)
    optimized = simulate_optimized_age(metrics, best_habit)
    
    delta = current["biological_age"] - optimized["biological_age"]
    # Research-backed: each year of biological age difference ≈ 0.8 years life expectancy
    life_years_gained = round(delta * 0.8, 1)
    
    return {
        "current_bio_age": current["biological_age"],
        "optimized_bio_age": optimized["biological_age"],
        "bio_age_improvement": round(delta, 1),
        "estimated_life_years_gained": life_years_gained,
    }
