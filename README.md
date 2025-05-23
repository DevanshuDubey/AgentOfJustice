
---

## ⚙️ Core Components

### 1. **Agents**
Located in `Agents.py`, the following role-specific agents are defined:
- `BaseAgent`: Shared logic (name, role, memory, response generation via Groq API)
- `JudgeAgent`
- `DefenseLawyerAgent`
- `ProsecutionLawyerAgent`
- `DefendantAgent`
- `PlaintiffAgent`
- `WitnessAgent`

Each agent stores its memory and uses structured prompts to generate contextual responses relevant to its role.

---

### 2. **Courtroom Sequence Manager**
trial progression:
- **Opening Statements**
- **Argumentation Phase**
- **Cross-Examination**
- **Defendant & Witness Testimonies**
- **Closing Statements**
- **Judge’s Final Verdict**

---

### 3. **Simulation Engine**
#### `trial_manager.py`
- Loads a case from `data.csv`
- Instantiates all agents
- Triggers courtroom flow in proper sequence

#### `main.py`
- Executes a trial for a single case
- Prints trial logs and verdict

#### `final.py`
- Iterates through multiple cases from `cases.csv`
- Logs outcomes to `output/output.csv`

---

## 🧪 Data

### 📄 `data/data.csv`
- 500 full-text case descriptions used as input
- Each row is a real-world legal scenario described in natural language

### 📄 `cases.csv`
- 100 sampled test cases for validation

### 📄 `output.csv`
- Output format
id, label
1975_38 ,1
1958_49,0
etc.


## How to run
- Just run final.py to get output.csv
