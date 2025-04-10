# app/main.py
from fastapi import FastAPI, Request
from app.services.github_service import GitHubService
from app.services.ai_service import AIService
from app.services.doc_service import DocService
from app.services.diagram_service import DiagramService
from app.utils.logger import logger

app = FastAPI()

# Initialize services
github_service = GitHubService()
ai_service = AIService()
doc_service = DocService()
diagram_service = DiagramService()

@app.post("/webhook")
async def github_webhook(request: Request):
    try:
        # Get the GitHub webhook payload
        payload = await request.json()
        event = request.headers.get('X-GitHub-Event')

        # Handle Pull Request events
        if event == "pull_request":
            action = payload.get("action")
            if action in ["opened", "synchronize"]:
                pr_data = payload.get("pull_request", {})
                pr_number = pr_data.get('number')
                
                # Step 1: Fetch files in the PR
                pr_files = github_service.get_pr_files(pr_number)
                file_changes = [file['filename'] for file in pr_files]

                # Log the files changed in the PR
                logger.info(f"Processing PR #{pr_number} with files: {file_changes}")
                
                # Step 2: Summarize code changes using AI
                summaries = []
                for file in file_changes:
                    code = github_service.get_file_content(pr_number, file)  # Fetch file content (we will implement this method next)
                    summary = ai_service.summarize_code(code)
                    summaries.append(f"File: {file} - Summary: {summary}")
                
                # Step 3: Suggest test cases for each file
                test_case_suggestions = []
                for file in file_changes:
                    code = github_service.get_file_content(pr_number, file)
                    test_case = ai_service.generate_test_case(code)
                    test_case_suggestions.append(f"Test Cases for {file}: {test_case}")
                
                # Step 4: Detect missing docstrings and generate them
                missing_docstrings = []
                for file in file_changes:
                    code = github_service.get_file_content(pr_number, file)
                    missing = doc_service.detect_missing_docstrings(code)
                    if missing:
                        missing_docstrings.append(f"Missing docstrings in file {file}: {missing}")

                # Step 5: Generate Mermaid.js diagram for code structure
                diagram = ""
                for file in file_changes:
                    code = github_service.get_file_content(pr_number, file)
                    diagram += diagram_service.generate_diagram(code)
                
                # Step 6: Comment back on the PR
                comments = "\n".join(summaries + test_case_suggestions + missing_docstrings + [diagram])
                github_service.comment_on_pr(pr_number, comments)

                return {"message": "PR processed successfully"}
        return {"message": "Event ignored"}
    
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return {"message": "Error processing webhook", "error": str(e)}