import io

import PySimpleGUI as sg
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageTk, ImageSequence
from matplotlib import cm
from matplotlib.backends.backend_tkagg import FigureCanvasAgg
from matplotlib.ticker import NullFormatter  # useful for `logit` scale

import evolution
import swarm

sg.theme('NeutralBlue')


def MachineLearningGUI():
    sg.set_options(text_justification='right')

    # flags = [[sg.CB('Normalize', size=(12, 1), default=True), sg.CB('Verbose', size=(20, 1))],
    #          [sg.CB('Cluster', size=(12, 1)), sg.CB(
    #              'Flush Output', size=(20, 1), default=True)],
    #          [sg.CB('Write Results', size=(12, 1)), sg.CB(
    #              'Keep Intermediate Data', size=(20, 1))],
    #          [sg.CB('Normalize', size=(12, 1), default=True),
    #           sg.CB('Verbose', size=(20, 1))],
    #          [sg.CB('Cluster', size=(12, 1)), sg.CB(
    #              'Flush Output', size=(20, 1), default=True)],
    #          [sg.CB('Write Results', size=(12, 1)), sg.CB('Keep Intermediate Data', size=(20, 1))], ]

    loss_functions = [[sg.Rad('8*x*x+4*x*y+5*y*y', 'loss', size=(16, 1)),
                       sg.Rad('5*x*y+4-y*2', 'loss', default=True, size=(16, 1))], ]

    command_line_parms = [[sg.Text('Number of individuals/Size of swarm', size=(30, 1)),
                           sg.Spin(values=[i for i in range(1, 1000)], initial_value=100, size=(6, 1), readonly=True)],
                          [sg.Text("Options for genetic algorithm")],
                          [sg.Text('Part of population with offspring', size=(25, 1), pad=((7, 3))),
                           sg.Spin(values=[i / 10 for i in range(1, 10)], initial_value=0.1, size=(6, 1),
                                   readonly=True)],
                          [sg.Text('Number of mutation step', size=(20, 1)),
                           sg.Spin(values=[i for i in range(1, 50)], initial_value=20, size=(6, 1), readonly=True),
                           sg.Text('Chance of mutations', size=(25, 1), pad=((7, 3))),
                           sg.Spin(values=[i / 10 for i in range(0, 10)], initial_value=0.1, size=(6, 1),
                                   readonly=True)],
                          [sg.Text('Options for swarm algorithm')],
                          [sg.Text('Current velocity ratio', size=(20, 1), pad=((7, 3))),
                           sg.Spin(values=[i / 10 for i in range(1, 100)], initial_value= 1.0, size=(6, 1),
                                   readonly=True)],
                          [sg.Text('Local velocity ratio', size=(20, 1)),
                           sg.Spin(values=[i / 10 for i in range(1, 100)], initial_value= 1.0, size=(6, 1),
                                   readonly=True),
                           sg.Text('Global velocity ratio', size=(25, 1), pad=((7, 3))),
                           sg.Spin(values=[i / 10 for i in range(40, 100)], initial_value= 5.0, size=(6, 1),
                                   readonly=True)],
                          [sg.Text('General options')],
                          [sg.Text('Number of lives', size=(20, 1)),
                           sg.Spin(values=[i for i in range(1, 150)], initial_value=30, size=(6, 1), readonly=True)],
                          [sg.Text('Start of interval', size=(20, 1)),
                           sg.Spin(values=[i for i in range(-100, 0)], initial_value=-30, size=(6, 1), readonly=True),
                           sg.Text('End of interval', size=(25, 1), pad=((7, 3))),
                           sg.Spin(values=[i for i in range(1, 100)], initial_value=30, size=(6, 1), readonly=True)], ]

    layout = [[sg.Frame('Parameters', command_line_parms, title_color='green', font='Any 12')],
              # [sg.Frame('Flags', flags, font='Any 12', title_color='blue')],
              [sg.Frame('Loss Functions', loss_functions,
                        font='Any 12', title_color='red')],
              [sg.Submit(button_text='Both algorithm'), sg.Button("Evolution"), sg.Button("Swarm"), sg.Cancel()]]

    sg.set_options(text_justification='left')

    window = sg.Window('Algorithms',
                       layout, font=("Helvetica", 12))
    event, values = window.read()
    if event == "Both algorithm":
        values["mode"] = '0'
    elif event == "Evolution":
        values["mode"] = '1'
    elif event == "Swarm":
        values["mode"] = '2'
    window.close()
    print(event, values)
    return values


