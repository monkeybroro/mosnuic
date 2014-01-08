import Image,os,sys,time,shutil,ImageStat
        
def split(img,tile_dimen,dic,target_rgb):
    """
    crop the target image into pieces due to the tile dimension
    and compute average color for each one

    arguments:
        img--target image path
        tile_dimen--tile image dimension
        dic--hash to store median color for pieces
        target_rgb--hash to store the average color for pieces

    crop every pixel from left to right, from top to down        
    """
    #measure starts 
    start=time.time()
    #print 'start spliting...'

    #get sizes
    image=Image.open(img)
    width,height=image.size
    tile_width,tile_height=tile_dimen

    #cropping size
    width_times=width/tile_width
    height_times=height/tile_height
    
    #variable for naming
    count=0
    total=width_times*height_times
    length=len(str(total))
    
    #cropping
    canon = '.tiff'
    for i in range(0,height_times):
        for j in range(0,width_times):
            count+=1
            box=(j*tile_width,i*tile_height,\
                 (j+1)*tile_width,(i+1)*tile_height)
            part=image.crop(box)
            if not part.mode == 'RGBA':
                part=part.convert('RGBA')
            c=str(count)
            name='0'*(length-len(c))+c+canon
            dic[name]=ImageStat.Stat(part.convert('L')).median[0]

            h = part.histogram()
            r=h[0:256]
            g=h[256:256*2]
            b=h[256*2:256*3]
            
            target_rgb[name] = (\
                sum( i*w for i,w in enumerate(r))/float(sum(r)),\
                sum( i*w for i,w in enumerate(g))/float(sum(g)),\
                sum( i*w for i,w in enumerate(b))/float(sum(b)))
      
    #measure ends
    #print "Total time for splitting is: "\
    #      +str(time.time()-start)+" seconds."

