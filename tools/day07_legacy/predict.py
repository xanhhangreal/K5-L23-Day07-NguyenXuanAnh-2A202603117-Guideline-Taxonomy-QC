"""Member 117 image-only prelabels using the existing YOLO11l + SAM ViT-B service."""
import base64
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import time

import numpy as np
from PIL import Image, ImageDraw
import requests
import torch
from ultralytics import YOLO

ROOT = Path('/workspace')
WORK = ROOT / 'work/legacy117'
SAM = 'http://nuclio-nuclio-pth-facebookresearch-sam-vit-b-cpu:8080'
CLASSES = {'person', 'car', 'truck', 'bus', 'motorcycle'}


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    tmp.replace(path)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sam_mask(raw, box):
    response = requests.post(SAM, json={'image': raw, 'obj_bbox': box, 'pos_points': [], 'neg_points': []}, timeout=180)
    response.raise_for_status()
    points = response.json()['shapes'][0]['points']
    x0, y0, x1, y1 = map(int, points[-4:])
    counts = np.asarray(points[:-4], dtype=np.int64)
    assert counts.min() >= 0 and counts.sum() == (x1-x0+1)*(y1-y0+1)
    mask = np.repeat(np.arange(len(counts)) % 2, counts).reshape(y1-y0+1, x1-x0+1).astype(bool)
    ys, xs = np.nonzero(mask)
    if not len(xs):
        return None
    return [float(x0+xs.min()), float(y0+ys.min()), float(x0+xs.max()+1), float(y0+ys.max()+1)]


def main():
    torch.set_num_threads(4)
    names = (ROOT/'submission/qc/assignments/117.txt').read_text().splitlines()
    assert len(names) == len(set(names)) == 20
    weights = Path('/cache/models/yolo11l.pt')
    config = {'backend': 'YOLO11l + SAM ViT-B CPU', 'weights_sha256': sha(weights),
              'ultralytics': importlib.metadata.version('ultralytics'), 'torch': torch.__version__,
              'imgsz': 1280, 'confidence': .25, 'iou': .5, 'sam_endpoint': SAM}
    signature = hashlib.sha256(json.dumps(config, sort_keys=True).encode()).hexdigest()
    save(WORK/'config.json', config)
    model = YOLO(str(weights))
    summary = []
    for index, name in enumerate(names, 1):
        image_path = ROOT/'work/117/images'/name
        key = sha(image_path)
        cache = WORK/'predictions'/(image_path.stem+'.json')
        if cache.exists():
            previous = json.loads(cache.read_text())
            if previous.get('image_sha256') == key and previous.get('config_signature') == signature:
                print(f'[{index}/20] {name}: cached {len(previous["objects"])} boxes', flush=True)
                summary.append(previous)
                continue
        started = time.monotonic()
        image = Image.open(image_path).convert('RGB')
        prediction = model.predict(image, imgsz=1280, conf=.25, iou=.5, device='cpu', max_det=150, verbose=False)[0]
        detections = []
        for box in prediction.boxes:
            label = prediction.names[int(box.cls.item())]
            if label in CLASSES:
                detections.append({'class': label, 'score': float(box.conf.item()), 'yolo_box': box.xyxy[0].tolist()})
        print(f'[{index}/20] {name}: {len(detections)} YOLO candidates -> SAM', flush=True)
        raw = base64.b64encode(image_path.read_bytes()).decode()
        objects = []
        for number, detection in enumerate(detections, 1):
            refined = sam_mask(raw, detection['yolo_box'])
            source = 'yolo_sam_vit_b' if refined is not None else 'yolo_empty_sam_mask'
            chosen = refined or detection['yolo_box']
            x1,y1,x2,y2 = chosen
            chosen = [max(0,x1), max(0,y1), min(image.width,x2), min(image.height,y2)]
            if chosen[2] > chosen[0] and chosen[3] > chosen[1]:
                objects.append({**detection, 'box': chosen, 'source': source,
                                'attributes': {'occluded_level':'0', 'truncated':'yes' if min(chosen[:2])<=1 or chosen[2]>=image.width-1 or chosen[3]>=image.height-1 else 'no', 'can_review':True}})
            if number % 10 == 0:
                print(f'  {name}: SAM {number}/{len(detections)}', flush=True)
        data = {'image':name, 'image_sha256':key, 'config_signature':signature, 'width':image.width,
                'height':image.height, 'objects':objects, 'seconds':round(time.monotonic()-started,2)}
        save(cache,data)
        summary.append(data)
        print(f'  saved {name}: {len(objects)} boxes in {data["seconds"]}s',flush=True)
    save(WORK/'raw_summary.json', {'status':'automatic_predictions_ready','human_review_complete':False,
                                 'completed_at':datetime.now(timezone.utc).isoformat(),
                                 'images':len(summary), 'objects':sum(len(r['objects']) for r in summary),
                                 'classes':dict(Counter(o['class'] for r in summary for o in r['objects']))})


if __name__ == '__main__':
    main()
