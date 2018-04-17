const ENVIRONMENTS = {
  'localhost': 'dev',
  'cinetubbies.local  ': 'dev',
  'odin.onthewifi.com': 'stage'
};

const BACKEND_HOSTNAMES = {
  'dev': 'http://localhost:8000',
  'stage': 'http://odin.onthewifi.com'
};

const API_ROUTE = '/api';

export {
  ENVIRONMENTS,
  BACKEND_HOSTNAMES,
  API_ROUTE
};
