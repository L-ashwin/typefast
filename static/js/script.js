var sourceTextElement = document.getElementById("sourceText");
var userInputElement = document.getElementById("userInput");
var startTime, newStrokeTime;
var position = 0, newPosition = 0; // till position-1 is already checked & correct
var strokes = [], strokeTimes = []
var incognito = false;
var plot_kind = 'speed'
putImgage();

document.getElementById("userInput").addEventListener("input", function(event) {
    console.log(event);
    var newStrokeTime = new Date();
    strokes.push(event.data);
    strokeTimes.push(newStrokeTime-startTime);
    handleDisplay(newStrokeTime);
});

function handleDisplay(newStrokeTime) {
    var sourceText = sourceTextElement.textContent;
    var userInputLength = userInputElement.value.length;
    position = newPosition;
    
    for (var i = 0; i < userInputLength; i++) {
        if(userInputElement.value[i] != sourceText[position+i]) {
            break; // break if there's a mistake at `position + i`
        }
    } // i will be equal to userInputLength if there's no mistake

    var formattedText = "<span style='color: green;'>" + sourceText.substring(0, position+i) + "</span>";
    var mistakesText = "<span style='color: red; background-color:pink'>" + sourceText.substring(position+i, position+userInputLength) + "</span>";
    sourceTextElement.innerHTML = formattedText + mistakesText + sourceText.substring(position+userInputLength);
    
    // after each word update the speed, clear input field & update where to check from 
    if ((userInputElement.value[userInputLength-1]==' ') && ( i == userInputLength)){
        newPosition = position+userInputLength;
        userInputElement.value = '';
        updateSpeed(newPosition, newStrokeTime);
    }

    // end of text -> shift focus to restart
    if (sourceText.length==position+i) {
        sourceTextElement.innerHTML = sourceText;
        userInputElement.value = '';
        userInputElement.disabled=true;
        document.getElementById('main-container').setAttribute('hidden', true);
        document.getElementById('kde-image').removeAttribute('hidden');
        updateSpeed(sourceText.length, newStrokeTime);
        if (!incognito) {
            save_session_data().then(() => {
                putImgage();
            })                
        }
        
        document.getElementById("reStart").focus();
    }
}

function save_session_data(){
    inputString = sourceTextElement.textContent
    
    var outTimes = []; // time curresponding to correct char typed
    var ptr = inputString.length - 1;
    for (let i = strokes.length - 1; ((i >= 0) & (ptr >=0)); i--) {
        const key = strokes[i];
        const time = strokeTimes[i]
        if (key == inputString[ptr]) {
            outTimes.push(time);
            ptr--;
        }
    }; outTimes.reverse();

    var jsonData = {
        'inputString': inputString,
        'outTimes':outTimes,
        'strokes': strokes,
        'strokeTimes': strokeTimes
    };

    return fetch('/save_data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsonData)
      })
}

function getText() {
    document.getElementById("clickButton").focus();
    fetchAndSetText();
    document.getElementById('kde-image').setAttribute('hidden', true);
    document.getElementById('main-container').removeAttribute('hidden');
}

function fetchAndSetText() {
    fetch('/get_string', {method: 'POST'})
    .then(response => response.text())
    .then(data => {
        sourceTextElement.innerHTML = data;
    })
    .catch(error => console.error('Error:', error));
}

function startTyping(){
    userInputElement.disabled=false;
    userInputElement.focus();

    startTime = new Date();
    position = 0, newPosition = 0;
    strokes = [], strokeTimes = []
}

function updateSpeed(nChars, endTime){
    var wpm = (nChars/5)/((endTime - startTime)/(1000*60));
    document.getElementById("wpm").textContent = Math.round(wpm) + ' WPS';
}

function putImgage() {
    fetch('/get_image?argument='+plot_kind)
        .then(response => response.blob())
        .then(blob => {
            const imageUrl = URL.createObjectURL(blob);
            const imageElement = document.createElement('img');
            imageElement.src = imageUrl;
            var div = document.getElementById('keyboard-image');
            div.innerHTML=''; div.appendChild(imageElement);
        });

    fetch('/get_kde')
        .then(response => response.blob())
        .then(blob => {
            const imageUrl = URL.createObjectURL(blob);
            const imageElement = document.createElement('img');
            imageElement.src = imageUrl;
            var div = document.getElementById('kde-image');
            div.innerHTML=''; div.appendChild(imageElement);
        });
}

document.getElementById('kind-button').addEventListener('click', function() {
    //var image = document.getElementById('keyboard-image');
    //image.style.display = (image.style.display === 'none' || image.style.display === '') ? 'block' : 'none';
    plot_kind = plot_kind === 'count' ? 'speed' : 'count';
    this.textContent = plot_kind === 'count' ? 'Count' : 'Speed';
    putImgage();
});

document.getElementById('clear-button').addEventListener('click', function() {
    const isConfirmed = window.confirm('Are you sure? This will clear the history.');
    if (isConfirmed) {
        fetch('/clear_session', { method: 'GET' }).then(putImgage)
    }
});

document.getElementById('toggleIncognito').addEventListener('change', function() {
    incognito = this.checked;
});