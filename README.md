# 📊 LucidSQL AI

### **Ask Your Database. Get Answers in SQL.**

**LucidSQL AI** is an AI-powered **Natural Language → SQL** application that lets users query a SQLite database using plain English.

Instead of manually writing SQL, simply ask:

> **"Show me the top 5 students by score."**

LucidSQL AI understands the database schema, generates a SQL query using **GPT-OSS 120B via Groq**, validates the query through a read-only safety layer, executes it against SQLite, and presents the results in a clean Streamlit interface.

---

## ✨ What Makes LucidSQL AI Different?

LucidSQL is designed around a simple idea:

> **You shouldn't need to know SQL to work with data.**

The application combines **LLM reasoning, database schema inspection, SQL generation, SQL validation, and data analysis** into one workflow.

```text
Natural Language
       ↓
   Schema-Aware
     Prompt
       ↓
   GPT-OSS 120B
       ↓
 Generated SQL
       ↓
 SQL Safety Layer
       ↓
     SQLite
       ↓
 Pandas DataFrame
       ↓
    Results
```

---

# 🚀 Features

### 🗣️ Natural Language Queries

Ask your database questions in everyday language without writing SQL manually.

Examples:

```text
Show all students

Show the top 5 students by score

Which subjects have an average score above 80?

How many students scored more than 85?
```

---

### 🤖 AI-Powered SQL Generation

LucidSQL uses:

```text
Groq
  └── openai/gpt-oss-120b
```

The model receives the database schema together with the user's question and generates SQLite-compatible SQL.

The application currently configures the Groq model with temperature `0` for more deterministic SQL generation.

---

### 🧠 Automatic Database Schema Discovery

LucidSQL does not rely on a hardcoded schema.

It connects to the SQLite database and dynamically discovers:

- Tables
- Column names
- Column data types

using SQLAlchemy's inspection API.

This allows the LLM to generate queries based on the **actual database structure**.

---

### 🔐 Read-Only SQL Safety

LLM-generated SQL should never be blindly trusted.

LucidSQL therefore includes a basic validation layer that allows only read-oriented queries beginning with:

```sql
SELECT
```

or:

```sql
WITH
```

It rejects potentially destructive operations including:

```text
INSERT
UPDATE
DELETE
DROP
ALTER
CREATE
REPLACE
TRUNCATE
ATTACH
DETACH
PRAGMA
```

This validation happens before the query is executed against the database.

> **Note:** This is an application-level safety layer, not a replacement for proper database permissions and production security controls.

---

### 📊 Interactive Results

Validated SQL is executed through SQLAlchemy/Pandas and displayed as an interactive DataFrame inside Streamlit.

Users can see both:

```text
Generated SQL
      +
Query Results
```

instead of having the AI response hidden behind the scenes.

---

### 🔍 Schema Viewer

LucidSQL includes an expandable database schema section so users can inspect the tables and columns available to the AI.

---

### 🎨 Clean Professional UI

The Streamlit interface includes:

- Responsive wide layout
- Theme-adaptive styling
- Gradient LucidSQL branding
- Centered query interface
- Result cards
- SQL syntax highlighting
- Interactive DataFrame rendering
- Query clearing
- Error handling

---

# 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │        USER         │
                         │                     │
                         │ "Show top 5 marks"  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      STREAMLIT      │
                         │      Frontend       │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    LANGCHAIN CORE   │
                         │                     │
                         │ Prompt + LLM Chain  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │        GROQ         │
                         │  GPT-OSS 120B       │
                         └──────────┬──────────┘
                                    │
                                    │ Generated SQL
                                    ▼
                         ┌─────────────────────┐
                         │    SQL CLEANER      │
                         │   Remove Markdown   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   SQL VALIDATOR     │
                         │                     │
                         │   Read-Only Check   │
                         └──────────┬──────────┘
                                    │
                           ┌────────┴────────┐
                           │                 │
                        VALID             INVALID
                           │                 │
                           ▼                 ▼
                  ┌────────────────┐      REJECT
                  │   SQLALCHEMY   │
                  │                │
                  │ SQLite Database│
                  └───────┬────────┘
                          │
                          ▼
                  ┌────────────────┐
                  │     PANDAS     │
                  │   DataFrame    │
                  └───────┬────────┘
                          │
                          ▼
                  ┌────────────────┐
                  │    STREAMLIT   │
                  │     Results    │
                  └────────────────┘
