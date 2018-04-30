
import Home from 'Components/Home.component';
import Login from 'Components/Login.component';
import Register from 'Components/Register.component';
import Welcome from 'Components/Welcome.component';
import Movies from 'Components/CinemaAdmin/Movies.component';
import Settings from 'Components/User/Settings.component';
import TheaterSettings from 'Components/Theaters/Settings.component';
import SystemAdminHome from 'Components/SystemAdmin/Home.component';
import Showtimes from 'Components/Showtimes/Showtimes.component';
import AdminHome from 'Components/CinemaAdmin/AdminHome.component';
import Reports from 'Components/CinemaAdmin/Reports.component';

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
    component: Movies,
    meta: {
      cinemaAdmin: true
    }
  },
  {
    path: '/user/settings',
    name: 'user-settings',
    component: Settings,
    meta: {
      logged: true
    }
  },
  {
    path: '/admin/system/:kind',
    name: 'admin-theaters',
    component: SystemAdminHome,
    meta: {
      logged: true
    }
  },
  {
    path: '/theater/settings',
    name: 'theater-settings',
    component: TheaterSettings,
    meta: {
      cinemaAdmin: true
    }
  },
  {
    path: '/showtimes',
    name: 'showtimes',
    component: Showtimes,
    meta: {
      cinemaAdmin: true
    }
  },
  {
    path: '/admin-home',
    name: 'adminHome',
    component: AdminHome,
    meta: {
      cinemaAdmin: true
    }
  },
  {
    path: '/reports',
    name: 'reports',
    component: Reports,
    meta: {
      cinemaAdmin: true
    }
  }
];
