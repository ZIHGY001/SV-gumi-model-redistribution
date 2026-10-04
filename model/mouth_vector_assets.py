"""Small code-defined puppet mouths; preserve the approved face outside its mouth."""
from pathlib import Path
import base64,io,json
import cv2
import numpy as np
from PIL import Image,ImageDraw

PATCH_BOX=(228,303,275,339)  # head.png coordinates; no eye/face-contour overlap
CENTER=(22,15)
SHAPES=[('closed',0,0),('small',15,8),('medium',22,13),('wide',28,19),('large',34,25),('round',18,25)]

def create(head_file,output_dir):
    output_dir=Path(output_dir);output_dir.mkdir(parents=True,exist_ok=True)
    original=Image.open(head_file).convert('RGBA').crop(PATCH_BOX)
    a=np.asarray(original).copy();mask=np.zeros(a.shape[:2],np.uint8)
    # Remove only the baked brown smile stroke, leaving face/eyes/hair untouched.
    ink=(a[:,:,0]<215)&(a[:,:,1]<175)&(a[:,:,2]<150)
    mask[5:26,3:41]=ink[5:26,3:41]*255
    mask=cv2.dilate(mask,np.ones((3,3),np.uint8))
    clean=cv2.inpaint(a[:,:,:3],mask,3,cv2.INPAINT_TELEA)
    feather=np.ones(a.shape[:2],np.float32)
    yy,xx=np.indices(feather.shape)
    edge=np.minimum.reduce([xx,yy,a.shape[1]-1-xx,a.shape[0]-1-yy])
    feather=np.clip(edge/3,0,1);alpha=np.rint(a[:,:,3]*feather).astype(np.uint8)
    clean_rgba=np.dstack([clean,alpha]);Image.fromarray(clean_rgba).save(output_dir/'mouth_clean_patch.png')
    files={};bounds={}
    for name,w,h in SHAPES:
        src=a.copy() if name=='closed' else np.dstack([clean,alpha])
        src[:,:,3]=alpha
        im=Image.fromarray(src).resize((src.shape[1]*4,src.shape[0]*4),Image.Resampling.BICUBIC)
        if name!='closed':
            dr=ImageDraw.Draw(im);cx,cy=CENTER
            box=tuple(round(v*4) for v in (cx-w/2,cy-h/2,cx+w/2,cy+h/2))
            dr.ellipse(box,fill=(108,67,67,255),outline=(150,88,70,255),width=5)
            # Soft tongue stays inside the opening, without a flashy teeth strip.
            tongue=Image.new('RGBA',im.size);td=ImageDraw.Draw(tongue)
            td.ellipse(tuple(round(v*4) for v in (cx-w*.32,cy+h*.07,cx+w*.32,cy+h*.43)),fill=(207,132,117,245))
            clip=Image.new('L',im.size);ImageDraw.Draw(clip).ellipse(box,fill=255)
            tongue.putalpha(Image.fromarray((np.asarray(tongue.getchannel('A')).astype(np.uint16)*np.asarray(clip)//255).astype(np.uint8)))
            im=Image.alpha_composite(im,tongue)
        im=im.resize((src.shape[1],src.shape[0]),Image.Resampling.LANCZOS)
        filename=output_dir/f'mouth_{name}.png';im.save(filename);files[name]=filename
        bounds[name]=[PATCH_BOX[0]+CENTER[0]-w/2,PATCH_BOX[1]+CENTER[1]-h/2,
                      PATCH_BOX[0]+CENTER[0]+w/2,PATCH_BOX[1]+CENTER[1]+h/2] if w else [233,312,265,325]
    metadata={'head_patch_box':list(PATCH_BOX),'global_patch_box':[v+7 for v in PATCH_BOX],
      'global_mouth_center':[PATCH_BOX[0]+CENTER[0]+7,PATCH_BOX[1]+CENTER[1]+7],
      'shape_bounds_head':bounds,'states':[x[0] for x in SHAPES],
      'thresholds':[0,.10,.30,.50,.74],'old_mouth_removed_only_for_open_states':True,
      'method':'Local original-skin patch, narrow baked-stroke mask; code-defined rounded mouth openings',
      'head_source':str(Path(head_file).name),'no_face_mesh_warp':True}
    (output_dir/'mouth_geometry.json').write_text(json.dumps(metadata,indent=2))
    return files,metadata

if __name__=='__main__':
    root=Path(__file__).resolve().parent
    create(root.parent/'assets/gumi/parts/head.png',root/'mouth_assets')
