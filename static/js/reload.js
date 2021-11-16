$(document).ready(function(){
  $("form").submit(function(event){
      event.preventDefault();
      var pageURL = $(location).attr("href"); // whole URL of webpage
      var sendURL = readURL(pageURL)
      console.log(sendURL) // check that its the right one lol
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

function readURL(URL) {
  return URL.substring(URL.lastIndexOf('/') + 1).toUpperCase(); // this is the /<coin> that i am sending to the backend to process the request
};