# DISTEMA
Prediction of the quality of single protein model using deep learning and residue-residue distance maps



# Installation
1. Before you run DISTEMA for protein quality prediction, please make sure you installed the [DeepDist](https://github.com/jianlin-cheng/DeepDist) in your environment. (If you have DeepDist predicted distance map, you can skip this step. To run example code, you do not need to install DeepDist.)

2. Download this DISTEMA [repo](https://github.com/jianlin-cheng/DISTEMA.git)
   ```bash
   # use your account to download
   git clone https://github.com/jianlin-cheng/DISTEMA.git 
   ```

3. Create a virtual python 3 environment 

   ```bash
   cd ./DISTEMA
   conda create -n DISTEMA python=3.8
   conda activate DISTEMA
   ```

4. Install required packages, CUDA is not requited.

   ```bash   
   # CUDA 10.2
   conda install pytorch==1.6.0 torchvision==0.7.0 cudatoolkit=10.2 -c pytorch
   
   # CPU Only
   conda install pytorch==1.6.0 torchvision==0.7.0 cpuonly -c pytorch
   
   pip install pandas
   ```

# Evaluation
5. Prepare predicted distance map
   ```bash
   # Extract distance map from pdb file
   conda activate DISTEMA
   cd DISTEMA
   unzip ./example/server_model/example_data.zip -d ./example/server_model
   rm ./example/server_model/example_data.zip
   python ./src/pdb2dist_wrapper.py  -i ./example/server_model -f ./example/sequence/T0949.fasta -o ./example/server_distmap
   ---
   paramerters: 
   -i --input: Input server model folder path
   -f --fasta: sequence fasta file path
   -o --output: Output folder path
   ```
   
6. Predict distance map by DeepDist.
Follow the instruction by  [DeepDist](https://github.com/jianlin-cheng/DeepDist) (To run example code, skip this step.)

7. Generate difference map
   ```bash
   conda activate DISTEMA
   cd DISTEMA
   python ./src/generate_difference_map.py -c 2 -s ./example/server_distmap -p ./example/pred_distmap/T0949.txt -o ./example/difference_map
   ---
   paramerters:
   -c --cores: multi-processiong cores
   -s --server_model: Server model distance maps folder path
   -p --predicted_map: DeepDist predicted distance map folder path
   -o --output_folder: Output folder path
   ```

8. Predicte protein quality score
   ```bash
   cd DISTEMA
   conda activate DISTEMA
   
   # gpu
   python ./src/eval.py -i ./example/difference_map -o ./example/test_output -m ./pretrain-model/pretrain.pth

   # cpu
   python ./src/eval.py -g cpu -i ./example/difference_map -o ./example/test_output -m ./pretrain-model/pretrain.pth
   ---
   parameters:
   -i --input: Input server model folder path
   -o --output: Output folder path
   -m --model: Pretrain model file path
   -g --gpu: gpu option, default: -g cuda, if you want to use cpu set -g: cpu
   ```