import os,time

def compare(tile_rgb,target_rgb,repeat,brightness,bri,subs):
    """
    find the best matches for all target image pieces
    from database using binary search

    arguments:
    tile_rgb -- hash storing tile average color
    target_rgb -- hash storing target piece average color
    repeat -- maximum repeat time allowed
    brightness -- median color of target image
    bri -- hash storing median color of each piece
    subs -- output hash storing best match 
    """
    
    #time measure starts
    start=time.time()
    #print 'start comparing...'

    K=20
    
    #hash storing image path to root-mean-square
    dic={}
    #array storing sorted root-mean-square for binary search
    arr=[]
    #hash storing image path to repeated times
    repeated_times={}

    #initialize dic and repeated_times hash  
    for line in tile_rgb.items():
        line_rmse = rmse(line[1])
        dic[line[0]]=line_rmse
        repeated_times[line[0]]=1

    #make tile binary-searchable       
    L=sorted(dic.items(),key=lambda x:x[1])
    arr=map((lambda x:x[1]),L)

    #by order of distance to median color        
    B=sorted(bri.items(),key=lambda x:abs(x[1]-brightness))
    
    #binary searching...
    for line in B:
        timg=int(line[0].split('.')[0])
        trmse=rmse(target_rgb[line[0]])
        while(1):
            found=bi_search(arr,trmse)
            if (found-K/2) > 0:
                b=found-K/2
            else:
                b=0
            if (found+(K-K/2)) > (len(L)-1):
                e=len(L)-1
            else:
                e=found+(K-K/2)
            k_dis=-1
            j=0
            for x in range(b,e):
                dis=((tile_rgb[L[x][0]][0]-target_rgb[line[0]][0])**2\
                     +(tile_rgb[L[x][0]][1]-target_rgb[line[0]][1])**2\
                     +(tile_rgb[L[x][0]][2]-target_rgb[line[0]][2])**2)**0.5
                if k_dis==-1 or dis<k_dis:
                    k_dis=dis
                    k_found=b+j
                j+=1
            if repeated_times[L[k_found][0]] > repeat:
                arr.pop(k_found)
                L.pop(k_found)
            else:
                repeated_times[L[k_found][0]] += 1
                break
        subs[timg] = L[k_found][0]
        
    #time measure ends
    #print 'Total time for comparing is: '\
    #      +str(time.time()-start)+' seconds.'
    
def rmse((r,g,b)):
    """
    return root-mean-square of red,green,black value tuple

    arguments:
    r,g,b--red,green,black value
    """
    return ((r*r+g*g+b*b)/3.0)**0.5

def bi_search(arr,x):
    """
    binary search closest item to x from arr

    arguments:
    arr--database from which to search
    x--element which to search
    """
    
    maxi=len(arr)-1
    mini=0
    while mini<=maxi:
        mid=(maxi+mini)/2
        if x==arr[mid]:
            return mid
        elif x>arr[mid]:
            mini=mid+1
        else:
            maxi=mid-1
    if maxi==len(arr)-1:
        return maxi
    else:
        return mini
            
    
