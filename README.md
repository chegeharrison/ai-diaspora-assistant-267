# AI Diaspora Assistant

AI Diaspora Assistant is a Django-based web application built for the Vunoh Global AI Internship Practical Test.

It helps Kenyans living abroad submit and track important tasks back home using plain-English requests. The application accepts a customer request, uses AI to classify the request and extract key details, calculates a risk score, creates a structured task, assigns it to the appropriate team, generates fulfilment steps, creates customer-facing confirmation messages, and stores everything in the database for tracking and audit purposes.

---

## Project Overview

Kenyans living abroad often rely on calls, WhatsApp messages, relatives, or word of mouth to manage tasks back home. These channels are often slow, informal, and difficult to track when something goes wrong.

This project demonstrates a more structured approach through an AI-powered assistant that supports:

- sending money
- hiring local services
- verifying documents
- arranging airport transfer support
- checking the status of an existing task

The goal was to build something that works end to end, is explainable, and shows sound product and engineering decisions.

---

## Features

### 1. Plain-English Request Input
Users can type requests in natural language, for example:

- `I need to send KES 15,000 to my mother in Kisumu urgently.`
- `Please verify my land title deed for the plot in Karen.`
- `Can someone clean my apartment in Westlands on Friday?`

### 2. AI Intent Extraction
The app uses an LLM to identify a valid intent and extract entities as structured JSON.

Supported intents:

- `send_money`
- `get_airport_transfer`
- `hire_service`
- `verify_document`
- `check_status`

Example extracted entities include:

- amount
- recipient
- location
- urgency
- document type
- service type
- schedule
- task code

### 3. Risk Scoring
Each task is assigned a risk score using backend rules based on the extracted details.

Examples:
- urgent money transfers are higher risk
- larger amounts increase transfer risk
- land/title document verification is higher risk than ordinary errands
- status checks are low risk

### 4. Task Creation
Each request creates a database task with:

- unique task code
- raw request
- intent
- entities
- risk score
- risk reason
- employee assignment
- status
- timestamps

### 5. Step Generation
The app generates task-specific fulfilment steps.

### 6. Three-Format Message Generation
Each task generates and stores:

- WhatsApp message
- Email message
- SMS message

### 7. Employee Assignment
Tasks are assigned to an employee category based on intent:

- Finance Team
- Operations Team
- Legal Team
- Customer Support

### 8. Task Dashboard
The dashboard displays:

- task code
- intent
- status
- risk score
- assigned team
- creation time

It also allows live status updates, which are saved immediately.

### 9. Status History
Every status change is stored in a `StatusHistory` table to preserve an audit trail.

---

## Tech Stack

### Backend
- Django

### Frontend
- HTML
- CSS
- Vanilla JavaScript

### Database
- SQLite

### AI Provider
- Groq API

---

## Project Structure

```text
ai-diaspora-assistant-267/
├── config/
├── core/
├── tasks/
│   ├── migrations/
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── assignment_service.py
│   │   ├── risk_service.py
│   │   └── task_creator.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
├── templates/
├── static/
│   └── css/
│       └── styles.css
├── sql/
│   └── vunoh_dump.sql
├── manage.py
├── requirements.txt
├── .env.example
└── README.md

```

## Setup Instructions
### 1. Clone the repository
```bash
git clone https://github.com/chegeharrison/ai-diaspora-assistant-267
cd ai-diaspora-assistant-267
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Create the .env file
Create a .env file in the project root and add the environment variables shown below.
### 5. Run migrations
```bash
python manage.py migrate
```
### 6. Create a superuser
```bash
python manage.py createsuperuser
```
### 7. Start the development server
```bash
python manage.py runserver
```
Then open:
```bash
http://127.0.0.1:8000/
```
### 8. Environment Variables
```bash
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

APP_NAME=AI Diaspora Assistant
TIME_ZONE=Africa/Nairobi

