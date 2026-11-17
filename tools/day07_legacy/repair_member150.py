"""Reproduce disclosed AI schema repair; does not create independent attributes.

Read the preserved raw submission. Geometry/classes remain unchanged. Missing
occlusion is derived from a matching submitted box, or provisionally zero;
truncation uses border contact. Every object remains can_review=true.
"""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from common import iou


def main():
    original = ROOT / 'submission/qc/imports/2026-11-17/member_150/original_150.json'
    data = json.loads(original.read_text(encoding='utf-8'))
    peers = []
    for member in ('117', '084', '133'):
        peer = json.loads((ROOT / f'submission/labels/{member}.json').read_text(encoding='utf-8'))
        images = {i['id']: Path(i['file_name']).name for i in peer['images']}
        cats = {c['id']: c['name'] for c in peer['categories']}
        peers.extend((images[a['image_id']], cats[a['category_id']], a) for a in peer['annotations'])
    images = {i['id']: i for i in data['images']}
    cats = {c['id']: c['name'] for c in data['categories']}
    xyxy = lambda b: (b[0], b[1], b[0]+b[2], b[1]+b[3])
    for ann in data['annotations']:
        cls = cats[ann['category_id']]
        if cls == 'ignore_region':
            continue
        image = images[ann['image_id']]
        box = xyxy(ann['bbox'])
        matches = [(iou(box, xyxy(a['bbox'])), a) for n, c, a in peers
                   if n == Path(image['file_name']).name and c == cls]
        score, peer = max(matches, key=lambda pair: pair[0]) if matches else (0, None)
        attrs = ann.setdefault('attributes', {})
        attrs['occluded_level'] = str(peer['attributes']['occluded_level']) if score >= .5 else '0'
        attrs['truncated'] = 'yes' if min(box[:2]) <= 0 or box[2] >= image['width'] or box[3] >= image['height'] else 'no'
        attrs['can_review'] = True
    data.setdefault('info', {})['attribute_repair'] = {
        'by': 'AI assistant', 'human_review_complete': False,
        'original': original.relative_to(ROOT).as_posix(),
        'warning': 'All original annotations lacked occluded_level/truncated. Added values are derived/provisional, not member 150 independent attribute decisions. can_review remains true.'}
    destination = ROOT / 'submission/labels/150.json'
    text = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if destination.exists() and json.loads(destination.read_text(encoding='utf-8')) != data:
        raise RuntimeError('Existing 150 labels changed; preserve their revision before applying repair again')
    destination.write_text(text, encoding='utf-8')
    print('Reproduced disclosed repair:', hashlib.sha256(destination.read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
