document.addEventListener("DOMContentLoaded", async () => {
  const navList = document.getElementById("nav-categories");
  const dropdown = document.getElementById("category-dropdown");

  const res = await fetch("/api/menu-categories/");
  const categories = await res.json();

  const brandsRes = await fetch("/api/brands/");
  const brands = await brandsRes.json();

  const menuItems = [
    { name: "Shop All", type: "shop_all" },
    ...categories.map(cat => ({ ...cat, type: "category" })),
    { name: "Brands", type: "brands" },
    { name: "Daily Deals", type: "daily_deals", highlight: true }
  ];

  menuItems.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item.name;

    if (item.highlight) li.classList.add("daily-deals");

    li.addEventListener("mouseenter", () => {
      if (item.type === "shop_all") {
        dropdown.classList.add("active");
        dropdown.innerHTML = buildCategoriesDropdown(categories);
      } else if (item.type === "category" && item.children) {
        dropdown.classList.add("active");
        dropdown.innerHTML = buildSubcategoriesDropdown(item);
      } else if (item.type === "brands") {
        dropdown.classList.add("active");
        dropdown.innerHTML = buildBrandsDropdown(brands);
      } else {
        dropdown.classList.remove("active");
      }
    });

    navList.appendChild(li);
  });

  function buildCategoriesDropdown(categories) {
    let html = `<ul>`;
    categories.forEach(cat => {
      html += `<li>${cat.name}</li>`;
    });
    html += `</ul>`;
    return html;
  }

  function buildSubcategoriesDropdown(category) {
    let html = `<h3>${category.name}</h3>`;
    if (category.children && category.children.length > 0) {
      html += `<ul>`;
      category.children.forEach(sub => {
        html += `<li><strong>${sub.name}</strong>`;
        if (sub.children && sub.children.length > 0) {
          html += `<ul>`;
          sub.children.forEach(subsub => {
            html += `<li>${subsub.name}</li>`;
          });
          html += `</ul>`;
        }
        html += `</li>`;
      });
      html += `</ul>`;
    } else {
      html += "<p>No subcategories</p>";
    }
    return html;
  }

  function buildBrandsDropdown(brands) {
    let html = `<div class="brands-top">`;
    brands.forEach(brand => {
      html += `<div class="brand-logo"><img src="${brand.logo}" alt="${brand.name}"></div>`;
    });
    html += `</div><ul class="brands-list">`;
    brands.forEach(brand => {
      html += `<li>${brand.name}</li>`;
    });
    html += `</ul>`;
    return html;
  }

  document.body.addEventListener("mouseleave", () => {
    dropdown.classList.remove("active");
  });
});
