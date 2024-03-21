import type { Metadata } from "next";
import { Inter } from "next/font/google";
import Navbar from "../components/navbar"
import "../styles/globals.css";
import Cookies from 'js-cookie'
import React, { useEffect } from "react";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Jinder",
  description: "Project Description",
  icons: {
    icon: "/favicon.ico"
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
      <Navbar/>
      {children}
      </body>
    </html>
  );
}
