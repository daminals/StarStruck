$(document).ready(function(){
  $("form").submit(function(event){
      event.preventDefault();
      $.post("/", "update", function(){
        setTimeout(function(){
          updatesrc = $('#graph').attr('src');
          $("#graph").removeAttr("src").attr("src", updatesrc + `?v=${getRandomInt(0,100)}`);
        }, 500);
      });
  });
});

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min) + min);
}