$(document).ready(function(){
  $("form").submit(function(event){
      event.preventDefault();
      $.post("/", "update", function(){
        setTimeout(function(){
          updatesrc = $('#graph').attr('src');
          $("#graph").attr("src", updatesrc);
        }, 500);
      });
  });
});


