// // src/components/Login.js
// import React, { useState } from 'react';
// import axios from 'axios';

// const Login = () => {
//   const [formData, setFormData] = useState({ username: '', password: '' });
//   const [token, setToken] = useState(null);
//   const [error, setError] = useState('');

//   const handleChange = e => {
//     setFormData({ ...formData, [e.target.name]: e.target.value });
//     setError('');
//   };

//   const handleSubmit = async e => {
//     e.preventDefault();
//     try {
//       const res = await axios.post('http://127.0.0.1:8000/users/login/', formData);
//       setToken(res.data.access);
//       localStorage.setItem('access_token', res.data.access);
//       localStorage.setItem('refresh_token', res.data.refresh);
//     } catch (err) {
//       setError('Invalid username or password');
//     }
//   };

//   return (
//     <div>
//       <h2>Login</h2>
//       {token ? (
//         <p style={{ color: 'green' }}>Logged in! Token: {token.slice(0, 30)}...</p>
//       ) : (
//         <form onSubmit={handleSubmit}>
//           <input type="text" name="username" placeholder="Username" onChange={handleChange} required />
//           <input type="password" name="password" placeholder="Password" onChange={handleChange} required />
//           <button type="submit">Login</button>
//         </form>
//       )}
//       {error && <p style={{ color: 'red' }}>{error}</p>}
//     </div>
//   );
// };

// export default Login;





// src/components/Login.js
import React, { useState } from 'react';
import axios from 'axios';

const Login = () => {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [tokens, setTokens] = useState({ access: '', refresh: '' });
  const [error, setError] = useState('');

  const handleChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError('');
  };

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const res = await axios.post('http://127.0.0.1:8000/users/login/', formData);
      const { access, refresh } = res.data;

      // Store in localStorage (optional)
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);

      // Set tokens to state to display
      setTokens({ access, refresh });
    } catch (err) {
      setError('Invalid username or password');
      setTokens({ access: '', refresh: '' });
    }
  };

  return (
    <div>
      <h2>Login</h2>
      {!tokens.access ? (
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="username"
            placeholder="Username"
            onChange={handleChange}
            required
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            onChange={handleChange}
            required
          />
          <button type="submit">Login</button>
        </form>
      ) : (
        <div>
          <h4>Logged in successfully!</h4>
          <p><strong>Access Token:</strong></p>
          <textarea rows="5" cols="80" readOnly value={tokens.access} />
          <p><strong>Refresh Token:</strong></p>
          <textarea rows="5" cols="80" readOnly value={tokens.refresh} />
        </div>
      )}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default Login;
