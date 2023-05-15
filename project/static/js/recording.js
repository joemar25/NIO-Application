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
    this.timerIntervalId = null;

    const recordBtn = document.getElementById("record-btn");
    const timerDiv = document.getElementById("timer");
    const countdownDiv = document.getElementById("countdown");
    const notif = document.getElementById("notif");
    const reminder = document.getElementById("reminder");

    recordBtn.addEventListener("click", () => {
      this.toggleState();
    });

    Object.assign(this, {
      recordBtn,
      timerDiv,
      countdownDiv,
      notif,
      reminder,
    });
  }

  toggleState() {
    const { state } = this.recordBtn.dataset;
    if (state === "ready") {
      this.recordBtn.dataset.state = "recording";
      this.reminder.classList.add("hidden");
      this.startCountdown();
      this.notif.textContent = "Prepare in...";
    } else if (state === "recording") {
      this.recordBtn.dataset.state = "ready";
      this.stopRecording();
      this.notif.textContent = "Processing audio...";
    }
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
    this.showRecordingUI();
    this.setUpRecordingTimer();
    try {
      await this.setUpMediaRecorder();
      this.startMediaRecorder();
    } catch (error) {
      console.error(error);
      window.location.href = "/process_audio_fail";
    }
  }

  showRecordingUI() {
    this.recordBtn.classList.remove("hidden");
    this.timerDiv.classList.remove("hidden");
    this.recordBtn.value = "Stop";
    this.recordBtn.disabled = false;
    this.recordBtn.dataset.state = "recording";
    this.notif.textContent = "Tap to stop recording";
  }

  setUpRecordingTimer() {
    this.remainingTime = 0;

    this.timerIntervalId = setInterval(() => {
      this.remainingTime += 1;
      const minutes = Math.floor(this.remainingTime / 60);
      const seconds = this.remainingTime % 60;
      this.timerDiv.textContent = `${minutes
        .toString()
        .padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
    }, 1000);
  }

  async setUpMediaRecorder() {
    this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    this.mediaRecorder = new MediaRecorder(this.stream, {
      mimeType: "audio/webm;codecs=opus",
    });

    this.mediaRecorder.addEventListener("dataavailable", ({ data }) => {
      this.chunks.push(data);
    });

    this.mediaRecorder.addEventListener("stop", async () => {
      await this.handleMediaRecorderStop();
    });
  }

  startMediaRecorder() {
    const recordingTimeLimit = 5 * 60 * 1000;
    this.recordingTimeoutId = setTimeout(() => {
      this.stopRecording();
    }, recordingTimeLimit);
    this.mediaRecorder.start();
  }

  async handleMediaRecorderStop() {
    clearInterval(this.timerIntervalId);
    const audioBlob = new Blob(this.chunks, { type: this.chunks[0].type });
    const timestamp = Date.now();
    const formData = new FormData();
    formData.append("audio", audioBlob, `${timestamp}.wav`);

    const loadingContainer = document.getElementById("loading-container");
    loadingContainer.classList.add("show");

    try {
      const response = await fetch("/upload", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        window.location.href = "/process_audio";
      } else {
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

    // loadingContainer.classList.remove("show");
  }

  stopRecording() {
    clearInterval(this.timerIntervalId);
    clearTimeout(this.recordingTimeoutId);
    this.mediaRecorder.stop();

    this.recordBtn.value = "Ready";
    this.recordBtn.disabled = true;
  }
}

if (window.location.pathname === "/main") {
  const recorder = new Recorder();
}
