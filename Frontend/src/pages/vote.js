// src/pages/vote.js
import React, { useState } from 'react';
import Image from 'next/image';

import styles from './vote.module.css';


export default function Vote() {
  const [images, setImages] = useState([{ src: '/image1.png', id: 1 }, { src: '/image1.png', id: 2 }]);
  const [selectedImage, setSelectedImage] = useState(null);

  const handleImageClick = (id) => {
    setSelectedImage(id);
    setTimeout(() => {
      setImages([{ src: '/image1.png', id: 3 }, { src: '/image1.png', id: 4 }]);
      setSelectedImage(null);
    }, 2000); // 2 seconds delay
  };

  return (
    <div className={styles.container}>
      {images.map((image) => (
        <div
          key={image.id}
          className={`${styles.imageWrapper} ${
            selectedImage === null
              ? styles.default
              : selectedImage === image.id
              ? styles.winning
              : styles.losing
          }`}
          onClick={() => handleImageClick(image.id)}
        >
          <Image
            src={image.src}
            alt='Votable Image'
            width={1024}
            height={1024}
            style={{ width: '100%', height: '100%' }}
          />
        </div>
      ))}
    </div>

  );
}


// import Image from "next/image";
// import { useState, useEffect } from "react";
// import eloRating from "elo-rating";
// import axios from "axios"; // Import axios for API requests

// export default function Vote() {
//   const [eloOne, setEloOne] = useState(1000);
//   const [eloTwo, setEloTwo] = useState(1000);
//   const [imageOne, setImageOne] = useState({});
//   const [imageTwo, setImageTwo] = useState({});

//   // Fetch random images from backend
//   const fetchRandomImages = async () => {
//     try {
//       const responseOne = await axios.get("http://localhost:5000/get_random_image");
//       const responseTwo = await axios.get("http://localhost:5000/get_random_image");
//       setImageOne(responseOne.data);
//       setImageTwo(responseTwo.data);
//       // Update ELOs if needed
//       setEloOne(responseOne.data.votes || 1000);
//       setEloTwo(responseTwo.data.votes || 1000);
//     } catch (error) {
//       console.error("Error fetching images:", error);
//     }
//   };

//   // Function to calculate ELO exchange and update backend
//   const vote = async (winner) => {
//     let result = eloRating.calculate(eloOne, eloTwo, winner === 1);
//     setEloOne(result.playerRating);
//     setEloTwo(result.opponentRating);

//     // API call to update the ELO rating in the backend
//     // You need to create this endpoint in your backend
//     await axios.post("http://localhost:5000/update_image_elo", {
//       imageIdOne: imageOne.id,
//       newEloOne: result.playerRating,
//       imageIdTwo: imageTwo.id,
//       newEloTwo: result.opponentRating,
//     });
//   };

//   // Load new images on each page load
//   useEffect(() => {
//     fetchRandomImages();
//   }, []);

//   return (
//     <div className="p-6">
//       <h1 className="text-4xl font-bold mb-6 text-center text-gray-700">
//         Voting
//       </h1>
//       <div className="flex justify-center gap-10 mb-4">
//         <div className="text-center">
//           <Image
//             src={imageOne.url}
//             alt="Image One"
//             className="w-60 h-60 object-cover rounded-lg shadow-lg hover:shadow-2xl cursor-pointer"
//             onClick={() => vote(1)}
//           />
//           <p className="mt-2 text-lg font-semibold">ELO: {eloOne}</p>
//         </div>
//         <div className="text-center">
//           <Image
//             src={imageTwo.url}
//             alt="Image Two"
//             className="w-60 h-60 object-cover rounded-lg shadow-lg hover:shadow-2xl cursor-pointer"
//             onClick={() => vote(2)}
//           />
//           <p className="mt-2 text-lg font-semibold">ELO: {eloTwo}</p>
//         </div>
//       </div>
//     </div>
//   );
// }
