// ========================================== Record Audio ==========================================

// variables for recording
let chunks = [];
let mediaRecorder;
let stream;

// use the blueimp-file-upload widget to upload the audio file when recording is complete
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
                formData.append("file", audioBlob, `${timestamp}.wav`);

                // Use the file upload widget to upload the audio file
                $('.fileupload').fileupload('send', { files: formData });

            });

        })
        .catch(function (error) {
            console.error(error);
        });
}


function stopRecording() {
    mediaRecorder.stop();
    stream.getTracks().forEach(track => track.stop());
    window.location.href = '/feedback'; // Redirect to the success page
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

