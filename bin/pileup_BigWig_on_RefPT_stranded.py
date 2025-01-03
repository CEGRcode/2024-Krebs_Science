import sys
import argparse
import pyBigWig

def getParams():
    '''Parse parameters from the command line'''
    parser = argparse.ArgumentParser(description='''
This script will pileup BigWig scores.

Example: python pileup_BigWig_on_RefPT_stranded.py -i INPUT.bw -r REF.bed -o OUTPUT.cdt''')
    parser.add_argument('-i','--input', metavar='bigwig_fn', required=True, help='a BigWig file of signal to pileup')
    parser.add_argument('-r','--reference', metavar='bed_fn', required=True, help='a BED file of RefPT to pileup around')
    parser.add_argument('-o','--output', metavar='basename', required=True, help='a basename for two CDT files with \'_same.cdt\' and \'_opposite.cdt\' suffixes')

    args = parser.parse_args()
    return(args)

def loadBedGraph(bg_fn):
    coord2score = {}
    reader = open(bg_fn,'r')
    for line in reader:
        if (line.find("chrom")==0):
            continue
        tokens = line.strip().split('\t')
        coord2score.setdefault(tokens[0], {})
        for i in range(int(tokens[1]), int(tokens[2])):
            coord2score[tokens[0]].update({i:float(tokens[3])})
    reader.close()
    return(coord2score)

if __name__ == "__main__":
	'''Gets per-bp BigWig signal within BED coordinate regions to build CDT pileup.'''

    # Load reference BED coordinates
    args = getParams()

    # Initialize indicator for when header is written
    headerWritten = False

    bw = pyBigWig.open(args.input)

    swriter = open('%s_same.cdt' % args.output,'w')
    owriter = open('%s_opposite.cdt' % args.output,'w')
    # Parse pileup
    reader = open(args.reference,'r')
    for line in reader:
        # Skip first line
        tokens = line.strip().split('\t')

        # Load RefPT info
        chrstr = tokens[0]
        start = int(tokens[1])
        stop = int(tokens[2])
        my_id = tokens[3]
        strand = tokens[5]

        # Write header if not yet written
        if (not headerWritten):
            swriter.write("YORF\tNAME\t" + "\t".join([str(i) for i in range(stop-start)]) + "\n")
            owriter.write("YORF\tNAME\t" + "\t".join([str(i) for i in range(stop-start)]) + "\n")
            headerWritten = True

        # Parse BigWig for values
#                values = [0] * (stop-start)
#                for interval in bw.intervals(chrstr, start, stop):
#                    i_start = interval[0] - start
#                    i_stop =  interval[1] - start
#                    [values.set(i,str(interval[2])) for i in range(i_start, i_stop)]
        scoreDict = {}
        fetched_intervals = bw.intervals(chrstr, start, stop)
        if (fetched_intervals != None):
            for interval in fetched_intervals:
                for index in range(interval[0],interval[1]):
                    scoreDict.update({index:interval[2]})

        # Write CDT values
        values = [str(scoreDict.get(i,0)) for i in range(start, stop)]
        if (strand == "-"):
            values.reverse()
            swriter.write(my_id + "\t" + my_id + "\t" + "\t".join(["0"]*len(values)) + "\n")
            owriter.write(my_id + "\t" + my_id + "\t" + "\t".join(values) + "\n")
        else:
            swriter.write(my_id + "\t" + my_id + "\t" + "\t".join(values) + "\n")
            owriter.write(my_id + "\t" + my_id + "\t" + "\t".join(["0"]*len(values)) + "\n")
    reader.close()
    swriter.close()
    owriter.close()
    bw.close()


