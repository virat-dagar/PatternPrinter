def rectangle_solid(design, l, b):
    # Print a solid rectangle of dimensions l x b
    for i in range(b):
        for j in range(l):
            print(f'{design} ', end='')
        print()

def rectangle_hollow(design, l, b):
    # Print a hollow rectangle with stars only at borders
    for i in range(b):
        for j in range(l):
            if i == 0 or i == b-1 or j == 0 or j == l-1:
                print(f'{design} ', end='')
            else:
                print('  ', end='')
        print()

def right_angle_tri_hypo_right(design, n):
    # Triangle with right angle on bottom-left; hypotenuse goes right
    for i in range(n):
        for j in range(i+1):
            print(f'{design}', end='')
        print()

def right_angle_tri_hypo_right_reverse(design, n):
    # Reversed version; right angle on top-left; hypotenuse goes right and down
    for i in range(n):
        for j in range(i, n):
            print(f'{design}', end='')
        print()

def right_angle_tri_hypo_right_reverse_holllow(design, n):
    # Hollow reversed right triangle; border stars only
    for i in range(n):
        for j in range(i, n):
            if i == 0 or i == n-1:
                print(f'{design}', end='')  # Top or bottom row is fully filled
            elif j == i or j == n-1:
                print(f'{design}', end='')  # Diagonal or last column
            else:
                print(' ', end='')
        print()

def right_angle_tri_hypo_right_hollow(design, n):
    # Hollow triangle with hypotenuse on right side
    for i in range(n):
        for j in range(i+1):
            if i == 0 or i == n-1:
                print(f'{design}', end='')  # Top and bottom fully filled
            elif j == 0 or j == i:
                print(f'{design}', end='')  # Borders of triangle
            else:
                print(' ', end='')
        print()

def right_angle_tri_hypo_left(design, n):
    # Right triangle aligned rightwards; right angle on bottom-right
    for i in range(1, n+1):
        for j in range(i, n):
            print(' ', end='')  # Left padding
        for j in range(i):
            print(f'{design}', end='')
        print()

def right_angle_tri_hypo_left_reverse(design, n):
    # Reversed triangle; right angle on top-right
    for i in range(n):
        for j in range(i):
            print(' ', end='')  # Leading spaces
        for j in range(i, n):
            print(f'{design}', end='')
        print()

def right_angle_tri_hypo_left_reverse_hollow(design, n):
    # Currently prints solid reversed left triangle
    for i in range(n):
        for j in range(i):
            print(' ', end='')
        for j in range(i, n):
            print(f'{design}', end='')
        print()
    # Note: can be modified to add hollow logic if desired

def right_angle_tri_hypo_left_hollow(design, n):
    # Hollow triangle with right angle bottom-right, aligned to right
    for i in range(1, n+1):
        for j in range(i, n):
            print(' ', end='')  # Left padding
        for j in range(i):
            if j == 0 or j == i-1 or i == n:
                print(f'{design}', end='')  # Borders and base
            else:
                print(' ', end='')
        print()

def hill(design, n):
    # Full pyramid (hill) pattern; center-aligned
    for i in range(n):
        for j in range(i, n-1):
            print(' ', end='')  # Left padding
        for j in range(i):
            print(f'{design}', end='')  # Left half
        for j in range(i+1):
            print(f'{design}', end='')  # Right half
        print()

def hill_reverse(design, n):
    # Inverted pyramid; base at top
    for i in range(n):
        for j in range(i):
            print(' ', end='')  # Left padding
        for j in range(i, n):
            print(f'{design}', end='')  # Left half
        for j in range(i, n-1):
            print(f'{design}', end='')  # Right half
        print()

def hill_reverse_hollow(design, n):
    # Hollow version of inverted hill
    for i in range(n):
        for j in range(i):
            print(' ', end='')
        for j in range(i, n):
            if i == 0 or i == n-1 or j == i:
                print(f'{design}', end='')  # Top row or left border
            else:
                print(' ', end='')
        for j in range(i, n-1):
            if i == 0 or i == n-1 or j == n-2:
                print(f'{design}', end='')  # Top row or right border
            else:
                print(' ', end='')
        print()

