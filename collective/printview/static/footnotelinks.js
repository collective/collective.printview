// Code based on http://blog.vicompany.nl/printing-links-better-with-jquery
// written by Kayren van Heems. It is modified by including it withing 
// $(document).ready(... ) call and by switching thisLink = $(this).attr("href")
// to this.href. Latter change makes script collect absolute paths insted of
// relative ones.
// - Jukka Ojaniemi

$(document).ready(function() {
    // only append list if there are any links
    if($(".content" + " a").length != 0){
        $("#links").css('display', 'block');
    }

    var myArr = []; // to store all the links
    var thisLink;   // to store each link individually
    var num = 1; // to keep count

    // loop trough all the links inside content
    $(".content" + " a").each(function(){
        thisLink = this.href;
        // if current link is not already in the list, add current link to the list
        if($.inArray(thisLink, myArr) == -1){
            $(this).after("<sup class='printOnly'>" + num + "</sup>");
            $("ol#printlinks").append("<li>" + thisLink + "</li>");
            myArr.push(thisLink);
            num++;
        }else{
            $(this).after("<sup class='printOnly'>" + parseInt($.inArray(thisLink, myArr) + 1) + "</sup>");
        }
    });
});
