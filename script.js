$(function () {
    $("#UID_boutonTest").click(function () {
        $.getJSON('/_get_message', {
            param: $("#UID_boutonTest").text()
        }, function (data) {
            $("#UID_afficheTest").text(data.result);
        });
        return false;
    });
});