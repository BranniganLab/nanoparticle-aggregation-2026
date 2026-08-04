import sys
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, "../Analysis/Figure_1_scripts/")
from order_density_contact_potter import *

CORETYPES = ["C1", "C5", "N0", "P1", "P5", "SS"]
DIRECTORY_PATH = Path("/media/jje63/easystore/Single_NP/")
LB_SIZE = 20
font = {
    "family": "serif",
    "color": "black",
    "weight": "normal",
    "size": 20,
}
C1dataord = make_thiol_dataset_O_C(
    DIRECTORY_PATH, "C1", "*thiol", "Replica*", DATA_FILE2, "order"
)
C1order_full_replica = create_order_full_replica_data(C1dataord)

C5dataord = make_thiol_dataset_O_C(
    DIRECTORY_PATH, "C5", "*thiol", "Replica*", DATA_FILE2, "order"
)
C5order_full_replica = create_order_full_replica_data(C5dataord)

N0dataord = make_thiol_dataset_O_C(
    DIRECTORY_PATH, "N0", "*thiol", "Replica*", DATA_FILE2, "order"
)
N0order_full_replica = create_order_full_replica_data(N0dataord)

P1dataord = make_thiol_dataset_O_C(
    DIRECTORY_PATH, "P1", "*thiol", "Replica*", DATA_FILE2, "order"
)
P1order_full_replica = create_order_full_replica_data(P1dataord)

P5dataord = make_thiol_dataset_O_C(
    DIRECTORY_PATH, "P5", "*thiol", "Replica*", DATA_FILE2, "order"
)
P5order_full_replica = create_order_full_replica_data(P5dataord)

SSdataord = make_thiol_dataset_O_C(
    DIRECTORY_PATH, "SS", "*thiol", "Replica*", DATA_FILE2, "order"
)
SSorder_full_replica = create_order_full_replica_data(SSdataord)

xaxis = np.arange(0, 50, 5)
figure, axs = plt.subplots(1, 6, figsize=(30, 6), constrained_layout=True)

Cores = [
    C1order_full_replica,
    C5order_full_replica,
    N0order_full_replica,
    P1order_full_replica,
    P5order_full_replica,
    SSorder_full_replica,
]

for i, thiol in enumerate(THIOL):
    coreplot = [
        Cores[0][thiol].iloc[0],
        Cores[1][thiol].iloc[0],
        Cores[2][thiol].iloc[0],
        Cores[3][thiol].iloc[0],
        Cores[4][thiol].iloc[0],
        Cores[5][thiol].iloc[0],
    ]
    coreplotstd = [
        Cores[0][thiol].iloc[1],
        Cores[1][thiol].iloc[1],
        Cores[2][thiol].iloc[1],
        Cores[3][thiol].iloc[1],
        Cores[4][thiol].iloc[1],
        Cores[5][thiol].iloc[1],
    ]
    for j, (cp, cstd) in enumerate(zip(coreplot, coreplotstd)):
        axs[j].errorbar(
            xaxis,
            cp,
            yerr=cstd / np.sqrt(3),
            capsize=4,
            fmt="-o",
            label=thiol,
        )
for i in range(6):
    axs[i].set_title(CORETYPES[i], fontdict=font)
    axs[i].set_xlabel(r"Distance ($\AA$)", fontdict=font)
    axs[i].set_ylabel(r"$S_{CC}$", fontdict=font)
    axs[i].set_xticks(np.arange(0, 60, 10), labels=np.arange(0, 60, 10))
    axs[i].tick_params(axis="both", labelsize=LB_SIZE)
handles, labels = axs[0].get_legend_handles_labels()

figure.legend(
    handles=handles,
    labels=labels,
    loc="outside upper center",  # Position outside below plots
    bbox_to_anchor=(0.5, 1.2),
    ncol=5,  # Make it horizontal (2 columns)
    fontsize=LB_SIZE,
)
SAVE_PATH = Path("../Graphs")
figure.savefig(
    SAVE_PATH.joinpath("SupplementaryFigureLipidOrder.pdf"),
    format="pdf",
    dpi=500,
    bbox_inches="tight",
)

plt.show()
