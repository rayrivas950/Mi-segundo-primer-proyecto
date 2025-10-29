import api from './api';

const register = (username, password) => {
  return api.post('/auth/register', {
    username,
    password,
  });
};

const login = async (username, password) => {
  const response = await api.post('/auth/login', {
    username,
    password,
  });
  if (response.data.access_token) {
    localStorage.setItem('user', JSON.stringify(response.data));
  }
  return response.data;
};

const logout = () => {
  localStorage.removeItem('user');
  // Opcional: llamar al endpoint /auth/logout del backend para invalidar el token allí también.
};

const authService = {
  register,
  login,
  logout,
};

export default authService;
