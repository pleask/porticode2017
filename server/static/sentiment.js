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
          sentimentresponse = response[0];
          console.log(sentimentresponse);
          that.table.append(
            `
              <tr class="stockrow" data-symbol="${stock.symbol}">
                <td>${stock.symbol}</td>
                <td>${stock.name}</td>
                <td>${sentimentresponse.posComp.toFixed(2)}</td>
                <td>${sentimentresponse.negComp.toFixed(2)}</td>
                <td>${sentimentresponse.posSto.toFixed(2)}</td>
                <td>${sentimentresponse.negSto.toFixed(2)}</td>
                <td>${sentimentresponse.posWord.toFixed(2)}</td>
                <td>${sentimentresponse.negWord.toFixed(2)}</td>
                <td>${sentimentresponse.positive.toFixed(2)}</td>
                <td>${sentimentresponse.negative.toFixed(2)}</td>
                <td>${sentimentresponse.score.toFixed(2)}</td>
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

  testlist = [{"symbol": "ACC", "name": "American Campus Communities Inc"}, {"symbol": "ACCO", "name": "Acco Brands Corp"}, {"symbol": "ACH", "name": "Aluminum Corporation of China Ltd"}, {"symbol": "ACM", "name": "Aecom Technology Corp"}, {"symbol": "ACN", "name": "Accenture Plc"}, {"symbol": "ACP", "name": "Avenue Income Credit Strategies"}, {"symbol": "ACRE", "name": "Ares Commercial Real Estate Cor"}, {"symbol": "ADX", "name": "Adams Express Company"}, {"symbol": "AEB", "name": "Aegon N.V. Perp Cap Secs Floating Rate [Ne]"}, {"symbol": "AED", "name": "Aegon N.V. Perp Cap Secs [Ne]"}, {"symbol": "AEE", "name": "Ameren Corp"}, {"symbol": "AEG", "name": "Aegon N.V."}, {"symbol": "AEH", "name": "Aegon N.V. Perp Cap Secs"}, {"symbol": "AEK", "name": "Aegon Nv 8.00% Non-Cum Notes Due 2042"}, {"symbol": "AEL", "name": "American Equity Investment Life"}, {"symbol": "AGM", "name": "Federal Agricultural Mortgage Corp"}, {"symbol": "AGM-A", "name": "Federal Agricultural Mortgage"}, {"symbol": "BZH", "name": "Beazer Homes USA"}, {"symbol": "C", "name": "Citigroup Inc"}, {"symbol": "FNFV", "name": "Fnfv Group of Fidelity National"}, {"symbol": "FNV", "name": "Franco Nev Corp"}, {"symbol": "FOE", "name": "Ferro Corp"}, {"symbol": "FSB", "name": "Franklin Financial Network Inc"}, {"symbol": "FSCE", "name": "Fifth Street Finance Corp"}, {"symbol": "FSD", "name": "High Income Long Short Fund"}, {"symbol": "FSIC", "name": "FS Investment Corp"}, {"symbol": "FSM", "name": "Fortuna Silver Mines"}, {"symbol": "FSS", "name": "Federal Signal Corp"}, {"symbol": "FT", "name": "Franklin Universal Trust"}, {"symbol": "SUP", "name": "Superior Industries International"}, {"symbol": "SUPV", "name": "Grupo Supervielle S.A."}, {"symbol": "SWN", "name": "Southwestern Energy Company"}];

  var senttab = new SentimentList('twittertable', testlist);
  senttab.writeLines();

});
