var startTime;
var sourceTextElement = document.getElementById("sourceText");
var userInputElement = document.getElementById("userInput");

var position = 0, newPosition = 0; // till position-1 is already checked & correct
document.getElementById("userInput").addEventListener("keyup", function(event) {
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
        updateSpeed(newPosition);
    }

    // end
    if (sourceText.length==position+i) {
        updateSpeed(sourceText.length);
        console.log('end!');
        document.getElementById("reStart").focus();
    }
});

function refreshPage() {
    userInputElement.value = '';
    document.getElementById("clickButton").focus();
    position = 0, newPosition = 0;
    
    fetch('/get_string', {method: 'POST'})
        .then(response => response.text())
        .then(data => {
            sourceTextElement.innerHTML = data;
        })
        .catch(error => console.error('Error:', error));
}

function startTyping(){
    document.getElementById("userInput").focus();
    startTime = new Date();
}

function updateSpeed(nChars){
    var endTime = new Date();
    var wpm = (nChars/5)/((endTime - startTime)/(1000*60));
    document.getElementById("wpm").textContent = Math.round(wpm) + ' WPS';
}