import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api";

export const registerUser = async (userData) => {
    return axios.post(`${API_BASE_URL}/register/`, userData);
};

export const loginUser = async (credentials) => {
    return axios.post(`${API_BASE_URL}/login/`, credentials);
};

export const getUserData = async (token) => {
    return axios.get(`${API_BASE_URL}/profile/`, {
        headers: { Authorization: `Bearer ${token}` },
        withCredentials: true
    });
};

export const refreshToken = async (refresh) => {
    return await axios.post(`${API_BASE_URL}/token/refresh/`, { refresh });
};

export const fetchAllApps = async () => {
    const token = localStorage.getItem("access_token");
    return axios.get(`${API_BASE_URL}/admin/apps/`, {
        headers: { Authorization: `Bearer ${token}` },
        withCredentials: true
    });
};