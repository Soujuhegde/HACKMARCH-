from fpdf import FPDF
from datetime import datetime

class HealthReport(FPDF):
    def __init__(self):
        super().__init__()
        self.set_margin(15)

    def header(self):
        # Logo placeholder or Title
        self.set_font("helvetica", "B", 20)
        self.set_text_color(6, 59, 150) # Clinical Blue
        self.cell(0, 10, "InsightCare Health Report", ln=True, align="C")
        self.set_font("helvetica", "I", 10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()} | AI-Generated Report | Confidential", align="C")

def create_pdf_report(metrics: dict, results: dict):
    pdf = HealthReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # 1. Patient Summary
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(6, 59, 150)
    pdf.cell(0, 10, "1. Patient Summary", ln=True)
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, f"Chronological Age: {metrics['age']} years", ln=True)
    pdf.cell(0, 8, f"BMI: {results['bio']['bmi']}", ln=True)
    pdf.cell(0, 8, f"Sleep: {metrics['sleep_hours']} hours/night", ln=True)
    pdf.ln(5)

    # 2. Prediction Results
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(6, 59, 150)
    pdf.cell(0, 10, "2. Prediction Results", ln=True)
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(0, 0, 0)
    
    bio_age = results['bio']['biological_age']
    age_delta = results['bio']['age_delta']
    status = "Older" if age_delta > 0 else "Younger"
    
    pdf.cell(0, 8, f"Biological Age: {bio_age} years ({status} by {abs(age_delta)} years)", ln=True)
    
    risk_level = "High" if results['bio']['cardio_risk'] > 60 or results['bio']['metabolic_risk'] > 60 else "Medium" if results['bio']['cardio_risk'] > 30 or results['bio']['metabolic_risk'] > 30 else "Low"
    pdf.cell(0, 8, f"Overall Risk Level: {risk_level}", ln=True)
    pdf.ln(5)

    # 3. Key Factors
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(6, 59, 150)
    pdf.cell(0, 10, "3. Key Risk Factors", ln=True)
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(0, 0, 0)
    
    pdf.multi_cell(180, 8, f"- Cardiovascular Risk Score: {results['bio']['cardio_risk']}/100\n"
                        f"- Metabolic Risk Score: {results['bio']['metabolic_risk']}/100\n"
                        f"- Cognitive Risk Score: {results['bio']['cognitive_risk']}/100")
    pdf.ln(5)

    # 4. Health Insights
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(6, 59, 150)
    pdf.cell(0, 10, "4. Health Insights", ln=True)
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(0, 0, 0)
    
    insight = (f"Your biological age is {bio_age}, which is {abs(age_delta)} years {'above' if age_delta > 0 else 'below'} "
               f"your chronological age. This trajectory is primarily influenced by your {'metabolic' if results['bio']['metabolic_risk'] > results['bio']['cardio_risk'] else 'cardiovascular'} profile.")
    pdf.multi_cell(180, 8, insight)
    pdf.ln(5)

    # 5. Recommendations
    pdf.set_font("helvetica", "B", 14)
    pdf.set_text_color(6, 59, 150)
    pdf.cell(0, 10, "5. Personalized Recommendations", ln=True)
    pdf.set_font("helvetica", "", 12)
    pdf.set_text_color(0, 0, 0)
    
    # We can pull these from ai_recs if available, or use defaults
    recs = [
        "Adopt a Mediterranean-style diet high in whole grains and lean proteins.",
        "Ensure at least 7-8 hours of quality sleep to reduce cognitive risk.",
        "Incorporate 150 minutes of moderate aerobic activity weekly."
    ]
    for rec in recs:
        pdf.set_x(15) # Ensure it starts at the left margin
        pdf.multi_cell(180, 8, f"- {rec}")
    pdf.ln(10)

    # 6. Disclaimer
    pdf.set_font("helvetica", "B", 10)
    pdf.set_text_color(200, 0, 0) # Red for disclaimer
    pdf.multi_cell(180, 5, "DISCLAIMER: This report is AI-generated and for informational purposes only. It is NOT a medical diagnosis or a substitute for professional medical advice. Always consult a qualified healthcare provider for medical concerns.", align="C")

    return pdf.output()
