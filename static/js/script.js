function randomText() {
    var text = "❏❐❑❒❍∆∇⎔";
    return text[Math.floor(Math.random() * text.length)];
}
function randomColor() {
    var colors = ["#757575", "#484848", "#1a1a1a"];
    return colors[Math.floor(Math.random() * colors.length)];
}

function createDrop() {
    let rainContainer = document.querySelector('.rain-container');
    let hr = document.querySelector('.separator');
    let hrBounds = hr.getBoundingClientRect();

    hrBounds.width = hrBounds.width - 15;

    let drop = document.createElement('div');
    drop.classList.add('drop');
    rainContainer.appendChild(drop);

    let left = Math.random() * hrBounds.width;
    let size = Math.random() * 1.5 + 0.5;
    let duration = Math.random() * 1.5 + 1.5;

    drop.innerText = randomText();
    drop.style.left = left + 'px';
    drop.style.fontSize = size + 'em';
    drop.style.animationDuration = duration + 's';
    drop.style.color = randomColor();
    drop.style.opacity = Math.random() * 0.7 + 0.3;

    setTimeout(() => {
        drop.remove();
    }, duration * 1000);
}

function rain() {
    let dropsPerCycle = 10;
    for (let i = 0; i < dropsPerCycle; i++) {
        createDrop();
    }
}

setInterval(rain, 50);