#!/usr/bin/env python3
# -*- mode: python; python-indent-offset: 4; indent-tabs-mode: nil -*-
# SPDX-License-Indentifier: MIT

''' Scan bluetooth for your lamps. Check for "unpaired" and MAC addresses starting with a4:c1:38 '''

import time
from bluepy.btle import Scanner

def scan_devices(duration=10):
    scanner = Scanner()
    devices = scanner.scan(duration)
    found = {}
    for dev in devices:
        found[dev.addr] = {
            'addrType': dev.addrType,
            'rssi': dev.rssi,
            'scanData': dev.getScanData()
        }
    return found

def print_device_info(addr, info):
    print(f"Device {addr} ({info['addrType']}), RSSI={info['rssi']} dB")
    for (adtype, desc, value) in info['scanData']:
        print(f"  {desc}: {value}")

if __name__ == "__main__":
    print("Step 1: Ensure your lamp is OFF, then press Enter to start scanning...")
    input()
    print("Scanning for BLE devices (lamp OFF)...")
    off_devices = scan_devices()
    print(f"Found {len(off_devices)} devices with lamp OFF.\n")

    print("Step 2: Turn your lamp ON (pairing mode), then press Enter to start scanning...")
    input()
    print("Scanning for BLE devices (lamp ON)...")
    on_devices = scan_devices()
    print(f"Found {len(on_devices)} devices with lamp ON.\n")

    # Find candidates: devices present only when lamp is ON
    candidates = {addr: info for addr, info in on_devices.items() if addr not in off_devices}

    if candidates:
        print("\nCandidate devices that appeared only when the lamp was ON (pairing mode):\n")
        print("Check for unpaired and MAC addresses starting with a4:c1:38\n")
        for addr, info in candidates.items():
            print_device_info(addr, info)
            print()
    else:
        print("No new devices found when the lamp was turned ON. Try again or check lamp pairing mode.")
