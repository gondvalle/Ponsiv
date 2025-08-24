import { BrowserRouter as Router, Routes, Route } from "react-router";
import { AuthProvider } from "@getmocha/users-service/react";
import HomePage from "@/react-app/pages/Home";
import AuthCallbackPage from "@/react-app/pages/AuthCallback";
import WardrobePage from "@/react-app/pages/Wardrobe";
import OutfitsPage from "@/react-app/pages/Outfits";
import SocialPage from "@/react-app/pages/Social";

export default function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/auth/callback" element={<AuthCallbackPage />} />
          <Route path="/wardrobe" element={<WardrobePage />} />
          <Route path="/outfits" element={<OutfitsPage />} />
          <Route path="/social" element={<SocialPage />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}
