$(document).ready(function (){
    $(".sideMenuToggler").on("click", function(){
        $(".wrapper").toggleClass("active"); 
        icon = $(this).find("i")
        if(icon.hasClass("fa-chevron-circle-left")){
            icon.removeClass("fa-chevron-circle-left").toggleClass("fa-chevron-circle-right");
        }else{
            icon.removeClass("fa-chevron-circle-right").toggleClass("fa-chevron-circle-left");
        }
    });

   
});


