window.onload = function (params) {
    //リスト1
    const Y = document.getElementById("rtn.Y");

    for (let i = 0; i <= 71; i++) {
        let op = document.createElement("option");
        op.setAttribute('value', 1949 + i);
        if (i == 0) {
            op.innerHTML = "";
        } else {
            op.innerHTML = i + 1949;
        }
        Y.appendChild(op);
    }

    //リスト2
    const M = document.getElementById("rtn.M");

    Y.addEventListener('change',
        function () {
            M.innerHTML = "";
            if (this.value != 1949) {
                for (let i = 0; i <= 12; i++) {
                    let op = document.createElement("option");

                    op.setAttribute('value', i);
                    if (i == 0) {
                        op.innerHTML = "";
                    } else {
                        op.innerHTML = i;
                    }
                    M.appendChild(op);
                }
            }
        },
        false)
}