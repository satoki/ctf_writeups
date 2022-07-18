function hatenaClick(){
    var $count = getCookie( 'nazotoki' );
    if( $count >= 99999999 ){
	alert("nazotokiCTF{ポラリス}");
    }
    if( !$count ){
        setCookie( 'nazotoki', 1, 1 );
    }else{
        setCookie( 'nazotoki', ++$count, 1 );
    }
}

function setCookie( $cookieName, $cookieValue, $days ){
    var $dateObject = new Date();
    var $days = 2; 
    $dateObject.setTime( $dateObject.getTime() + ( $days*24*60*60*1000 ) );
    var $expires = "expires=" + $dateObject.toGMTString();
    document.cookie = $cookieName + "=" + $cookieValue + "; " + $expires + "; domain=.ctf.nazotoki.tech";
}
function getCookie( $cookieName ){
    var $cookies = document.cookie.split(';');
    for( var $i=0; $i < $cookies.length; $i++ ){
        var $cookie = $cookies[$i].trim().split( '=' );
        if( $cookie[0] == $cookieName ){
            return $cookie[1];
        }
    }
    return "";
}

