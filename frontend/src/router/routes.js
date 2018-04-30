
import Home from 'Components/Home.component';
import Login from 'Components/Login.component';
import Register from 'Components/Register.component';
import Welcome from 'Components/Welcome.component';
import Movies from 'Components/Movies/Movies.component';
import Settings from 'Components/User/Settings.component';
import SystemAdminHome from 'Components/SystemAdmin/Home.component';
import FanZoneHome from 'Components/FanZone/Home.component';

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
    path: '/fan-zone',
    name: 'fan-zone',
    component: FanZoneHome,
    meta: {
      logged: true
    }
  }
];
