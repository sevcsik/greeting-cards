import { TRACKS, getTrackFromQuery } from "./config.js";
import { AudioPlayer } from "./player.js";

const audioElement = document.getElementById("audio");
const elements = {
  playPauseBtn: document.getElementById("play-pause-btn"),
  prevBtn: document.getElementById("prev-btn"),
  nextBtn: document.getElementById("next-btn"),
  playIcon: document.querySelector(".icon--play"),
  pauseIcon: document.querySelector(".icon--pause"),
  progressBar: document.getElementById("progress-bar"),
  currentTime: document.getElementById("current-time"),
  duration: document.getElementById("duration"),
  trackTitle: document.getElementById("track-title"),
  trackList: document.getElementById("track-list"),
};

const deepLinkTrack = getTrackFromQuery();
const player = new AudioPlayer({
  audioElement,
  tracks: TRACKS,
  elements,
  autoPlay: Boolean(deepLinkTrack),
});

if (deepLinkTrack) {
  player.selectTrackById(deepLinkTrack.id, { autoplay: true });
}
