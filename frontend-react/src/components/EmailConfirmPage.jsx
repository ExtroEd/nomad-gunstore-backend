import { useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Form, Input, Button, message } from 'antd';
import { MailOutlined, ClockCircleOutlined, ReloadOutlined } from '@ant-design/icons';
import logo from "../assets/images/logo.png";
import "../assets/styles/email-confirm-page.css";


const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function EmailConfirmPage() {
  const [code, setCode] = useState(['', '', '', '', '', '']);
  const inputRefs = useRef([]);
  const [cooldown, setCooldown] = useState(0);
  const [email, setEmail] = useState('');
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const emailFromRegister = location.state?.email;
    if (!emailFromRegister) navigate('/customer/account/create');
    else setEmail(emailFromRegister);
  }, []);

  useEffect(() => {
    if (cooldown > 0) {
      const timer = setTimeout(() => setCooldown(cooldown - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [cooldown]);

  const handleChange = (val, index) => {
    if (!/^[0-9]?$/.test(val)) return;

    const newCode = [...code];
    newCode[index] = val;
    setCode(newCode);

    if (val && index < 5) inputRefs.current[index + 1]?.focus();
  };

  const handleKeyDown = (e, index) => {
    if (e.key === 'Backspace' && !code[index] && index > 0) {
      const newCode = [...code];
      newCode[index - 1] = '';
      setCode(newCode);
      inputRefs.current[index - 1]?.focus();
    }
  };

  const handlePaste = (e) => {
    const paste = e.clipboardData.getData('text').replace(/\D/g, '');
    if (paste.length === 6) {
      const newCode = paste.split('').slice(0, 6);
      setCode(newCode);
      inputRefs.current[5]?.focus();
    }
  };

  const handleSubmit = async () => {
    const fullCode = code.join('');
    if (fullCode.length !== 6) return message.error('Enter the 6-digit code');

    try {
      const res = await fetch(`${API_URL}/api/auth/verify-email/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, code: fullCode })
      });

      if (!res.ok) throw await res.json();
      message.success('Email verified!');
      navigate('/customer/account/');
    } catch (err) {
      console.error(err);
      message.error(err.code?.[0] || err.detail || 'Verification failed');
    }
  };

  const resendCode = async () => {
    try {
      const res = await fetch(`${API_URL}/api/auth/resend-verification-code/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email })
      });

      if (!res.ok) throw await res.json();
      message.success('Verification code resent.');
      setCooldown(60);
    } catch (err) {
      console.error(err);
      message.error(err.detail || 'Could not resend code.');
    }
  };

  const openEmail = (domain) => {
    const links = {
      gmail: 'https://mail.google.com/',
      mailru: 'https://e.mail.ru/',
      yahoo: 'https://mail.yahoo.com/',
      outlook: 'https://outlook.live.com/'
    };
    window.open(links[domain], '_blank');
  };

  return (
    <div className="email-confirm-page">
      <div className="confirm-box">
        <img src={logo} alt="Logo" className="logo" />
        <h2>We emailed you a code</h2>
        <p>We sent an email to <strong>{email}</strong>. Enter the code here or tap the button in the email to continue.</p>
        <p>If you don’t see the email, check your spam or junk folder.</p>

        <div className="code-input" onPaste={handlePaste}>
          {code.map((digit, index) => (
            <Input
              key={index}
              id={`digit-${index}`}
              maxLength={1}
              value={digit}
              onChange={e => handleChange(e.target.value, index)}
              onKeyDown={e => handleKeyDown(e, index)}
              ref={el => inputRefs.current[index] = el}
              className="digit-box"
            />
          ))}
        </div>

        <div className="email-links">
          <Button icon={<MailOutlined />} onClick={() => openEmail('gmail')}>Open Gmail</Button>
          <Button icon={<MailOutlined />} onClick={() => openEmail('mailru')}>Mail.ru</Button>
          <Button icon={<MailOutlined />} onClick={() => openEmail('outlook')}>Outlook</Button>
          <Button icon={<MailOutlined />} onClick={() => openEmail('yahoo')}>Yahoo</Button>
        </div>

        <div className="resend-section">
          <span>Can’t find your code? </span>
          <Button
            type="link"
            onClick={resendCode}
            disabled={cooldown > 0}
            icon={<ReloadOutlined />}
          >
            Request a new code
          </Button>
          {cooldown > 0 && <ClockCircleOutlined style={{ marginLeft: 8 }} />}
          {cooldown > 0 && <span style={{ marginLeft: 4 }}>{cooldown}s</span>}
        </div>

        <Button
          type="primary"
          danger
          className="submit-btn"
          onClick={handleSubmit}
        >
          Submit
        </Button>
      </div>
    </div>
  );
}
