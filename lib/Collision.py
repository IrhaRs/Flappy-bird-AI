import math


def Circle_Circle_Collision(c1x,c1y,c1r,c2x,c2y,c2r):
	distance = Distance_Line(c1x,c1y,c2x,c2y)
	if c1r+c2r >=distance:
		return True
	return False

def Circle_Rect_Collision(cx,cy,radius,rx,ry,rw,rh):
    #temp variables
    testX = cx
    testY = cy

    if cx < rx: 
        testX = rx
    elif cx > rx+rw: 
        textX = rx+rw
    if cy < ry: 
        testY = ry
    elif cy > ry+rh:
        testY = ry+rh
    
    #get distance from closest edge 
    distance = Distance_Line(cx,cy,testX,testY)
    #if distance less than the radius -> collision
    if distance <= radius:
        return True
    return False

def Circle_Rect_Collision2(circle,rect):
    cx,cy,rad = circle
    rx,ry,rw,rh = rect
    return Circle_Rect_Collision(cx,cy,rad,rx,ry,rw,rh)

def Circle_Line_Collision(cx,cy,cr,lsx,lsy,lex,ley):
	#circle to line/vector segment Collision 

	#check if the ends of the line are inside of the circle
	inside1 = Point_Circle_Collision(lsx,lsy, cx,cy,cr)
	inside2 = Point_Circle_Collision(lex,ley, cx,cy,cr)
	if (inside1 or inside2):
		return True

	#get length of the line
	length = Distance_Line(lsx,lex,lsy,ley)

	#create dot product
	dot = (((cx-lsx)*(lex-lsx))+ ((cy-lsy)*(ley-lsy))) / math.pow(length,2)

	#get the closest point to the line
	closestX = lsx + (dot * (lex-lsx))
	closestY = lsy + (dot * (ley-lsy))

	#get if the point is on the line.
	onSegment = Point_Line_Collision(closestX,closestY,lsx,lsy,lex,ley)
	if not onSegment:
		return False

	#get distance between circle point and point on line
	distance = Distance_Line(closestX,closestY,cx,cy)
	#check if distance is smaller than radius
	if distance <= cr:
		return True
	return False

def AABB_Collision(x1,y1,w1,h1,x2,y2,w2,h2):
	#AABB Collision to check if something is within the rectangle.
	if (x1<x2 + w2 and x1 + w1 > x2 and y1<y2+h2 and y1+h1 > y2):
		return True

def AABB_Collision_rect(rect1,rect2):
	#pass through to the AABB function
	x1,y1,w1,h1=rect1
	x2,y2,w2,h2=rect2
	return AABB_Collision(x1,y1,w1,h1,x2,y2,w2,h2)



def Point_Circle_Collision(px,py,cx,cy,cr):
	#point in circle Collision
	distance = Distance_Line(px,py,cx,cy)

	if distance <= cr:
		return True
	return False

def Point_Line_Collision(px,py,lx1,ly1,lx2,ly2):
	lineLen = Distance_Line(lx1,ly1,lx2,ly2)

	d1 = Distance_Line(px,py,lx1,ly1)
	d2 = Distance_Line(px,py,lx2,ly2)

	buf=0.1

	if (d1+d2 >= lineLen-buf and d1+d2 <= lineLen+buf): 
		return True
	return False

def Distance_Line(x1, y1, x2, y2):
	dist_x = x1 - x2
	dist_y = y1 - y2
	distance = math.sqrt((dist_x*dist_x)+(dist_y*dist_y))
	return distance