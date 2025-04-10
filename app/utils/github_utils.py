# app/utils/github_utils.py

import requests
from app.config import GITHUB_TOKEN, GITHUB_REPO

def fetch_github_data(endpoint: str):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/{endpoint}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    return response.json()
