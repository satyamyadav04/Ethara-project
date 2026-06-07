import api from "./client";

export const productsApi = {
  // GET /api/products
  getAll: (params = {}) => api.get("/api/products", { params }).then((r) => r.data),

  // GET /api/products/:id
  getById: (id) => api.get(`/api/products/${id}`).then((r) => r.data),

  // GET /api/products/categories
  getCategories: () => api.get("/api/products/categories").then((r) => r.data),

  // POST /api/products
  create: (data) => api.post("/api/products", data).then((r) => r.data),

  // PUT /api/products/:id
  update: (id, data) => api.put(`/api/products/${id}`, data).then((r) => r.data),

  // DELETE /api/products/:id
  delete: (id) => api.delete(`/api/products/${id}`),
};
