import React, { useEffect, useState } from "react";
import logo from "../assets/images/logo.png";
import "../assets/styles/styles.css";
import axios from "axios";


const Header = () => {
  const [siteSettings, setSiteSettings] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const response = await axios.get(`/api/site-settings/?t=${Date.now()}`);
        setSiteSettings(response.data);
      } catch (error) {
        console.error("Error fetching site settings:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchSettings();
  }, []);

    const renderIcon = (iconType) => {
      if (!siteSettings?.icons?.[iconType]) {
        const fallbackIcons = {
          search: "/images/search-icon.svg",
          login: "/images/account-icon.svg",
          help: "/images/customer-service-icon.svg",
          cart: "/images/cart-icon.svg"
        };
        return <img src={fallbackIcons[iconType]} alt={`${iconType} icon`} />;
      }

      const svgString = siteSettings.icons[iconType];
      const parser = new DOMParser();
      const svgDoc = parser.parseFromString(svgString, 'image/svg+xml');
      const svgElement = svgDoc.querySelector('svg');

      if (!svgElement) {
        return <span>Invalid SVG</span>;
      }

      const svgHTML = new XMLSerializer().serializeToString(svgElement);
      return <span dangerouslySetInnerHTML={{ __html: svgHTML }} />;
    };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <header className="header">
      <div className="header-inner container">
        <div className="header-left">
          <a href="/" className="logo-link">
            <img
              src={siteSettings?.logo || logo}
              alt="Logo"
              className="logo"
            />
          </a>

          <form className="search-bar">
            <input
              type="text"
              className="search-input"
              placeholder={`Search ${siteSettings?.site_name || ''}...`}
            />
            <button type="submit" className="search-button">
              <span className="icon-wrapper">
                {renderIcon('search')}
              </span>
            </button>
          </form>
        </div>

        <div className="header-right">
          <button className="header-button">
            <span className="icon-wrapper">
              {renderIcon('login')}
            </span>
            <span>Log In</span>
          </button>

          <button className="header-button">
            <span className="icon-wrapper">
              {renderIcon('help')}
            </span>
            <span>Help Center</span>
          </button>

          <button className="header-button">
            <span className="icon-wrapper">
              {renderIcon('cart')}
            </span>
            <span>View Cart</span>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
