
import Home from 'Components/Home.component';
import Login from 'Components/Login.component';
import Register from 'Components/Register.component';
import Welcome from 'Components/Welcome.component';
import Movies from 'Components/Movies/Movies.component';

export const routes = [
  {
    path: '/',
    name: 'welcome',
    component: Welcome,
    meta: {
      guest: true
    }
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: {
      guest: true
    }
  },
  {
    path: '/register',
    name: 'register',
    component: Register,
    meta: {
      guest: true
    }
  },
  {
    path: '/home',
    name: 'home',
    component: Home,
    meta: {
      logged: true
    }
  },
  {
    path: '/movies',
    name: 'movies',
    component: Movies
  }
];
