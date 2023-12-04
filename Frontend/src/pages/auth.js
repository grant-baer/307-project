// auth.js (utility file)

// Import the required libraries
import jwt from 'jsonwebtoken';

// Secret key used to sign the JWT tokens (should match the key used in your backend)
const JWT_SECRET = 'CHANGE_TO_SECURE_KEY';

// Function to check if the user is authenticated based on the JWT token
export function isAuthenticated(token) {
  try {
    // Verify and decode the JWT token
    const decodedToken = jwt.verify(token, JWT_SECRET);

    // If the verification is successful, the user is authenticated
    return true;
  } catch (error) {
    // If there's an error, such as an expired or invalid token, the user is not authenticated
    return false;
  }
}