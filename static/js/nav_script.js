$(document).ready(function() {
    var $sticky = $(".sticky");
    var stickyOffsetTop = $sticky.offset().top;
  
    $(window).scroll(function(e) {
      e.preventDefault();
  
      var scrollTop = $(window).scrollTop();
  
      if (scrollTop > stickyOffsetTop) {
        $sticky.addClass("is-fixed");
      } else {
        $sticky.removeClass("is-fixed");
      }
    });
  });
  