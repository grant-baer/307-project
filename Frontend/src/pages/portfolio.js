import Link from "next/link";
import { isAuthenticated } from "./auth"; // Make sure to use the correct path
import Cookie from "js-cookie";
import React, { useEffect, useState } from "react";
import Image from "next/image";
import axios from "axios";

export default function Portfolio() {
  const [portfolio, setPortfolio] = useState(null);

  useEffect(() => {
    async function fetch_portfolio() {
      await axios.get("http://localhost:5000/fetch_portfolio",
        {
          headers: {
            "Authorization": `Bearer ${Cookie.get("token")}`
          }
        }).then(response => {
          console.log(response.data);
          setPortfolio(response.data);
        }).catch((error) => console.error("Error: ", error));
    }
    fetch_portfolio();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl mb-4">Portfolio</h1>
      <div className="grid grid-cols-3 gap-4">
        {portfolio && portfolio.map((image) =>
            <Image
                loader={() => image.url}
                src={image.url}
                width={500}
                height={500}
            />)}
      </div>
    </div>
  );
}
