"""Run unchanged lab IAA on an explicitly isolated subset with two submitted labels."""
import csv
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import re
from collections import Counter

ROOT=Path(__file__).resolve().parents[2]
ACTIVE=['084','117','133']
EXCLUDED='150'
STAMP='2026-11-17_084_117_133'
STAGE=ROOT/'work'/('partial_iaa_'+STAMP)
OUT=ROOT/'submission/qc'/('partial_'+STAMP)


def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def write_csv(path,fields,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader();writer.writerows(rows)


def main():
    global STAGE,OUT
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run-tag',default=STAMP,help='Use a new safe name to replay without overwriting prior evidence')
    args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_-]+',args.run_tag):parser.error('Unsafe run tag')
    STAGE=ROOT/'work'/('partial_iaa_'+args.run_tag)
    OUT=ROOT/'submission/qc'/('partial_'+args.run_tag)
    if OUT.exists() or STAGE.exists():
        raise FileExistsError('Preserve the previous run; choose another timestamp for a new comparison')
    rows=list(csv.DictReader((ROOT/'submission/qc/assignment.csv').open(encoding='utf-8-sig',newline='')))
    sources={member:json.loads((ROOT/f'submission/labels/{member}.json').read_text(encoding='utf-8')) for member in ACTIVE}
    image_sets={member:{Path(image['file_name']).name for image in data['images']} for member,data in sources.items()}
    coverage=[];eligible=[];missing=[]
    for row in rows:
        original=row['annotators'].split('|')
        submitted=[member for member in original if member in ACTIVE and row['image'] in image_sets[member]]
        coverage.append({'image':row['image'],'original_annotators':row['annotators'],'submitted_annotators':'|'.join(submitted),
                         'submitted_count':len(submitted),'required_count':len(original),
                         'status':'eligible_for_partial_iaa' if len(submitted)>=2 else 'needs_second_independent_label'})
        if len(submitted)>=2:
            eligible.append({'image':row['image'],'annotators':'|'.join(submitted),'n_annotators':len(submitted)})
        else:
            assert len(submitted)==1
            missing.append({'image':row['image'],'existing_annotator':submitted[0],'excluded_original_member':EXCLUDED})
    assert len(eligible)==20 and len(missing)==20
    for folder in ['scripts','schemas']:
        shutil.copytree(ROOT/folder,STAGE/folder,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    for relative in ['submission/taxonomy.json','submission/guidelines/guideline_v1.0_agreed.md','data/ATTRIBUTION.csv']:
        dest=STAGE/relative;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/relative,dest)
    (STAGE/'data/images').mkdir(exist_ok=True)
    for row in eligible:
        shutil.copyfile(ROOT/'data/images'/row['image'],STAGE/'data/images'/row['image'])
    write_csv(STAGE/'submission/qc/assignment.csv',['image','annotators','n_annotators'],eligible)
    for member,data in sources.items():
        expected={row['image'] for row in eligible if member in row['annotators'].split('|')}
        images=[image for image in data['images'] if Path(image['file_name']).name in expected]
        ids={image['id'] for image in images}
        subset={**data,'images':images,'annotations':[annotation for annotation in data['annotations'] if annotation['image_id'] in ids]}
        save(STAGE/f'submission/labels/{member}.json',subset)
    for script,args in [('validate_labels.py',['--all']),('qc_compare.py',[]),('viz_disagreement.py',['--images','flagged'])]:
        subprocess.run([sys.executable,str(STAGE/'scripts'/script),*args],cwd=STAGE,check=True)
    OUT.mkdir(parents=True)
    for path in (STAGE/'submission/qc').iterdir():
        if path.is_file():shutil.copyfile(path,OUT/path.name)
    for member in ACTIVE:
        dest=OUT/f'input_subset/labels/{member}.json';dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(STAGE/f'submission/labels/{member}.json',dest)
    write_csv(OUT/'coverage_full_batch.csv',list(coverage[0]),coverage)
    write_csv(OUT/'missing_second_label.csv',list(missing[0]),missing)
    counts=Counter({member:20 for member in ACTIVE})
    supplement=[]
    for row in missing:
        candidates=[member for member in ACTIVE if member!=row['existing_annotator']]
        chosen=min(candidates,key=lambda member:(counts[member],member));counts[chosen]+=1
        supplement.append({**row,'new_annotator':chosen})
    write_csv(OUT/'supplemental_assignments.csv',list(supplement[0]),supplement)
    for member in ACTIVE:
        images=[row['image'] for row in supplement if row['new_annotator']==member]
        (OUT/f'supplemental_{member}.txt').write_text('\n'.join(images)+'\n',encoding='utf-8')
    hashes={f'submission/labels/{member}.json':hashlib.sha256((ROOT/f'submission/labels/{member}.json').read_bytes()).hexdigest() for member in ACTIVE}
    hashes['submission/qc/assignment.csv']=hashlib.sha256((ROOT/'submission/qc/assignment.csv').read_bytes()).hexdigest()
    scope={'status':'HOLD_FULL_BATCH_INCOMPLETE','active_members':ACTIVE,'excluded_missing_member':EXCLUDED,
           'full_batch_images':40,'full_batch_completed_assignments':sum(row['submitted_count'] for row in coverage),
           'full_batch_required_assignments':sum(int(row['n_annotators']) for row in rows),
           'images_with_at_least_one_submission':sum(row['submitted_count']>0 for row in coverage),
           'partial_iaa_images':len(eligible),'partial_iaa_assignments':2*len(eligible),'single_annotator_images':len(missing),
           'warning':'All iaa_summary metrics in this directory apply ONLY to the 20-image subset. 40/40 assignments in that summary means 40/40 within the subset, not 80/80 for the original batch.',
           'source_hashes':hashes,'partial_subset_labels_are_derived_not_original_submissions':True,
           'original_labels_and_assignment_modified':False,'replay_workspace':STAGE.relative_to(ROOT).as_posix(),
           'source_117':'YOLO + SAM ViT-B with assistant visual review, not a claim of independent human-only annotation',
           'supplemental_assignments_are_plan_only':True,'planned_final_loads':dict(counts)}
    save(OUT/'SCOPE.json',scope)
    summary=json.loads((OUT/'iaa_summary.json').read_text());overall=summary['overall']
    report=f'''# IAA một phần — bỏ qua thành viên 150

**Trạng thái toàn lô: HOLD.** Theo yêu cầu người dùng, không chờ 150 để phân tích phần đã có. Không thay bảng phân công gốc, không tạo nhãn thay người chưa nộp.

## Dữ liệu đã nhận

- 117: 20 ảnh, 203 annotation; nhãn tự động và AI đã xem lại.
- 084: 20 ảnh, 274 annotation, import nguyên byte từ ZIP mới.
- 133: 20 ảnh, 281 annotation, import nguyên byte từ ZIP mới.
- 150: chưa có nhãn, được loại khỏi lượt phân tích này.
- Validator của ba file đều chạy thành công. Bản 133 có cảnh báo vật nhỏ dưới 20 px cần đối chiếu guideline; không tự sửa nhãn độc lập đã nộp.

## Phạm vi và mẫu số

- Toàn lô có dữ liệu cho **40/40 ảnh**, nhưng mới đủ **60/80 lượt gán (75%)**.
- **20/40 ảnh** có hai người đã nộp: dùng để tính IAA bên dưới.
- **20/40 ảnh** mới có một người: không đưa vào phép đo đồng thuận.
- Con số 40/40 trong iaa_summary.md là 40 lượt của **tập con 20 ảnh**, không phải toàn lô 40 ảnh.

## Kết quả trên 20 ảnh đủ cặp

- Cặp box ghép được: **{overall['n_matched_pairs']}** (ghép 1–1, không phân biệt lớp, IoU ≥ 0,5).
- IoU trung bình: **{overall['mean_iou']:.3f}**; đồng thuận lớp: **{overall['class_agreement']*100:.1f}%**.
- Box chưa ghép ở hai phía cộng theo từng cặp: **{overall['n_unmatched_a']}/{overall['n_unmatched_b']}**.
- Ca bất đồng/cần xem: **{summary['n_issues']}**, trên **{summary['n_flagged_images']}/20 ảnh**.
- Kết quả này là đồng thuận của các nguồn đã nộp, không phải độ chính xác so với ground truth; 117 có sử dụng mô hình và AI.

Chi tiết: `iaa_summary.md`, `calibration_candidates.csv`, `image_scores.csv`. `consensus_draft.json` chỉ là nháp tự động của 20 ảnh trong phạm vi này, chưa là nhãn cuối.

## Làm tiếp khi không dùng bài của 150

Đã lập `supplemental_assignments.csv` cho **20 lượt gán bổ sung độc lập**, giao cho người khác người đã gán ảnh đó. Tải dự kiến sau bổ sung: 084 = {counts['084']}, 117 = {counts['117']}, 133 = {counts['133']} ảnh. Đây là phân công mới cần thực hiện, không phải kết quả đã có. Mỗi người không được xem nhãn hiện có của ảnh bổ sung trước khi gán.

Có thể mở overlay trong `{(STAGE/'work/viz').relative_to(ROOT).as_posix()}` để calibration các ảnh đã đủ cặp. Giữ nguyên nhãn độc lập ban đầu. Chưa điền quyết định calibration, chưa tạo nhãn cuối hoặc báo cáo Release toàn lô.

Nguồn import và SHA-256 ZIP gốc: `../imports/2026-11-17/import_manifest.json`. Phạm vi và mã băm đầu vào: `SCOPE.json`.
'''
    (OUT/'PARTIAL_IAA_REPORT.md').write_text(report,encoding='utf-8')
    print('Saved partial report:',OUT/'PARTIAL_IAA_REPORT.md')
    print('Full batch coverage: 60/80; eligible subset: 20 images; supplemental plan:',dict(counts))


if __name__=='__main__':main()
