// ========================================== Record Audio ==========================================

let chunks = [];
let mediaRecorder;
let stream;

async function startRecording() {
    // reset chunks array
    chunks = [];

    try {
        // get user media
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        // create media recorder
        mediaRecorder = new MediaRecorder(stream, {
            mimeType: 'audio/webm;codecs=opus',
        });

        // handle data and stop events
        mediaRecorder.addEventListener("dataavailable", function (event) {
            chunks.push(event.data);
        });

        mediaRecorder.addEventListener("stop", async function () {
            // create audio blob and form data
            const audioBlob = new Blob(chunks, { type: chunks[0].type });
            const timestamp = Date.now();
            const formData = new FormData();
            formData.append("audio", audioBlob, `${timestamp}.wav`);

            // show loading animation
            const loadingContainer = document.getElementById("loading-container");
            loadingContainer.classList.add("show");

            try {
                // send audio to server
                const response = await fetch("/upload", {
                    method: "POST",
                    body: formData
                });

                if (response.ok) {
                    // the upload was successful, so redirect to the success page
                    window.location.href = '/process_audio';
                } else {
                    // the upload failed, so show an error message
                    console.error("Error sending audio recording to server:", response.statusText);
                    window.location.href = '/process_audio_fail';
                }
            } catch (error) {
                console.error("Error sending audio recording to server:", error);
                window.location.href = '/process_audio_fail';
            }

            // hide loading animation
            loadingContainer.classList.remove("show");
        });

        // start recording
        mediaRecorder.start();
    } catch (error) {
        console.error(error);
        window.location.href = '/process_audio_fail';
    }
}

function stopRecording() {
    mediaRecorder.stop();
    stream.getTracks().forEach(track => track.stop());

    const loadingContainer = document.getElementById("loading-container");
    loadingContainer.classList.remove("show");

    const record_btn = document.getElementById("record-btn");
    record_btn.style.display = "none";
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
        }
    });
}

// ============================================== End ===============================================
