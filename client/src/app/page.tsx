"use client"

import "./globals.css"
import Navbar from "./components/navbar"
import React, { useEffect } from "react";
import Image from 'next/image'
import dog from "../../public/doggo.jpg";

export default function Home() {
  return (
    <main>
      <Navbar/>
      <div className="homepage">
        <Image className="doggoPicture" src={dog} alt="Dog Picture"/>
        <h1 className="text-2xl">Hello World</h1>
      </div>
    </main>
  );
}
