import math

class Path:

    def __init__(self):
        self.pointList = []
        self.cost = 0



def first_point_y(contour):
    return contour[0][1]

def first_point_x(contour):
    return contour[0][0]

def last_point_y(contour):
    return contour[len(contour)-1][1]

def last_point_x(contour):
        return contour[len(contour)-1][0]


def find_start_contour(contours, imHeight, imWidth):
    # find starting contour by contour closest to edge
    start_contour = None
    minDist = float('inf')
    for line in contours:
        dist = min(first_point_x(line), first_point_y(line), imWidth-first_point_x(line), imHeight-first_point_y(line))
        if dist < minDist:
            minDist = dist
            start_contour = line

    return start_contour

def distance(point, contour):
    x = first_point_x(contour)
    y = first_point_y(contour)
    return math.sqrt((x - point[0]) ** 2 + (y - point[1]) ** 2)

def point_dist(p1, p2):
    return math.sqrt( (p1[0] - p2[0])**2 +  (p1[1] - p2[1])**2)


def find_nearest(curr_line,  contours):
    nearest_line = None
    min_dist = float('inf')
    curr_x = curr_line[len(curr_line)-1][0]
    curr_y = curr_line[len(curr_line)-1][1]
    for line in contours:
        if curr_line != line:
            dist = math.sqrt((curr_x - first_point_x(line))**2 + (curr_y - first_point_y(line))**2)
            if dist < min_dist:
                min_dist = dist
                nearest_line = line

            #also check dist to last point in contour
            dist_to_last = math.sqrt((curr_x - last_point_x(line))**2 + (curr_y - last_point_y(line))**2)
            if dist_to_last < min_dist:
                min_dist = dist_to_last
                nearest_line = list(reversed(line))


    return nearest_line

# trying slow approach to allow backtracking. Check every point on curr_contour compared with every point on every other
#contour
def find_nearest_backtrack(curr_line,  contours):
    nearest_line = None
    min_dist = float('inf')
    curr_x = curr_line[len(curr_line)-1][0]
    curr_y = curr_line[len(curr_line)-1][1]
    i = 0
    for line in contours:
        if curr_line != line:
            for curr_contour_point in curr_line:
                for point in line:
                    dist = math.sqrt((curr_contour_point[0] - point[0])**2 + (curr_contour_point[1] - point[1])**2)
                    if dist < min_dist:
                        min_dist = dist
                        nearest_line = line
                        nearest_point = point
        print(i)
        i+=1
    return nearest_line, point


def surrounding_bins(curr_bin):
    x = curr_bin[0]
    y = curr_bin[1]
    surr_bins = []
    surr_bins.append((x-1, y+1))
    surr_bins.append((x-1, y))
    surr_bins.append((x-1, y-1))
    surr_bins.append((x, y+1))
    surr_bins.append((x, y-1))
    surr_bins.append((x + 1, y + 1))
    surr_bins.append((x + 1, y))
    surr_bins.append((x + 1, y - 1))

    return surr_bins

def in_bounds(index, bins):
    return 0 <= index[0] < len(bins) and 0 <= index[1] < len(bins[0])

#todo: If there are no contours in surrounding binn, need to search next level out
def search_surrounding_bins(point, curr_bin,  bins):
    nearest = None
    min_dist = float('inf')
    surr_bins = surrounding_bins(curr_bin)
    for bin_ind in surr_bins:
        #make sure bin_ind is in bounds
        if in_bounds(bin_ind, bins):
            near = find_nearest(point, bins[bin_ind[0]][bin_ind[1]])
            if distance(point, near) < min_dist:
                min_dist = distance(point, near)
                nearest = near
    return nearest


