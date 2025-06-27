import React, { useEffect, useState } from "react";
import LoginModal from "./LoginModal";
import "../assets/styles/navbar.css";


const NavBar = () => {
  const [isDropdownVisible, setDropdownVisible] = useState(false);
  const [activeItemName, setActiveItemName] = useState(null);

  const menuItems = [
    { name: "Shop All", type: "shop_all" },
    { name: "Guns", type: "guns" },
    { name: "PSA", type: "psa" },
    { name: "AR-15", type: "ar_15" },
    { name: "AR-10", type: "ar_10" },
    { name: "AK-47", type: "ak_47" },
    { name: "Ammo", type: "ammo" },
    { name: "Suppressors", type: "suppressors" },
    { name: "Brands", type: "brands" },
    { name: "Daily Deals", type: "daily_deals", highlight: true },
  ];

  const imageMap = {
    shop_all: "/images/screenshots/img_6.png",
    guns: "/images/screenshots/img_7.png",
    psa: "/images/screenshots/img_8.png",
    ar_15: "/images/screenshots/img_9.png",
    ar_10: "/images/screenshots/img_10.png",
    ak_47: "/images/screenshots/img_11.png",
    ammo: "/images/screenshots/img_12.png",
    suppressors: "/images/screenshots/img_13.png",
    brands: "/images/screenshots/img_14.png",
  };

  const handleMouseEnter = (item) => {
    setDropdownVisible(true);
    setActiveItemName(item.name);
  };

  const handleMouseLeave = () => {
    setDropdownVisible(false);
    setActiveItemName(null);
  };

  return (
    <>
      <nav className="nav-bar">
        <ul className="nav-categories" onMouseLeave={handleMouseLeave}>
          {menuItems.map((item, index) => (
            <li
              key={index}
              className={item.highlight ? "daily-deals" : ""}
              onMouseEnter={() => handleMouseEnter(item)}
            >
              {item.name}
            </li>
          ))}
        </ul>
      </nav>

      {isDropdownVisible && activeItemName && (
        <div
          className="container"
          style={{
            marginTop: "10px",
            marginBottom: "20px",
          }}
        >
          <img
            src={imageMap[
              menuItems.find((m) => m.name === activeItemName)?.type
            ]}
            alt={activeItemName}
            style={{
              width: "100% !important",
              height: "auto !important",
              display: "block",
              borderRadius: "12px",
              boxShadow: "0 4px 12px rgba(0,0,0,0.2)",
              objectFit: "cover",
            }}
          />
        </div>
      )}
    </>
  );
};

export default NavBar;
