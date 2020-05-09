import math

def first_point_y(contour):
    return contour[0][1]

def first_point_x(contour):
    return contour[0][0]



def find_start_contour(contours, bins, xBins, yBins, imHeight, imWidth):
    # find starting contour by contour closest to edge
    start_contour = None
    minDist = imHeight * imWidth
    for x in range(xBins):
        # go through top row bins, then bottom ro
        for contour in bins[x][0]:
            y_val = first_point_y(contour)
            if y_val < minDist:
                minDist = y_val
                start_contour = contour
        for contour in bins[x][yBins - 1]:
            y_val = first_point_y(contour)
            if imHeight - y_val < minDist:
                minDist = y_val
                start_contour = contour

    for y in range(yBins):
        # go through first column then last column
        for contour in bins[0][y]:
            x_val = first_point_x(contour)
            if x_val < minDist:
                minDist = x_val
                start_contour = contour
        for contour in bins[xBins - 1][y]:
            x_val = first_point_x(contour)
            if x_val < minDist:
                minDist = x_val
                start_contour = contour
    return start_contour

def distance(point, contour):
    x = first_point_x(contour)
    y = first_point_y(contour)
    return math.sqrt((x - point[0]) ** 2 + (y - point[1]) ** 2)

def find_nearest(point,  bin):
    nearest = None
    min_dist = float('inf')
    for contour in bin:
        dist = distance(point, contour)

        if dist < min_dist:
            nearest = contour
            min_dist = dist

    return nearest


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