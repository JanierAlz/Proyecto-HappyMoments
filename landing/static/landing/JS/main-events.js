ScrollReveal().reveal(".portfolio-item")
ScrollReveal().reveal(".row")

$(document).ready(function () {
     $(window).scroll(function() {
      
      if($(this).scrollTop() >= 10) { 
          $('#nav').addClass("nav2");
      } else {
          $('#nav').removeClass("nav2");
      }
    });
});