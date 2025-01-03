from kdtree import KDTree, Point
import numpy as np
pointsFloating = [(np.float64(0.18145161290322576), np.float64(0.2959677419354838)), (np.float64(0.6693548387096775), np.float64(0.07251082251082264)), (np.float64(-0.13306451612903225), np.float64(0.48548387096774204)), (np.float64(-0.028225806451612767), np.float64(-0.006451612903225823)), (np.float64(0.41532258064516125), np.float64(-0.09516129032258058)), (np.float64(-0.27419354838709675), np.float64(-0.0669354838709677)), (np.float64(-0.27822580645161277), np.float64(-0.07096774193548383)), (np.float64(0.153225806451613), np.float64(-0.48484848484848486)), (np.float64(0.14516129032258074), np.float64(-0.474025974025974)), (np.float64(-0.5120967741935484), np.float64(0.14826839826839833)), (np.float64(-0.5927419354838709), np.float64(-0.27922077922077926)), (np.float64(-0.3588709677419355), np.float64(-0.38203463203463206)), (np.float64(-0.4677419354838709), np.float64(-0.09112903225806446)), (np.float64(0.653225806451613), np.float64(0.04596774193548381)), (np.float64(-0.24596774193548376), np.float64(-0.3129032258064516)), (np.float64(0.3306451612903225), np.float64(-0.29004329004329)), (np.float64(0.14919354838709675), np.float64(0.2919354838709678)), (np.float64(-0.185483870967742), np.float64(-0.1114718614718615)), (np.float64(0.23790322580645173), np.float64(-0.5281385281385281)), (np.float64(0.6290322580645162), np.float64(-0.16774193548387095)), (np.float64(0.7540322580645162), np.float64(-0.1872294372294372)), (np.float64(0.7540322580645162), np.float64(-0.1872294372294372)), (np.float64(0.6935483870967742), np.float64(-0.17640692640692635)), (np.float64(0.7177419354838708), np.float64(-0.17099567099567103)), (np.float64(0.8306451612903227), np.float64(-0.1655844155844155)), (np.float64(0.8306451612903227), np.float64(-0.23051948051948057)), (np.float64(0.8306451612903227), np.float64(-0.23051948051948057)), (np.float64(0.8306451612903227), np.float64(-0.23051948051948057)), (np.float64(0.6653225806451613), np.float64(0.045454545454545414)), (np.float64(0.6733870967741935), np.float64(-0.24675324675324672)), (np.float64(0.9032258064516128), np.float64(-0.22510822510822504)), (np.float64(0.38306451612903225), np.float64(-0.4902597402597403)), (np.float64(-0.5806451612903225), np.float64(-0.4145021645021645)), (np.float64(-0.8629032258064515), np.float64(-0.48484848484848486))]
pointsFloatingArea = [(0.15,-0.6),(0.5,-0.4)]
pointsIntegers = [(-2,3,1),(-1,2,3),(1,1,4),(2,2,6),(1,4,1),(1,-2,0),(1,2,2)]
pointsIntegersArea = [(0,0,0),(4,4,4)]
tuplesToPointIntegers = [ Point(e[0],e[1],e[2]) for e in pointsIntegers ]
tree = KDTree(K=3)
testingPoints = tuplesToPointIntegers

tree.build_tree(testingPoints)
tree.insert_point(testingPoints[0])
tree.insert_point(testingPoints[2])
tree.insert_point(testingPoints[2])
tree.delete_point(testingPoints[2])
tree.delete_point(Point(1,1,4))
tree.delete_point(Point(1,1,4))
tree.delete_point(Point(1,2,2))
tree.delete_point(Point(1,2,2))

count, resultPoints = tree.get_points_in_rectangle(*pointsIntegersArea) 

print(count)
for point in resultPoints:
    print(point)
