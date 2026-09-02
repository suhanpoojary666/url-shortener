# URL Shortener — Backend

A backend URL shortener built with Django REST Framework. Users can shorten a long URL and get redirected to the original when the short code is visited.

```
Original: https://example.com/a-very-long-url
Short:    https://domain.com/F/
```
## Live

- API (backend): https://url-shortener-wj7g.onrender.com
- Client (frontend<->backend): https://url-shortener-client-hg11.onrender.com

## Features

- Create, update, delete short URLs
- URL expiration
- Per-URL click statistics
- JWT authentication (register / login / refresh)
- Redis caching for fast redirects
- Celery for async analytics processing
- PostgreSQL for persistent storage
- Dockerized setup

## Tech Stack

- Django + Django REST Framework
- PostgreSQL
- Redis
- Celery
- JWT
- Docker

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register/` | Register a new user |
| POST | `/api/token/` | Obtain JWT access/refresh tokens (login) |
| POST | `/api/token/refresh/` | Refresh an access token |
| POST | `/shorten/` | Create a short URL |
| GET | `/myurls/` | List the authenticated user's URLs |
| GET | `/<short_code>/` | Redirect to the original URL |
| GET | `/<short_code>/stats/` | Get click stats for a short URL |
| PUT/PATCH | `/<short_code>/update/` | Update a short URL |
| PATCH | `/<short_code>/modify_expiration/` | Change a URL's expiration |
| DELETE | `/<short_code>/delete/` | Delete a short URL |

## Basic Workflow

-User creates a short URL by providing the original URL.

-Store the mapping between the short code and the original URL

-When the short code is requested, look up the corresponding URL

-Redirect the user to the original URL.

## Caching, Rate Limiting & Celery

- **Redis caching:** redirect lookups, per-URL stats, and a user's `myurls` list are all cached in Redis, so repeat requests are served straight from cache instead of hitting PostgreSQL every time.
- **Rate limiting:** Redis also tracks per-user (and per-IP for registration) request counts, capping how often endpoints like create, update, delete, and register can be called.
- **Celery:** Each redirect queues a background analytics task instead of updating data inline, allowing the user to be redirected immediately while Celery handles the analytics separately.

## Performance

With Redis + Celery enabled, the production median redirect response time dropped from **912 ms to 285 ms** — roughly a **68.8%** reduction.

## Getting Started

### Requirements

- Docker and Docker Compose

### Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/suhanpoojary666/url-shortener
   cd url-shortener
   ```
2. Create a `.env` file in the project root with:
   ```env
   SECRET_KEY=your-own-secret-key
   DEBUG=False
   DATABASE_URL=postgresql://postgres:postgres@db:5432/urlshortener
   REDIS_URL=redis://redis:6379
   ```
3. Start the stack:
   ```bash
   docker compose up
   ```
   This starts three containers: `web` (Django app), `db` (PostgreSQL), and `redis` (Redis). The `web` container's entrypoint runs `python manage.py migrate` automatically before starting Django, so migrations are applied on every startup — no manual step needed.

The API will be available at `http://127.0.0.1:8000`.

## Project Structure

```
server/
├── urlshortener/
├── shortener/
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── requirements.txt
└── manage.py
```

- `urlshortener/` — Django project folder
- `shortener/` — Main app folder