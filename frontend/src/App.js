import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [skills, setSkills] = useState("");
  const [results, setResults] = useState(null);

  const analyzeSkills = async () => {
    try {
      const skillArray = skills.split(",").map((s) => s.trim());

      const response = await axios.post("http://localhost:8000/analyze", {
        skills: skillArray,
      });

      setResults(response.data);
    } catch (error) {
      console.error("Error:", error);
      alert("Backend not running or CORS issue");
    }
  };

  return (
    <div className="container">
      <h1> Personal AI Economy Engine</h1>

      <input
        type="text"
        placeholder="Enter skills (e.g. Python, AI, React)"
        value={skills}
        onChange={(e) => setSkills(e.target.value)}
      />

      <button onClick={analyzeSkills}>Analyze</button>

      {results && (
        <div className="results">
          <h2>📈 Skill Analysis</h2>

          {results.analyzed_skills.map((skill, index) => (
            <div
              key={index}
              className={
                skill.skill === results.best_skill_to_focus
                  ? "card best"
                  : "card"
              }
            >
              <h3>
                {skill.skill}
                {skill.skill === results.best_skill_to_focus}
              </h3>

              <p> Demand Score: {skill.demand_score}</p>
              <div className="bar">
                <div
                  className="fill"
                  style={{ width: `${skill.demand_score * 100}%` }}
                ></div>
              </div>

              <p> Average Salary: ₹{skill.avg_salary}</p>
            </div>
          ))}

          <h3 className="total">
              Total Market Strength: {results.total_market_strength}
          </h3>
        </div>
      )}
    </div>
  );
}

export default App;