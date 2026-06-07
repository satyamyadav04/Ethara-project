import api from "./client";

export const ordersApi = {
  // GET /api/orders
  getAll: (params = {}) => api.get("/api/orders", { params }).then((r) => r.data),

  // GET /api/orders/:id
  getById: (id) => api.get(`/api/orders/${id}`).then((r) => r.data),

  // POST /api/orders
  create: (data) => api.post("/api/orders", data).then((r) => r.data),

  // PUT /api/orders/:id  (update status, notes, etc.)
  update: (id, data) => api.put(`/api/orders/${id}`, data).then((r) => r.data),

  // DELETE /api/orders/:id
  delete: (id) => api.delete(`/api/orders/${id}`),
};
