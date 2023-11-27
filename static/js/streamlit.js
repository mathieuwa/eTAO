var radiogroups = window.parent.document.querySelectorAll('section[data-testid="stSidebar"] div[role="radiogroup"]')
for (let i=0; i < radiogroups.length; i++) {
    rg = radiogroups[i].childNodes;
    if (rg.length == 3) {
        rg[0].classList.add("green-button");
        rg[1].classList.add("orange-button");
        rg[2].classList.add("red-button");
    }
    else if (rg.length == 4) {
        rg[0].classList.add("green-button");
        rg[1].classList.add("yellow-button");
        rg[2].classList.add("orange-button");
        rg[3].classList.add("red-button");
    }
    for (let j=0; j< rg.length; j++) {
        rg[j].classList.add("btn")
    }

}