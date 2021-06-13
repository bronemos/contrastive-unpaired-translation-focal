import os
import re
import matplotlib.pyplot as plt
import sys

fid_re = re.compile(r"FID: (.*)")


def calculate_fids(model_name: str, n_epochs: int):
    fids = list()
    epochs = list()

    for epoch in range(5, n_epochs + 5, 5):
        os.system(
            f"python test.py --dataroot ./datasets/maps --name {model_name} --CUT_mode FastCUT --num_test 500 --epoch {epoch} --gpu 0"
        )
        fid = float(
            fid_re.match(
                os.popen(
                    f"python -m pytorch_fid ./datasets/maps/testB results/{model_name}/test_{epoch}/images/fake_B/ --gpu 0"
                ).read()
            ).group(1)
        )
        print(f"{epoch}: {fid}")
        epochs.append(epoch)
        fids.append(fid)

    return epochs, fids


def plot_fids(epochs, fids):
    plt.plot(epochs, fids)


def main():
    try:
        epochs, fids = calculate_fids(sys.argv[1], int(sys.argv[2]))
        with open("fids.txt", "w") as f:
            f.writelines(map(lambda x: str(x) + "\n", fids))
    except:
        with open("fids_fast_ce.txt", "r") as f:
            epochs = list(range(5, 205, 5))
            fids = [float(x.strip()) for x in f.readlines()]
        plot_fids(epochs, fids)
        with open("fids_fast_focal.txt", "r") as f:
            epochs = list(range(5, 205, 5))
            fids = [float(x.strip()) for x in f.readlines()]
        plot_fids(epochs, fids)
        plt.legend(["FastCUT - CE", "FastCUT - Focal"])
        plt.xlabel("Epoch")
        plt.ylabel("FID on test set")
        plt.show()
    print(fids)


if __name__ == "__main__":
    main()
