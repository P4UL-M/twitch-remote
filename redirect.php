<?php
    if (isset($_GET['access_token'])) {
        $monfichier = fopen('twitch-bot/.env', 'r+');
        $content = fgets($monfichier);
        $new = "\nUSER_TOKEN = " . $_GET['access_token'] . " \nTOKEN_TYPE = " . $_GET['token_type'];
        fseek($monfichier, 113);
        fputs($monfichier, $new);
        fclose($monfichier);
        header('Location: https://paul.famille-mairesse.fr/Le_Picard_Fr/remote.html');
        exit();
    }
    else{
        echo 'wait ...';
    }
?>
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        <title>redirect</title>
        <script type="text/javascript">
            // data = JSON.parse('{"' + document.location.hash.substr(1).replace(/"/g, '\\"').replace(/&/g, '","').replace(/=/g,'":"') + '"}')
            if (document.location.hash !== '') {
                document.location.href="https://paul.famille-mairesse.fr/Le_Picard_Fr/redirect.php?" + document.location.hash.substr(1)
            }
        </script>
    </head>
</html>