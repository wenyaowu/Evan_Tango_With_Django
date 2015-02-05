/**
 * Created by evanwu on 2/4/15.
 */
$(document).ready(function(){


    $("#").click( function(event){
        alert("You click the button");
    });
    // Jquery code to be added in here

    $("about-btn").addClass('btn btn-primary')

    $("#about-btn").click( function(event){
       msgstr = $("#msg").html()
        msgstr = msgstr + "o"
        $("#msg").html(msgstr)
    });
});