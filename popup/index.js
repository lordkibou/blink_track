const startButton = document.getElementById("start-tracking-button")
const stopButton = document.getElementById("stop-tracking-button")

//------------------------------- Start Button ---------------------------------
startButton.addEventListener("click", async function () {
    const classState = startButton.className == "can-active"
    if (classState) {
        try {
            const data = await startRecording();
        }
        catch (e) { 
            console.log("Error: ", e)
            //Here we can handle the error
        }

        //Toggle buttons classes
        startButton.className = "cant-active"
        stopButton.className = "can-stop"
    }
    else {
        //Show that it is already working
    }
})


//------------------------------- Stop Button ---------------------------------
stopButton.addEventListener("click", async function () {
    const classState = stopButton.className == "can-stop"
    if (classState) {
        mediaRecorder.stop() //Stop recording using media object

        //Toggle buttons classes
        startButton.className = "can-active"
        stopButton.className = "cant-stop"
    }
    else {
        //Show that it is already stopped
    }
})
//Do not use document write or document.innerHTML use innerText instead, more secure