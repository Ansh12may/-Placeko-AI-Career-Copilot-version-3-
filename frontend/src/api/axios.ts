import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

api.interceptors.request.use(
  (config) => {
    const token =
      localStorage.getItem("access_token");

    if (token) {
      config.headers.Authorization =
        `Bearer ${token}`;
    }

    // -------------------------------------------------------
    // JSON requests
    // -------------------------------------------------------
    // Only set JSON content type when the request
    // is NOT using FormData.
    //
    // For FormData, the browser must automatically
    // generate multipart/form-data + boundary.
    // -------------------------------------------------------

    if (!(config.data instanceof FormData)) {
      config.headers["Content-Type"] =
        "application/json";
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;