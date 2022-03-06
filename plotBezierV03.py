import matplotlib.pyplot as plt
import numpy as np

N = 0
isCubic = False
isAlt = False
xpos = 0
ypos = 0

def calcN(X, Y, iscubic):
    if iscubic == False:
        N = max(abs(2 * X[1]), abs(2 * Y[1]))  # Ax
        N = max(N, abs(2 * (X[2] - 2 * X[1])),
                abs(2 * (Y[2] - 2 * Y[1])))  # 2Bx
        # N = max(N, abs(2 * (X[1] + (X[2] - 2 * X[1]))), # Ax +2Bx
        #           abs(2 * (Y[1] + (Y[2] - 2 * Y[1]))))
        N = max(N, abs(2 * (X[2] - X[1])),
                abs(2 * (Y[2] - Y[1])))  # Ax +2Bx
    else:
        N = max(abs(3*X[1]), abs(3*Y[1]))  # A
        N = max(N, abs(6 * (3 * (X[1] - X[2]) + X[3])),
                abs(6 * (Y[2] - 2 * Y[1])))  # 2bX
        N = max(N, abs(6 * (3*(X[1] - X[2]) + X[3])),
                abs(6 * (3*(Y[1] - Y[2]) + Y[3])))  # ^Cx
        # because N = max(N, abs(3 * X[1] + 6 * (X[2] - 2 * X[1])), 
        #      abs(2 * (Y[1] + (Y[2] - 2 * Y[1])))) # Ax + 2Bx
        N = max(N, abs(6 * X[2] - 9 * X[1]),
                abs(6 * Y[2] - 9 * Y[1]))  # Ax + 2Bx
        # N = max(N, 3 * X[1] + 6 * (X[2] - 2 *X[1]) + 6 * (3*(X[1] - X[2]) + X[3])))
        # N = max(N, 3 * Y[1] + 6 * (Y[2] - 2 *Y[1]) + 6 * (3*(Y[1] - Y[2]) + Y[3])))
        N = max(N, abs(9 * X[1] - 9 * X[2] + 6 * X[3]),
                abs(9*Y[1] - 9*Y[2] + 6 * Y[3]))  # Ax+2Bx+6Cx
    return N

def incrIntBezier(X, Y, N, iscubic):
  
    def divsub(delta, ndx):
        sum[ndx] += delta
        if (sum[ndx] > N / 2):
            sum[ndx] -= N
            return 1
        if (sum[ndx] < -N / 2):
            sum[ndx] += N
            return -1
        return 0

    xincr1 = 0
    yincr1 = 0
    xquot0 = 0
    yquot0 = 0
    xquot2 = 0
    yquot2 = 0
    sum = [0,0,0,0,0,0]
    xstep = 0
    ystep = 0
    xpos = 0
    ypos = 0
    xp = []
    yp = []

    if iscubic == False:
        Ax = 2 * X[1]
        Ay = 2 * Y[1]
        Bx = X[2] - 2 * X[1]
        By = Y[2] - 2 * Y[1]
        Cx = Cy = 0
    else:
        Ax = 3 * X[1]
        Ay = 3 * Y[1]
        Bx = 3 * (X[2] - 2 * X[1])
        By = 3 * (Y[2] - 2 * Y[1])
        Cx = (3 * (X[1] - X[2]) + X[3])
        Cy = (3 * (Y[1] - Y[2]) + Y[3])

    xquot0 = Ax
    yquot0 = Ay
    xquot1 = 2 * Bx
    yquot1 = 2 * By
    xquot2 = 6 * Cx
    yquot2 = 6 * Cy

    for stepcount in range(1, N + 1):
        if iscubic:  # else quadratic Bezier
            xincr1 += divsub(xquot2, 4)
            yincr1 += divsub(yquot2, 5)
        xquot0 += divsub(xquot1 + xincr1, 2)
        yquot0 += divsub(yquot1 + yincr1, 3)
        xstep = divsub(xquot0, 0)
        ystep = divsub(yquot0, 1)
        if (xstep == 0) & (ystep == 0):
            continue
        xpos += xstep
        ypos += ystep
        xp.append(xpos)
        yp.append(ypos)
    return xp, yp