```

---

# 🧰 Tech Stack

| Technology | Role |
|---|---|
| 🐍 **Python** | Core application logic |
| 🎈 **Streamlit** | Web UI |
| ⚡ **Groq** | Cloud LLM inference |
| 🧠 **GPT-OSS 120B** | Natural Language → SQL |
| 🔗 **LangChain Core** | Prompt and LLM pipeline |
| 🗄️ **SQLite** | Relational database |
| 🔧 **SQLAlchemy** | Database connection and schema inspection |
| 🐼 **Pandas** | Query result processing |
| 🔐 **python-dotenv** | Environment variable management |
| 🧹 **Regex** | SQL cleaning and validation |

---

# 📁 Project Structure

```text
LucidSQL-AI-Capstone/
│
├── app.py
├── project.db
├── create_database.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

### `app.py`

Main Streamlit application containing:

- UI
- Database connection
- Schema extraction
- Groq integration
- Prompt engineering
- SQL generation
- SQL cleaning
- SQL validation
- Query execution
- Result display

The current implementation performs database inspection, initializes the Groq model, constructs the SQL chain, validates SQL, and displays the query/result workflow in the Streamlit application. 

### `project.db`

SQLite database used by the application.

### `create_database.py`

Script used to create and populate the demonstration database.

### `.env`

Contains the Groq API key.

### `requirements.txt`

Contains project dependencies.

---

# 🗄️ Database

LucidSQL currently uses SQLite:

```text
project.db
```

The application connects using:

```python
engine = create_engine("sqlite:///project.db")
```

The schema is dynamically inspected and formatted before being provided to the LLM.

---

# 🧪 Demo Database

The demo database contains a:

```text
grades
```

table.

### Schema

```sql
CREATE TABLE grades (
    id INTEGER PRIMARY KEY,
    name TEXT,
    subject TEXT,
    score INTEGER,
    grade TEXT
);
```

### Example Data

| ID | Name | Subject | Score | Grade |
|---:|---|---|---:|---|
| 1 | Aman | Math | 95 | A |
| 2 | Anshu | Math | 78 | C |
| 3 | Akshu | History | 88 | B |
| 4 | Rahul | History | 92 | A |
| 5 | Divyansh | Science | 85 | B |
| 6 | Nandini | Math | 65 | D |
| 7 | Upayan | Life | 85 | B |
| 8 | Verstappen | F1 | 95 | A |
| 9 | Leo | Football | 100 | E |
| 10 | Student | Java | 64 | D |

The dataset is intended for demonstration and testing.

---

# 🧠 How LucidSQL Works

Suppose the user asks:

```text
Show the top 5 students by score
```

### 1️⃣ Schema Discovery

LucidSQL inspects the SQLite database and discovers:

```text
Table: grades

- id      (INTEGER)
- name    (TEXT)
- subject (TEXT)
- score   (INTEGER)
- grade   (TEXT)
```

### 2️⃣ Prompt Construction

The model receives:

```text
DATABASE SCHEMA:
Table: grades
- id (INTEGER)
- name (TEXT)
- subject (TEXT)
- score (INTEGER)
- grade (TEXT)

USER QUESTION:
Show the top 5 students by score
```

The application explicitly instructs the model to use only available tables/columns, generate SQLite-compatible SQL, return only SQL, and avoid write operations.

### 3️⃣ SQL Generation

The LLM might generate:

```sql
SELECT name, score
FROM grades
ORDER BY score DESC
LIMIT 5;
```

### 4️⃣ SQL Cleaning

The application removes accidental Markdown code fences from the model output before validation.

### 5️⃣ SQL Validation

The generated query passes through the read-only SQL validator.

```text
SELECT
  ↓
Allowed ✅
```

A destructive statement such as:

```sql
DROP TABLE grades;
```

is rejected.

### 6️⃣ Query Execution

The validated query is executed against SQLite.

### 7️⃣ Result Presentation

The result is converted into a Pandas DataFrame and displayed in Streamlit.

---

# 💬 Example Questions

Try asking LucidSQL:

```text
Show all students
```

```text
Show the top 5 students by score
```

```text
Who scored more than 80?
```

```text
What is the average score?
```

```text
Show the average score for each subject
```

```text
How many students are there?
```

```text
Show students ordered by score from highest to lowest
```

```text
Which students got an A?
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

The application loads environment variables with:

```python
from dotenv import load_dotenv

