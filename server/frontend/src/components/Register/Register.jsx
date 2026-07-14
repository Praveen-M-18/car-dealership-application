import React, { useState } from 'react';
import './Register.css'; // Optional styling

const Register = () => {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [email, setEmail] = useState("");

    const handleRegister = async (e) => {
        e.preventDefault();
        
        // Target endpoint for user registration
        const registerUrl = window.location.origin + "/djangoapp/register";
        
        try {
            const res = await fetch(registerUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    "userName": username,
                    "password": password,
                    "firstName": firstName,
                    "lastName": lastName,
                    "email": email
                }),
            });

            const data = await res.json();
            if (data.status === "Authenticated") {
                sessionStorage.setItem('username', data.userName);
                alert("Registration successful! Welcome, " + data.userName);
                window.location.href = "/";
            } else if (data.error === "Already Registered") {
                alert("This username is already registered. Please try logging in.");
            } else {
                alert("Registration failed. Please check your inputs.");
            }
        } catch (error) {
            console.error("Error registering user:", error);
            alert("An error occurred. Please try again.");
        }
    };

    return (
        <div className="container d-flex justify-content-center align-items-center" style={{ minHeight: '80vh' }}>
            <div className="card p-4 shadow-sm" style={{ width: '100%', maxWidth: '450px' }}>
                <h3 className="text-center mb-4">Create an Account</h3>
                <form onSubmit={handleRegister}>
                    <div className="mb-3">
                        <label className="form-label">Username</label>
                        <input 
                            type="text" 
                            className="form-control" 
                            placeholder="Enter username" 
                            value={username} 
                            onChange={(e) => setUsername(e.target.value)} 
                            required 
                        />
                    </div>
                    <div className="mb-3">
                        <label className="form-label">First Name</label>
                        <input 
                            type="text" 
                            className="form-control" 
                            placeholder="Enter first name" 
                            value={firstName} 
                            onChange={(e) => setFirstName(e.target.value)} 
                            required 
                        />
                    </div>
                    <div className="mb-3">
                        <label className="form-label">Last Name</label>
                        <input 
                            type="text" 
                            className="form-control" 
                            placeholder="Enter last name" 
                            value={lastName} 
                            onChange={(e) => setLastName(e.target.value)} 
                            required 
                        />
                    </div>
                    <div className="mb-3">
                        <label className="form-label">Email Address</label>
                        <input 
                            type="email" 
                            className="form-control" 
                            placeholder="Enter email" 
                            value={email} 
                            onChange={(e) => setEmail(e.target.value)} 
                            required 
                        />
                    </div>
                    <div className="mb-3">
                        <label className="form-label">Password</label>
                        <input 
                            type="password" 
                            className="form-control" 
                            placeholder="Enter password" 
                            value={password} 
                            onChange={(e) => setPassword(e.target.value)} 
                            required 
                        />
                    </div>
                    <button type="submit" className="btn btn-primary w-100 mt-2">Register</button>
                </form>
            </div>
        </div>
    );
};

export default Register;
