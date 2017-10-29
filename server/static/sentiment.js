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

      console.log(stock);

      var sentimentresponse;
      $.ajax({
        type: "POST",
        url: "/twitter",
        contentType: "application/json",
        data: JSON.stringify({'data':stock.name}),
        dataType:'json',
        success: function (response) {
          sentimentresponse = response;
          that.table.append(
            `
              <tr class="stockrow" data-symbol="${stock.symbol}">
                <td>${stock.symbol}</td>
                <td>${stock.name}</td>
                <td>${sentimentresponse.posComp}</td>
                <td>${sentimentresponse.negComp}</td>
                <td>${sentimentresponse.posSto}</td>
                <td>${sentimentresponse.negSto}</td>
                <td>${sentimentresponse.posWord}</td>
                <td>${sentimentresponse.negWord}</td>
                <td>${sentimentresponse.positive}</td>
                <td>${sentimentresponse.negative}</td>
                <td>${sentimentresponse.score}</td>
              </tr>
            `
          )

          return sentimentresponse;
        },
        error: function (err) {
          console.log('error', err);
          return;
        }
      });

      // that.table.append(
      //   `

      //   `
      // );
    });
  };

  testlist = [
    {'name':'Citigroup', 'symbol': 'C'},
    {'name':'Aegon', 'symbol': 'AEG'},
    {'name':'Microsoft', 'symbol': 'MSFT'},
    {'name':'Yahoo', 'symbol': 'YHOO'},
  ];

  var senttab = new SentimentList('twittertable', testlist);
  senttab.writeLines();

});
