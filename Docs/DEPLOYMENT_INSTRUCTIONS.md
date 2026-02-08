# 🚀 Deployment Instructions - Cookie Management System

## ✅ What's New

Your YouTube MP3 Downloader now includes a **Cookie Management System** that allows you to bypass YouTube's bot detection by using authenticated cookies.

---

## 📋 Quick Start

### 1. Deploy to Leapcell

The code is already pushed to GitHub. Leapcell will automatically redeploy if you have auto-deploy enabled.

**Check deployment status:**
- Go to your Leapcell dashboard
- Look for the latest deployment
- Wait for it to complete (2-3 minutes)

---

### 2. Set Admin Password (IMPORTANT!)

**Generate a password hash:**

```bash
# Run locally
python generate_admin_hash.py
```

This will prompt you for a password and generate a hash like:
```
ADMIN_PASSWORD_HASH=5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
```

**Add to Leapcell:**
1. Go to Leapcell dashboard
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Add new variable:
   - **Key**: `ADMIN_PASSWORD_HASH`
   - **Value**: `<the hash from above>`
5. Click **Save**
6. **Redeploy** the application

> ⚠️ **IMPORTANT**: If you don't set this, the default password will be `admin123` (only for development)

---

### 3. Export YouTube Cookies

Follow the guide in [COOKIE_GUIDE.md](file:///c:/Room/ItsMe/mp3dowloaderProject/COOKIE_GUIDE.md) for detailed instructions.

**Quick steps:**
1. Install browser extension:
   - Chrome: "Get cookies.txt LOCALLY"
   - Firefox: "cookies.txt"
2. Go to youtube.com and log in
3. Click the extension icon
4. Export cookies to a `.txt` file

---

### 4. Upload Cookies to Your App

1. **Access admin panel:**
   ```
   https://your-app.leapcell.app/admin
   ```

2. **Login:**
   - Enter your admin password
   - Click "Iniciar Sesión"

3. **Upload cookies:**
   - Drag and drop your `cookies.txt` file
   - Or click to select it
   - Click "Subir Cookies"

4. **Verify:**
   - You should see "✅ Cookies activas"
   - With the upload date

---

### 5. Test Downloads

1. Go to your main app: `https://your-app.leapcell.app`
2. Try downloading a YouTube video
3. It should work without the "bot detection" error!

---

## 🔄 Maintenance

### When to Update Cookies

Cookies typically last **1-2 weeks**. You'll know they expired when:
- Downloads start failing
- You see the "Sign in to confirm you're not a bot" error

### How to Update

1. Export fresh cookies (2 minutes)
2. Go to `/admin`
3. Upload new cookies
4. Done!

---

## 🔒 Security Notes

### Default Password (Development Only)

If `ADMIN_PASSWORD_HASH` is not set, the default password is `admin123`.

**⚠️ This is ONLY for local development. NEVER use this in production!**

### Setting a Secure Password

1. Choose a strong password (minimum 8 characters)
2. Run `python generate_admin_hash.py`
3. Add the hash to Leapcell environment variables
4. Redeploy

### Cookie Security

- ✅ Cookies are stored only on your server
- ✅ Not committed to Git (in `.gitignore`)
- ✅ Admin panel is password protected
- ✅ Can be deleted anytime via `/admin`

---

## 📁 New Files

### Backend
- `backend/app.py` - Updated with cookie support and admin endpoints
- `backend/templates/admin.html` - Admin interface

### Documentation
- `COOKIE_GUIDE.md` - Complete guide for exporting cookies
- `generate_admin_hash.py` - Utility to generate password hash
- `DEPLOYMENT_INSTRUCTIONS.md` - This file

### Configuration
- `.gitignore` - Updated to exclude cookie files

---

## 🧪 Testing Locally

Before deploying, you can test locally:

```bash
# 1. Run the server
cd backend
python app.py

# 2. Access admin panel
# http://localhost:5000/admin
# Password: admin123 (default)

# 3. Upload cookies

# 4. Test download
# http://localhost:5000
```

---

## 🐛 Troubleshooting

### "Contraseña incorrecta"
- Make sure you set `ADMIN_PASSWORD_HASH` in Leapcell
- Verify the hash was generated correctly
- Check that you redeployed after adding the variable

### "Cookies subidas pero las descargas siguen fallando"
- Verify you logged into YouTube before exporting cookies
- Try exporting cookies again
- Make sure the file is in Netscape format (.txt)

### "No puedo acceder a /admin"
- Check that the deployment completed successfully
- Verify the URL is correct: `https://your-app.leapcell.app/admin`
- Check browser console for errors

---

## 📊 Architecture

```
User Browser
    ↓
Admin Panel (/admin)
    ↓
Upload cookies.txt
    ↓
Server stores in backend/youtube_cookies.txt
    ↓
yt-dlp uses cookies for downloads
    ↓
Downloads work! 🎉
```

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Leapcell redeployed automatically
- [ ] Generated admin password hash
- [ ] Added `ADMIN_PASSWORD_HASH` to Leapcell
- [ ] Redeployed after adding environment variable
- [ ] Exported YouTube cookies
- [ ] Accessed `/admin` panel
- [ ] Logged in successfully
- [ ] Uploaded cookies
- [ ] Verified "Cookies activas" status
- [ ] Tested download - it works!

---

## 🎯 Summary

You now have a fully functional YouTube MP3 downloader that:
- ✅ Works from anywhere (deployed on Leapcell)
- ✅ Bypasses YouTube bot detection (using cookies)
- ✅ Requires minimal maintenance (update cookies every 1-2 weeks)
- ✅ Is secure (password-protected admin panel)

**Time to maintain**: ~2 minutes every 1-2 weeks

**Next steps**: Follow the checklist above to complete the deployment!