LLM_PROVIDER=groq
LLM_API_KEY=your_groq_api_key
LLM_API_URL=https://api.groq.com/openai/v1/chat/completions
LLM_MODEL=openai/gpt-oss-20b
```

### 9. Database and SQL Dump

This project uses SQLite for local development.

A SQL dump file is included in:
```bash 
sql/vunoh_dump.sql
```
#### Contents of the SQL Dump

The dump contains:

- Database schema  
- Sample tasks  
- Extracted entities  
- Generated steps  
- Generated messages  
- Risk scores  
- Employee assignments  
- Status history  

The SQL dump is included to meet the test requirement of having a committed database with:
- Schema
- At least five complete sample tasks

---

# How the Application Works

## Step 1: Customer Submits a Request
The user enters a request in plain English.

## Step 2: AI Analyzes the Request
The first AI call extracts:
- Intent  
- Entities  
- Fulfilment steps  

## Step 3: Backend Validates AI Output
The backend:
- Validates intent  
- Normalizes unsupported aliases  
- Cleans blank values  
- Ensures steps are meaningful  
- Rejects incomplete or invalid outputs  

## Step 4: Risk Calculation
A deterministic risk score and reason are calculated.

## Step 5: Task Creation
The system:
- Saves the task  
- Generates a unique task code  
- Assigns a default status  

## Step 6: Customer Messages Generation
A second AI call generates:
- WhatsApp message  
- Email message  
- SMS message  

This second step uses the real saved task code so the messages feel more useful and realistic.

## Step 7: Dashboard Tracking
Tasks appear in a dashboard where status can be updated:

- Pending  
- In Progress  
- Completed  

Each status change is saved immediately and recorded in status history.

---

# Data Model

## Task
Stores the main task data:
- Task code  
- Raw request  
- Intent  
- Entities  
- Risk score  
- Risk reason  
- Employee assignment  
- Status  
- Created at  
- Updated at  

## TaskStep
Stores fulfilment steps linked to a task.

## TaskMessage
Stores messages per channel:
- WhatsApp  
- Email  
- SMS  

## StatusHistory
Tracks every status change.

---

# Key Design Decisions

## Why Django
I used Django because the brief explicitly preferred Django, and it gave me a strong foundation out of the box. It provided routing, ORM, migrations, templates, and the admin interface, which helped me move quickly while keeping the project structured and explainable.

## Why SQLite
I used SQLite because it is lightweight and easy to set up, which made it a practical choice for a timed take-home project. It also made it easy to generate the required SQL dump for submission. 

## Why Django Templates + Vanilla JavaScript
The brief allowed only HTML, CSS, and vanilla JavaScript on the frontend, so I used Django templates for page rendering and vanilla JavaScript only where needed for interactivity, especially for live dashboard status updates. 

## Why `base.html`
I created base.html so that all pages could inherit the same layout, navigation, and stylesheet loading. This reduced repeated code and kept the frontend consistent and easier to maintain.

## Why I created a `services` folder inside the tasks app
I created a services folder to keep the business logic separate from views and models. This made the code cleaner, easier to debug, and easier to explain. 


#### Services Breakdown

#### `ai_service.py`
Handles:
- AI request analysis  
- AI message generation
- Output validation  
- Intent normalization  
- Entity cleanup  
Separated this because the AI workflow was the most complex part of the application and deserved its own module.

#### `risk_service.py`
- Contains deterministic risk logic  
- separate so that the scoring rules remain deterministic and easy to explain.

#### `assignment_service.py`
- Maps task intents to employee categories  

#### `task_creator.py`
This file orchestrates the main workflow:
- Request AI analysis  
- Risk scoring  
- Employee Assignment  
- Task creation  
- Step creation  
- Message generation  
- Status history creation  
Separated this flow because it became the central orchestration point of the application.

## Design Choices

#### Why I used a JSON field for entities
Used because:
- Different requests require different fields  
- Avoids rigid schema constraints  

Examples:
- Money transfer → amount, recipient  
- Document verification → document type  
- Status check → task code  
A JSON field gave me flexibility without forcing too many rigid columns into the schema.

#### Why I split AI analysis and message generation into two AI calls
Instead of one:

1. Extract intent, entities, steps  
2. Save task and generate task code  
3. Generate messages using real task data  

This improves realism and accuracy.

## Backend Validation
Added because AI output can be unreliable.

Validation includes:
- Intent normalization  
- Rejecting invalid intents  
- Minimum 3 meaningful steps  
- All 3 messages required  
- Cleaning placeholders (`N/A`, `None`, `null`)  

## Backend Risk Scoring
Kept in Python to ensure:
- Deterministic behavior  
- Explainability  
- Real-world relevance  

## Risk Logic Design
Reflects real scenarios:

- Money transfer → financial & fraud risk  
- Large amounts → higher risk  
- Urgency → increased fraud risk  
- Document verification → legal risk  
- Land/title tasks → higher sensitivity  
- Hiring → coordination risk  
- Status checks → low risk  

## Database-Backed Status Checks
Instead of AI guessing:
- AI extracts task code  
- Backend retrieves actual task  
- Status is sourced from database  

Improves trust and accuracy.

## No Document Upload
Excluded because:
- Not required in the brief  
- Keeps scope focused  

---

# Prompt Design

## Included
- Valid intent list  
- Classification rules  
- Output structure  
- Step quality requirements  
- Message formatting rules  
- Brand consistency  

## Excluded
- Unsupported intents  
- Vague responses  
- Overly creative outputs  

Goal: **Structured, parseable, reliable AI output**

---

# AI Usage

AI was used for:
- Prompt design  
- Code structuring ideas  
- Debugging  
- Validation refinement  
- Message wording  
- Documentation improvement  

Final decisions were manually reviewed.

---

# Overridden AI Decisions

## Status Checking
AI initially guessed task progress → replaced with DB lookup.

## Intent Normalization
Unsupported intents (e.g., `schedule_service`) → mapped to valid ones.

---

# Challenges and Fixes

## Issues
- Incorrect LLM configuration  
- Overuse of certain intents  
- Weak AI outputs  

## Fixes
- Proper environment configuration  
- Strong validation layer  
- Improved prompts  
- Split AI workflow  
- Database-backed status checks  

---

# Key Learnings

- AI output must be validated  
- Deterministic logic improves reliability  
- Service-based architecture improves clarity  
- Strong prompts alone are not enough  

---

# Limitations

- No authentication  
- No document upload  
- No employee database  
- No payment integration  
- No external service integrations  
- No default deployment  

---

# Future Improvements

- Document upload support  
- Dashboard filters and search  
- Customer authentication  
- Audit logs  
- Notification systems  
- Public deployment  
- Advanced risk analytics  

---

# Final Submission Notes

This repository includes:
- Source code  
- Setup instructions  
- Structured documentation  
- SQL dump with schema and sample data  

The SQL dump is committed as required.

---

# Author

Built as part of the **Vunoh Global AI Internship Practical Test**.






## 




## Chunk 1

## Chunk 2### Decision: Build the request-intake and task-creation flow before real AI integration
I chose to first build a working request submission pipeline that accepts user input, extracts a provisional intent/entities structure, calculates risk, assigns the task, and stores everything in the database. I did this so I could validate the end-to-end application flow before introducing external LLM API complexity. This made debugging easier and ensured the database and business logic were stable before integrating AI-generated outputs.

## Decisions I made and why

### Why I used Django
I chose Django because the test brief explicitly listed Django as the preferred backend option. It also helped me move faster by providing built-in admin, ORM, routing, migrations, and template rendering.

### Why I used SQLite
I used SQLite for the build phase because it is lightweight and fast to set up, which was practical for a timed take-home project. It allowed me to focus on application logic first, while still meeting the requirement for database persistence and SQL export later.

### Why I created a shared base template
I created `base.html` so the pages could reuse a common layout, navigation, and shared styling. This reduced repeated code and made the frontend structure cleaner and easier to maintain.

### Why I separated the logic into service files
I split the business logic into service files such as `ai_service.py`, `risk_service.py`, `assignment_service.py`, and `task_creator.py`. I did this so that the Django views would stay simple and the logic would be easier to test, debug, and explain.

### Why I used a JSON field for extracted entities
I stored extracted entities in a JSON field because each intent has a slightly different set of useful details. For example, a money transfer request needs amount and recipient information, while a document verification request needs document type and location. A JSON field gave me flexibility without overcomplicating the schema.

### Why I used Groq
I chose Groq because it provides an OpenAI-compatible API pattern, which made it easier to integrate structured LLM calls into a Python/Django backend. This let me focus on prompt design, validation, and persistence rather than provider-specific SDK complexity.

### Why I split task analysis and message generation into two AI calls
I initially generated intent, steps, and messages in one AI call, but I later changed the design. I split the workflow into:
1. AI analysis for intent, entities, and fulfilment steps
2. task creation in the database to generate the real task code
3. a second AI call to generate WhatsApp, Email, and SMS messages using the saved task details

I made this change because the final messages needed the actual task code and task context to feel realistic and useful.

### Why I added backend validation on AI output
I found that the model could sometimes return unsupported intent names like `schedule_service` or low-quality placeholder steps. To make the output reliable, I added backend validation to:
- normalize unsupported aliases to the closest valid intent
- reject invalid intents
- require at least 3 meaningful steps
- require non-empty WhatsApp, Email, and SMS messages

This improved consistency and made the saved data more trustworthy.

### Why I kept risk scoring in backend Python instead of leaving it fully to the AI
I kept the final risk score in backend logic so it would stay deterministic, explainable, and grounded in the Kenyan diaspora context. This was important because the brief specifically asked for risk scoring logic that I could explain clearly.

### Why I used separate models for tasks, steps, messages, and status history
I created separate related models so the system could persist all required outputs clearly:
- main task
- generated fulfilment steps
- three-format customer messages
- status change history

This matched the requirement that everything be saved and visible in the application.

### One thing that did not work as expected and how I resolved it
At first, my LLM integration was silently falling back to generic default responses, which caused requests like airport pickup and money transfer to be misclassified. I debugged this by checking whether Django was correctly loading the Groq environment variables and by surfacing real errors instead of hiding them behind fallback logic. After fixing the configuration and improving the AI validation layer, the intent classification became much more reliable.

### One decision where I overrode what the AI suggested
In some cases, the LLM returned unsupported intent names such as `schedule_service`, or produced low-quality placeholder steps. Instead of saving that output directly, I added backend validation and normalization rules. For example, I mapped `schedule_service` to `hire_service` and rejected outputs that did not meet the expected structure. I did this to keep the workflow aligned with the test specification.