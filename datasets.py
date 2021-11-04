from torchvision.datasets.vision import *
from PIL import Image


class Dataset1(VisionDataset):
    def __init__(
        self, 
        root: str, 
        split: str = "train",
        transforms: Optional[Callable] = None, 
        transform: Optional[Callable] = None, 
        target_transform: Optional[Callable] = None
    ) -> None:
        super().__init__(root, transforms=transforms, transform=transform, target_transform=target_transform)
        
        if split not in ("train", "test"):
            assert "err"
        
        self.objs = list(filter(os.path.isdir, [os.path.join(root, d) for d in os.listdir(root)]))
        self.objs.sort()
        self.images = []
        self.targets = []
        self.target_type = ("idk", "idk2", "idk3")


        for obj in self.objs:
            files = [os.path.join(obj, f) for f in os.listdir(obj)]
            files.sort()
            self.images.append(files[-1])
            self.targets.append(files[:-1])
            
    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        """
        Args:
            index (int): Index
        Returns:
            tuple: (image, target) where target is a tuple of all target types
        """

        image = Image.open(self.images[index]).convert('RGB')
        
        targets = []
        for i, t in enumerate(self.target_type):
            target = Image.open(self.targets[index][i])
            targets.append(target)

        target = tuple(targets) if len(targets) > 1 else targets[0]

        if self.transforms is not None:
            image, target = self.transforms(image, target)

        return image, target

    def __len__(self) -> int:
        return len(self.images)


class Dataset2(VisionDataset):
    def __init__(
        self, 
        root: str, 
        split: str = "train",
        transforms: Optional[Callable] = None, 
        transform: Optional[Callable] = None, 
        target_transform: Optional[Callable] = None
    ) -> None:
        super().__init__(root, transforms=transforms, transform=transform, target_transform=target_transform)
        
        dataset_path = {
            "train" : "a. Training Set",
            "test" : "b. Testing Set"
        }

        if split not in dataset_path:
            assert "err"


        self.images = os.listdir(os.path.join(root, "A. Segmentation", "1. Original Images", dataset_path[split] ) )
        self.images = [ os.path.join(root, "A. Segmentation", "1. Original Images", dataset_path[split], f) for f in self.images]
        self.images.sort()

        self.targets = {
            "1. Microaneurysms" : None,
            "2. Haemorrhages"   : None,
            "3. Hard Exudates"  : None,
            "4. Soft Exudates"  : None,
            "5. Optic Disc"     : None,
        }

        for t in self.targets:
            self.targets[t] = os.listdir( os.path.join(root , "A. Segmentation" , "2. All Segmentation Groundtruths" , dataset_path[split] , t) )
            self.targets[t] = [ os.path.join(root , "A. Segmentation" , "2. All Segmentation Groundtruths" , dataset_path[split] , t, f) for f in self.targets[t]]
            self.targets[t].sort()

    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        """
        Args:
            index (int): Index
        Returns:
            tuple: (image, target) where target is a tuple of all target types
        """

        image = Image.open(self.images[index]).convert('RGB')

        targets = []
        for t in self.targets:
            target = Image.open(self.targets[t][index])
            targets.append(target)

        target = tuple(targets) if len(targets) > 1 else targets[0]

        if self.transforms is not None:
            image, target = self.transforms(image, target)

        return image, target

    def __len__(self) -> int:
        return len(self.images)
