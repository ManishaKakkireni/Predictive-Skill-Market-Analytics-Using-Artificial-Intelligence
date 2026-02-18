import json

# Load economic intelligence data
with open("../data/skill_market_data.json", "r") as f:
    skill_data = json.load(f)


def analyze_skills(user_skills):
    total_score = 0
    best_skill = None
    highest_salary = 0

    results = []

    for skill in user_skills:
        if skill in skill_data:
            data = skill_data[skill]
            demand = data["demand_score"]
            salary = data["avg_salary"]

            total_score += demand

            if salary > highest_salary:
                highest_salary = salary
                best_skill = skill

            results.append({
                "skill": skill,
                "demand_score": demand,
                "avg_salary": salary
            })

    return {
        "analyzed_skills": results,
        "total_market_strength": round(total_score, 4),
        "best_skill_to_focus": best_skill
    }


# Test Run
if __name__ == "__main__":
    test_skills = ["Python", "JavaScript"]
    report = analyze_skills(test_skills)
    print(report)