import os
import Image
import time

def compose(subs,name,target_dimen,tile_dimen):
    """
    compose the final mosaic

    arguments:
    subs--hash storing best matches
    name--the name of the output
    target_dimen--the output dimension
    tile_dimen--tile image dimension
    """

    #time measure starts
    start=time.time()
    #print 'start composing...'

    #for loop use
    width,height=target_dimen
    tile_width,tile_height=tile_dimen
    width_times=width/tile_width
    height_times=height/tile_height

    #create a canvas
    layer=Image.new("RGB",(width,height))

    #sort the hash by tile name
    O=sorted(subs.items(),key=lambda x:x[0])

    #start pasting
    c=0
    for i in range(0,height_times):
        for j in range(0,width_times):
            im=Image.open(O[c][1])
            c+=1
            layer.paste(im,(j*tile_width,i*tile_height,\
                        (j+1)*tile_width,(i+1)*tile_height))
    #name the output
    layer.save(name)

    #time measure ends
    #print "Total time for composing is: "\
    #      +str(time.time()-start)+"seconds."
