import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Helmet } from "react-helmet";
import { Form, Input, Checkbox, Button, message } from 'antd';
import InputMask from 'react-input-mask';
import '../assets/styles/RegisterPage.css';


export default function RegisterPage() {
  const [form] = Form.useForm();
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleFinish = async (values) => {
    try {
      const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

      const response = await fetch(`${API_URL}/api/auth/register/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          first_name: values.firstName,
          last_name: values.lastName,
          email: values.email,
          phone_number: values.phone,
          use_phone_for_2fa: values.usePhoneFor2FA || false,
          sms_daily_deals: values.smsDailyDeals || false,
          newsletter_subscription: values.newsletter ?? true,
          password: values.password,
          confirm_password: values.confirmPassword,
        })
      });

      if (response.status === 201) {
        message.success("Account created! Please check your email for verification.");
        form.resetFields();
        navigate("/customer/account/confirm", {
          state: { email: values.email },
        });
      } else {
        const data = await response.json();
        const firstError = Object.values(data)?.[0]?.[0] || "Registration failed.";
        message.error(firstError);
        console.error("Backend error:", data);
      }
    } catch (error) {
      message.error("Server error. Please try again later.");
      console.error("Request error:", error);
    }
  };

  const phonePrefix = '+996';

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

          <Form
            form={form}
            onFinish={handleFinish}
            layout="vertical"
            className="register-form"
          >
            <h3 className="register-section-title">Personal Information</h3>

            <Form.Item
              label="First Name"
              name="firstName"
              rules={[{ required: true, message: 'This is a required field.' },
              { pattern: /^[A-Za-z ]+$/, message: 'Please use only letters (a-z or A-Z) or spaces only in this field.' }]}
            >
              <Input placeholder="Eren" />
            </Form.Item>

            <Form.Item
              label="Last Name"
              name="lastName"
              rules={[{ required: true, message: 'This is a required field.' },
              { pattern: /^[A-Za-z ]+$/, message: 'Please use only letters (a-z or A-Z) or spaces only in this field.' }]}
            >
              <Input placeholder="Yeger" />
            </Form.Item>

            <Form.Item
              label="Phone"
              name="phone"
              rules={[{
                required: false
              }, {
                pattern: /^\d{3}\s\d{3}\s\d{3}$/, message: 'Please enter a valid phone number. For example 700 123 456.'
              }]}
            >
              <Input
                addonBefore={phonePrefix}
                placeholder="700 123 456"
                maxLength={11}
              />
            </Form.Item>

            <Form.Item name="usePhoneFor2FA" valuePropName="checked">
              <Checkbox>
                Use this phone number for two factor authentication via SMS
              </Checkbox>
            </Form.Item>

            <Form.Item name="smsDailyDeals" valuePropName="checked">
              <Checkbox>
                Please send me Daily Deal Notifications at this phone number.
                Message frequency varies. Message and data rates may apply. Reply HELP for HELP or STOP to cancel.
              </Checkbox>
            </Form.Item>

            <p className="sms-terms-link">
              <a href="/help-center/terms-conditions.html#sms-marketing" target="_blank" rel="noopener noreferrer">SMS Terms of Service</a> &nbsp;&&nbsp;
              <a href="/opt-out" target="_blank" rel="noopener noreferrer">Privacy Policy</a>
            </p>

            <h3 className="register-section-title">Sign-in Information</h3>

            <Form.Item
              label="Email"
              name="email"
              rules={[{ required: true, message: 'This is a required field.' },
              { type: 'email', message: 'Please enter a valid email address (Ex: erenyeger@domain.com).' }]}
            >
              <Input placeholder="you@example.com" />
            </Form.Item>

            <Form.Item name="newsletter" valuePropName="checked" initialValue={true}>
              <Checkbox>Sign Up for Newsletter</Checkbox>
            </Form.Item>

            <Form.Item
              label="Password"
              name="password"
              rules={[{ required: true, message: 'This is a required field.' },
              {
                validator: (_, value) => {
                  if (!value || value.trim().length < 8) {
                    return Promise.reject('Minimum length of this field must be equal or greater than 8 symbols. Leading and trailing spaces will be ignored.');
                  }
                  const classes = [/[a-z]/, /[A-Z]/, /[0-9]/, /[^A-Za-z0-9]/];
                  const passed = classes.filter(rx => rx.test(value)).length;
                  if (passed < 3) {
                    return Promise.reject('Minimum of different classes of characters in password is 3. Classes of characters: Lower Case, Upper Case, Digits, Special Characters.');
                  }
                  return Promise.resolve();
                }
              }]}
            >
              <Input.Password visibilityToggle placeholder="Password" />
            </Form.Item>

            <Form.Item
              label="Confirm Password"
              name="confirmPassword"
              dependencies={["password"]}
              rules={[
                { required: true, message: 'This is a required field.' },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (!value || getFieldValue('password') === value) {
                      return Promise.resolve();
                    }
                    return Promise.reject('Passwords do not match.');
                  }
                })
              ]}
            >
              <Input.Password visibilityToggle placeholder="Confirm Password" />
            </Form.Item>

            <Form.Item
              name="notRobot"
              valuePropName="checked"
              rules={[{ validator: (_, value) => value ? Promise.resolve() : Promise.reject('Please confirm you are not a robot.') }]}
            >
              <Checkbox>I am not a robot</Checkbox>
            </Form.Item>

            <Form.Item>
              <Button type="primary" htmlType="submit" className="register-submit-btn">
                Submit
              </Button>
            </Form.Item>
          </Form>
        </div>
      </div>
    </>
  );
}
