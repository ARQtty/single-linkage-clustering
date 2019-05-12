# Подключается в gui

def depthOfChildren(v, currDepth=0):
    lDepth = 0
    rDepth = 0

    if v.lChild:
        lDepth = max(depthOfChildren(v.lChild, currDepth)) + 1
    if v.rChild:
        rDepth = max(depthOfChildren(v.rChild, currDepth)) + 1

    return (lDepth, rDepth)

