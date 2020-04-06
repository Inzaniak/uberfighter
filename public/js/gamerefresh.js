window.setInterval(function() {
  /// call your function here
  get_game_data();
}, 3000);

function get_game_data() {
  var request = $.ajax({ url: "/getGameData?game_id=" + gameID });
  request.done(function(response) {
    if (response.reset_votes == 1) {
      document.getElementById("charactera").setAttribute( "onClick","send_vote(1,"+gameID+")");
      document.getElementById("characterb").setAttribute( "onClick","send_vote(2,"+gameID+")");
    };
    $("#table_c_a").text(response.table_c_a);
    $("#table_a_aa").text(response.table_a_aa);
    $("#table_a_ab").text(response.table_a_ab);
    $("#table_c_b").text(response.table_c_b);
    $("#table_a_ba").text(response.table_a_ba);
    $("#table_a_bb").text(response.table_a_bb);
    $("#table_l").text(response.table_l);
    $("#table_e").text(response.table_e);
    $("#table_c_ae").text(response.table_c_ae);
    $("#table_c_av").text(response.table_c_av);
    $("#table_a_aae").text(response.table_a_aae);
    $("#table_a_abe").text(response.table_a_abe);
    $("#table_c_be").text(response.table_c_be);
    $("#table_c_bv").text(response.table_c_bv);
    $("#table_a_bae").text(response.table_a_bae);
    $("#table_a_bbe").text(response.table_a_bbe);
    $("#table_le").text(response.table_le);
    $("#table_ee").text(response.table_ee);
    $("#pl1").css("background", response.pl1);
    $("#pl1").css("border-color", response.pl1);
    $("#pl2").css("background", response.pl2);
    $("#pl2").css("border-color", response.pl2);
    $("#pl3").css("background", response.pl3);
    $("#pl3").css("border-color", response.pl3);
    $("#pl4").css("background", response.pl4);
    $("#pl4").css("border-color", response.pl4);
    $("#pl5").css("background", response.pl5);
    $("#pl5").css("border-color", response.pl5);
    $("#pl6").css("background", response.pl6);
    $("#pl6").css("border-color", response.pl6);
    $("#pl7").css("background", response.pl7);
    $("#pl7").css("border-color", response.pl7);
    $("#pl8").css("background", response.pl8);
    $("#pl8").css("border-color", response.pl8);
    $("#pl9").css("background", response.pl9);
    $("#pl9").css("border-color", response.pl9);
    $("#pl10").css("background", response.pl10);
    $("#pl10").css("border-color", response.pl10);
    $("#pl11").css("background", response.pl11);
    $("#pl11").css("border-color", response.pl11);
    $("#pl12").css("background", response.pl12);
    $("#pl12").css("border-color", response.pl12);
  });
  // request.fail(function(jqXHR, textStatus)
  // {
  //   alert('Request failed: ' + textStatus);
  // });
}

function send_vote(character, gameID) {
  var request = $.ajax({
    url: "/vote?character=" + character + "&game_id=" + gameID
  });
  document.getElementById("charactera").setAttribute("onClick","");
  document.getElementById("characterb").setAttribute("onClick","");
}
