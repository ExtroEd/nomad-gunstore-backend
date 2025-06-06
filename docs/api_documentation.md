# API Documentation

## Overview
This project is a backend for an online store inspired by Palmetto State Armory. It is built using Django and Django REST Framework, following RESTful principles. The API is containerized with Docker, uses Redis and Celery for asynchronous tasks, and includes features such as registration, authentication, product listing, cart management, and order processing.

---

## Endpoints

### Authentication (users)
- `POST /api/users/register/` – Register new user
- `POST /api/users/login/` – Log in
- `GET /api/users/profile/` – Retrieve user profile (requires auth)

### Products
- `GET /api/products/` – List all products
- `GET /api/products/{id}/` – Retrieve product details
- `GET /api/products/?category={slug}` – Filter products by category

### Categories
- `GET /api/categories/` – Retrieve all categories
- `GET /api/menu-categories/` – Structured hierarchical menu for navigation

### Brands
- `GET /api/brands/` – List all brands with logos
- `GET /api/brands/{slug}/` – Retrieve products by brand

### Cart
- `GET /api/cart/` – Get cart items for logged in user
- `POST /api/cart/add/` – Add product to cart
- `DELETE /api/cart/remove/{product_id}/` – Remove product from cart

### Orders
- `POST /api/orders/` – Create new order
- `GET /api/orders/` – List user's orders
- `GET /api/orders/{id}/` – Get details of a specific order

---

## Technologies
- **Django + DRF**
- **Celery + Redis** (for async tasks)
- **Cloudinary** (media)
- **Docker, Nginx, CI/CD**