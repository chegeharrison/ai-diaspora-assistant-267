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

#### 1. Plain-English Request Input
Users can type requests in natural language, for example:

- `I need to send KES 15,000 to my mother in Kisumu urgently.`
- `Please verify my land title deed for the plot in Karen.`
- `Can someone clean my apartment in Westlands on Friday?`

#### 2. AI Intent Extraction
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

#### 3. Risk Scoring
Each task is assigned a risk score using backend rules based on the extracted details.

Examples:
- urgent money transfers are higher risk
- larger amounts increase transfer risk
- land/title document verification is higher risk than ordinary errands
- status checks are low risk

#### 4. Task Creation
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

#### 5. Step Generation
The app generates task-specific fulfilment steps.

#### 6. Three-Format Message Generation
Each task generates and stores:

- WhatsApp message
- Email message
- SMS message

#### 7. Employee Assignment
Tasks are assigned to an employee category based on intent:

- Finance Team
- Operations Team
- Legal Team
- Customer Support

#### 8. Task Dashboard
The dashboard displays:

- task code
- intent
- status
- risk score
- assigned team
- creation time

It also allows live status updates, which are saved immediately.

#### 9. Status History
Every status change is stored in a `StatusHistory` table to preserve an audit trail.

---

## Tech Stack

#### Backend
- Django

#### Frontend
- HTML
- CSS
- Vanilla JavaScript

#### Database
- SQLite

#### AI Provider
- Groq API
  Groq provides an OpenAI-compatible API pattern, which made it easier to integrate structured LLM calls into a Python/Django backend.

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
#### 1. Clone the repository
```bash
git clone https://github.com/chegeharrison/ai-diaspora-assistant-267
cd ai-diaspora-assistant-267
```

#### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
#### 3. Install dependencies
```bash
pip install -r requirements.txt
```
#### 4. Create the .env file
Create a .env file in the project root and add the environment variables shown below.
#### 5. Run migrations
```bash
python manage.py migrate
```
#### 6. Create a superuser
```bash
python manage.py createsuperuser
```
#### 7. Start the development server
```bash
python manage.py runserver
```
Then open:
```bash
http://127.0.0.1:8000/
```
#### 8. Environment Variables
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

#### 9. Database and SQL Dump

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

## How the Application Works

#### Step 1: Customer Submits a Request
The user enters a request in plain English.

#### Step 2: AI Analyzes the Request
The first AI call extracts:
- Intent  
- Entities  
- Fulfilment steps  

#### Step 3: Backend Validates AI Output
The backend:
- Validates intent  
- Normalizes unsupported aliases  
- Cleans blank values  
- Ensures steps are meaningful  
- Rejects incomplete or invalid outputs  

#### Step 4: Risk Calculation
A deterministic risk score and reason are calculated.

#### Step 5: Task Creation
The system:
- Saves the task  
- Generates a unique task code  
- Assigns a default status  

#### Step 6: Customer Messages Generation
A second AI call generates:
- WhatsApp message  
- Email message  
- SMS message  

This second step uses the real saved task code so the messages feel more useful and realistic.

#### Step 7: Dashboard Tracking
Tasks appear in a dashboard where status can be updated:

- Pending  
- In Progress  
- Completed  

Each status change is saved immediately and recorded in status history.

---

## Data Model

#### Task
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

#### TaskStep
Stores fulfilment steps linked to a task.

#### TaskMessage
Stores messages per channel:
- WhatsApp  
- Email  
- SMS  

#### StatusHistory
Tracks every status change.

---

## Key Design Decisions

#### Why Django
I used Django because the brief explicitly preferred Django, and it gave me a strong foundation out of the box. It provided routing, ORM, migrations, templates, and the admin interface, which helped me move quickly while keeping the project structured and explainable.

#### Why SQLite
I used SQLite because it is lightweight and easy to set up, which made it a practical choice for a timed take-home project. It also made it easy to generate the required SQL dump for submission. 

#### Why Django Templates + Vanilla JavaScript
The brief allowed only HTML, CSS, and vanilla JavaScript on the frontend, so I used Django templates for page rendering and vanilla JavaScript only where needed for interactivity, especially for live dashboard status updates. 

