import numpy as np
import ipdb
import matplotlib.pylab as plt
from os import system
plt.ioff()
klyr_to_center = 27.2

def main():
    d_right, d_up, mag = get_star_data()
    fig, ax = initialize_figure()
    draw_galaxy(ax)
    plot_stars(ax, d_right, d_up, mag, mag_min=0, mag_max=3.0, color='#FFFFCC', psize=16, alpha=0.7)
    plot_stars(ax, d_right, d_up, mag, mag_min=3.0, mag_max=4.5, color='#FFFF66', psize=8, alpha=0.5)
    plot_stars(ax, d_right, d_up, mag, mag_min=4.5, mag_max=6.0, color='#FFCC66', psize=4, alpha=0.5)
    add_local_info(ax)
    convert_to_html_and_open(fig)

def draw_galaxy(ax):
    from matplotlib.patches import Ellipse

    # main disk
    alpha=0.04
    nell = 10
    for w,h in zip(np.linspace(60,80,nell), np.linspace(0.9,2.2,nell)):
        ax.add_patch(Ellipse(xy=(klyr_to_center,0), width=w, height=h, angle=0, color='white', alpha=alpha))

    # dust
    #ax.add_patch(Ellipse(xy=(klyr_to_center,0), width=70, height=0.3, angle=0, color='brown', alpha=0.1))

    # bulge
    alpha=0.06
    nell = 5
    for w,h in zip(1.3*np.linspace(4,8,nell), np.linspace(4,8,nell)):
        ax.add_patch(Ellipse(xy=(klyr_to_center,0), width=w, height=h, angle=0, color='white', alpha=alpha))


def add_local_info(ax):
    from matplotlib.patches import Circle
    plt.text(0,2,'hello deezer',color='white')
    ax.add_patch(Circle((0,0), radius=0.5, color='red', fill=False, linewidth=1))
    #ax.add_patch(Circle((0,0), radius=0.05, color='blue', fill=False))

def convert_to_html_and_open(fig):
    from mpld3 import fig_to_d3
    html = fig_to_d3(fig)
    file=open('small.html','w')
    file.write('<style type="text/css">@import url("custom.css");</style>')
    file.write(html)
    file.close()
    system('open small.html')


def plot_stars(ax, d_right, d_up, mag, mag_min=0, mag_max=3.0, 
               color='#FFFF99', psize=6, alpha=0.3):
    wh=np.where((mag>mag_min)&(mag<=mag_max))[0]
    #wh=wh[0:-1:1]
    plt.scatter(d_right[wh], d_up[wh], 
                alpha=alpha, s=psize, 
                color=color, linewidths=0)


def initialize_figure():
    aratio = 2.3
    sf = 5.5
    minx=-6;maxx=33.5
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

    
def get_star_data():
    from pandas.io.parsers import read_csv
    d=read_csv('../HYG-Database/hygxyz.csv')
    ra=15.*d['RA']; dec=d['Dec']; mag=d['Mag'];
    dis=d['Distance']*3.262/1000 #convert from parsec to klyr
    ra_gal_center = 15.*(17. + 45.6/60.)
    dec_gal_center = -28.94
    ra_gal_npole = 15.*(12. + 51.4/60.)
    dec_gal_npole = 27.13
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



