if (typeof window.WebAssembly === 'undefined') {
    alert('WebAssembly seems to not be implemented on your browser. Try using an updated version of Firefox, Chrome, or Safari. ');
    throw 'no wasm :(';
}

let wasm = null;
fetch("./code.wasm").then(res => res.arrayBuffer()).then(buffer => WebAssembly.instantiate(buffer)).then(res => {
    wasm = res;
}).catch(err => {
    console.warn('If you\'re seeing this logged, something broke');
    throw err;
})



const input = document.querySelector('input');
const response = document.querySelector('p#response-text');

document.querySelector('button').addEventListener('click', () => {
    if (wasm) {
        const memory = new Uint8Array(wasm.instance.exports.memory.buffer);
        memory.set(new TextEncoder().encode(input.value + "\x00"));

        const responseText = wasm.instance.exports.checkFlag(0) ? "Correct flag" : "Incorrect flag";

        response.innerText = responseText;
    } else {
        response.innerText = "Please try again in a few seconds";
    }
}, 1);
