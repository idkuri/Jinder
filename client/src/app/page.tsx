"use client"

import "./globals.css"
import Navbar from "./components/navbar"
import React, { useEffect } from "react";

export default function Home() {
  return (
    <main>
      <Navbar></Navbar>
      <div className="homepage">
        <h1 className="text-2xl">Hello World</h1>
      </div>
    </main>
  );
}