#### Why `base.html`
I created base.html so that all pages could inherit the same layout, navigation, and stylesheet loading. This reduced repeated code and kept the frontend consistent and easier to maintain.

#### Why I created a `services` folder inside the tasks app
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

---

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
At first, I tried generating everything in one AI call. Later I changed the design.

The final flow became:

1. First AI call for intent, entities, and steps 
2. Save the task and generate the real task code
3. Second AI call for the customer-facing messages

Made this decision because the messages needed the actual task code and saved task context to feel realistic.

#### Why I added backend validation on AI output
The model sometimes returned unsupported intent names, blank messages, or poor placeholder steps. I added backend validation to make the stored data more reliable.

Validation includes:
- Intent normalization  aliases like `schedule_service`
- Rejecting invalid intents  
- Minimum 3 meaningful steps  
- All 3 messages required  
- Converting values like (`N/A`, `None`, `null`) into empty strings

#### Why I kept risk scoring in backend Python
I deliberately kept risk scoring in backend logic instead of leaving it entirely to the AI. I did this because the risk rules needed to be deterministic, explainable, and grounded in real diaspora scenarios.

#### Why I designed the risk logic the way I did
The risk logic was built to reflect realistic concerns, for example:

- Money transfer → financial & fraud risk  
- Large amounts → higher risk  
- Urgency → increased fraud risk  
- Document verification → legal risk  
- Land/title tasks → higher sensitivity  
- Hiring → coordination risk  
- Status checks → low risk  

#### Why I used database-backed status lookup for check_status
At first, the model tried to generate status updates by itself, which caused hallucinated answers.

I changed that design so that:
- AI extracts task code  
- Backend retrieves actual task  
- The saved task status is used in the UI and messages

This made the tracking feature more trustworthy.

---


## Prompt Design
I designed the prompts to return structured, parseable results rather than conversational free text.

#### Included
- Valid intent list  
- Classification rules  
- Output structure  
- Step quality requirements  
- Message formatting rules  
- Brand consistency rules
- Clear structure for AI output

#### Excluded
- Unsupported intents  
- Vague free-form explanations 
- Unnecessary creative wording
- Overly open-ended responses

The goal was to make the AI output dependable enough to validate and save directly.



## AI Usage

AI was used for:
- Prompt design  
- Code structuring ideas  
- Debugging  
- Validation refinement  
- Message wording  
- Documentation improvement  

I still reviewed and adjusted the final implementation decisions manually

---

## Overridden AI Decisions

#### Decision Where I Overrode the AI - Status Checking
One important place where I overrode the AI was `check_status`.
The model initially tried to guess the progress of tasks. I changed the design so that the backend uses the actual saved task from the database instead.

#### Intent Normalization
I also overrode unsupported intent names such as `schedule_service` by normalizing them into the closest valid system-defined intent.

---

## Challenges and Fixes
At one point, the AI integration appeared connected, but the app was still saving weak or incorrect outputs.

##### The main problems were:
- Incorrect LLM configuration  
- Overuse of certain intents  
- Weak AI outputs  

##### Fixes
- Exposing the required LLM settings properly in Django
- Validating AI output before saving  
- Rewriting the system prompt  
- Splitting analysis and message generation into two AI calls
- Replacing hallucinated status replies with database-backed status lookups  

---

## Key Learnings

- AI output should not be trusted blindly 
- Deterministic logic improves reliability  
- Good service separation makes Django applications easier to understand and maintain  
- Backend validation is necessary even with strong prompting  

---

## Limitations

- No customer authentication
- No document upload  
- No employee database  
- No payment integration  
- No external service integrations, eg transport 

---

## Future Improvements

- Document upload support  
- Dashboard filters and search  
- Customer authentication  
- Audit logs  
- Notification systems   
- Advanced risk analytics  

---

## Final Submission Notes

This repository includes:
- Source code  
- Setup instructions  
- Structured documentation  
- SQL dump with schema and sample data  


---
## Author
Built as part of the **Vunoh Global AI Internship Practical Test**.













