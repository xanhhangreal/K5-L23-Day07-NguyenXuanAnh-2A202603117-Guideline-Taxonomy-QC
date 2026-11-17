"""Apply traceable assistant corrections to raw predictions and make CVAT rectangles."""
from collections import Counter
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[2]
WORK=ROOT/'work/legacy117'


def save(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main():
    names=(ROOT/'submission/qc/assignments/117.txt').read_text().splitlines()
    frames=json.loads((WORK/'meta.json').read_text())['frames']
    assert [Path(frame['name']).name for frame in frames]==names
    labels=json.loads((WORK/'labels.json').read_text())['results']
    mapping={label['name']:label for label in labels}
    categories=[{'id':label['id'],'name':label['name']} for label in labels]
    corrections=json.loads((ROOT/'tools/day07_legacy/corrections117.json').read_text())
    payload={'version':json.loads((WORK/'annotations_before.json').read_text()).get('version',0),'tags':[],'tracks':[],'shapes':[]}
    coco={'info':{'description':'YOLO11l + SAM ViT-B, assistant visual corrections; human review pending','human_review_complete':False},'images':[],'categories':categories,'annotations':[]}
    trace=[]
    for frame,name in enumerate(names):
        raw=json.loads((WORK/'predictions'/(Path(name).stem+'.json')).read_text())
        source=ROOT/'data/images'/name
        assert hashlib.sha256(source.read_bytes()).hexdigest()==raw['image_sha256']
        edit=corrections['images'].get(name,{})
        image=Image.open(source).convert('RGB');draw=ImageDraw.Draw(image)
        coco['images'].append({'id':frame+1,'file_name':name,'width':image.width,'height':image.height})
        kept=[]
        for index,obj in enumerate(raw['objects']):
            if edit.get('remove_all') or index in edit.get('remove',[]):continue
            obj=json.loads(json.dumps(obj))
            change=edit.get('modify',{}).get(str(index),{})
            for key in ('box','class'):
                if key in change:obj[key]=change[key]
            attrs=obj['attributes']
            for key in ('occluded_level','truncated'):
                if key in change:attrs[key]=change[key]
            x1,y1,x2,y2=obj['box']
            assert 0<=x1<x2<=image.width and 0<=y1<y2<=image.height,(name,index,obj)
            label='ignore_region' if y2-y1<20 else obj['class']
            attrs['truncated']='yes' if x1<=0 or y1<=0 or x2>=image.width or y2>=image.height else 'no'
            attrs['can_review']=True
            cvat_attrs=[]
            if label!='ignore_region':
                cvat_attrs=[{'spec_id':a['id'],'value':str(attrs[a['name']]).lower()} for a in mapping[label]['attributes']]
            shape={'type':'rectangle','frame':frame,'label_id':mapping[label]['id'],'points':[x1,y1,x2,y2],
                   'occluded':attrs['occluded_level']!='0','outside':False,'z_order':0,'rotation':0,
                   'attributes':cvat_attrs,'source':'auto'}
            payload['shapes'].append(shape)
            ann_id=len(coco['annotations'])+1
            coco['annotations'].append({'id':ann_id,'image_id':frame+1,'category_id':mapping[label]['id'],
                                        'bbox':[x1,y1,x2-x1,y2-y1],'area':(x2-x1)*(y2-y1),'iscrowd':0,
                                        'attributes':attrs if label!='ignore_region' else {}})
            draw.rectangle([x1,y1,x2-1,y2-1],outline='orange' if label=='ignore_region' else 'red',width=2)
            draw.text((x1,max(0,y1-12)),f'{ann_id}:{label}',fill='orange' if label=='ignore_region' else 'red')
            kept.append({'raw_index':index,'class':label,'box':[x1,y1,x2,y2],'attributes':attrs,'source':obj['source'], 'assistant_modified':bool(change)})
        overlay=WORK/'overlays_final'/(Path(name).stem+'.jpg');overlay.parent.mkdir(exist_ok=True);image.save(overlay)
        trace.append({'image':name,'source_sha256':raw['image_sha256'],'raw_count':len(raw['objects']),'final_count':len(kept),
                      'assistant_actions':edit,'human_review_complete':False,'objects':kept})
    assert len(coco['images'])==20 and payload['shapes']
    save(WORK/'annotations_to_import.json',payload)
    save(WORK/'117.json',coco)
    save(WORK/'provenance.json',{'backend':json.loads((WORK/'config.json').read_text()),'human_review_complete':False,
                               'assistant_review':'Image overlays inspected; documented rule-based corrections only, no human QC claim.',
                               'images':trace,'counts':dict(Counter(c['name'] for a in coco['annotations'] for c in categories if c['id']==a['category_id']))})
    print('Ready:',len(coco['images']),'images,',len(coco['annotations']),'annotations')
    for row in trace:print(row['image'],row['raw_count'],'->',row['final_count'])


if __name__=='__main__':main()
