// src/components/Register.js
import React, { useState } from 'react';
import axios from 'axios';

const Register = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    password2: '',
    email: '',
    first_name: '',
    last_name: '',
  });

  const [message, setMessage] = useState('');
  const [errors, setErrors] = useState({});

  const handleChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setErrors({});
  };

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/users/register/', formData);
      setMessage(response.data.message);
      setErrors({});
    } catch (error) {
      setErrors(error.response.data);
      setMessage('');
    }
  };

  return (
    <div>
      <h2>Register</h2>
      {message && <p style={{ color: 'green' }}>{message}</p>}
      <form onSubmit={handleSubmit}>
        {['username', 'email', 'first_name', 'last_name', 'password', 'password2'].map(field => (
          <div key={field}>
            <input
              type={field.includes('password') ? 'password' : 'text'}
              name={field}
              placeholder={field.replace('_', ' ')}
              value={formData[field]}
              onChange={handleChange}
              required
            />
            {errors[field] && <p style={{ color: 'red' }}>{errors[field]}</p>}
          </div>
        ))}
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;
