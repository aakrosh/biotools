from multiprocessing import Pool
from sys import stderr

class VCFMapReduce:
    def __init__(self, refname, vcfname, threads, mapfunc, redfunc):
        self.refname = refname  
        self.vcfname = vcfname
        self.threads = threads
        self.mapfunc = mapfunc
        self.redfunc = redfunc

    def run(self):
        # partition the genome based on the number of threads
        chroms = []
        with open("%s.fai" % self.refname, 'r') as f:
            for line in f:
                chrom,length,_,_,_ = line.strip().split("\t")
                chroms.append((chrom,int(length)))
        print >> stderr, "Read the fasta index"
 
        size = int(sum([x for _,x in chroms]) * 1.0 / self.threads)
        partitions = []
        for c,l in chroms:
            for x in xrange(0,l,size):
                partitions.append((self.vcfname,c,x,min(x+size,l)))
        print >> stderr, "Partitioned the genome"
    
        # run all the instances 
        pool = Pool(processes=self.threads,)
        outputs = []
        print >> stderr, "Running %d threads" % self.threads
        for output in  pool.imap_unordered(self.mapfunc, partitions):
            outputs.append(output)
        pool.close()
        pool.join()

        # collate the results       
        self.redfunc(outputs)

if __name__ == "__main__":
    from sys import argv, stderr, stdin, exit, stdout
    from getopt import getopt, GetoptError
    import vcf

    refname = argv[1]
    vcfname = argv[2]

    def count_regional_var((refname,chrom,start,stop)):
        print "here doing %s:%d-%d" % (chrom,start,stop)
        count = 0
        reader = vcf.Reader(open(refname, 'r'))
        try:
            for record in reader.fetch(chrom,start,stop):
                count += 1
        except ValueError:
            pass
        print "done doing %s:%d-%d" % (chrom,start,stop)
        return count
    
    def sum_up_vars(args):
        total = 0
        for s in args:
            total += s
        print "total number is %d" % total
        return total

    mr = VCFMapReduce(refname, vcfname, 2, count_regional_var, sum_up_vars)
    mr.run()
