import os,sys,Image,time,shutil,imghdr

one_tile_err = '''
Error: There must be at least one tile!
'''
tile_format_err='''
Tile format error:

All of the tiles (in dir2) must be in one of
the five formats allowed for the target image.

All the tile images must be the same formats.
'''

tile_dimen_err='''
Dimension error:

All the tiles must have the same dimensions in pixels.
'''

construct_err='''
Construction error:

it is not possible to construct an output image
of the required size without using at least one tile
more often than is permitted by n4
'''

dimen_error='''
Dimension error:

The width of each tile must be a divisor of the width
of the target image, and the height of each tile must
be a divisor of the height of the target image.
'''

def prepro(target,tiles,repeat,canon):
    """
    preprocess the input
    make sure the input is valid
    and format tile name for later use

    arguments:
    target--target image
    tile--tile images path
    repeat--maximun repeat times per tile

    output:
    target_dimen--target image dimension
    tile_dimen--tile image dimension
    """
    #time measure starts
    start=time.time()
    #print 'start preprocessing...'
    
    #get target image's dimension
    img=Image.open(target)
    target_dimen=img.size

    #check there is at least one tile 
    if not len(os.listdir(tiles)) > 0:
        print one_tile_err
        cleanup(canon)
        sys.exit()
        
    #get tile image's format and dimension    
    for tile in os.listdir(tiles):
        try:
            tile_img=Image.open(tiles+'/'+tile)
            tile_format=imghdr.what(tiles+'/'+tile)
        except:
            print tile_format_err
            print tiles+'/'+tile
            cleanup(canon)
            sys.exit()
        break
    tile_dimen=tile_img.size

    
    if not tile_format in ['jpeg','png','bmp','tiff','gif']:
        print tile_format_err
        print tiles+'/'+tile
        cleanup(canon)
        sys.exit()
        
    #make sure dimension requirements meet
    if target_dimen[0]%tile_dimen[0] or target_dimen[1]%tile_dimen[1]:
        print dimen_error
        cleanup(canon)
        sys.exit()

    #check if tiles can construct final mosaic under
    #repeat time restriction
    width_time=target_dimen[0]/tile_dimen[0]
    height_time=target_dimen[1]/tile_dimen[1]
    num_of_tile=width_time*height_time
    num_available=repeat*len(os.listdir(tiles))
    if num_of_tile > num_available:
        print construct_err
        cleanup(canon)
        sys.exit()

    L=sorted(os.listdir(tiles),key=lambda x: os.path.splitext(x)[0])
        
    #process every tile 
    for tile in L:
        each_format=imghdr.what(tiles+'/'+tile)
        if each_format not in \
           ['jpeg','png','bmp','tiff','gif']:
            print tile_format_err
            print tiles+'/'+tile
            cleanup(canon)
            sys.exit()
        
        try:
            each_tile=Image.open(tiles+'/'+tile)
        except:
            print 'Error: tile invalid!'
            print tiles+'/'+tile
            cleanup(canon)
            sys.exit()

        if not tile_dimen==each_tile.size:               
            print tile_dimen_err
            print tiles+'/'+tile
            cleanup(canon)
            sys.exit()
            
        if not each_format == tile_format:
            print tile_format_err
            print tiles+'/'+tile
            cleanup(canon)
            sys.exit()
                      
    #print "Total time for preprocessing: "\
    #      + str(time.time()-start)+ " seconds."         
    return (target_dimen,tile_dimen)

def cleanup(canon):
    canon = str(canon)+'.tiff'
    if os.path.exists('/tmp/canonical'+canon):
        os.remove('/tmp/canonical'+canon)