def create_figure(alg):
    fig, ax = plt.subplots()
    ax.plot(alg.bestVector, color='red')
    try:
        ax.plot(alg.meanVector, color='green')
        ax.set_xlabel('Поколение')
        ax.set_ylabel('Макс/средняя приспособленность')
        fig.suptitle('Зависимость максимальной и средней приспособленности от поколения')

    except:
        ax.set_xlabel('Поколение')
        ax.set_ylabel('Макс приспособленность')
        fig.suptitle('Зависимость максимальной и средней приспособленности от поколения')

    return fig


def create_gif(alg):
    gif_filename = alg.file

    layout = [[sg.Button('Again', key='but')],
              [sg.Image(key='-IMAGE-')]]

    window = sg.Window('Evolution gif', layout, element_justification='c', margins=(0, 0), element_padding=(0, 0),
                       finalize=True)

    window['-IMAGE-'].expand(True, True, True)  # Make the Text element expand to take up all available space

    interframe_duration = Image.open(gif_filename).info['duration']  # get how long to delay between frames

    while True:
        for frame in ImageSequence.Iterator(Image.open(gif_filename)):
            event, values = window.read(timeout=interframe_duration)
            if event == sg.WIN_CLOSED:
                window.CloseNonBlocking()
                return
            window['-IMAGE-'].update(data=ImageTk.PhotoImage(frame))
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.CloseNonBlocking()
            return
        elif event == 'Again':
            continue


def pandas_population(alg):
    print('hahah')
    df = alg.oldPopulation[0]
    data = df.values.tolist()  # read everything else into a list of rows
    header_list = list(df.columns)
    table = sg.Table(values=data,
                     headings=header_list,
                     display_row_numbers=True,
                     border_width=2,
                     key='tab',
                     font=30,
                     auto_size_columns=True,
                     num_rows=min(30, len(data)))
    layout = [[sg.Text('Number of population', size=(20, 1)),
               sg.Spin(values=[i for i in range(-9999, 9999)], key='spin', initial_value=0, size=(6, 1)),
               sg.Button('Enter')],
              [table]
              ]

    window = sg.Window('Table', layout, grab_anywhere=False)
    while True:
        event, values = window.read()
        print(values)
        if event == sg.WIN_CLOSED:
            window.close()
            return
        if event == 'Enter':
            if int(values['spin']) > a.numberLives - 1:
                df = a.oldPopulation[a.numberLives - 1]
            elif int(values['spin']) < 0:
                df = a.oldPopulation[1]
            else:
                df = a.oldPopulation[int(values['spin'])]
            window['tab'].update(values=df.values.tolist())


def create_subplot_3d(alg):
    fig = plt.figure()

    ax = fig.add_subplot(1, 2, 1, projection='3d')
    X = np.arange(-10, 10, 0.25)
    Y = np.arange(-10, 10, 0.25)
    X, Y = np.meshgrid(X, Y)
    # R = np.sqrt(X ** 2 + Y ** 2)
    # Z = np.sin(R)
    Z = alg.function(X, Y)
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    # ax.set_zlim3d(-1.01, 1.01)

    fig.colorbar(surf, shrink=1, aspect=5)

    ax = fig.add_subplot(1, 2, 2, projection='3d')
    ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
    return fig


