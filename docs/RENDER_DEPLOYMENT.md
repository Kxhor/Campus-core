# Deploying Campus Core to Render

This guide explains how to deploy Campus Core to Render using a free PostgreSQL database and Supabase for permanent file storage.

## 1. Prerequisites
- A GitHub account.
- A free account on [Render](https://render.com).
- A free account on [Supabase](https://supabase.com).

## 2. Set Up Supabase Storage
Render's free tier uses ephemeral storage, which means any files uploaded directly to the server will be deleted when the server sleeps. We use Supabase to permanently store uploaded certificates, QR codes, and signatures.

1. Go to the [Supabase Dashboard](https://app.supabase.com/) and create a new project.
2. In the left menu, go to **Storage**.
3. Click **New Bucket**.
4. Name the bucket exactly: `campuscore-uploads`.
5. Ensure the bucket is set to **Private**. (Our Flask server will securely stream these files to authenticated users).
6. Go to **Project Settings** -> **API**.
7. Copy your `Project URL` (This is your `SUPABASE_URL`).
8. Copy your `anon public` key (This is your `SUPABASE_KEY`).

## 3. Deploy to Render (The Easy Way)
Since this repository includes a `render.yaml` configuration file, deployment is entirely automated.

1. Go to the [Render Dashboard](https://dashboard.render.com).
2. Click **New +** and select **Blueprint**.
3. Connect your GitHub account and select this repository.
4. Render will automatically detect the Web Service and PostgreSQL database defined in `render.yaml`.
5. Render will ask you to provide values for two environment variables:
   - `SUPABASE_URL`: Paste the URL you copied in Step 2.
   - `SUPABASE_KEY`: Paste the anon key you copied in Step 2.
6. Click **Apply**.

Render will now build your application and spin up the database. The `render.yaml` configuration automatically tells Render to:
- Build the app (`pip install -r requirements.txt`)
- Run database migrations (`flask db upgrade`)
- Boot the server (`gunicorn -k eventlet -w 1 app_legacy:app`)

## 4. Final Verification
Once Render marks the service as **Live**, click the URL provided in the dashboard (e.g., `https://campus-core-abc.onrender.com`).
- Log in and create an event.
- Upload a PDF certificate to test the Supabase integration.
- Check the Supabase Storage dashboard to confirm the file appeared in the `campuscore-uploads` bucket.
