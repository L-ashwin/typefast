var sourceTextElement = document.getElementById("sourceText");
var userInputElement = document.getElementById("userInput");
var startTime, newStrokeTime;
var position = 0, newPosition = 0; // till position-1 is already checked & correct
strokes = [], strokeTimes = []


document.getElementById("userInput").addEventListener("keyup", function(event) {
    var newStrokeTime = new Date();
    strokes.push(event.key);
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
        updateSpeed(sourceText.length, newStrokeTime);
        userInputElement.disabled=true;
        document.getElementById("reStart").focus();
        console.log(strokes, strokeTimes);

        var jsonData = {
            'inputString': sourceTextElement.textContent,
            'strokes': strokes,
            'strokeTimes': strokeTimes
        };
    
        fetch('/save_data', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonData)
          })

    }
}

function refreshPage() {
    userInputElement.value = '';
    document.getElementById("clickButton").focus();
    
    fetch('/get_string', {method: 'POST'})
        .then(response => response.text())
        .then(data => {
            sourceTextElement.innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
}

function startTyping(){
    userInputElement.disabled=false;
    
    startTime = new Date();
    position = 0, newPosition = 0;
    strokes = [], strokeTimes = []
    
    userInputElement.focus();
    
}

function updateSpeed(nChars, endTime){
    var wpm = (nChars/5)/((endTime - startTime)/(1000*60));
    document.getElementById("wpm").textContent = Math.round(wpm) + ' WPS';
}