def create_pyplot_scales():
    plt.close('all')
    # Fixing random state for reproducibility
    np.random.seed(19680801)

    # make up some data in the interval ]0, 1[
    y = np.random.normal(loc=0.5, scale=0.4, size=1000)
    y = y[(y > 0) & (y < 1)]
    y.sort()
    x = np.arange(len(y))

    # plot with various axes scales
    plt.figure(1)

    # linear
    plt.subplot(221)
    plt.plot(x, y)
    plt.yscale('linear')
    plt.title('linear')
    plt.grid(True)

    # log
    plt.subplot(222)
    plt.plot(x, y)
    plt.yscale('log')
    plt.title('log')
    plt.grid(True)

    # symmetric log
    plt.subplot(223)
    plt.plot(x, y - y.mean())
    plt.yscale('symlog', linthreshy=0.01)
    plt.title('symlog')
    plt.grid(True)

    # logit
    plt.subplot(224)
    plt.plot(x, y)
    plt.yscale('logit')
    plt.title('logit')
    plt.grid(True)
    # Format the minor tick labels of the y-axis into empty strings with
    # `NullFormatter`, to avoid cumbering the axis with too many labels.
    plt.gca().yaxis.set_minor_formatter(NullFormatter())
    # Adjust the subplot layout, because the logit one may take more space
    # than usual, due to y-tick labels like "1 - 10^{-3}"
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
                        wspace=0.35)
    return plt.gcf()


# ----------------------------- The draw figure helpful function -----------------------------

def draw_figure(element, figure):
    """
    Draws the previously created "figure" in the supplied Image Element

    :param element: an Image Element
    :param figure: a Matplotlib figure
    :return: The figure canvas
    """

    plt.close('all')  # erases previously drawn plots
    canv = FigureCanvasAgg(figure)
    buf = io.BytesIO()
    canv.print_figure(buf, format='png')
    if buf is None:
        return None
    buf.seek(0)
    element.update(data=buf.read())
    return canv


# ----------------------------- The GUI Section -----------------------------

def animation(alg):
    dictionary_of_figures = {'Subplot 3D': create_subplot_3d,
                             'Table of evolution': pandas_population,
                             'Adaptability chart': create_figure,
                             'Evolution gif': create_gif}

    left_col = [[sg.T('Figures to Draw')],
                [sg.Listbox(list(dictionary_of_figures), default_values=[list(dictionary_of_figures)[0]], size=(15, 5),
                            key='-LB-')],
                [sg.T('Matplotlib Styles')],
                [sg.Combo(plt.style.available, key='-STYLE-')]]
    try:
        layout = [[sg.T('Statistics and plots', font='Any 20')],
              [sg.T("Number of lives: " + str(alg.numberLives) + "; Number of compute adaptability function: " + str(
                  alg.numberOfCompute))],
              [sg.T('Best score: ' + str(round(alg.bestScore, 4)))],
              [sg.Column(left_col), sg.Image(key='-IMAGE-')],
              [sg.B('Draw'), sg.B('Exit')]]
    except:
        layout = [[sg.T('Statistics and plots', font='Any 20')],
                  #[sg.T("Number of lives: " + str(alg.numberLives) + "; Number of compute adaptability function: " + str(
                  #    alg.numberOfCompute))],
                  [sg.T('Best score: ' + str(round(alg.globalBestScore, 4)))],
                  [sg.Column(left_col), sg.Image(key='-IMAGE-')],
                  [sg.B('Draw'), sg.B('Exit')]]

    window = sg.Window('Evolution algorithm', layout)

    image_element = window['-IMAGE-']  # type: sg.Image

    while True:
        event, values = window.read()
        print(event, values)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        if event == 'Draw' and values['-LB-']:
            # Get the function to call to make figure. Done this way to get around bug in Web port (default value not working correctly for listbox)
            func = dictionary_of_figures.get(values['-LB-'][0], list(dictionary_of_figures.values())[0])
            if values['-STYLE-']:
                plt.style.use(values['-STYLE-'])
            if func == create_gif:
                create_gif(alg)
            elif func == pandas_population:
                pandas_population(alg)
            else:
                draw_figure(image_element, func(alg))

    window.close()


