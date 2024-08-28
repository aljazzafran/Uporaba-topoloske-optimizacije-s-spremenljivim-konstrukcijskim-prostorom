#Podatki
sila = 20000 # [N] sila
velikost_KE = 10 # [mm] velikost KE
poves_max = 0.5 # [mm] maksimalni dovoljeni poves
napetost_max = 167 # [MPa] maksimalna dovoljena napetost

static = Model.Analyses[0]

# Material
material = Model.Geometry.GetChildren(DataModelObjectCategory.Body, True)[0]
material.Material = "Structural Steel"

#Simetrija
simetrija = Model.AddSymmetry()
sim_povrsina = simetrija.AddSymmetryRegion()
sim_povrsina.Location = ExtAPI.DataModel.GetObjectsByName("simetrija")[0]
sim_povrsina.SymmetryNormal = SymmetryNormalType.YAxis

sim_sila = sila / 2 # velikost sile se razpolovi zaradi simetrije

# Mreza KE
mreza = Model.Mesh
mreza.ElementSize = Quantity(velikost_KE, "mm")

# Robni pogoji
podpora = static.AddFixedSupport()
podpora.Location = ExtAPI.DataModel.GetObjectsByName("podpora")[0]

sila = static.AddForce()
sila.Location = ExtAPI.DataModel.GetObjectsByName("obremenitev")[0]
sila.DefineBy = LoadDefineBy.Components
sila.ZComponent.Output.SetDiscreteValue(0, Quantity(sim_sila, "N"))

# Rezultati
napetost = static.Solution.AddEquivalentStress()
deformacija = static.Solution.AddTotalDeformation()
deformacija_Z = static.Solution.AddDirectionalDeformation()
deformacija_Z.NormalOrientation = NormalOrientationType.ZAxis
#static.Solution.Solve(True) # racunanje staticne analize

# Topoloska optimizacija
top_opt = Model.AddTopologyOptimizationAnalysis()
top_opt.TransferDataFrom(static)
resp_con = top_opt.GetChildren(DataModelObjectCategory.ResponseConstraint, True)[0]
resp_con.Delete()

# Ciljna funkcija - minimiziramo maso
objective = top_opt.GetChildren(DataModelObjectCategory.Objective, True)[0]
objective.Worksheet.SetObjectiveType(0, ObjectiveType.MinimizeMass) 

# Omejitev za najvecji dovoljeni poves
top_opt.AddDisplacementConstraint()
max_poves = top_opt.GetChildren(DataModelObjectCategory.DisplacementConstraint, True)[0]
max_poves.Location = ExtAPI.DataModel.GetObjectsByName("obremenitev")[0]
max_poves.ZComponentMax.Output.DefinitionType = VariableDefinitionType.Discrete
max_poves.ZComponentMax.Output.SetDiscreteValue(0, Quantity(poves_max, "mm"))

# Omejitev za najvecjo dovoljeno napetost
top_opt.AddGlobalVonMisesStressConstraint()
max_napetost = top_opt.GetChildren(DataModelObjectCategory.GlobalVonMisesStressConstraint, True)[0]
max_napetost.Maximum.Output.SetDiscreteValue(0, Quantity(napetost_max, "MPa"))

top_opt.Solution.Solve(True) # racunanje topoloske optimizacije