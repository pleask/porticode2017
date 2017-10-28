var allColors = [
  'rgb(255, 0, 0)',
  'rgb(0, 128, 255)',
  'rgb(255, 255, 0)',
  'rgb(128, 255, 0)',
  'rgb(0, 255, 128)',
  'rgb(255, 128, 0)',
];

var DataStore = function () {
  /*
    Object for storing market data for display.
    Includes parameters about what is to be shown, including date range,
    name of stock price, step size etc. etc.
  */
  this.observers = new resources.ObserverList();

  this.usedColors = [];

  this.data = [];
};

DataStore.prototype.addObserver = function (observer) {
  this.observers.add(observer);
};


DataStore.prototype.removeObserver = function (observer) {
  this.observers.removeAt( this.observers.indexOf( observer, 0 ) );
};

DataStore.prototype.notify = function (context) {
  var observerCount = this.observers.count();
  for(var i=0; i < observerCount; i++){
    this.observers.get(i).update( context );
  }
};

DataStore.prototype.addData = function (data) {
  /* data comes in following format:
    {
      'name',
      'data',
      'startDate',
      'endDate'
    }
  */

  var dataCount = this.data.length;
  for ( var i = 0 ; i < dataCount; i ++) {
      if (this.data[i].name === data.name) {
        return;
      }
  }

  var newdata = {
    'name': null,
    'data': null,
    'startDate': null,
    'endDate': null
  };

  var that = this;

  if (!data.name) {
    throw 'Data needs a name';
  } else {
    newdata.name = data.name;
  }

  if (!data.data) {
    throw 'Data needs to exist';
  } else {
    newdata.data = data.data;
  }

  if (!data.startDate) {
    throw 'Data needs a start date';
  } else {
    newdata.startDate = data.startDate;
  }

  if (!data.endDate) {
    data.endDate = Date.now();
  } else {
    newdata.endDate = data.endDate;
  }

  newdata.color = this.remainingColors()[0];
  this.usedColors.push(newdata.color);

  this.data.push(newdata);


  this.notify(this.data);
};

DataStore.prototype.remainingColors = function () {
  var that = this;
  return allColors.filter(function(x) { return that.usedColors.indexOf(x) < 0 ;});
};

DataStore.prototype.removeData = function (name) {
  var dataCount = this.data.length;
  for ( var i = 0 ; i < dataCount; i ++) {
      if (this.data[i].name === name) {

        this.usedColors.splice(this.usedColors.indexOf(this.data[i].color), 1)
        this.data.splice(i, 1);
        break;
      }
  }

  this.notify(this.data);
};

var StockChart = function (canvasID) {
  this.canvasID = canvasID;
};

StockChart.prototype.update = function (data) {
  this.data = data;
  this.plot();
};

StockChart.prototype.plot = function () {

  var that = this;
  var ctx = document.getElementById('tickercanvas').getContext('2d');
  var myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: that.labelsFormat(),
      datasets: that.tickerFormat()
    }
  });
};

StockChart.prototype.labelsFormat = function () {
  labels = [];
  this.data[0].data.forEach(function (datum) {
    labels.push(new Date(datum.date));
  });
  return labels;
};

StockChart.prototype.tickerFormat = function () {
  var datasets = [];
  this.data.forEach(function (dataSet) {
      currdata = {};
      currdata.label = dataSet.name;
      currdata.data = [];
      dataSet.data.forEach( function (x) {
        currdata.data.push(x.price);
      });
      currdata.borderColor = dataSet.color;
      currdata.fill = false;
      datasets.push(currdata);
  });


  return datasets;
};

var StockList = function (tableID) {
  this.table = $("#" + tableID);
};

var sampleData = {
  'name': 'AAPL',
  'data': [
    {'date': '2017-07-24', 'price': '152.09'},
    {'date': '2017-07-25', 'price': '152.74'},
    {'date': '2017-07-25', 'price': '152.74'},
    {'date': '2017-07-26', 'price': '153.46'}
  ],
  'startDate': '2017-07-24',
  'endDate': '2017-08-04'
};

var sampleData2 = {
  'name': 'GOOG',
  'data': [
    {'date': '2017-07-24', 'price': '162.09'},
    {'date': '2017-07-25', 'price': '162.74'},
    {'date': '2017-07-25', 'price': '162.74'},
    {'date': '2017-07-26', 'price': '163.46'}
  ],
  'startDate': '2017-07-24',
  'endDate': '2017-08-04'
};

var sampleData3 = {
  'name': 'AMAZ',
  'data': [
    {'date': '2017-07-24', 'price': '172.09'},
    {'date': '2017-07-25', 'price': '172.74'},
    {'date': '2017-07-25', 'price': '172.74'},
    {'date': '2017-07-26', 'price': '173.46'}
  ],
  'startDate': '2017-07-24',
  'endDate': '2017-08-04'
};

var sampleData4 = {
  'name': 'MCST',
  'data': [
    {'date': '2017-07-24', 'price': '182.09'},
    {'date': '2017-07-25', 'price': '182.74'},
    {'date': '2017-07-25', 'price': '182.74'},
    {'date': '2017-07-26', 'price': '183.46'}
  ],
  'startDate': '2017-07-24',
  'endDate': '2017-08-04'
};


$(document).ready(function () {

  var testdata = new DataStore();

  var testUser = new StockChart('tickercanvas');

  testdata.addObserver(testUser);

  testdata.addData(sampleData);
  testdata.addData(sampleData2);
  testdata.addData(sampleData3);
  testdata.addData(sampleData4);
  // testdata.removeData('AAPL');
});
