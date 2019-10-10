const axios = require('axios');


const receiveUserInfo = (user) => ({
  type: 'SET_USER_INFO',
  user
});


export const fetchUserInfo = () => (dispatch, getState) => {
  axios.get('/api/users/me')
    .then(function (response) {
      dispatch(receiveUserInfo(response.data));
    })
    .catch(function (error) {
      console.log(error);
    });
};


const receiveAvailableCalendars = (calendars) => ({
  type: 'SET_AVAILABLE_CALENDARS',
  calendars
});


export const fetchAvailableCalendars = () => (dispatch, getState) => {
  axios.get('/api/calendars')
    .then(function (response) {
      dispatch(receiveAvailableCalendars(response.data));
    })
    .catch(function (error) {
      console.log(error);
    });
};


export const selectCalendar = (calendarId, selected) => ({
  type: 'SELECT_CALENDAR',
  calendarId,
  selected
});
