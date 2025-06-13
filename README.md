# Cloud Computing with FastAPI & Firebase

This project was originally built as part of a cloud computing course. It uses **FastAPI** as the backend framework and connects to **Google Firebase** using direct REST API calls and an authorization key (instead of the Firestore Python client).

#⚙️ Key Features

- FastAPI-based backend with endpoints for managing teams and drivers
- Firebase used as the backend database (manual API integration)
- Simple HTML/CSS frontend
- Authentication handled via API key
- Good UI layout and design

# 🔍 Notes

This project does **not** use the official Firestore Python library. Instead, it manually sends HTTP requests to Firebase using an API key.  
During grading, the evaluator couldn’t run the code fully due to the missing `serviceAccountKey.json` file (which was excluded for security).

#📚 What I Learned

- How to use FastAPI to build clean REST APIs
- Manual handling of authentication with Firebase
- Frontend integration with backend APIs
- The importance of providing setup files for reproducibility

#🚫 Excluded Files

For security reasons, the Firebase service account key JSON file is not included.

---

> 🔐 To run this project, you'll need your own Firebase project and `serviceAccountKey.json`.
