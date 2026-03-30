import sys

def main():
    min_sup = int(sys.argv[1])
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    print("min_sup:", min_sup)
    print("input:", input_file)
    print("output:", output_file)

    with open(input_file, 'r') as f:
        data = f.readlines()

    with open(output_file, 'w') as f:
        f.write("test\n")

if __name__ == "__main__":
    main()