import api from "./client";

export const dashboardApi = {
  // GET /api/dashboard/stats
  getStats: () => api.get("/api/dashboard/stats").then((r) => r.data),
};
