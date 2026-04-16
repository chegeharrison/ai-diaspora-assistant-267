# AI Diaspora Assistant

AI-powered web application for helping Kenyans living abroad initiate and track tasks back home.

## Planned features
- Send money
- Hire local services
- Verify documents
- Check task status
- Airport transfer support

## Tech stack
- Backend: Django
- Frontend: HTML, CSS, Vanilla JavaScript
- Database: SQLite
- AI: LLM API integration coming next

 ## Chunk 1

 ## Chunk 2
 ### Decision: Build the request-intake and task-creation flow before real AI integration
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