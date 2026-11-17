"""Build the explicitly AI-assisted correction, preserving submitted source boxes.

Run after recording visual edits for all 40 images. This is not evidence of
independent human annotation or group sign-off. Core lab gates are unchanged.
"""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import sys

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
from calibration import calibration_export_path
from common import iou


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def write_csv(path, fields, rows):
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    work = ROOT / 'work/assistant_batch'
    evidence = ROOT / 'submission/automation/batch_review'
    qc = ROOT / 'submission/qc'
    seed = json.loads((evidence / 'seed.json').read_text(encoding='utf-8'))
    edits = json.loads((evidence / 'edits.json').read_text(encoding='utf-8'))
    edit_hash = hashlib.sha256((evidence / 'edits.json').read_bytes()).hexdigest()
    assert set(seed) == set(edits) == {f'img_{n:03}.jpg' for n in range(1, 41)}
    tax = json.loads((ROOT / 'submission/taxonomy.json').read_text(encoding='utf-8'))
    cats = {c['name']: i for i, c in enumerate(tax['classes'], 1)}
    coco = {'info': {'description': 'AI-assisted full-batch correction; human approval pending',
                     'human_review_complete': False, 'reviewer': 'AI assistant; reserved code 999',
                     'independent_human_qc': False},
            'images': [], 'categories': [{'id': v, 'name': k} for k, v in cats.items()], 'annotations': []}
    logs = []
    for image_id, (name, entry) in enumerate(sorted(seed.items()), 1):
        source = ROOT / 'data/images' / name
        assert hashlib.sha256(source.read_bytes()).hexdigest() == entry['sha256']
        width, height = entry['size']
        edit = edits[name]
        assert set(edit.get('remove', [])) <= set(range(len(entry['objects'])))
        assert {int(i) for i in edit.get('modify', {})} <= set(range(len(entry['objects'])))
        coco['images'].append({'id': image_id, 'file_name': name, 'width': width, 'height': height})
        image = Image.open(source).convert('RGB')
        draw = ImageDraw.Draw(image)
        objects = []
        for index, original in enumerate(entry['objects']):
            if index in edit.get('remove', []):
                continue
            obj = json.loads(json.dumps(original))
            obj.update(edit.get('modify', {}).get(str(index), {}))
            obj['source_index'] = index
            objects.append(obj)
        objects.extend(edit.get('add', []))
        ids = []
        flagged = []
        conversions = []
        for obj in objects:
            x1, y1, x2, y2 = obj['box']
            assert 0 <= x1 < x2 <= width and 0 <= y1 < y2 <= height, (name, obj)
            cls = obj['class']
            attrs = obj.get('attributes', {}).copy()
            for key in ('occluded_level', 'truncated', 'can_review'):
                if key in obj:
                    attrs[key] = obj[key]
            attrs.setdefault('occluded_level', '0')
            attrs.setdefault('truncated', 'yes' if min(x1, y1) <= 0 or x2 >= width or y2 >= height else 'no')
            attrs.setdefault('can_review', False)
            attrs['occluded_level'] = str(attrs['occluded_level'])
            if y2-y1 < tax['rules']['min_box_height_px'] and cls != 'ignore_region':
                conversions.append({'source_class': cls, 'box': obj['box']})
                cls = 'ignore_region'
            if cls == 'ignore_region':
                attrs = {}
            ann_id = len(coco['annotations']) + 1
            ann = {'id': ann_id, 'image_id': image_id, 'category_id': cats[cls],
                   'bbox': [x1, y1, x2-x1, y2-y1], 'area': (x2-x1)*(y2-y1), 'iscrowd': 0,
                   'attributes': attrs}
            coco['annotations'].append(ann)
            ids.append(ann_id)
            if attrs.get('can_review') in (True, 'true'):
                flagged.append(ann_id)
            color = 'orange' if cls == 'ignore_region' else '#ff3050' if cls == 'person' else '#00dfff'
            draw.rectangle([x1, y1, x2, y2], outline=color, width=2)
            draw.text((x1, max(0, y1-12)), f'{ann_id}:{cls}', fill=color, stroke_width=1, stroke_fill='black')
        (work / 'final_overlays').mkdir(exist_ok=True)
        image.save(work / 'final_overlays' / (Path(name).stem + '.png'))
        logs.append({'image': name, 'source': entry['source'], 'source_annotations': len(entry['objects']),
                     'final_annotation_ids': ids, 'remaining_can_review': flagged,
                     'small_objects_to_ignore': conversions, 'actions': edit,
                     'reviewer': 'AI assistant', 'human_review_complete': False})

    save(evidence / 'review_log.json', {'reviewed_images': 40, 'human_review_complete': False,
                                      'reviewer_code': '999 (reserved for AI, not a group member)', 'images': logs})
    save(evidence / 'corrected_batch.json', coco)
    rows = list(csv.DictReader((qc / 'calibration_candidates.csv').open(encoding='utf-8', newline='')))
    fields = ['case_id', 'image', 'quyet_dinh', 'quy_tac_ghi_vao_guideline', 'phien_ban_guideline',
              'nguoi_chot', 'phieu_sua', 'kiem_lai', 'pham_vi']
    decisions = []
    xyxy = lambda b: (b[0], b[1], b[0]+b[2], b[1]+b[3])
    by_image = {i['file_name']: [a for a in coco['annotations'] if a['image_id'] == i['id']]
                for i in coco['images']}
    for row in rows:
        image = row['image']
        boxes = [xyxy(json.loads(row[k])) for k in ('box_a', 'box_b') if row.get(k)]
        linked = [a['id'] for a in by_image[image]
                  if any(iou(box, xyxy(a['bbox'])) >= .3 for box in boxes)]
        rules = {'sai_lop': 'R-01/R-07', 'sai_thuoc_tinh': 'R-02', 'iou_thap': 'R-03',
                 'bo_sot_thua': 'R-03/R-04/R-07', 'bat_dong_ignore': 'R-09',
                 'co_can_review': 'R-10', 'can_review_anh': 'R-10'}
        decisions.append({'case_id': row['case_id'], 'image': image,
                          'quyet_dinh': 'Đề xuất sửa của AI; chưa có chốt nhóm. ' + edits[image]['note'],
                          'quy_tac_ghi_vao_guideline': rules.get(row['issue_type'], 'R-10'),
                          'phien_ban_guideline': 'v1.1',
                          'nguoi_chot': 'AI assistant đề xuất; người thật chưa xác nhận',
                          'phieu_sua': f'AI batch {image}; edits SHA256 {edit_hash}; final object IDs {linked}; xem automation/batch_review/review_log.json',
                          'kiem_lai': 'AI đã đối chiếu overlay; chưa phải kiểm độc lập bởi thành viên',
                          'pham_vi': 'anh'})
    # Record every image even when its issues did not produce an IAA candidate.
    for n, log in enumerate(logs, 1):
        decisions.append({'case_id': f'AI{n:03}', 'image': log['image'],
                          'quyet_dinh': 'AI rà toàn ảnh: ' + log['actions']['note'],
                          'quy_tac_ghi_vao_guideline': 'R-01/R-02/R-03/R-07/R-09/R-10',
                          'phien_ban_guideline': 'v1.1', 'nguoi_chot': 'AI assistant; chưa có xác nhận nhóm',
                          'phieu_sua': 'automation/batch_review/review_log.json#' + log['image'] + '; edits SHA256 ' + edit_hash,
                          'kiem_lai': 'Đã mở ảnh và overlay bằng AI; người thật chưa duyệt', 'pham_vi': 'anh'})
    write_csv(qc / 'calibration_decisions.csv', fields, decisions)
    save(qc / 'calibration_context.json', {'iaa_summary_sha256': hashlib.sha256((qc/'iaa_summary.json').read_bytes()).hexdigest()})
    export = calibration_export_path(set(seed))
    save(export, coco)
    print('Prepared', export.relative_to(ROOT), len(coco['annotations']), 'annotations,', len(decisions), 'traceable proposal rows')
    print('Human sign-off is pending. AI reviewer 999 is not member 117/084/133/150.')


if __name__ == '__main__':
    main()
