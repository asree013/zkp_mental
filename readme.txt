// Active Project
source venv/bin/activate
// Install pip install

// Run Project 
uvicorn main:app --reload
//or run fix ip and port
uvicorn main:app --reload --host 0.0.0.0 --port 8000