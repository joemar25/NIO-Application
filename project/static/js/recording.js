// ========================================== Record Audio ==========================================

let chunks = [];
let mediaRecorder;
let stream;

function startRecording() {
    // reset chunks array
    chunks = [];

    // get user media
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(function (audioStream) {
            // create media recorder
            stream = audioStream;
            mediaRecorder = new MediaRecorder(stream, {
                mimeType: 'audio/webm;codecs=opus',
            });

            // start recording
            mediaRecorder.start();

            // handle data and stop events
            mediaRecorder.addEventListener("dataavailable", function (event) {
                chunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", function () {
                // create audio blob and form data
                const audioBlob = new Blob(chunks, { type: chunks[0].type });
                const timestamp = Date.now();
                const formData = new FormData();
                formData.append("audio", audioBlob, `${timestamp}.wav`);

                // show loading element
                const loading = document.getElementById("loading");
                loading.style.display = "block";

                // send audio to server
                fetch("/upload", {
                    method: "POST",
                    body: formData
                })
                    .then(response => {
                        if (response.ok) {
                            // the upload was successful, so redirect to the success page
                            window.location.href = '/process_audio';
                        } else {
                            // the upload failed, so show an error message
                            console.error("Error sending audio recording to server:", response.statusText);
                        }
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
    // hide loading element
    const loading = document.getElementById("loading");
    loading.style.display = "none";
    // redirect to success page
    // window.location.href = '/process_audio';
}

const recordBtn = document.getElementById("record-btn");
if (recordBtn) {
    recordBtn.addEventListener("click", function () {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            stopRecording();
            this.value = "Record";
        } else {
            startRecording();
            this.value = "Stop";
            // this.classList.replace('ready', 'recording');
        }
    });
} else {
    // button is not found in page - no worries, this button is present in recording page/main
    // console.error("record-btn element not found");
}

// ============================================== End ===============================================
