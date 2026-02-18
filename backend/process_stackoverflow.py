import pandas as pd
import json
from collections import defaultdict

# ---------- STEP 1: LOAD DATA ----------
file_path = r"C:\Users\kakki\OneDrive\Desktop\Hackathon\data\survey_results_public.csv"

print("Loading dataset...")
df = pd.read_csv(file_path, low_memory=False)

required_columns = [
    "LanguageHaveWorkedWith",
    "ConvertedCompYearly",
    "YearsCode"
]

df = df[required_columns]

# Drop rows with missing salary or skills
df = df.dropna(subset=["LanguageHaveWorkedWith", "ConvertedCompYearly"])

print("Dataset cleaned.")

# ---------- STEP 2: BUILD SKILL DEMAND + SALARY MODEL ----------

skill_salary = defaultdict(list)
skill_count = defaultdict(int)

for _, row in df.iterrows():
    skills = str(row["LanguageHaveWorkedWith"]).split(";")
    salary = row["ConvertedCompYearly"]

    for skill in skills:
        skill = skill.strip()
        if skill:
            skill_count[skill] += 1
            skill_salary[skill].append(salary)

print("Skill data aggregated.")

# ---------- STEP 3: CALCULATE DEMAND SCORE + AVG SALARY ----------

total_responses = len(df)

skill_market_data = {}

for skill in skill_count:
    demand_score = skill_count[skill] / total_responses
    avg_salary = sum(skill_salary[skill]) / len(skill_salary[skill])

    skill_market_data[skill] = {
        "demand_score": round(demand_score, 4),
        "avg_salary": round(avg_salary, 2)
    }

print("Economic intelligence created.")

# ---------- STEP 4: SAVE TO JSON ----------

output_path = r"C:\Users\kakki\OneDrive\Desktop\Hackathon\data\skill_market_data.json"

with open(output_path, "w") as f:
    json.dump(skill_market_data, f, indent=4)

print("✅ skill_market_data.json saved successfully!")
print("Phase 2 Completed 🚀")