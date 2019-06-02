#-*- coding: utf-8 -*-
from Scripts.object import loadOBJ
from Scripts.Tex import Texturas
from Scripts.Bitmap import Bitmap
from math import cos, sin


class SR(object):

	def glInit(self):
		
		self.__bmmp = Bitmap(0,0)
		self.__InSize = (0,0)
		self.__FinalSize = (0,0)
		self.__color = self.__bmmp.SetColor(0,191,255)
		self.__filename = "output.bmp"
		self.__OBBJ = None
		self.__FullFill = None

	def setbmmp(self, bmp):
		self.__bmmp = bmp

	def glCreateWindow(self, width, height):
		
		self.__bmmp = Bitmap(width, height)
		self.__FinalSize = (width, height)

	def glViewPort(self, x, y, width, height):
		
		self.__InSize = (x, y)
		self.__FinalSize = (width,height)

	def glClear(self):
		
		self.__bmmp.clear()

	def glClearColor(self, r, g, b):
		
		self.__bmmp.clear(int(255*r), int(255*g), int(255*b))

	def glVertex(self, x, y):
		
		viewPortX = int(self.__FinalSize[0] * (x+1) * (1/2) + self.__InSize[0])
		viewPortY = int(self.__FinalSize[1] * (y+1) * (1/2) + self.__InSize[1])
		self.__bmmp.point(viewPortX, viewPortY, self.__color)

	def glVertexV4(self, x, y):
		
		viewPortX = int(self.__FinalSize[0] * (x+1) * (1/2) + self.__InSize[0])
		viewPortY = int(self.__FinalSize[1] * (y+1) * (1/2) + self.__InSize[1])
		self.__bmmp.point(viewPortX, viewPortY, self.__color)
		self.__bmmp.point(viewPortX, viewPortY+1, self.__color)
		self.__bmmp.point(viewPortX+1, viewPortY, self.__color)
		self.__bmmp.point(viewPortX+1, viewPortY+1, self.__color)



	def  glColor(self, r, g, b):
		
		self.__color = self.__bmmp.SetColor(int(255*r), int(255*g), int(255*b))
		return self.__bmmp.SetColor(int(255*r), int(255*g), int(255*b))

	def glFinish(self):
		
		self.__bmmp.write(self.__filename)

	def glLine(self, xo, yo, xf, yf):
	
		x1 = int(self.__FinalSize[0] * (xo+1) * (1/2) + self.__InSize[0])
		y1 = int(self.__FinalSize[1] * (yo+1) * (1/2) + self.__InSize[1])
		x2 = int(self.__FinalSize[0] * (xf+1) * (1/2) + self.__InSize[0])
		y2 = int(self.__FinalSize[1] * (yf+1) * (1/2) + self.__InSize[1])
		dy = abs(y2 - y1)
		dx = abs(x2 - x1)
		steep = dy > dx
		if steep:
			x1, y1 = y1, x1
			x2, y2 = y2, x2
		if (x1 > x2):
			x1, x2 = x2, x1
			y1, y2 = y2, y1
		dy = abs(y2 - y1)
		dx = abs(x2 - x1)
		offset = 0
		threshold = dx
		y = y1
		for x in range(x1, x2 + 1):
			if steep:
				self.__bmmp.point(y, x, self.__color)
			else:
				self.__bmmp.point(x, y, self.__color)

			offset += dy * 2
			if offset >= threshold:
				y +=1 if y1 < y2 else -1
				threshold += 2 * dx
	
	def setFileName(self, filename):
	
		self.__filename = filename

	def loadOBJ(self, filename, translate=(0, 0, 0), scale=(1, 1, 1), fill=True, textured=None, rotate=(0, 0, 0), shader=None):
		
		self.modelMatrix(translate, scale, rotate)
		self.__OBBJ = loadOBJ(filename)
		self.__OBBJ.cargo()
		light = self.norm((0,0,1))
		faces = self.__OBBJ.facces()
		vertex = self.__OBBJ.Verticess()
		materials = self.__OBBJ.Matts()
		tvertex = self.__OBBJ.XYTex()
		nvertex = self.__OBBJ.Normalist()
		matFaces = self.__OBBJ.MTLF()
		self.__FullFill = Texturas(textured)

		

		if materials:
			for mats in matFaces:
				start, stop = mats[0]
				color = materials[mats[1]].difuseColor
				for index in range(start, stop):
					face = faces[index]
					vcount = len(face)

					if vcount == 3:
						f1 = face[0][0] - 1
						f2 = face[1][0] - 1
						f3 = face[2][0] - 1

						a = self.transform(vertex[f1])
						b = self.transform(vertex[f2])
						c = self.transform(vertex[f3])

						if shader:
							t1 = face[0][1] - 1
							t2 = face[1][1] - 1
							t3 = face[2][1] - 1
							nA = nvertex[t1]
							nB = nvertex[t2]
							nC = nvertex[t3]
							self.triangle(a, b, c, baseColor=color, shader=shader, normals=(nA, nB, nC))
						else:
							normal = self.norm(self.cross(self.sub(b,a), self.sub(c,a)))
							intensity = self.dot(normal, light)

							if not self.__FullFill.HasTexture():
								if intensity < 0:
									continue
								self.triangle(a, b, c,color=self.glColor(color[0]*intensity, color[1]*intensity, color[2]*intensity))

		else:
			
			for face in faces:
				vcount = len(face)

				if vcount == 3:
					f1 = face[0][0] - 1
					f2 = face[1][0] - 1
					f3 = face[2][0] - 1

					a = self.transform(vertex[f1])
					b = self.transform(vertex[f2])
					c = self.transform(vertex[f3])

					if shader:
						nA = nvertex[f1]
						nB = nvertex[f2]
						nC = nvertex[f3]
						self.triangle(a, b, c, baseColor=color, shader=shader, normals=(nA, nB, nC))
					else:

						normal = self.norm(self.cross(self.sub(b,a), self.sub(c,a)))
						intensity = self.dot(normal, light)

						if not self.__FullFill.isTextured():
							if intensity < 0:
								continue
							self.triangle(a, b, c,color=self.glColor(intensity, intensity, intensity))
						else:
							if self.__FullFill.isTextured():
								t1 = face[0][-1] - 1
								t2 = face[1][-1] - 1
								t3 = face[2][-1] - 1
								tA = tvertex[t1]
								tB = tvertex[t2]
								tC = tvertex[t3]
								self.triangle(a, b, c, texture=self.__FullFill.isTextured(), texture_coords=(tA, tB, tC), intensity=intensity)
				else:
					f1 = face[0][0] - 1
					f2 = face[1][0] - 1
					f3 = face[2][0] - 1
					f4 = face[3][0] - 1

					vertexList = [
						self.transform(vertex[f1]),
						self.transform(vertex[f2]),
						self.transform(vertex[f3]),
						self.transform(vertex[f4])
					]
					normal = self.norm(self.cross(self.sub(vertexList[0], vertexList[1]), self.sub(vertexList[1], vertexList[2]))) 
					intensity = self.dot(normal, light)
					A, B, C, D = vertexList
					if not textured:
						if intensity < 0:
							continue
						self.triangle(A, B, C, color=self.glColor(intensity, intensity, intensity))
						self.triangle(A, C, D, color=self.glColor(intensity, intensity, intensity))
					else:
						if self.__FullFill.isTextured():
							t1 = face[0][-1] - 1
							t2 = face[1][-1] - 1
							t3 = face[2][-1] - 1
							t4 = face[3][-1] - 1
							tA = tvertex[t1]
							tB = tvertex[t2]
							tC = tvertex[t3]
							tD = tvertex[t4]
							self.triangle(A, B, C, texture=self.__FullFill.isTextured(), texture_coords=(tA, tB, tC), intensity=intensity)
							self.triangle(A, C, D, texture=self.__FullFill.isTextured(), texture_coords=(tA, tC, tD), intensity=intensity)


	def triangle(self, A, B, C, color=None, texture=None, texture_coords=(), intensity=1, normals=None, shader=None, baseColor=(1,1,1)):
		
		bbox_min, bbox_max = self.bbox(A, B, C)

		for x in range(bbox_min[0], bbox_max[0] + 1):
			for y in range(bbox_min[1], bbox_max[1] + 1):
				w, v, u = self.barycentric(A, B, C, x, y)
				if w < 0 or v < 0 or u < 0:
					continue
				if texture:
					tA, tB, tC = texture_coords
					tx = tA[0] * w + tB[0] * v + tC[0] * u
					ty = tA[1] * w + tB[1] * v + tC[1] * u
					color = self.__FullFill.getColor(tx, ty, intensity)
				elif shader:
					color = shader(self, bary=(w,u,v), Vnormals=normals, baseColor=baseColor)
				z = A[2] * w + B[2] * v + C[2] * u
				if x<0 or y<0:
					continue
				if z > self.__bmmp.collectZaxis(x,y):
					self.__bmmp.point(x, y, color)
					self.__bmmp.placeZaxis(x,y,z)


	def bbox(self, *vertexList):
		
		xs = [vertex[0] for vertex in vertexList]
		ys = [vertex[1] for vertex in vertexList]
		xs.sort()
		ys.sort()
		return (xs[0], ys[0]), (xs[-1], ys[-1])

	def load(self, filename, translate=(0, 0, 0), scale=(1, 1, 1), fill=True, textured=None, rotate=(0, 0, 0)):
		
		self.modelMatrix(translate, scale, rotate)
		self.__OBBJ = OBJ(filename)
		self.__OBBJ.load()
		vertex = self.__OBBJ.Verticess()
		faces = self.__OBBJ.facces()
		nvertex = self.__OBBJ.Normalist()
		materials = self.__OBBJ.Matts()
		tvertex = self.__OBBJ.XYTex()
		light = (0,0,1)
		
		if materials and not textured:
			matIndex = self.__OBBJ.MTLF()
			for mat in matIndex:
				difuseColor = materials[mat[1]].difuseColor
				for i in range(mat[0][0], mat[0][1]):
					cooList = []
					textCoo = []
					for face in faces[i]:
						coo = ((vertex[face[0]-1][0] + translate[0]) * scale[0], (vertex[face[0]-1][1] + translate[1]) * scale[1], (vertex[face[0]-1][2] + translate[2]) * scale[2])
						cooList.append(coo)
					if fill:
						inten = self.dot(nvertex[face[1]-1], light)
						if inten < 0:
							continue
						self.glFilledPolygon(cooList, color=(inten*difuseColor[0],inten*difuseColor[1],inten*difuseColor[2]))
					else:
						self.glPolygon(cooList)
		elif textured and not materials:
			for face in faces:
				cooList = []
				textCoo = []
				for vertexN in face:
					coo = ((vertex[vertexN[0]-1][0] + translate[0]) * scale[0], (vertex[vertexN[0]-1][1] + translate[1]) * scale[1], (vertex[vertexN[0]-1][2] + translate[2]) * scale[2])
					cooList.append(coo)
					if len(vertexN) > 2:
						text = ((tvertex[vertexN[2]-1][0]+ translate[0]) * scale[0], (tvertex[vertexN[2]-1][1]+ translate[1]) * scale[1])
						textCoo.append(text)
				if fill:
					inten = self.dot(nvertex[vertexN[1]-1], light)
					if inten < 0:
						continue
					self.glFilledPolygon(cooList, intensity=inten, texture=textured, textureCoords=textCoo)
				else:
					self.glPolygon(cooList)
				cooList = []
		else:
			for face in faces:
				cooList = []
				textCoo = []
				for vertexN in face:
					coo = vertex[vertexN[0]-1] #self.transform(vertex[vertexN[0]-1])
					cooList.append(coo)
				if fill:
					inten = self.dot(nvertex[vertexN[1]-1], light)
					if inten < 0:
						continue
					self.glFilledPolygon(cooList, color=(inten,inten,inten))
				else:
					self.glPolygon(cooList)
				cooList = []

	def glRenderTextureGrid(self, filename=None, newfile=True, translate=(0, 0), scale=(1, 1)):
		
		if self.__OBBJ:

			faces = self.__OBBJ.facces()
			materials = self.__OBBJ.Matts()
			tvertex = self.__OBBJ.XYTex()

			if newfile and filename:
				canvas = SR()
				canvas.glInit()
				canvas.glCreateWindow(self.__bmmp.Wd, self.__bmmp.Hd)
				canvas.glViewPort(self.__InSize[0], self.__InSize[1], self.__FinalSize[0], self.__FinalSize[1])
				canvas.setFileName(filename)
			else:
				canvas = self

			if materials:
				matIndex = self.__OBBJ.MTLF()
				for mat in matIndex:
					difuseColor = materials[mat[1]].difuseColor
					for i in range(mat[0][0], mat[0][1]):
						textCoo = []
						for face in faces[i]:
							if len(face) > 2:
								text = ((tvertex[face[2]-1][0]+ translate[0]) * scale[0], (tvertex[face[2]-1][1]+ translate[1]) * scale[1], 0)
								textCoo.append(text)
							if len(textCoo)>2:
								canvas.glPolygon(textCoo)
			else:
				for face in faces:
					textCoo = []
					for vertexN in face:
						if len(vertexN) > 2:
							text = ((tvertex[vertexN[2]-1][0]+ translate[0]) * scale[0], (tvertex[vertexN[2]-1][1]+ translate[1]) * scale[1],0)
							textCoo.append(text)
						if len(textCoo)>2:
							canvas.glPolygon(textCoo)
			return canvas


	def glPolygon(self, vertexList):
		
		for i in range(len(vertexList)):
			if i == len(vertexList)-1:
				st = vertexList[i]
				fi = vertexList[0]
			else:
				st = vertexList[i]
				fi = vertexList[i+1]
			self.glLine(st[0], st[1], fi[0], fi[1])

	def glFilledPolygon(self, vertexList, color=None, texture=None, intensity=1, textureCoords = (), zVal=True):
		inten = intensity
		if not texture:
			color = self.__color if color == None else self.__bmmp.SetColor(int(255*color[0]), int(255*color[1]), int(255*color[2]))
		else:
			if self.__FullFill == None:
				text = Texture(texture)
				self.__FullFill = text
			else:
				text = self.__FullFill
		startX = (sorted(vertexList, key=lambda tup: tup[0])[0][0])
		finishX = (sorted(vertexList, key=lambda tup: tup[0], reverse = True)[0][0])

		startY = (sorted(vertexList, key=lambda tup: tup[1])[0][1])
		finishY = (sorted(vertexList, key=lambda tup: tup[1], reverse=True)[0][1])
		
		startX = int(self.__FinalSize[0] * (startX+1) * (1/2) + self.__InSize[0])
		finishX = int(self.__FinalSize[0] * (finishX+1) * (1/2) + self.__InSize[0])

		startY = int(self.__FinalSize[0] * (startY+1) * (1/2) + self.__InSize[0])
		finishY = int(self.__FinalSize[0] * (finishY+1) * (1/2) + self.__InSize[0])
		for x in range(startX, finishX+1):
			for y in range(startY, finishY+1):
				isInside = self.glPointInPolygon(self.norX(x), self.norY(y), vertexList)
				if isInside:
					if texture:
						A = (self.norInvX(vertexList[0][0]), self.norInvX(vertexList[0][1]))
						B = (self.norInvX(vertexList[1][0]), self.norInvX(vertexList[1][1]))
						C = (self.norInvX(vertexList[2][0]), self.norInvX(vertexList[2][1]))
						w,v,u = self.barycentric(A, B, C, x, y)
						A = textureCoords[0]
						B = textureCoords[1]
						C = textureCoords[2]
						tx = A[0] * w + B[0] * v +  C[0] * u
						ty = A[1] * w + B[1] * v + C[1] * u
						color = text.getColor(tx, ty, intensity=inten)
					z = self.glPLaneZ(vertexList, x, y)
					if z > self.__bmmp.collectZaxis(x,y):
						self.__bmmp.point(x, y, color)
						self.__bmmp.placeZaxis(x,y,z)

	def barycentric(self, A, B, C, x, y):
		
		v1 = (C[0]-A[0], B[0]-A[0],A[0]-x)
		v2 = (C[1]-A[1], B[1]-A[1],A[1]-y)		
		bary = self.cross(v1, v2)	
		if abs(bary[2])<1:
			return -1,-1,-1

		return ( 1 - (bary[0] + bary[1]) / bary[2], bary[1] / bary[2], bary[0] / bary[2])
	
	def norX(self, x):
		
		norX = ((2*x)/self.__FinalSize[0]) - self.__InSize[0] - 1
		return norX

	def norY(self, y):
		
		norY = ((2*y)/self.__FinalSize[1]) - self.__InSize[1] - 1
		return norY

	def norInvX(self, x):
		
		norX = int(self.__FinalSize[0] * (x+1) * (1/2) + self.__InSize[0])
		return norX

	def norInvY(self, y):
		
		norY = int(self.__FinalSize[0] * (y+1) * (1/2) + self.__InSize[0])
		return norY

	def norm(self, v0):
		v = self.length(v0)
		if not v:
			return [0,0,0]
		return [v0[0]/v, v0[1]/v, v0[2]/v]

	def length(self, v0):
		return (v0[0]**2 + v0[1]**2 + v0[2]**2)**0.5

	def glPointInPolygon(self,x, y, vertexList):
		
		counter = 0
		p1 = vertexList[0]
		n = len(vertexList)
		for i in range(n+1):
			p2 = vertexList[i % n]
			if(y > min(p1[1], p2[1])):
				if(y <= max(p1[1], p2[1])):
					if(p1[1] != p2[1]):
						xinters = (y-p1[1])*(p2[0]-p1[0])/(p2[1]-p1[1])+p1[0]
						if(p1[0] == p2[0] or x <= xinters):
							counter += 1
			p1 = p2
		if(counter % 2 == 0):
			return False
		else:
			return True
			
	def dot(self, v0, v1):
		
		return v0[0] * v1[0] + v0[1] * v1[1] + v0[2] * v1[2]

	def cross(self, v0, v1):
		
		return [v0[1] * v1[2] - v0[2] * v1[1], v0[2] * v1[0] - v0[0] * v1[2], v0[0] * v1[1] - v0[1] * v1[0]]

	def vector(self, p, q):
		
		return [q[0]-p[0], q[1]-p[1], q[2]-p[2]]

	def sub(self, v0, v1):
		return [v0[0] - v1[0], v0[1] - v1[1], v0[2] - v1[2]]

	def glPLaneZ(self, vertexList, x,y):
		pq = self.vector(vertexList[0], vertexList[1])
		pr = self.vector(vertexList[0], vertexList[2])
		normal = self.cross(pq, pr)
		if normal[2]:
			z = ((normal[0]*(x-vertexList[0][0])) + (normal[1]*(y-vertexList[0][1])) - (normal[2]*vertexList[0][2]))/(-normal[2])
			return z
		else:
			return -float("inf")

	def glRenderZBuffer(self, filename = None):
		if filename == None:
			filename = self.__filename.split(".")[0] + "ZBuffer.bmp"
		self.__bmmp.write(filename, zbuffer = True)

	def matMult(self, m1,m2):
		if len(m1[0]) == len(m2):
			filas1 = len(m1)
			col1 = len(m1[0])
			filas2 = len(m2)
			col2 = len(m2[0])
			matResult = []
			for i in range(filas1):
				matResult.append([0] * col2)
			for i in range(filas1):
				for j in range(col2):
					for k in range(col1):
						matResult[i][j] = m1[i][k] * m2[k][j]
			return matResult
		else:
			print("error")
			return 0

	def modelMatrix(self, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
		
		translation_matrix = Matrix([[1, 0, 0, translate[0]],[0, 1, 0, translate[1]],[0, 0, 1, translate[2]],[0, 0, 0, 1],])
		a = rotate[0]
		rotation_matrix_x = Matrix([[1, 0, 0, 0],[0, cos(a), -sin(a), 0],[0, sin(a),  cos(a), 0],[0, 0, 0, 1]])
		a = rotate[1]
		rotation_matrix_y = Matrix([[cos(a), 0,  sin(a), 0],[     0, 1,       0, 0],[-sin(a), 0,  cos(a), 0],[     0, 0,       0, 1]])
		a = rotate[2]
		rotation_matrix_z = Matrix([[cos(a), -sin(a), 0, 0],[sin(a),  cos(a), 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]])
		rotation_matrix = rotation_matrix_x * rotation_matrix_y * rotation_matrix_z
		scale_matrix = Matrix([[scale[0], 0, 0, 0],[0, scale[1], 0, 0],[0, 0, scale[2], 0],[0, 0, 0, 1],])
		self.Model = translation_matrix * rotation_matrix * scale_matrix

	def viewMatrix(self, x, y, z, center):
		m = Matrix([[x[0], x[1], x[2],  0],[y[0], y[1], y[2], 0],[z[0], z[1], z[2], 0],[0,0,0,1]])
		o = Matrix([[1, 0, 0, -center[0]],[0, 1, 0, -center[1]],[0, 0, 1, -center[2]],[0, 0, 0, 1]])
		self.View = m * o

	def projectionMatrix(self, coeff):
		
		self.Projection = Matrix([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, 0],[0, 0, coeff, 1]])

	def viewportMatrix(self, x=0, y =0):
		
		self.Viewport =  Matrix([[self.__bmmp.Wd/2, 0, 0, x + self.__bmmp.Wd/2],[0, self.__bmmp.Hd/2, 0, y + self.__bmmp.Hd/2],[0, 0, 128, 128],[0, 0, 0, 1]])

	def lookAt(self, eye, center, up):
		
		z = self.norm(self.sub(eye, center))
		x = self.norm(self.cross(up, z))
		y = self.norm(self.cross(z,x))
		self.viewMatrix(x, y, z, center)
		self.projectionMatrix(-1/self.length(self.sub(eye, center)))
		self.viewportMatrix()

	def transform(self, vertex):
		agv = Matrix([[vertex[0]],[vertex[1]],[vertex[2]],[1]])
		transformed_vertex = self.Viewport * self.Projection * self.View * self.Model * agv
		transformed_vertex = transformed_vertex.tolist()
		tra = [round(transformed_vertex[0][0]/transformed_vertex[3][0]), round(transformed_vertex[1][0]/transformed_vertex[3][0]), round(transformed_vertex[2][0]/transformed_vertex[3][0])]
		return tra

class Matrix(object):
	
	def __init__(self, data):
		
		self.data = data
		self.row = len(data)
		self.col = len(data[0])

	def __mul__(self, m2):
		
		result = []
		for i in range(self.row):
			result.append([])
			for j in range(m2.col):
				result[-1].append(0)

		for i in range(self.row):
			for j in range(m2.col):
				for k in range(m2.row):
					result[i][j] += self.data[i][k] * m2.data[k][j]

		return Matrix(result)

	def tolist(self):
		
		return self.data
