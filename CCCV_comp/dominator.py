import glob

if __name__ == '__main__':
    src_path = "/opt/data-safe/users/terrencege"
    des_path = "/opt/data-safe/users/dasgao/CCCV_img"
    fis = glob.glob("pro*.json")
    for fi_ in fis:
        cmd = "python subprocess.py " + fi_
