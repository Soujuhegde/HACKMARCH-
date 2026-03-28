import streamlit as st
import json
from explanation_engine import fetch_medical_references

def explain_projection(metrics, sim_metrics, current_bio_age, optimized_bio_age):
    """
    Analyzes the user's habits and calculates the epidemiological reasoning and PubMed research
    to fully justify their 10-year projected outcomes and time saved.
    """
    time_saved = round(current_bio_age - optimized_bio_age, 1)
    
    # Calculate what changed
    changes = []
    if float(sim_metrics['sleep_hours']) > float(metrics['sleep_hours']):
        changes.append("sleep")
    if int(sim_metrics['steps_per_day']) > int(metrics['steps_per_day']):
        changes.append("daily steps")
    if int(sim_metrics['exercise_min_week']) > int(metrics['exercise_min_week']):
        changes.append("physical activity")
    if int(sim_metrics['stress_level']) < int(metrics['stress_level']):
        changes.append("stress reduction")
    if int(sim_metrics['diet_quality']) > int(metrics['diet_quality']):
        changes.append("dietary quality")

    if not changes:
        changes_str = "maintaining your current baseline"
        query_topic = "lifestyle unchanged mortality risk"
    else:
        changes_str = "improving " + ", ".join(changes)
        query_topic = f"impact of {changes[0]} on biological aging and life expectancy"

    # Box 1: Current Path
    current_path = {
        "explanation": f"If you keep up your current daily habits for the next 10 years, your body will age to {current_bio_age} biological years.",
        "reasoning": "Not improving your diet, exercise, or stress levels means your body and cells will continue to age at their normal, everyday pace.",
        "scientific_basis": "Large studies show that ignoring healthy lifestyle habits directly speeds up the aging process and increases the risk of early health issues.",
        "references": fetch_medical_references("cellular aging sedentary lifestyle unchanged mortality risk")
    }
    
    # Box 2: Simulated Path
    simulated_path = {
        "explanation": f"By making healthier choices ({changes_str}), your new projected biological age drops nicely to {optimized_bio_age}.",
        "reasoning": "These changes help your body reduce hidden inflammation and improve how your cells repair themselves, physically slowing down your biological clock.",
        "scientific_basis": "Medical research confirms that even small, consistent improvements in sleep, nutrition, and daily movement can significantly protect your heart and help you live a much healthier life.",
        "references": fetch_medical_references(query_topic)
    }
    
    # Box 3: Time Saved
    time_saved_obj = {
        "explanation": f"Your healthier choices have the potential to win back {time_saved} biological years.",
        "reasoning": "Building good habits over a 10-year period removes a huge amount of stress from your organs, allowing them to stay strong and function like they belong to a younger person.",
        "scientific_basis": "Global clinical studies prove that combining multiple healthy behaviors—like moving more and sleeping better—can actually reverse biological damage and add real, active years to your life expectancy.",
        "references": fetch_medical_references("healthy lifestyle interventions adding years to life expectancy longevity")
    }
    
    return {
        "current_path": current_path,
        "simulated_path": simulated_path,
        "time_saved": time_saved_obj
    }
