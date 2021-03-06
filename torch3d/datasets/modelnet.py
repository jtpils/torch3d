import os
import h5py
import numpy as np
from torchvision.datasets import VisionDataset
from torchvision.datasets.utils import download_and_extract_archive, check_integrity


class ModelNet40(VisionDataset):
    """
    The `ModelNet40 <https://modelnet.cs.princeton.edu/>`_ dataset.

    """

    name = "modelnet40"
    url = "https://shapenet.cs.stanford.edu/media/modelnet40_ply_hdf5_2048.zip"
    basedir = "modelnet40_ply_hdf5_2048"
    splits = {
        "train": [
            ("ply_data_train0.h5", "3176385ffc31a7b6b5af22191fd920d1"),
            ("ply_data_train1.h5", "e3f613fb500559403b34925112754dc4"),
            ("ply_data_train2.h5", "0c56e233a090ff87c3049d4ce08e7d8b"),
            ("ply_data_train3.h5", "9d2af465adfa33a3285c369f3ca66c45"),
            ("ply_data_train4.h5", "dff38de489b2c41bfaeded86c2208984"),
        ],
        "test": [
            ("ply_data_test0.h5", "e9732e6d83b09e79e9a7617df058adee"),
            ("ply_data_test1.h5", "aba4b12a67c34391cc3c015a6f08ed4b"),
        ],
    }
    categories = [
        "airplane",
        "bathtub",
        "bed",
        "bench",
        "bookshelf",
        "bottle",
        "bowl",
        "car",
        "chair",
        "cone",
        "cup",
        "curtain",
        "desk",
        "door",
        "dresser",
        "flower_pot",
        "glass_box",
        "guitar",
        "keyboard",
        "lamp",
        "laptop",
        "mantel",
        "monitor",
        "night_stand",
        "person",
        "piano",
        "plant",
        "radio",
        "range_hood",
        "sink",
        "sofa",
        "stairs",
        "stool",
        "table",
        "tent",
        "toilet",
        "tv_stand",
        "vase",
        "wardrobe",
        "xbox",
    ]

    def __init__(
        self,
        root,
        train=True,
        download=False,
        transform=None,
        target_transform=None,
        transforms=None,
    ):
        super(ModelNet40, self).__init__(root, transforms, transform, target_transform)
        self.train = train

        if download:
            self.download()

        if not self._check_integrity():
            raise RuntimeError("Dataset not found or corrupted.")

        if self.train:
            flist = self.splits["train"]
        else:
            flist = self.splits["test"]

        self.data = []
        self.targets = []

        for filename, md5 in flist:
            h5 = h5py.File(os.path.join(self.root, self.name, filename), "r")
            assert "data" in h5 and "label" in h5
            self.data.append(np.array(h5["data"][:]))
            self.targets.append(np.array(h5["label"][:]))
            h5.close()
        self.data = np.concatenate(self.data, axis=0)
        self.targets = np.concatenate(self.targets, axis=0)
        self.targets = np.squeeze(self.targets).astype(np.int64)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, i):
        pcd = self.data[i]
        target = self.targets[i]
        if self.transforms is not None:
            pcd, target = self.transforms(pcd, target)
        return pcd, target

    def download(self):
        if not self._check_integrity():
            download_and_extract_archive(self.url, self.root)
            os.rename(
                os.path.join(self.root, self.basedir),
                os.path.join(self.root, self.name),
            )

    def _check_integrity(self):
        flist = self.splits["train"] + self.splits["test"]
        for filename, md5 in flist:
            fpath = os.path.join(self.root, self.name, filename)
            if not check_integrity(fpath, md5):
                return False
        return True
