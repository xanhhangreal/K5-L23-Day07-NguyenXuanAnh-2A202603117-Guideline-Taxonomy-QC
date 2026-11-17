"""Import into empty Task 25, verify saved rectangles and export genuine CVAT COCO."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import time
from urllib.parse import quote, urlsplit
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[2]
WORK=ROOT/'work/legacy117'


def call(path,method='GET',data=None,download=False):
    parsed=urlsplit(path)
    if parsed.netloc:
        assert parsed.hostname=='localhost' and parsed.scheme=='http'
        path=parsed.path+('?' + parsed.query if parsed.query else '')
    request=WORK/'request.json'
    request.write_text(json.dumps({'path':path,'method':method,'data':data or {},'download':download}),encoding='utf-8')
    subprocess.run(['docker','cp',str(request),'cvat_server:/tmp/day07-117-request.json'],check=True,capture_output=True)
    result=subprocess.run(['docker','exec','cvat_server','python','/tmp/day07-117-api.py','/tmp/day07-117-request.json'],check=True,capture_output=True,text=True,encoding='utf-8')
    response=json.loads(result.stdout.split('DAY07_RESULT=')[-1])
    if response['status']>=400:raise RuntimeError(response)
    return response['data']


def signature(shape):
    return (shape['frame'],shape['label_id'],shape['type'],tuple(round(v,4) for v in shape['points']),
            tuple(sorted((a['spec_id'],str(a['value']).lower()) for a in shape['attributes'])),shape['source'])


def main():
    payload=json.loads((WORK/'annotations_to_import.json').read_text())
    previous=call('/api/tasks/25/annotations')
    backup=WORK/('annotations_backup_'+str(time.time_ns())+'.json')
    backup.write_text(json.dumps(previous,ensure_ascii=False,indent=2),encoding='utf-8')
    if any(previous.get(k) for k in ('shapes','tracks','tags')):
        if Counter(map(signature,previous['shapes'])) != Counter(map(signature,payload['shapes'])):
            raise RuntimeError('Existing annotations do not match this run; no overwrite')
        print('Matching annotations already saved; export only',flush=True)
    else:
        payload['version']=previous.get('version',0)
        call('/api/tasks/25/annotations','PUT',payload)
    stored=call('/api/tasks/25/annotations')
    assert Counter(map(signature,stored['shapes']))==Counter(map(signature,payload['shapes']))
    (WORK/'annotations_after.json').write_text(json.dumps(stored,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Verified CVAT Task 25:',len(stored['shapes']),'saved rectangles',flush=True)
    request=call('/api/tasks/25/dataset/export?format=COCO%201.0&save_images=false&location=local','POST')
    request_id=request['rq_id']
    (WORK/'export_request.json').write_text(json.dumps(request),encoding='utf-8')
    deadline=time.monotonic()+600
    last=None
    while time.monotonic()<deadline:
        result=call('/api/requests/'+quote(request_id,safe=''))
        status=result['status']
        if status!=last:print('Export:',status,flush=True);last=status
        if status=='finished':break
        if status=='failed':raise RuntimeError(result)
        time.sleep(3)
    else:raise TimeoutError('CVAT export still running; request ID saved')
    downloaded=call(result['result_url'],download=True)
    exports=ROOT/'submission/exports';exports.mkdir(exist_ok=True)
    archive=exports/'117_cvat_coco.zip'
    if archive.exists():raise FileExistsError('Export already exists; preserve it before replacing')
    subprocess.run(['docker','cp','cvat_server:'+downloaded['file'],str(archive)],check=True,capture_output=True)
    output=ROOT/'submission/labels/117.json'
    if output.exists():raise FileExistsError('Existing submission label file preserved')
    with ZipFile(archive) as z:
        assert z.testzip() is None
        instances=[name for name in z.namelist() if name.startswith('annotations/') and name.endswith('.json')]
        assert len(instances)==1,instances
        original_bytes=z.read(instances[0])
        coco=json.loads(original_bytes)
        assert len(coco['images'])==20 and len(coco['annotations'])==len(payload['shapes'])
        output.write_bytes(original_bytes)
    subprocess.run(['python',str(ROOT/'scripts/validate_labels.py'),str(output)],check=True,cwd=ROOT)
    record={'task_id':25,'job_id':25,'task_url':'http://localhost:8080/tasks/25',
            'status':'auto_annotated_exported_validated','human_review_complete':False,
            'source':'YOLO11l + SAM ViT-B CPU with assistant visual corrections',
            'images':20,'annotations':len(coco['annotations']),'export_request':request_id,
            'exported_at':datetime.now(timezone.utc).isoformat(),
            'coco_sha256':hashlib.sha256(original_bytes).hexdigest(),
            'zip_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}
    (WORK/'completion.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(record,ensure_ascii=False,indent=2),flush=True)


if __name__=='__main__':main()
