def noise(meta,limit):
    newMeta=[]
    for each in meta:
        if each["meta"]["score"]>limit:
            newMeta.append(each)
    return newMeta
