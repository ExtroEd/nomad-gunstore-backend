import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";

import Header from "./components/Header";
import Footer from "./components/Footer";
import NavBar from "./components/NavBar";
import ImageGrid from './components/ImageGrid';
import AgeVerification from "./components/AgeVerification";
import LoginModal from "./components/LoginModal";
import RegisterPage from "./components/RegisterPage";
import EmailConfirmPage from "./components/EmailConfirmPage";
import ScreenShots from "./components/ScreenShots";
import './app.css';


const ScrollToTopButton = () => {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setVisible(window.scrollY > 300);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return visible ? (
    <button
      className={`scroll-to-top ${visible ? "show" : ""}`}
      onClick={scrollToTop}
    >
      🡅
    </button>
  ) : null;
};

const AppContent = () => {
  const location = useLocation();

  const minimalRoutes = [
    "/customer/account/create",
    "/customer/account/confirm"
    ];

  const isMinimalPage = minimalRoutes.includes(location.pathname);

  return (
    <>
      <Header />
      <NavBar />

      {!isMinimalPage && <ImageGrid />}
      {!isMinimalPage && <ScreenShots />}

      <main>
        <Routes>
          <Route path="/customer/account/create" element={<RegisterPage />} />
          <Route path="/customer/account/confirm" element={<EmailConfirmPage />} />
        </Routes>
      </main>

      <Footer isMinimalPage={isMinimalPage} />

      {!isMinimalPage && <AgeVerification />}
      {!isMinimalPage && <LoginModal />}
      <ScrollToTopButton />
    </>
  );
};

const App = () => {
  return (
    <Router>
      <AppContent />
    </Router>
  );
};

export default App;
