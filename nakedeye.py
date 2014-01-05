import numpy as np
import ipdb
import matplotlib.pylab as plt
from os import system
plt.ioff()
#plt.ion()
klyr_to_center = 27.2
ra_gal_center = 15.*(17. + 45.6/60.)
dec_gal_center = -28.94
ra_gal_npole = 15.*(12. + 51.4/60.)
dec_gal_npole = 27.13
ra_ecl_npole = 15.*18.0
dec_ecl_npole = 66. + 33./60. + 38.55/3600.
lyr_per_pc = 3.2616


fontsize=20
yspacing = fontsize/20*0.15
textcolor = '#99FFFF'
textcolor = 'white'
charwidth=29
# http://cdsarc.u-strasbg.fr/viz-bin/Cat?cat=I%2F239&target=http&
# http://cdsarc.u-strasbg.fr/viz-bin/nph-Cat/fits?I%2F239/hip_main.dat.gz

def main():
    d_right, d_up, mag = get_star_data()
    fig, ax = initialize_figure()
    draw_galaxy(ax)

    plot_stars(ax, d_right, d_up, mag, mag_min=-99, mag_max=3.0, color='#FFFFFC', psize=16, alpha=0.6)
    plot_stars(ax, d_right, d_up, mag, mag_min=3.0, mag_max=6.0, color='#FFCC66', psize=5, alpha=0.3)
    #plot_stars(ax, d_right, d_up, mag, mag_min=3.0, mag_max=4.5, color='#FFFF66', psize=10, alpha=0.4)
    #plot_stars(ax, d_right, d_up, mag, mag_min=4.5, mag_max=6.0, color='#FFCC66', psize=5, alpha=0.3)

    add_local_info(ax)
    convert_to_html_and_open(fig)

def draw_galaxy(ax):
    from matplotlib.patches import Ellipse

    # main disk
    alpha=0.04
    nell = 10
    for w,h in zip(np.linspace(60,80,nell), np.linspace(1.0,2.0,nell)):
        ax.add_patch(Ellipse(xy=(klyr_to_center,0), width=w, height=h, angle=0, color='white', alpha=alpha))

    # bulge
    alpha=0.06
    nell = 5
    for w,h in zip(1.3*np.linspace(4,8,nell), np.linspace(4,8,nell)):
        ax.add_patch(Ellipse(xy=(klyr_to_center,0), width=w, height=h, angle=0, color='white', alpha=alpha))
    text_rectangle(klyr_to_center+0.1, 0.3, charwidth, fontsize, textcolor, yspacing, 'The center of the Milky Way is about 30,000 light-years away, and the light we see from it today was emitted around the time that humans began farming.')
