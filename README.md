# CTG_RP
ML/DL analysis of Cardiotocography (CTG) traces using Recurrence Plot

This Repo contains Jupyter Notebooks and code to reproduce the results of the paper [Computer-Aided Diagnosis System of Fetal Hypoxia Incorporating Recurrence Plot With Convolutional Neural Network](https://www.frontiersin.org/articles/10.3389/fphys.2019.00255/full)
 by Zhidong Zhao, Yang Zhang, Zafer Comert and Yanjun Deng.

## Implementation Details

Key Jupyter Notebooks (_currently configured to run on Google Colab per below_):
- [CTG_RP_Startup_Config](https://github.com/williamsdoug/CTG_RP/blob/master/CTG_RP_Startup_Config.ipynb)
  - Initializes fresh colab instance, downloading source files, packages and dataset
  - [view using nbviewer](https://nbviewer.jupyter.org/github/williamsdoug/CTG_RP/blob/master/CTG_RP_Startup_Config.ipynb)
- [CTG_RP_Generate_Recurrence_Plots](https://github.com/williamsdoug/CTG_RP/blob/master/CTG_RP_Generate_Recurrence_Plots.ipynb)
  - Creates individual RP Images.  _IMAGES_DIR/rp_images_index.json_ contains metadata associated with images for each recording
  - [view using nbviewer](https://nbviewer.jupyter.org/github/williamsdoug/CTG_RP/blob/master/CTG_RP_Generate_Recurrence_Plots.ipynb)
- [CTG_RP_Train_Model](https://github.com/williamsdoug/CTG_RP/blob/master/CTG_RP_Train_Model.ipynb)
  - Trains FastAI Model
  - [view using nbviewer](https://nbviewer.jupyter.org/github/williamsdoug/CTG_RP/blob/master/CTG_RP_Train_Model.ipynb)

Other Notebooks:
- [CTG_RP_Display_Denoised](https://github.com/williamsdoug/CTG_RP/blob/master/CTG_RP_Display_Denoised.ipynb)
  - Displays sample denoised signals
  - [view using nbviewer](https://nbviewer.jupyter.org/github/williamsdoug/CTG_RP/blob/master/CTG_RP_Display_Denoised.ipynb)
- [CTG_RP_Explore_Datasets](https://github.com/williamsdoug/CTG_RP/blob/master/CTG_RP_Explore_Datasets.ipynb)
  - Builds Databunch and displays contents
  - [view using nbviewer](https://nbviewer.jupyter.org/github/williamsdoug/CTG_RP/blob/master/CTG_RP_Explore_Datasets.ipynb)
- [CTG_RP_Train_ResNet_Model](https://github.com/williamsdoug/CTG_RP/blob/master/CTG_RP_Train_ResNet_Model.ipynb)
  - Uses transfer learning to train using ResNet32 model
  - [view using nbviewer](https://nbviewer.jupyter.org/github/williamsdoug/CTG_RP/blob/master/CTG_RP_Train_ResNet_Model.ipynb)


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
    - Installed by default on Google Colab
  - [wfdb](https://wfdb.readthedocs.io/en/latest/index.html)
    - Waveform Database Utilities.  Used to read Physionet Recording Files
    - `pip install wfdb`
    
- Computation:
  - [Google Colab](https://colab.research.google.com)
    - Jupyter Notebook service with no-cost access to GPU accelerated instances