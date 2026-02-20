# Streamlit Cloud Deployment Guide 🚀

Complete guide to deploy your Document Automation System so your brother can use it from any browser without installation!

---

## 📋 What You'll Need

1. ✅ **GitHub account** (you have this!)
2. ⏱️ **10-15 minutes** of your time
3. 🔑 **Two free API keys:**
   - Gemini API (for AI summaries)
   - CloudConvert API (for PDF conversion in the cloud)

---

## Part 1: Get Your API Keys (5 minutes)

### A) Gemini API Key (FREE - 60 requests/minute)

1. Go to: **https://makersuite.google.com/app/apikey**
2. Sign in with your Google account
3. Click **"Create API Key"**
4. **Copy and save** the key somewhere safe

### B) CloudConvert API Key (FREE - 25 conversions/day)

CloudConvert is needed because Streamlit Cloud doesn't have LibreOffice installed.

1. Go to: **https://cloudconvert.com/register**
2. Sign up (free account)
3. Verify your email
4. Go to: **https://cloudconvert.com/dashboard/api/v2/keys**
5. Click **"Create New API Key"**
6. Give it a name like "Document Automation"
7. **Copy and save** the key

**Note:** 25 free conversions/day should be plenty for normal use!

---

## Part 2: Upload Files to GitHub (3 minutes)

### Method 1: Drag & Drop (Easiest)

1. Go to **https://github.com** and sign in
2. Click **"New repository"** (green button)
3. Repository settings:
   - **Name:** `document-automation` (or any name you like)
   - **Visibility:** ✅ **Public** (required for free Streamlit hosting)
   - ❌ DON'T check "Add a README file"
4. Click **"Create repository"**

5. Download all the project files I created (from the previous chat)

6. On your new GitHub repository page:
   - Click **"uploading an existing file"** link
   - **Drag and drop** all these files:
     - `streamlit_app.py`
     - `document_automation.py`
     - `requirements.txt`
     - `README.md`
     - `QUICKSTART.md`
     - `config.json.template`
   - Click **"Commit changes"**

### Method 2: Git Command Line (If You Prefer)

```bash
# Clone your empty repository
git clone https://github.com/YOUR-USERNAME/document-automation.git
cd document-automation

# Copy all project files into this folder

# Add and commit
git add .
git commit -m "Initial commit - Document Automation System"
git push origin main
```

---

## Part 3: Deploy to Streamlit Cloud (5 minutes)

### Step 1: Sign Up for Streamlit Cloud

1. Go to: **https://share.streamlit.io**
2. Click **"Sign up"** or **"Get started"**
3. Choose **"Continue with GitHub"**
4. Click **"Authorize streamlit"** when prompted

### Step 2: Create New App

1. Click **"New app"** button (or "Create app")
2. Fill in the form:

   **Repository settings:**
   - **Repository:** Select `YOUR-USERNAME/document-automation`
   - **Branch:** `main` (or `master` - check your GitHub)
   - **Main file path:** `streamlit_app.py`

   **App settings:**
   - **App URL:** Choose a custom name (e.g., `legal-doc-automation`)
     - This will be: `https://legal-doc-automation.streamlit.app`
     - ⚠️ Must be unique - try variations if taken

3. Click **"Deploy!"**

### Step 3: Wait for Deployment

- ⏱️ First deployment takes **2-5 minutes**
- You'll see logs showing:
  - Installing dependencies
  - Setting up environment
  - Starting app
- When done, you'll see: **"Your app is live!"** ✅

### Step 4: Configure API Keys

1. Once your app loads, you'll see the dashboard
2. **In the sidebar**, expand **"🔑 API Keys"**
3. Enter both API keys:
   - **Gemini API Key:** Paste your Gemini key
   - **CloudConvert API Key:** Paste your CloudConvert key
4. Click **"💾 Save Configuration"**

5. **IMPORTANT:** Click the **☰ menu** (top right) → **"Reboot app"**
   - This ensures the config is properly saved

---

