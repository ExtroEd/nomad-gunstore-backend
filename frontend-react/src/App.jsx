import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Header from "./components/Header";
import Footer from "./components/Footer";
import NavBar from "./components/NavBar";
import AgeVerification from "./components/AgeVerification";
import LoginModal from "./components/LoginModal";
import RegisterPage from "./components/RegisterPage";
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

const App = () => {
  return (
    <Router>
      <Header />
      <NavBar />

      <main>
        <Routes>
          <Route path="/customer/account/create" element={<RegisterPage />} />
          {/* сюда добавляй другие страницы */}
        </Routes>
      </main>

      <Footer />

      <AgeVerification />
      <LoginModal />
      <ScrollToTopButton />
    </Router>
  );
};

export default App;
