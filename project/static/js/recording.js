let mediaRecorder, stream, chunks = [];

async function startRecording() {
    try {
        // get user media
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        // create media recorder
        mediaRecorder = new MediaRecorder(stream, {
            mimeType: 'audio/webm;codecs=opus',
        });

        // handle data and stop events
        mediaRecorder.addEventListener("dataavailable", ({ data }) => {
            chunks.push(data);
        });

        mediaRecorder.addEventListener("stop", async () => {
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

                // handle response
                if (response.ok) {
                    // redirect to success page
                    window.location.href = '/process_audio';
                } else {
                    // show error message
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

    const recordBtn = document.getElementById("record-btn");
    recordBtn.textContent = "Record";
}

const recordBtn = document.getElementById("record-btn");
if (recordBtn) {
    recordBtn.addEventListener("click", function () {
        if (mediaRecorder && mediaRecorder.state === "recording") {
            stopRecording();
        } else {
            startRecording();
            this.textContent = "Stop";
        }
    });
}