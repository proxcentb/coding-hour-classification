# coding-hour-classification

These are project files for this series on youtube: <br>
https://youtu.be/QizLa7RdrZo <br>
https://youtu.be/gF75Abn3A_8 <br>
https://youtu.be/lX_Ysn8nhAA <br>

There are several minor improvements made to the original files.

# Quick overview
1. First of all you have activate the conda environment specified in `environment.yml` file. Some packages might be missing, so install on your own!
2. Then you can generate your own images (or use already created ones in `created_images` directory): ```python image_generator.py```
3. Then you have to reorder them: ```python prepare_images.py```
4. Then train you neural network: ```python train.py```
5. Finally, check out  your result: ```python image_predictor.py``` <br>

![2022-10-01-09:46:51 921726232](https://user-images.githubusercontent.com/17691153/193405498-1a0b669f-56e5-44b0-a25c-6248f05b8e64.gif)
