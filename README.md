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
