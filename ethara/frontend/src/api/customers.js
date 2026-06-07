import api from "./client";

export const customersApi = {
  // GET /api/customers
  getAll: (params = {}) => api.get("/api/customers", { params }).then((r) => r.data),

  // GET /api/customers/:id
  getById: (id) => api.get(`/api/customers/${id}`).then((r) => r.data),

  // POST /api/customers
  create: (data) => api.post("/api/customers", data).then((r) => r.data),

  // PUT /api/customers/:id
  update: (id, data) => api.put(`/api/customers/${id}`, data).then((r) => r.data),

  // DELETE /api/customers/:id
  delete: (id) => api.delete(`/api/customers/${id}`),
};
