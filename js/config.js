export const TRACKS = [
  {
    id: 1,
    slug: "Éva néni",
    title: "Éva néni",
    src: "assets/audio/track1.m4a",
  },
  {
    id: 2,
    slug: "Margó",
    title: "Margó",
    src: "assets/audio/track2.m4a",
  },
  {
    id: 3,
    slug: "Lilla",
    title: "Lilla",
    src: "assets/audio/track3.m4a",
  },
  {
    id: 4,
    slug: "Kati",
    title: "Kati",
    src: "assets/audio/track4.m4a",
  },
];

export function normalizeTrackKey(value) {
  return value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

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

  const queryKey = normalizeTrackKey(rawValue);
  return (
    TRACKS.find((track) => normalizeTrackKey(track.slug) === queryKey) ?? null
  );
}
