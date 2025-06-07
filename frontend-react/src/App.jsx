import React from "react";
import Header from "./components/Header";
import Footer from "./components/Footer";
import NavBar from "./components/NavBar";
import AgeVerification from "./components/AgeVerification";
import LoginModal from "./components/LoginModal";


const App = () => {
  return (
    <>
      <Header />
      <main>
        <NavBar />
      </main>
      <Footer />
      <AgeVerification />
      <LoginModal />
    </>
  );
};

export default App;
