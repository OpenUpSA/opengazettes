$(function() {
  // track outbound links
  $('a[href^=http]').on('click', function(e) {
    ga('send', 'event', 'outbound-click', e.target.href);
  });

  var url = window.location.href.split('/');

  $('#' + url[url.length - 1]).addClass('active');
});
