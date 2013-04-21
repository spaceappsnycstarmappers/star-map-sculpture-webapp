# Create a mock array of tuples
# generate an OpenSCAD file from that data.
# 
# Robert Carlsen | @robertcarlsen

from random import *
from solid import * # SolidPython

#import numpy
#import scipy
#from scipy import spatial

# the mock data is normalized...let's make this bigger
# this is just the coordinate scale at the moment
# lets presume this is mm.
SCALE = 100
STAR_BASE_RADIUS = 3.0
COLUMN_RADIUS = [2.0, 1.0]

def make_mock_stars():
	mock_stars = []
	for i in range(0, 20, 1):
	    this_star = []
	    for c in range(3):
	        this_star.append(random())
	    mock_stars.append(this_star)
	return mock_stars

def render_scad(stars, fp, method=None):
	if method == "ball-and-stick":
		u = _ball_and_stick_impl(stars)
	elif method == "sophisticated-bubble":
		u = _sophisticated_bubble_impl(stars)
	else:
		raise Exception("strange method given")
	scad = scad_render(u)
	fp.write("$fn=20;\n")
	fp.write(scad)

# this is the naive 'ball and stick' representation:
def _ball_and_stick_impl(stars):
	model_data = []
	for i, coord in enumerate(stars):
	    #print coord
	    scaled_coord = [x*SCALE for x in coord]

	    # testing
	    star_rand_scale = uniform(0.5, 1.25)

	    s = translate(scaled_coord)(
	              sphere(star_rand_scale * STAR_BASE_RADIUS),
	              translate([0,0,-scaled_coord[2]])(
	                  cylinder(r1=COLUMN_RADIUS[0], r2=COLUMN_RADIUS[1], h=scaled_coord[2])
	                  )
	            )
	    model_data.append(s)

	# combine all model_data and add a base plate, 
	u = translate([-SCALE/2, -SCALE/2, 0])(model_data,cube([SCALE, SCALE, 2]))
	return u

# trying a more sophisticated model
def _sophisticated_bubble_impl(stars):
	model_data = []
	neighbors_list = []
	# play with the leafsize here
	star_tree = scipy.spatial.cKDTree(mock_stars,leafsize=100)
	for star in mock_stars:
	    # need to twiddle these dials
	    neighbors = star_tree.query(star,k=2,distance_upper_bound=20)
	    # print neighbors
    
	    scaled_coord = [x*SCALE for x in mock_stars[neighbors[1][0]]]
	    # make a column between the current
	    neighbors_list.append(
	            # getting our location, and the distance as the sphere
	            translate(scaled_coord)(sphere(SCALE*neighbors[0][1]))
	            )
	model_data = neighbors_list

	# no need for a base plate here (but may need support)
	u = translate([-SCALE/2, -SCALE/2, 0])(model_data)
	return u
