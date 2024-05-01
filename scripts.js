var startTime;
var sourceTextElement = document.getElementById("sourceText");
const sourceText = sourceTextElement.textContent;

function refreshPage() {
    console.log('reload')
    location.reload();
}

function startTyping(){
    document.getElementById("userInput").focus();
    startTime = new Date();
}

var position = 0, newPosition = 0; // till position-1 is already checked & correct
document.getElementById("userInput").addEventListener("keyup", function(event) {
    var userInputElement = document.getElementById("userInput");
    var userInput = userInputElement.value;
    var userInputLength = userInput.length;
    position = newPosition;
    
    for (var i = 0; i < userInputLength; i++) {
        if(userInput[i] != sourceText[position+i]) {
            break; //mistake at position + i 
        }
    } // i will be userInputLength if there's no mistake

    var formattedText = "<span style='color: green;'>" + sourceText.substring(0, position+i) + "</span>";
    var mistakesText = "<span style='color: red; background-color:pink'>" + sourceText.substring(position+i, position+userInputLength) + "</span>";
    var remainingText = sourceText.substring(position+userInputLength, sourceText.length) // remaining text
    sourceTextElement.innerHTML = formattedText + mistakesText + remainingText;
    
    // after each word
    if ((userInput[userInputLength-1]==' ') && ( i == userInputLength)){
        newPosition = position+userInputLength;
        userInputElement.value = '';

        var endTime = new Date();
        var wpm = (newPosition/5)/((endTime - startTime)/(1000*60));
        document.getElementById("wpm").textContent = Math.round(wpm);
    }

    // end
    if (sourceText.length==position+i) {
        var endTime = new Date();
        var wpm = (sourceText.length/5)/((endTime - startTime)/(1000*60));
        document.getElementById("wpm").textContent = Math.round(wpm);

        console.log('end!');
        document.getElementById("reStart").focus();
    }
});
