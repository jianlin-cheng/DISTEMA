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
   # CUDA 10.2
   conda install pytorch==1.6.0 torchvision==0.7.0 cudatoolkit=10.2 -c pytorch
   
   # CPU Only
   conda install pytorch==1.6.0 torchvision==0.7.0 cpuonly -c pytorch
   
   pip install pandas
   pip install scipy
   ```

# Evaluation
5. Prepare predicted distance map
   ```bash
   # Extract distance map from pdb file
   conda activate DIFFQA
   cd DIFFQA
   unzip ./example/server_model/example_data.zip -d ./example/server_model
   rm ./example/server_model/example_data.zip
   python ./src/pdb2dist_wrapper.py  -i ./example/server_model -f ./example/sequence/T0949.fasta -o ./example/server_distmap 
   ```
6. Predict distance map by DeepDist.
Follow the instruction by  [DeepDist](https://github.com/jianlin-cheng/DeepDist)

7. Generate difference map
   ```bash
   conda activate DIFFQA
   cd DIFFQA
   python ./src/generate_difference_map.py -c 2 -s ./example/server_distmap -p ./example/pred_distmap/T0949.txt -o ./example/difference_map
   ```

8. Predicte protein quality score
   ```bash
   cd DIFFQA
   conda activate DIFFQA
   
   # gpu
   python ./src/eval.py -i ./example/difference_map -o ./example/test_output -m ./pretrain-model/pretrain.pth

   # cpu
   python ./src/eval.py -g cpu -i ./example/difference_map -o ./example/test_output -m ./pretrain-model/pretrain.pth
   ```