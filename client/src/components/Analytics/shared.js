const defaultChartJsOptions = {
  maintainAspectRatio: false,
  scales: {
    xAxes: [{
      stacked: true,
      gridLines: {
        display:false
      }
    }],
    yAxes: [{
      stacked: true,
      ticks: {
        beginAtZero: true,
        callback: function (value, index, values) {
          return `${value}%`;
        }
      },
      gridLines: {
        display:false
      }
    }]
  },
  legend: {
    position: 'bottom'
  }
}


export {
  defaultChartJsOptions,
}
