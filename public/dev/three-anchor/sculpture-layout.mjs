export const TARGET_SIZE = 384;
export const DISPLAY_CARD_SIZE = 256;
export const DISPLAY_GAP = 32;
export const LINK_LENGTH = (DISPLAY_CARD_SIZE + DISPLAY_GAP) / DISPLAY_CARD_SIZE;

export const TARGETS = [
  { index: 0, name: 'Anchor One', color: '#f7734a', seed: 19 },
  { index: 1, name: 'Anchor Two', color: '#57d6cb', seed: 47 },
  { index: 2, name: 'Anchor Three', color: '#f4c15d', seed: 83 },
];

export function segmentForTarget(index) {
  if (!Number.isInteger(index) || index < 0 || index >= TARGETS.length) {
    throw new RangeError(`Unknown target index: ${index}`);
  }

  return {
    nodes: [{ position: [0, 0, 0.16], color: TARGETS[index].color }],
    links: index < TARGETS.length - 1
      ? [{ from: [0, 0, 0.16], to: [LINK_LENGTH, 0, 0.16] }]
      : [],
  };
}
