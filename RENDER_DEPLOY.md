# 🚀 Deploying TrueVal on Render

## 1. Prerequisites
- A Render account (https://render.com)
- A GitHub repo containing your codebase

## 2. Setup on Render
1. Log in to [Render](https://render.com) and click “New Web Service”
2. Connect your GitHub repo and pick your TrueVal repo
3. Configure:
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Set environment variables if needed in the Render dashboard

## 3. Port Binding
Make sure Flask app is set to run on `0.0.0.0` and uses port `5000` or the environment variable `PORT`.

```python
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
```

## 4. Done
Click "Create Web Service" and wait for your app to build & deploy.