## Part 4: Share with Your Brother (1 minute)

### Your App URL

Your app is now live at:
```
https://YOUR-APP-NAME.streamlit.app
```

**Send this URL to your brother!** He can:
- ✅ Open it on any device (phone, tablet, computer)
- ✅ Bookmark it for easy access
- ✅ Use it without installing anything
- ✅ Upload documents and get PDFs with QR codes

### Security Note

⚠️ **The API keys are stored in Streamlit's secure cloud storage** (not visible in the URL or code). However:
- Anyone with the URL can use the app
- They'll use YOUR API quotas (Gemini: 60/min, CloudConvert: 25/day)

**If you want to restrict access:**
- Keep the URL private (don't post publicly)
- Monitor your API usage dashboards
- OR upgrade Streamlit to Teams plan for password protection

---

## 🎉 You're Done!

Your brother can now:
1. Visit the URL you shared
2. Upload a Word document
3. Get a PDF with QR code summary
4. Download or receive by email (if configured)

---

## 📊 Managing Your Deployment

### Check API Usage

**Gemini:**
- Dashboard: https://makersuite.google.com/app/apikey
- Limit: 60 requests/minute (plenty for normal use)

**CloudConvert:**
- Dashboard: https://cloudconvert.com/dashboard
- Limit: 25 conversions/day (resets daily)
- If you need more: $9/month for 1000 conversions

### Update Your App

To make changes:
1. Edit files on GitHub (or push updates via Git)
2. Streamlit Cloud automatically redeploys within 1-2 minutes
3. Changes go live automatically!

### Monitor App Health

- View logs: Click "Manage app" → "Logs"
- Check status: See if app is running or has errors
- Reboot if needed: "Manage app" → "Reboot"

### Delete/Pause App

Don't want it running anymore?
- Go to https://share.streamlit.io/
- Find your app
- Click "⋮" → "Delete"

---

## 🆘 Troubleshooting

### "App is not loading"
- Wait 2-3 minutes for first deployment
- Check logs for errors
- Ensure all files uploaded correctly

### "Module not found" error
- Check that `requirements.txt` was uploaded
- Verify file names are exactly correct (case-sensitive)

### "CloudConvert API error"
- Verify API key is correct (no extra spaces)
- Check you haven't exceeded 25 conversions/day
- Ensure CloudConvert account is verified

### "Gemini API error"
- Verify API key is correct
- Check API is enabled at: https://makersuite.google.com
- Ensure you haven't hit rate limits

### Brother can't access the app
- Check if URL is correct (no typos)
- Ensure app status shows "Running"
- Try opening in incognito/private browser window
- Check if Streamlit services are operational: https://status.streamlit.io

---

## 💡 Tips for Your Brother

Create a simple guide for him:

```
Como usar o Sistema de Automação de Documentos

1. Abra o link: [SEU-LINK-AQUI]

2. Na aba "Processar Documento":
   - Clique ou arraste seu documento Word (.docx)
   - Aguarde o processamento (1-2 minutos)
   - Baixe o PDF final com QR code

3. O QR code contém um resumo do documento
   - Escaneie com seu celular para ler
   - Útil para referência rápida

4. Se precisar de ajuda:
   - Veja a aba "Histórico" para documentos anteriores
   - Veja a aba "Sobre" para mais informações
```

---

## 🔄 Alternative: Share Config via Streamlit Secrets

If you don't want your brother to see/configure API keys:

1. In GitHub repository, create `.streamlit/secrets.toml`:
```toml
gemini_api_key = "YOUR_KEY_HERE"
cloudconvert_api_key = "YOUR_KEY_HERE"
```

2. Modify `streamlit_app.py` to read from secrets:
```python
if 'gemini_api_key' in st.secrets:
    st.session_state.config['gemini_api_key'] = st.secrets['gemini_api_key']
```

3. Your brother won't need to configure anything!

---

**Questions? Issues? Check the README.md for detailed documentation!**

**🎉 Congratulations! Your brother can now automate documents from anywhere!**
