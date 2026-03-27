"""
THE TIME MACHINE — Health Future Simulator
Projects health score and risk trajectories over 10 years.
"""

from biological_age import calculate_biological_age, simulate_optimized_age


def project_health_trajectory(metrics: dict, years: int = 10) -> dict:
    current_result = calculate_biological_age(metrics)
    best_habit, label = find_best_single_improvement(metrics)
    optimized_result = simulate_optimized_age(metrics, best_habit)

    year_labels = list(range(0, years + 1))
    current_bio_ages, optimized_bio_ages = [], []
    current_cardio, optimized_cardio = [], []

    for y in range(years + 1):
        growth_factor = 1 + (current_result["age_delta"] / 100)
        current_bio_ages.append(round(current_result["biological_age"] + (y * growth_factor * 0.85), 1))

        improvement = current_result["biological_age"] - optimized_result["biological_age"]
        optimized_bio_ages.append(round(
            optimized_result["biological_age"] + (y * 0.75) - (improvement * min(y / 3, 1)), 1
        ))

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
        "best_habit_label": label,
        "age_savings": round(current_bio_ages[-1] - optimized_bio_ages[-1], 1),
        "cardio_risk_reduction": round(current_cardio[-1] - optimized_cardio[-1], 1),
        "current_result": current_result,
        "optimized_result": optimized_result,
    }


def find_best_single_improvement(metrics: dict) -> tuple:
    current_bio = calculate_biological_age(metrics)["biological_age"]
    candidates = [
        ({"sleep_hours": 8},         "Sleep 8 hours/night"),
        ({"steps_per_day": 10000},   "Walk 10,000 steps/day"),
        ({"stress_level": 4},        "Reduce stress to moderate"),
        ({"exercise_min_week": 150}, "Exercise 150 min/week"),
        ({"diet_quality": 8},        "Improve diet quality"),
        ({"alcohol_units_week": 3},  "Reduce alcohol intake"),
    ]
    best_change, best_label, best_gain = None, "", 0
    for change, label in candidates:
        gain = current_bio - simulate_optimized_age(metrics, change)["biological_age"]
        if gain > best_gain:
            best_gain, best_change, best_label = gain, change, label
    return best_change or {"sleep_hours": 8}, best_label or "Sleep 8 hours/night"


def calculate_life_expectancy_bonus(metrics: dict) -> dict:
    current = calculate_biological_age(metrics)
    best_habit, _ = find_best_single_improvement(metrics)
    optimized = simulate_optimized_age(metrics, best_habit)
    delta = current["biological_age"] - optimized["biological_age"]
    return {
        "current_bio_age": current["biological_age"],
        "optimized_bio_age": optimized["biological_age"],
        "bio_age_improvement": round(delta, 1),
        "estimated_life_years_gained": round(delta * 0.8, 1),
    }
