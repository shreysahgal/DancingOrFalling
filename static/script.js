var count = 4;
var redirect = "/wrong";

function countDown(){
    var timer = document.getElementById("timer");
    if(count > 1){
        count--;
        timer.innerHTML = count;
        // timer.innerHTML = "<button type=\"button\" class=\"btn btn-primary\">" + count + "</button>";
        setTimeout("countDown()", 1000);
    }else{
        window.location.href = redirect;
    }
}