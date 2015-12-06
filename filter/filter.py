import pandas
import numpy
import datetime

def createIndex( start , width , data):
    end = data[-1][0]
    end += datetime.timedelta( seconds = width )
    bins  = pandas.date_range( start = start , end = end , freq = "%ds" % width )
    size = len(data)
    index = numpy.ndarray( shape = [size] , dtype = numpy.int32 )    
    index.fill( -1 )

    bin_index = 0
    for i in range(len(data)):
        t = data[i][0]
        if t > end:
            break

        if t >= bins[bin_index]:
            while t > bins[bin_index + 1]:
                bin_index += 1

        index[i] = bin_index
    
    return (bins , index)


def count(start , width , data):
    bins , index = createIndex( start , width , data)
    counts = [ 0 ] * (len( bins) - 1)
    for i in range(len(data)):
        bin_index = index[i]
        counts[bin_index] += 1
    
    return counts



def blockedMean(start , width , data):

    bins , index = createIndex( start , width , data)
    size = len(bins) - 1
    counts = numpy.zeros( shape = [size] , dtype = numpy.float32)    
    totals = numpy.zeros( shape = [size] , dtype = numpy.float32)
    for i in range(len(data)):
        bin_index = index[i]
        counts[bin_index] += 1
        totals[bin_index] += data[i][1]

    return numpy.divide( totals , counts )




#################################################################

def blockedMax(start , width , data):

    bins , index = createIndex( start , width , data)
    size = len(bins) - 1
    max_value = numpy.zeros( shape = [size] , dtype = numpy.float32)    
    max_value.fill( -10000000 )
    for i in range(len(data)):
        bin_index = index[i]

        value = data[i][1]
        if value > max_value[bin_index]:
            max_value[bin_index] = value

    return max_value


def blockedMin(start , width , data):

    bins , index = createIndex( start , width , data)
    size = len(bins) - 1
    min_value = numpy.zeros( shape = [size] , dtype = numpy.float32)    
    min_value.fill( 10000000 )
    for i in range(len(data)):
        bin_index = index[i]

        value = data[i][1]
        if value < min_value[bin_index]:
            min_value[bin_index] = value

    return min_value





