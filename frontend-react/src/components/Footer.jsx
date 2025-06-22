import React from "react";
import { FaPaperPlane } from "react-icons/fa";
import '../assets/styles/footer.css';
import { useLocation, Link } from "react-router-dom";


const Footer = () => {
  const location = useLocation();
  const isRegisterPage = location.pathname === "/customer/account/create";

  return (
    <footer>
      {/* 1. Newsletter Block */}
      {!isRegisterPage && (
        <section className="footer-newsletter">
          <div className="footer-newsletter-overlay" />

          <div className="newsletter-container text-center text-white">
            <div className="newsletter-text">
              <h2 className="fw-bold mb-3">Spirit of the Mountains</h2>
              <p className="fst-italic mb-4">
                As the wind guards the peaks of Ala-Too, so too shall the people guard their freedom.
                A nation born in resilience shall never kneel.
              </p>
            </div>

            <div className="newsletter-form d-flex justify-content-center">
              <input
                type="email"
                className="form-control w-auto"
                style={{ minWidth: '300px', maxWidth: '400px' }}
                placeholder="Sign up for our Daily Deals and News"
              />
              <button className="btn btn-danger ms-2">
                <FaPaperPlane className="text-white" />
              </button>
            </div>
          </div>
        </section>
      )}

      {/* 2. Content Placeholder */}
      <section className="footer-content text-white">
        <div className="container">
          <div className="footer-cta">
            <p className="footer-cta-text">
              Questions? Need help? Call us:{" "}
              <a href="tel:+996555553377" className="footer-cta-phone">
                (996) 555-55-33-77
              </a>
            </p>
          </div>

          <div className="footer-main">
            <div className="footer-badges d-flex flex-column">
              <img
                src="/images/c-cs_3x.png"
                alt="Static Badge"
                className="footer-badge-img badge-img-1"
              />

              <img
                src="/images/sezzle.png"
                alt="Static Badge"
                className="footer-badge-img badge-img-2"
              />

              <div className="d-flex gap-2">
                <a
                  href="https://sealserver.trustwave.com/cert.php?customerId=8ddd13daf2a0463ebd4bae185a989849&size=105x54&style="
                  target="_blank"
                  rel="noopener noreferrer"
                >
                <img
                  src="/images/secure-trust_3x.png"
                  alt="SSL Certificate"
                  className="footer-badge-img badge-img-3"
                />
                </a>
                <img
                  src="/images/siteseal-enterprise-ssl.png"
                  alt="Static Badge"
                  className="footer-badge-img badge-img-4"
                />
              </div>

              <a
                href="https://comodosslstore.com/blog/beginners-guide-to-comodo-ssl-certificate.html"
                target="_blank"
                rel="noopener noreferrer"
                className="text-white text-decoration-underline"
              >
                About SSL Certificates
              </a>

              <a
                href="https://www.bbb.org/us/sc/columbia/profile/gun-dealers/palmetto-state-armory-0663-34084856/#sealclick"
                target="_blank"
                rel="noopener noreferrer"
                className="footer-badge-img badge-img-5"
              >
              <img
                src="/images/bbb_3.png"
                alt="BBB"
                className="img-fluid"
              />
              </a>

              <a
                href="https://www.bbb.org/us/sc/columbia/profile/gun-dealers/palmetto-state-armory-0663-34084856/#sealclick"
                target="_blank"
                rel="noopener noreferrer"
                className="text-white text-decoration-underline"
              >
                Accredited as of 6/17/2025 | See BBB Reviews
              </a>
            </div>

            <div className="footer-links">
              <div className="footer-links-column">
                <h4 className="text-brand-red">Company</h4>
                <ul className="list-unstyled">
                  {[
                    "Blog",
                    "Careers",
                    "About PSA",
                    "Affiliate Program",
                    "Retail Stores",
                    "Defense Courses",
                    "SC CWP Info",
                    "Shoot Responsibly",
                    "Forum",
                    "The Gathering",
                    "Communication Preferences",
                  ].map((item, idx) => (
                    <li key={idx}>
                      <a href="#" className="text-white text-decoration-none">
                        {item}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="footer-links-column">
                <h4 className="text-brand-red">Info</h4>
                <ul className="list-unstyled">
                  {[
                    "Buying a Suppressor Online",
                    "Buying a Gun Online",
                    "Check Shipping Status",
                    "My Account",
                    "Contact Us",
                    "Rebates & Promotions",
                    "Check Order Status",
                    "Gift Card Balance",
                    "FAQ",
                    "FFL Locator",
                    "Product Manuals",
                    "California Buying Guide",
                    "Gun Terms Glossary",
                  ].map((item, idx) => (
                    <li key={idx}>
                      <a href="#" className="text-white text-decoration-none">
                        {item}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="footer-links-column">
                <h4 className="text-brand-red">Legal</h4>
                <ul className="list-unstyled">
                  {[
                    "Terms & Conditions",
                    "Retail Return Policy",
                    "Full Lifetime Warranty",
                    "Shipping Restrictions",
                    "Sitemap",
                  ].map((item, idx) => (
                    <li key={idx}>
                      <a href="#" className="text-white text-decoration-none">
                        {item}
                      </a>
                    </li>
                  ))}
                  <li className="footer-legal-item d-flex align-items-center gap-2">
                    <a href="#" className="text-white text-decoration-none">
                      Privacy Policy
                    </a>
                  </li>
                  <li className="footer-legal-item d-flex align-items-center gap-2">
                    <img
                      src="/images/optout-icon-blue.svg"
                      alt="Privacy Choices"
                      className="footer-privacy-icon"
                    />
                    <a href="#" className="text-white text-decoration-none">
                      Your Privacy Choices
                    </a>
                  </li>
                </ul>
              </div>

              <div className="footer-links-column d-flex flex-column">
                <div>
                  <h4 className="text-brand-red">Contact Information</h4>
                  <p className="mb-1">Palmetto State Armory</p>
                  <p className="mb-1">3760 Fernandina Rd.</p>
                  <p className="mb-3">Columbia, SC 29210</p>
                </div>
                <Link to="/help-center" className="btn-brand-red footer-help-btn text-white">
                  Help Center
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 3. Copyright */}
      <section className="footer-copyright d-flex flex-column w-100" style={{ backgroundColor: "#570c0a" }}>
        <div className="container d-flex justify-content-between align-items-center px-3" style={{ height: "77px" }}>
          <div className="d-flex gap-2">
            <a
              href="https://www.facebook.com/PalmettoStateArmory"
              className="social-btn d-flex align-items-center justify-content-center"
              target="_blank"
              rel="noopener noreferrer"
            >
              <i className="bi bi-facebook text-white"></i>
            </a>
            <a
              href="https://www.youtube.com/user/PSAGVEGAS"
              className="social-btn d-flex align-items-center justify-content-center"
              target="_blank"
              rel="noopener noreferrer"
            >
              <i className="bi bi-youtube text-white"></i>
            </a>
            <a
              href="https://x.com/palmettoarmory"
              className="social-btn d-flex align-items-center justify-content-center"
              target="_blank"
              rel="noopener noreferrer"
            >
              <i className="bi bi-twitter-x text-white"></i>
            </a>
            <a
              href="https://www.instagram.com/palmettostatearmoryofficial"
              className="social-btn d-flex align-items-center justify-content-center"
              target="_blank"
              rel="noopener noreferrer"
            >
              <i className="bi bi-instagram text-white"></i>
            </a>
          </div>

          <p className="footer-copyright-text">
            &copy; 2025 Nomad Tactical. All Rights Reserved.
          </p>
        </div>

        <div className="icon-credits">
          <p className="mb-0">
            Icons by{" "}
            <a href="https://www.flaticon.com/free-icons/search" target="_blank" rel="noopener noreferrer">Royyan Wijaya</a>,{" "}
            <a href="https://www.flaticon.com/free-icons/account" target="_blank" rel="noopener noreferrer">Google</a>,{" "}
            <a href="https://www.flaticon.com/free-icons/customer-service" target="_blank" rel="noopener noreferrer">Freepik</a>,{" "}
            <a href="https://www.flaticon.com/free-icons/retail" target="_blank" rel="noopener noreferrer">Frey Wazza</a>,{" "}
            <a href="https://www.flaticon.com/free-icons/admin" target="_blank" rel="noopener noreferrer">Us and Up</a>{" "}
            from <a href="https://www.flaticon.com/" target="_blank" rel="noopener noreferrer">Flaticon</a>
          </p>
        </div>
      </section>
    </footer>
  );
};

export default Footer;
