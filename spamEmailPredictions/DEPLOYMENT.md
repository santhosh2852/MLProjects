# Deployment Guide

You asked to deploy this project to Vercel using Docker. It is important to note that **Vercel does not support deploying Docker containers directly**. Vercel is designed for static sites, Next.js, and Serverless Functions.

However, I have set up your project to support **two robust deployment strategies** that achieve your goal:

1.  **Hybrid Deployment (Recommended for Docker usage)**:
    *   **Frontend**: Deployed to Vercel (Native Next.js support).
    *   **Backend**: Deployed to **Render** (or Railway/Fly.io) using the **Dockerfiles** I created. This gives you the full Docker containerization you asked for.

2.  **Full Vercel Deployment**:
    *   **Frontend**: Deployed to Vercel.
    *   **Backend**: Deployed to Vercel as **Serverless Functions**. I added a `vercel.json` to make this possible.

---

## 1. Local Development (with Docker)

You can now run the entire stack locally using Docker Compose:

```bash
docker-compose up --build
```

*   **Frontend**: http://localhost:3000
*   **Backend**: http://localhost:8000

---

## 2. Hybrid Deployment (Frontend on Vercel, Backend on Render)

This is the best way to use Docker for your backend.

### Step A: Deploy Backend to Render
1.  Push your code to GitHub.
2.  Go to [Render Dashboard](https://dashboard.render.com/).
3.  Click **New +** -> **Web Service**.
4.  Connect your GitHub repository.
5.  Select the **backend** directory as the Root Directory (if asked) or just configure the build context.
    *   **Root Directory**: `backend`
    *   **Runtime**: Docker
6.  Render will automatically detect the `Dockerfile` in the `backend` folder and build it.
7.  Once deployed, copy the **Backend URL** (e.g., `https://spam-backend.onrender.com`).

### Step B: Deploy Frontend to Vercel
1.  Go to [Vercel Dashboard](https://vercel.com/).
2.  Click **Add New...** -> **Project**.
3.  Import your GitHub repository.
4.  Configure the project:
    *   **Root Directory**: `frontend` (Click "Edit" next to Root Directory and select `frontend`).
    *   **Framework Preset**: Next.js (Auto-detected).
5.  **Environment Variables**:
    *   Add a new variable:
        *   **Name**: `NEXT_PUBLIC_API_URL`
        *   **Value**: Your Render Backend URL (e.g., `https://spam-backend.onrender.com`).
        *   *Note: Do not add a trailing slash.*
6.  Click **Deploy**.

---

## 3. Full Vercel Deployment (Serverless)

If you prefer to keep everything on Vercel (without Docker for the backend):

### Step A: Deploy Backend
1.  Import the repo to Vercel *again* (or as a separate project).
2.  **Root Directory**: `backend`.
3.  Vercel will detect the `vercel.json` I created and deploy it as a Python Serverless Function.
4.  Copy the **Backend URL** (e.g., `https://my-spam-backend.vercel.app`).

### Step B: Deploy Frontend
1.  Same as above (Root Directory: `frontend`).
2.  Set `NEXT_PUBLIC_API_URL` to the Vercel Backend URL.

---

## Summary of Changes Made
*   **Frontend**: Updated `SpamChecker.tsx` to use `NEXT_PUBLIC_API_URL`. Added `Dockerfile`.
*   **Backend**: Added `Dockerfile` and `vercel.json`.
*   **Root**: Added `docker-compose.yml`.
