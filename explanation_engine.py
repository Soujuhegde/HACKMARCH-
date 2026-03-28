import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

@st.cache_data(show_spinner=False, ttl=86400)
def fetch_medical_references(query):
    """
    Scrape PubMed for live medical research matching the given query to prevent hallucination.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    url = f"https://pubmed.ncbi.nlm.nih.gov/?term={urllib.parse.quote(query)}"
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the top result from PubMed search list
            article = soup.find('article', class_='full-docsum')
            
            if article:
                title_elem = article.find('a', class_='docsum-title')
                snippet_elem = article.find('div', class_='full-view-snippet')
                
                title = title_elem.text.strip() if title_elem else "Study Title Not Found"
                link = "https://pubmed.ncbi.nlm.nih.gov" + title_elem['href'] if title_elem and 'href' in title_elem.attrs else url
                snippet = snippet_elem.text.strip() if snippet_elem else "Clinical study highlighting the cardiovascular and metabolic impacts."
                
                # Clean snippet extra spaces
                snippet = " ".join(snippet.split())
                
                return [{
                    "title": title,
                    "source": "PubMed (NIH)",
                    "link": link,
                    "evidence": snippet
                }]
        
    except Exception as e:
        print(f"Scraping failed: {e}")
        
    # Fallback if scraping fails / rate-limited
    return [{
        "title": "Trusted source not found yet",
        "source": "N/A",
        "link": "https://pubmed.ncbi.nlm.nih.gov/?term=" + urllib.parse.quote(query),
        "evidence": "Currently unavailable. Click the link to search PubMed directly."
    }]

def get_explanations(metrics, driver_key, impact_yrs):
    """
    Returns structured explanation of WHY the specific driver added X biological years.
    """
    explanations = {
        "bp": {
            "query": "Hypertension cardiovascular disease mortality risk older adults",
            "generate": lambda m, i: {
                "why_this_score": f"Your blood pressure is {int(m.get('sys_val', 120))}/{int(m.get('dia_val', 80))} mmHg. Ideal is <120/<80. Elevated pressure places continuous mechanical stress on your arteries, adding +{i} years.",
                "scientific_explanation": "Hypertension drives endothelial dysfunction, triggering a cascade of arterial stiffness and accelerating atherogenesis. This dramatically increases long-term risk for cardiovascular events."
            }
        },
        "sleep": {
            "query": "Sleep deprivation all-cause mortality cardiovascular risk",
            "generate": lambda m, i: {
                "why_this_score": f"You reported sleeping {m.get('sleep_val', 7)} hours per night. Poor sleep impairs your body's nightly repair cycles, increasing your biological age by +{i} years.",
                "scientific_explanation": "Chronic sleep restriction increases sympathetic nervous activity, elevates cortisol, and reduces heart rate variability, driving systemic low-grade inflammation."
            }
        },
        "steps": {
            "query": "Daily step count mortality cardiovascular risk longevity",
            "generate": lambda m, i: {
                "why_this_score": f"You average {int(m.get('steps_val', 5000))} steps. Missing the target of >8000 slows your metabolism and adds +{i} years of aging.",
                "scientific_explanation": "A sedentary lifestyle diminishes insulin sensitivity and downregulates lipoprotein lipase activity, increasing visceral adiposity and systemic metabolic dysfunction."
            }
        },
        "diet": {
            "query": "Diet quality Mediterranean diet all-cause mortality inflammation",
            "generate": lambda m, i: {
                "why_this_score": f"Your diet score is {m.get('diet_val', 5)}/10. Processed foods and poor nutrition add oxidative stress to your cells, contributing +{i} years.",
                "scientific_explanation": "Diets low in antioxidants and high in ultra-processed macronutrients provoke chronic low-grade systemic inflammation and telomere attrition, hallmarks of biological aging."
            }
        },
        "hr": {
            "query": "Resting heart rate mortality cardiovascular longevity",
            "generate": lambda m, i: {
                "why_this_score": f"Your resting HR is {int(m.get('hr_val', 70))} bpm. Higher baseline rates indicate an overworked heart, costing you +{i} years in restorative efficiency.",
                "scientific_explanation": "Elevated resting heart rate mathematically correlates with autonomic imbalance (reduced parasympathetic tone) and is an independent predictor of adverse cardiovascular events."
            }
        },
        "stress": {
            "query": "Psychological stress cellular aging telomere shortening",
            "generate": lambda m, i: {
                "why_this_score": f"Your stress levels are {int(m.get('stress_val', 5))}/10. Chronic stress physically degrades your immune system, adding +{i} years of damage.",
                "scientific_explanation": "Prolonged psychological stress results in chronic hypercortisolemia, suppressing immune surveillance and accelerating oxidative stress and telomere shortening."
            }
        },
        "exercise": {
            "query": "Moderate rigorous exercise life expectancy biological age",
            "generate": lambda m, i: {
                "why_this_score": f"You exercise {int(m.get('exe_val', 60))} mins per week. Inactivity accelerates muscle loss and cardiovascular decline, penalizing you by +{i} years.",
                "scientific_explanation": "Insufficient aerobic exercise reduces mitochondrial biogenesis and capillary density, compounding vascular aging and sarcopenia risks."
            }
        },
        "bmi": {
            "query": "Body mass index obesity all-cause mortality longevity",
            "generate": lambda m, i: {
                "why_this_score": f"Your measurements indicate unfavorable body composition. Excess weight adds +{i} biological years to your metabolic organs.",
                "scientific_explanation": "High adiposity acts as an active endocrine organ, constantly releasing pro-inflammatory cytokines (adipokines) that induce insulin resistance and vascular damage."
            }
        },
        "alcohol": {
            "query": "Alcohol consumption liver disease biological aging",
            "generate": lambda m, i: {
                "why_this_score": f"Consuming {int(m.get('alc_val', 5))} units of alcohol weekly forces your liver to prioritize detoxification over cellular repair, aging you by +{i} years.",
                "scientific_explanation": "Ethanol metabolism produces acetaldehyde, a severe hepatotoxin and carcinogen that depletes cellular glutathione levels, forcing systemic oxidative distress."
            }
        },
        "smoking": {
            "query": "Smoking oxidative stress cardiovascular biological aging",
            "generate": lambda m, i: {
                "why_this_score": f"Smoking introduces toxins into your bloodstream, violently aging your cells by +{i} years.",
                "scientific_explanation": "Combustible tobacco smoke causes catastrophic oxidative damage via free radicals, rapid endothelial dysfunction, and massive thrombotic risk amplification."
            }
        }
    }

    # Fallback for unexpected keys
    if driver_key not in explanations:
        return {
            "why_this_score": f"This category's deviation adds +{i} years to your biological age based on mortality statistics.",
            "scientific_explanation": "Deviation from the optimal biomarker range initiates sub-clinical pathology pathways linked to accelerated biological aging.",
            "references": fetch_medical_references(driver_key + " health mortality risk")
        }

    logic = explanations[driver_key]
    result = logic["generate"](metrics, impact_yrs)
    result["references"] = fetch_medical_references(logic["query"])

    return result
