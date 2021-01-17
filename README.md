# DIFFQA

Prediction of the quality of single protein model using deep learning and residue-residue distance maps



# Installation

1. Before you run DIFFQA for protein quality prediction, please make sure you installed the [DeepDist](https://github.com/jianlin-cheng/DeepDist) in your environment.

2. Download this git [repo](https://github.com/jianlin-cheng/DIFFQA.git)
   ```bash
   # use your account to download
   git clone https://XiaoChen1992@github.com/jianlin-cheng/DIFFQA.git 
   ```

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

# Evaluation
5. Prepare predicted distance map
   ```bash
   # Extract distance map from pdb file
   conda activate DIFFQA
   cd DIFFQA
   unzip DIFFQA/example/server_model/example_data.zip
   rm DIFFQA/example/server_model/example_data.zip
   python ./src/pdb2dist.py example/T0949.pdb example/T0949.fasta example_output 
   ```
6. Predict distance map by DeepDist.
Follow the instruction by  [DeepDist](https://github.com/jianlin-cheng/DeepDist)

7. Generate difference map
   ```bash
   conda activate DIFFQA
   cd DIFFQA
   python DIFFQA/src/generate_diffmap.py -c 4 -s -p -o example_difference_output
   ```

8. Predicte protein quality score
   ```bash
   cd DIFFQA
   conda activate DIFFQA
   python DIFFQA/src/eval_gpu.py -i DIFFQA/example/example_data -o DIFFQA/example/test_output
   ```