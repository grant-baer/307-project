import Link from "next/link";
import { useState, useEffect } from "react";

export default function Leaderboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    // Generate fake data
    const fakeData = Array.from({ length: 10 }, (_, index) => ({
      id: index + 1,
      username: `User${index + 1}`,
      elo: 1000 + Math.floor(Math.random() * 500), // Random ELO between 1000 and 1500
    }));
    setData(fakeData);
  }, []);

  return (
    <div className="p-6">

      <h1 className="text-4xl font-bold mb-6 text-center text-gray-700">Leaderboard</h1>
      <table className="w-full text-left border-collapse border border-gray-400">
        <thead className="bg-gray-800 text-white">
          <tr>
            <th className="border border-gray-300 p-3">Name</th>
            <th className="border border-gray-300 p-3">Rank</th>
            <th className="border border-gray-300 p-3">ELO</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={item.id} className={`${index % 2 === 0 ? "bg-gray-100" : "bg-white"}`}>
              <td className="border border-gray-300 p-2">{item.username}</td>
              <td className="border border-gray-300 p-2">{index + 1}</td>
              <td className="border border-gray-300 p-2">{item.elo}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
