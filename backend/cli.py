from backend.patterns import list_patterns, render_pattern


def main() -> None:
    patterns = list_patterns()

    print("Available patterns:")
    for index, pattern in enumerate(patterns, start=1):
        print(f"{index}. {pattern['name']}")

    try:
        choice = int(input("Enter the serial number of your chosen pattern: "))
        selected = patterns[choice - 1]
    except (ValueError, IndexError):
        print("Invalid selection. Please run the program again.")
        return

    symbol = input("Enter the design symbol you would like to use: ") or "*"

    if selected["requires_rectangle"]:
        width = int(input("Enter rectangle width: "))
        height = int(input("Enter rectangle height: "))
        output = render_pattern(selected["id"], symbol=symbol, width=width, height=height)
    else:
        size = int(input("Enter number of lines: "))
        output = render_pattern(selected["id"], symbol=symbol, size=size)

    print(output)


if __name__ == "__main__":
    main()
