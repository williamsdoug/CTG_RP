# CTG_RP
ML/DL analysis of CTG traces using Recurrence Plot

This Repo contains Jupyter Notebooks and code to reproduce the results of the paper [Computer-Aided Diagnosis System of Fetal Hypoxia Incorporating Recurrence Plot With Convolutional Neural Network](https://www.frontiersin.org/articles/10.3389/fphys.2019.00255/full)

## Implementation Details

Jupyter Notebooks currently configured to run on Google Colab (see below).


## Key Dependencies

- Data: 
  - [CTU-UHB Intrapartum Cardiotocography Database](https://physionet.org/physiobank/database/ctu-uhb-ctgdb/)
    - Paper: [Open access intrapartum CTG database](https://bmcpregnancychildbirth.biomedcentral.com/track/pdf/10.1186/1471-2393-14-16)
    - Download: 
      - `rsync -Cavz physionet.org::ctu-uhb-ctgdb  /content/ctu-uhb-ctgdb`

- Libraries:
  - [pyts](https://pyts.readthedocs.io/en/latest/)
    - Used for generation of Recurrence Plots
    - `pip install pyts`
  - [FastAI V1](https://docs.fast.ai/) library running on [PyTorch](https://pytorch.org/)
    - Used for deep learning
  - [wfdb](https://wfdb.readthedocs.io/en/latest/index.html)
    - Waveform Database Utilities.  Used to read Physionet Recording Files
    - `pip install wfdb`
    
- Computation:
  - [Google Colab](https://colab.research.google.com)
    - Jupyter Notebook service withy no-cost access to GPU accelerated instances