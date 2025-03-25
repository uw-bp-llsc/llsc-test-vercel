# Deployment Guide: Vercel (Frontend) + Railway (Backend/Database)

This guide provides instructions for deploying this application using Vercel for the frontend and Railway for the backend and database.

## Prerequisites

- GitHub repository with your code
- [Vercel account](https://vercel.com/)
- [Railway account](https://railway.app/)

## Deployment Overview

1. Deploy the PostgreSQL database on Railway
2. Deploy the backend on Railway
3. Deploy the frontend on Vercel
4. Connect the services

## 1. Database Deployment on Railway

Railway provides PostgreSQL as a service with automatic backups, monitoring, and scaling.

1. **Create a new Railway project**:
   - Log in to your Railway account
   - Click **New Project**
   - Select **PostgreSQL**

2. **Note your database credentials**:
   - Railway automatically provides environment variables to your connected services
   - The key variables are:
     - `DATABASE_URL`: Complete PostgreSQL connection string
     - `PGHOST`: Database hostname
     - `PGDATABASE`: Database name
     - `PGUSER`: Database username
     - `PGPASSWORD`: Database password
     - `PGPORT`: Database port (usually 5432)

## 2. Backend Deployment on Railway

1. **Connect your GitHub repository**:
   - In your Railway project, click **New Service**
   - Select **GitHub Repo**
   - Choose your repository
   - Specify the root directory as `/backend`

2. **Configure environment variables**:
   - In your service's **Variables** tab, add:
     - `FASTAPI_CONFIG=production`
     - `PORT=8080` (Railway sets this automatically)
     - Any other required variables from your `.env.sample` file such as AWS/Firebase credentials

3. **Configure deployment**:
   - Railway will use your `railway.json` configuration for deployment
   - The migrations will run as part of the build process

### Database Migrations on Railway

Migrations will run automatically during the build process because:

1. We've updated `railway.json` to include `alembic upgrade head` in the build command
2. We've modified `migrations/env.py` to handle Railway's database URL format
3. We've created a dedicated `run_migrations.py` script for manual migration execution

#### Manual Migration Execution

If you need to run migrations manually, you can use Railway's CLI:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Run migrations script
railway run python backend/run_migrations.py
```

## 3. Frontend Deployment on Vercel

1. **Connect your GitHub repository**:
   - Go to [Vercel](https://vercel.com/) and log in
   - Click **Add New...** > **Project**
   - Import your GitHub repository
   - Configure the project:
     - Framework Preset: Next.js
     - Root Directory: `/frontend`

2. **Configure environment variables**:
   - In the project settings, add:
     - `NEXT_PUBLIC_API_URL`: Your Railway backend URL (e.g., `https://your-backend-service.railway.app`)

3. **Deploy**:
   - Click **Deploy**

## 4. Connecting Services

1. **Update CORS settings**:
   - Your backend already has CORS configured for Vercel domains in `backend/app/__init__.py`
   - Update `https://your-project-name.vercel.app` to your actual Vercel domain

2. **Update API URL**:
   - In Vercel environment variables, set `NEXT_PUBLIC_API_URL` to your actual Railway backend URL

## Troubleshooting

### Database Connection Issues

If you encounter database connection problems:

1. **Check environment variables**:
   - Verify `DATABASE_URL` is correctly set in Railway
   - Ensure your backend is using this variable in production mode

2. **Migration failures**:
   - Check Railway logs for specific errors
   - Run migrations manually using the Railway CLI and the `run_migrations.py` script
   - If needed, connect to your database directly using Railway's connect feature to debug:
     ```bash
     railway connect
     ```

### CORS Issues

If the frontend can't communicate with the backend:

1. **Check CORS configuration**:
   - Update the allowed origins in `backend/app/__init__.py` to include your exact Vercel domain
   - Temporarily, you can add `"*"` to the allowed origins list for testing

2. **Verify API URL**:
   - Ensure `NEXT_PUBLIC_API_URL` in Vercel points to the correct Railway backend URL

## CI/CD and Automatic Deployments

Both Railway and Vercel support automatic deployments:

- Commits to your main branch will trigger deployments on both platforms
- For preview deployments, both platforms support branch and PR-based previews

## Database Backups

Railway automatically handles daily backups for your PostgreSQL database. You can:

1. **Create manual backups**:
   - In Railway, go to your database service
   - Click on the **Backups** tab
   - Click **Create Backup**

2. **Restore from backups**:
   - In the **Backups** tab, find the backup you want to restore
   - Click the menu and select **Restore** 