#   during the Upper Paleolithic, when humans were not yet farming but beginning to produce art')
#   when early humans were painting in caves but not yet farming.')



    # lmc
    ra_lmc = 80.893
    dec_lmc = -69.75611
    dot_gal_center_lmc = dot_ra_dec(ra_gal_center, dec_gal_center, ra_lmc, dec_lmc)
    dot_gal_npole_lmc = dot_ra_dec(ra_gal_npole, dec_gal_npole, ra_lmc, dec_lmc)
    print 'lmc ',np.sqrt(1.-dot_gal_center_lmc**2.-dot_gal_npole_lmc**2.),dot_gal_center_lmc,dot_gal_npole_lmc
    d_klyr_lmc = 163.
    d_right_lmc = d_klyr_lmc*dot_gal_center_lmc
    d_up_lmc = d_klyr_lmc*dot_gal_npole_lmc
    diam_klyr_lmc = 14.
    alpha=0.1
    nell = 5
    for w,h in zip(np.linspace(0.3*diam_klyr_lmc,diam_klyr_lmc,nell), np.linspace(0.3*diam_klyr_lmc,diam_klyr_lmc,nell)):
        ax.add_patch(Ellipse(xy=(d_right_lmc,d_up_lmc), width=w, height=h, angle=0, color='white', alpha=alpha))
    text_rectangle(d_right_lmc+0.1, d_up_lmc+1.6, charwidth, fontsize, textcolor, yspacing, "The Large Magellanic Cloud is a dwarf galaxy and one of the Milky Way's satellites.  It's located about 160,000 light-years from Earth.")
    text_rectangle(d_right_lmc+0.1, d_up_lmc+0.65, charwidth, fontsize, textcolor, yspacing, "Note that many of the objects shown on this page are even farther away than they appear to be.  You just can't see the distances into and out of the screen.")


    # smc
    ra_smc = 13.18666
    dec_smc = -72.828
    dot_gal_center_smc = dot_ra_dec(ra_gal_center, dec_gal_center, ra_smc, dec_smc)
    dot_gal_npole_smc = dot_ra_dec(ra_gal_npole, dec_gal_npole, ra_smc, dec_smc)
    print 'smc ',np.sqrt(1.-dot_gal_center_smc**2.-dot_gal_npole_smc**2.),dot_gal_center_smc,dot_gal_npole_smc
    d_klyr_smc = 197.
    d_right_smc = d_klyr_smc*dot_gal_center_smc
    d_up_smc = d_klyr_smc*dot_gal_npole_smc
    diam_klyr_smc = 7.
    alpha=0.1
    nell = 5
    for w,h in zip(np.linspace(0.3*diam_klyr_smc,diam_klyr_smc,nell), np.linspace(0.3*diam_klyr_smc,diam_klyr_smc,nell)):
        ax.add_patch(Ellipse(xy=(d_right_smc,d_up_smc), width=w, height=h, angle=0, color='white', alpha=alpha))
    text_rectangle(d_right_smc+0.1, d_up_smc+0.4, charwidth, fontsize, textcolor, yspacing, "The Small Magellanic Cloud is about 200,000 light-years from Earth.")
    text_rectangle(d_right_smc+0.1, d_up_smc-0.2, charwidth, fontsize, textcolor, yspacing, "The light we see from it originated right around the time that homo sapiens first appeared in Africa.")

    # m31
    ra_m31 = 10.6845
    dec_m31 = 41.2691
    dot_gal_center_m31 = dot_ra_dec(ra_gal_center, dec_gal_center, ra_m31, dec_m31)
    dot_gal_npole_m31 = dot_ra_dec(ra_gal_npole, dec_gal_npole, ra_m31, dec_m31)
    print 'm31 ',np.sqrt(1.-dot_gal_center_m31**2.-dot_gal_npole_m31**2.),dot_gal_center_m31,dot_gal_npole_m31
    d_klyr_m31 = 2.54*1000.
    d_right_m31 = d_klyr_m31*dot_gal_center_m31
    d_up_m31 = d_klyr_m31*dot_gal_npole_m31
    # main disk
    alpha=0.04
    nell = 10
    for w,h in zip(np.linspace(60,80,nell), 4.*np.linspace(1.1,2.4,nell)):
        ax.add_patch(Ellipse(xy=(d_right_m31,d_up_m31), width=w, height=h, angle=-30, color='white', alpha=alpha))

    # bulge
    alpha=0.05
    nell = 5
    for w,h in zip(1.4*1.3*np.linspace(4,8,nell), 1.4*np.linspace(4,8,nell)):
        ax.add_patch(Ellipse(xy=(d_right_m31,d_up_m31), width=w, height=h, angle=-30, color='white', alpha=alpha))
    #x0=-1.75
    #y0=d_up_m31+2.2
    x0=-2.32
    y0=d_up_m31+1.2
    text_rectangle(d_right_m31+x0, y0, charwidth, fontsize, textcolor, yspacing, "The Andromeda Galaxy is the nearest spiral galaxy to the Milky Way but is still very far away, about 2.5 million light-years.  It is by far the most distanct object visible to the naked eye, and the light we see from it was produced way back hominids were first learning to use stone tools.")

    text_rectangle(d_right_m31+x0, y0-1.6, charwidth, fontsize, textcolor, yspacing, "It's incredible that, thanks to some fluke of physics and evolution, we can see this far with our eyeballs!")

    #x=d_right_m31+x0; y=d_up_m31-0.1
    x=d_right_m31+0.25; y=y0-1.6#d_up_m31-1.1
    text_rectangle(x, y, charwidth, fontsize, textcolor, yspacing, "Modern telescopes allow us to see much, much farther, but this is the end of the line for objects visible to the naked eye, and for this page.  I promise that, no matter how much you zoom out, you will never never get to the Cosmic Microwave Background.")



    # draw connecting lines
    linestyle='--'
    color='#660000'
    lw=1.0
    d_right_mc = 0.5*(d_right_lmc+d_right_smc)
    d_up_mc = 0.5*(d_up_lmc+d_up_smc)
    plt.plot([0,klyr_to_center],[0,0], linestyle, color=color,linewidth=lw)
    if False:
        plt.plot([klyr_to_center,d_right_mc],[0,d_up_mc], linestyle, color=color,linewidth=lw)
        plt.plot([d_right_mc, d_right_m31],[d_up_mc, d_up_m31], linestyle, color=color,linewidth=lw)
    else:
        plt.plot([klyr_to_center,d_right_lmc],[0,d_up_lmc], linestyle, color=color,linewidth=lw)
        plt.plot([d_right_lmc, d_right_smc],[d_up_lmc, d_up_smc], linestyle, color=color,linewidth=lw)
        plt.plot([d_right_smc, d_right_m31],[d_up_smc, d_up_m31], linestyle, color=color,linewidth=lw)


    