load_dotenv()
```

and checks that the Groq API key is available before starting.

### ⚠️ Never commit your API key

Add this to `.gitignore`:

```text
.env
```

---

# 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/ramtanay/LucidSQL-AI-Capstone.git
```

```bash
cd LucidSQL-AI-Capstone
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv myvenv
```

```bash
myvenv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv myvenv
```

```bash
source myvenv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or:

```bash
pip install streamlit pandas sqlalchemy langchain-core langchain-groq python-dotenv
```

### 4. Configure Groq

Create `.env`:

```env
GROQ_API_KEY=your_groq_api_key
```

### 5. Create the database

Run:

```bash
python create_database.py
```

### 6. Start the application

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

# 📸 User Experience

```text
┌────────────────────────────────────────────────────┐
│                                                    │
│                   LucidSQL AI                      │
│      Enterprise-Grade Natural Language to SQL      │
│                                                    │
│                Ask Your Database                   │
│                                                    │
│ ┌────────────────────────────────────────────────┐ │
│ │ Show the top 5 students by score               │ │
│ └────────────────────────────────────────────────┘ │
│                                                    │
│          [ Generate Query 🚀 ]     [ Clear ]      │
│                                                    │
└────────────────────────────────────────────────────┘


┌────────────────────────┐   ┌───────────────────────┐
│    Generated SQL       │   │       Results         │
│                        │   │                       │
│ SELECT name, score     │   │ Name       Score      │
│ FROM grades            │   │ Leo         100       │
│ ORDER BY score DESC    │   │ Aman         95       │
│ LIMIT 5;               │   │ Verstappen   95       │
│                        │   │ Rahul        92       │
└────────────────────────┘   └───────────────────────┘
```

---

# 🔐 Security

LucidSQL includes a basic safety layer to reduce the risk of executing destructive SQL generated by an LLM.

However, for a production deployment, additional controls should be implemented:

- Database-level read-only permissions
- SQL parser / AST validation
- Query timeout limits
- Result-size limits
- Authentication and authorization
- Rate limiting
- Audit logging
- Input validation

The current validator is intentionally lightweight and based on query structure and forbidden SQL keywords.

---

# 📈 Future Roadmap

LucidSQL can evolve into a complete AI data-analysis platform.

### 🔮 Planned Improvements

- [ ] Multi-table JOIN support improvements
- [ ] Conversational follow-up questions
- [ ] Query history
- [ ] Automatic chart generation
- [ ] SQL explanation mode
- [ ] Database upload
- [ ] CSV support
- [ ] PostgreSQL support
- [ ] MySQL support
- [ ] DuckDB support
- [ ] Advanced SQL parser-based validation
- [ ] User authentication
- [ ] Query caching
- [ ] AI-generated insights from query results

### Example Future Interaction

```text
User:
Show the top 5 students.

AI:
[SQL + Results]

User:
Only show Math students.

AI:
[Updated SQL + Results]

User:
Make a bar chart.

AI:
[Visualization]
```

---

# 🎯 Learning Outcomes

This project demonstrates practical experience with:

- Python application development
- SQL and relational databases
- SQLite
- SQLAlchemy
- Pandas
- Streamlit
- LangChain
- Prompt engineering
- LLM APIs
- Groq inference
- Natural Language → SQL systems
- Schema introspection
- LLM output parsing
- SQL validation
- AI application security
- Environment variable management

---

# 🌟 Why This Project?

Traditional database applications require users to understand SQL.

LucidSQL explores a more accessible interface:

```text
Traditional Approach

User
 ↓
Learn SQL
 ↓
Write Query
 ↓
Execute Query
 ↓
Analyze Result
```

LucidSQL:

```text
User
 ↓
Ask in Natural Language
 ↓
AI Generates SQL
 ↓
Safety Validation
 ↓
Execute Query
 ↓
View Result
```

The goal isn't to replace SQL.

The goal is to make **data querying dramatically more accessible while still exposing the generated SQL for transparency and learning.**

---

# 👨‍💻 Author

## **Ramtanay Chakraborty**

AI / ML • Data Analytics • Python • Backend Development

GitHub: [ramtanay](https://github.com/ramtanay)

---

<p align="center">
  <b>Built with Python • Streamlit • LangChain • Groq • SQLAlchemy • SQLite</b>
</p>

<p align="center">
  ⭐ Star the repository if you found LucidSQL AI interesting!
</p>