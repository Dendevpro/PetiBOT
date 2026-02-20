# Quick Start Guide 🚀

Get your Document Automation System running in 5 minutes!

## Step 1: Install Python (if not already installed)

1. Download Python 3.8+ from: https://www.python.org/downloads/
2. During installation, **CHECK** "Add Python to PATH"
3. Verify installation:
   ```bash
   python --version
   ```

## Step 2: Install LibreOffice

1. Download from: https://www.libreoffice.org/download/
2. Install the full version
3. Verify installation:
   ```bash
   soffice --version
   ```

## Step 3: Get Gemini API Key (FREE)

1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. **Copy** the key (you'll need it in Step 5)

## Step 4: Install Project Dependencies

Open terminal/command prompt in the project folder:

```bash
pip install -r requirements.txt
```

**If you get errors on Windows:**
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Step 5: Launch the Dashboard

```bash
streamlit run streamlit_app.py
```

Your browser will open automatically at: http://localhost:8501

## Step 6: Configure

In the dashboard sidebar:

1. **Expand "🔑 API Keys"**
   - Paste your Gemini API Key
   - Click "💾 Save Configuration"

2. **Email is OPTIONAL** - skip if you don't need automatic sending

## Step 7: Process Your First Document

1. Click **"📤 Process Document"** tab
2. **Upload** a .docx file (drag & drop or click)
3. Click **"🚀 Process Document"**
4. Watch the progress bar!
5. **Download** your PDF with QR code

## 🎉 Done!

You're now ready to automate document processing!

---

## Common Issues & Quick Fixes

### "LibreOffice not found"
- Make sure LibreOffice is installed
- **Windows:** Add to PATH: `C:\Program Files\LibreOffice\program`
- Restart terminal/command prompt

### "Module not found"
```bash
pip install -r requirements.txt --force-reinstall
```

### "Gemini API error"
- Check if API key is correct
- Try creating a new API key
- Check quota at: https://makersuite.google.com/

### "Streamlit won't start"
```bash
pip install streamlit --upgrade
streamlit run streamlit_app.py
```

---

## Need Help with Email Setup?

### Gmail Users:
1. Enable 2-Step Verification: https://myaccount.google.com/security
2. Get App Password: https://myaccount.google.com/apppasswords
3. Use the 16-character App Password (not your regular password!)

### Outlook Users:
1. Go to Account Settings > Security
2. Generate App Password
3. Use `smtp.office365.com` as SMTP server

---

## Tips for Best Results

✅ **Use templates** - Keep Word docs with headers/footers pre-formatted
✅ **Short summaries** - QR codes work best with <500 characters
✅ **Test first** - Try with a simple document first
✅ **Check history** - View all past processes in the History tab
✅ **Save config** - Always save after changing settings

---

## What Gets Created?

After processing, you'll have:

- ✅ **Original Word document** (unchanged)
- ✅ **QR Code image** (.png) with summary
- ✅ **Final PDF** with QR code in header
- ✅ **Email sent** (if configured)
- ✅ **History entry** in dashboard

All files saved to: `output/` folder

---

**Ready to go? Run:** `streamlit run streamlit_app.py`

For detailed documentation, see: README.md
