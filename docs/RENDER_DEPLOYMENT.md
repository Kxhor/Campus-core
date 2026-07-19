# Deploying Campus Core (Free Tier)

This guide explains how to deploy Campus Core entirely for free using Render for hosting the web server, and Supabase for the PostgreSQL database and permanent file storage.

## 1. Prerequisites
- A GitHub account.
- A free account on [Render](https://render.com) (for the Python web server).
- A free account on [Supabase](https://supabase.com) (for the Database and File Storage).

## 2. Set Up Supabase (Database & Storage)
We will use Supabase for everything data-related since Render's free PostgreSQL databases expire after 30 days. Supabase is permanently free.

1. Go to the [Supabase Dashboard](https://app.supabase.com/) and create a new project.
2. **Get your Database URL**: 
   - Go to **Project Settings** -> **Database**.
   - Under "Connection string" -> "URI", copy the URL. (It looks like `postgresql://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres`). Remember to replace `[password]` with your actual database password.
3. **Get your API Keys**:
   - Go to **Project Settings** -> **API**.
   - Copy your `Project URL` (This is your `SUPABASE_URL`).
   - Copy your `anon public` key (This is your `SUPABASE_KEY`).
4. **Create the Storage Bucket**:
   - In the left menu, go to **Storage** and click **New Bucket**.
   - Name the bucket exactly: `campuscore-uploads`.
   - Set the bucket to **Private**.

## 3. Deploy to Render
Since this repository includes a `render.yaml` configuration file, deployment is entirely automated.

1. Go to the [Render Dashboard](https://dashboard.render.com).
2. Click **New +** and select **Blueprint**.
3. Connect your GitHub account and select this repository.
4. Render will ask you to provide values for three environment variables:
   - `DATABASE_URL`: Paste the PostgreSQL connection string you copied in Step 2.
   - `SUPABASE_URL`: Paste the project URL you copied in Step 2.
   - `SUPABASE_KEY`: Paste the anon key you copied in Step 2.
5. Click **Apply**.

Render will now build your application. The `render.yaml` configuration automatically tells Render to:
- Use the **Free** instance type.
- Build the app (`pip install -r requirements.txt`)
- Run database migrations against your Supabase database (`flask db upgrade`)
- Boot the server (`gunicorn -k eventlet -w 1 app_legacy:app`)

## 4. Final Verification
Once Render marks the service as **Live**, click the URL provided in the dashboard (e.g., `https://campus-core-abc.onrender.com`).
- Log in and create an event.
- Upload a PDF certificate to test the Supabase storage integration.
- Check the Supabase Storage dashboard to confirm the file appeared in the `campuscore-uploads` bucket.
