# 🚀 Quick Deployment Guide

## 🎯 Choose Your Deployment Path

### ⚡ Fastest (Railway.app) - 5 minutes
```bash
1. Go to railway.app
2. Login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your email-triage repo
5. Add environment variable: HF_TOKEN=your_token
6. Railway auto-detects Docker and deploys!
```

✅ **Benefits:** Easiest, free tier, auto-HTTPS  
⏱️ **Time:** 5 minutes  
💰 **Cost:** Free (or $5/month)

---

### 🖥️ Local Docker (Your Machine) - 2 minutes

**Windows:**
```bash
# Make sure Docker Desktop is running
# Then run:
.\deploy.bat
```

**Mac/Linux:**
```bash
chmod +x deploy.sh
./deploy.sh
```

✅ **Benefits:** Full control, no cloud needed  
⏱️ **Time:** 2 minutes  
💰 **Cost:** Free

---

### 🐳 Docker Hub (Persistent) - 10 minutes

```bash
# Login to Docker Hub
docker login

# Build and push
docker build -t your_username/email-triage:latest .
docker push your_username/email-triage:latest

# Anyone can now run:
docker run -p 8000:8000 -e HF_TOKEN=your_token your_username/email-triage:latest
```

✅ **Benefits:** Shareable, version control  
⏱️ **Time:** 10 minutes  
💰 **Cost:** Free

---

## 📋 Pre-Deployment Checklist

```
☐ HF_TOKEN obtained from huggingface.co
☐ Docker installed (if local deployment)
☐ .env file created in project root
☐ Git repo pushed to GitHub (if cloud deployment)
☐ Port 8000 available (if local)
```

---

## 🔑 Getting Your HF_TOKEN

1. Go to [huggingface.co](https://huggingface.co)
2. Sign up or login
3. Click profile → Settings → Access Tokens
4. Create new token (read access is fine)
5. Copy token to `.env` file:

```env
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxx
```

---

## ✅ After Deployment

**Check it's working:**
```bash
curl http://your-deployed-url/health
```

**Should return:**
```json
{"status": "ok", "service": "email-triage-env"}
```

**Access the UI:**
- 📚 Swagger Docs: `http://your-deployed-url/docs`
- 🔧 ReDoc: `http://your-deployed-url/redoc`

---

## 📊 Deployment Comparison

| Platform | Time | Cost | Ease | Scaling |
|----------|------|------|------|---------|
| **Local Docker** | 2 min | Free | ⭐⭐⭐ | Low |
| **Railway** | 5 min | Free* | ⭐⭐⭐⭐⭐ | Auto |
| **Render** | 5 min | Free* | ⭐⭐⭐⭐⭐ | Manual |
| **AWS** | 15 min | $$$| ⭐⭐ | High |
| **Docker Hub** | 10 min | Free | ⭐⭐⭐⭐ | Manual |

*Free tiers have limitations

---

## 🆘 Troubleshooting

**"Docker not found"**
→ Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop)

**"Port 8000 already in use"**
→ Change port in docker-compose.yml: change `8000:8000` to `8001:8000`

**"HF_TOKEN not working"**
→ Verify token is correct and has appropriate permissions at huggingface.co

**"Container keeps restarting"**
→ Check logs: `docker-compose logs api`

---

## 🎓 Next Steps

1. **Monitor:** Setup logging and error tracking
2. **Scale:** Add load balancer for multiple instances
3. **Automate:** Setup CI/CD with GitHub Actions
4. **Secure:** Add authentication and rate limiting
5. **Optimize:** Performance tuning and caching

---

## 📞 Get Help

- 📖 Full guide: See [DEPLOYMENT.md](DEPLOYMENT.md)
- 🆘 Check logs: `docker-compose logs -f`
- 💬 API Docs: `http://localhost:8000/docs` (when running)
- 🐛 Report issues on GitHub

---

**Ready to deploy? Pick your path above and follow the instructions!** 🚀
