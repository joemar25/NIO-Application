// ========================================== Record Audio ==========================================

let chunks = [];
let mediaRecorder;
let stream;

function startRecording() {
    chunks = []; // reset chunks array
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function (audioStream) {
            stream = audioStream;
            mediaRecorder = new MediaRecorder(stream, {
                mimeType: 'audio/webm;codecs=opus',
            });
            mediaRecorder.start();

            mediaRecorder.addEventListener("dataavailable", function (event) {
                chunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", function () {
                const audioBlob = new Blob(chunks, { type: chunks[0].type });
                const timestamp = Date.now(); // use timestamp as filename
                const formData = new FormData();
                formData.append("audio", audioBlob, `${timestamp}.wav`);

                fetch("/upload", {
                    method: "POST",
                    body: formData
                })
                    .then(response => {
                        console.log("Audio recording sent to server");
                    })
                    .catch(error => {
                        console.error("Error sending audio recording to server:", error);
                    });
            });

        })
        .catch(function (error) {
            console.error(error);
        });
}

function stopRecording() {
    mediaRecorder.stop();
    stream.getTracks().forEach(track => track.stop());
}

const recordBtn = document.getElementById("record-btn");
if (recordBtn) {
    recordBtn.addEventListener("click", function () {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            stopRecording();
            this.innerText = "Record";
        } else {
            startRecording();
            this.innerText = "Stop";
        }
    });
} else {
    // button is not found in page - no worries, this button is present in recording page/main
    // console.error("record-btn element not found");
}

// ============================================== End ===============================================

