def depthOfChildren(v, currDepth=0):
    lDepth = 0
    rDepth = 0

    if v.lChild:
        lDepth = max(depthOfChildren(v.lChild, currDepth)) + 1
    if v.rChild:
        rDepth = max(depthOfChildren(v.rChild, currDepth)) + 1

    return (lDepth, rDepth)



def depthOfNode(searchV, treeV):

    if searchV == treeV:
        return 0
    
    else:
        if treeV.lChild:
            depth = depthOfNode(searchV, treeV.lChild)
            if depth != None: return depth+1
            
        if treeV.rChild:
            depth = depthOfNode(searchV, treeV.rChild)
            if depth != None: return depth+1
        
    print("Узел ", searchV, " не найден")
    return None