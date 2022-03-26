import argparse

from assembler.assembler import AsmError, assemble


def main():
    parser = argparse.ArgumentParser(description="H6809 Assembler")
    parser.add_argument("filename", type=str, help="Program file (.asm)")

    args = parser.parse_args()

    if not args.filename:
        print("No filename specified.")
        exit(1)

    if not args.filename.endswith(".asm"):
        print("Unsupported file type.")

    try:
        with open(args.filename) as file:
            binary_code, org, start = assemble(file)
            print(binary_code, org, start)
    except AsmError as exc:
        print(exc.message)
    except Exception as exc:
        print(exc)


if __name__ == "__main__":
    main()
