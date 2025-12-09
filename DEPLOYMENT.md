# 🚀 Deployment Guide - Salmeen Platform

## Deployment Options

### Option 1: Streamlit Cloud (Recommended for MVP)

#### Prerequisites
- GitHub account
- Streamlit Cloud account (free)

#### Steps
1. **Push to GitHub**
   ```bash
   cd salmeen
   git init
   git add .
   git commit -m "Initial commit - Salmeen MVP"
   git remote add origin https://github.com/yourusername/salmeen.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository: `yourusername/salmeen`
   - Main file path: `app.py`
   - Click "Deploy"

3. **Access Your App**
   - Your app will be live at: `https://yourusername-salmeen.streamlit.app`
   - Share the link with stakeholders

---

### Option 2: Docker Deployment

#### Create Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Build and Run
```bash
# Build image
docker build -t salmeen-app .

# Run container
docker run -p 8501:8501 salmeen-app
```

#### Access
- Local: `http://localhost:8501`
- Network: `http://your-server-ip:8501`

---

### Option 3: AWS EC2 Deployment

#### 1. Launch EC2 Instance
- AMI: Ubuntu 22.04 LTS
- Instance type: t2.medium (recommended)
- Security group: Allow port 8501

#### 2. Connect and Setup
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3.11 python3-pip -y

# Clone or upload project
git clone https://github.com/yourusername/salmeen.git
cd salmeen

# Install dependencies
pip3 install -r requirements.txt
```

#### 3. Run with systemd (Production)
Create service file: `/etc/systemd/system/salmeen.service`
```ini
[Unit]
Description=Salmeen Streamlit App
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/salmeen
ExecStart=/usr/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable salmeen
sudo systemctl start salmeen
sudo systemctl status salmeen
```

#### 4. Setup Nginx Reverse Proxy (Optional)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

---

### Option 4: Azure App Service

#### 1. Create App Service
```bash
az webapp create \
  --resource-group salmeen-rg \
  --plan salmeen-plan \
  --name salmeen-app \
  --runtime "PYTHON:3.11"
```

#### 2. Deploy Code
```bash
az webapp up \
  --name salmeen-app \
  --resource-group salmeen-rg \
  --runtime "PYTHON:3.11"
```

#### 3. Configure Startup Command
In Azure Portal → Configuration → Startup Command:
```bash
streamlit run app.py --server.port=8000 --server.address=0.0.0.0
```

---

### Option 5: Google Cloud Run

#### 1. Create Dockerfile (same as Option 2)

#### 2. Build and Push to GCR
```bash
# Build
gcloud builds submit --tag gcr.io/your-project-id/salmeen

# Deploy
gcloud run deploy salmeen \
  --image gcr.io/your-project-id/salmeen \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Environment Variables

For production deployment, set these environment variables:

```bash
# Optional: Disable Streamlit analytics
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Optional: Set server settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
```

---

## Performance Optimization

### 1. Enable Caching
Already implemented in the code:
- `@st.cache_data` for data loading
- `@st.cache_resource` for ML models

### 2. Optimize Data Loading
For large datasets:
```python
# Use chunking
df = pd.read_csv("driving_data.csv", chunksize=1000)
```

### 3. Use CDN for Static Assets
For production, serve images/CSS from CDN

### 4. Database Integration
For real production:
- Replace CSV with PostgreSQL/MySQL
- Use connection pooling
- Implement data pagination

---

## Security Considerations

### 1. Authentication
Add Streamlit authentication:
```python
import streamlit_authenticator as stauth

# Configure authentication
authenticator = stauth.Authenticate(...)
name, authentication_status, username = authenticator.login('Login', 'main')
```

### 2. HTTPS
Always use HTTPS in production:
- Use Let's Encrypt for free SSL
- Configure reverse proxy (Nginx/Apache)

### 3. API Keys
Store sensitive data in environment variables:
```python
import os
api_key = os.getenv("ABSHER_API_KEY")
```

### 4. Rate Limiting
Implement rate limiting for API endpoints

---

## Monitoring

### 1. Application Monitoring
Use Streamlit built-in metrics:
```python
import streamlit as st
st.write(st.session_state)
```

### 2. Server Monitoring
- Use CloudWatch (AWS)
- Use Azure Monitor (Azure)
- Use Stackdriver (GCP)

### 3. Error Tracking
Integrate Sentry:
```python
import sentry_sdk
sentry_sdk.init(dsn="your-dsn")
```

---

## Scaling

### Horizontal Scaling
- Use load balancer (AWS ELB, Azure Load Balancer)
- Deploy multiple instances
- Use shared database

### Vertical Scaling
- Increase instance size
- Add more RAM/CPU

### Database Scaling
- Use read replicas
- Implement caching (Redis)
- Use connection pooling

---

## Backup Strategy

### 1. Database Backup
```bash
# Daily backup
0 2 * * * pg_dump salmeen_db > /backups/salmeen_$(date +\%Y\%m\%d).sql
```

### 2. Code Backup
- Use Git for version control
- Tag releases
- Keep deployment history

### 3. Data Backup
- S3 for file storage
- Automated daily backups
- Retention policy (30 days)

---

## Cost Estimation

### Streamlit Cloud (Free Tier)
- **Cost**: $0/month
- **Limitations**: Public apps only, limited resources
- **Best for**: MVP, demos, hackathons

### AWS EC2 (t2.medium)
- **Cost**: ~$30-40/month
- **Specs**: 2 vCPU, 4GB RAM
- **Best for**: Small to medium production

### Azure App Service (B2)
- **Cost**: ~$55/month
- **Specs**: 2 cores, 3.5GB RAM
- **Best for**: Enterprise deployment

### Google Cloud Run
- **Cost**: Pay-per-use (~$10-30/month)
- **Best for**: Variable traffic

---

## Maintenance

### Regular Tasks
- [ ] Update dependencies monthly
- [ ] Review and rotate API keys
- [ ] Monitor error logs
- [ ] Check performance metrics
- [ ] Backup database weekly
- [ ] Update SSL certificates

### Quarterly Tasks
- [ ] Security audit
- [ ] Performance optimization
- [ ] User feedback review
- [ ] Feature updates

---

## Rollback Plan

### If Deployment Fails
1. Check logs: `streamlit run app.py --logger.level=debug`
2. Verify dependencies: `pip list`
3. Test locally first
4. Use previous Git tag
5. Restore from backup

### Quick Rollback
```bash
# Revert to previous version
git revert HEAD
git push

# Or use specific commit
git reset --hard <commit-hash>
git push --force
```

---

## Support

For deployment issues:
1. Check Streamlit docs: https://docs.streamlit.io/deploy
2. Community forum: https://discuss.streamlit.io
3. GitHub issues: https://github.com/streamlit/streamlit/issues

---

**Good luck with your deployment! 🚀**
