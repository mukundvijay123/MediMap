import random
import pandas as pd

# Define departments
departments = [
    "Cardiac", "Orthopedic", "Neurology", "General Medicine",
    "Pediatrics", "Dermatology", "Ophthalmology", "ENT", 
    "Gastroenterology", "Oncology", "Pulmonology", "Urology",
    "Psychiatry", "Endocrinology", "Gynecology", "Nephrology",
    "Infectious Diseases", "Traumatology", "Hematology", "Rheumatology"
]

# Define sample phrases for each department
report_templates = {
    "Cardiac": [
        "Patient complains of severe chest pain and shortness of breath.",
        "High blood pressure and irregular heartbeat detected.",
        "Heart attack symptoms observed, needs immediate attention."
    ],
    "Orthopedic": [
        "Fractured leg from a road accident.",
        "Shoulder dislocation due to a fall.",
        "Severe back pain reported after lifting heavy weight."
    ],
    "Neurology": [
        "Head injury with dizziness and blurred vision.",
        "Stroke symptoms including numbness and weakness on one side.",
        "Patient reports frequent migraines and memory loss."
    ],
    "General Medicine": [
        "Fever and persistent cough for the past week.",
        "Severe dehydration and fatigue symptoms.",
        "Abdominal pain with signs of infection."
    ],
    "Pediatrics": [
        "Child with high fever and difficulty breathing.",
        "Patient complains of ear pain and throat infection.",
        "Vomiting and signs of dehydration observed in a young child."
    ],
    "Dermatology": [
        "Rash and severe itching after allergic reaction.",
        "Patient reports sudden hair loss and brittle nails.",
        "Chronic skin condition with redness and scaling."
    ],
    "Ophthalmology": [
        "Blurred vision and redness in the left eye.",
        "Patient reports difficulty seeing at night.",
        "Cataract symptoms observed in both eyes."
    ],
    "ENT": [
        "Severe ear pain with loss of hearing.",
        "Persistent sore throat and swollen tonsils.",
        "Nasal congestion and sinus infection reported."
    ],
    "Gastroenterology": [
        "Patient reports severe abdominal pain and nausea.",
        "Chronic constipation and bloating symptoms observed.",
        "Signs of jaundice and liver dysfunction detected."
    ],
    "Oncology": [
        "Lump in breast detected during physical examination.",
        "Unexplained weight loss and fatigue symptoms reported.",
        "Persistent cough with traces of blood observed."
    ],
    "Pulmonology": [
        "Shortness of breath and wheezing diagnosed as asthma.",
        "Chronic cough with signs of lung infection.",
        "Patient diagnosed with pneumonia after X-ray."
    ],
    "Urology": [
        "Patient reports difficulty in urination and back pain.",
        "Signs of kidney stones detected during ultrasound.",
        "Frequent urinary tract infections with fever."
    ],
    "Psychiatry": [
        "Patient reports severe anxiety and trouble sleeping.",
        "Symptoms of depression with feelings of hopelessness.",
        "Frequent panic attacks and inability to focus at work."
    ],
    "Endocrinology": [
        "High blood sugar levels indicate diabetes.",
        "Patient reports unexplained weight gain and fatigue.",
        "Signs of thyroid dysfunction observed during examination."
    ],
    "Gynecology": [
        "Patient reports irregular menstrual cycles and abdominal pain.",
        "Severe pelvic pain diagnosed as ovarian cyst.",
        "Pregnancy-related complications detected during routine checkup."
    ],
    "Nephrology": [
        "Patient diagnosed with chronic kidney disease.",
        "Swelling in legs and face with high creatinine levels.",
        "Symptoms of kidney infection with fever and back pain."
    ],
    "Infectious Diseases": [
        "Patient diagnosed with dengue fever after blood test.",
        "High fever and chills indicate malaria infection.",
        "Tuberculosis symptoms with persistent cough and weight loss."
    ],
    "Traumatology": [
        "Severe head injury from a car crash.",
        "Compound fracture observed in right leg.",
        "Multiple injuries caused by a fall from height."
    ],
    "Hematology": [
        "Patient diagnosed with anemia due to low hemoglobin levels.",
        "Symptoms of blood clotting disorder detected.",
        "Unusual bruising and fatigue indicate leukemia."
    ],
    "Rheumatology": [
        "Patient reports joint pain and stiffness in the morning.",
        "Diagnosed with rheumatoid arthritis after tests.",
        "Chronic swelling and redness in multiple joints."
    ]
}

# Generate synthetic accident reports
def generate_synthetic_reports(num_reports=100):
    reports = []
    for _ in range(num_reports):
        department = random.choice(departments)
        report = random.choice(report_templates[department])
        reports.append({"report": report, "department": department})
    return reports

# Create synthetic data
synthetic_data = generate_synthetic_reports(200)  # Generate 200 reports

# Save to CSV
df = pd.DataFrame(synthetic_data)
df.to_csv("synthetic_accident_reports.csv", index=False)
print("Synthetic accident reports generated and saved to 'synthetic_accident_reports.csv'")
