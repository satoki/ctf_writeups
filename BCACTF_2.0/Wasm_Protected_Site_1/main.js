if (typeof window.WebAssembly === 'undefined') {
    alert('WebAssembly seems to not be implemented on your browser. Try using an updated version of Firefox, Chrome, or Safari. ');
    throw 'no wasm :(';
}

const fetchWASMCode = () => {
    return new Promise((res, rej) => {
        const req = new XMLHttpRequest();

        req.onload = function () {
            res(req.response);
        }
        req.onerror = (err) => {
            console.warn('If you\'re seeing this logged, something broke');
            rej(err)
        }
        req.open("GET", "./code.wasm");
        req.responseType = "arraybuffer";
        req.send();
    });
};

let wasm = null;
fetchWASMCode().then(buffer => {
    WebAssembly.instantiate(buffer).then(res => {
        wasm = res;
    }).catch(err => {
        console.warn('If you\'re seeing this logged, something broke');
        throw err;
    })
});


const input = document.querySelector('input#password');
const response = document.querySelector('p#response-text');

document.querySelector('button').addEventListener('click', () => {
    if (wasm) {
        const memory = new Uint8Array(wasm.instance.exports.memory.buffer);
        memory.set(new TextEncoder().encode(input.value + "\x00"));

        const resultAddr = wasm.instance.exports.checkPassword(0);

        const end = memory.indexOf(0, resultAddr);

        response.innerText = "Response: " + new TextDecoder().decode(memory.subarray(resultAddr, end));
    } else {
        response.innerText = "Please try again in a few seconds";
    }
}, 1);
