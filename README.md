# All-in-One AI Blog Platform: Generate, Build, Serve & Manage with Admin Panel

> *OpenAI-powered content, static site generation, admin management, and zero-touch CI/CD deployment.*

## Overview

**openai-blog-ssg** is a comprehensive platform for building, managing, and serving AI-powered blogs. It integrates a Django admin panel for backend management, an OpenAI-powered AI module to generate blog posts, a static site generator to build and optimize HTML pages, and an automated CI/CD workflow for continuous deployment. Blogs are served lightning-fast via Nginx, with all components fully Dockerized for portability.

* **AI-Powered Content**: Auto-generate blog posts with OpenAI GPT.
* **Admin Management**: Easily manage blog content and tags through a powerful Django admin panel.
* **Frontend Blog Site**: Clean, SEO-optimized static pages for fast public viewing.
* **Automated Static Site Generation**: The backend transforms all content into optimized static HTML files for maximum performance and security.
* **Automated CI/CD**: Pushes to `main` branch deploy instantly to your server via GitHub Actions, Docker Compose, and Nginx.
* **Secure Environment Management**: Handles secrets and config safely with .env and GitHub Secrets.

---

## Features

* **Blog & Project Pages**: Create and display blogs and project portfolios.
* **OpenAI GPT Integration**: Use AI to draft blog posts from titles or prompts.
* **Image Processing**: Automated resizing and WebP conversion.
* **SEO & RSS**: Generates meta tags, RSS feeds, and search indices for discoverability.
* **Admin Backend**: Django-based panel for content, tags, and categories.
* **PostgreSQL Database**: Robust and reliable backend for admin data.
* **Static Asset Serving**: Nginx serves the generated HTML, CSS, and images.
* **Complete Dockerization**: All services (admin, AI, SSG, frontend, static) run in containers.
* **Modular Architecture**: Easily extend or swap any part of the stack.

---

## Architecture

* **Backend / Admin Panel:** Django app for creating, editing, and managing blog content, tags, and categories. Data is stored in PostgreSQL.
* **AI Agent:** Python-based service using OpenAI's API to generate blog content automatically based on given titles or prompts.
* **Static Site Generator (SSG):** Converts all stored blog posts and projects into static HTML files, optimizing for SEO and fast load times.
* **Frontend:** Clean, responsive static pages for visitors to read blogs and browse projects.
* **CI/CD Pipeline:** On each push to `main`, GitHub Actions triggers automated deployment: code is copied to the server, Docker Compose builds all services, and Nginx serves the new site.

---

## How it Works

1. **Admin creates blog titles or content** via the Django panel.
2. **AI Agent generates articles** automatically with OpenAI GPT, based on those titles or prompts.
3. **SSG backend transforms content** into SEO-optimized static HTML, ready for blazing-fast serving.
4. **Static frontend** displays all blog content to visitors, with search, feed, and project support.
5. **CI/CD pipeline** auto-deploys any code/content change to production using GitHub Actions and Docker Compose.

---

## Quick Start

### 1. **Clone and Configure**

```bash
git clone https://github.com/emirbaycan/openai-blog-ssg.git
cd openai-blog-ssg
cp .env.example .env
# Fill in your OpenAI key and other required settings
```

### 2. **Build & Run with Docker**

```bash
docker compose up -d --build
```

* Access the admin panel: [http://localhost:8000/admin](http://localhost:8000/admin)
* View the blog: [http://localhost:8080](http://localhost:8080)

### 3. **OpenAI Content Generation**

* Add new blog titles in the Django admin or via CLI
* The AI container will generate blog content and save it to the content directory

### 4. **Deploy to Production**

1. SSH key-based access to your production server is required
2. Add your server and SSH key to GitHub Secrets (`SERVER_HOST`, `SERVER_USER`, `SERVER_SSH_KEY`)
3. Edit `.github/workflows/deploy.yml` as needed
4. Push to `main` branch — GitHub Actions will handle deploy, Docker build, and Nginx serving

---

## Directory Structure

```
/
├── admin/          # Django admin backend
├── ai/             # OpenAI-powered content generator
├── ursus/          # Static site generator core
├── frontend/       # Blog/project content, templates, images
├── output/         # Generated static files for Nginx
├── .github/workflows/deploy.yml  # CI/CD workflow
├── docker-compose.yml
├── Dockerfile.*
└── .env
```

---

## Environment Variables

* `OPENAI_API_KEY` – Required for AI content
* `SITE_URL`, `HTML_URL_EXTENSION`, ... – Site build/config options
* Database connection variables for PostgreSQL
* **Never commit secrets or production .env files to your repo!**

---

## Tech Stack

* **Python** (Django, custom SSG)
* **OpenAI GPT** (content generation)
* **PostgreSQL** (database)
* **Docker Compose** (container orchestration)
* **Nginx** (static file serving)
* **GitHub Actions** (CI/CD)

---

## Customization

* Extend AI agents for custom prompts/workflows
* Add new templates or content types
* Integrate with additional deployment or notification services

---

## Security Best Practices

* Keep your `.env` file and API keys out of source control
* Use branch protection and CI/CD secrets for automated deploys
* Rotate your SSH and API keys regularly

---

## License

MIT.
See [LICENSE](LICENSE) for details.

---

## Author

[Emir Baycan](https://github.com/emirbaycan)

---

**Ready to automate your blog creation, management, and deployment? Fork, clone, and get started!**