def new_animation():
    dictionary_of_figures = {'Subplot 3D': create_subplot_3d,
                             'Table of evolution': pandas_population,
                             'Table of swarm': pandas_population,
                             'Adaptability chart evolution': create_figure,
                             'Adaptability chart swarm': create_figure,
                             'Evolution gif': create_gif,
                             'Swarm gif': create_gif}

    left_col = [[sg.T('Figures to Draw')],
                [sg.Listbox(list(dictionary_of_figures), default_values=[list(dictionary_of_figures)[0]], size=(30, 5),
                            key='-LB-')],
                [sg.T('Matplotlib Styles')],
                [sg.Combo(plt.style.available, key='-STYLE-')]]

    layout = [[sg.T('Statistics and plots', font='Any 20')],
              [sg.T("Number of lives: " + str(a.numberLives) + "; Number of compute adaptability function: " + str(
                  a.numberOfCompute))],
              [sg.T('Best score evolution: ' + str(round(a.bestScore, 4)))],
              [sg.T('Best score swarm: ' + str(round(b.globalBestScore, 4)))],
              [sg.Column(left_col), sg.Image(key='-IMAGE-')],
              [sg.B('Draw'), sg.B('Exit')]]

    window = sg.Window('Evolution algorithm', layout)

    image_element = window['-IMAGE-']  # type: sg.Image
    while True:
        event, values = window.read()
        print(event, values)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            break
        if event == 'Draw' and values['-LB-']:
            # Get the function to call to make figure. Done this way to get around bug in Web port (default value not working correctly for listbox)
            func = dictionary_of_figures.get(values['-LB-'][0], list(dictionary_of_figures.values())[0])
            if values['-STYLE-']:
                plt.style.use(values['-STYLE-'])
            if values['-LB-'][0] == 'Evolution gif':
                create_gif(a)
            elif values['-LB-'][0] == 'Swarm gif':
                create_gif(b)
            elif values['-LB-'][0] == 'Table of evolution':
                pandas_population(a)
            elif values['-LB-'][0] == 'Table of swarm':
                pandas_population(b)
            elif values['-LB-'][0] == 'Adaptability chart evolution':
                draw_figure(image_element, func(a))
            elif values['-LB-'][0] == 'Adaptability chart swarm':
                draw_figure(image_element, func(b))
            else:
                draw_figure(image_element, func(a))
            # if func == create_gif:
            #     create_gif()
            # elif func == pandas_population:
            #     pandas_population()
            # else:
            #     draw_figure(image_element, func())

    window.close()


if __name__ == '__main__':
    # analis.start()
    args = MachineLearningGUI()
    if args['mode'] == '1':
        if args[10]:
            a = evolution.Genetic(args[0], args[1], args[2], args[3], args[7], evolution.F, args[8], args[9])
        else:
            a = evolution.Genetic(args[0], args[1], args[2], args[3], args[7], evolution.F1, args[8], args[9])
        a.startGenetic()
        animation(a)
    elif args['mode'] == '2':
        if args[10]:
            a = swarm.Swarm(args[0], args[4], args[5], args[6], args[7], swarm.F, args[8], args[9])
            print()
        else:
            a = swarm.Swarm(args[0], args[4], args[5], args[6], args[7], swarm.F1, args[8], args[9])
        a.startSwarm()
        animation(a)
    elif args['mode'] == '0':
        if args[10]:
            a = evolution.Genetic(args[0], args[1], args[2], args[3], args[7], evolution.F, args[8], args[9])
            b = swarm.Swarm(args[0], args[4], args[5], args[6], args[7], swarm.F, args[8], args[9])
            a.startGenetic()
            b.startSwarm()
            new_animation()
        else:
            a = evolution.Genetic(args[0], args[1], args[2], args[3], args[7], evolution.F1, args[8], args[9])
            b = swarm.Swarm(args[0], args[4], args[5], args[6], args[7], swarm.F1, args[8], args[9])
            a.startGenetic()
            b.startSwarm()
            new_animation()

