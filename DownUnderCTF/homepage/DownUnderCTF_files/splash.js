(function() {
    const END = new Date("2020-09-20T19:00:00.000+10:00");
    const dispMain = document.getElementById("countdown");

    const disp = {
        ending: dispMain.querySelector("#ending"),
        hour: dispMain.querySelector("#countdown>.hour"),
        minute: dispMain.querySelector("#countdown>.minute"),
        second: dispMain.querySelector("#countdown>.second"),
    }
    let timeout = 0;

    function countdown() {
        const diff = Math.floor((END - new Date()) / 1000);
        if (diff < 0) {
            ending.parentNode.removeChild(ending);
            dispMain.innerHTML = "<h3>thanks for playing</h3>";
            return;
        }

        disp.hour.textContent = (Math.floor(diff / 3600)).toString().padStart(2, "0");
        disp.minute.textContent = (Math.floor(diff / 60) % 60).toString().padStart(2, "0");
        disp.second.textContent = (diff % 60).toString().padStart(2, "0");
        setTimeout(countdown, 1000);
    }
    countdown();
})();
(function () {
    function randomColor() {
        var letters = "0123456789ABCDEF";
        var color = "#";
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(6 + Math.random() * 10)];
        }
        return color;
      }

    function reset(elem) {
        return function() {
            elem.style.fill = "";
        }
    }
    const lol = "00101000000010000010111101100001101001011101000101101110100001100011111101101010" +
        "1010001111000111101000110010000001000000010010001000011111011101001111101001110111101010" +
        "0110011110010111100011011110001010000010001100110110000101011001110101010001011101001001" +
        "0110000011011110001010110011001011111001110010011101100011110000110111111001000011010101" +
        "0100000000101000111110101000111001111100111000010001000100110";


    document.querySelectorAll("#logo circle").forEach(function (c, k) {
        c.addEventListener("mouseover", function (e) {
            e.target.style.fill = lol[k] === "0" ? "#005248" : "#C3FCF1";
        })
    });
})();
