import { use, useEffect, useState } from "react";
import { getUserData, refreshToken } from "../utils/api";
import { useNavigate } from "react-router-dom";
import React from "react";

const Dashboard = () => {
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem("access_token");
        const refresh = localStorage.getItem("refresh_token");

        if (!token || !refresh) {
            navigate("/login");
        } else {
            getUserData(token)
                .then(response => {
                    setUser(response.data);
                    // if (response.data.is_admin) {
                    //     navigate("/admin");
                    // }
                    
                })
                .catch(async (error) => {
                    if (error.response && error.response.status === 401) {
                        try {
                            const response = await refreshToken(refresh);
                            localStorage.setItem("access_token", response.data.access);
                            getUserData(response.data.access)
                                .then(response => setUser(response.data))
                                .catch(() => navigate("/login"));
                        } catch (refreshError) {
                            navigate("/login");
                        }
                    } else {
                        navigate("/login");
                    }
                });
        }
        
    }, []);

    const logout = () => {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        navigate("/login");
    };

    return (
        <div className="flex justify-center items-center h-screen bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-md w-96 text-center">
                <h2 className="text-2xl font-bold">Dashboard</h2>
                {user ? <p className="mt-4 text-gray-700">Welcome, {user.username}!</p> : <p>Loading...</p>}
                <button onClick={logout} className="w-full mt-4 bg-red-500 text-white py-2 rounded hover:bg-red-600">Logout</button>
            </div>
        </div>
    );
};

export default Dashboard;
