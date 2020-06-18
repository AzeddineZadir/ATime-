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


    const elem = document.getElementById('range');
    Datepicker.active
    Datepicker.locales.fr = {
        days: ["dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"],
        daysShort: ["dim.", "lun.", "mar.", "mer.", "jeu.", "ven.", "sam."],
        daysMin: ["d", "l", "ma", "me", "j", "v", "s"],
        months: ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"],            monthsShort: ["janv.", "févr.", "mars", "avril", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."],
        today: "Aujourd'hui",
        monthsTitle: "Mois",
        clear: "Effacer",
        weekStart: 1,
        format: "dd/mm/yyyy"
    };
    const dateRangePicker = new DateRangePicker(elem, {
        language:'fr',   
    });     
    
});





