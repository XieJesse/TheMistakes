document.addEventListener("DOMContentLoaded", function(event) {
    // On DOM loaded do this

    // Get the radio inputs
    var mainRadio = document.setup.mainColor;
    var altRadio = document.setup.altColor;

    // Get list of cards 
    var mainCards = document.getElementsByClassName("main-color");
    var altCards = document.getElementsByClassName("alt-color");

    setCardHandlers(mainRadio, mainCards, "--suit-main");
    setCardHandlers(altRadio, altCards, "--suit-alt");
});

function setCardHandlers(radio, propertyName) {
    // Update the cards when the corresponding form is changed
    for (var i = 0; i < radio.length; i++) {
        radio[i].addEventListener("change", function() {
            document.documentElement.style.setProperty(propertyName, "rgb(" + this.value + ")");
        });
    }
}