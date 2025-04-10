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

        logger.info(f"Received event: {event}")

        # Handle Pull Request events
        if event == "pull_request":
            action = payload.get("action")
            logger.info(f"Pull request action: {action}")

            if action in ["opened", "synchronize"]:
                pr_data = payload.get("pull_request", {})
                pr_number = pr_data.get('number')
                logger.info(f"Processing pull request #{pr_number}")

                # Step 1: Fetch files in the PR
                pr_files = github_service.get_pr_files(pr_number)
                file_changes = [file['filename'] for file in pr_files]
                logger.info(f"Files changed in PR #{pr_number}: {file_changes}")

                # Step 2: Summarize code changes using AI
                summaries = []
                for file in file_changes:
                    logger.info(f"Fetching content for file: {file}")
                    code = github_service.get_file_content(pr_number, file)
                    logger.debug(f"Code content for {file}: {code[:100]}...")  # Log first 100 characters of the code
                    summary = ai_service.summarize_code(code)
                    logger.info(f"Summary for {file}: {summary}")
                    summaries.append(f"File: {file} - Summary: {summary}")

                # Step 3: Suggest test cases for each file
                test_case_suggestions = []
                for file in file_changes:
                    logger.info(f"Generating test cases for file: {file}")
                    code = github_service.get_file_content(pr_number, file)
                    test_case = ai_service.generate_test_case(code)
                    logger.info(f"Test cases for {file}: {test_case}")
                    test_case_suggestions.append(f"Test Cases for {file}: {test_case}")

                # Step 4: Detect missing docstrings and generate them
                missing_docstrings = []
                for file in file_changes:
                    logger.info(f"Detecting missing docstrings in file: {file}")
                    code = github_service.get_file_content(pr_number, file)
                    missing = doc_service.detect_missing_docstrings(code)
                    if missing:
                        logger.warning(f"Missing docstrings in file {file}: {missing}")
                        missing_docstrings.append(f"Missing docstrings in file {file}: {missing}")

                # Step 5: Generate Mermaid.js diagram for code structure
                # diagram = ""
                # for file in file_changes:
                #     logger.info(f"Generating diagram for file: {file}")
                #     code = github_service.get_file_content(pr_number, file)
                #     diagram_part = diagram_service.generate_diagram(code)
                #     logger.debug(f"Diagram for {file}: {diagram_part}")
                #     diagram += diagram_part
                # diagram = ""
                # for file in file_changes:
                #     logger.info(f"Generating diagram for file: {file}")
                #     code = github_service.get_file_content(pr_number, file)
                #     diagram_part = ai_service.generate_diagram(code)  # Use AI to generate the diagram
                #     logger.debug(f"Diagram for {file}: {diagram_part}")
                #     diagram += diagram_part
                diagram = ""
                for file in file_changes:
                    # Skip non-code files (e.g., text files)
                    if not file.endswith(('.py', '.js', '.java', '.ts')):  # You can adjust the file types as needed
                        continue
                    
                    logger.info(f"Generating diagram for file: {file}")

                    # Fetch the "before" code (previous commit version)
                    previous_code = github_service.get_previous_file_content(pr_number, file)
                    
                    # Fetch the "after" code (current version)
                    current_code = github_service.get_file_content(pr_number, file)

                    # Generate Mermaid diagrams for both the before and after versions of the code
                    before_diagram = ai_service.generate_diagram(previous_code)
                    after_diagram = ai_service.generate_diagram(current_code)
                    
                    # Combine both diagrams
                    # diagram += f"### Before Code Changes for {file}\n```mermaid\n{before_diagram}\n```\n\n"
                    # diagram += f"### After Code Changes for {file}\n```mermaid\n{after_diagram}\n```\n\n"
                    diagram = f"### Before Code Changes for {file}\n{before_diagram}\n\n"
                    diagram += f"### After Code Changes for {file}\n{after_diagram}\n\n"

                # Step 6: Comment back on the PR
                comments = "\n".join(summaries + test_case_suggestions + missing_docstrings + [diagram])
                logger.info(f"Posting comment to PR #{pr_number}")
                github_service.comment_on_pr(pr_number, comments)

                logger.info(f"PR #{pr_number} processed successfully")
                return {"message": "PR processed successfully"}
        logger.info("Event ignored")
        return {"message": "Event ignored"}
    
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}", exc_info=True)
        return {"message": "Error processing webhook", "error": str(e)}