# Exercise 8 - Cats, Cats, Cats (WORK IN PROGRESS)

Are you sad that you have watched all cat movies and seen all cat photos on the internet? Then be sad no more - in this exercise we will make a *Cat Synthesizer* where you can create all the cat photos you will ever need!

Also, you can help your friends with missing cats to find the perfect new *twin cat*.
 
To be able to do these wonderful things we will harness the power of image based *principal component analysis*. The methods we will use, can be called *classical machine learning*.


## Learning Objectives

After completing this exercise, the student should be able to do the following:

1. Use the python function `glob` to find all files with a given pattern in a folder.

## Importing required Python packages

We will use the virtual environment from the previous exercise (`course02502`). 

Let us start with some imports:

```python
from skimage import io
from skimage.util import img_as_ubyte
from skimage.util import img_as_float
import matplotlib.pyplot as plt
import numpy as np
import glob
from sklearn.decomposition import PCA
from skimage.transform import SimilarityTransform
from skimage.transform import warp
import os
```

## Exercise data and material

The data and material needed for this exercise can be found here: 
[exercise data and material](https://github.com/RasmusRPaulsen/DTUImageAnalysis/tree/main/exercises/ex8-CatsCatsCats/data)

The main part of the data is a large database of photos of cats, where there are also a set of landmarks per photo.

Start by unpacking all the training photos in folder you choose.

## Preprocessing data for machine learning

The photos contains cats in many situations and backgrounds. To make it easier to do machine learning, we will *preprocess* the data, so the photos only contains the face of the cat. Preprocessing is and important step in most machine learning approaches.

The preprocessing steps are:

- Define a model cat (`ModelCat.jpg`) with associated landmarks (`ModelCat.jpg.cat`)
- For each cat in the training data:
  - Use landmark based registration with a *similarity transform* to register the photo to the model cat
  - Crop the registered photo
  - Save the result in a fold called **preprocessed**

**Exercise 1:** *Preprocess all image in the training set. To do the preprocessing, you can use the code snippets supplied* [here](https://github.com/RasmusRPaulsen/DTUImageAnalysis/tree/main/exercises/ex8-CatsCatsCats/data)

The result of the preprocessing is a directory containing smaller photos of the same shape containing cat faces.

## Gathering data into a data matrix

To start, we want to collect all the image data into a data matrix. The matrix should have dimensions `[n_samples, n_features]` where **n_samples** is the number of photos in our training set and **n_features** is the number of values per image. Since we are working with RGB images, the number of features are given by `n_features = height * width * 3`. 

The data matrix can be constructed by:

- Find the number of image files in the **preprocessed** folder using `glob`
- Read the first photo and use that to find the height and width of the photos
- Set **n_samples** and **n_features**
- Make an empty matrix `data_matrix = np.zeros((n_samples, n_features))`
- Read the image files one by one and use `flatten()` to make each image into a 1-D vector (flat_img). 
- Put the image vector (flat_img) into the data matrix by for example `data_matrix[idx, :] = flat_img` , where idx is the index of the current image.

**Exercise 2:** *Compute the data matrix.* 

## Compute and visualize a mean cat

In the data matrix, one row is one cat. You can therefore compute an average cat, **The Mean Cat** by computing one row, where each element is the average of the column. 

**Exercise 2:** *Compute the average cat.* 

You can use the supplied function `create_u_byte_image_from_vector` to create an image from a 1-D image vector.

**Exercise 3:** *Visualize the Mean Cat* 

## Find a missing cat or a cat that looks like it (using image comparison)

Oh! no! You were in such a hurry to get to DTU that you forgot to close your window. Now your cat is gone!!! What to do? 

**Exercise 4:** *Decide that you quickly buy a new cat that looks very much like the missing cat - so nobody notices* 

To find a cat that looks like the missing cat, you start by comparing the missing cat pixels to the pixels of the cats in the training set. The comparison between the missing cat data and the training data can be done using the sum-of-squared differences (SSD).

**Exercise 5:** *Use the `preprocess_one_cat` function to preprocess the photo of the poor missing cat*

**Exercise 6:** *Flatten the pixel values of the missing cat so it becomes a vector of values.*

**Exercise 7:** *Subtract you missing cat data from all the rows in the data_matrix and for each row compute the sum of squared differences. This can for example be done by `sub_distances = np.linalg.norm(sub_data, axis=1)`, where sub_data are the subtracted pixel data.*

**Exercise 8:** *Find the training cat that looks most like your missing cat by finding the cat, where the SSD is smallest. You can for example use `np.argmin`.*

**Exercise 9:** *Extract the found cat from the data_matrix and use `create_u_byte_image_from_vector` to create an image that can be visualized. Did you find a good replacement cat?*

**Exercise 10:** *You can use `np.argmax` to find the cat that looks the least like the missing cat.*

You can also use your own photo of a cat (perhaps even your own cat). To do that you should:

- Place a jpg version of your cat photo in the folder where you had your missing cat photo. Call it for example **mycat.jpg**
- Create a landmark file called something like **mycat.jpg.cat**. It is a text file.
- In the landmark file you should create three landmarks: `3 189 98 235 101 213 142` . Here the first `3` just say there are three landmarks. The following 6 numbers are the (x, y) positions of the right eye, the left eye and the nose. You should manually add these numbers.
- Use the `preprocess_one_cat` function to preprocess the photo
- Now you can do the above routine to match your own cat.

**Optional Exercise:** *Use a photo of your own cat to find its twins*


## Principal component analysis on the cats 

We now move to more classical machine learning on cats. Namely Principal component analysis  (PCA) analysis of the cats image.

To compute the PCA, we use the [sci-kit learn PCA](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html). Not that this version of PCA automatically *centers* data. It means that it will subtract the average cat from all cats for you.

**Exercise 11:** *Start by computing the first 50 principal components:*
```python
print("Computing PCA")
cats_pca = PCA(n_components=50)
cats_pca.fit(data_matrix)
```

This might take some time. If your compute can not handle so many images, you can manually move or delete som photos out of the **preprocessed** folder before computing the data matrix.

The amount of the total variation that each component explains can be found in `cats_pca.explained_variance_ratio_`.

**Exercise 12:** *Plot the amount of the total variation explained by each component as function of the component number.*

**Exercise 13:** *How much of the total variation is explained by the first component?*

We can now project all out cat images into the PCA space (that is 50 dimensional):

**Exercise 14:** *Project the cat images into PCA space*:
```python
components = cats_pca.transform(data_matrix)
```

Now each cat has a position in PCA space. For each cat this position is 50-dimensional vector. Each value in this vector describes *how much of that component* is present in that cat photo.

We can plot the first two dimensions of the PCA space, to see where the cats are placed. The first PCA coordinate for all the cats can be found using `pc_1 = components[:, 0]` .

**Exercise 15:** *Plot the PCA space by plotting all the cats first and second PCA coordinates in a (x, y) plot*

## Cats in space

We would like to explore what the PCA learnt about our cats in the data set. 

### Extreme cats

We start by finding out which cats that have the most *extreme coordinates* in PCA space. 

**Exercise 16:** *Use `np.argmin` and `np.argmax` to find the ids of the cats that have extreme values in the first and second PCA coordinates. Extract the cats data from the data matrix and use `create_u_byte_image_from_vector` to visualize these cats.*

**Exercise 17:** *How do these extreme cat photo look like? Are some actually of such bad quality that they should be removed from the training set*

### The first synthesized cat

We can use the PCA to make a so-called **generative model** that can create synthetic samples from the learnt data. It is done by adding a linear combination of principal components to the average cat image:

$$
I_\text{synth} = I_\text{average} + w_1 * P_1 + w_2 * P_2 + \ldots + w_k * P_k \enspace ,
$$

where we $P_1$ is the first principal component, $P_2$ the second and so on. Here we use $k$ principal components.

The principal components are stored in `cats_pca.components_`. So the first principal component is `cats_pca.components_[0, :]` .

**Exercise 18:** *Create your first fake cat using the average image and the first principal component. You should choose experiment with different weight values (w)* :
```python
synth_cat = average_cat + w * cats_pca.components_[0, :]
```

**Exercise 18:** *Use `create_u_byte_image_from_vector` visualize your fake cat.*

You can use the PCA plot we did before to select some suitable values for w.

**Exercise 19:** *Synthesize some cats, where you use both the first and second principal components and select their individual weights based on the PCA plot.*

### The major cat variation in the data set

A very useful method to get an overview of the **major modes of variation** in a dataset is to synthesize the samples that are lying on the outer edges of the PCA space.

If we for example move a distance out of the first principal axis we can synthesize the cat image there. In this case we will try to move to $\pm \sqrt(\text{explained variance})$, where *explained variance* is the variance explained by that principal component. In code, this will look like:

```python
synth_cat_plus = average_cat + 3 * np.sqrt(cats_pca.explained_variance_[m]) * cats_pca.components_[m, :]
synth_cat_minus = average_cat - 3 * np.sqrt(cats_pca.explained_variance_[m]) * cats_pca.components_[m, :]
```  

here **m** is the principal component that we are investigating.

**Exercise 20:** *Synthesize and visualize cats that demonstrate the first three major modes of variation. Try show the average cat in the middle of a plot, with the negative sample to the left and the positive to the right. Can you recognise some visual patterns in these modes of variation?*

### The Cat Synthesizer (EigenCats)

We are now ready to make true cat synthesizer, where cat images are synthesized based on random locations in PCA space. You can start by setting your `synth_cat = average_cat`. Then you can add all the components you want by for example:

```python
synth_cat = average_cat
for m in range(n_components_to_use):
	w = select a random number in [-3, 3]
	synth_cat = synth_cat + w * np.sqrt(cats_pca.explained_variance_[m]) * cats_pca.components_[m, :]
```

**Exercise 21:** *Generate as many cat photos as your heart desires.*.

## Cat identification in PCA space

Now back to your missing cat. We could find similar cats by computing the difference between the missing cat and all the photos in the databased. Imagine that you only needed to store the 50 weights per cats in your database to do the same type of identification?

**Exercise 22:** *Start by finding the PCA space coordinates of your missing cat:*

```python
im_miss = io.imread("data/cats/MissingCatProcessed.jpg")
im_miss_flat = im_miss.flatten()
im_miss_flat = im_miss_flat.reshape(1, -1)
pca_coords = cats_pca.transform(im_miss_flat)
pca_coords = pca_coords.flatten()
```

The `flatten` calls are needed to bring the arrays into the right shapes.

**Exercise 23:** *Plot all the cats in PCA space using the first two dimensions. Plot your missing cat in the same plot, with another color and marker. Is it placed somewhere sensible and does it have close neighbours?*

We can generate the synthetic cat that is the closest to your missing cat, by using the missing cats position in PCA space:

```python
n_components_to_use = ?
synth_cat = average_cat
for idx in range(n_components_to_use):
	synth_cat = synth_cat + pca_coords[idx] * cats_pca.components_[idx, :]
```

**Exercise 24:** *Generate synthetic versions of your cat, where you change the n_components_to_use from 1 to for example 50.*

We can compute (squared) Euclidean distances in PCA space between your cat and all the other cats by:

```python
comp_sub = components - pca_coords
pca_distances = np.linalg.norm(comp_sub, axis=1)
``` 

**Exercise 25:** *Find the id of the cat that has the smallest and largest distance in PCA space to your missing cat. Visualize these cats. Are they as you expected? Do you think your friends and family will notice a difference?*

You can also find the n closest cats by using the `np.argpartition` function. 

**Exercise 26:** *Find the ids of and visualize the 5 closest cats in PCA space. Do they look like your cat?*

What we have been doing here is what has been used for face identification and face recognition (*Matthew Turk and Alex Pentland: Eigenfaces for Recognition, 1991*)

In summary, we can now synthesize all the cat photos you will only need and we can help people that are loooking for cats that looks like another cat. On top of that, we can now use methods that are considered state-of-the-art before the step into deep learning.



## References
- [Cat data set](https://www.kaggle.com/datasets/crawford/cat-dataset)