import os

import Components

defaultDir = "ComponentPics"
if not os.path.exists(defaultDir):
    os.makedirs(defaultDir)

allAttributes = dir(Components)
componentNames = [attr for attr in allAttributes if not attr.startswith("__")]
componentNames.remove("ComponentBase")

componentList = []
for componentName in componentNames:
    ref = getattr(Components, componentName)
    if isinstance(ref, type):
        componentList.append(ref)
    else:
        print(f"Model Settings: The ref of {componentName} is not a type")

for ref in componentList:
    if hasattr(ref, "GetDiagram"):
        diagram = ref.GetDiagram()
        path = os.path.join(defaultDir, ref.__name__ + ".png")
        diagram.save(path)
