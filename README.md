# Bean Disease Classification Dataset - Uganda

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](#changelog)

A dataset of bean plant images for disease classification, collected and organized for computer vision and deep learning research in agricultural applications. This dataset follows the standardized dataset structure specification.

- Project page: `https://storage.googleapis.com/ibeans/`
- Original dataset: `https://storage.googleapis.com/ibeans/train.zip`, `https://storage.googleapis.com/ibeans/test.zip`, `https://storage.googleapis.com/ibeans/validation.zip`

## TL;DR

- Task: classification (detection with full-image bounding boxes)
- Modality: RGB
- Platform: handheld/field
- Real/Synthetic: real
- Images: 1,295 across 3 disease/health categories
- Resolution: 500×500 pixels
- Annotations: per-image CSV and JSON; COCO format available
- License: CC BY 4.0 (see LICENSE)
- Citation: see below

## Table of contents

- [Download](#download)
- [Dataset structure](#dataset-structure)
- [Sample images](#sample-images)
- [Annotation schema](#annotation-schema)
- [Stats and splits](#stats-and-splits)
- [Quick start](#quick-start)
- [Evaluation and baselines](#evaluation-and-baselines)
- [Datasheet (data card)](#datasheet-data-card)
- [Known issues and caveats](#known-issues-and-caveats)
- [License](#license)
- [Citation](#citation)
- [Changelog](#changelog)
- [Contact](#contact)

## Download

- Original dataset:
  - Train: `https://storage.googleapis.com/ibeans/train.zip`
  - Test: `https://storage.googleapis.com/ibeans/test.zip`
  - Validation: `https://storage.googleapis.com/ibeans/validation.zip`
- This repo hosts structure and conversion scripts only; place the downloaded folders under `data/origin/` directory.
- The original data structure (train/, validation/, test/) is preserved in `data/origin/` for reference.
- Local license file: see `LICENSE` (Creative Commons Attribution 4.0 International).

## Dataset structure

This dataset follows the standardized dataset structure specification:

```
bean_disease_uganda/
├── beans/                           # Category directory
│   ├── labelmap.json               # Label mapping for all subcategories
│   ├── healthy/                    # Healthy bean plants subcategory
│   │   ├── csv/                    # CSV annotations per image
│   │   ├── json/                   # JSON annotations per image
│   │   ├── images/                 # JPEG images
│   │   └── sets/                    # Dataset splits
│   │       ├── train.txt
│   │       ├── val.txt
│   │       ├── test.txt
│   │       ├── all.txt
│   │       └── train_val.txt
│   ├── bean_rust/                  # Bean rust disease subcategory
│   │   ├── csv/
│   │   ├── json/
│   │   ├── images/
│   │   └── sets/
│   └── angular_leaf_spot/           # Angular leaf spot disease subcategory
│       ├── csv/
│       ├── json/
│       ├── images/
│       └── sets/
├── annotations/                     # COCO format JSON (generated)
│   ├── healthy_instances_train.json
│   ├── healthy_instances_val.json
│   ├── healthy_instances_test.json
│   ├── bean_rust_instances_train.json
│   ├── bean_rust_instances_val.json
│   ├── bean_rust_instances_test.json
│   ├── angular_leaf_spot_instances_train.json
│   ├── angular_leaf_spot_instances_val.json
│   ├── angular_leaf_spot_instances_test.json
│   ├── combined_instances_train.json
│   ├── combined_instances_val.json
│   └── combined_instances_test.json
├── scripts/
│   ├── convert_to_coco.py          # Convert CSV to COCO format
│   └── reorganize_dataset.py       # Dataset reorganization script
├── data/                            # Original data directory
│   └── origin/                      # Original dataset structure (train/, validation/, test/)
├── LICENSE
├── README.md
└── requirements.txt
```

- Splits: `beans/{subcategory}/sets/train.txt`, `beans/{subcategory}/sets/val.txt`, `beans/{subcategory}/sets/test.txt` (and also `all.txt`, `train_val.txt`) list image basenames (no extension). If missing, all images are used.

## Sample images

Below are example images from this dataset. Paths are relative to this README location.

<table>
  <tr>
    <th>Category</th>
    <th>Sample</th>
  </tr>
  <tr>
    <td><strong>Healthy</strong></td>
    <td>
      <img src="beans/healthy/images/healthy_train_0.jpg" alt="Healthy bean plant" width="260"/>
      <div align="center"><code>beans/healthy/images/healthy_train_0.jpg</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Bean Rust</strong></td>
    <td>
      <img src="beans/bean_rust/images/bean_rust_train_0.jpg" alt="Bean rust disease" width="260"/>
      <div align="center"><code>beans/bean_rust/images/bean_rust_train_0.jpg</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Angular Leaf Spot</strong></td>
    <td>
      <img src="beans/angular_leaf_spot/images/angular_leaf_spot_train_0.jpg" alt="Angular leaf spot disease" width="260"/>
      <div align="center"><code>beans/angular_leaf_spot/images/angular_leaf_spot_train_0.jpg</code></div>
    </td>
  </tr>
</table>

## Annotation schema

- CSV per-image schemas (stored under `beans/{subcategory}/csv/` folder):
  - Columns include `item, x, y, width, height, label` (bounding boxes in absolute pixel coordinates).
  - For classification tasks, each image has a full-image bounding box `[0, 0, image_width, image_height]` with the category label.
- JSON per-image schemas (stored under `beans/{subcategory}/json/` folder):
  - Each image has a corresponding JSON file with COCO-style format
  - Bounding boxes: `[x, y, width, height]` in absolute pixel coordinates
- COCO-style (generated):
```json
{
  "info": {"year": 2025, "version": "1.0.0", "description": "Bean Disease Uganda beans healthy train split", "url": "https://storage.googleapis.com/ibeans/"},
  "images": [{"id": 1, "file_name": "beans/healthy/images/healthy_train_0.jpg", "width": 500, "height": 500}],
  "categories": [{"id": 1, "name": "healthy", "supercategory": "bean"}],
  "annotations": [{"id": 1, "image_id": 1, "category_id": 1, "bbox": [0, 0, 500, 500], "area": 250000, "iscrowd": 0}]
}
```

- Label maps: `beans/labelmap.json` defines the category mapping:
```json
[
  {"object_id": 0, "label_id": 0, "keyboard_shortcut": "0", "object_name": "background"},
  {"object_id": 1, "label_id": 1, "keyboard_shortcut": "1", "object_name": "bean_rust"},
  {"object_id": 2, "label_id": 2, "keyboard_shortcut": "2", "object_name": "angular_leaf_spot"},
  {"object_id": 3, "label_id": 3, "keyboard_shortcut": "3", "object_name": "healthy"}
]
```

## Stats and splits

**Dataset Statistics**:
- Total images: 1,295
- Categories: 3 (healthy, bean_rust, angular_leaf_spot)

**Per-category statistics**:

| Category | Train | Val | Test | Total |
|----------|-------|-----|------|-------|
| healthy | 341 | 44 | 42 | 427 |
| bean_rust | 348 | 45 | 43 | 436 |
| angular_leaf_spot | 345 | 44 | 43 | 432 |

**Combined statistics**:
- Training set: 1,034 images
- Validation set: 133 images
- Test set: 128 images

- Splits provided via `beans/{subcategory}/sets/*.txt`. You may define your own splits by editing those files.

## Quick start

Python (COCO):
```python
from pycocotools.coco import COCO
coco = COCO("annotations/combined_instances_train.json")
img_ids = coco.getImgIds()
img = coco.loadImgs(img_ids[0])[0]
ann_ids = coco.getAnnIds(imgIds=img['id'])
anns = coco.loadAnns(ann_ids)
```

Convert to COCO JSON:
```bash
# Generate separate COCO files for each subcategory
python scripts/convert_to_coco.py --root . --out annotations --category beans --splits train val test

# Generate combined COCO files for all subcategories
python scripts/convert_to_coco.py --root . --out annotations --category beans --splits train val test --combined
```

Dependencies:
- Required: `Pillow>=9.5`
- Optional (for COCO API): `pycocotools>=2.0.7`

## Evaluation and baselines

This dataset is designed for bean plant disease classification tasks. Evaluation metrics:
- Classification accuracy
- Per-class precision, recall, and F1-score
- Confusion matrix analysis

## Datasheet (data card)

### Motivation

This dataset was created to support research in agricultural AI, specifically for bean plant disease detection and classification. It addresses the need for high-quality, annotated datasets for training computer vision models in precision agriculture applications.

### Composition

The dataset contains:
- **1,295 images** of bean plants in various conditions
- **3 disease/health categories**: healthy, bean_rust, angular_leaf_spot
- **High-resolution images**: 500×500 pixels
- **Full-image annotations**: Each image is annotated with a full-image bounding box indicating the disease/health category

### Collection process

- **Source**: Images collected from various sources and organized into train/test/validation splits
- **Annotation**: Each image annotated with COCO-style JSON format, including full-image bounding boxes for classification tasks
- **Validation**: Manual validation of images and annotations

### Preprocessing

- Images standardized to 512×512 pixels
- Annotations converted to standardized CSV and JSON formats
- Dataset reorganized to follow standardized structure specification

### Distribution

The dataset is distributed via:
- Original source: `https://storage.googleapis.com/ibeans/`
- This repository: Standardized structure and conversion scripts

### Maintenance

This dataset is maintained as part of the standardized dataset collection. Issues and improvements can be reported through the repository.

## Known issues and caveats

- **Classification task**: This dataset uses full-image bounding boxes for classification. Each image has a single bounding box covering the entire image `[0, 0, 500, 500]` with the category label.
- **Image format**: All images are in JPEG format, 500×500 pixels.
- **File naming**: Image files use a naming pattern `{category}_{split}_{index}.jpg` (e.g., `healthy_train_0.jpg`).
- **Coordinate system**: Bounding boxes use absolute pixel coordinates with origin at top-left corner.

## License

This dataset is licensed under the Creative Commons Attribution 4.0 International License (CC BY 4.0). See `LICENSE` file for details.

Check the original dataset terms and cite appropriately.

## Citation

If you use this dataset, please cite:

```bibtex
@dataset{bean_disease_uganda_2025,
  title={Bean Disease Classification Dataset - Uganda},
  author={Dataset Contributors},
  year={2025},
  url={https://storage.googleapis.com/ibeans/},
  license={CC BY 4.0}
}
```

## Changelog

- **V1.0.0** (2025): Initial standardized structure and COCO conversion utility

## Contact

- **Maintainers**: Dataset maintainers
- **Original authors**: See original dataset source
- **Source**: `https://storage.googleapis.com/ibeans/`
