import { formatTime } from "./config.js";

export class AudioPlayer {
  constructor({ audioElement, tracks, elements, autoPlay = false }) {
    this.audio = audioElement;
    this.tracks = tracks;
    this.elements = elements;
    this.autoPlay = autoPlay;
    this.currentTrackIndex = 0;
    this.isSeeking = false;

    this.bindEvents();
    this.loadTrack(this.currentTrackIndex, { autoplay: autoPlay });
  }

  bindEvents() {
    this.elements.playPauseBtn.addEventListener("click", () => this.togglePlayback());
    this.elements.prevBtn?.addEventListener("click", () => this.previousTrack());
    this.elements.nextBtn?.addEventListener("click", () => this.nextTrack());
    this.elements.progressBar.addEventListener("input", () => this.onSeekInput());
    this.elements.progressBar.addEventListener("change", () => this.onSeekCommit());

    this.audio.addEventListener("loadedmetadata", () => this.updateDuration());
    this.audio.addEventListener("timeupdate", () => this.updateProgress());
    this.audio.addEventListener("play", () => this.updatePlayButton(true));
    this.audio.addEventListener("pause", () => this.updatePlayButton(false));
  }

  loadTrack(index, { autoplay = false } = {}) {
    const track = this.tracks[index];
    if (!track) {
      return;
    }

    this.currentTrackIndex = index;
    this.audio.src = track.src;
    this.audio.load();
    this.elements.trackTitle.textContent = track.title;
    this.resetProgress();

    if (autoplay) {
      this.play().catch(() => {
        /* Autoplay may be blocked until user interaction. */
      });
    }
  }

  selectTrack(index, { autoplay = false } = {}) {
    if (index === this.currentTrackIndex && this.audio.src) {
      if (autoplay) {
        this.play().catch(() => {});
      }
      return;
    }

    this.loadTrack(index, { autoplay });
  }

  selectTrackById(trackId, { autoplay = false } = {}) {
    const index = this.tracks.findIndex((track) => track.id === trackId);
    if (index === -1) {
      return false;
    }

    this.selectTrack(index, { autoplay });
    return true;
  }

  previousTrack() {
    const previousIndex =
      this.currentTrackIndex > 0
        ? this.currentTrackIndex - 1
        : this.tracks.length - 1;
    this.selectTrack(previousIndex, { autoplay: !this.audio.paused });
  }

  nextTrack() {
    const nextIndex =
      this.currentTrackIndex < this.tracks.length - 1
        ? this.currentTrackIndex + 1
        : 0;
    this.selectTrack(nextIndex, { autoplay: !this.audio.paused });
  }

  async togglePlayback() {
    if (this.audio.paused) {
      await this.play();
    } else {
      this.pause();
    }
  }

  async play() {
    await this.audio.play();
  }

  pause() {
    this.audio.pause();
  }

  onSeekInput() {
    this.isSeeking = true;
    const duration = this.audio.duration || 0;
    const nextTime = (Number(this.elements.progressBar.value) / 100) * duration;
    this.elements.currentTime.textContent = formatTime(nextTime);
  }

  onSeekCommit() {
    const duration = this.audio.duration || 0;
    const nextTime = (Number(this.elements.progressBar.value) / 100) * duration;
    this.audio.currentTime = nextTime;
    this.isSeeking = false;
  }

  updateProgress() {
    if (this.isSeeking) {
      return;
    }

    const duration = this.audio.duration || 0;
    const currentTime = this.audio.currentTime || 0;
    const progress = duration > 0 ? (currentTime / duration) * 100 : 0;

    this.elements.progressBar.value = String(progress);
    this.elements.currentTime.textContent = formatTime(currentTime);
  }

  updateDuration() {
    this.elements.duration.textContent = formatTime(this.audio.duration || 0);
  }

  resetProgress() {
    this.elements.progressBar.value = "0";
    this.elements.currentTime.textContent = "0:00";
    this.elements.duration.textContent = "0:00";
  }

  updatePlayButton(isPlaying) {
    this.elements.playIcon.classList.toggle("hidden", isPlaying);
    this.elements.pauseIcon.classList.toggle("hidden", !isPlaying);
    this.elements.playPauseBtn.setAttribute(
      "aria-label",
      isPlaying ? "Szünet" : "Lejátszás",
    );
  }

}
