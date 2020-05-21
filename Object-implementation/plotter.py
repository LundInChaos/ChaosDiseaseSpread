import numpy as np
import matplotlib.pylab as plt
import matplotlib.animation as animation
from  matplotlib.animation import FuncAnimation
from scipy import signal
import cv2
import copy

class plotter:
    verbal = 0

    def __init__(self, susMat, infMat, remMat):
        self.susMat = susMat
        self.infMat = infMat
        self.remMat = remMat

        self.xSize = susMat.shape[0]
        self.ySize = susMat.shape[1]
        self.iters = susMat.shape[2]

    def plot_all(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for n in range(self.xSize):
            for m in range (self.ySize):
                c1 = [((n + m)/(np.max(self.xSize) + np.max(self.ySize))), 0, 0]
                c2 = [0, ((n + m)/(np.max(self.xSize) + np.max(self.ySize))), 0]
                c3 = [0, 0, ((n + m)/(np.max(self.xSize) + np.max(self.ySize)))]

                if n == (self.xSize-1) and m == (self.ySize-1):
                    l1, = ax.plot(self.susMat[n, m, :], color = c1)
                    l2, = ax.plot(self.infMat[n, m, :], color = c2)
                    l3, = ax.plot(self.remMat[n, m, :], color = c3)

                else:
                    ax.plot(self.susMat[n, m, :], color = c1)
                    ax.plot(self.infMat[n, m, :], color = c2)
                    ax.plot(self.remMat[n, m, :], color = c3)

        plt.legend([l1, l2, l3], ['Susceptible', 'Infected', 'Removed'], loc='center right')
        plt.show()

    def animate_inf_sus(self):
        fig = plt.figure()

        def f1(time):
            return self.susMat[:, :, time]

        def f2(time):
            return self.infMat[:, :, time]

        self.time = -1;

        plt.subplot(1, 2, 1)
        im1 = plt.imshow(f1(self.time), animated=True, vmin=np.min(self.susMat), vmax=np.max(self.susMat))
        plt.title('Susceptibale')

        plt.subplot(1, 2, 2)
        im2 = plt.imshow(f2(self.time), animated=True, vmin=np.min(self.infMat), vmax=np.max(self.infMat))
        plt.title('Infected')

        def updatefig(*args):
            global time
            self.time += 10
            if self.time >= self.iters:
                self.time = 0
            print(self.time)
            im1.set_array(f1(self.time))
            im2.set_array(f2(self.time))
            return im1, im2,

        ani = animation.FuncAnimation(fig, updatefig, frames=10, interval=0.1, blit=True)
        plt.show()

    def animate_all(self):
        fig = plt.figure()

        def f1(time):
            return self.susMat[:, :, time]

        def f2(time):
            return self.infMat[:, :, time]

        def f3(time):
            return self.remMat[:, :, time]

        def iniPlot():
            print("init")
            for n in range(self.xSize):
                for m in range (self.ySize):
                    c1 = [((n + m)/(np.max(self.xSize) + np.max(self.ySize))), 0, 0]
                    c2 = [0, ((n + m)/(np.max(self.xSize) + np.max(self.ySize))), 0]
                    c3 = [0, 0, ((n + m)/(np.max(self.xSize) + np.max(self.ySize)))]

                    if n == (self.xSize-1) and m == (self.ySize-1):
                        l1, = plt.plot(self.susMat[n, m, :], color = c1)
                        l2, = plt.plot(self.infMat[n, m, :], color = c2)
                        l3, = plt.plot(self.remMat[n, m, :], color = c3)

                    else:
                        plt.plot(self.susMat[n, m, :], color = c1)
                        plt.plot(self.infMat[n, m, :], color = c2)
                        plt.plot(self.remMat[n, m, :], color = c3)

            plt.legend([l1, l2, l3], ['Susceptible', 'Infected', 'Removed'], loc='center right')
            plt.xlabel("Time (days)")

            x = np.zeros(self.iters)
            x[100] = 1
            y = np.linspace(0, 1, self.iters)
            #line, = plt.plot(x, y)

            #return line,

        self.time = -1;

        #Writer = animation.writers['ffmpeg']
        #writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

        plt.subplot(2, 2, 1)
        im1 = plt.imshow(f1(self.time), animated=True, vmin=np.min(self.susMat), vmax=np.max(self.susMat))
        plt.title('Susceptibale')

        plt.subplot(2, 2, 2)
        im2 = plt.imshow(f2(self.time), animated=True, vmin=np.min(self.infMat), vmax=np.max(self.infMat))
        plt.title('Infected')

        plt.subplot(2, 2, 3)
        im3 = plt.imshow(f2(self.time), animated=True, vmin=np.min(self.remMat), vmax=np.max(self.remMat))
        plt.title('Removed')

        plt.subplot(2, 2, 4)
        iniPlot()

        def updPlot(time):
            global line

            x = np.zeros(self.iters)
            x[time] = 1
            y = np.linspace(0, 1, self.iters)

            line.set_data(x, y)

            return line,

        def updatefig(*args):
            global time
            self.time += 10
            if self.time >= self.iters:
                self.time = 0

            if self.verbal == 5:
                v = f1(self.time)
                print(v)
            print(self.time)

            im1.set_array(f1(self.time))
            im2.set_array(f2(self.time))
            im3.set_array(f3(self.time))

            return im1, im2, im3,

        ani = animation.FuncAnimation(fig, updatefig, frames=10, interval=0.1, blit=True)
        #ani.save('lines.mp4', writer=writer)
        plt.show()

    def phase_diagrams(self, x, y):
        fig = plt.figure()

        plt.subplot(2, 2, 1)
        p1 = plt.plot(self.susMat[x,y,0:-1], np.diff(self.susMat[x,y,:]))
        plt.title('Susceptibale')
        plt.xlabel("S")
        plt.ylabel("dS/dt")

        plt.subplot(2, 2, 2)
        p1 = plt.plot(self.infMat[x,y,0:-1], np.diff(self.infMat[x,y,:]))
        plt.title('Infected')
        plt.xlabel("I")
        plt.ylabel("dI/dt")

        plt.subplot(2, 2, 3)
        p1 = plt.plot(self.remMat[x,y,0:-1], np.diff(self.remMat[x,y,:]))
        plt.title('Removed')
        plt.xlabel("R")
        plt.ylabel("dR/dt")

        plt.show()

    def biforcation_diagram(self, num, para):
        fig = plt.figure()

        ax1 = plt.subplot(2, 2, 1)
        plt.title('Susceptibale')
        plt.xlabel("Parameter")

        ax2 = plt.subplot(2, 2, 2)
        plt.title('Infected')
        plt.xlabel("Parameter")

        ax3 = plt.subplot(2, 2, 3)
        plt.title('Removed')
        plt.xlabel("Parameter")

        for n in range(self.xSize):
            for m in range (self.ySize):
                c1 = [((n + m)/(np.max(self.xSize) + np.max(self.ySize))), 0, 0]
                c2 = [0, ((n + m)/(np.max(self.xSize) + np.max(self.ySize))), 0]
                c3 = [0, 0, ((n + m)/(np.max(self.xSize) + np.max(self.ySize)))]

                if n < 2 and m < 1 and self.verbal == 1:
                    print(self.infMat[n, m, -num:])
                    print(para[n,m])

                ax1.plot(np.ones((num))*para[n,m], self.susMat[n, m, -num:], '.', color = c1)
                ax2.plot(np.ones((num))*para[n,m], self.infMat[n, m, -num:], '.', color = c2)
                ax3.plot(np.ones((num))*para[n,m], self.remMat[n, m, -num:], '.', color = c3)

        plt.show()

