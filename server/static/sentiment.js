$(document).ready(function() {

  var SentimentList = function (tableID, sentimentlist) {
    this.table = $("#" + tableID);
    this.stocks = sentimentlist;
  };

  SentimentList.prototype.setStocks = function (stocks) {
    this.stocks = stocks;
    this.writeLines();
  };

  /*stocks will look like
    {
      'symbol',
      'name',
      'value',
      'predicted'
    }
   */

  SentimentList.prototype.writeLines = function () {
    var that = this;
    this.stocks.forEach(function (stock) {

      getSentiment(stock.name);

      // that.table.append(
      //   `
      //     <tr class="stockrow" data-symbol="${stock.symbol}">
      //       <td>${stock.symbol}</td>
      //       <td>${stock.name}</td>
      //       <td>${stock.value}</td>
      //       <td>${stock.predicted}</td>
      //     </tr>
      //   `
      // );
    });
  };

  testlist = [
    {'name':'Apple', 'symbol': 'APPL'},
    {'name':'Google', 'symbol': 'GOOG'},
    {'name':'Microsoft', 'symbol': 'MCST'},
    {'name':'Yahoo', 'symbol': 'YAHO'},
  ];

  var senttab = new SentimentList('sentimenttable', testlist);
  senttab.writeLines();

  function getSentiment(name) {
    console.log('getsentiment', name);
    var sentimentresponse;
    $.ajax({
      type: "POST",
      url: "/twitter",
      contentType: "application/json",
      data: JSON.stringify({'data':'blackrock'}),
      dataType:'json',
      success: function (response) {
        sentimentresponse = response;
        console.log(sentimentresponse);

        return sentimentresponse;
      },
      error: function (err) {
        console.log('error', err);
        return;
      }
    });



  }
});
