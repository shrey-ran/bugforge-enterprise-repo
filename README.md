# Enterprise E-Commerce Platform

A production-grade Python backend for an e-commerce platform featuring authentication, order processing, payment handling, search, and analytics.

## Project Structure

```
src/
  auth/         - Authentication, sessions, permissions
  api/          - REST API endpoints (users, orders)
  services/     - Business logic (payments, search, notifications)
  models/       - Data models (products, carts, users)
  utils/        - Helpers (math, dates, caching, validation)
config/         - Application configuration
tests/          - Test suite
```

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```
