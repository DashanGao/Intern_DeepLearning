
def plot(file, x, y, xlim=None, ylim=None, name=None, align="top", save="img.png", xlabel="", ylabel="", title="", savetxt=None):
    """
    :param file: txt file
    :param x: [[str:pattern name, axis], [], [], ...], if pattern has more than one {num}, 
              axis(optional) is needed to identify one {num} you want
    :param y: same as x
    :param xlim: x axis value limitation
    :param ylim: same as xlim
    :param name: legend name, len(x) == len(y) == len(name)
    :param align: if lenth of x/y pare in extracted number not equal, align at top or bottom
    :param save: save data to txt
    :return:
    """
    from util import num_extractor as nex
    import matplotlib.pyplot as plt
    
    if len(x) != len(y):
        raise ValueError("len(x) != len(y) " + str(len(x)) + " vs. " + str(len(y)))
    with open(file) as f:
        txt = f.read()

    plots = []
    for i, j in zip(x, y):
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
        plots.append(plt.plot(tx, ty)[0])
    if name is not None:
        if len(name) != len(plots):
            raise ValueError("len(legend name) != len(plots) " + str(len(name)) + " vs. " + str(len(plots)))
        plt.legend(name, loc=0, ncol=1)
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(save)
#    plt.show()

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
                l += "nan nan "
                continue
            l += str(data[j][0][i]) + " " + str(data[j][1][i]) + " "
        out.append(l.rstrip(" ") + "\n")

    with open(savetxt, 'w') as f:
        f.writelines(out)
        