def hill_hollow(design, n):
    # Hollow hill/pyramid with stars on boundary only
    for i in range(n):
        for j in range(i, n):
            print(' ', end='')  # Left padding
        for j in range(i):
            if i == 0 or i == n-1 or j == 0:
                print(f'{design}', end='')  # Left slope
            else:
                print(' ', end='')
        for j in range(i+1):
            if j == i or i == 0 or i == n-1:
                print(f'{design}', end='')  # Right slope
            else:
                print(' ', end='')
        print()

def diamond_printing_with_for_loop(design, n):
    # Diamond pattern by merging upward and downward pyramids
    for i in range(n - 1):
        for j in range(i, n-1):
            print(' ', end='')  # Left padding
        for j in range(i):
            print(f'{design}', end='')
        for j in range(i + 1):
            print(f'{design}', end='')
        print()
        
    for i in range(n):
        for j in range(i):
            print(' ', end='')
        for j in range(i, n - 1):
            print(f'{design}', end='')
        for j in range(i, n):
            print(f'{design}', end='')
        print()

def diamond_printing_with_for_loop_holllow(design, n):
    # Hollow diamond pattern
    for i in range(n):
        for j in range(i, n-1):
            print(' ', end='')
        for j in range(i):
            if j == 0:
                print(f'{design}', end='')  # Left slope
            else:
                print(' ', end='')
        for j in range(i+1):
            if j == i:
                print(f'{design}', end='')  # Right slope
            else:
                print(' ', end='')   
        print()
    
    for i in range(n-1):
        for j in range(i+1):
            print(' ', end='')
        for j in range(i, n-1):
            if j == i:
                print(f'{design}', end='')  # Left slope
            else:
                print(' ', end='')   
        for j in range(i, n-2):
            if j == n-3:
                print(f'{design}', end='')  # Right slope
            else:
                print(' ', end='')
        print()



patterns = {
    'solid rectangle': rectangle_solid,
    
    'hollow rectangle': rectangle_hollow,
    
    'right-angled triangle with hypotenuse to the right': right_angle_tri_hypo_right,
    
    'hollow right-angled triangle with hypotenuse to the right': right_angle_tri_hypo_right_hollow,
    
    'reversed right-angled triangle with hypotenuse to the right': right_angle_tri_hypo_right_reverse,
    
    'hollow reversed right-angled triangle with hypotenuse to the right': right_angle_tri_hypo_right_reverse_holllow,
    
    'right-angled triangle with hypotenuse to the left': right_angle_tri_hypo_left,
    
    'hollow right-angled triangle with hypotenuse to the left': right_angle_tri_hypo_left_hollow,
    
    'reversed right-angled triangle with hypotenuse to the left': right_angle_tri_hypo_left_reverse,
    
    'hollow reversed right-angled triangle with hypotenuse to the left': right_angle_tri_hypo_left_reverse_hollow,
    
    'full hill pattern': hill,
    
    'hollow hill pattern': hill_hollow,
    
    'inverted hill pattern': hill_reverse,
    
    'hollow inverted hill pattern': hill_reverse_hollow,
    
    'solid diamond pattern': diamond_printing_with_for_loop,
    
    'hollow diamond pattern': diamond_printing_with_for_loop_holllow
}



pattern_list = list(patterns.keys())

print("Available patterns:")
for idx, name in enumerate(pattern_list, start=1):
    print(f"{idx}. {name}")

try:
    choice = int(input("Enter the serial number of your chosen pattern: "))
    if 1 <= choice <= len(pattern_list):
        pattern_name = pattern_list[choice - 1]
        if 'rectangle' in pattern_name.lower():
            l = int(input('Enter length of rectangle: '))
            b = int(input('Enter breadth of rectangle: '))
            design = input('enter the design you would like the pattern to be in: ')
            patterns[pattern_name](design, l, b)
        else:
            n = int(input('Enter number of lines: '))
            design = input('enter the design you would like the pattern to be in: ')
            patterns[pattern_name](design, n)
    else:
        print("Invalid serial number. Please try again.")
except ValueError:
    print("Invalid input. Please enter a number.")
