import React from "react";
import logo from ".../public/logo.png";
import "../assets/styles/styles.css";


const Header = ({ siteSettings }) => {
  const hasLogo = siteSettings?.logo;

  const getSvg = (name, fallbackPath) => {
    if (siteSettings?.svgIcons?.[name]) {
      return <span dangerouslySetInnerHTML={{ __html: siteSettings.svgIcons[name] }} />;
    }
    return <img src={fallbackPath} alt={`${name} icon`} />;
  };

  return (
    <header className="header">
      <div className="header-inner container">
        <div className="header-left">
          <a href="/" className="logo-link">
            <img
              src={hasLogo ? siteSettings.logo : logo}
              alt="Logo"
              className="logo"
            />
          </a>

          <form className="search-bar">
            <input
              type="text"
              className="search-input"
              placeholder="Search Nomad Tactical..."
            />
            <button type="submit" className="search-button">
              <span className="icon-wrapper">
                {getSvg("icon_search", "frontend-react/src/assets/images/search-icon.svg")}
              </span>
            </button>
          </form>
        </div>

        <div className="header-right">
          <button className="header-button">
            <span className="icon-wrapper">
              {getSvg("icon_login", "frontend-react/src/assets/images/account-icon.svg")}
            </span>
            <span>Log In</span>
          </button>

          <button className="header-button">
            <span className="icon-wrapper">
              {getSvg("icon_help", "frontend-react/src/assets/images/customer-service-icon.svg")}
            </span>
            <span>Help Center</span>
          </button>

          <button className="header-button">
            <span className="icon-wrapper">
              {getSvg("icon_cart", "frontend-react/src/assets/images/cart-icon.svg")}
            </span>
            <span>View Cart</span>
          </button>
        </div>
      </div>
    </header>
  );
};

export default Header;
