import re
import os
import glob
import sys


if len(sys.argv) != 4:
    print('This program needs three parameters: 1. pdb file, 2. fasta file, 3. output folder')
    sys.exit(1)

pdb_file = os.path.abspath(sys.argv[1]) 
fasta = os.path.abspath(sys.argv[2])
dist_folder = os.path.abspath(sys.argv[3])

script_path = os.path.dirname(os.path.realpath(__file__))

if not os.path.exists(dist_folder):
    os.makedirs(dist_folder, exist_ok=True)


if __name__=="__main__":
    # Calculating real dist file
    target = os.path.basename(pdb_file)
    target = re.sub("\.pdb", "", target)
    os.system("perl " + script_path + "/pdb2dist.pl " + pdb_file + " CA 0 8 > " + dist_folder + "/" + target + "_CA.dist")
    os.system("perl " + script_path + "/pdb2dist.pl " + pdb_file + " CB 0 8 > " + dist_folder + "/" + target + "_CB.dist")
    for line_f in open(fasta, "r"):

        if line_f.startswith('>'):
            continue

        line_f = line_f.rstrip()
        custom = len(line_f)
        L=custom
        CB = dict()
        CA = dict()
        f = open(dist_folder + "/" + target + ".dist", "w")

        for line in open(dist_folder + "/" + target + "_CB.dist", "r"):
            line = line.rstrip()
            arr = line.split()
            CB[arr[0] + ' ' + arr[1]] = arr[2]
        
        for line in open(dist_folder + "/" + target + "_CA.dist", "r"):
            line = line.rstrip()
            arr = line.split()
            CA[arr[0] + ' ' + arr[1]] = arr[2]
        
        for i in range(0, L):
            for j in range(i + 1, L):
                if (str(i + 1) + " " + str(j + 1)) in CB:
                    f.write(str(i + 1) + " " + str(j + 1) + " " + CB[str(i + 1) + " " + str(j + 1)] + "\n")
                elif (str(i + 1) + " " + str(j + 1)) in CA:
                    f.write(str(i + 1) + " " + str(j + 1) + " " + CA[str(i + 1) + " " + str(j + 1)] + "\n")
        f.close()

    # Converting real dist file to distance map
    os.system("perl " + script_path + "/generate-Y-realDistance.pl " + fasta + " " + dist_folder + "/" + target + ".dist > " + dist_folder + "/" + target + ".txt")

