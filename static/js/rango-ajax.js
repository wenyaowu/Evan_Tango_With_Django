/**
 * Created by evanwu on 2/6/15.
 */
$(document).ready(function() {
    $('#likes').click(
        function () { //When clicked, call this function
        var catid;
        catid = $(this).attr("data-catid");
        $.get('/rango/like_category/', {category_id: catid}, function (data) {
            $('#like_count').html(data);
            $('#likes').hide();
        });
    }) //end click();

    });

/** Work flow
 * Html page, with some input components(with id), along with some attributes
 *  => when active => ajax.js
 *  => Call function of corresponding id tag (in this case, #like)
 *  => (1) extract needed variables (in this case, var catid)
 *  => make and sen Httprequest(get, post) with some parameters
 *  => call another function which changes the attributes of the Html components
 *  associated with specific tag.
 */
