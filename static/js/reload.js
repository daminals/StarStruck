$(document).ready(function(){
  $("form").submit(function(event){
      event.preventDefault();
      var pageURL = $(location).attr("href");
      var sendURL = pageURL.substring(pageURL.lastIndexOf('/') + 1).toUpperCase();
      console.log(sendURL)
      if (sendURL) {
        $.post('/coinPostRqs', {"data": sendURL}, function(){
          setTimeout(function(){
            updatesrc = $('#graph').attr('src');
            console.log("UPDATING GRAPH")
            $("#graph").removeAttr("src").attr("src", updatesrc + `?v=${getRandomInt(0,100)}`);
          }, 500);
        });
      } else {
        $.post('/', {"data": "portfolio"}, function(){
          setTimeout(function(){
            updatesrc = $('#graph').attr('src');
            console.log("UPDATING GRAPH")
            $("#graph").removeAttr("src").attr("src", updatesrc + `?v=${getRandomInt(0,100)}`);
          }, 500);
        });
      };
  });
});

function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min) + min);
};