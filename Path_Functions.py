import math

def first_point_y(contour):
    return contour[0][1]

def first_point_x(contour):
    return contour[0][0]



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
    return nearest_line


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