# Podatki
a = 500 # dolzina
b = 150 # visina
c = 100 # sirina

c_sim = c/2 # upostevanje simetrije
d = a - 100 # obremenjena povrsina

ClearAll()

# Skica
ravnina = Plane.PlaneZX
ViewHelper.SetSketchPlane(ravnina)
tocka_1 = Point2D.Create(MM(0),MM(0))
tocka_2 = Point2D.Create(MM(b),MM(0))
tocka_3 = Point2D.Create(MM(b),MM(a))
SketchRectangle.Create(tocka_1, tocka_2, tocka_3)
mode = InteractionMode.Solid
ViewHelper.SetViewMode(mode)

# Extrude
sel = FaceSelection.Create(GetRootPart().Bodies[0].Faces[0])
options = ExtrudeFaceOptions()
options.ExtrudeType = ExtrudeType.Add
ExtrudeFaces.Execute(sel, MM(c_sim), options)

# Obremenjena povrsina
ravnina = Plane.PlaneXY
ViewHelper.SetSketchPlane(ravnina)
tocka_1 = Point2D.Create(MM(0),MM(0))
tocka_2 = Point2D.Create(MM(d),MM(0))
tocka_3 = Point2D.Create(MM(d),MM(c_sim))
SketchRectangle.Create(tocka_1, tocka_2, tocka_3)
mode = InteractionMode.Solid
ViewHelper.SetViewMode(mode)

# Skupine za robne pogoje
sel = FaceSelection.Create(GetRootPart().Bodies[0].Faces[5])
sel.CreateAGroup("obremenitev")
sel = FaceSelection.Create(GetRootPart().Bodies[0].Faces[2])
sel.CreateAGroup("podpora")
sel = FaceSelection.Create(GetRootPart().Bodies[0].Faces[4])
sel.CreateAGroup("simetrija")