import { useEffect, useState } from "react";
import axios from "axios";
import React from "react";

const AdminPanel = () => {
    const [apps, setApps] = useState([]);
    const [formData, setFormData] = useState({
        name: "",
        link: "",
        category: "",
        sub_category: "",
        points: 0,
    });

    useEffect(() => {
        checkAdmin();
        fetchApps();
    }, []);

    const checkAdmin = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/api/profile/", { withCredentials: true });
            if (!response.data.is_admin) {
                navigate("/login");
            }
        } catch (error) {
            console.error("Error checking admin status:", error);
            navigate("/login");
        }
    };

    const fetchApps = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:8000/admin/apps/", { withCredentials: true });
            setApps(response.data.apps);
        } catch (error) {
            console.error("Error fetching apps:", error);
        }
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post("http://127.0.0.1:8000/admin/apps/create/", formData, { withCredentials: true });
            fetchApps();
        } catch (error) {
            console.error("Error adding app:", error);
        }
    };

    const handleDelete = async (id) => {
        try {
            await axios.delete(`http://127.0.0.1:8000/admin/apps/delete/${id}/`, { withCredentials: true });
            fetchApps();
        } catch (error) {
            console.error("Error deleting app:", error);
        }
    };

    return (
        <div className="container mx-auto p-8">
            <h1 className="text-3xl font-bold mb-4">Admin Panel - Manage Apps</h1>
            <form onSubmit={handleSubmit} className="mb-4 p-4 bg-white shadow rounded flex flex-wrap gap-2">
                <input type="text" name="name" placeholder="App Name" className="border p-2 flex-1" onChange={handleChange} required />
                <input type="url" name="link" placeholder="App Link" className="border p-2 flex-1" onChange={handleChange} required />
                <input type="text" name="category" placeholder="Category" className="border p-2 flex-1" onChange={handleChange} required />
                <input type="text" name="sub_category" placeholder="Sub-category" className="border p-2 flex-1" onChange={handleChange} required />
                <input type="number" name="points" placeholder="Points" className="border p-2 w-24" onChange={handleChange} required />
                <button type="submit" className="bg-blue-500 text-white p-2 rounded">Add App</button>
            </form>

            <ul className="bg-gray-100 p-4 rounded">
                {apps.map((app) => (
                    <li key={app.id} className="flex justify-between p-2 bg-white shadow mb-2 rounded">
                        <span>{app.name} - {app.points} Points</span>
                        <button onClick={() => handleDelete(app.id)} className="bg-red-500 text-white p-1 rounded">Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default AdminPanel;
