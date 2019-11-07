import React from 'react';
import {connect} from 'react-redux';
import CssBaseline from '@material-ui/core/CssBaseline';
import Container from '@material-ui/core/Container';
import Checkbox from '@material-ui/core/Checkbox';
import Button from '@material-ui/core/Button';
import FormControl from '@material-ui/core/FormControl';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import Visibility from '@material-ui/icons/Visibility';
import VisibilityOff from '@material-ui/icons/VisibilityOff';
import ReactTooltip from 'react-tooltip'
import * as actions from '../actions';
import { syncStatusPerCalendar } from '../getters';


const mapStateToProps = (state) => ({
  userEmail: state.getIn(['userInfo', 'email']),
  availableCalendars: state.get('availableCalendars'),
  syncedCalendars: state.get('syncedCalendars'),
  syncStatusPerCalendar: syncStatusPerCalendar(state),
  connectionDetails: state.get('databaseDetails')
});


class Cleartext extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      justCopied: false
    };
  }

  copy = () => {
    const { text } = this.props;

    navigator.clipboard.writeText(text);

    this.setState({justCopied: true});

    window.setTimeout(this.setState.bind(this, {justCopied: false}), 2000);
  };

  render() {
    const { text } = this.props;
    const { justCopied } = this.state;
    let dataTip = !justCopied ? 'Click to copy' : 'Copied!';
    if (!this.props.clickToCopy) {
      dataTip = null;
    }

    return (
        <span
          key={justCopied ? 'copied' : 'copy' /* (forces re-render of tooltip) */}
          data-tip={dataTip}
          style={{cursor: 'pointer'}}
          onClick={this.props.clickToCopy ? this.copy : () => {}}
        >
          {text}
          <ReactTooltip effect="solid" />
        </span>
    )
  }
}


class PasswordCell extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      showPassword: false,
    };
  }

  togglePassword = () => {
    this.setState({ showPassword: !this.state.showPassword });
  };

  render() {
    const { password } = this.props;
    const { showPassword } = this.state;

    return (
        <TableCell
            align="right"
            style={{display: 'flex', alignItems: 'center', 'fontFamily': '"Courier New", Courier, monospace'}}
        >
          {showPassword ?
              <VisibilityOff
                style={{marginLeft: '5px', cursor: 'pointer'}}
                onClick={this.togglePassword}
              />
              : <Visibility
                  style={{marginLeft: '5px', cursor: 'pointer'}}
                  onClick={this.togglePassword}
                />
          }
          {!showPassword ? <span>************</span> :
            <Cleartext text={password} clickToCopy={true} />
          }
        </TableCell>
    )
  }
}

const SyncStarted = () => {
  return  (
              <div>
                <p>
                  Aika has started syncing your calendar data to your very own MySQL database. Aika
                  initially syncs events from 30 days in the past and 30 days in the future, and the
                  sync will take about 30 seconds per calendar.
                </p>
                <p>
                  While we're working hard to add more analytics directly into Aika,
                  we also want you to be able to run any analysis you like as easily as
                  possible. To that end, we've already added you to
                  a <a href="https://www.metabase.com" target="_blank" rel="noopener noreferrer">Metabase</a> instance
                  we manage for you. You can use Metabase to:
                </p>
                <ul>
                  <li>
                    Create charts and dashboards using pure SQL
                  </li>
                  <li>
                    Create charts and dashboards using a point-and-click interface (no SQL required)
                  </li>
                  <li>
                    Examine the schema of the MySQL database we created for you
                  </li>
                </ul>
                <p>
                  To start using Metabase with your calendar data, head to <a href="https://bi.getaika.com">bi.getaika.com</a>. You're already signed in! &#x1f680;
                </p>
              </div>
  )
}

const ConnectionDetails = ({ details }) => {
  if (!details) return null;

  const rows = [
    {
      label: 'Host',
      value: details.get('host'),
      clickToCopy: true
    },
    {
      label: 'Port',
      value: details.get('port'),
      clickToCopy: true
    },
    {
      label: 'Username',
      value: details.get('username'),
      clickToCopy: true
    },
    {
      label: 'Password',
      value: details.get('password'),
      clickToCopy: true
    },
    {
      label: 'Database name',
      value: details.get('name'),
      clickToCopy: true
    },
    {
      label: 'Certificate Authority file for SSL',
      value: (
        <a href="https://s3.amazonaws.com/rds-downloads/rds-ca-2015-root.pem" target="_blank" rel="noopener noreferrer">
          Download here
        </a>
      ),
      clickToCopy: false
    }
  ];

  return (
      <div>
        <h4>
          MySQL connection details
        </h4>
        <Table aria-label="simple table">
          <TableBody>
            {rows.map(row => (
                <TableRow key={row.label}>
                  <TableCell component="th" scope="row">
                    {row.label}
                  </TableCell>
                      {row.label !== 'Password' ?
                      <TableCell align="right" style={{'fontFamily': '"Courier New", Courier, monospace'}}>

                            <Cleartext text={row.value} clickToCopy={row.clickToCopy} />
                      </TableCell>
                      : <PasswordCell password={row.value}/>
                      }
                </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
  );
};


class CalendarsSelector extends React.Component {
  constructor(props) {
    super(props);

    this.state = { syncing: false };
  }

  componentDidMount() {
    if (this.props.syncedCalendars.size === 0) {
      this.selectAll(true);
    }
  }

  selectAll = (select) => {
    this.props.availableCalendars.forEach(cal => this.props.selectCalendar(cal.get('id'), select));
  };

  handleChange = calendarId => event => {
    this.props.selectCalendar(calendarId, event.target.checked);
  };

  handleSubmit = () => {
    this.props.updateSyncSettings();

    this.setState({ syncing: true });
  };

  bulkSelect = () => {
    const noneSelected = this.props.syncedCalendars.size === 0;

    if (noneSelected) {
      this.selectAll(true);
    } else {
      this.selectAll(false);
    }
  };

  render() {
    const sortedCalendars = this.props.availableCalendars.sort(
      (cal1, cal2) => cal1.get('id') === this.props.userEmail ? -1 : 0
    );

    const noneSelected = this.props.syncedCalendars.size === 0;
    const allSelected = this.props.availableCalendars.size === this.props.syncedCalendars.size;

    return (
        <div>
          <h4>
            Calendars to sync
          </h4>
          <FormControl component="fieldset">
            <FormGroup>
              <FormControlLabel
                control={
                  <Checkbox
                    checked={!noneSelected}
                    onChange={this.bulkSelect}
                    color="secondary"
                    indeterminate={!noneSelected && !allSelected}
                  />
                }
                label=""
              />
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
                style={{marginTop: '5px'}}
                onClick={this.handleSubmit}
            >
              Start sync
            </Button>
          </FormControl>
          <div style={{marginTop: '20px'}} />
          {
            !this.state.syncing ? null :
            <SyncStarted />
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
          <Container maxWidth="md">
            <div style={{height: '20px'}}></div>
            <p>
              You are signed in as <b>{this.props.userEmail}</b>.
            </p>
            {this.props.availableCalendars.size === 0 ? null :
                <CalendarsSelectorContainer />
            }
            <br />
            <ConnectionDetails details={this.props.connectionDetails} />
          </Container>
        </React.Fragment>
    );
  }
}

export default connect(
    mapStateToProps,
    actions
)(DatabaseDetails);
