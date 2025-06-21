import React, { useEffect, useState } from "react";
import LoginModal from "./LoginModal";
import "../assets/styles/navbar.css";


const NavBar = () => {
  const [categories, setCategories] = useState([]);
  const [brands, setBrands] = useState([]);
  const [activeContent, setActiveContent] = useState(null);
  const [isDropdownVisible, setDropdownVisible] = useState(false);
  const [activeContentType, setActiveContentType] = useState(null);
  const [activeItemName, setActiveItemName] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const catRes = await fetch("/api/menu-categories/");
      const catData = await catRes.json();
      setCategories(catData);

      const brandRes = await fetch("/api/brands/");
      const brandData = await brandRes.json();
      setBrands(brandData);
    };

    fetchData();
  }, []);

  const menuItems = [
    { name: "Shop All", type: "shop_all" },
    ...categories.map(cat => ({ ...cat, type: "category" })),
    { name: "Brands", type: "brands" },
    { name: "Daily Deals", type: "daily_deals", highlight: true },
  ];

  const handleMouseEnter = (item) => {
    setDropdownVisible(true);
    setActiveContentType(item.type);
    setActiveItemName(item.name);

    if (item.type === "shop_all") {
      setActiveContent(buildCategoriesDropdown(categories));
    } else if (item.type === "category") {
      setActiveContent(buildSubcategoriesDropdown(item));
    } else if (item.type === "brands") {
      setActiveContent(buildBrandsDropdown(brands));
    } else {
      setDropdownVisible(false);
    }
  };

  const handleMouseLeave = () => {
    setDropdownVisible(false);
    setActiveContent(null);
    setActiveContentType(null);
    setActiveItemName(null);
  };

  return (
    <nav className="nav-bar">
      <ul className="nav-categories" onMouseLeave={handleMouseLeave}>
        {menuItems.map((item, index) => (
          <li
            key={index}
            className={item.highlight ? "daily-deals" : ""}
            onMouseEnter={() => handleMouseEnter(item)}
          >
            {item.name}

            {isDropdownVisible && activeItemName === item.name && (
              <div className="category-dropdown active">
                {activeContent}
              </div>
            )}
          </li>
        ))}
      </ul>
    </nav>
  );
};

// --- Sub-render functions ---
const buildCategoriesDropdown = (categories) => (
  <ul>
    {categories.map(cat => (
      <li key={cat.id}>{cat.name}</li>
    ))}
  </ul>
);

const buildSubcategoriesDropdown = (category) => (
  <div>
    <h3>{category.name}</h3>
    {category.children && category.children.length > 0 ? (
      <ul>
        {category.children.map(sub => (
          <li key={sub.id}>
            <strong>{sub.name}</strong>
            {sub.children && sub.children.length > 0 && (
              <ul>
                {sub.children.map(subsub => (
                  <li key={subsub.id}>{subsub.name}</li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>
    ) : (
      <p>No subcategories</p>
    )}
  </div>
);

const buildBrandsDropdown = (brands) => (
  <>
    <div className="brands-top">
      {brands.map(brand => (
        <div key={brand.id} className="brand-logo">
          <img src={brand.logo} alt={brand.name} />
        </div>
      ))}
    </div>
    <ul className="brands-list">
      {brands.map(brand => (
        <li key={brand.id}>{brand.name}</li>
      ))}
    </ul>
  </>
);

export default NavBar;
