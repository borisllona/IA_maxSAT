import argparse
import sys
import msat_runner
import wcnf

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
        dependences,conflicts,packages = [],[],[]
        
        with open(file_path, 'r') as stream:
            reader = (l for l in (ll.strip() for ll in stream) if l)

            for line in reader:
                l = line.split()
                if l[0] == 'p':
                    self.n_packages = int(l[2])
                elif l[0] == 'n':
                    packages.append((l[1]))
                elif l[0] == 'd':
                    dependences.append(list([l[x] for x in range(1,len(l))])) #Alomejor falta ponerlo en una ()
                elif l[0] == 'c':
                    conflicts.append(list([l[1],l[2]]))

            self.packages = tuple(tuple([x]) for x in packages)
            self.dependences = tuple(tuple(x) for x in dependences)
            self.conflicts = tuple(tuple(x) for x in conflicts)


    def softwarePackageUpgrades(self,solver):
        packages = {}
        result = []
        formula = wcnf.WCNFFormula()

        for el in self.packages:
            packages[el[0]] = formula.new_var() 
        
        #Soft Clauses
        for p in packages.values():
            formula.add_clause([p],weight=1)

        #Hard Clauses
        for d in self.dependences:
            pklist = []
            for pk in d:
                if d[0] == pk: pklist.append(-packages[pk]) 
                else: pklist.append(packages[pk])
            formula.add_clause(pklist,weight=wcnf.TOP_WEIGHT)    

        for c1, c2 in self.conflicts:
            v1, v2 = packages[c1], packages[c2]
            formula.add_clause([-v1,-v2],weight=wcnf.TOP_WEIGHT)

        opt, model = solver.solve(formula)
        print(len(self.packages))
        for i in model: #Search the values of files that can't be used and then gets their name
            if i<0: result.append(list(packages.keys())[list(packages.values()).index(-i)]) 
        
        print("o:",opt)
        print("v:", " ".join(sorted(result)))

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

if __name__ == "__main__":
    #python spu_solver.py ./maxino-static instances/software-package-upgrades/sample.spu 
    sys.exit(main())