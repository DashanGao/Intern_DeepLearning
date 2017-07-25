

def plot(file_x_y_drop, xlim=None, ylim=None, legend=None, align="top",
         xlabel="", ylabel="", title="", saveimg=None, savetxt=None):
    """
    Draw plot, multi source files, multi lines, optional smooth, xlabel, ylabel, legend, title, save line data to txt
    Only need to provide txt pattern to extract data, e.g. - "Test net output #2: loss = {num}"
    :param file_x_y_drop: tuple or list of tuple - (file, x, y, drop)
                          [(file, [x1_pattern, ...], [y1_pattern, ...], [drop1, ...](optional)), ...]
                          drop1 - a int, average adjacent drop1 points to smooth line, default no smooth
    :param xlim: x axis value limitation
    :param ylim: same as xlim
    :param legend: legend name, len(x) == len(y) == len(name)
    :param align: if lenth of x/y pare in extracted number not equal, align at top or bottom
    :param xlabel: x label
    :param ylabel: y label
    :param title: image title
    :param saveimg: str, if need to save image, default not save
    :param savetxt: str. if need to save data in txt, default not save
    :return: None
    """
    from util import num_extractor as nex
    import matplotlib.pyplot as plt
    import math
    import numpy as np

    def add_plot(file, _x, _y, _drop=None):
        if len(_x) != len(_y):
            raise ValueError("len(x) != len(y) " + str(len(_x)) + " vs. " + str(len(_y)))
        if _drop is None:
            _drop = [1] * len(_x)
        with open(file) as f:
            txt = f.read()

        plots = []
        for i, j, drop in zip(_x, _y, _drop):
            ix = nex(txt, i[0], recall=i[1]) if isinstance(i, list) else nex(txt, i)
            jy = nex(txt, j[0], recall=j[1]) if isinstance(j, list) else nex(txt, j)
            if len(ix) == 0:
                raise ValueError("Pattern <" + str(i) + "> not match")
            if len(jy) == 0:
                raise ValueError("Pattern <" + str(j) + "> not match")
            min_len = min(len(ix), len(jy))
            if align == "top":
                tx = ix[:min_len - 1]
                ty = jy[:min_len - 1]
            elif align == "bottom":
                tx = ix[1 - min_len:]
                ty = jy[1 - min_len:]
            if drop != 1:
                len_drop = int(math.ceil(float(len(tx) - 2) / float(drop)) + 2)
                drop_x = np.zeros(len_drop, dtype=np.float)
                drop_y = np.zeros(len_drop, dtype=np.float)
                drop_x[0] = tx[0]
                drop_y[0] = ty[0]
                drop_x[-1] = tx[-1]
#                drop_y[-1] = ty[-1]
                drop_y[-1] = np.sum(ty[len(tx) - drop: len(tx)]) / float(drop)
                drop_x[-2] = tx[int(math.floor(((len_drop - 3) * drop + 1 + len(tx) - 2) / 2))]
                drop_y[-2] = np.sum(ty[len(tx) - 2 * drop: len(tx) - drop]) / float(drop)
                for i in range(1, len_drop - 2):
                    drop_x[i] = tx[int((i - 1) * drop + math.ceil(float(drop) / 2.))]
                    drop_y[i] = np.sum(ty[(i - 1) * drop : i * drop]) / drop
                tx = drop_x
                ty = drop_y
            plots.append(plt.plot(tx, ty)[0])
        return plots

    plots = []
    if isinstance(file_x_y_drop, tuple):
        if len(file_x_y_drop) < 3:
            raise TypeError("tuple file_x_y must follow format (file_name, "
                            "[x1_pattern, x2_pattern, ...], [y1_pattern, y2_pattern, ...], ([drop1, drop2 ,...]))")
        plots += add_plot(*file_x_y_drop)
    elif isinstance(file_x_y_drop, list):
        for i in file_x_y_drop:
            if len(i) < 3:
                raise TypeError("tuple file_x_y must follow format (file_name, "
                                "[x1_pattern, x2_pattern, ...], [y1_pattern, y2_pattern, ...], ([drop1, drop2 ,...]))")
            plots += add_plot(*i)
    if legend is not None:
        if len(legend) != len(plots):
            raise ValueError("len(legend name) != len(plots) " + str(len(legend)) + " vs. " + str(len(plots)))
        plt.legend(legend, loc=0, ncol=1)
    plt.grid(linewidth='0.3', linestyle='--')
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if saveimg is not None:
        plt.savefig(saveimg)
    else:
        plt.show()

    if savetxt is None:
        return
    data = [x.get_data(True) for x in plots]
    maxlen = 0
    for i in data:
        maxlen = max(maxlen, len(i[1]))
    out = []
    for i in range(maxlen):
        l = ""
        for j in range(len(data)):
            if i >= len(data[j][0]):
                l += "null null "
                continue
            l += str(data[j][0][i]) + " " + str(data[j][1][i]) + " "
        out.append(l.rstrip(" ") + "\n")

    with open(savetxt, 'w') as f:
        f.writelines(out)
    plt.close('all')
        

