# Placeko — AI Career Copilot

> **An AI-native career intelligence platform that combines LLMs, NLP, semantic search, embeddings, and agentic interview workflows to help candidates move from resume to job application and interview readiness.**

Placeko is a full-stack **Generative AI application** built around a candidate's resume, target roles, interview preparation, and job-search workflow.

The core idea is simple:

```text
Resume
  ↓
Candidate Intelligence
  ↓
Job Understanding
  ↓
Semantic Job Matching
  ↓
Personalized Interview Planning
  ↓
AI Question Generation
  ↓
Answer Evaluation
  ↓
Interview Insights
  ↓
Application Tracking
```

Rather than building a generic chatbot, Placeko uses AI inside a structured software architecture where **LLMs handle reasoning and personalization while deterministic backend services handle validation, state, authentication, and persistence.**

---

#  Why Placeko?

Traditional career platforms usually treat each part of the job search independently:

```text
Resume Tool
Job Portal
Interview Platform
Application Tracker
```

Placeko connects these workflows.

A candidate's resume becomes the foundation for downstream AI capabilities:

```text
                  ┌──────────────────┐
                  │     RESUME       │
                  └────────┬─────────┘
                           │
             ┌─────────────┼─────────────┐
             ↓             ↓             ↓
       Resume AI      Job Matching   Interview AI
             │             │             │
             ↓             ↓             ↓
       Candidate      Relevant Jobs   Personalized
       Profile                         Questions
                                           │
                                           ↓
                                      AI Evaluation
                                           │
                                           ↓
                                    Interview Report
                                           │
                                           ↓
                                   Application Tracker
```

This creates a **context-aware career intelligence system** rather than a collection of unrelated AI features.

---

#  AI Capabilities

## 1.  Resume Intelligence

The resume is converted from an unstructured document into structured candidate information.

```text
PDF / Resume
      ↓
Document Processing
      ↓
Text Extraction
      ↓
NLP Processing
      ↓
Semantic Information Extraction
      ↓
Candidate Profile
```

The resulting candidate representation can contain:

- Skills
- Education
- Experience
- Projects
- Technologies
- Career information
- Relevant achievements

This structured representation becomes context for other AI workflows.

---

# 2.  Semantic Job Matching

Placeko uses **embedding-based semantic matching** instead of relying only on keyword overlap.

```text
Candidate Profile
       ↓
Text Representation
       ↓
Embedding Model
       ↓
Candidate Vector
       │
       │ Cosine Similarity
       ↓
Job Vectors
       ↓
Ranked Job Recommendations
```

The system can identify relationships between semantically similar concepts even when the exact wording differs.

For example:

```text
Candidate:
"Built REST APIs using FastAPI"

Job:
"Experience developing Python backend services"
```

A semantic representation can recognize the relationship between these concepts beyond exact keyword matching.

---

# 3.  AI Mock Interview Engine

Placeko contains an interview workflow designed around **personalized question generation rather than static question banks**.

The interview system uses context such as:

- Candidate resume
- Candidate projects
- Candidate skills
- Target job
- Interview type
- Difficulty
- Focus topics
- Expected concepts
- Previously generated questions

### Interview pipeline

```text
Candidate Profile
       +
Target Job
       ↓
Interview Planning
       ↓
Question Generation
       ↓
Question Validation
       ↓
Candidate Answer
       ↓
Answer Evaluation
       ↓
Structured Feedback
       ↓
Interview Report
```

---

# 4.  Interview Planning

The interview module separates **interview orchestration** from **question generation**.

The planning layer determines the structure of an interview before individual questions are generated.

Example:

```text
Interview Plan

Mode:
Technical

Difficulty:
Medium

Focus:
Backend + AI/ML

Question Types:
├── Project
├── Technical
├── System Design
└── Behavioral
```

This makes the interview workflow deterministic at the orchestration layer while allowing the LLM to provide contextual reasoning.

---

# 5.  Context-Aware Question Generation

Questions are generated dynamically from candidate and job context.

The system prioritizes:

```text
Candidate Projects
        ↓
Work Experience
        ↓
Resume ↔ Job Skill Overlap
        ↓
Role-Specific Concepts
```

The question generator also considers previous questions to reduce repetition.

Instead of:

```text
Question Bank → Random Question
```

Placeko follows:

```text
Candidate Context
       +
Job Context
       +
Interview State
       ↓
LLM Reasoning
       ↓
Next Best Question
```

---

# 6.  Structured AI Outputs

LLM responses are not treated as arbitrary strings wherever structured application data is required.

Placeko uses schema-driven AI outputs.

Conceptually:

```text
LLM
 ↓
Structured Output
 ↓
Pydantic Schema
 ↓
Validation
 ↓
Application Logic
```

This provides:

- Predictable contracts
- Validation
- Easier frontend integration
- Reduced parsing complexity
- Better separation between AI reasoning and application logic