def add_local_info(ax):
    from matplotlib.patches import Circle
    lw = 1
    ax.add_patch(Circle((0,0), radius=0.200, color='lightgray', fill=False, linewidth=lw, linestyle='-'))
    ax.add_patch(Circle((0,0), radius=0.500, color='lightgray', fill=False, linewidth=lw, linestyle='-'))
    plt.text(0,0.21, '200 lyr', color=textcolor, size=fontsize, horizontalalignment='center')
    plt.text(0,0.51, '500 lyr', color=textcolor, size=fontsize, horizontalalignment='center')
    plt.text(0,0.51, '500 lyr', color=textcolor, size=fontsize, horizontalalignment='center')
    
    coltmp = '#666666'
    plt.text(0, -0.68-0.045, 'star positions from', color=coltmp, size=fontsize, horizontalalignment='center')
    plt.text(0, -0.81-0.045, 'the Hipparcos sattelite', color=coltmp, size=fontsize, horizontalalignment='center')

    x0=-2.6; y0=0.4
    text_rectangle(x0, y0, charwidth, fontsize, textcolor, yspacing, 'The stars you can see with your naked eye are typically several hundreds of light-years away.')
    text_rectangle(x0, y0-0.55, charwidth, fontsize, '#FFFFFC', yspacing, 'The white stars show what you might see from a city,')
    text_rectangle(x0, y0-0.85, charwidth, fontsize, '#FFFFFC', yspacing, 'the yellow stars from the country.')



    text_rectangle(x0, -1, charwidth, fontsize, '#666666', yspacing, 'Zoom in and out to explore.')
    text_rectangle(1.0, 0.03, 4*charwidth, fontsize, '#995555', yspacing, '>  to the center of the Milky Way  >')


def text_rectangle(x, y, charwidth, fontsize, color, yspacing, thetext):
    words = thetext.split(' ')
    wordcount=0
    line=''
    nlines=-1
    for word in words:
        line += word
        line += ' '
        wordcount+=1
        if (len(line)>charwidth) or (wordcount==len(words)):
            nlines+=1
            plt.text(x, y-nlines*yspacing, line, color=color, size=fontsize)
            line=''
    
    
    
    

def convert_to_html_and_open(fig):
    from mpld3 import fig_to_d3
    html = fig_to_d3(fig)
    file=open('index.html','w')
    file.write('<style type="text/css">@import url("custom.css");</style>')
    file.write(html)
    file.close()
    system('open index.html')


