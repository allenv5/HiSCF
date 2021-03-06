import sys
import getopt
import TriangleMotifGenerator as triMG
import RectangleMotifGenerator as recMG
import TriangleTensorDataGenerator as triTDG
import RectangleTensorDataGenerator as recTDG


if __name__ == "__main__":
    input_file = ''
    output_file = ''
    motif = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:m:", ['input=', 'output=', 'motif='])
    except getopt.GetoptError:
        print('main.py -i <GraphFile> -o <OutputFile> -m <MotifType>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <GraphFile> -o <OutputFile> -m <MotifType>')
            sys.exit()
        elif opt in ("-i", "--input"):
            input_file = arg
        elif opt in ("-o", "--output"):
            output_file = arg
        elif opt in ("-m", "--motif"):
            motif = arg

    motif = int(motif)
    if motif == 1:
        motif_file = triMG.run(input_file)
        triTDG.run(motif_file, output_file)
    elif motif == 2:
        motif_file = recMG.run(input_file)
        recTDG.run(motif_file, output_file)
    else:
        print('error')
