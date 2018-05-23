const ENVIRONMENTS = {
  'localhost': 'dev',
  'cinetubbies.local  ': 'dev',
  'odin.onthewifi.com': 'stage',
  'cinetubbies.pseudonick.com': 'stage',
};

const BACKEND_HOSTNAMES = {
  'dev': 'http://localhost:8000',
  'stage': 'https://cinetubbies.pseudonick.com',
};

const API_ROUTE = '/api';

export {
  ENVIRONMENTS,
  BACKEND_HOSTNAMES,
  API_ROUTE
};
