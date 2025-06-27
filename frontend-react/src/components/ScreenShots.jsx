import React from 'react';

const screenshots = [
  '/images/screenshots/img.png',
  '/images/screenshots/img_1.png',
  '/images/screenshots/img_2.png',
  '/images/screenshots/img_3.png',
  '/images/screenshots/img_4.png',
  '/images/screenshots/img_5.png',
];

const Screenshots = () => {
  return (
    <div className="container mt-5">
      <h2 className="mb-4">Скриншоты проекта</h2>
      <div className="row">
        {screenshots.map((src, index) => (
          <div className="col-12 mb-4" key={index}>
            <img src={src} alt={`Screenshot ${index + 1}`} className="img-fluid rounded shadow" />
          </div>
        ))}
      </div>
    </div>
  );
};

export default Screenshots;
