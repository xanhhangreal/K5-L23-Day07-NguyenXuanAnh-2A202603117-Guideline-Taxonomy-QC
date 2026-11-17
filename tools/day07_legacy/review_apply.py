"""Prepare and apply the documented full-image assistant review with snapshot protection."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
from PIL import Image,ImageDraw

ROOT=Path(__file__).resolve().parents[2]
WORK=ROOT/'work/review117_v2'


def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def main():
    before=json.loads((WORK/'before.json').read_text())
    meta=json.loads((WORK/'meta.json').read_text())
    labels=json.loads((WORK/'labels.json').read_text())
    edits=json.loads((ROOT/'tools/day07_legacy/review117_v2.json').read_text())
    byname={l['name']:l for l in labels};byid={l['id']:l for l in labels}
    assert set(edits['images'])=={Path(f['name']).name for f in meta['frames']}
    payload={'version':before.get('version',0),'tags':before['tags'],'tracks':before['tracks'],'shapes':[]}
    log=[]
    coco={'images':[],'categories':[{'id':l['id'],'name':l['name']} for l in labels],'annotations':[]}
    for frame,item in enumerate(meta['frames']):
        name=Path(item['name']).name;edit=edits['images'][name]
        objects=[s for s in before['shapes'] if s['frame']==frame]
        valid_ids={s['id'] for s in objects}
        for key in ('remove','truncated'):
            assert set(edit.get(key,[]))<=valid_ids,(name,key)
        for key in ('modify','occlusion','uncertain'):
            assert {int(i) for i in edit.get(key,{})}<=valid_ids,(name,key)
        image=Image.open(ROOT/'data/images'/name).convert('RGB');draw=ImageDraw.Draw(image)
        coco['images'].append({'id':frame+1,'file_name':name,'width':image.width,'height':image.height})
        final=[];changes=[]
        for original in objects:
            obj=json.loads(json.dumps(original));old_id=obj['id']
            if old_id in edit.get('remove',[]):continue
            change=edit.get('modify',{}).get(str(old_id),{})
            if 'box' in change:obj['points']=change['box']
            if 'class' in change:obj['label_id']=byname[change['class']]['id']
            label=byid[obj['label_id']]
            occlusion=str(edit.get('occlusion',{}).get(str(old_id),0))
            uncertain=edit.get('uncertain',{}).get(str(old_id))
            attrs={'occluded_level':occlusion,'truncated':'yes' if old_id in edit.get('truncated',[]) else 'no',
                   'can_review':bool(uncertain)}
            obj['attributes']=[{'spec_id':a['id'],'value':str(attrs[a['name']]).lower()} for a in label['attributes']]
            obj['occluded']=occlusion!='0'
            changes.append({'previous_id':old_id,'label':label['name'],'box':obj['points'],'attributes':attrs,'remaining_question':uncertain})
            obj.pop('id',None)
            final.append(obj)
        for addition in edit.get('add',[]):
            label=byname[addition['class']]
            attrs={'occluded_level':str(addition['occluded_level']),'truncated':'no','can_review':False}
            obj={'type':'rectangle','frame':frame,'label_id':label['id'],'points':addition['box'],'occluded':attrs['occluded_level']!='0',
                 'outside':False,'z_order':0,'rotation':0,'source':'auto',
                 'attributes':[{'spec_id':a['id'],'value':str(attrs[a['name']]).lower()} for a in label['attributes']]}
            final.append(obj);changes.append({'previous_id':None,'label':label['name'],'box':obj['points'],'attributes':attrs,'addition_reason':addition['reason']})
        for obj in final:
            x1,y1,x2,y2=obj['points'];label=byid[obj['label_id']]
            assert 0<=x1<x2<=image.width and 0<=y1<y2<=image.height
            assert label['name']=='ignore_region' or y2-y1>=20,(name,obj)
            attr_names={a['id']:a['name'] for a in label['attributes']}
            attrs={attr_names[a['spec_id']]:a['value'] for a in obj['attributes']}
            if 'can_review' in attrs:attrs['can_review']=attrs['can_review']=='true'
            coco['annotations'].append({'id':len(coco['annotations'])+1,'image_id':frame+1,'category_id':label['id'],
                                        'bbox':[x1,y1,x2-x1,y2-y1],'attributes':attrs})
            draw.rectangle([x1,y1,x2-1,y2-1],outline='orange' if attrs.get('can_review') else 'lime',width=2)
            draw.text((x1,max(0,y1-11)),label['name'],fill='orange' if attrs.get('can_review') else 'lime')
        payload['shapes'].extend(final)
        log.append({'image':name,'reviewed':True,'reviewer':'assistant_visual_review','human_review_complete':False,
                    'note':edit['note'],'before_count':len(objects),'after_count':len(final),'removed_ids':edit.get('remove',[]),
                    'remaining_questions':edit.get('uncertain',{}),'objects':changes})
        out=WORK/'after_overlays';out.mkdir(exist_ok=True);image.save(out/(Path(name).stem+'.jpg'))
    save(WORK/'117.json',coco);save(WORK/'after_payload.json',payload)
    save(WORK/'review_log.json',{'reviewed_images':len(log),'reviewer':'assistant_visual_review','human_review_complete':False,
                               'before_annotations':len(before['shapes']),'after_annotations':len(payload['shapes']),'images':log})
    print('Prepared',len(log),'reviewed images,',len(before['shapes']),'->',len(payload['shapes']),'annotations')
    print('Remaining calibration questions:',sum(len(row['remaining_questions']) for row in log))


if __name__=='__main__':main()
