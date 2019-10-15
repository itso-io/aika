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
  syncStatusPerCalendar: syncStatusPerCalendar(state),
  connectionDetails: state.get('databaseDetails')
});


class ClickToCopyText extends React.Component {
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

    return (
        <span
          key={justCopied ? 'copied' : 'copy' /* (forces re-render of tooltip) */}
          data-tip={!justCopied ? 'Click to copy' : 'Copied!'}
          style={{cursor: 'pointer'}}
          onClick={this.copy}
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
            style={{display: 'flex', alignItems: 'center', 'font-family': '"Courier New", Courier, monospace'}}
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
            <ClickToCopyText text={password} />
          }
        </TableCell>
    )
  }
}


const ConnectionDetails = ({ details }) => {
  if (!details) return null;

  const rows = [
    {
      label: 'Host',
      value: details.get('host')
    },
    {
      label: 'Port',
      value: details.get('port')
    },
    {
      label: 'Username',
      value: details.get('username')
    },
    {
      label: 'Password',
      value: details.get('password')
    },
    {
      label: 'Database name',
      value: details.get('name')
    }
  ];

  return (
      <div>
        <h4>
          MySQL Connection Details
        </h4>
        <Table aria-label="simple table">
          <TableBody>
            {rows.map(row => (
                <TableRow key={row.label}>
                  <TableCell component="th" scope="row">
                    {row.label}
                  </TableCell>
                  {row.label !== 'Password' ?
                      <TableCell align="right" style={{'font-family': '"Courier New", Courier, monospace'}}>
                        <ClickToCopyText text={row.value} />
                      </TableCell>
                      : <PasswordCell password={row.value} />
                  }
                </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
  );
};




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
          <h4>
            Calendars to sync
          </h4>
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
