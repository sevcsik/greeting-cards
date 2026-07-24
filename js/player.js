export class AudioPlayer {
  constructor({ audioElement, tracks, elements, autoPlay = false }) {
    this.audio = audioElement;
    this.tracks = tracks;
    this.elements = elements;
    this.autoPlay = autoPlay;
    this.currentTrackIndex = 0;
    this.hasEnded = false;

    this.bindEvents();
    this.loadTrack(this.currentTrackIndex, { autoplay: autoPlay });
    this.updateTransportButton(false);
  }

  bindEvents() {
    this.elements.playPauseBtn.addEventListener("click", () => this.togglePlayback());
    this.audio.addEventListener("ended", () => this.onTrackEnded());
    this.audio.addEventListener("play", () => {
      this.hasEnded = false;
      this.updateTransportButton(true);
    });
    this.audio.addEventListener("pause", () => this.updateTransportButton(false));
  }

  loadTrack(index, { autoplay = false } = {}) {
    const track = this.tracks[index];
    if (!track) {
      return;
    }

    this.currentTrackIndex = index;
    this.audio.src = track.src;
    this.audio.load();
    this.hasEnded = false;

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

  async togglePlayback() {
    if (this.hasEnded || this.audio.ended) {
      this.audio.currentTime = 0;
      this.hasEnded = false;
      await this.play();
      return;
    }

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

  onTrackEnded() {
    this.hasEnded = true;
    this.updateTransportButton(false);
  }

  updateTransportButton(isPlaying) {
    const showReplay = !isPlaying && (this.hasEnded || this.audio.ended);

    this.elements.playIcon.classList.toggle("hidden", isPlaying || showReplay);
    this.elements.pauseIcon.classList.toggle("hidden", !isPlaying);
    this.elements.replayIcon.classList.toggle("hidden", !showReplay);
    this.elements.playPauseBtn.setAttribute(
      "aria-label",
      isPlaying ? "Szünet" : showReplay ? "Újrajátszás" : "Lejátszás",
    );
  }
}
