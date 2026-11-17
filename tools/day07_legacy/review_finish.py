"""Save a snapshot-checked review, export genuine COCO, and complete the CVAT job."""
from collections import Counter
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time
from urllib.parse import quote
from zipfile import ZipFile

from finish import call,signature

ROOT=Path(__file__).resolve().parents[2]
WORK=ROOT/'work/review117_v2'


def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main():
    before=json.loads((WORK/'before.json').read_text())
    payload=json.loads((WORK/'after_payload.json').read_text())
    expected_hash=hashlib.sha256(json.dumps(before,sort_keys=True).encode()).hexdigest()
    current=call('/api/tasks/25/annotations')
    if Counter(map(signature,current['shapes']))!=Counter(map(signature,payload['shapes'])):
        assert hashlib.sha256(json.dumps(current,sort_keys=True).encode()).hexdigest()==expected_hash,'Live labels changed; no overwrite'
        request={'path':'/api/tasks/25/annotations','method':'PUT','data':payload,'expected_annotations_sha256':expected_hash}
        path=WORK/'replace_request.json';save(path,request)
        subprocess.run(['docker','cp',str(path),'cvat_server:/tmp/day07-117-review-request.json'],check=True,capture_output=True)
        result=subprocess.run(['docker','exec','cvat_server','python','/tmp/day07-117-api.py','/tmp/day07-117-review-request.json'],check=True,capture_output=True,text=True,encoding='utf-8')
        result=json.loads(result.stdout.split('DAY07_RESULT=')[-1]);assert result['status']==200,result
    stored=call('/api/tasks/25/annotations')
    assert Counter(map(signature,stored['shapes']))==Counter(map(signature,payload['shapes']))
    save(WORK/'stored_after.json',stored)
    print('Verified reviewed CVAT annotations:',len(stored['shapes']),flush=True)
    request=call('/api/tasks/25/dataset/export?format=COCO%201.0&save_images=false&location=local','POST')
    save(WORK/'export_request.json',request)
    deadline=time.monotonic()+600
    last=None
    while time.monotonic()<deadline:
        result=call('/api/requests/'+quote(request['rq_id'],safe=''))
        if result['status']!=last:print('Export:',result['status'],flush=True);last=result['status']
        if result['status']=='finished':break
        if result['status']=='failed':raise RuntimeError(result)
        time.sleep(3)
    else:raise TimeoutError('Export request saved, not finished')
    download=call(result['result_url'],download=True)
    temporary=WORK/'117_reviewed_cvat.zip'
    subprocess.run(['docker','cp','cvat_server:'+download['file'],str(temporary)],check=True,capture_output=True)
    with ZipFile(temporary) as z:
        assert z.testzip() is None
        paths=[n for n in z.namelist() if n.startswith('annotations/') and n.endswith('.json')]
        assert len(paths)==1
        data=z.read(paths[0]);coco=json.loads(data)
        assert len(coco['images'])==20 and len(coco['annotations'])==len(stored['shapes'])
    validation=WORK/'117.json';validation.write_bytes(data)
    subprocess.run(['python',str(ROOT/'scripts/validate_labels.py'),str(validation)],cwd=ROOT,check=True)
    history=ROOT/'submission/exports/history';history.mkdir(parents=True,exist_ok=True)
    for source in [ROOT/'submission/labels/117.json',ROOT/'submission/exports/117_cvat_coco.zip']:
        digest=hashlib.sha256(source.read_bytes()).hexdigest()[:12]
        backup=history/(source.stem+'_before_review_'+digest+source.suffix)
        if not backup.exists():shutil.copyfile(source,backup)
    shutil.copyfile(temporary,ROOT/'submission/exports/117_cvat_coco.zip')
    (ROOT/'submission/labels/117.json').write_bytes(data)
    # Complete annotation work; task status is checked rather than inferred.
    job=call('/api/jobs/25','PATCH',{'state':'completed'})
    task=call('/api/tasks/25')
    if task.get('status')!='completed':
        job=call('/api/jobs/25','PATCH',{'stage':'acceptance','state':'completed'})
        task=call('/api/tasks/25')
    assert job['state']=='completed' and task['status']=='completed',(job,task)
    review=json.loads((WORK/'review_log.json').read_text())
    count=sum(len(row['remaining_questions']) for row in review['images'])
    record={'member':'117','task_id':25,'job_id':25,'reviewer':'assistant_visual_review','reviewed_images':20,
            'human_review_complete':False,'before_annotations':len(before['shapes']),'after_annotations':len(stored['shapes']),
            'calibration_questions':count,'job_stage':job['stage'],'job_state':job['state'],'task_status':task['status'],
            'completed_at':datetime.now(timezone.utc).isoformat(),
            'coco_sha256':hashlib.sha256(data).hexdigest(),'zip_sha256':hashlib.sha256(temporary.read_bytes()).hexdigest(),
            'before_snapshot_sha256':expected_hash,'source':'YOLO11l + SAM ViT-B, then assistant inspection of all 20 images'}
    save(WORK/'completion.json',record)
    save(ROOT/'submission/automation/117_review_v2.json',review)
    save(ROOT/'submission/automation/117_completion.json',record)
    print(json.dumps(record,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':main()
