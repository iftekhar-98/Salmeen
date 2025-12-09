# 🚀 Deploy Salmeen to Streamlit Cloud - Step by Step

## ⏱️ Total Time: ~10 minutes

This guide will help you deploy your Salmeen platform permanently with a public URL that never expires.

---

## 📋 Prerequisites

- GitHub account (free) - [Sign up here](https://github.com/join)
- Streamlit Cloud account (free) - [Sign up here](https://share.streamlit.io/signup)

---

## 🎯 Step 1: Extract the Project (1 minute)

1. **Download** the `salmeen-mvp.tar.gz` file (already attached)

2. **Extract** it:
   - **Windows**: Right-click → Extract All
   - **Mac/Linux**: 
     ```bash
     tar -xzf salmeen-mvp.tar.gz
     cd salmeen
     ```

3. **Verify** you see these files:
   ```
   salmeen/
   ├── .streamlit/
   │   └── config.toml
   ├── app.py
   ├── model.py
   ├── utils.py
   ├── driving_data.csv
   ├── requirements.txt
   ├── packages.txt
   └── README.md
   ```

---

## 🐙 Step 2: Create GitHub Repository (3 minutes)

### 2.1 Create New Repository

1. Go to **https://github.com/new**

2. Fill in the details:
   - **Repository name**: `salmeen` (or any name you prefer)
   - **Description**: `Saudi Smart Traffic Safety Platform - Hackathon MVP`
   - **Visibility**: ✅ **Public** (required for free Streamlit deployment)
   - ❌ **DO NOT** check "Add a README file"
   - ❌ **DO NOT** add .gitignore or license

3. Click **"Create repository"**

### 2.2 Push Your Code

You'll see a page with instructions. Follow the **"push an existing repository"** section:

```bash
cd salmeen

# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit - Salmeen MVP"

# Add your GitHub repository
git remote add origin https://github.com/YOUR_USERNAME/salmeen.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

**Replace `YOUR_USERNAME`** with your actual GitHub username!

### 2.3 Verify Upload

1. Refresh your GitHub repository page
2. You should see all files uploaded
3. ✅ Confirm you see: `app.py`, `model.py`, `utils.py`, `requirements.txt`

---

## ☁️ Step 3: Deploy to Streamlit Cloud (5 minutes)

### 3.1 Sign Up / Log In

1. Go to **https://share.streamlit.io**

2. Click **"Sign up"** or **"Sign in"**

3. Choose **"Continue with GitHub"**

4. Authorize Streamlit to access your GitHub repositories

### 3.2 Create New App

1. Click **"New app"** button (top right)

2. Fill in the deployment form:

   **Repository:**
   - Select: `YOUR_USERNAME/salmeen`
   
   **Branch:**
   - Select: `main`
   
   **Main file path:**
   - Enter: `app.py`
   
   **App URL (optional):**
   - Leave default OR customize: `salmeen-saudi-traffic` (or any unique name)

3. Click **"Deploy!"**

### 3.3 Wait for Deployment

- ⏳ Streamlit will install dependencies (2-3 minutes)
- 📦 You'll see logs showing installation progress
- ✅ When complete, your app will automatically load

### 3.4 Get Your Permanent URL

Your app will be live at:
```
https://YOUR_APP_NAME.streamlit.app
```

Example: `https://salmeen-saudi-traffic.streamlit.app`

**This URL is permanent and publicly accessible!** 🎉

---

## ✅ Step 4: Verify Deployment (1 minute)

### Test Your Live App

1. **Check the URL** - Should load the Salmeen homepage

2. **Test Citizen View**:
   - Click "👤 الملف الشخصي" in sidebar
   - Verify safety score gauge appears
   - Check score history chart loads
   - Read AI recommendations

3. **Test Ministry Dashboard**:
   - Click "🏛️ لوحة التحكم الوزارية" in sidebar
   - Verify heatmap loads (may take a few seconds)
   - Check analytics charts appear

4. **Test Arabic RTL**:
   - Confirm all text is right-aligned
   - Verify Arabic text renders correctly

---

## 🎨 Step 5: Customize (Optional)

### Change App Settings

In Streamlit Cloud dashboard:

1. Click **"⚙️ Settings"** (on your app page)

2. **Secrets** (for future API keys):
   ```toml
   # Add when you integrate real APIs
   ABSHER_API_KEY = "your-key-here"
   ```

3. **Resources** (if needed):
   - Free tier: 1 GB RAM (sufficient for MVP)
   - Upgrade available if needed

### Update Your App

Whenever you push changes to GitHub:

```bash
cd salmeen
# Make your changes to files
git add .
git commit -m "Update: description of changes"
git push
```

**Streamlit Cloud auto-deploys** within 1-2 minutes! 🚀

---

## 📱 Step 6: Share Your App

### Get Shareable Link

Your permanent URL:
```
https://YOUR_APP_NAME.streamlit.app
```

### Share Options

1. **Direct Link**: Copy and share the URL

2. **QR Code**: Use a QR code generator with your URL

3. **Embed**: Add to your website:
   ```html
   <iframe src="https://YOUR_APP_NAME.streamlit.app" 
           width="100%" height="800px"></iframe>
   ```

4. **Social Media**: Share on Twitter, LinkedIn, etc.

---

## 🔧 Troubleshooting

### Issue: "Module not found" error

**Solution**: Check `requirements.txt` includes all dependencies
```bash
# Verify requirements.txt has:
streamlit>=1.28.0
scikit-learn>=1.3.0
pydeck>=0.8.0
plotly>=5.17.0
pandas>=2.0.0
numpy>=1.24.0
```

### Issue: App won't load / keeps spinning

**Solution**: 
1. Check Streamlit Cloud logs for errors
2. Click "Manage app" → "Logs"
3. Look for red error messages
4. Common fix: Restart the app (⋮ menu → Reboot)

### Issue: Heatmap not showing

**Solution**: PyDeck maps need a moment to load
- Wait 5-10 seconds
- Refresh the page
- Check browser console for errors

### Issue: Arabic text shows as boxes

**Solution**: 
- Use Chrome or Firefox (best Arabic support)
- Clear browser cache
- Ensure UTF-8 encoding in CSV

### Issue: "This app has gone to sleep"

**Solution**: 
- Free tier apps sleep after inactivity
- Just click to wake it up (takes 10 seconds)
- Upgrade to prevent sleeping

---

## 💰 Cost & Limits

### Free Tier (Current)
- ✅ Unlimited public apps
- ✅ 1 GB RAM per app
- ✅ Unlimited viewers
- ✅ Community support
- ⚠️ Apps sleep after inactivity
- ⚠️ Public repositories only

### Paid Tier (Optional)
- 💰 $20/month per user
- ✅ Private repositories
- ✅ More resources (4 GB RAM)
- ✅ No sleeping
- ✅ Priority support
- ✅ Custom domains

**For MVP/Hackathon: Free tier is perfect!** 🎉

---

## 🔐 Security Notes

### Current Setup (Safe for MVP)
- ✅ No real user data
- ✅ Dummy data only
- ✅ No authentication needed
- ✅ Public access is fine

### For Production (Future)
- [ ] Add user authentication
- [ ] Use Streamlit secrets for API keys
- [ ] Enable HTTPS (automatic on Streamlit Cloud)
- [ ] Add rate limiting
- [ ] Implement data encryption

---

## 📊 Monitoring Your App

### View Analytics

In Streamlit Cloud dashboard:

1. **Viewers**: See real-time viewer count
2. **Logs**: Monitor errors and warnings
3. **Resources**: Check RAM/CPU usage
4. **Uptime**: See availability stats

### Get Notified

1. Go to app settings
2. Enable email notifications
3. Get alerts for:
   - Deployment failures
   - Runtime errors
   - Resource limits

---

## 🚀 Next Steps After Deployment

### Immediate (Day 1)
- [ ] Share URL with hackathon judges
- [ ] Test on mobile devices
- [ ] Gather initial feedback
- [ ] Monitor for errors

### Short-term (Week 1)
- [ ] Add Google Analytics (optional)
- [ ] Create demo video
- [ ] Write blog post
- [ ] Submit to Streamlit gallery

### Long-term (Month 1+)
- [ ] Integrate real Absher API
- [ ] Add user authentication
- [ ] Implement database (PostgreSQL)
- [ ] Add more features from roadmap

---

## 📞 Support Resources

### Streamlit Cloud Help
- **Docs**: https://docs.streamlit.io/deploy
- **Community**: https://discuss.streamlit.io
- **Status**: https://streamlitstatus.com

### GitHub Help
- **Docs**: https://docs.github.com
- **Support**: https://support.github.com

### Salmeen Project
- **README**: See README.md for full documentation
- **Issues**: Create GitHub issues for bugs
- **Discussions**: Use GitHub Discussions for questions

---

## ✅ Deployment Checklist

Before going live, verify:

- [ ] All files pushed to GitHub
- [ ] `requirements.txt` is complete
- [ ] `.streamlit/config.toml` exists
- [ ] `app.py` runs locally without errors
- [ ] Streamlit Cloud deployment successful
- [ ] App loads at public URL
- [ ] Both views (Citizen + Ministry) work
- [ ] Charts and maps render correctly
- [ ] Arabic text displays properly
- [ ] Mobile responsive (test on phone)
- [ ] Shared URL with team/judges

---

## 🎉 Congratulations!

Your Salmeen platform is now **permanently deployed** and accessible worldwide!

**Your app URL**: `https://YOUR_APP_NAME.streamlit.app`

Share it proudly! 🚗💨

---

## 🆘 Need Help?

If you encounter any issues:

1. **Check the logs** in Streamlit Cloud dashboard
2. **Search** Streamlit Community forum
3. **Review** the troubleshooting section above
4. **Contact** Streamlit support (for deployment issues)

---

**قد بسلامة! Drive Safe!** 🇸🇦
