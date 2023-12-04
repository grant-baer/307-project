import Link from "next/link";
import { isAuthenticated } from "./auth"; // Make sure to use the correct path

export default function Portfolio() {
  return (
    <div className="p-6">
      <nav className="mb-4 flex justify-between">
        <Link href="/portfolio">Portfolio</Link>
        <Link href="/vote">Vote</Link>
        <Link href="/leaderboard">Leaderboard</Link>
        <button className="bg-blue-500 text-white py-1 px-3 rounded">
          Sign Out
        </button>
      </nav>
      <h1 className="text-2xl mb-4">Portfolio</h1>
      <div className="grid grid-cols-3 gap-4">
        {/* You can map through your portfolio images/items here */}
      </div>
    </div>
  );
}

export async function getServerSideProps(context) {
  const { req } = context;
  const token = req.cookies["token"]; // Replace "your_cookie_name" with your actual cookie name

  if (!isAuthenticated(token)) {
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
