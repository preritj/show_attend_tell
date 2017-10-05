## Show and Tell : A Neural Caption Generator for Live Camera Stream

**Credits** :

* This repo uses Tensorflow implementation of show found at [tensorflow/models](https://github.com/tensorflow/models/) of the image-to-text paper described below : 

* "Show and Tell: Lessons learned from the 2015 MSCOCO Image Captioning Challenge."
Oriol Vinyals, Alexander Toshev, Samy Bengio, Dumitru Erhan.
Full text available at: http://arxiv.org/abs/1609.06647

* Pretrained model was borrowed from [github page of KranthiGV](https://github.com/KranthiGV/Pretrained-Show-and-Tell-model). For convenience, here is the checkpoint file : https://drive.google.com/file/d/0B3laN3vvvSD2T1RPeDA5djJ6bFE/view?usp=sharing) | [Released under MIT License](https://github.com/KranthiGV/Pretrained-Show-and-Tell-model/blob/master/LICENSE). 
Be sure to credit the original author if you use the checkpoint file.

Here is a sample on a live camera feed without any fine-tuning: 

[![captions](http://img.youtube.com/vi/_LEVX2OyycE/0.jpg)](http://www.youtube.com/watch?v=_LEVX2OyycE "captions")


## Setup instructions

* Clone the repository.
* Install Python 3.5+, Numpy 1.2+, Tensorflow 1.2+ . You may need to install python packages if they are missing. 
* Download the pretrained checkpoint file from the link specified above and place the checkpoint file, along with the corresponding index file, in `models` directory. 
* The live camera feed url as well as other camera parameters should be specified in `stream_utils/config.ini`. 
* Finally, edit and run the script `run.sh`.  
