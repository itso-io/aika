import React from 'react';
import {connect} from 'react-redux';
import CssBaseline from '@material-ui/core/CssBaseline';
import Container from '@material-ui/core/Container';
import Checkbox from '@material-ui/core/Checkbox';
import Button from '@material-ui/core/Button';
import FormControl from '@material-ui/core/FormControl';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import * as actions from '../actions';
import { syncStatusPerCalendar } from '../getters';


const mapStateToProps = (state) => ({
  userEmail: state.getIn(['userInfo', 'email']),
  availableCalendars: state.get('availableCalendars'),
  syncStatusPerCalendar: syncStatusPerCalendar(state)
});


class SyncProgressIndicator extends React.Component {
  constructor(props) {
    super(props);

    this.state = { dotCount: 0 };
  }

  time() {
    const dotCount = this.state.dotCount === 3 ? 0 : this.state.dotCount + 1;

    this.setState({ dotCount });

    setTimeout(this.time.bind(this), 500);
  }

  componentDidMount() {
    this.time();
  }

  render() {
    return (
      <div>{`Syncing${[...Array(this.state.dotCount).keys()].map(k => '.').join('')}`}</div>
    );
  }
}


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
                onClick={this.props.updateSyncSettings}
            >
              Start sync
            </Button>
          </FormControl>
          <div style={{marginTop: '20px'}} />
          {
            this.props.syncStatus !== 'syncing' ? null :
                <SyncProgressIndicator />
          }
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
