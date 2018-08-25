"""FilenameSort is a utility to aid in "human-like" sorting of file names.

Normally using sort, ["file_1_10a.png","file_1_1a.png","file_1_5a.png"] would sort as:
["file_1_10a.png","file_1_1a.png","file_1_5a.png"]

Using the function getSortableList instead results in:
["file_1_1a.png","file_1_5a.png","file_1_10a.png"]

Which is more like what one would expect."""

from __future__ import absolute_import
from __future__ import print_function

__author__ = "David N. Mashburn <david.n.mashburn@gmail.com>"

import glob,copy,os
from time import time

# The two dinky little functions sort files according to human-based sorting...
# They avoid the usual sorting problem with non-0 buffered integers in names...:
# 0a,1a,10a,11a,12a,13a,14a,15a,16a,17a,18a,19a,2a,20a ...
# with this function sorts properly (like follows) instead:
# 0a,1a,2a,3a,4a,5a,6a,7a,8a,9a,10a,11a,12a,13a,14a,15a,16a,17a,18a,19a,20a ...
def getSortableList(s):
    '''Turns a string into a list where numbers and non-numbers are separated'''
    currentNumber=[]
    currentNonNumber=[]
    sortableList=[os.path.split(s)[0]]
    for i in os.path.splitext(os.path.split(s)[1])[0]:
        if i.isdigit():
            currentNumber.append(i)
            if currentNonNumber!=[]:
                sortableList.append(''.join(currentNonNumber))
                currentNonNumber=[]
        else:
            currentNonNumber.append(i)
            if currentNumber!=[]:
                sortableList.append(int(''.join(currentNumber)))
                currentNumber=[]
    if currentNumber!=[]:
        sortableList.append(int(''.join(currentNumber)))
    elif currentNonNumber!=[]:
        sortableList.append(''.join(currentNonNumber))
    sortableList.append(os.path.splitext(s)[1])
    return sortableList

def getSortedListOfFiles(d,globArg='*[!.txt]',exclude_dirs=True):
    files = glob.glob(os.path.join(d,globArg))
    
    files.sort(key=getSortableList)
    
    if exclude_dirs:
        files = [f for f in files if not os.path.isdir(f)]
    
    return files

def AreFilenamesNumericalIncrements(f1,f2):
    l1=getSortableList(f1)
    l2=getSortableList(f2)
    
    if len(l1)!=len(l2):
        return False
    
    for i in range(len(l1)):
        if not l1[i]==l2[i] and (not l1[i].__class__==int or not l2[i].__class__==int):
            return False
    
    return True

def getSortedListOfNumericalEquivalentFiles(f,d):
    sortedList=getSortedListOfFiles(d,globArg='*')
    for i in range(len(sortedList)-1,-1,-1):
        if not AreFilenamesNumericalIncrements(f,sortedList[i]):
            del sortedList[i]
    
    return sortedList

#########################################################################
## Some fancy list functions to deal with missing values in file lists ##
## only public functions are fillingMissingWithNone and                ##
## getSortedListOfFiles_fillingMissingWithNone                         ##
#########################################################################

def _NDListBuilder(val,shape):
    '''Utility function to build an empty (list-of...)-lists with n-dimensional shape'''
    if len(shape)>1:
        return [ _NDListBuilder(val,shape[1:]) for i in range(shape[0]) ]
    else:
        return [ val for i in range(shape[0]) ]

def _SetNDListValue(ndList,ndims,indexList, value):
    '''Set a value in the ndList, equivalent to ndList[indexList[0]][indexList[1]]... '''
    assert len(indexList)==ndims
    # Dig down into the nested lists:
    l = ndList
    for i in indexList[:-1]:
        l = l[i]
    # And in the bottom-most list, set the value:
    l[indexList[-1]] = value

def _flattenNDList(ndList,ndims):
    '''Flatten an ND-list in place; also returns list'''
    for i in range(ndims-1):
        ndList = [j for i in ndList for j in i]
    return ndList

def fillingMissingWithNone(sortedListOfFiles,startVal=0):
    '''Assumes that any time there is a numerical value, there should be a range of these in every sub-tree'''
    if sortedListOfFiles==[]:
        return []
    
    assert startVal in [0,1], 'startVal must be either 0 or 1!'
    
    split = list(map(getSortableList,sortedListOfFiles))
    splitT = list(zip(*split))
    ndims = len(splitT)
    maximums = [None for i in range(ndims)]
    variations = [None for i in range(ndims)]
    for i in range(ndims):
        if all([ isinstance(j,int) for j in splitT[i] ]):
            if startVal==1:
                assert not min(splitT[i])==0, "Shouldn't have value of 0 if counting from 1! Change startVal to 0!"
            variations[i] = list(range(startVal,splitT[i][-1]+1))
        else:
            variations[i] = sorted(set(splitT[i]))
    
    ndList = _NDListBuilder( None, shape = list(map(len,variations)) )
    
    for v in split:
        indexes = [ variations[i].index(v[i]) for i in range(ndims) ]
        value = os.path.join( v[0] , ''.join(map(str,v[1:])) )
        _SetNDListValue(ndList,ndims,indexes, value )

    return _flattenNDList(ndList,len(variations))

def getSortedListOfFiles_fillingMissingWithNone(d,globArg,startVal=0):
    '''Assumes that any time there is a numerical value, there should be a range of these in every sub-tree'''
    return fillingMissingWithNone( getSortedListOfFiles(d,globArg), startVal=startVal )

########################################################################
##                              Old                                   ##
########################################################################

def getSortedListOfFilesOld(d,globArg='*[!.txt]'):# old attempt at this using re... way too complicated...
    import re
    files = glob.glob(os.path.join(d,globArg))
    l=copy.deepcopy(files)

    start,end=0,-1
    # Find the first character that does not match in all strings
    done=False
    for i in range(len(l[0])):
        for f in l:
            if f[i]!=l[0][i]:
                start = i
                done=True
                break
        if done:
            break
    
    # Do the same from the end...
    done=False
    for i in range(len(l[0])-1,-1,-1):
        for f in l:
            if f[i]!=l[0][i]:
                end = i-len(l[0])
                done=True
                break
        if done:
            break
    
    # Find any non-numerical parts of the filename
    m=re.findall('\\D*',l[0][start:end])
    if m!=[]:
        print(m)
        for i in m:
            l[0].find()
    
    for i in range(len(l[0])-1,-1,-1):
        pass
    if not l[0].isdigit():
        pass
    
    l.sort( key = lambda x: float(x[start:end]) )
    
    return l

# These were stolen from VolumeGif...

# Comparison to avoid the problem of improper file name sorting.
# This was not sorting properly if files are like: GBR_0_0etc, GBR_1_0etc, ..., GBR_13_0etc, ...
# Because '_' has a lower priority than digits, so 13 comes in before 1!!!
# ...Could potentially also pad the z-values w/zeros
def cmp_fnames_A(f1,f2):
    if f1==f2:
        return 0
    s1=os.path.split(f1)[1].split('_')
    s2=os.path.split(f2)[1].split('_')
    maxDigits=max(len(s1[1]),len(s2[1]))
    s1a='0'*(maxDigits-len(s1[1]))+s1[1]+'_'+s1[2]
    s2a='0'*(maxDigits-len(s2[1]))+s2[1]+'_'+s2[2]
    return (s1a>s2a)*2-1

def cmp_fnames(f1,f2):
    if f1==f2:
        return 0
    return (os.path.getmtime(f1)>os.path.getmtime(f2))*2-1