def altIncrIntBezier(X, Y, N, iscubic):
    incr = [0,0,0,0,0,0]
    quot = [0,0,0,0,0,0]
    sum  = [0,0,0,0,0,0]
    div  = [N,N,N,N,N,N]

    xstep = 0
    ystep = 0
    xpos = 0
    ypos = 0
    xp = []
    yp = []
 
    def divsub(ndx):
        sum[ndx] += incr(ndx)
        if (sum[ndx] > div[ndx] / 2):
            sum[ndx] -= div[ndx]
            return 1
        if (sum[ndx] < -div[ndx] / 2):
            sum[ndx] += div[ndx]
            return -1
        return 0

    if iscubic == False:
        Ax = 2 * X[1]
        Ay = 2 * Y[1]
        Bx = X[2] - 2 * X[1]
        By = Y[2] - 2 * Y[1]
        Cx = Cy = 0
    else:
        Ax = 3 * X[1]
        Ay = 3 * Y[1]
        Bx = 3 * (X[2] - 2 * X[1])
        By = 3 * (Y[2] - 2 * Y[1])
        Cx = (3 * (X[1] - X[2]) + X[3])
        Cy = (3 * (Y[1] - Y[2]) + Y[3])

    quot[0] = Ax
    quot[3] = Ay
    quot[1] = 2 * Bx
    quot[4] = 2 * By
    quot[2] = 6 * Cx
    quot[5] = 6 * Cy
    sum[1]  = -Bx
    sum[4]  = -By

    for stepcount in range(1, N + 1):
        if iscubic:  # else quadratic Bezier
            incr[1] += divsub(quot[2], sum[2])
            incr[5] += divsub(quot[5], sum[5])
        quot[0] += divsub(quot[1] + incr[1], sum[1])
        quot[3] += divsub(quot[4] + incr[4], sum[4])
        xstep = divsub(quot[0], sum[0])
        ystep = divsub(quot[3], sum[3])
        if (xstep == 0) & (ystep == 0):
            continue
        xpos += xstep
        ypos += ystep
        xp.append(xpos)
        yp.append(ypos)
    return xp, yp


def floatBezier(X, Y, N, iscubic):
    t = np.linspace(1, N + 1, N)
    s = t / N
    if iscubic == False:
        xf = 2.0 * X[1] * (1.0 - s) * s + X[2] * s * s
        yf = 2.0 * Y[1] * (1.0 - s) * s + Y[2] * s * s
    else:
        xf = 3.0 * X[1] * (1.0 - s) * (1.0 - s) * s + 3.0 * \
            X[2] * (1.0 - s) * s * s + X[3] * s * s * s
        yf = 3.0 * Y[1] * (1.0 - s) * (1.0 - s) * s + 3.0 * \
            Y[2] * (1.0 - s) * s * s + Y[3] * s * s * s
    return xf, yf

def plotBezier(X, Y, iscubic, isalt):
    X.insert(0, 0)  # prepend zero so that X[1] is X1
    Y.insert(0, 0)
    isCubic = iscubic
    N = calcN(X, Y, isCubic)
    if isalt == False:
        xint, yint = incrIntBezier(X, Y, N, isCubic)
    else:
        xint, yint = altIncrIntBezier(X, Y, N, isCubic)
    xf, yf = floatBezier(X, Y, N, isCubic)
    bez = 3 if iscubic else 2
    plt.title(
        f"Bezier{bez}: X1={X[1]}, Y1={Y[1]}, X2={X[2]}, Y2={Y[2]}, X3={X[3]}, Y3={Y[3]}, N={N}", fontsize=9)
    plt.plot(xint, yint, 'b')
    plt.plot(xf, yf, 'r')
    plt.show()


def main():     # simple module tests
    i = 5
    isalt = False
    if i == 0:
        iscubic = True
        X = [11, 33, -111]
        Y = [22, -44, 22]
    elif i == 1:
        iscubic = True
        X = [11, 33, 11]
        Y = [22, -44, 22]
    elif i == 2:
        iscubic = True
        X = [1000, -1000, 2000]
        Y = [5000, 1000, 2000]
    elif i == 3:
        iscubic = True
        isalt = True
        X = [1000, -1000, 2000]
        Y = [5000, 1000, 2000]
    elif i == 4:
        iscubic = False
        X = [-100, 400, 0]
        Y = [100,  0, 0]
    elif i == 5:
        isalt = True
        iscubic = False
        X = [-100, 400, 0]
        Y = [100,  0, 0]
    else:
        iscubic = False
        X = [-10000, 40000, 666]
        Y = [10000,  0, 666]
    isalt = False
    lambda ndx: 2 if iscubic else 1
    plotBezier(X, Y, iscubic, isalt)
    if (xpos != X[3]) | (ypos != Y[3]):
        print("###### ERROR #####")


# if __name__ == "__main__":
#     main()
