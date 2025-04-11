# Unified Dev Assistant

The **Unified Dev Assistant** is a versatile application that leverages LangChain, OpenAI, and Git to assist developers by summarizing PRs, generating test cases, visualizing code structures, and more.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Framework and Tools](#framework-and-tools)
- [Project Setup](#project-setup)
- [How to Run](#how-to-run)
- [Video Demonstration](#video-demonstration)
- [Future Scope](#future-scope)

## Overview

The Unified Dev Assistant is an AI powered developer assistant. It summarizes PR changes as soon as a PR is created, generates test cases on the PR, generates mermaids showing differences in code, suggests improvements, and posts all this as a comment on github!

## Features

An AI-powered tool that automatically analyzes GitHub pull requests and local codebases, performing the following actions:

-   Efficient Github Interaction (Read PR data such as old and new files, post comments onto Github)
-   Review Pull Requests
-   Summarize code changes in a PR in a clear and concise format.
-   Flag risky or complex changes for human review.
-   Suggest missing or necessary test cases based on the diff.
-   Generate mermaid on code changes before and after.
-   Auto-Tag and Summarize Issues: (Future)
    -   When a PR is linked to issues (or when analyzing standalone issues), automatically summarize the issue and apply intelligent tags (e.g., bug, enhancement, documentation).
    -   Suggest relevant tests if the issue describes a bug.
-   Post the above info as a comment on the github PR.

**Modes of Operation:**
-   **GitHub Integration:** Works automatically when a new pull request is opened or updated.
-   **Standalone App (Future):** Works as a standalone app supporting 


## Framework and Tools

| Purpose                             | Library/Tool                | Install Command               |
|-------------------------------------|-----------------------------|-------------------------------|
| AI Models and LLMs                  | openai                      | `pip install openai`          |
| LangChain Framework                 | langchain                   | `pip install langchain`       |
| GitHub API access                   | PyGithub                    | `pip install PyGithub`        |
| Web App (optional for UI later)     | fastapi, uvicorn            | `pip install fastapi uvicorn` |
| Environment Variables (API keys)    | python-dotenv               | `pip install python-dotenv`   |
| Mermaid Diagram Generation          | (No Python lib needed)      |  generate Mermaid syntax text |
| Git (for local PR diffs)            | GitPython                   | `pip install GitPython`       |
| Parsing and Diffing Files           | difflib, os, pathlib        | Already included with Python  |

## Project Setup

### 1. Fork Clone the repository
First, fork the repository to your personal repo in github. Then, clone the repository to your local machine:

```bash
git clone https://github.com/varshabhat42/unified-dev-assistant.git
cd unified-dev-assistant
```

### 2. Install the required dependencies
Make sure you have Python 3.8+ installed. You can install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

### 3. Set up OpenAI API Key and Github Token
Before running the application, you'll need to create an OpenAI API Key.

How to create an OpenAI API Key:

Visit the OpenAI platform.
Generate a new API key and copy it.
Once you have the API key, add it to the .env.

How to create a github token:
Visit Github platform (logged in) -> Settings -> Developer settings -> Personal Access Tokens -> Token (classic). Give atleast repo, workflow, write:packages, gist, notifications, write:discussion, project permissions. 
**Note:** DO NOT use fine-grained tokens, they might cause issues

How to use these keys:
Create a .env file in the root directory (if not present). Add the below lines to it


```bash
OPENAI_API_KEY="your_api_key_here"
GITHUB_TOKEN="your_github_token"
GITHUB_REPO=varshabhat42/unified-dev-assistant
```

### 4. Additional installation 
You will also need to install ngork to test the working
Chocoletey is the easiest way to install ngork for Windows. Use the command below after chocoletey installation to install ngork. Make sure you run Windows PowerShell as administrator

```bash
choco install ngrok
```


## How to Run
Preferred environment: VSCode
Open the project in vscode, and the a terminal. Use the following commands - 

```bash
.\venv\Scripts\Activate
uvicorn app.main:app
```

You should see a message saying "INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)"
Keep this terminal open. Now open powershell and type the below command. Keep this powershell window open as well.

```bash
ngrok http 8000
```

Ngork spits out a forwarding URL with the message "Forwarding                    https://6903-2601-646-827e-7b20-ac2c-50f4-f402-b51c.ngrok-free.app -> http://localhost:800"

Copy this URL, go to this repository, go to repository settings -> webhooks -> paste the payload URL in the below format. Pay attention to "/webhook" appended at the end. Set the content type to application/json, enable SSL verification, click let me select individual events -> Pull request. Also make sure "Active" is checked and click "Update/Create webhook"

As your app is already running through steps above, github will attempt to ping the app, and you should see a ping coming through both on your ngork terminal and application logs in VSCode terminal.

```bash
https://6903-2601-646-827e-7b20-ac2c-50f4-f402-b51c.ngrok-free.app/webhook
```

We are now ready to see the app work!

Now go to this github repo, and create a new branch. Name it "my_new_branch_1"
Make a change in the ai_service.py file. Add a simple method as below at the end of the file. Commit it to the branch and open a PR. DO NOT MERGE THE PR TO MAIN. And that's it! You should see the logs coming through, our app generating comments based on LIVE data, generating test cases and generating mermaids.
After the app has run successfully, you will see a comment on the PR.

```python
def divide(self, a, b):
    return a/b
```

## Video Demonstration
A link to the working of the app from start to finish has been provided below - 
https://www.youtube.com/watch?v=TmYX_F8Rtk0


## Future Work
For the purposes of Hackathon, this tool only has limited functionality, but it can be so much more!

Some add on features include:
- Build as standalone app, with repository names passed through env_variables. This provides scalability to all repositories
- Provide additional features, such as issue tagging
- Allow app to run in other modes, which will allow documentation generation for ANY Repo, mermaid diagrams for ANY repo. Very useful for an overall design of the system
- Auto-Tag and Summarize Issues:
    -   When a PR is linked to issues (or when analyzing standalone issues), automatically summarize the issue and apply intelligent tags (e.g., bug, enhancement, documentation).
    -   Suggest relevant tests if the issue describes a bug.
- Known issue: As the mermaids are AI generated, the mermaid syntax output is sometimes incorrect. Solution: Refine the prompt and add some parsing logic after AI generates the mermaid for an easy fix.