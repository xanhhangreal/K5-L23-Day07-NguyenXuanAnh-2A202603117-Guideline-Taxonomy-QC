"""Use the existing user's local CVAT REST views, scoped to Task 25 only."""
import json
import hashlib
import os
from pathlib import Path
import sys
from urllib.parse import urlsplit

os.environ.setdefault('DJANGO_SETTINGS_MODULE','cvat.settings.production')
sys.path.insert(0,'/home/django')
import django
django.setup()
from django.test import override_settings
from rest_framework.test import APIClient
from cvat.apps.engine.models import Task
from cvat.apps.engine.models import Job

task=Task.objects.get(pk=25)
assert task.name=='Day07_117_v1.0' and task.owner is not None
client=APIClient()
client.force_authenticate(task.owner)
request=json.loads(Path(sys.argv[1]).read_text())
path=request['path']
parsed=urlsplit(path)
assert not parsed.scheme and not parsed.netloc
assert (parsed.path.startswith('/api/tasks/25/') or parsed.path=='/api/tasks/25'
        or parsed.path=='/api/labels' and 'task_id=25' in parsed.query
        or parsed.path=='/api/jobs/25'
        or parsed.path.startswith('/api/requests/'))
method=request.get('method','GET').lower()
assert method in ('get','post','put','patch')
if method=='patch':
    assert parsed.path=='/api/jobs/25' and Job.objects.get(pk=25).segment.task_id==25
    assert set(request.get('data',{})) <= {'state','stage'}
if method=='put':
    assert parsed.path=='/api/tasks/25/annotations'
    current=client.get('/api/tasks/25/annotations',HTTP_HOST='localhost').json()
    if any(current.get(key) for key in ('shapes','tracks','tags')):
        expected=request.get('expected_annotations_sha256')
        actual=hashlib.sha256(json.dumps(current,sort_keys=True).encode()).hexdigest()
        if not expected or actual!=expected:
            raise RuntimeError('Task changed or no exact backup hash provided; do not overwrite')
with override_settings(SENDFILE_BACKEND='django_sendfile.backends.development'):
    response=getattr(client,method)(path,data=request.get('data',{}),format='json',HTTP_HOST='localhost')
    if request.get('download') and response.status_code==200:
        dest=Path('/tmp/day07-117-export.zip')
        with dest.open('wb') as f:
            if response.streaming:
                for part in response.streaming_content:f.write(part)
            else:f.write(response.content)
        body={'file':str(dest),'bytes':dest.stat().st_size}
    else:
        try:body=response.json()
        except Exception:body=response.content.decode(errors='replace')[:2000]
print('DAY07_RESULT='+json.dumps({'status':response.status_code,'data':body},ensure_ascii=False))
