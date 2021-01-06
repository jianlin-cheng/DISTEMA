# DIFFQA

Prediction of the quality of single protein model using deep learning and residue-residue distance maps



# Installation

1. Before you run DIFFQA for protein quality prediction, please make sure you installed the [DeepDist](https://github.com/jianlin-cheng/DeepDist) in your environment.

2. Download this git [repo](https://github.com/jianlin-cheng/DIFFQA.git)

3. Create a virtual python 3 environment 

   ```bash
   cd ./DIFFQA
   conda create -n DIFFQA python=3.8
   conda activate DIFFQA
   ```

4. Install required packages, CUDA is not requited.

   ```bash
   # CUDA 9.2
   conda install pytorch==1.6.0 torchvision==0.7.0 cudatoolkit=9.2 -c pytorch
   
   # CUDA 10.1
   conda install pytorch==1.6.0 torchvision==0.7.0 cudatoolkit=10.1 -c pytorch
   
   # CUDA 10.2
   conda install pytorch==1.6.0 torchvision==0.7.0 cudatoolkit=10.2 -c pytorch
   
   # CPU Only
   conda install pytorch==1.6.0 torchvision==0.7.0 cpuonly -c pytorch
   
   pip install pandas
   pip install scipy
   pip install matplotlib
   ```

5. Prepare predicted distance map

6. Convert protein model to distance map

7. Predicti protein quality score