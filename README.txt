Deliverables:
	Project report.pdf
	positive		---- Directory contains images with face
	In positive directory:
		list of images that contains faces
		list.sh		---- generate a list of PNG image names
		list.txt	---- output file of list.sh
		coordinates.txt	---- list of face coordinates in each image from list.txt. Output of marker.py.
		info.txt	---- formatted coordinates of faces. For cascade classifier training. Output of format.py
		bw.py		---- shows images in list.txt in black and white. For observing patterns of faces


	faceDetection.py	---- main program that detect face in a image
	marker.py		---- manually mark faces in an image. Click top left and bottom right of a face to mark a face. Output to 
				     coordinates.txt in positive directory
	format.py		---- take coordinates.txt as input and output list of formatted coordinates. Output to info.txt in positive
				     directory
	showPositive.py		---- showing images listed in list.txt with face marked in info.txt


Run:
	Only openCV and numpy are required.
	python3 <name of python file>            to run 
	in faceDetection.py, an image name is required as input. 