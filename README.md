# 👁️ RepoMind Vision
> **The World's First Multimodal Whole-Repo Debugger powered by Gemini 2.5.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Powered by Gemini](https://img.shields.io/badge/Powered%20by-Gemini%202.5%20Flash-4c8bf5)](https://ai.google.dev/)

## 🔴 The Problem: "The Blind AI Paradox"
Developers spend 50% of their time fixing UI/UX bugs. Current AI tools (like GitHub Copilot or ChatGPT) are **blind**.
*   They can read code, but they can't see what the user sees.
*   They have limited context windows, making it impossible to debug complex interactions between 50+ files.

## 🟢 The Solution: RepoMind Vision
RepoMind is a **Multimodal Debugger** that ingests your **Entire Codebase** AND **Screenshots** simultaneously.

By leveraging the massive context window and vision capabilities of **Google Gemini 2.5 Flash**, it correlates pixel-level visual errors with logic-level code definitions.

## ✨ Key Features
*   **Whole-Repo Context:** Upload a `.zip` of your project. We ingest 1M+ tokens instantly.
*   **Multimodal Vision:** Upload a screenshot of the bug. The AI "looks" at the UI while reading the code.
*   **Gemini 2.5 Flash Engine:** Powered by Google's latest, fastest model for real-time debugging.

## 🛠️ How it Works
1.  **Upload Code:** The user uploads a ZIP file of their project.
2.  **Upload Evidence:** The user uploads a screenshot of the visual bug.
3.  **Analysis:** RepoMind Vision uses Gemini 2.5 to cross-reference the visual artifacts (e.g., "invisible button") with the CSS/JS code (e.g., `opacity: 0.0`).
4.  **Fix:** The AI provides the exact file name, line number, and corrected code.

## 🚀 How to Run Locally
1. Clone the repo: https://github.com/Chirag-sharma001/RepoMind.git
2. Install dependencies: pip install -r requirements.txt
3. Run the app: streamlit run app.py

👥 Team
Built with ❤️ at CODESPIRE 3.0 (AITR Indore)
