from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

app = FastAPI(title="Personal AI Economy Engine")

# ✅ CORS (important for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load economic intelligence data
with open(r"C:\Users\kakki\OneDrive\Desktop\Hackathon\data\skill_market_data.json", "r") as f:
    skill_data = json.load(f)

class SkillRequest(BaseModel):
    skills: list[str]

@app.get("/")
def home():
    return {"message": "Personal AI Economy Engine is running 🚀"}

@app.post("/analyze")
def analyze_skills(request: SkillRequest):
    results = []
    total_score = 0
    best_skill = None
    highest_salary = 0

    for user_skill in request.skills:
        skill_clean = user_skill.strip()
        found = False

        # Case-insensitive matching
        for key in skill_data.keys():
            if key.lower() == skill_clean.lower():
                data = skill_data[key]
                demand = data["demand_score"]
                salary = data["avg_salary"]

                total_score += demand

                if salary > highest_salary:
                    highest_salary = salary
                    best_skill = key

                results.append({
                    "skill": key,
                    "demand_score": demand,
                    "avg_salary": salary
                })

                found = True
                break

        # If skill not found
        if not found:
            results.append({
                "skill": skill_clean,
                "demand_score": 0,
                "avg_salary": 0
            })

    return {
        "analyzed_skills": results,
        "total_market_strength": round(total_score, 4),
        "best_skill_to_focus": best_skill
    }

# ✅ NEW ROUTE (must be outside analyze function)
@app.get("/top-skills")
def top_skills():
    sorted_skills = sorted(
        skill_data.items(),
        key=lambda x: x[1]["demand_score"],
        reverse=True
    )[:10]

    return [
        {
            "skill": skill,
            "demand_score": data["demand_score"],
            "avg_salary": data["avg_salary"]
        }
        for skill, data in sorted_skills
    ]