#!/usr/bin/swift
import CoreGraphics
import Foundation

let opts = CGWindowListOption(arrayLiteral: .optionOnScreenOnly, .excludeDesktopElements)
guard let list = CGWindowListCopyWindowInfo(opts, kCGNullWindowID) as? [[String: Any]] else {
    fputs("no windows\n", stderr)
    exit(1)
}

var bestArea: CGFloat = 0
var bestId: UInt32 = 0

for w in list {
    let owner = (w[kCGWindowOwnerName as String] as? String ?? "").lowercased()
    if owner.contains("crash") {
        continue
    }
    if !owner.contains("firefox") && !owner.contains("nightly") {
        continue
    }
    guard let bounds = w[kCGWindowBounds as String] as? [String: CGFloat] else { continue }
    let width = bounds["Width"] ?? 0
    let height = bounds["Height"] ?? 0
    if width < 400 || height < 300 { continue }
    let layer = w[kCGWindowLayer as String] as? Int ?? 0
    if layer != 0 { continue }
    let area = width * height
    if area > bestArea {
        bestArea = area
        bestId = w[kCGWindowNumber as String] as? UInt32 ?? 0
    }
}

if bestId == 0 {
    fputs("firefox window not found\n", stderr)
    exit(2)
}

print(bestId)
