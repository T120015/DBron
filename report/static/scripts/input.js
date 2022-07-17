window.onload = function (params) {

    //リスト1
    const posi = document.getElementById("posi");

    for (let i = 0; i < 3; i++) {
        let op = document.createElement("option");
        op.setAttribute('value', posi_list[i]);
        op.innerHTML = posi_list[i];
        posi.appendChild(op);
    }

    //リスト2
    const cls = document.getElementById("cls");
    for (let i = 0; i < 3; i++) {
        let op = document.createElement("option");
        op.setAttribute('value', cls_list[i]);
        op.innerHTML = cls_list[i];
        cls.appendChild(op);
    }

    posi.addEventListener('change',
        function () {
            cls.innerHTML = "";
            for (let i = 0; i < 3; i++) {
                let op = document.createElement("option");
                if (this.value == posi_list[0]) {
                    op.setAttribute('value', cls_list[i]);
                    op.innerHTML = cls_list[i];
                    cls.appendChild(op);
                } else if (this.value == posi_list[1]) {
                    op.setAttribute('value', cls_list[i + 3])
                    op.innerHTML = cls_list[i + 3];
                    cls.appendChild(op);
                } else {
                    op.setAttribute('value', cls_list[i + 6])
                    op.innerHTML = cls_list[i + 6];
                    cls.appendChild(op);
                }
            }
        },
        false)
}