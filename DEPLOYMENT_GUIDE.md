# Smart Pharmacy System - Public Access & 24/7 Cloud Deployment Guide

This guide explains why temporary tunnels stop working when Antigravity closes, and provides two solutions:
1. **Option A (Recommended for 24/7 "Anytime, Anywhere" Access)**: Host on a permanent free cloud server (Render.com or PythonAnywhere) so the site stays online even when your laptop is turned off!
2. **Option B (Instant Local Launcher)**: Run the public link in an independent Windows window so you can close Antigravity completely without the link dying.

---

## 1. Why Did "Error 1033" Happen?

When you saw:
```
Error 1033 - Cloudflare Tunnel error
laboratories-formula-sets-pages.trycloudflare.com
```
* **The Cause:** That Cloudflare Quick Tunnel was running directly on your laptop inside the Antigravity task runner. When Antigravity was closed, the local processes (`python app.py` and `cloudflared.exe`) were terminated. Because the website was running on your local machine, closing Antigravity cut off the connection, leading Cloudflare to display Error 1033.
* **The Nature of Quick Tunnels:** Quick tunnels (`trycloudflare.com`) are temporary test tunnels. They randomly generate a new address each time they start, and they only remain active while the host computer is awake and running the process.

---

## 2. Option A: Permanent 24/7 Cloud Hosting (Opens Anytime & Anywhere)

If you want a link that **never changes** and **works from any phone, college lab PC, or evaluator's browser 24/7 (even when your laptop is completely powered off and Antigravity is closed)**, host it on a free cloud platform.

We have already configured your project with:
- [`wsgi.py`](file:///c:/Users/Deekshita/Downloads/smart-pharmacy-system/smart-pharmacy-system/wsgi.py) (Production WSGI entrypoint)
- [`requirements.txt`](file:///c:/Users/Deekshita/Downloads/smart-pharmacy-system/smart-pharmacy-system/requirements.txt) (Includes `gunicorn` production server)
- [`render.yaml`](file:///c:/Users/Deekshita/Downloads/smart-pharmacy-system/smart-pharmacy-system/render.yaml) & [`Procfile`](file:///c:/Users/Deekshita/Downloads/smart-pharmacy-system/smart-pharmacy-system/Procfile) (Cloud deployment configuration)
- [`init_deploy.py`](file:///c:/Users/Deekshita/Downloads/smart-pharmacy-system/smart-pharmacy-system/init_deploy.py) (Automatic database creation, demo users, and medicines)

---

### Method 1: Deploy on Render.com (100% Free Forever)

Render is one of the easiest, most reliable free cloud platforms for Python Flask applications.

1. **Upload your project to GitHub**:
   - Go to [github.com](https://github.com) and create a new repository (e.g., `smart-pharmacy-system`).
   - Upload the files from your folder (`c:\Users\Deekshita\Downloads\smart-pharmacy-system\smart-pharmacy-system`) to the GitHub repository.

2. **Deploy on Render**:
   - Go to [render.com](https://render.com) and Sign In (choose **Continue with GitHub**).
   - In the Render Dashboard, click **New +** and select **Web Service**.
   - Connect your `smart-pharmacy-system` repository.
   - Render will display the settings:
     * **Name:** `smart-pharmacy-system` (or any custom name)
     * **Language:** `Python 3`
     * **Region:** Any (e.g., Singapore or Oregon)
     * **Branch:** `main`
     * **Build Command:** `pip install -r requirements.txt && python init_deploy.py`
     * **Start Command:** `gunicorn wsgi:app`
     * **Instance Type:** `Free`
   - Click **Deploy Web Service**.

3. **Your Permanent Link**:
   - Within 2 minutes, Render assigns you a permanent, custom HTTPS domain:
     `https://smart-pharmacy-system.onrender.com`
   - This link stays online 24/7/365, never changes, and works from any device anywhere in the world!

---

### Method 2: Deploy on PythonAnywhere.com (No Git Needed!)

If you do not want to use GitHub, PythonAnywhere allows uploading directly via your browser:

1. Create a free account at [pythonanywhere.com](https://www.pythonanywhere.com).
2. Go to the **Files** tab and upload a `.zip` of this project folder, then open a **Bash Console** and unzip it:
   ```bash
   unzip smart-pharmacy-system.zip
   ```
3. Go to the **Web** tab, click **Add a new web app**, choose **Manual configuration**, and select **Python 3.10** (or 3.11).
4. Under the **Code** section on the Web tab:
   - **Source code:** `/home/<your-username>/smart-pharmacy-system`
   - **Working directory:** `/home/<your-username>/smart-pharmacy-system`
   - Click on the **WSGI configuration file** link to edit it, clear the default text, and paste:
     ```python
     import sys
     path = '/home/<your-username>/smart-pharmacy-system'
     if path not in sys.path:
         sys.path.append(path)

     from wsgi import app as application
     ```
   - Save the file.
5. In the Bash Console, run:
   ```bash
   python init_deploy.py
   ```
6. Click the green **Reload <your-username>.pythonanywhere.com** button.
7. Your permanent live link is:
   `https://<your-username>.pythonanywhere.com`

---

## 3. Option B: Instant Local Launch (Run Independent of Antigravity)

If you need a working public link immediately on your laptop without keeping Antigravity open:

1. Open File Explorer and navigate to:
   `c:\Users\Deekshita\Downloads\smart-pharmacy-system\smart-pharmacy-system`
2. **Double-click `run_public.bat`**.
3. A Windows Command Prompt window will appear. It will:
   - Start the Flask backend.
   - Securely connect the Cloudflare tunnel.
   - Automatically display your live public link (e.g. `https://xxxx.trycloudflare.com`).
   - Automatically open the link in your web browser.
   - Write the link to `PUBLIC_LINK.txt` and create a desktop shortcut `OPEN_PUBLIC_LINK.url`.
4. **Crucial Difference:** Because you launched this directly in Windows (and NOT inside Antigravity), **you can safely close Antigravity IDE!**
5. **Keep the Command Prompt window open** on your laptop for as long as you want people to visit the site.

---

## 4. Default Demo Accounts

Both local and cloud deployments come pre-configured with the following credentials:

| Role | Email | Password |
|---|---|---|
| **Admin** | `admin@pharmacy.com` | `Admin1234!` |
| **Pharmacist** | `pharmacist@pharmacy.com` | `Pharmacist1234!` |

*(The login page also has 1-click **Auto-fill Demo Credentials** buttons for quick access.)*
