import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import MeetingTimePercentage from './MeetingTimePercentage';


import {connect} from 'react-redux';
import * as actions from '../../actions';
import { syncedCalendarDetails } from '../../getters';


const mapStateToProps = (state) => ({
  syncedCalendarDetails: syncedCalendarDetails(state)
});




class Analyses extends React.Component {
  render() {
    const calendarOptions = this.props.syncedCalendarDetails.map(cal => ({
      id: cal.get('id'),
      label: cal.get('summary')
    })).toJS();

    return (
        <div>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <MeetingTimePercentage calendarOptions={calendarOptions}/>
            </Grid>
          </Grid>
        </div>
    );
  }
}


export default connect(
    mapStateToProps,
    actions
)(Analyses)
