import Image
import sys,os,time

def analyze(tiles,tile_rgb):
    """
    calculate average colors for tiles

    arguments:
    tiles--folder path containing images to be calculated
    tile_rgb-- hash to store output
    """

    #time measure starts
    start=time.time()
    #print 'start analyzing...'

    #calculating
    for tile in sorted(os.listdir(tiles), \
                       key=lambda x: os.path.splitext(x)[0]):
        image = Image.open(tiles+'/'+tile)
        #convert to RGB mode if not
        if not image.mode=='RGB':
            image=image.convert('RGB')

        h = image.histogram()
        r=h[0:256]
        g=h[256:256*2]
        b=h[256*2:256*3]
            
        tile_rgb[tiles+'/'+tile]= \
                (sum( i*w for i,w in enumerate(r))/float(sum(r)),\
                sum( i*w for i,w in enumerate(g))/float(sum(g)),\
                sum( i*w for i,w in enumerate(b))/float(sum(b)))

    #time measure ends
    #print "Total time for analyzing: "\
    #      + str(time.time()-start)+ " seconds."
