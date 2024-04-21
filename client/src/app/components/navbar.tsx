"use client"
import "../styles/navbar.css";
import React, {useEffect, useState} from 'react'
import Cookies from "js-cookie"

export default function Navbar() 
{
    const [mode, setMode] = useState(0) // if mode == 0, it means not logged in. if mode == 1 it means logged in
    const [username, setUsername] = useState("")

    useEffect(() => {
        authenticate()
      })
      
      async function authenticate() {
        const response = await fetch("/api/authenticate", {
          method: "GET",
        })
        if (response.status == 200) {
            const responseData = await response.json()
            setUsername(responseData['username'])
            setMode(1)
        }
      }

      async function logout() {
        const response = await fetch("/api/logout", {
            method: "POST"
        })
        if (response.status == 200) {
            window.location.reload()
        }
      }

      function renderNavbar() {
        if (mode === 0) {
            return(
                <div className="navbar">
                    <div className="flex-1">
                        <button className="btn btn-ghost text-xl" onClick={() => {window.location.href = "/"}}>Jinder</button>
                    </div>
                    <button className="btn btn-ghost text-l" onClick={() => {window.location.href = "/login"}}>Login</button>
                    <button className="btn btn-ghost text-l" onClick={() => {window.location.href = "/register"}}>Register</button>
                </div>
            )
        }
        else if (mode === 1) {
            return(
                <div className="navbar">
                    <div className="flex-1">
                        <button className="btn btn-ghost text-xl" onClick={() => {window.location.href = "/"}}>Jinder</button>
                    </div>
                    <button className="btn btn-ghost text-l" onClick={() => {window.location.href = "/chat"}}>Chatroom</button>
                    <h1 className="text-l">{username}</h1>
                    <button className="btn btn-ghost text-l" onClick={logout}>Logout</button>
                </div>
            )
        }
      }

    return (
        <>
        {renderNavbar()}
        </>
    );
}