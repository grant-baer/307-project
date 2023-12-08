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
    <div className="bg-gray-100 min-h-screen p-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {portfolio && portfolio.map((image) => (
            <div key={image.url} className="w-full h-64 relative rounded-lg overflow-hidden mb-4"> {/* Add key here */}
              <Image 
                src={image.url}
                loader={() => image.url}
                layout="fill"
                objectFit="cover"
              />
            </div>
          ))}

        <Link legacyBehavior href="/create" passHref>
          <a className="w-full h-64 rounded-lg flex justify-center items-center border-4 border-dotted border-gray-300 hover:border-solid hover:bg-gray-50 transition-all duration-300 cursor-pointer">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
            </svg>
          </a>
        </Link>
      </div>
    </div>
  );
};


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
