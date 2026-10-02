# XR Sandbox: Three Anchor Tracker Comparison

This public GitHub Pages test compares MindAR and the MIT 8th Wall Engine image tracker with the same three image targets and one procedural sculpture.

- Board: `https://jlicerio.github.io/xr-sandbox-three-anchor-test/dev/three-anchor/?mode=board`
- MindAR: `https://jlicerio.github.io/xr-sandbox-three-anchor-test/dev/three-anchor/index.html?mode=scan&engine=mindar`
- 8th Wall image tracking: `https://jlicerio.github.io/xr-sandbox-three-anchor-test/dev/three-anchor/index.html?mode=scan&engine=8thwall`
- Composite print target: `https://jlicerio.github.io/xr-sandbox-three-anchor-test/dev/three-anchor/?mode=board&layout=composite`
- Composite 8th Wall scan: `https://jlicerio.github.io/xr-sandbox-three-anchor-test/dev/three-anchor/index.html?mode=scan&engine=8thwall&layout=composite`

Scan the engine QR code with a phone. Tap **Start camera**. Test each engine in a separate run. Keep all three target cards in one fixed row.

The 8th Wall mode uses `@8thwall/engine@0.1.0` under its MIT license. This engine build supports image tracking. It does not include world tracking. This test disables world tracking.

The 8th Wall target metadata and luminance images use output from the official `@8thwall/image-target-cli@1.0.0`. The input targets are the same PNG files that MindAR compiles in the browser.

The three shared target cards use distinct monochrome, rounded-square code patterns with rounded corners. They are image targets, not standard ArUco codes. Run `python3 public/dev/three-anchor/tools/generate-targets.py` to regenerate the PNG cards and 8th Wall image files.

The composite print target places all three rounded code images on one text-free portrait sheet. The composite scan uses one image target and places the full sculpture over its three panels.

The 8th Wall camera view uses the XR Sandbox cover-fit method. Its scanner shows the configured and detected target names.

MindAR 1.2.5 and its MIT license are in `public/vendor/mindar/1.2.5`. The Three.js module uses the same vendor file. The QR code library loads from jsDelivr.

A static deployment check confirms page and asset access. A phone test must confirm camera access, detection, pose stability, target loss, and recovery.
