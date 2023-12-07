// src/pages/leaderboard.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Image from 'next/image';

const Leaderboard = () => {
  const [images, setImages] = useState([]);

  useEffect(() => {
    // Make a GET request to your Flask server to fetch the top 20 images
    axios.get('http://localhost:5000/top_elo_images')
      .then((response) => {
        setImages(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <div className="bg-gray-100 min-h-screen py-8">
      <div className="container mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {images.map((image) => (
            <div key={image.id} className="bg-white p-4 rounded-lg shadow-md">
              <Image
              src={image.url}
               alt='Votable Image'
            width={1024}
            height={1024}
            style={{ width: '100%', height: '100%' }}
            className="w-full h-64 object-cover rounded-lg mb-4"
          />

              <div className="text-center">
                <p className="text-lg font-semibold">{image.creator}</p>
                <p className="text-gray-600">ELO: {image.elo}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Leaderboard;




// import Link from "next/link";
// import { useState, useEffect } from "react";

// export default function Leaderboard() {
//   const [data, setData] = useState([]);

//   useEffect(() => {
//     // Generate fake data
//     const fakeData = Array.from({ length: 10 }, (_, index) => ({
//       id: index + 1,
//       username: `User${index + 1}`,
//       elo: 1000 + Math.floor(Math.random() * 500), // Random ELO between 1000 and 1500
//     }));
//     setData(fakeData);
//   }, []);

//   return (
//     <div className="p-6">
//       <h1 className="text-4xl font-bold mb-6 text-center text-gray-700">
//         Leaderboard
//       </h1>
//       <table className="w-full text-left border-collapse border border-gray-400">
//         <thead className="bg-gray-800 text-white">
//           <tr>
//             <th className="border border-gray-300 p-3">Name</th>
//             <th className="border border-gray-300 p-3">Rank</th>
//             <th className="border border-gray-300 p-3">ELO</th>
//           </tr>
//         </thead>
//         <tbody>
//           {data.map((item, index) => (
//             <tr
//               key={item.id}
//               className={`${index % 2 === 0 ? "bg-gray-100" : "bg-white"}`}
//             >
//               <td className="border border-gray-300 p-2">{item.username}</td>
//               <td className="border border-gray-300 p-2">{index + 1}</td>
//               <td className="border border-gray-300 p-2">{item.elo}</td>
//             </tr>
//           ))}
//         </tbody>
//       </table>
//     </div>
//   );
// }
