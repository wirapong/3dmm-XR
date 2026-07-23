# 3dmm-XR

A lightweight 3DMM–CNN pipeline for real-time single-image 3D face
reconstruction — prototyping personalised avatars for **Extended Reality
(XR) applications** (VR / AR / MR).

> **Paper:** *A Lightweight 3DMM-CNN Pipeline for Real-Time Single-Image 3D
> Face Reconstruction: Prototyping Personalised Avatars for Extended Reality
> Applications.*
> **Authors:** Qianqian He¹, Wirapong Chansanam¹, Lan Thi Nguyen¹,*, Kannikar Intawong², and Kitti Puritat²,* 
> ¹ Department of Information Science, Faculty of Humanities and Social
> ²	Faculty of Public Health, Chiang Mai University, Chiang Mai 50200, Thailand; kannikar.i@cmu.ac.th
> 3	Department of Library and Information Science, Faculty of Humanities, Chiang Mai University, 
Chiang Mai 50200, Thailand

> Sciences, KKU, Thailand
> \* Corresponding author: `wirach@kku.ac.th`

---

## What is here

```
3dmm-XR/
├── project/                          # Training & inference code
│   ├── bin/                          #   entry-points (train.py, test.py, ...)
│   ├── lib/                          #   Model, Renderer, MorphabelModel, ...
│   ├── shader/                       #   GLSL shaders
│   ├── data/                         #   data-loading helpers (datasets excluded)
│   └── model/                        #   model architecture (weights excluded)
├── figures/
│   ├── build/                        # matplotlib scripts that build each figure
│   │   ├── figure3_prototype_walkthrough.py
│   │   ├── figure4_two_panels.py
│   │   └── figure6_qualitative_gallery_endash_patch.py
│   └── outputs/                      # 400-dpi PNG + vector PDF
│       ├── Figure3_prototype.png/.pdf
│       ├── Figure4_two_panels.png/.pdf
│       ├── Figure5-Figure_ablation_studies.png/.pdf
│       └── Figure6-Figure_qualitative_gallery.png
├── requirements.txt
├── LICENSE                           # MIT
└── README.md
```

## Model weights & datasets (external — download separately)

The following files are **not** shipped with the repository because they
exceed GitHub's 100 MB per-file limit and/or carry separate licences.
Download them into the paths below before running training/inference:

| Path | Size | Source |
|------|------|--------|
| `project/model/BFM.mat` | ~261 MB | [Basel Face Model](https://faces.dmi.unibas.ch/bfm/) (research licence) |
| `project/model/shape_predictor_68_face_landmarks.dat` | ~95 MB | [dlib](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2) |
| `project/model/fit_model.pth` | ~90 MB | *Provided on request from the corresponding author* |
| `project/data/AFLW2000/` | ~105 MB | [AFLW2000-3D dataset](http://www.cbsr.ia.ac.cn/users/xiangyuzhu/projects/3DDFA/main.htm) |
| `project/data/train/` | (varies) | prepared by user |
| `project/data/test/`  | (varies) | prepared by user |

## Reproduce the manuscript figures

```bash
# Install dependencies (Python 3.11 recommended)
pip install -r requirements.txt

# Regenerate the figures
python figures/build/figure3_prototype_walkthrough.py
python figures/build/figure4_two_panels.py
python figures/build/figure6_qualitative_gallery_endash_patch.py
```

Outputs will be written to `/tmp/` by default (adjust `DST` in each script if
you want a different path).

## Train / evaluate the model

```bash
cd project
python bin/train.py            # or train-fixv2.0.py for the latest variant
python bin/test.py             # evaluation on AFLW2000-3D
```

Refer to comments inside `project/bin/` for CLI flags and dataset layout.

## Citation

If you use this repository in your research, please cite the paper (BibTeX to
be added on acceptance):

```bibtex
@article{He2026_3dmm_xr,
  title   = {A Lightweight 3DMM-CNN Pipeline for Real-Time Single-Image 3D
             Face Reconstruction: Prototyping Personalised Avatars for
             Extended Reality Applications},
  author  = {He, Qianqian and Chansanam, Wirapong and Nguyen, Lan Thi},
  journal = {Informatics (MDPI)},
  year    = {2026},
  note    = {Manuscript in review}
}
```

## Licence

Source code in this repository is released under the [MIT Licence](LICENSE).
The Basel Face Model, dlib landmark predictor, and AFLW2000-3D dataset each
carry their own licences — please consult the upstream sources.
