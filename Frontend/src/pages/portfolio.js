import Link from "next/link";
import { isAuthenticated } from "./auth";
import Cookie from "js-cookie";
import React, { useEffect, useState } from "react";
import Image from "next/image";
import axios from "axios";

export default function Portfolio() {
  const [portfolio, setPortfolio] = useState(null);

  useEffect(() => {
    async function fetch_portfolio() {
      await axios
        .get("http://localhost:5000/fetch_portfolio", {
          headers: {
            Authorization: `Bearer ${Cookie.get("token")}`,
          },
        })
        .then((response) => {
          setPortfolio(response.data);
        })
        .catch((error) => console.error("Error: ", error));
    }
    fetch_portfolio();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl mb-4">Portfolio</h1>
      <div className="grid grid-cols-3 gap-4">
        {portfolio &&
          portfolio.map((image) => (
            <Image
              src={"data:image/png;base64, " + image.data}
              loader={() => image.url}
              height={500}
              width={500}
              alt="Portfolio Image"
            />
          ))}
      </div>
    </div>
  );
}

export async function getServerSideProps(context) {
  const { req } = context;
  const token = req.cookies["token"];

  if (!await isAuthenticated(token)) {
    // If the user is not authenticated, redirect them to the login page
    return {
      redirect: {
        destination: "/login",
        permanent: false,
      },
    };
  }

  // If the user is authenticated, render the Portfolio page
  return {
    props: {}, // Will be passed to the page component as props
  };
}