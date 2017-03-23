$(function() {
  // track outbound links
  $('a[href^=http]').on('click', function(e) {
    ga('send', 'event', 'outbound-click', e.target.href);
  });

  var url = window.location.href.split('/');

  $('#' + url[url.length - 1]).addClass('active');
});

$(".monthly-chart").each(function(i) {
  var thisYear = $(this).attr("year");
  var data = collection.year_month[thisYear];
  
  var months = d3.keys(data).sort();

  var monthlyData = months.map(function(month) {
    return { 
      month: month,
      number: data[month],
    };
  });

  var margin = {top: 0, right: 0, bottom: 20, left: 0},
      width = $(this).parent().width() - margin.left - margin.right,
      height = 50 - margin.top - margin.bottom;

  var svg = d3.select(this).append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)

  var x = d3.scaleBand().rangeRound([0, width]).padding(0.1),
      y = d3.scaleLinear().rangeRound([height, 0]);

  var g = svg.append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  x.domain(monthlyData.map(function(d) { return d.month; }));
  y.domain([0, d3.max(monthlyData, function(d) { return d.number; })]);

  g.append("g")
    .attr("class", "axis axis--x")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x)
      .tickFormat(function(d) {
        return { 
          "01": "J",
          "02": "F",
          "03": "M",
          "04": "A",
          "05": "M",
          "06": "J",
          "07": "J",
          "08": "A",
          "09": "S",
          "10": "O",
          "11": "N",
          "12": "D",
          }[d];
        }));

  g.selectAll(".bar")
    .data(monthlyData)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.month); })
      .attr("y", function(d) { return y(d.number); })
      .attr("width", x.bandwidth())
      .attr("height", function(d) { return height - y(d.number); })
      .on("click", function(d) { document.location = thisYear + "#" + d.month });

  svg.selectAll("text.bar")
      .data(monthlyData)
    .enter().append("text")
      .attr("class", "bar")
      .attr("text-anchor", "middle")
      .attr("x", function(d) { return x(d.month) + x.bandwidth()/2; })
      .attr("y", function(d) { return y(d.number) - 5; })
      .text(function(d) { return d.number; });
});