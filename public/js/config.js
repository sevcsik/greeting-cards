export const TRACKS = [
  {
    id: 1,
    title: "Üdvözlő 1",
    src: "assets/audio/track1.mp3",
  },
  {
    id: 2,
    title: "Üdvözlő 2",
    src: "assets/audio/track2.mp3",
  },
  {
    id: 3,
    title: "Üdvözlő 3",
    src: "assets/audio/track3.mp3",
  },
  {
    id: 4,
    title: "Üdvözlő 4",
    src: "assets/audio/track4.mp3",
  },
];

export function formatTime(seconds) {
  if (!Number.isFinite(seconds) || seconds < 0) {
    return "0:00";
  }

  const wholeSeconds = Math.floor(seconds);
  const minutes = Math.floor(wholeSeconds / 60);
  const remainingSeconds = wholeSeconds % 60;
  return `${minutes}:${String(remainingSeconds).padStart(2, "0")}`;
}

export function getTrackFromQuery() {
  const params = new URLSearchParams(window.location.search);
  const rawValue = params.get("track");

  if (!rawValue) {
    return null;
  }

  const trackId = Number.parseInt(rawValue, 10);
  if (!Number.isInteger(trackId)) {
    return null;
  }

  return TRACKS.find((track) => track.id === trackId) ?? null;
}
