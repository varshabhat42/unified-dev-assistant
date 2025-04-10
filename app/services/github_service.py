# app/services/github_service.py

import requests
from app.config import GITHUB_TOKEN, GITHUB_REPO

class GitHubService:
    def __init__(self):
        self.base_url = f"https://api.github.com/repos/{GITHUB_REPO}"
        self.headers = {
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get_pr_files(self, pr_number: int):
        url = f"{self.base_url}/pulls/{pr_number}/files"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_file_content(self, pr_number: int, filename: str):
        url = f"{self.base_url}/pulls/{pr_number}/files"
        response = requests.get(url, headers=self.headers)
        files = response.json()
        for file in files:
            if file['filename'] == filename:
                return file['patch']  # Returns the file content (diffs)
        return ""

    def comment_on_pr(self, pr_number: int, comment: str):
        url = f"{self.base_url}/issues/{pr_number}/comments"
        payload = {"body": comment}
        response = requests.post(url, json=payload, headers=self.headers)
        return response.json()

    async def process_pull_request(self, pr_data):
        pr_number = pr_data.get('number')
        pr_files = self.get_pr_files(pr_number)

        # Extract PR changes, files, etc.
        changes = [file['filename'] for file in pr_files]
        
        # Process these files with the AI service
        print(f"Processing PR #{pr_number} with files: {changes}")