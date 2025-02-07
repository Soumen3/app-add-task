import { useState, useEffect } from "react";
import { registerUser } from "../utils/api";
import { useNavigate } from "react-router-dom";
import React from "react";

const Signup = () => {
    const [formData, setFormData] = useState({ username: "", first_name:"", last_name:"", email: "", password: "" });
    const navigate = useNavigate();
    const [isMounted, setIsMounted] = useState(false);
    
    useEffect(() => {
        if (!isMounted) {
            const accessToken = localStorage.getItem("access_token");
            if (accessToken) {
                alert("You are already logged in!");
                navigate("/dashboard");
            }
            setIsMounted(true);
        }
    }, [isMounted, navigate]);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await registerUser(formData);
            alert("Signup successful!");
            navigate("/login");
        } catch (error) {
            console.log(error);
            
            alert("Signup failed!");
        }
    };

    return (
        <div className="flex justify-center items-center h-screen bg-gray-100">
            <div className="bg-white p-8 rounded-lg shadow-md w-96">
                <h2 className="text-2xl font-bold text-center mb-4">Sign Up</h2>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <input type="text" name="username" placeholder="Username" className="w-full p-2 border rounded" onChange={handleChange} required />
                    <input type="text" name="first_name" placeholder="First Name" className="w-full p-2 border rounded" onChange={handleChange} required />
                    <input type="text" name="last_name" placeholder="Last Name" className="w-full p-2 border rounded" onChange={handleChange} required />
                    <input type="email" name="email" placeholder="Email" className="w-full p-2 border rounded" onChange={handleChange} required />
                    <input type="password" name="password" placeholder="Password" className="w-full p-2 border rounded" onChange={handleChange} required />
                    <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">Sign Up</button>
                </form>
                <p className="text-center mt-4 text-gray-600">
                    Already have an account? <a href="/login" className="text-blue-500">Login</a>
                </p>
            </div>
        </div>
    );
};

export default Signup;
