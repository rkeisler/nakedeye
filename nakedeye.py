import numpy as np
import ipdb
import matplotlib.pylab as pl
pl.ion()


def dot_ra_dec(ra0, dec0, ra, dec):
    d2r = np.pi/180.
    phi0 = ra0*d2r
    th0 = (90.-dec0)*d2r
    x0 = np.cos(phi0)*np.sin(th0)
    y0 = np.sin(phi0)*np.sin(th0)
    z0 = np.cos(th0)

    phi = ra*d2r
    th = (90.-dec)*d2r
    x = np.cos(phi)*np.sin(th)
    y = np.sin(phi)*np.sin(th)
    z = np.cos(th)    
    dot = x*x0 + y*y0 + z*z0
    return dot


def parseData():
    ra_gal_center = 15.*(17. + 45.6/60.)
    dec_gal_center = -28.94
    ra_gal_npole = 15.*(12. + 51.4/60.)
    dec_gal_npole = 27.13
    f=open('../HYG-Database/hygxyz.csv','r')
    f.next()
    mag=[];x=[];y=[];z=[];dist=[];ra=[];dec=[]
    for line in f:
        tmp = line.split(',')
        mag.append(np.float(tmp[13]))
        dist.append(3.262/1000.*np.float(tmp[9])) #klyr
        ra.append(15.*np.float(tmp[7]))
        dec.append(np.float(tmp[8]))
    f.close()
    mag = np.array(mag)
    dist = np.array(dist)
    ra = np.array(ra)
    dec = np.array(dec)
    dot_gal_center = dot_ra_dec(ra_gal_center, dec_gal_center, ra, dec)
    dot_gal_npole = dot_ra_dec(ra_gal_npole, dec_gal_npole, ra, dec)
    dist_gal_center = dist*dot_gal_center
    dist_gal_npole = dist*dot_gal_npole
    # need to clean up the crazy distances here.
    # namely, convert to ecliptic coordinates (astropy), then 
    # cut out points near the ecliptic.
    #ipdb.set_trace()

    wh=np.where((mag<6)&(np.abs(dec)>30.))[0]
    wh=np.where((mag<6))[0]
    minx=-5;maxx=30.
    miny=-1.;maxy=1.
    ratio = 1.*(maxx-minx)/(maxy-miny)
    sf=3.8;
    
    #pl.figure(1,figsize=(sf*ratio,sf*1.))

    pl.figure(1,figsize=(17.5, 1.0))
    pl.clf();
    pl.plot(dist_gal_center[wh], dist_gal_npole[wh],'.')
    pl.plot(27.2,0,'ro')
    pl.xlim(minx,maxx)
    pl.ylim(miny,maxy)


    pl.figure(2,figsize=(5,5))
    pl.clf();
    pl.plot(dist_gal_center[wh], dist_gal_npole[wh],'.')
    rrr=0.5
    pl.xlim(-rrr,rrr)
    pl.ylim(-rrr,rrr)

    print np.median(dist[wh])

    '''
    wh=np.where(mag<7)[0]
    print len(wh),np.percentile(dist[wh],90)
    from mpl_toolkits.mplot3d import Axes3D
    fig = figure(1)
    fig.clf()
    ax = Axes3D(fig)
    ax.plot(x[wh], y[wh], z[wh], '.')
    rr=500
    ax.set_xlim3d(-rr,rr)
    ax.set_ylim3d(-rr,rr)
    ax.set_zlim3d(-rr,rr)
    '''


