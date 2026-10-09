#!/usr/bin/env python3
"""Reproduce the unofficial v2.8.0-private.1 JS; no npm/source rebuild implied."""
import argparse
import hashlib
from pathlib import Path
from urllib.request import urlopen

URL = 'https://github.com/droans/mass-player-card/releases/download/v2.8.0/mass-player-card.js'
INPUT_SHA256 = '32b9f15f182ea1edad3853f4db6218c6173d912ba95f04672c7b0f1125ada1f1'
OUTPUT_SHA256 = '52920f63b12cbf3aa52205a9cc7b0fc788969344402a82138017c2cebb46120d'

def transform(data):
    if hashlib.sha256(data).hexdigest() != INPUT_SHA256:
        raise ValueError('Upstream input SHA256 mismatch')
    if data.count(b'lit-virtualizer') != 9:
        raise ValueError('Expected exactly nine names')
    result = data.replace(b'lit-virtualizer', b'mass-player-virtualizer')
    if hashlib.sha256(result).hexdigest() != OUTPUT_SHA256:
        raise ValueError('Output SHA256 mismatch')
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, help='Optional upstream JS for offline use')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    data = args.input.read_bytes() if args.input else urlopen(URL, timeout=60).read()
    result = transform(data)
    with args.output.open('xb') as output:
        output.write(result)
    print(OUTPUT_SHA256 + '  ' + str(args.output))
