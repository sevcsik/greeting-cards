import { TRACKS, getTrackFromQuery } from "./config.js";
import { AudioPlayer } from "./player.js";

const audioElement = document.getElementById("audio");
const elements = {
  playPauseBtn: document.getElementById("play-pause-btn"),
  playIcon: document.querySelector(".icon--play"),
  pauseIcon: document.querySelector(".icon--pause"),
  replayIcon: document.querySelector(".icon--replay"),
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
