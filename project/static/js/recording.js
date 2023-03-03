// ========================================== Record Audio ==========================================

let chunks = [];
let mediaRecorder;
let stream;

const startRecording = async () => {
    // reset chunks array
    chunks = [];

    try {
        // get user media
        stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        // create media recorder
        mediaRecorder = new MediaRecorder(stream, {
            mimeType: "audio/webm;codecs=opus",
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

            // show loading element
            const loading = document.getElementById("loading");
            loading.style.display = "block";

            try {
                // send audio to server
                const response = await fetch("/upload", {
                    method: "POST",
                    body: formData,
                });

                const { ok, statusText } = response;

                if (ok) {
                    // the upload was successful, so redirect to the success page
                    window.location.href = "/process_audio";
                } else {
                    // the upload failed, so show an error message
                    console.error("Error sending audio recording to server:", statusText);
                    window.location.href = "/process_audio_fail";
                }
            } catch (error) {
                console.error("Error sending audio recording to server:", error);
                window.location.href = "/process_audio_fail";
            }

            loading.style.display = "none";
        });

        // start recording
        mediaRecorder.start();
    } catch (error) {
        console.error(error);
        window.location.href = "/process_audio_fail";
    }
};

const stopRecording = () => {
    mediaRecorder.stop();
    stream.getTracks().forEach((track) => track.stop());

    const loading = document.getElementById("loading");
    loading.style.display = "none";

    const recordBtn = document.getElementById("record-btn");
    recordBtn.style.display = "none";
};

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
