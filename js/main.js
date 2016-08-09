$(function() {
  // track outbound links
  $('a[href^=http]').on('click', function(e) {
    ga('send', 'event', 'outbound-click', e.target.href);
  });
});
