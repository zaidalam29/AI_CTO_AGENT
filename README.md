

<div align="center">

# 🤖 AI CTO Agent By Zaid Alam

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Next.js](https://img.shields.io/badge/nextjs-16-green)
![Python](https://img.shields.io/badge/python-3.9+-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-orange)
![License](https://img.shields.io/badge/license-MIT-red)

**Artificial Intelligence Chief Technology Officer - Your AI-powered technical project advisor**

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [API](#-api) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [AI Agents](#-ai-agents)
- [API Endpoints](#-api-endpoints)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage Examples](#-usage-examples)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**AI CTO Agent** is an intelligent system that automates the role of a Chief Technology Officer. It helps you:

| Area | Capability |
|------|------------|
| 📋 **Planning** | Break down requirements into features, estimate timeline & cost |
| 🏗️ **Architecture** | Design scalable system architecture, database schema, APIs |
| ⚠️ **Risk** | Identify technical, business, and security risks with ML |
| 📅 **Sprints** | Create detailed sprint plans with user stories |
| 🔧 **DevOps** | Design CI/CD pipelines, infrastructure, monitoring |
| 👨‍💻 **Code Review** | Analyze code quality, security, performance |

> 🚀 **From requirements to complete technical plan in minutes!**

---

## ✨ Features

### 🤖 **6 Specialized AI Agents**

| Agent | Responsibility | Output |
|-------|---------------|--------|
| **Planner Agent** | Requirements analysis | Features, Tech stack, Estimates |
| **Architect Agent** | System design | Architecture, Database, APIs |
| **Risk Agent** | Risk assessment | Risk score, Mitigation strategies |
| **Sprint Agent** | Agile planning | Sprints, User stories, Timeline |
| **DevOps Agent** | Infrastructure | CI/CD, Monitoring, Backup |
| **Code Review Agent** | Code quality | Quality score, Security issues |

### 🚀 **Key Capabilities**

- **Parallel Processing** - All agents work simultaneously
- **ML-Powered** - Risk prediction using machine learning
- **Vector Memory** - Learns from past projects using ChromaDB
- **Multi-LLM Support** - OpenAI, OpenRouter, Cohere
- **REST API** - Easy integration with any system
- **Swagger UI** - Interactive API documentation
- **Rate Limiting** - Prevent API abuse
- **Request Tracking** - Unique ID for each request
- **Comprehensive Logging** - Debug and monitor easily

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Client (Browser/API)                   │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Server (8000)                   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Routes    │  │ Middleware  │  │   Error     │          │
│  │             │  │             │  │  Handlers   │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└───────────────────────────────┬─────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────┐
│                     ORCHESTRATOR                          │
│              (Manages all agents in parallel)             │
└───┬───────────┬───────────┬───────────┬───────────┬───────┘
    │           │           │           │           │
    ▼           ▼           ▼           ▼           ▼
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│Planner  │ │Architect│ │  Risk   │ │ Sprint  │ │ DevOps  │
│ Agent   │ │ Agent   │ │  Agent  │ │ Agent   │ │ Agent   │
└─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
    │           │           │           │           │
    └───────────┴───────────┴───────────┴───────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                 Vector Database (ChromaDB)                  │
│              (Stores project history for learning)          │
└─────────────────────────────────────────────────────────────┘
```

---

## 🤖 AI Agents Details

### 1. 📋 **Planner Agent**
**File:** `app/agents/planner_agent.py`

```python
# Converts requirements into structured plan
features = planner.extract_features(requirements)
tech_stack = planner.suggest_tech_stack(requirements, features)
timeline = planner.estimate_timeline(features)
```

**Output Example:**
```json
{
  "features": [
    {"name": "User Authentication", "priority": "high", "hours": 40},
    {"name": "Product Catalog", "priority": "high", "hours": 60}
  ],
  "tech_stack": {
    "frontend": ["Next.js", "TypeScript"],
    "backend": ["FastAPI", "Python"],
    "database": ["PostgreSQL"]
  },
  "estimated_timeline_months": 3.5,
  "estimated_cost_range": "$50,000 - $75,000"
}
```

### 2. 🏗️ **Architect Agent**
**File:** `app/agents/architect_agent.py`

```python
# Designs complete system architecture
architecture = architect.design_system_architecture(
    requirements, features
)
database_schema = architect.design_database_schema(requirements)
api_spec = architect.design_api_spec(requirements)
```

**Output Example:**
```json
{
  "high_level_design": "Microservices with API Gateway",
  "components": ["Frontend", "Backend API", "Database", "Cache"],
  "database_schema": {
    "tables": ["users", "products", "orders"],
    "relationships": ["users->orders", "products->orders"]
  },
  "scaling_plan": "Horizontal scaling with load balancers"
}
```

### 3. ⚠️ **Risk Agent**
**File:** `app/agents/risk_agent.py`

```python
# Assesses project risks using ML
risks = risk.assess_project_risks(
    requirements, features, tech_stack, timeline
)
risk_score = risk.calculate_risk_score(risks)
```

**Output Example:**
```json
{
  "overall_risk_score": 45,
  "risk_level": "Medium",
  "risks": [
    {
      "category": "technical",
      "description": "Payment integration complexity",
      "probability": 0.7,
      "impact": "high",
      "mitigation": "Start with simple integration, thorough testing"
    }
  ]
}
```

### 4. 📅 **Sprint Agent**
**File:** `app/agents/sprint_agent.py`

```python
# Creates sprint plans
sprint_plan = sprint.create_sprint_plan(
    features, team_size=5, sprint_duration=14
)
```

**Output Example:**
```json
{
  "total_sprints": 4,
  "sprints": [
    {
      "number": 1,
      "user_stories": [
        {"title": "User login", "points": 5},
        {"title": "User registration", "points": 3}
      ],
      "capacity": 40
    }
  ],
  "estimated_velocity": 35
}
```

### 5. 🔧 **DevOps Agent**
**File:** `app/agents/devops_agent.py`

```python
# Designs DevOps strategy
devops_plan = devops.create_devops_plan(
    tech_stack, project_type="web_app"
)
```

**Output Example:**
```json
{
  "ci_cd_pipeline": [
    "GitHub for version control",
    "GitHub Actions for CI/CD",
    "Unit tests",
    "Integration tests",
    "Deploy to staging"
  ],
  "infrastructure": {
    "web_server": "2x t3.medium instances",
    "database": "db.t3.medium with Multi-AZ"
  },
  "monitoring_tools": ["Prometheus", "Grafana", "Sentry"]
}
```

### 6. 👨‍💻 **Code Review Agent**
**File:** `app/agents/code_review_agent.py`

```python
# Reviews code quality
review = code_review.review_code(
    code_snippet, language="python"
)
```

**Output Example:**
```json
{
  "quality_score": 85,
  "issues": [
    {
      "line": 42,
      "severity": "warning",
      "message": "Unused variable",
      "suggestion": "Remove or use the variable"
    }
  ],
  "security_issues": [],
  "performance_concerns": ["N+1 query in loop"]
}
```

---

## 🌐 API Endpoints

### Base URL: `http://localhost:8000`

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| GET | `/` | API Information | None |
| GET | `/health` | Health Check | None |
| GET | `/docs` | Swagger UI | None |
| GET | `/redoc` | ReDoc UI | None |
| POST | `/api/v1/projects/analyze` | Analyze Project | JSON (below) |
| GET | `/api/v1/projects/health` | API Health | None |
| GET | `/api/v1/projects/metrics` | API Metrics | None |

### 📤 **POST /api/v1/projects/analyze**

**Request:**
```json
{
  "name": "E-commerce Platform",
  "requirements": "Build an e-commerce platform with user auth, product catalog, shopping cart, payment integration, order management, admin dashboard. Tech: FastAPI, React, PostgreSQL.",
  "project_type": "web_app",
  "budget_range": "$50,000 - $100,000",
  "timeline": "3 months"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Project analysis completed",
  "data": {
    "project_planning": { ... },
    "system_architecture": { ... },
    "risk_assessment": { ... },
    "sprint_planning": { ... },
    "devops_plan": { ... }
  },
  "request_id": "req_abc123",
  "processing_time": "5.23s",
  "agents_used": ["planner", "architect", "risk", "sprint", "devops"]
}
```

---

## ⚡ Quick Start

### One-Line Setup (Windows PowerShell)
```powershell
powershell -Command "Invoke-WebRequest -Uri https://raw.githubusercontent.com/yourusername/ai_cto_agent/main/setup.ps1 -OutFile setup.ps1; .\setup.ps1"
```

### Manual Setup (5 Minutes)

```bash
# 1. Clone repository
git clone https://github.com/yourusername/ai_cto_agent.git
cd ai_cto_agent

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
copy .env.example .env  # Windows
cp .env.example .env     # Linux/Mac

# 6. Edit .env with your API keys
notepad .env  # Windows
nano .env     # Linux/Mac

# 7. Create directories
python create_folders.py

# 8. Run the app
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 9. Open browser
start http://localhost:8000/docs  # Windows
open http://localhost:8000/docs    # Mac
```

---

## 📥 Installation Details

### Prerequisites
- Python 3.9 or higher
- Git
- 8GB RAM minimum
- 4GB free disk space

### Step-by-Step Installation

#### **Windows**
```powershell
# 1. Install Python from python.org
# 2. Install Git from git-scm.com

# 3. Open PowerShell as Administrator
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# 4. Clone and setup
git clone https://github.com/zaidalam29/AI_CTO_AGENT.git
cd AI_CTO_AGENT

python -m venv venv
.\venv\Scripts\activate

pip install -r requirements.txt

# Create directories
New-Item -ItemType Directory -Force -Path @(
    "app\api", "app\core", "app\agents", "app\llm",
    "app\memory", "app\ml", "app\db", "app\schemas",
    "app\utils", "app\mcp", "app\middleware",
    "logs", "vector_store", "models", "tests"
)

# Create __init__.py files
$folders = @("api","core","agents","llm","memory","ml","db","schemas","utils","mcp","middleware")
foreach ($folder in $folders) {
    New-Item -ItemType File -Path "app\$folder\__init__.py" -Force
}

# Run
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### **Linux/Mac**
```bash
# 1. Install Python 3.9+
sudo apt update
sudo apt install python3.9 python3.9-venv git  # Ubuntu
# brew install python@3.9 git  # Mac

# 2. Clone and setup
git clone https://github.com/zaidalam29/AI_CTO_AGENT.git
cd AI_CTO_AGENT

python3.9 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Create directories
mkdir -p app/{api,core,agents,llm,memory,ml,db,schemas,utils,mcp,middleware}
mkdir logs vector_store models tests

# Create __init__.py files
for folder in api core agents llm memory ml db schemas utils mcp middleware; do
    touch app/$folder/__init__.py
done

# Run
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## ⚙️ Configuration

### **.env File Configuration**

```env
# ==============================
# APP SETTINGS
# ==============================
APP_NAME=AI_CTO_AGENT
ENVIRONMENT=development
DEBUG=True
SECRET_KEY=your-secret-key-here
HOST=0.0.0.0
PORT=8000

# ==============================
# OPENAI (REQUIRED)
# ==============================
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_MODEL_HIGH=gpt-4
OPENAI_MODEL_MEDIUM=gpt-3.5-turbo-16k
OPENAI_MODEL_FAST=gpt-3.5-turbo
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002

# ==============================
# OPENROUTER (Optional)
# ==============================
OPENROUTER_API_KEY=sk-xxxxxxxxxxxx
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_DEFAULT_MODEL=mistralai/mistral-7b-instruct

# ==============================
# COHERE (Optional)
# ==============================
COHERE_API_KEY=xxxxxxxxxxxx
COHERE_EMBED_MODEL=embed-english-v2.0

# ==============================
# VECTOR DATABASE
# ==============================
VECTOR_DB_TYPE=chroma
VECTOR_DB_PATH=./vector_store

# ==============================
# LOGGING
# ==============================
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
LOG_RETENTION=10
LOG_ROTATION=500 MB

# ==============================
# RATE LIMITING
# ==============================
RATE_LIMIT_REQUESTS=60
RATE_LIMIT_PERIOD=60

# ==============================
# TELEMETRY
# ==============================
ANONYMIZED_TELEMETRY=False
```

---

## 🔑 API Keys Required

### **1. OpenAI API Key** (Required)
- **Get it from:** [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Cost:** Pay-per-use (~$0.002 per request)
- **Steps:**
  1. Go to [OpenAI Platform](https://platform.openai.com)
  2. Sign up / Login
  3. Go to API Keys section
  4. Click "Create new secret key"
  5. Copy and save the key

### **2. OpenRouter API Key** (Optional - for fallback)
- **Get it from:** [https://openrouter.ai/keys](https://openrouter.ai/keys)
- **Cost:** Various models, some free

### **3. Cohere API Key** (Optional - for embeddings)
- **Get it from:** [https://dashboard.cohere.com/api-keys](https://dashboard.cohere.com/api-keys)
- **Cost:** Free tier available

---

## 📝 Usage Examples

### **Example 1: Simple Web App**
```python
import requests

url = "http://localhost:8000/api/v1/projects/analyze"

project = {
    "name": "Todo App",
    "requirements": "Build a todo app with user login, create tasks, mark complete, delete tasks. Use React and Node.js.",
    "project_type": "web_app"
}

response = requests.post(url, json=project)
print(response.json())
```

### **Example 2: E-commerce Platform**
```python
project = {
    "name": "E-commerce Platform",
    "requirements": """
    Build a scalable e-commerce platform with:
    - User authentication (JWT)
    - Product catalog with search and filters
    - Shopping cart and checkout
    - Payment integration (Stripe)
    - Order management system
    - Admin dashboard with analytics
    - Mobile responsive design
    - Review and rating system
    
    Tech preferences: 
    - Backend: Python FastAPI
    - Frontend: React with TypeScript
    - Database: PostgreSQL with Redis
    """,
    "project_type": "web_app",
    "budget_range": "$75,000 - $120,000",
    "timeline": "4 months"
}
```

### **Example 3: Using cURL**
```bash
curl -X POST "http://localhost:8000/api/v1/projects/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mobile Banking App",
    "requirements": "Secure mobile banking with UPI, transfers, bill payments",
    "project_type": "mobile_app"
  }'
```

### **Example 4: Python Script with Error Handling**
```python
import requests
import json
from datetime import datetime

def analyze_project(project_data):
    """Send project for analysis with error handling"""
    
    url = "http://localhost:8000/api/v1/projects/analyze"
    
    try:
        print(f"[{datetime.now()}] Sending request...")
        response = requests.post(url, json=project_data, timeout=120)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Success! Processing time: {result.get('processing_time')}")
            return result
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.ConnectionError:
        print("Connection error - is the server running?")
    except Exception as e:
        print(f"Error: {str(e)}")
    
    return None

# Test
project = {
    "name": "Task Manager",
    "requirements": "Simple task management app",
    "project_type": "web_app"
}

result = analyze_project(project)
if result:
    print(json.dumps(result, indent=2))
```

---

## 📁 Project Structure

```
ai_cto_agent/
│
├── app/                          # Main application
│   ├── api/                      # API endpoints
│   │   ├── projects.py           # Project analysis
│   │   └── __init__.py
│   │
│   ├── agents/                    # AI Agents
│   │   ├── planner_agent.py       # 📋 Planning
│   │   ├── architect_agent.py     # 🏗️ Architecture
│   │   ├── risk_agent.py          # ⚠️ Risk
│   │   ├── sprint_agent.py        # 📅 Sprints
│   │   ├── devops_agent.py        # 🔧 DevOps
│   │   ├── code_review_agent.py   # 👨‍💻 Code review
│   │   └── __init__.py
│   │
│   ├── core/                      # Core functionality
│   │   ├── orchestrator.py        # Agent coordinator
│   │   └── __init__.py
│   │
│   ├── llm/                       # LLM clients
│   │   ├── openai_client.py       # OpenAI
│   │   ├── openrouter_client.py   # OpenRouter
│   │   ├── cohere_client.py       # Cohere
│   │   └── __init__.py
│   │
│   ├── memory/                     # Memory systems
│   │   ├── vector_store.py         # ChromaDB
│   │   └── __init__.py
│   │
│   ├── ml/                         # Machine Learning
│   │   ├── risk_model.py           # Risk prediction
│   │   └── __init__.py
│   │
│   ├── schemas/                    # Pydantic models
│   │   ├── project_schema.py
│   │   ├── agent_schema.py
│   │   └── __init__.py
│   │
│   ├── utils/                      # Utilities
│   │   ├── logger.py
│   │   ├── exceptions.py
│   │   ├── rate_limiter.py
│   │   └── __init__.py
│   │
│   ├── middleware/                  # Middleware
│   │   ├── request_logging.py
│   │   ├── request_id.py
│   │   └── __init__.py
│   │
│   ├── config.py                    # Configuration
│   └── main.py                      # Entry point
│
├── logs/                            # Log files
├── vector_store/                     # ChromaDB data
├── models/                           # ML models
├── tests/                            # Tests
│
├── .env                              # Environment variables
├── .env.example                      # Example env
├── requirements.txt                   # Dependencies
├── README.md                          # This file
└── create_folders.py                  # Setup script
```

---

## 🔍 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| **ModuleNotFoundError** | Run `pip install -r requirements.txt` |
| **OpenAI API key missing** | Add `OPENAI_API_KEY` to `.env` file |
| **Port 8000 already in use** | `uvicorn app.main:app --port 8001` |
| **Vector store errors** | Delete `vector_store/` and restart |
| **Slow responses** | Check OpenAI API key quota |
| **Memory errors** | Reduce requirements length (<5000 chars) |
| **Windows path errors** | Use backslashes `\` in paths |

### Debug Mode
```bash
# Set DEBUG=True in .env
DEBUG=True

# Check logs
# Windows:
type logs\app.log
# Linux/Mac:
tail -f logs/app.log
```

### Verify Installation
```bash
# Check Python version
python --version  # Should be 3.9+

# Check installed packages
pip list | findstr fastapi  # Windows
pip list | grep fastapi      # Linux/Mac

# Test API
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

---

## ❓ FAQ

### Q: Do I need all API keys?
**A:** Only OpenAI API key is required. OpenRouter and Cohere are optional.

### Q: How much does it cost?
**A:** ~$0.10-0.50 per project analysis depending on requirements length.

### Q: Can I use it without internet?
**A:** No, it requires internet for OpenAI API calls.

### Q: How long does analysis take?
**A:** 30 seconds to 2 minutes depending on requirements complexity.

### Q: Can I analyze multiple projects?
**A:** Yes, with rate limiting (60 requests per minute by default).

### Q: Is my data secure?
**A:** Data is sent to OpenAI for processing. Don't send sensitive information.

### Q: Can I customize the agents?
**A:** Yes, all agent code is in `app/agents/` directory.

### Q: What if OpenAI is down?
**A:** The system falls back to OpenRouter if configured.

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork the repository**
2. **Create a branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guide
- Add docstrings for new functions
- Add tests for new features
- Update documentation
- Use type hints

---

## 📜 License

MIT License

Copyright (c) 2026 AI CTO Agent

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 🙏 Acknowledgments

- **OpenAI** - For GPT models
- **FastAPI** - For amazing web framework
- **ChromaDB** - For vector database
- **Loguru** - For beautiful logging
- **All Contributors** - For making this project better

---

## 🚀 Quick Command Summary

```bash
# Clone
git clone https://github.com/zaidalam29/AI_CTO_AGENT.git
cd AI_CTO_AGENT

# Setup
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate        # Linux/Mac

# Install
pip install -r requirements.txt

# Configure
copy .env.example .env          # Windows
cp .env.example .env             # Linux/Mac
# Edit .env with your API keys

# Create folders
python create_folders.py

# Run
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Open
start http://localhost:8000/docs  # Windows
open http://localhost:8000/docs    # Mac
```

---

<div align="center">
  
**Made with ❤️ by Zaid Alam - Full Stack Developer + Gen AI/ML Engineer**

</div>