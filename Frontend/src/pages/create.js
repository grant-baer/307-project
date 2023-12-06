import React, { useState } from "react";
import axios from "axios";
import Image from "next/image";
import Cookie from "js-cookie";

export default function Home() {
  const [text, setText] = useState("");
  const [url, setUrl] = useState("");
  const [isImageAccepted, setImageAccepted] = useState(null); // null = not decided, true = accepted, false = rejected
  const [generating, setGenerating] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setGenerating(true);
      await axios.post(
        "http://localhost:5000/generate_image",
        { prompt: text },
      ).then(response => {
          if (response.data.output) {
            setUrl(response.data.output);
            setImageAccepted(null); // Reset the decision state when a new image is fetched
          } else if (response.data.error) {
            console.error(response.data.error);
          }
      }).then(() => setGenerating(false));

    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleAccept = () => {
    setImageAccepted(true);
    axios.post("http://localhost:5000/store_image",
        {
            "prompt": text,
            "url": url
        },
        {
            headers: {
                "Authorization": `Bearer ${Cookie.get("token")}`
            }
        });
  };

  const handleReject = () => {
    setImageAccepted(false);
    setUrl(""); // Clear the image if rejected, or add any other logic if needed
  };

  return (
    <div className="bg-gray-100 min-h-screen flex flex-col justify-center items-center">
      <form
        onSubmit={handleSubmit}
        className="p-8 bg-white shadow-lg rounded-lg"
      >
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter some text"
          className="border border-gray-300 p-2 rounded w-full mb-4"
        />
        <button
          type="submit"
          className="bg-blue-500 text-white p-2 rounded w-full hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-blue-300"
          disabled={generating}
        >
          {generating ? "Loading..." : "Submit"}
        </button>
      </form>

      {url && isImageAccepted === null && (
        <div className="mt-8">
          <Image
            loader={() => url}
            src={url}
            alt="Generated from input"
            width={500}
            height={500}
          />
          <div className="mt-4 flex justify-center gap-4">
            <button
              onClick={handleAccept}
              className="bg-green-500 text-white p-2 rounded hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500"
            >
              Accept
            </button>
            <button
              onClick={handleReject}
              className="bg-red-500 text-white p-2 rounded hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500"
            >
              Reject
            </button>
          </div>
        </div>
      )}

      {isImageAccepted === true && (
        <p className="mt-8 text-green-500">Image accepted!</p>
      )}
      {isImageAccepted === false && (
        <p className="mt-8 text-red-500">Image rejected.</p>
      )}
    </div>
  );
}