---

# 7.  AI Answer Evaluation

Interview answers are evaluated in context rather than as isolated text.

The evaluator can receive:

```text
Candidate Profile
      +
Target Job
      +
Question
      +
Question Category
      +
Difficulty
      +
Expected Topics
      +
Candidate Answer
```

This allows evaluation to consider whether the candidate actually addressed the concepts expected by the question.

The result is represented using structured interview feedback.

---

# 8.  Multimodal Interview Input

Placeko supports voice-based interview answers in addition to text answers.

```text
Microphone
    ↓
MediaRecorder
    ↓
Audio Blob
    ↓
Multipart FormData
    ↓
FastAPI
    ↓
Audio Processing
    ↓
Transcript
    ↓
AI Evaluation
```

This creates a foundation for multimodal interview experiences where the candidate is not limited to typing answers.

---

# 9.  AI Interview Reports

Interview sessions can be transformed into structured performance information.

The report can capture areas such as:

- Answer quality
- Strengths
- Weaknesses
- Technical understanding
- Communication quality
- Areas for improvement

This allows the interview system to move beyond question generation toward **candidate performance intelligence**.

---

# 10.  AI → Application Workflow

Placeko connects AI-driven career workflows with a deterministic application management system.

```text
AI Job Recommendation
          ↓
     Target Job
          ↓
   Interview Preparation
          ↓
     Job Application
          ↓
   Application Kanban
```

Applications can move through:

```text
Saved
  ↓
Applied
  ↓
Screening
  ↓
Interview
  ↓
Offer
  ↓
Accepted

Rejected / Withdrawn
```

The application state is persisted in MongoDB.

---

#  AI-Native Architecture

The architecture separates **AI reasoning** from deterministic application infrastructure.

```text
                         ┌──────────────────────────┐
                         │       React + TS         │
                         │        Frontend          │
                         └────────────┬─────────────┘
                                      │
                                      │ REST API
                                      ↓
                         ┌──────────────────────────┐
                         │         FastAPI          │
                         │       API Layer          │
                         └────────────┬─────────────┘
                                      │
             ┌────────────────────────┼────────────────────────┐
             │                        │                        │
             ↓                        ↓                        ↓
      ┌─────────────┐          ┌─────────────┐          ┌─────────────┐
      │   Resume    │          │    Jobs     │          │  Interview  │
      │     AI      │          │     AI      │          │     AI      │
      └──────┬──────┘          └──────┬──────┘          └──────┬──────┘
             │                        │                        │
             │                        │                        │
             └────────────────────────┼────────────────────────┘
                                      │
                                      ↓
                           ┌─────────────────────┐
                           │ Application Service │
                           │  Business Logic     │
                           └──────────┬──────────┘
                                      │
                                      ↓
                           ┌─────────────────────┐
                           │   Repository Layer  │
                           └──────────┬──────────┘
                                      │
                                      ↓
                           ┌─────────────────────┐
                           │       MongoDB       │
                           └─────────────────────┘
```

---

#  AI vs Deterministic Logic

A key architectural principle is:

> **LLMs should reason; software should enforce rules.**

### AI responsibilities

```text
LLM / AI
│
├── Resume understanding
├── Semantic interpretation
├── Job matching
├── Interview planning
├── Question generation
└── Answer evaluation
```

### Deterministic responsibilities

```text
Backend
│
├── Authentication
├── Authorization
├── Input validation
├── Status transitions
├── Database operations
├── API contracts
└── Application state
```

This reduces the impact of LLM unpredictability on critical application state.

---

#  AI Pipeline Design

A typical AI workflow follows:

```text
Raw Input
   ↓
Preprocessing
   ↓
Context Construction
   ↓
Prompt / Model Invocation
   ↓
Structured Output
   ↓
Schema Validation
   ↓
Business Logic
   ↓
Persisted / Returned Result
```

The model is therefore one component inside a larger pipeline rather than the entire system.

---

#  Backend Architecture

Placeko uses a modular service-oriented backend.

```text
Controller
    ↓
Service
    ↓
Repository
    ↓
Database
```

### Controllers

Handle:

- HTTP requests
- Authentication dependencies
- Request validation
- Response formatting

### Services

Handle:

- Business logic
- AI orchestration
- Workflow logic
- Domain rules

### Repositories

Handle:

- Persistence
- Database queries
- Data retrieval
- Storage abstraction

This prevents AI logic, business logic, and persistence logic from being tightly coupled.

---

#  Application Module

The application tracker follows:

```text
Frontend
   ↓
Axios API Client
   ↓
FastAPI Controller
   ↓
ApplicationService
   ↓
ApplicationRepository
   ↓
MongoDB
```

For example:

```text
PATCH /api/applications/{id}/status
                ↓
       Controller Validation
                ↓
       ApplicationService
                ↓
       Status Business Rules
                ↓
       MongoDB Repository
```

---

#  Persistence

MongoDB stores persistent application state.

The application module was initially developed using an in-memory repository and later migrated to MongoDB.

This transition demonstrates the value of the repository abstraction:

```text
ApplicationService
       ↓
ApplicationRepository
       ↓
     Storage
```

The service does not need to know whether the underlying storage is in-memory or MongoDB.

---

#  Authentication Architecture

Placeko uses JWT-based authentication for protected workflows.

```text
Login
  ↓
Credential Validation
  ↓
JWT Generation
  ↓
Frontend Storage
  ↓
Axios Interceptor
  ↓
Authorization: Bearer <token>
  ↓
FastAPI Authentication Dependency
  ↓
Authenticated User
```

User-scoped resources are queried using the authenticated user's identity.

---

#  Technology Stack

## AI / ML

- Large Language Models
- Langgraph(Agentic AI)
- Generative AI
- Prompt Engineering
- Structured LLM Outputs
- NLP
- Embeddings
- Semantic Similarity
- Vector Search
- Speech / Audio Processing

## Backend

- Python
- FastAPI
- Pydantic
- Uvicorn
- Motor
- MongoDB

## Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Axios
- Lucide React

## Engineering

- REST APIs
- JWT Authentication
- Service Layer
- Repository Pattern
- Modular Architecture
- Git / GitHub

---

#  Reliability Strategy

Generative AI introduces uncertainty.

Placeko therefore uses several boundaries around AI components:

```text
LLM
 ↓
Structured Output
 ↓
Pydantic Validation
 ↓
Application Logic
 ↓
Persistence
```

The system avoids allowing arbitrary model output to directly mutate critical application state.

This is particularly important for workflows such as:

- Authentication
- Application status
- Database persistence
- Interview state
- API contracts

---

#  Engineering Challenges

## Context-Aware AI

Generating useful interview questions requires combining multiple context sources:

```text
Resume
+
Target Job
+
Interview Plan
+
Previous Questions
+
Difficulty
```

The challenge is not simply generating text, but generating the **right next question**.

## Semantic Matching

Traditional keyword matching can miss relationships between related concepts.

Embeddings provide a semantic representation that enables similarity-based retrieval and ranking.

## AI Reliability

LLMs can produce unexpected output.

Structured schemas and deterministic business logic provide a boundary between probabilistic AI reasoning and reliable application behavior.

## Multimodal Input

Voice interviews require coordinating:

```text
Browser Recording
→ Audio Upload
→ Backend Processing
→ Transcription
→ Evaluation
```

## Stateful Workflows

Interview sessions and application pipelines contain state that should not depend on an LLM's interpretation.

The backend therefore owns workflow state explicitly.

---

# 📈 Example End-to-End AI Workflow

```text
                    USER
                      │
                      ↓
                Resume Upload
                      │
                      ↓
              Resume Intelligence
                      │
                      ↓
             Candidate Profile
                      │
          ┌───────────┴───────────┐
          ↓                       ↓
   Job Recommendations       Interview AI
          │                       │
          ↓                       ↓
      Target Job            Interview Plan
                                  │
                                  ↓
                          Question Generation
                                  │
                                  ↓
                             User Answer
                                  │
                    ┌─────────────┴─────────────┐
                    ↓                           ↓
                  Text                        Voice
                    │                           │
                    │                    Audio Processing
                    │                           │
                    └─────────────┬─────────────┘
                                  ↓
                           Answer Evaluation
                                  │
                                  ↓
                           Interview Report
                                  │
                                  ↓
                         Application Tracking
```



---

#  What This Project Demonstrates

Placeko demonstrates practical implementation of:

- Generative AI applications
- LLM integration
- Structured LLM outputs
- Prompt engineering
- NLP pipelines
- Embedding-based semantic search
- AI workflow orchestration
- Context-aware generation
- Multimodal AI input
- FastAPI backend architecture
- React + TypeScript
- MongoDB persistence
- JWT authentication
- Service-repository architecture
- REST API design
- Stateful workflows
- AI reliability boundaries
- Full-stack system design

---

#  Core Philosophy

> **AI should provide intelligence; the software architecture should provide control.**

Placeko combines probabilistic AI components with deterministic engineering:

```text
Generative AI
      +
NLP
      +
Embeddings
      +
Structured Outputs
      +
Workflow Orchestration
      +
Deterministic Backend
      +
Persistent State
      =
AI Career Copilot
```

---

#  Author

**Ashutosh Kushwaha**

B.Tech — Computer Science Engineering  
Specialization: Artificial Intelligence & Machine Learning

---

##  Placeko

**AI Career Copilot — Resume Intelligence • Semantic Job Matching • Personalized Interviews • AI Evaluation • Application Intelligence**
