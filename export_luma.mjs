import fs from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {GLTFExporter} from 'three/addons/exporters/GLTFExporter.js';
import {FontLoader} from 'three/addons/loaders/FontLoader.js';
import {TextGeometry} from 'three/addons/geometries/TextGeometry.js';
globalThis.FileReader=class{async readAsArrayBuffer(blob){this.result=await blob.arrayBuffer();this.onloadend?.()}async readAsDataURL(blob){this.result='data:'+blob.type+';base64,'+Buffer.from(await blob.arrayBuffer()).toString('base64');this.onloadend?.()}};
const raw=await fs.readFile('luma-base.glb');
const gltf=await new Promise((resolve,reject)=>new GLTFLoader().parse(raw.buffer.slice(raw.byteOffset,raw.byteOffset+raw.byteLength),'',resolve,reject));
const data=JSON.parse(await fs.readFile('luma-layout.json','utf8'));
const font=new FontLoader().parse(JSON.parse(await fs.readFile('assets/helvetiker_regular.typeface.json','utf8')));
const architecturalScene=gltf.scene;architecturalScene.name='EDITABLE ARCHITECTURE';architecturalScene.scale.z=-1;const root=new THREE.Group();root.name='LUMA GALLERIA';root.add(architecturalScene);const signage=new THREE.Group();signage.name='SIGNAGE';signage.userData.category='signage';root.add(signage);
const mat=new THREE.MeshStandardMaterial({color:0xe5cf9c,roughness:.45,metalness:.35});mat.name='Embossed bronze-gold letters';
for(const s of data.signs){
 const geo=new TextGeometry(s.text,{font,size:1,depth:.015,curveSegments:2,bevelEnabled:false});geo.computeBoundingBox();const span=geo.boundingBox.max.x-geo.boundingBox.min.x;const scale=Math.min(s.width/span,s.text==='LUMA GALLERIA'?1.08:.46);geo.translate(-span/2,0,0);const mesh=new THREE.Mesh(geo,mat);mesh.name=s.text+' / dimensional lettering';mesh.scale.setScalar(scale);mesh.position.set(s.position[0],s.position[1],-s.position[2]);mesh.rotation.y=Math.PI-s.rotation;mesh.userData.category=s.position[2]<0?'exterior_signage':'signage';signage.add(mesh);
}
root.userData={project:'LUMA GALLERIA',units:'metres',designStatus:data.design_status};
const out=await new GLTFExporter().parseAsync(root,{binary:true,onlyVisible:false});await fs.writeFile('luma-galleria.glb',Buffer.from(out));
const bounds=new THREE.Box3().setFromObject(root);const categories={};let meshes=0;root.traverse(o=>{if(o.isMesh){meshes++;const c=o.userData.category;categories[c]=(categories[c]||0)+1;}});
await fs.writeFile('luma-export-validation.json',JSON.stringify({meshCount:meshes,categories,boundsMin:bounds.min.toArray(),boundsMax:bounds.max.toArray(),glbBytes:out.byteLength,textMeshes:signage.children.length,units:'metres'},null,2));
console.log(JSON.stringify({meshCount:meshes,glbBytes:out.byteLength,textMeshes:signage.children.length,bounds:bounds.getSize(new THREE.Vector3()).toArray()}));
