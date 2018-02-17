window.setInterval(function(){
    /// call your function here
    get_game_data()
  }, 3000);

function get_game_data(){
    var request = $.ajax({'url': '/getGameData?game_id='+gameID});
    request.done(function(response) 
    {
      $('#table_c_a').text(response.table_c_a);
      $('#table_a_aa').text(response.table_a_aa);
      $('#table_a_ab').text(response.table_a_ab);
      $('#table_c_b').text(response.table_c_b);
      $('#table_a_ba').text(response.table_a_ba);
      $('#table_a_bb').text(response.table_a_bb);
      $('#pl1').css("background", response.pl1);
      $('#pl1').css("border-color", response.pl1);
      $('#pl2').css("background", response.pl2);
      $('#pl2').css("border-color", response.pl2);
      
    });
    // request.fail(function(jqXHR, textStatus) 
    // {
    //   alert('Request failed: ' + textStatus);
    // });
}
