import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "@/react-app/auth-shim";
import ExplorePage from "@/react-app/pages/Explore";
import LooksPage from "@/react-app/pages/Looks";
import FeedPage from "@/react-app/pages/Feed";
import CartPage from "@/react-app/pages/Cart";
import ProfilePage from "@/react-app/pages/Profile";
import AuthCallbackPage from "@/react-app/pages/AuthCallback";

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<ExplorePage />} />
          <Route path="/looks" element={<LooksPage />} />
          <Route path="/feed" element={<FeedPage />} />
          <Route path="/cart" element={<CartPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/auth/callback" element={<AuthCallbackPage />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}
