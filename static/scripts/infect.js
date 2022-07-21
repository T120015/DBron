const infect = document.getElementsByName("infect");
const hospital = document.getElementById("hospital");

function radio() {
    if (infect[0].checked){
        hospital.innerHTML = "診断病院";
        let inp = document.createElement('input');
        inp.setAttribute('type',"text");
        inp.setAttribute('name', "hospital");
        hospital.appendChild(inp);
    }else{
        hospital.innerHTML = "";        
    }
}

window.onload = function(){
    radio();
}