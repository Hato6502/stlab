#!/usr/bin/python
# coding: utf-8
import numpy as np
import pickle
import bpy
from mathutils import Vector

with open('bridge_z', 'rb') as f:
	stereo = pickle.load(f, encoding='latin-1');
with open('bridge_c', 'rb') as f:
	colormap = pickle.load(f, encoding='latin-1');

print('3D モデル生成中…')
xz = 0.01
yz = 0.01
zz = 0.00125
bpy.ops.object.delete()
verts = []
edges = []
faces = []
for y in range(stereo.shape[0]):
	for x in range(stereo.shape[1]):
		verts.append(Vector(((x-stereo.shape[1]/2.0)*xz, (y-stereo.shape[0]/2.0)*yz, stereo[y, x]*zz)))
	#print(str(int((y+1)/stereo.shape[0]*100.0))+'%')
i = 0
vci = []
for y in range(stereo.shape[0]-1):
	for x in range(stereo.shape[1]-1):
		faces.append([i, i+1, i+stereo.shape[1]])
		vci.extend([i, i+1, i+stereo.shape[1]])
		faces.append([i+1, i+stereo.shape[1], i+stereo.shape[1]+1])
		vci.extend([i+1, i+stereo.shape[1], i+stereo.shape[1]+1])
		i += 1
	i += 1
mesh = bpy.data.meshes.new(name='Mesh')
mesh.from_pydata(verts, edges, faces)
mesh.vertex_colors.new('col')
for idx, vc in enumerate(mesh.vertex_colors['col'].data):
	i = vci[idx]
	color = colormap[int(i/colormap.shape[1]), i%colormap.shape[1]]
	vc.color = [color[2]/255.0, color[1]/255.0, color[0]/255.0]
obj = bpy.data.objects.new('Object', mesh)
obj.location = (0, 0, 0)
bpy.context.scene.objects.link(obj)
obj.select=True
bpy.ops.export_mesh.stl(filepath = 'output.stl')

#print('レンダリング中…')
#bpy.ops.render.render()
#bpy.data.images['Render Result'].save_render(filepath = 'rendered.png')
