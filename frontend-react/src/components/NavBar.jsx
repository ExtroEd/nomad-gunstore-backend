import React from "react";


const NavBar = () => {
  return (
    <>
      <nav className="nav-bar">
        <ul className="nav-categories" id="nav-categories"></ul>
      </nav>
      <div className="category-dropdown" id="category-dropdown"></div>
    </>
  );
};

export default NavBar;
