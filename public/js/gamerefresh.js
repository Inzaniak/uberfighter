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
      $('#table_l').text(response.table_l);
      $('#table_e').text(response.table_e);
      $('#table_c_ae').text(response.table_c_ae);
      $('#table_a_aae').text(response.table_a_aae);
      $('#table_a_abe').text(response.table_a_abe);
      $('#table_c_be').text(response.table_c_be);
      $('#table_a_bae').text(response.table_a_bae);
      $('#table_a_bbe').text(response.table_a_bbe);
      $('#table_le').text(response.table_le);
      $('#table_ee').text(response.table_ee);
      $('#pl1').css("background", response.pl1);
      $('#pl1').css("border-color", response.pl1);
      $('#pl2').css("background", response.pl2);
      $('#pl2').css("border-color", response.pl2);
      $('#pl3').css("background", response.pl3);
      $('#pl3').css("border-color", response.pl3);
      $('#pl4').css("background", response.pl4);
      $('#pl4').css("border-color", response.pl4);
      
    });
    // request.fail(function(jqXHR, textStatus) 
    // {
    //   alert('Request failed: ' + textStatus);
    // });
}
