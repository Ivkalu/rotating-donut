
import numpy as np
from math import cos, sin
import sys
import os

def main():
    A, B = 0,0
    WIDTH, HEIGHT = 80, 40
    
    R1 = float(os.environ.get("R1", 1))
    R2 = float(os.environ.get("R2", 2))
    K2 = float(os.environ.get("K2", 5))
    K1 = float(os.environ.get("K1", 15.625))

    r,g,b = 150,0,80
    chars =  ".,-~:;=!*#$@"
    theta_inc = 0.07*2
    phi_inc = 0.02*2
    source = np.array([0, 1, -1])

    while True:

        output = [' '] * (WIDTH * HEIGHT)
        zbuffer = [0] * (WIDTH * HEIGHT)
        
        for theta in np.arange(0, 6.28, theta_inc):
            for phi in np.arange(0, 6.28, phi_inc):
                
                mat = np.array([R2 + R1*cos(theta), R1*sin(theta), 0])
                luminance = np.array([cos(theta), sin(theta), 0])
                
                mat1 = np.array([
                    [sin(phi), cos(phi), 0],
                    [0, 0, 1],
                    [cos(phi), -sin(phi), 0],
                ])
                mat2 = np.array([
                    [1, 0, 0],
                    [0, cos(A), sin(A)],
                    [0, -sin(A), cos(A)],
                ])
                mat3 = np.array([
                    [cos(B), sin(B), 0],
                    [-sin(B), cos(B), 0],
                    [0, 0, 1],
                ])
                
                x, y, z = mat@mat1@mat2@mat3
                normal = luminance@mat1@mat2@mat3
                
                L = normal@source/np.linalg.norm(source)
                ooz = 1/(z+K2)

                xp = int(WIDTH/2+ 1.5*K1*ooz*x)
                yp = int(HEIGHT/2-K1*ooz*y)

                position = xp+WIDTH*yp
                if 0 < position < len(zbuffer) and ooz > zbuffer[position]: 
                    zbuffer[position] = ooz
                    output[position] = chars[int(L*len(chars))] if int(L*len(chars)) > 0 else ' '

        print('\033c', end="")
        if os.environ.get("DISABLE_COLOR", '').lower() != "true":
            r,g,b = r+1, g-3, b+6
            print(f'\033[38;2;{r%255};{g%255};{b%255}m', end="")
        for k in range(WIDTH * HEIGHT):
            print(output[k], end="\n" if k % WIDTH == WIDTH - 1 else "")
        
        A += 0.04
        B += 0.02
                        
if __name__ == "__main__":
    if '-h' in sys.argv:
        print("Usage: \'[K1=<env>] [K2=<env>] [R1=<env>] [R2=<env>] python dougnut.py [-c]\'")
        exit()
    if '-c' in sys.argv:
        os.environ["DISABLE_COLOR"]="True"
    main()
