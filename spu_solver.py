import argparse
import sys
import msat_runner


class FileSystem(object):
    def __init__(self,file_path=''):
        self.n_packages = 0
        self.packages = []
        self.dependences = []
        self.conflicts = []

        if file_path: self.read(file_path)

    def read(self,file_path):
        ''' Loads the packages, their dependences and their conflicts from the input file'''
        n_packages = -1
        dependences,conflicts,packages = set(),set(),set()
        
        with open(file_path, 'r') as stream:
            reader = (l for l in (ll.strip() for ll in stream) if l)

            for line in reader:
                l = line.split()
                if l[0] == 'p':
                    self.n_packages = int(l[2])
                elif l[0] == 'n':
                    packages.add((l[1]))
                elif l[0] == 'd':
                    dependences.add(frozenset([l[x] for x in range(1,len(l))])) #Alomejor falta ponerlo en una ()
                elif l[0] == 'c':
                    conflicts.add(frozenset([l[1],l[2]]))

            self.packages = tuple(tuple([x]) for x in packages)
            self.dependences = tuple(tuple(x) for x in dependences)
            self.conflicts = tuple(tuple(x) for x in conflicts)
    
    def softwarePackageUpgrades(self,solver):
        pass


def parameters(argv=None):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("solver", help="Path to the MaxSAT solver.")
    parser.add_argument("instance", help="Path to the instance of the problem to solve")
    
    return parser.parse_args(args=argv)

def main(argv=None):
    args = parameters(argv)
    solver = msat_runner.MaxSATRunner(args.solver)
    fs = FileSystem(args.instance)

    spu = fs.softwarePackageUpgrades(solver)
    print("SPU", " ".join(map(str, spu)))

    #print("pck"+str(spu.packages))
    #print("d"+str(spu.dependences))
    #print("c"+str(spu.conflicts))

if __name__ == "__main__":
    sys.exit(main())