def plot_stars(ax, d_right, d_up, mag, mag_min=0, mag_max=3.0, 
               color='#FFFF99', psize=6, alpha=0.3):
    wh=np.where((mag>mag_min)&(mag<=mag_max))[0]
    #wh=wh[0:-1:1]
    plt.scatter(d_right[wh], d_up[wh], 
                alpha=alpha, s=psize, 
                color=color, linewidths=0)


def initialize_figure():
    aratio = 2.3
    sf = 5.2

    aratio = 1.9
    sf = 6.5

    #minx=-6;maxx=33.5
    minx=-2.9;maxx=2.9
    miny=-0.5*(maxx-minx)/aratio;
    maxy=0.5*(maxx-minx)/aratio;
    fig = plt.figure(frameon=False, figsize=(aratio*sf,1.*sf))
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.set_axis_bgcolor('k')
    plt.xlim(minx,maxx)
    plt.ylim(miny,maxy)
    return fig, ax

    
def get_star_data_old():
    from pandas.io.parsers import read_csv
    d=read_csv('../HYG-Database/hygxyz.csv')
    ra=15.*d['RA']; dec=d['Dec']; mag=d['Mag'];
    dis=d['Distance']*lyr_per_pc/1000. #convert from parsec to klyr
    dot_gal_center = dot_ra_dec(ra_gal_center, dec_gal_center, ra, dec)
    dot_gal_npole = dot_ra_dec(ra_gal_npole, dec_gal_npole, ra, dec)
    dist_gal_center = dis*dot_gal_center
    dist_gal_npole = dis*dot_gal_npole
    
    #tempp!#tmpp!  convert to equatorial
    wh=np.where(np.abs(dec)>30.)[0]
    dist_gal_center = dist_gal_center[wh]
    dist_gal_npole = dist_gal_npole[wh]
    mag = mag[wh]

    return dist_gal_center, dist_gal_npole, mag

def dot_ra_dec(ra0, dec0, ra, dec):
    # ra/dec should be in degrees.
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


def get_star_data(quick=True):
    import cPickle as pickle
    if quick: ra, dec, plx, e_plx, Vmag, d_kpc, d_klyr = pickle.load(open('get_star_data.pkl','r'))
    else:
        from astropy.io import fits
        d=fits.open('I_239_hip_main.dat.gz.fits')[1].data
        frac_err = 0.2
        max_Vmag = 6.0
        whok = np.where((np.abs(d['e_Plx']/d['Plx'])<frac_err)&(d['Plx']>0.)&(d['Vmag']<max_Vmag))[0]
        whok2 = np.where((d['Plx']>0.)&(d['Vmag']<max_Vmag))[0]
        print 1.*len(whok)/len(whok2) # efficiency of frac_err cut
        ra=d['RAdeg'][whok]; dec=d['DEdeg'][whok]
        plx=d['Plx'][whok]; e_plx=d['e_Plx'][whok]
        Vmag = d['Vmag'][whok]
        d_kpc = 1./plx
        d_klyr = d_kpc*lyr_per_pc
        pickle.dump((ra, dec, plx, e_plx, Vmag, d_kpc, d_klyr), open('get_star_data.pkl','w'))

    # i'm curious about the typical and max distances for various flux cuts.
    wh=np.where((Vmag>-99.)&(Vmag<3.0))[0]; print np.median(d_klyr[wh]), np.max(d_klyr[wh])
    wh=np.where((Vmag>3.0)&(Vmag<4.5))[0]; print np.median(d_klyr[wh]), np.max(d_klyr[wh])
    wh=np.where((Vmag>4.5)&(Vmag<6.0))[0]; print np.median(d_klyr[wh]), np.max(d_klyr[wh])

    dot_gal_center = dot_ra_dec(ra_gal_center, dec_gal_center, ra, dec)
    dot_gal_npole = dot_ra_dec(ra_gal_npole, dec_gal_npole, ra, dec)
    d_gal_center = d_klyr*dot_gal_center
    d_gal_npole = d_klyr*dot_gal_npole
    return d_gal_center, d_gal_npole, Vmag
    
    
    

    



    
