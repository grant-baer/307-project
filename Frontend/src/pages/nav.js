// Import React
import React from "react";

// NavBar Component
const NavBar = () => {
  return (
    <nav className="bg-black shadow-lg">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex justify-between">
          <div className="flex space-x-7">
            <div>
              {/* Brand Logo */}
              <a href="/" className="flex items-center py-4 px-2">
                <span className="font-semibold text-blue-500 text-lg">
                  PicturePerfect
                </span>
              </a>
            </div>
            {/* Primary Navbar items */}
            <div className="hidden md:flex items-center space-x-1">
              <a
                href="/"
                className="py-4 px-2 text-gray-300 font-semibold hover:text-blue-400 transition duration-300"
              >
                Home
              </a>
              <a
                href="/vote"
                className="py-4 px-2 text-gray-300 font-semibold hover:text-blue-400 transition duration-300"
              >
                Vote
              </a>
              <a
                href="/portfolio"
                className="py-4 px-2 text-gray-300 font-semibold hover:text-blue-400 transition duration-300"
              >
                Portfolio
              </a>
              <a
                href="/leaderboard"
                className="py-4 px-2 text-gray-300 font-semibold hover:text-blue-400 transition duration-300"
              >
                leaderboard
              </a>
            </div>
          </div>
          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button className="outline-none mobile-menu-button">
              <svg
                className=" w-6 h-6 text-gray-300 hover:text-blue-400 "
                x-show="!showMenu"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path d="M4 6h16M4 12h16M4 18h16"></path>
              </svg>
            </button>
          </div>
        </div>
      </div>
      {/* Mobile menu */}
      <div className="hidden mobile-menu">
        <ul className="">
          <li>
            <a
              href="/"
              className="block text-sm px-2 py-4 text-white bg-blue-500 font-semibold"
            >
              Home
            </a>
          </li>
          <li>
            <a
              href="/Vote"
              className="block text-sm px-2 py-4 hover:bg-blue-500 transition duration-300"
            >
              Vote
            </a>
          </li>
          <li>
            <a
              href="/Portfolio"
              className="block text-sm px-2 py-4 hover:bg-blue-500 transition duration-300"
            >
              Portfolio
            </a>
          </li>
          <li>
            <a
              href="/leaderboard"
              className="block text-sm px-2 py-4 hover:bg-blue-500 transition duration-300"
            >
              leaderboard
            </a>
          </li>
        </ul>
      </div>
    </nav>
  );
};

// Export NavBar
export default NavBar;
