export const TRACKS = [
  {
    id: 1,
    title: "Éva",
    src: "assets/audio/track1.m4a",
  },
  {
    id: 2,
    title: "Margó",
    src: "assets/audio/track2.m4a",
  },
  {
    id: 3,
    title: "Lilla",
    src: "assets/audio/track3.m4a",
  },
  {
    id: 4,
    title: "Kati",
    src: "assets/audio/track4.m4a",
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
