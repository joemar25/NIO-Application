/*
 * This is a JavaScript class that defines a simple audio recorder. The recorder
 * allows users to record audio from their device's microphone and upload it to
 * a server for further processing. The recorder interface displays a timer that
 * shows the elapsed time during recording, a countdown before recording starts,
 * and a button to start and stop the recording.
 *
 * The class uses the Web Audio API and the MediaRecorder API to capture and
 * record audio data, and the fetch() function to upload the recorded audio to
 * a server. The recorder also includes error handling for cases where the user
 * denies access to the microphone or the server returns an error response.
 *
 * This code was written for educational purposes only and should not be used in
 * production environments without proper testing and security considerations.
 */

class Recorder {
  constructor() {
    this.mediaRecorder = null;
    this.stream = null;
    this.chunks = [];
    this.remainingTime = 0;
    this.countdownIntervalId = null;
    this.recordingIntervalId = null;

    const recordBtn = document.getElementById("record-btn");
    // const cancelBtn = document.getElementById("cancel-btn");
    const timerDiv = document.getElementById("timer");
    const countdownDiv = document.getElementById("countdown");

    recordBtn.addEventListener("click", () => {
      const { state } = recordBtn.dataset;
      if (state === "ready") {
        this.startCountdown();
      } else if (state === "recording") {
        this.stopRecording();
        recordBtn.value = "Ready";
        recordBtn.disabled = true;
      }
    });

    // cancelBtn.addEventListener("click", () => {
    //   this.cancelRecording();
    //   recordBtn.value = "Ready";
    // });

    Object.assign(this, {
      recordBtn,
      // cancelBtn,
      timerDiv,
      countdownDiv,
    });
  }

  startCountdown() {
    this.recordBtn.disabled = true;
    this.recordBtn.classList.add("hidden");

    const countDown = (count) => {
      if (count > 0) {
        this.countdownDiv.textContent = count;
        setTimeout(() => countDown(count - 1), 1000);
      } else {
        this.countdownDiv.classList.add("hidden");
        this.startRecording();
      }
    };

    this.countdownDiv.classList.remove("hidden");
    countDown(3);
  }

  async startRecording() {
    // Remove the countdown and show recording UI elements
    this.showRecordingUI();

    // Set up the recording timer and interval
    this.setUpRecordingTimer();

    try {
      // Get user media and create media recorder
      await this.setUpMediaRecorder();

      // Start the media recorder
      this.startMediaRecorder();
    } catch (error) {
      console.error(error);
      window.location.href = "/process_audio_fail";
    }
  }

  showRecordingUI() {
    this.recordBtn.classList.remove("hidden");
    this.countdownDiv.classList.add("hidden");
    this.timerDiv.classList.remove("hidden");
    this.recordBtn.value = "Stop";
    this.recordBtn.disabled = false;
    this.recordBtn.dataset.state = "recording";
    // this.cancelBtn.style.display = "inline-block";
  }

  setUpRecordingTimer() {
    this.remainingTime = 0;

    this.recordingIntervalId = setInterval(() => {
      this.remainingTime += 1;
      const minutes = Math.floor(this.remainingTime / 60);
      const seconds = this.remainingTime % 60;
      this.timerDiv.textContent = `${minutes
        .toString()
        .padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
    }, 1000);
  }

  async setUpMediaRecorder() {
    // Get user media
    this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    // Create media recorder
    this.mediaRecorder = new MediaRecorder(this.stream, {
      mimeType: "audio/webm;codecs=opus",
    });

    // Handle data and stop events
    this.mediaRecorder.addEventListener("dataavailable", ({ data }) => {
      this.chunks.push(data);
    });

    this.mediaRecorder.addEventListener("stop", async () => {
      await this.handleMediaRecorderStop();
    });
  }

  startMediaRecorder() {
    // Set recording time limit
    const recordingTimeLimit = 5 * 60 * 1000; // 5 minutes in milliseconds
    setTimeout(() => {
      this.stopMediaRecorder();
    }, recordingTimeLimit);

    // Start the media recorder
    this.mediaRecorder.start();
  }

  async handleMediaRecorderStop() {
    // Clear recording timer
    clearInterval(this.recordingIntervalId);
    // Create audio blob and form data
    const audioBlob = new Blob(this.chunks, { type: this.chunks[0].type });
    const timestamp = Date.now();
    const formData = new FormData();
    formData.append("audio", audioBlob, `${timestamp}.wav`);

    // Show loading animation
    const loadingContainer = document.getElementById("loading-container");
    loadingContainer.classList.add("show");

    try {
      // Send audio to server
      const response = await fetch("/upload", {
        method: "POST",
        body: formData,
      });

      // Handle response
      if (response.ok) {
        // Redirect to success page
        window.location.href = "/process_audio";
      } else {
        // Show error message
        console.error(
          "Error sending audio recording to server:",
          response.statusText
        );
        window.location.href = "/process_audio_fail";
      }
    } catch (error) {
      console.error("Error sending audio recording to server:", error);
      window.location.href = "/process_audio_fail";
    }

    // Hide loading animation
    loadingContainer.classList.remove("show");
  }

  stopMediaRecorder() {
    this.mediaRecorder.stop();
  }

  stopRecording(callback) {
    clearInterval(this.recordingIntervalId);
    clearInterval(this.timerIntervalId);
    clearTimeout(this.recordingTimeoutId);
    this.mediaRecorder.stop();
    if (callback) {
      callback();
    }
  }

  // cancelRecording() {
  //   clearInterval(this.recordingIntervalId);
  //   clearTimeout(this.recordingTimeoutId);
  //   this.stopMediaRecorder();
  //   this.chunks = [];
  //   this.recordBtn.value = "Ready";
  //   this.recordBtn.dataset.state = "ready";
  //   this.countdownDiv.classList.add("hidden");
  //   this.timerDiv.classList.add("hidden");
  //   this.cancelBtn.style.display = "none";
  // }
}

if (window.location.pathname === "/main") {
  const recorder = new Recorder();
}
