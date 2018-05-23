import Home from 'Components/Home.component';
import Login from 'Components/Login.component';
import Register from 'Components/Register.component';
import Welcome from 'Components/Welcome.component';
import Movies from 'Components/CinemaAdmin/Movies.component';

import Profile from 'Components/User/Profile.component';
import UserProps from 'Components/User/Props.component';
import UserPropReservations from 'Components/User/PropReservations.component';
import UserSettings from 'Components/User/Settings.component';

import TheaterSettings from 'Components/Theaters/Settings.component';
import Theater from 'Components/Theaters/Theater.component';
import Movie from 'Components/Theaters/Movie.component';

import SystemAdminHome from 'Components/SystemAdmin/Home.component';
import SystemAdminRewards from 'Components/SystemAdmin/Rewards.component';

import FanZoneHome from 'Components/FanZone/Home.component';
import PropDetail from 'Components/FanZone/PropDetail.component';

import FanZoneAdminHome from 'Components/FanZoneAdmin/Home.component';
import PendingProps from 'Components/FanZoneAdmin/PendingProps.component';

import Showtimes from 'Components/Showtimes/Showtimes.component';
import Reports from 'Components/CinemaAdmin/Reports.component';
import TicketsOnSale from 'Components/CinemaAdmin/TicketsOnSale.component';

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
    component: UserSettings,
    meta: {
      logged: true
    }
  },
  {
    path: '/user/profile',
    name: 'user-profile',
    component: Profile,
    meta: {
      logged: true
    }
  },
  {
    path: '/user/props',
    name: 'user-props',
    component: UserProps,
    meta: {
      logged: true
    }
  },
  {
    path: '/user/prop-reservations',
    name: 'user-prop-reservations',
    component: UserPropReservations,
    meta: {
      logged: true
    }
  },
  {
    path: '/admin/system/rewards',
    name: 'system-admin-rewards',
    component: SystemAdminRewards,
    meta: {
      admin: true
    }
  },
  {
    path: '/admin/system/:kind',
    name: 'system-admin-theaters',
    component: SystemAdminHome,
    meta: {
      admin: true
    }
  },
  {
    path: '/admin/fan-zone/pending',
    name: 'admin-fan-zone-pending',
    component: PendingProps,
    meta: {
      fanZoneAdmin: true
    }
  },
  {
    path: '/admin/fan-zone/home',
    name: 'admin-fan-zone',
    component: FanZoneAdminHome,
    meta: {
      fanZoneAdmin: true
    }
  },
  {
    path: '/fan-zone',
    name: 'fan-zone',
    component: FanZoneHome,
    meta: {
      quest: true
    }
  },
  {
    path: '/fan-zone/prop/:id',
    name: 'fan-zone-prop',
    component: PropDetail,
    props: true,
    meta: {
      quest: true
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
    path: '/theater/:theaterId',
    name: 'theater',
    component: Theater,
    props: true
  },
  {
    path: '/theater/:theaterId/movie/:movieId',
    name: 'theater-movie',
    component: Movie,
    props: true
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
    path: '/reports',
    name: 'reports',
    component: Reports,
    meta: {
      cinemaAdmin: true
    }
  },
  {
    path: '/tickets-on-sale',
    name: 'ticketsOnSale',
    component: TicketsOnSale,
    meta: {
      cinemaAdmin: true
    }
  }
];
