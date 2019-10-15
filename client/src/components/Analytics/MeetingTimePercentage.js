import axios from 'axios';
import React from "react";
import Chart from "chart.js";
import FormControl from '@material-ui/core/FormControl';
import Input from '@material-ui/core/Input';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import Select from '@material-ui/core/Select';
import Chip from '@material-ui/core/Chip';
import { defaultChartJsOptions } from './shared';

const _ = require('lodash');


const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};


class PeriodSelector extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      selected: 'day'
    }
  }

  handleChange = event => {
    this.setState({selected: event.target.value});

    this.props.onChange(event.target.value);
  };

  render() {
    const { selected } = this.state;
    const { periodOptions: options } = this.props;

    return (
      <FormControl>
        <InputLabel htmlFor="select-period">Per</InputLabel>
        <Select
          value={selected}
          onChange={this.handleChange}
          input={<Input id="select-period" style={{minWidth: '100px'}} />}
        >
          {options.map(option => (
            <MenuItem key={option} value={option}>{option}</MenuItem>
          ))}
        </Select>
      </FormControl>
    )
  }
}


class CalendarSelector extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      selected: []
    }
  }

  handleChange = event => {
    this.setState({selected: event.target.value});
  };

  handleClose = () => {
    this.props.onChange(this.state.selected);
  };

  render() {
    const { selected } = this.state;
    const { calendarOptions: options } = this.props;

    const labelsById = options.reduce((byId, option) => {
      byId[option.id] = option.label;

      return byId;
    }, {});

    return (
        <FormControl>
          <InputLabel htmlFor="select-multiple-cals">Calendars</InputLabel>
          <Select
            multiple
            value={selected}
            onChange={this.handleChange}
            onClose={this.handleClose}
            input={<Input id="select-multiple-cals" style={{minWidth: '100px'}} />}
            renderValue={selected => (
              <div>
                {selected.map(id => (
                  <Chip key={id} label={labelsById[id]} />
                ))}
              </div>
            )}
            MenuProps={MenuProps}
          >
            {options.map(option => (
              <MenuItem key={option.id} value={option.id}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
    )
  }
}


class Controls extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      selectedCalendars: [],
      period: 'day'
    }
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    if (_.isEqual(prevState, this.state)) return;

    this.props.onChange(this.state);
  }

  onChange = (setting, value) => {
    if (this.state[setting] === undefined) throw Error(`Unexpected setting "${setting}"`)

    this.setState({[setting]: value});
  };

  render() {
    return (
        <div style={{margin: '10px 0', display: 'flex', alignItems: 'flex-end'}}>
          <CalendarSelector
              calendarOptions={this.props.calendarOptions}
              onChange={this.onChange.bind(this, 'selectedCalendars')}
          />
          <div style={{width: '10px'}} />
          <PeriodSelector
              periodOptions={['day', 'week', 'month']}
              onChange={this.onChange.bind(this, 'period')}
          />
        </div>
    );
  }
}


const backgroundColors = ['#512c62', '#f75f00', '#43ab92'];

const options = Object.assign(defaultChartJsOptions, {
  tooltips: {
    callbacks: {
      label: function (tooltipItem, data) {
        return `${data.datasets[tooltipItem.datasetIndex].label}: ${tooltipItem.yLabel}%`
      }
    }
  }
});

options.scales.yAxes[0].ticks = {
  callback: function (value, index, values) {
    return `${value}%`;
  }
};
options.scales.yAxes[0].gridLines.display = true;


export default class MeetingTimePercentage extends React.Component {

  constructor(props) {
    super(props);

    this.state = {
      rawData: null,
      latestCompletedQuery: null,
      settings: {
        calendarIds: [],

      },
    };
  }

  componentDidMount() {
    const initialQuery = 'SELECT date, confirmed_meeting_hours, unconfirmed_meeting_hours, remaining_hours FROM something'; // TODO: Real query.

    this.runQuery(initialQuery);
  }

  runQuery(query) {
    axios.get('/api/query', {
        params: {
          query: query
        }
      })
      .then(function (response) {
        this.setState({
          latestCompletedQuery: query,
          rawData: response.data
        })
      }.bind(this))
      .catch(function (error) {
        console.log(error);
      });
  }

  handleQueryCompleted() {
    const data = this.getFormattedData();

    var ctx = document.getElementById('percentageChart').getContext('2d');

    new Chart(ctx, {
        type: 'bar',
        data,
        options
    });
  }

  handleSettingsChange(newSettings) {
    // TODO: Construct new SQL query and run it.
    this.runQuery(JSON.stringify(newSettings))
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    if (prevState.latestCompletedQuery !== this.state.latestCompletedQuery){
      this.handleQueryCompleted();
    }
  }

  getFormattedData = () => {
    if (!this.state.rawData) return null;

    const { rawData } = this.state;

    const data = rawData.map((period) => {
      const totalHours = period.confirmed_meeting_hours + period.unconfirmed_meeting_hours + period.remaining_hours;

      return ['confirmed_meeting_hours', 'unconfirmed_meeting_hours', 'remaining_hours'].reduce((p, k) => {
        // TODO: Round percentages and ensure they add to 100.
        p[k] = p[k] / totalHours * 100;

        return p;
      }, period);
    });

    return {
        labels: data.map((period) => period.date),
        datasets: ['confirmed_meeting_hours', 'unconfirmed_meeting_hours', 'remaining_hours'].map((key, i) => ({
          label: key,
          data: rawData.map(period => period[key]),
          backgroundColor: backgroundColors[i],
          borderColor: 'black',
          borderWidth: 0
        }))
    };
  };

  render() {
    return (
      <div style={{display: 'flex', flexDirection: 'column'}}>
        <h4>
          Percentage of time spent in meetings
        </h4>
        <Controls
            calendarOptions={this.props.calendarOptions}
            onChange={this.handleSettingsChange.bind(this)}
        />
        <div>
          <canvas
              id="percentageChart"
              style={{height: '40vh', maxHeight: '500px'}}
          />
        </div>
      </div>
    );
  }
}
