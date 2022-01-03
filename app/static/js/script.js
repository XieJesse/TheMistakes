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

function setCardBase(cards, lightness) {
    // Adjust the card's base color if the suit color is too light
    if (lightness > 159) {
        for (var i = 0; i < cards.length; i++) {
            cards[i].classList.add("dark");
        }
    } else {
        for (var i = 0; i < cards.length; i++) {
            cards[i].classList.remove("dark");
        }
    }
}


function lightness(channels) {
    // Get the lightness component of an RGB color
    r = channels[0];
    g = channels[1];
    b = channels[2];
    return (Math.max(r,g,b) + Math.min(r,g,b)) / 2.0;
}

function setCardHandlers(radio, cardList, propertyName) {
    // Update the cards when the corresponding form is changed
    for (var i = 0; i < radio.length; i++) {
        radio[i].addEventListener("change", function() {
            document.documentElement.style.setProperty(propertyName, "rgb(" + this.value + ")");
            console.log(this.value)
            var channels = this.value.split(",");
            setCardBase(cardList, lightness(channels));
        });
    }
}