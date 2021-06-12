# Rock-sample-masking
This codes generates masks for a list of images in a semi-automated approach. Those masks can be used in photogrammetry software for 3D model reconstruction.
It was designed specifically to be integrated with Agisoft Metashape, so the masks filenames are saved following the software's template.

The code still lacks a proper user interface. In order to change the source or destination directory, you must hard code it.

After running the code, you must interact with the trackbars in order to find the ideal HSV range value for you image.
Once you adjust the mask, all other images will be masked using the same range values.

Because of that, maybe your other images will have some noise. Remember to check every imagem after processing. 
If it is needed, fine tune the masks using Metashape's selection tool.

**Real time mask editing:**
![interface](https://user-images.githubusercontent.com/66284195/121759302-71378c80-cafb-11eb-8097-99390b97de51.png)


**Masks imported directly on Metashape**
![metashape](https://user-images.githubusercontent.com/66284195/121759301-6e3c9c00-cafb-11eb-8d4b-44373dccdfcd.jpg)

