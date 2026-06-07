from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import engine
from app.db.base import Base
from app.api.routes import products, customers, orders, dashboard

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ethara API",
    description="Inventory & Order Management System API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(customers.router, prefix="/api/customers", tags=["Customers"])
app.include_router(orders.router, prefix="/api/orders", tags=["Orders"])


@app.get("/")
def root():
    return {"message": "Ethara API is running", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "ok"}
