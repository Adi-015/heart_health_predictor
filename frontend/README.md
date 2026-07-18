# Frontend — Heart Health Predictor

React + Vite + Tailwind single-page app. Submits patient data to the FastAPI backend and displays risk prediction with SHAP explanations.

## Local dev

```bash
cd frontend
cp .env.example .env          # then edit VITE_API_URL to point at your backend
npm install
npm run dev                   # http://localhost:5173
```

## Deploying to Vercel

1. Push branch to GitHub.
2. Go to [vercel.com](https://vercel.com) → **Add New Project** → import your repo.
3. Set **Root Directory** to `frontend`.
4. Vercel auto-detects Vite — build command (`npm run build`) and output dir (`dist`) are already set in `vercel.json`.
5. Add environment variable in the Vercel dashboard:
   - `VITE_API_URL` = `https://your-render-backend-url.onrender.com`
6. Click **Deploy**.

> Variables starting with `VITE_` are inlined at build time by Vite. Set them in the Vercel dashboard before deploying, not after.
