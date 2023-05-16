import os
import random as rnd
from math import *
import pandas as pd
import imageio
import matplotlib.pyplot as plt


def F(x, y):
    return 8 * x * x + 4 * x * y + 5 * y * y


def F1(x, y):
    return (y - x * x) ** 2 + 100 * (1 - x) ** 2


class Unit:

    def __init__(self, start, end, currentVelocityRatio, localVelocityRatio, globalVelocityRatio, function):
        # область поиска
        self.start = start
        self.end = end
        # коэффициенты для изменения скорости
        self.currentVelocityRatio = currentVelocityRatio
        self.localVelocityRatio = localVelocityRatio
        self.globalVelocityRatio = globalVelocityRatio
        # функция
        self.function = function
        # лучшая локальная позиция
        self.localBestPos = self.getFirsPos()
        self.localBestScore = self.function(*self.localBestPos)
        # текущая позиция
        self.currentPos = self.localBestPos[:]
        self.score = self.function(*self.localBestPos)
        # значение глобальной позиции
        self.globalBestPos = []
        # скорость
        self.velocity = self.getFirstVelocity()

    def getFirstVelocity(self):
        """ Метод для задания первоначальной скорости"""
        minval = -(self.end - self.start)
        maxval = self.end - self.start
        return [rnd.uniform(minval, maxval), rnd.uniform(minval, maxval)]

    def getFirsPos(self):
        """ Метод для получения начальной позиции"""
        return [rnd.uniform(self.start, self.end), rnd.uniform(self.start, self.end)]

    def nextIteration(self):
        """ Метод для нахождения новой позиции частицы"""
        # случайные данные для изменения скорости
        rndCurrentBestPosition = [rnd.random(), rnd.random()]
        rndGlobalBestPosition = [rnd.random(), rnd.random()]
        # делаем перерасчет скорости частицы исходя из всех введенных параметров
        velocityRatio = self.localVelocityRatio + self.globalVelocityRatio
        commonVelocityRatio = 2 * self.currentVelocityRatio / abs(2 - velocityRatio - sqrt(velocityRatio ** 2 - 4 * velocityRatio))
        multLocal = list(map(lambda x: x * commonVelocityRatio * self.localVelocityRatio, rndCurrentBestPosition))
        betweenLocalAndCurPos = [self.localBestPos[0] - self.currentPos[0], self.localBestPos[1] - self.currentPos[1]]
        betweenGlobalAndCurPos = [self.globalBestPos[0] - self.currentPos[0],
                                  self.globalBestPos[1] - self.currentPos[1]]
        multGlobal = list(map(lambda x: x * commonVelocityRatio * self.globalVelocityRatio, rndGlobalBestPosition))
        newVelocity1 = list(map(lambda coord: coord * commonVelocityRatio, self.velocity))
        newVelocity2 = [coord1 * coord2 for coord1, coord2 in zip(multLocal, betweenLocalAndCurPos)]
        newVelocity3 = [coord1 * coord2 for coord1, coord2 in zip(multGlobal, betweenGlobalAndCurPos)]
        self.velocity = [coord1 + coord2 + coord3 for coord1, coord2, coord3 in
                         zip(newVelocity1, newVelocity2, newVelocity3)]
        # передвигаем частицу и смотрим, какое значение целевой фунции получается
        self.currentPos = [coord1 + coord2 for coord1, coord2 in zip(self.currentPos, self.velocity)]
        newScore = self.function(*self.currentPos)
        if newScore < self.localBestScore:
            self.localBestPos = self.currentPos[:]
            self.localBestScore = newScore
        return newScore


class Swarm:

    def __init__(self, sizeSwarm,
                 currentVelocityRatio,
                 localVelocityRatio,
                 globalVelocityRatio,
                 numbersOfLife,
                 function,
                 start,
                 end):
        # размер популяции частиц
        self.sizeSwarm = sizeSwarm
        # коэффициенты изменения скорости
        self.currentVelocityRatio = currentVelocityRatio
        self.localVelocityRatio = localVelocityRatio
        self.globalVelocityRatio = globalVelocityRatio
        # количество итераций алгоритма
        self.numberLives = numbersOfLife
        # функция для поиска экстремума
        self.function = function
        # область поиска
        self.start = start
        self.end = end
        # рой частиц
        self.swarm = []
        # данные о лучшей позиции
        self.globalBestPos = []
        self.globalBestScore = float('inf')
        self.bestVector = []
        #
        self.oldPopulation = []
        self.file = 'swarm.gif'
        # создаем рой
        self.createSwarm()



    def saveSwarm(self, swarm):
        vec = []
        for individ in swarm:
            vec.append([swarm.index(individ)+1, round(individ.score, 4), *individ.currentPos])
        df = pd.DataFrame(vec, columns=['Индекс', 'Целевое значение', 'X', 'Y'])
        df = df.set_index('Индекс')
        self.oldPopulation.append(df)

    def createSwarm(self):
        """ Метод для создания нового роя"""
        pack = [self.start, self.end, self.currentVelocityRatio, self.localVelocityRatio, self.globalVelocityRatio,
                self.function]
        self.swarm = [Unit(*pack) for _ in range(self.sizeSwarm)]
        # пересчитываем лучшее значение для только что созданного роя
        for unit in self.swarm:
            if unit.localBestScore < self.globalBestScore:
                self.globalBestScore = unit.localBestScore
                self.globalBestPos = unit.localBestPos
        self.saveSwarm(self.swarm)
        self.bestVector.append(self.globalBestScore)

    def startSwarm(self):
        """ Метод для запуска алгоритма"""
        dataForGIF = []
        for _ in range(self.numberLives):
            oneDataX = []
            oneDataY = []
            for unit in self.swarm:
                oneDataX.append(unit.currentPos[0])
                oneDataY.append(unit.currentPos[1])
                unit.globalBestPos = self.globalBestPos
                score = unit.nextIteration()
                if score < self.globalBestScore:
                    self.globalBestScore = score
                    self.globalBestPos = unit.localBestPos
            dataForGIF.append([oneDataX, oneDataY])
            self.saveSwarm(self.swarm)
            self.bestVector.append(self.globalBestScore)

        # рисуем gif
        fnames = []
        i = 0
        # dataForGIF = []
        for x, y in dataForGIF:
            i += 1
            fname = f"g{i}.png"
            fig, (ax1, ax2) = plt.subplots(1, 2)
            fig.suptitle(f"Итерация: {i}")
            ax2.plot(x, y, 'bo')
            ax2.set_xlim(self.start, self.end)
            ax2.set_ylim(self.start, self.end)
            ax1.plot(x, y, 'bo')
            fig.savefig(fname)
            plt.close()
            fnames.append(fname)

        with imageio.get_writer('swarm.gif', mode='I') as writer:
            for filename in fnames:
                image = imageio.imread(filename)
                writer.append_data(image)

        for filename in set(fnames):
            os.remove(filename)


#a = Swarm(650, 0.1, 1, 5, 200, F, -30, 30)
#a.startSwarm()
#print("РЕЗУЛЬТАТ:", a.globalBestScore, "В ТОЧКЕ:", a.globalBestPos)
