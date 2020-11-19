<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>Test CLEM clem</title>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
        <script type="text/javascript">
        $(function() {
            $("#UID_boutonTest").click(function()
            {
                $.getJSON(url ='/_get_message', {
                    param: $("#UID_boutonTest").text()
                        }, function(data) {
                        $("#afficheTest").text(data.result);
                });
                return false;
            });
        });
        </script>
    </head>
    <body>
        <button id="UID_boutonTest" style='left:50px;height:50px;width:200px;'>clickServeur</button>
        <span id="afficheTest"style='text-align: center;'>MESSAGEDUSERVEUR</span>
    </body>
</html>