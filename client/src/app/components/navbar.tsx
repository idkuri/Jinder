"use client"
import "../styles/navbar.css";

export default function Navbar() {
    return (
        <div className="navbar">
            <div className="flex-1">
                <button className="btn btn-ghost text-xl" onClick={() => {window.location.href = "/"}}>Jinder</button>
            </div>
            <button className="btn btn-ghost text-l" onClick={() => {window.location.href = "/login"}}>Login</button>
            <button className="btn btn-ghost text-l" onClick={() => {window.location.href = "/register"}}>Register</button>
        </div>
    );
}