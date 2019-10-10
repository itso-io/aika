import React from 'react';
import {connect} from 'react-redux';
import CssBaseline from '@material-ui/core/CssBaseline';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';
import Checkbox from '@material-ui/core/Checkbox';
import Button from '@material-ui/core/Button';
import * as actions from '../actions';
import { syncStatusPerCalendar } from '../getters';


import FormLabel from '@material-ui/core/FormLabel';
import FormControl from '@material-ui/core/FormControl';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormHelperText from '@material-ui/core/FormHelperText';


const mapStateToProps = (state) => ({
  userEmail: state.getIn(['userInfo', 'email']),
  availableCalendars: state.get('availableCalendars'),
  syncStatusPerCalendar: syncStatusPerCalendar(state)
});


class CalendarsSelector extends React.Component {
  handleChange = calendarId => event => {
    this.props.selectCalendar(calendarId, event.target.checked);
  };

  render() {
    const sortedCalendars = this.props.availableCalendars.sort(
      (cal1, cal2) => cal1.get('id') === this.props.userEmail ? -1 : 0
    );

    return (
        <div>
          <p>
            Calendars to sync:
          </p>
          <FormControl component="fieldset">
            <FormGroup>
              {sortedCalendars.map(calendar => {
                const calendarId = calendar.get('id');

                return (
                    <FormControlLabel
                      key={calendarId}
                      control={<Checkbox checked={this.props.syncStatusPerCalendar.get(calendarId)} color="primary" onChange={this.handleChange(calendarId)} value={calendarId} />}
                      label={calendar.get('summary')}
                    />
                )
              })}
            </FormGroup>
            <Button
                variant="contained"
                color="primary"
                onClick={() => alert('yo')}
            >
              Start sync
            </Button>
          </FormControl>
        </div>
    );
  }
}

const CalendarsSelectorContainer = connect(
    mapStateToProps,
    actions
)(CalendarsSelector);


class DatabaseDetails extends React.Component {
  render() {
    if (!this.props.userEmail) return null;

    return (
        <React.Fragment>
          <CssBaseline />
          <Container maxWidth="sm">
            <div style={{height: '20px'}}></div>
            <p>
              You are signed in as <b>{this.props.userEmail}</b>.
            </p>
            <CalendarsSelectorContainer />
          </Container>
        </React.Fragment>
    );
  }
}

export default connect(
    mapStateToProps,
    actions
)(DatabaseDetails);
