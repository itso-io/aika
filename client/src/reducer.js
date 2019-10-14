import { Map, Set, fromJS } from 'immutable';

export default (state = Map(), action) => {
  switch (action.type) {
    case 'SET_STATE':
      return state.merge(fromJS(action.state));

    case 'SET_USER_INFO':
      return state.set('userInfo', fromJS(action.user));

    case 'SET_AVAILABLE_CALENDARS':
      return state.set('availableCalendars', fromJS(action.calendars));

    case 'SELECT_CALENDAR':
      return state.update(
          'syncedCalendars',
          cals => cals[action.selected ? 'add' : 'delete'](action.calendarId)
      );

    case 'UPDATE_SYNC_SETTINGS':
      return state
          .set('syncedCalendars', Set(action.syncConfig.synced_calendars))

    default:
      return state;
  }
}
