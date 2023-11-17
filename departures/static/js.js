
window.onload = function () {
    document.querySelector("#btn-stations").addEventListener("click", () => {
        window.location.href = 'stations';
    })
    document.querySelector("#btn-reload-stations").addEventListener("click", () => {
        window.location.href = 'deletestations';
    })
}