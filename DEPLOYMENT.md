# GitHub & Railway Deployment Guide

## 📋 Prerequisites
- GitHub account
- Railway account (sign up at https://railway.app)
- Git installed locally

---

## 🚀 Step 1: Push to GitHub

### 1. Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `multilingual-complaint-classifier`
3. Description: `Multilingual municipal complaint classification API using ML`
4. Make it **Public** (for Railway free tier)
5. **Do NOT** initialize with README (we already have one)
6. Click "Create repository"

### 2. Connect Local Repository to GitHub

```powershell
# Add remote origin (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/multilingual-complaint-classifier.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Your code is now on GitHub!** ✅

---

## 🚂 Step 2: Deploy to Railway

### Option A: Deploy via Railway Dashboard (Recommended)

1. **Go to Railway**: https://railway.app
2. **Sign in** with GitHub
3. **New Project** → "Deploy from GitHub repo"
4. **Select your repository**: `multilingual-complaint-classifier`
5. Railway will automatically:
   - Detect Python project
   - Install dependencies from `requirements.txt`
   - Use `Procfile` for startup command
   - Assign a public URL

6. **Wait for deployment** (2-3 minutes)
7. **Get your URL**: Click on your project → Settings → Generate Domain

### Option B: Deploy via Railway CLI

```powershell
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

---

## 🌐 Step 3: Test Your Deployed API

Once deployed, you'll get a URL like: `https://your-app.up.railway.app`

### Test Endpoints

```bash
# Health check
curl https://your-app.up.railway.app/health

# Single prediction
curl -X POST "https://your-app.up.railway.app/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "The road has many potholes"}'

# Interactive docs
https://your-app.up.railway.app/docs
```

---

## 📝 Quick Commands Reference

### Git Commands
```powershell
# Check status
git status

# Add changes
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main
```

### Railway Commands
```powershell
# Check logs
railway logs

# Open in browser
railway open

# Add environment variable
railway variables set KEY=VALUE

# Restart service
railway restart
```

---

## 🔧 Configuration (Optional)

### Environment Variables on Railway

1. Go to your Railway project
2. Click on your service
3. Go to **Variables** tab
4. Add:
   ```
   PORT=8000
   MODEL_PATH=models/multilingual_classifier_improved.pkl
   ```

### Custom Domain

1. Go to **Settings** → **Networking**
2. Click **Generate Domain** (free subdomain)
3. Or add your custom domain

---

## 🐛 Troubleshooting

### Build Failed
- Check Railway logs: `railway logs`
- Ensure `requirements.txt` has correct versions
- Model file size should be < 100MB

### API Not Responding
- Check if service is running in Railway dashboard
- Verify environment variables
- Check logs for errors

### Model Not Loading
- Ensure `models/` folder is committed to Git
- Check `MODEL_PATH` environment variable
- Verify `.gitignore` isn't excluding model file

---

## 📊 Monitor Your Deployment

### Railway Dashboard
- View logs in real-time
- Monitor CPU/Memory usage
- Check deployment history
- Set up custom domains

### Health Endpoint
```bash
curl https://your-app.up.railway.app/health
```

---

## 🎉 Success Checklist

- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] Service deployed successfully
- [ ] Public URL working
- [ ] `/health` endpoint returns 200
- [ ] `/docs` showing Swagger UI
- [ ] Test prediction working
- [ ] Model loaded successfully

---

## 🔄 Update Your Deployment

```powershell
# Make changes to your code
# ...

# Commit and push
git add .
git commit -m "Update: description of changes"
git push origin main

# Railway will auto-deploy!
```

Railway automatically redeploys when you push to `main` branch! 🚀

---

## 💡 Tips

1. **Free Tier Limits**: Railway provides $5/month free credit
2. **Cold Starts**: First request may be slow (15-30 seconds)
3. **Logs**: Always check logs if something doesn't work
4. **Documentation**: Keep `/docs` endpoint for testing
5. **Version Control**: Always commit before pushing

---

## 🆘 Need Help?

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **GitHub Issues**: Create an issue in your repo

---

**Your API is now live and accessible worldwide!** 🌍✨
