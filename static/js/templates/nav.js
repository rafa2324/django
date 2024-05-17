document.getElementById('nav_icon').addEventListener('click', function() {
    // si menu : header__usernav está visible => ocultarlo
    if ( document.getElementById("header_usernav").classList.contains("header__usernav__show") )
        document.getElementById("header_usernav").classList.toggle("header__usernav__show");        

    document.getElementById("nav").classList.toggle("nav__show");
})

document.getElementById('user_icon').addEventListener('click', function() {
    // si menu principal : nav está visible => ocultarlo
    if ( document.getElementById("nav").classList.contains("nav__show") )
        document.getElementById("nav").classList.toggle("nav__show");        

    document.getElementById("header_usernav").classList.toggle("header__usernav__show");
})

