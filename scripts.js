var startTime;
var sourceTextElement = document.getElementById("sourceText");
const sourceText = sourceTextElement.textContent;

var position = 0, newPosition = 0; // till position-1 is already checked & correct
document.getElementById("userInput").addEventListener("keyup", function(event) {
    var userInputElement = document.getElementById("userInput");
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
    console.log('reload')
    location.reload();
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