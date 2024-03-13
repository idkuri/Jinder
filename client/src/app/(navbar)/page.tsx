import "../styles/globals.css"
import React, { useEffect } from "react";
import Image from 'next/image'
import dog from "../../../public/doggo.jpg";

export const Home: React.FC = () => {
  return (
    <main>
      <div className="homepage">
        <Image className="doggoPicture" src={dog} alt="Dog Picture"/>
        <h1 className="text-2xl">Welcome to Jinder!</h1>
      </div>
    </main>
  );
}

export default Home;
