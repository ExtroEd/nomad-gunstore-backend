import React, { useState, useEffect } from 'react';
import '../assets/styles/RegisterPage.css';
import { Helmet } from "react-helmet";


export default function RegisterPage() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    phone: '',
    email: '',
    newsletter: true,
    usePhoneFor2FA: false,
    smsDailyDeals: false,
    password: '',
    confirmPassword: ''
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Регистрация:', formData);
    // Добавь отправку на backend
  };

  return (
    <>
      <Helmet>
        <title>Create New Customer Account | Nomad Tactical</title>
      </Helmet>
      <div className="register-page">
        <div className="register-box">
          <h2 className="register-title">Create an Account</h2>
          <p className="register-subtitle">
            Create an account to track orders and access special promotions.
          </p>

          <form onSubmit={handleSubmit} className="register-form">
            <h3 className="register-section-title">Personal Information</h3>

            <label>First Name <span className="required">*</span></label>
            <input name="firstName" type="text" value={formData.firstName} onChange={handleChange} required />

            <label>Last Name <span className="required">*</span></label>
            <input name="lastName" type="text" value={formData.lastName} onChange={handleChange} required />

            <label>Phone</label>
            <input name="phone" type="tel" value={formData.phone} onChange={handleChange} placeholder="(996) 000-000" />

            <div className="checkbox-group">
              <label>
                <input type="checkbox" name="usePhoneFor2FA" checked={formData.usePhoneFor2FA} onChange={handleChange} />
                Use this phone number for two factor authentication via SMS
              </label>

              <label>
                <input type="checkbox" name="smsDailyDeals" checked={formData.smsDailyDeals} onChange={handleChange} />
                Please send me Daily Deal Notifications at this phone number.
                Message frequency varies. Message and data rates may apply. Reply HELP for HELP or STOP to cancel.
              </label>

              <p className="sms-terms-link">
                <a href="/help-center/terms-conditions.html#sms-marketing" target="_blank" rel="noopener noreferrer">SMS Terms of Service</a> &nbsp;&&nbsp;
                <a href="/opt-out" target="_blank" rel="noopener noreferrer">Privacy Policy</a>
              </p>
            </div>

            <h3 className="register-section-title">Sign-in Information</h3>

            <label>Email <span className="required">*</span></label>
            <input name="email" type="email" value={formData.email} onChange={handleChange} required />

            <label>
              <input type="checkbox" name="newsletter" checked={formData.newsletter} onChange={handleChange} />
              Sign Up for Newsletter
            </label>

            <label>Password <span className="required">*</span></label>
            <input name="password" type="password" value={formData.password} onChange={handleChange} required />
            <p className="password-strength">Password Strength: No Password</p>

            <label>Confirm <span className="required">*</span></label>
            <input name="confirmPassword" type="password" value={formData.confirmPassword} onChange={handleChange} required />

            <button type="submit" className="register-submit-btn">Submit</button>
          </form>
        </div>
      </div>
    </>
  );
}
