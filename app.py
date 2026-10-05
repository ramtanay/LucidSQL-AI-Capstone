import os
import re

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, inspect, text

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    st.error(
        "GROQ_API_KEY is not configured. "
        "Please add it to your .env file."
    )
    st.stop()


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="LucidSQL AI",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# THEME-ADAPTIVE PROFESSIONAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Do NOT override background */
    .stApp {
        background: none;
    }

    /* Hero Title */
    .hero-title {
        font-size: 58px;
        font-weight: 800;
        text-align: center;
        letter-spacing: -1px;
        margin-bottom: 10px;
    }

    /* Gradient Accent */
    .hero-title span {
        background: linear-gradient(90deg, #2563EB, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Subtitle */
    .hero-subtitle {
        text-align: center;
        font-size: 18px;
        opacity: 0.8;
        margin-bottom: 40px;
    }

    /* Theme Adaptive Card */
    .theme-card {
        padding: 35px;
        border-radius: 18px;
        border: 1px solid rgba(128,128,128,0.25);
    }

    /* Result Card */
    .result-card {
        padding: 25px;
        border-radius: 16px;
        border: 1px solid rgba(128,128,128,0.25);
    }

    /* Buttons */
    div.stButton > button {
        border-radius: 12px;
        font-weight: 600;
        padding: 10px 18px;
    }

    /* Primary Button */
    div.stButton > button:first-child {
        background-color: #2563EB;
        color: white;
        border: none;
    }

    div.stButton > button:first-child:hover {
        background-color: #1E40AF;
    }

    /* Footer */
    .footer {
        text-align: center;
        font-size: 13px;
        opacity: 0.6;
        margin-top: 60px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    '<div class="hero-title">Lucid<span>SQL</span> AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Enterprise-Grade Natural Language to SQL Intelligence'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

DATABASE_URL = "sqlite:///project.db"

try:
    engine = create_engine(DATABASE_URL)

    # Test database connection
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()


# ============================================================
# DATABASE SCHEMA EXTRACTION
# ============================================================

def get_database_schema(engine):
    """
    Extract database tables and columns using SQLAlchemy.
    """

    inspector = inspect(engine)

    tables = inspector.get_table_names()

    if not tables:
        return "No tables found in the database."

    schema_parts = []

    for table in tables:

        columns = inspector.get_columns(table)

        schema_parts.append(f"Table: {table}")

        for column in columns:

            column_name = column["name"]
            column_type = column["type"]

            schema_parts.append(
                f"  - {column_name} ({column_type})"
            )

        schema_parts.append("")

    return "\n".join(schema_parts)


schema = get_database_schema(engine)


# ============================================================
# GROQ LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# ============================================================
# SQL GENERATION PROMPT
# ============================================================

prompt = ChatPromptTemplate.from_template(
    """
You are a senior data analyst and SQL expert.

Your task is to convert the user's natural-language question
into a valid SQLite SQL query.

DATABASE SCHEMA:
{schema}

USER QUESTION:
{question}

STRICT RULES:

1. Use ONLY tables and columns present in the schema.
2. Generate SQLite-compatible SQL.
3. Return ONLY the SQL query.
4. Do NOT use markdown code blocks.
5. Do NOT provide explanations.
6. Do NOT generate INSERT statements.
7. Do NOT generate UPDATE statements.
8. Do NOT generate DELETE statements.
9. Do NOT generate DROP statements.
10. Do NOT generate ALTER statements.
11. Do NOT generate CREATE statements.
12. Only generate read-only SELECT queries.
"""
)


# ============================================================
# LANGCHAIN SQL CHAIN
# ============================================================

sql_chain = prompt | llm | StrOutputParser()


# ============================================================
# SQL SAFETY VALIDATION
# ============================================================

def clean_sql(sql_query):
    """
    Remove markdown formatting accidentally returned by the LLM.
    """

    sql_query = sql_query.strip()

    # Remove ```sql
    sql_query = re.sub(
        r"^```sql\s*",
        "",
        sql_query,
        flags=re.IGNORECASE
    )

    # Remove ```
    sql_query = re.sub(
        r"```$",
        "",
        sql_query
    )

    return sql_query.strip()


def validate_sql(sql_query):
    """
    Basic read-only SQL validation.

    LucidSQL currently allows only SELECT queries.
    """

    normalized = sql_query.strip().lower()

    # Must start with SELECT or WITH
    if not (
        normalized.startswith("select")
        or normalized.startswith("with")
    ):
        return False, "Only SELECT queries are allowed."

    forbidden_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "create",
        "replace",
        "truncate",
        "attach",
        "detach",
        "pragma"
    ]

    for keyword in forbidden_keywords:

        pattern = rf"\b{keyword}\b"

        if re.search(pattern, normalized):
            return False, (
                f"Unsafe SQL detected: "
                f"'{keyword.upper()}' operation is not allowed."
            )

    return True, ""


# ============================================================
# SESSION STATE
# ============================================================

if "question" not in st.session_state:
    st.session_state.question = ""

if "sql_query" not in st.session_state:
    st.session_state.sql_query = None

if "result" not in st.session_state:
    st.session_state.result = None

if "error" not in st.session_state:
    st.session_state.error = None


# ============================================================
# INPUT CARD
# ============================================================

center = st.columns([1, 2, 1])[1]

with center:

    st.markdown(
        '<div class="theme-card">',
        unsafe_allow_html=True
    )

    st.markdown("### Ask Your Database")

    st.session_state.question = st.text_input(
        "Query",
        value=st.session_state.question,
        placeholder="e.g., Show top 5 students by total marks",
        label_visibility="collapsed"
    )

    col1, col2 = st.columns([3, 1])

    submit = col1.button(
        "Generate Query 🚀",
        use_container_width=True
    )

    clear = col2.button(
        "Clear",
        use_container_width=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# CLEAR BUTTON
# ============================================================

if clear:

    st.session_state.question = ""
    st.session_state.sql_query = None
    st.session_state.result = None
    st.session_state.error = None

    st.rerun()


# ============================================================
# SUBMIT BUTTON
# ============================================================

if submit:

    question = st.session_state.question.strip()

    if not question:

        st.warning("Please enter a question.")

    else:

        # Reset previous error
        st.session_state.error = None

        with st.spinner("Analyzing database..."):

            try:

                # ------------------------------------------------
                # STEP 1: Generate SQL using Groq
                # ------------------------------------------------

                sql_query = sql_chain.invoke(
                    {
                        "schema": schema,
                        "question": question
                    }
                )

                # ------------------------------------------------
                # STEP 2: Clean generated SQL
                # ------------------------------------------------

                sql_query = clean_sql(sql_query)

                # ------------------------------------------------
                # STEP 3: Validate SQL
                # ------------------------------------------------

                is_valid, validation_message = validate_sql(
                    sql_query
                )

                if not is_valid:

                    st.session_state.sql_query = sql_query
                    st.session_state.result = None
                    st.session_state.error = validation_message

                else:

                    # ------------------------------------------------
                    # STEP 4: Execute SQL
                    # ------------------------------------------------

                    df = pd.read_sql_query(
                        sql_query,
                        engine
                    )

                    # ------------------------------------------------
                    # STEP 5: Store results
                    # ------------------------------------------------

                    st.session_state.sql_query = sql_query
                    st.session_state.result = df
                    st.session_state.error = None

            except Exception as e:

                st.session_state.sql_query = None
                st.session_state.result = None
                st.session_state.error = str(e)


# ============================================================
# ERROR DISPLAY
# ============================================================

if st.session_state.error:

    st.error(
        f"Error: {st.session_state.error}"
    )


# ============================================================
# RESULTS SECTION
# ============================================================

if st.session_state.sql_query:

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    # ----------------------------------------------------------
    # GENERATED SQL
    # ----------------------------------------------------------

    with col1:

        st.markdown(
            '<div class="result-card">',
            unsafe_allow_html=True
        )

        st.markdown("### Generated SQL")

        st.code(
            st.session_state.sql_query,
            language="sql"
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    # ----------------------------------------------------------
    # RESULTS
    # ----------------------------------------------------------

    with col2:

        st.markdown(
            '<div class="result-card">',
            unsafe_allow_html=True
        )

        st.markdown("### Results")

        if st.session_state.result is not None:

            df = st.session_state.result

            if df.empty:

                st.info(
                    "The query executed successfully, "
                    "but returned no rows."
                )

            else:

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )

                st.caption(
                    f"{len(df)} row(s) returned"
                )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# ============================================================
# DATABASE INFORMATION
# ============================================================

with st.expander("🔍 Database Schema"):

    st.code(
        schema,
        language="text"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">'
    'Powered by LangChain • Groq • SQLAlchemy • Streamlit<br>'
    'Developed by Ramtanay Chakraborty'
    '</div>',
    unsafe_allow_html=True
)