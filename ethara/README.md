# Ethara — Inventory & Order Management System

A full-stack inventory and order management system built with **React + Vite** (frontend) and **FastAPI + PostgreSQL** (backend).

---

## Project Structure

```
ethara/
├── backend/                  # FastAPI application
│   ├── app/
│   │   ├── api/routes/       # Route handlers (products, customers, orders, dashboard)
│   │   ├── core/config.py    # Settings (reads from .env)
│   │   ├── db/               # SQLAlchemy engine & session
│   │   ├── models/           # ORM models (Product, Customer, Order, OrderItem)
│   │   ├── schemas/          # Pydantic schemas (request / response)
│   │   ├── services/         # Business logic layer
│   │   └── main.py           # App entry point + CORS
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env                  # Backend env vars
│
├── frontend/                 # React + Vite application
│   ├── src/
│   │   ├── api/              # ← Axios client + per-resource API modules
│   │   │   ├── client.js     #   Base Axios instance (reads VITE_API_URL)
│   │   │   ├── products.js
│   │   │   ├── customers.js
│   │   │   ├── orders.js
│   │   │   ├── dashboard.js
│   │   │   └── index.js      #   Barrel export
│   │   ├── hooks/
│   │   │   └── useApi.js     #   useApi + useMutation hooks
│   │   └── ...               #   Your existing pages/components
│   ├── vite.config.js        # Dev proxy: /api → localhost:8000
│   ├── .env                  # VITE_API_URL=http://localhost:8000
│   └── Dockerfile
│
└── docker-compose.yml        # Orchestrates db + backend + frontend
```

---

## Quick Start

### Option A — Docker (recommended)

```bash
# From the project root
docker compose up --build
```

| Service  | URL                       |
|----------|---------------------------|
| Frontend | http://localhost          |
| Backend  | http://localhost:8000     |
| API Docs | http://localhost:8000/docs|
| DB       | localhost:5432            |

### Option B — Local Development (no Docker)

**1. PostgreSQL**
```bash
# Make sure PostgreSQL is running locally, then:
createuser -P ethara          # password: ethara
createdb -O ethara ethara
```

**2. Backend**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Edit .env if needed (DATABASE_URL defaults to localhost)
uvicorn app.main:app --reload --port 8000
```

**3. Frontend**
```bash
cd frontend
npm install
npm run dev                    # Vite proxy forwards /api → http://localhost:8000
```

---

## API Endpoints

### Dashboard
| Method | Path                   | Description         |
|--------|------------------------|---------------------|
| GET    | /api/dashboard/stats   | Aggregated KPIs     |

### Products
| Method | Path                         | Description              |
|--------|------------------------------|--------------------------|
| GET    | /api/products                | List (search, category, low_stock_only) |
| GET    | /api/products/categories     | Distinct categories      |
| GET    | /api/products/:id            | Single product           |
| POST   | /api/products                | Create product           |
| PUT    | /api/products/:id            | Update product           |
| DELETE | /api/products/:id            | Delete product           |

### Customers
| Method | Path                   | Description              |
|--------|------------------------|--------------------------|
| GET    | /api/customers         | List (search)            |
| GET    | /api/customers/:id     | Single customer          |
| POST   | /api/customers         | Create customer          |
| PUT    | /api/customers/:id     | Update customer          |
| DELETE | /api/customers/:id     | Delete customer          |

### Orders
| Method | Path               | Description                   |
|--------|--------------------|-------------------------------|
| GET    | /api/orders        | List (status, customer, search)|
| GET    | /api/orders/:id    | Single order with items        |
| POST   | /api/orders        | Create order (deducts stock)   |
| PUT    | /api/orders/:id    | Update status / notes          |
| DELETE | /api/orders/:id    | Cancel & restore stock         |

---

## Frontend Usage — API Hooks

```jsx
import { useApi, useMutation } from "@/hooks/useApi";
import { productsApi, ordersApi } from "@/api";

// Fetch all products
function ProductList() {
  const { data: products, loading, error, refetch } = useApi(productsApi.getAll);
  if (loading) return <p>Loading...</p>;
  if (error)   return <p>Error: {error}</p>;
  return products.map(p => <div key={p.id}>{p.name}</div>);
}

// Create a product
function CreateProduct() {
  const { mutate, loading } = useMutation(productsApi.create);

  const handleSubmit = async (formData) => {
    const { data, error } = await mutate(formData);
    if (error) alert(error);
    else console.log("Created:", data);
  };
  // ...
}

// Fetch with filters
function LowStockAlert() {
  const { data } = useApi(productsApi.getAll, { low_stock_only: true });
  // ...
}
```

---

## Environment Variables

### Backend (`backend/.env`)
| Variable         | Default                                      |
|------------------|----------------------------------------------|
| `DATABASE_URL`   | `postgresql://ethara:ethara@db:5432/ethara`  |
| `ALLOWED_ORIGINS`| `["http://localhost:5173","http://localhost"]`|

### Frontend (`frontend/.env`)
| Variable        | Default                    |
|-----------------|----------------------------|
| `VITE_API_URL`  | `http://localhost:8000`    |
