import math

class PathLine:
    def __init__(self, line_in):
        self.line = line_in
        self.closest_line = None
        self.closest_line_point = None
        self.this_closest_point = None

    def find_closest_line(self, other_path_lines):
        this_line = self.line
        min_dist = float('inf')
        nearest_contour = []
        this_contour_nearest_point = []
        other_contour_nearest_point = []

        for other_path_line in other_path_lines:
            other_line = other_path_line.line
            if this_line != other_line:
                if PathConnector.distance(this_line[0], other_line[0]) < 100: #only check all points if first points are nearby
                    for this_line_point in this_line:
                        for other_line_point in other_line:
                            curr_dist = PathConnector.distance(this_line_point, other_line_point)
                            if curr_dist < min_dist:
                                min_dist = curr_dist
                                nearest_contour = other_path_line
                                this_contour_nearest_point = this_line_point
                                other_contour_nearest_point = other_line_point
        self.closest_line = nearest_contour
        self.this_closest_point = this_contour_nearest_point
        self.closest_line_point = other_contour_nearest_point

#TODO: speed this up. Can think of 2 ways. 1 reimplement a grid style search where the algo only searches
#TODO: within the same or nearby grids. Or look at first and last points of both lines and ignore if theyre
#TODO: too far apart
class PathConnector:

    def __init__(self, contours):
        self.og_path_line_list = []
        for contour_line in contours:
            self.og_path_line_list.append(PathLine(contour_line))
        self.path_line_list = self.og_path_line_list
        self.unconected_lines = self.path_line_list

        # go through each line, for each point in that look at each point of all other lines and find nearest line
        i = 0
        for this_line in self.path_line_list:
            this_line.find_closest_line(self.path_line_list)
            i += 1
            print(i)




    #def connect_line_list(self):
        #for line in self.unconected_lines:
            # case where 2 lines are eachothers nearest line. Need to remove both from list, and insert back as one connected line
            #if line == line.closest_line.closest_line:


    @staticmethod
    def distance(point_a, point_b):
        return math.sqrt((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1])**2)