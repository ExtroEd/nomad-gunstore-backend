import { Link } from 'react-router-dom';
import "../assets/styles/ImageGrid.css";


const ImageGrid = () => {
  return (
    <div className="image-block container mb-3">
      <div className="top-row">
        <Link to="/daily-deals-new/ar-15-pistol-sale">
          <img src="/images/ImageGrid/PSA-Homepage-2-AR15andARPCC.jpg" alt="Large" className="img-large" />
        </Link>
        <div className="wide-images">
          <Link to="/jakl">
            <img src="/images/ImageGrid/jakl10-3col.jpg" alt="Wide 1" />
          </Link>
          <Link to="/brands/pulsar">
            <img src="/images/ImageGrid/PSA-Web-3Col1-PulsarOpticsCL25.jpg" alt="Wide 2" />
          </Link>
          <Link to="/sabre">
            <img src="/images/ImageGrid/sabre_wood1_3col.jpg" alt="Wide 3" />
          </Link>
        </div>
      </div>
      <div className="bottom-row">
        <Link to="/brands/master-cutlery">
          <img src="/images/ImageGrid/Master-Cutlery-OTF-1x1.jpg" alt="Medium 1" />
        </Link>
        <Link to="/daily-deals-new/magazines">
          <img src="/images/ImageGrid/PSA-Block-1-JuneMag25.jpg" alt="Medium 2" />
        </Link>
        <div className="medium-with-text">
          <Link to="/brands/h-r-arms-co">
            <img src="/images/ImageGrid/PSA-W1x1-1-H_R.jpg" alt="Medium 3" />
          </Link>
          <h3>H&amp;R</h3>
        </div>
        <div className="medium-with-text">
          <Link to="/rebates-promotions">
            <img src="/images/ImageGrid/PSA-Homepage-1-Promos25.jpg" alt="Medium 4" />
          </Link>
          <h3>Promotions</h3>
        </div>
      </div>
    </div>
  );
};

export default ImageGrid;
