import React, { useState } from "react";
import "./App.css";
import { PieChart, Pie, Cell, Tooltip, Legend } from "recharts";

// Color palette for pie chart slices
const COLORS = [
  "#8884d8", "#82ca9d", "#ffc658", "#ff7f50", "#aqua",
  "#dda0dd", "#90ee90", "#ff69b4", "#87cefa", "#ffb6c1",
  "#cd5c5c", "#40e0d0", "#ff6347", "#8a2be2", "#00ced1",
  "#d2691e", "#6495ed", "#db7093", "#ff8c00", "#20b2aa"
];

// Predefined sample suggestions for autocomplete
const SUGGESTIONS = [
  "Show me diabetic patients over 60",
  "List asthma patients over 70",
  "Get cancer patients over 75",
  "Find flu patients older than 50",
  "Patients with hypertension over 65"
];

function App() {
  // State for query input, backend response, suggestion filtering, and result preservation
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [filteredSuggestions, setFilteredSuggestions] = useState([]);
  const [fullResults, setFullResults] = useState([]);

  // Submits query to the backend API and processes the response
  const handleSubmit = async (customQuery = null) => {
    const input = customQuery || query;
    try {
      const res = await fetch("http://localhost:5000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: input })
      });
      const data = await res.json();
      setResponse(data);                // Current view
      setFullResults(data.results);     // Backup for filters
      setQuery(input);                  // Update input field
      setFilteredSuggestions([]);       // Hide suggestions after submit
    } catch (err) {
      console.error("Error:", err);
      alert("Failed to fetch data from backend.");
    }
  };

  // Groups patients into age ranges for pie chart
  const groupByAgeRange = (patients) => {
    const ranges = { "50–59": 0, "60–69": 0, "70–79": 0, "80+": 0 };
    patients.forEach((p) => {
      if (p.age >= 50 && p.age <= 59) ranges["50–59"]++;
      else if (p.age >= 60 && p.age <= 69) ranges["60–69"]++;
      else if (p.age >= 70 && p.age <= 79) ranges["70–79"]++;
      else if (p.age >= 80) ranges["80+"]++;
    });
    return Object.entries(ranges)
      .filter(([_, count]) => count > 0)
      .map(([range, count]) => ({ name: range, value: count }));
  };

  return (
    <div style={{ fontFamily: "Segoe UI, sans-serif", backgroundColor: "#f9f9fb", minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      
      {/* Header */}
      <header style={{ backgroundColor: "#007bff", color: "white", padding: "20px 0", textAlign: "center", boxShadow: "0 2px 8px rgba(0,0,0,0.1)" }}>
        <h1 style={{ margin: 0, fontSize: "24px" }}>🩺 AI on FHIR Dashboard</h1>
        <p style={{ margin: 0, fontSize: "14px" }}>FHIR-powered patient insights from natural language queries</p>
      </header>

      {/* Main Content */}
      <main style={{ flex: 1, padding: "40px 20px" }}>
        <div style={{ maxWidth: "960px", margin: "0 auto", backgroundColor: "#fff", padding: "30px", borderRadius: "12px", boxShadow: "0 4px 12px rgba(0,0,0,0.05)" }}>
          
          {/* Query Input */}
          <input
            type="text"
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);
              setFilteredSuggestions(
                SUGGESTIONS.filter(s =>
                  s.toLowerCase().includes(e.target.value.toLowerCase())
                )
              );
            }}
            placeholder="e.g., Show me diabetic patients over 60"
            style={{
              width: "100%",
              padding: "12px",
              fontSize: "16px",
              marginBottom: "10px",
              border: "1px solid #ccc",
              borderRadius: "6px"
            }}
          />

          {/* Autocomplete Suggestions */}
          {filteredSuggestions.length > 0 && (
            <div style={{ marginBottom: "20px" }}>
              {filteredSuggestions.map((s, i) => (
                <div
                  key={i}
                  onClick={() => handleSubmit(s)}
                  style={{
                    padding: "10px",
                    backgroundColor: "#f5f5f5",
                    border: "1px solid #ddd",
                    borderRadius: "4px",
                    marginBottom: "5px",
                    cursor: "pointer"
                  }}
                >
                  {s}
                </div>
              ))}
            </div>
          )}

          {/* Run Query Button */}
          <button
            onClick={() => handleSubmit()}
            style={{
              width: "100%",
              padding: "12px",
              fontSize: "16px",
              backgroundColor: "#007bff",
              color: "#fff",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
              marginBottom: "30px"
            }}
          >
            Run Query
          </button>

          {/* Results Section */}
          {response && (
            <>
              <h2 style={{ marginTop: 30 }}>👥 Patient Results</h2>

              {/* Age Group Filter */}
              <div style={{ marginBottom: 15 }}>
                <label style={{ fontWeight: "bold", marginRight: 10 }}>Filter by age group:</label>
                <select
                  onChange={(e) => {
                    const selectedRange = e.target.value;
                    if (!selectedRange) {
                      setResponse({ ...response, results: fullResults });
                      return;
                    }
                    const [min, max] = selectedRange.split("-").map(Number);
                    const filtered = fullResults.filter((p) => p.age >= min && p.age <= max);
                    setResponse({ ...response, results: filtered });
                  }}
                >
                  <option value="">-- All --</option>
                  <option value="50-59">50–59</option>
                  <option value="60-69">60–69</option>
                  <option value="70-79">70–79</option>
                  <option value="80-200">80+</option>
                </select>
              </div>

              {/* Patient Table */}
              <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "16px", marginBottom: "30px" }}>
                <thead style={{ backgroundColor: "#f0f0f0" }}>
                  <tr>
                    <th style={{ padding: "10px", border: "1px solid #ddd" }}>Name</th>
                    <th style={{ padding: "10px", border: "1px solid #ddd" }}>Age</th>
                    <th style={{ padding: "10px", border: "1px solid #ddd" }}>Condition</th>
                  </tr>
                </thead>
                <tbody>
                  {response.results.map((p, i) => (
                    <tr key={i} style={{ backgroundColor: i % 2 === 0 ? "#fff" : "#f9f9f9" }}>
                      <td style={{ padding: "10px", border: "1px solid #ddd" }}>{p.name}</td>
                      <td style={{ padding: "10px", border: "1px solid #ddd" }}>{p.age}</td>
                      <td style={{ padding: "10px", border: "1px solid #ddd" }}>{p.condition}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              {/* Pie Chart Visualization */}
              <h2 style={{ marginTop: 30 }}>📊 Patient Count by Age Group</h2>
              <div style={{
                display: "flex",
                justifyContent: "center",
                backgroundColor: "#fdfdfd",
                borderRadius: "12px",
                padding: "20px",
                boxShadow: "0 2px 10px rgba(0,0,0,0.05)"
              }}>
                <PieChart width={400} height={300}>
                  <Pie
                    data={groupByAgeRange(response.results)}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    label
                  >
                    {groupByAgeRange(response.results).map((_, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </div>
            </>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer style={{
        backgroundColor: "#f1f1f1",
        padding: "15px 0",
        textAlign: "center",
        fontSize: "14px",
        color: "#666",
        borderTop: "1px solid #ddd"
      }}>
        Built by Mani Kumar Edukoju • For demo purposes only
      </footer>
    </div>
  );
}

export default App;
