# gentex.feature package
#
# note - what's in init should be rewritten in C similar to makecomat.c
# for a significant speed increase - current question is how
#        to handle the possibility of being handed a variable number
#        of images and the mask to build the feature space with, using cytypes

import numpy as np


class features:
    """
    Class features for generating and manipulating feature spaces

    Class Methods
    --------------

    __init__(images,mask,template)

    
    clusfs(method,numclus,clusmax)

    Class Variables
    ----------------

    Class variables required by constructor:

    images:   array of 1-4 dimensional ndarrays (images) used to build
              feature space

    mask:     1-4 dimensional mask used to determines which
              voxels to use for building feature space

    template: set of points relative to an anchor point
              used to build feature space

    Internal class variables:

    fs:       P x F ndarray constituing feature space. P is the number
              of points in the image(s) such that the template fell
              within the mask and hence generated a feature space
              point. F is the number of features (i.e. number of template
              points times number of images)

    fsc:      P X D ndarray constituing array of coordinates associated with
              the points in feature space where as for fs, P is the number
              of points in the image(s) such that the template fell
              within the mask, and D is the underlying dimension of the
              image space.

    fsmask    Image mask with 1's where the template coordinates were
              inside the image and mask (i.e. image coordinates for which
              the feature space points were obtained)
              
    clusim    clustered feature space image - currently uses kmeans
              to cluster the image using the feature space values

    numclus - int
              Number of clusters used to generate segmented image

    clusmax - int
              if numclus is passed to the clusfs() function with a value
              less than 2 then clusf() will try to determine the optimal
              number of clusters (if the default 'Kmeans' method is being
              used) and clusmax specifies the maximum number of clusters
              to try

              default = 20
              

    cluscrit - string
               penalty method to use with k-means to determine
               number of epsilon machine states when estimating
               epsilon machine from the cooccurence matrix.
               One of:
               'AIC' - Akaike's information criterion [Akaike, 1974]
               'BIC' - Bayesian information criterion [Schwartz, 1978]
               'ICL' - Integrated completed likelihood [Biernacki, 2000]
               
               default = 'BIC'
    
    """

    def __init__(self, images, mask, template):

        self.images = images
        self.mask = mask
        self.template = template
        self.fs = np.array([], dtype=np.float32)
        self.fsc = np.array([], dtype=np.int16)
        self.fsmask = np.zeros(self.images[0].shape, dtype=np.int16)
        self.foundfeat = 0
        self.clusim = np.zeros(self.images[0].shape, dtype=np.int16)
        self.numclus = 3
        self.cluscrit = 'BIC'
        self.clusmax = 20

        # Need to do conversion to numpy.int16 here (and back later)
        # to squeeze as much memory as we can for big images

        # Make sure images and mask have same dimension
        self.dims = images[0].shape
        assert len(self.dims) == len(self.mask.shape)
        # same for images and template
        assert len(self.dims) == len(template[0])

        # Determinxe number of features
        self.numfeats = len(template) * len(images)

        # Get upper and lower bounds in image to grab
        # by getting max and min values from template
        # points
        maxs = np.max(np.array(self.template), axis=0)
        mins = np.min(np.array(self.template), axis=0)
        # don't bump into edge of array
        uplim = self.dims - maxs
        # for negative offsets need to move away from lower boundary
        # otherwise can start at zero
        lowlim = np.where(np.greater(-mins, 0), -mins, 0)
        # Get feature space co-ordinate array, fsc;
        # already determined by image parsing limits uplim,lowlim
        ind = np.indices(uplim - lowlim)
        # self.fsc = np.transpose(np.array([np.ravel(ind[i]+lowlim[i]) for i in range(len(lowlim))]))
        self.fsc = np.array([np.ravel(ind[i] + lowlim[i]) for i in range(len(lowlim))], dtype=np.int16)
        # Now get feature space columns, i.e. each column is
        # a combination of image + template element
        # This is REALLY parallelizable - i.e. each column can be done
        # independently
        imcount = 0
        colcount = 0
        for im in images:  #
            for temp in template:  # template points
                upl = uplim + temp
                downl = lowlim + temp
                # Thanks to Robert Kern for the following bit of index magic
                thiscol = np.ravel(
                    (np.where(self.mask == 1, im, np.inf))[tuple([slice(down, up) for down, up in zip(downl, upl)])])
                # Do some gymnastics for shortening feature space vectors
                # as you go re. memory efficiency
                if colcount == 0:
                    badelts = np.array(np.where(thiscol == np.inf)[0])
                    # oops !
                    # self.fs = np.array(np.delete(thiscol,badelts,0),dtype=np.int16)
                    self.fs = np.array(np.delete(thiscol, badelts, 0), dtype=np.float32)
                else:
                    badnew = np.array(np.where(thiscol == np.inf)[0])
                    newstack = np.array(np.delete(thiscol, badelts, 0), dtype=np.float32)
                    shortnew = np.where(newstack == np.inf)[0]
                    badelts = np.array(np.unique(np.append(badelts, badnew)))
                    if colcount == 1:
                        if newstack.size != 0:
                            self.fs = np.vstack((np.delete(self.fs, shortnew, 0), np.delete(newstack, shortnew, 0)))
                    else:
                        if newstack.size != 0:
                            self.fs = np.vstack((np.delete(self.fs, shortnew, 1), np.delete(newstack, shortnew, 0)))
                colcount += 1
            del (im)
            imcount += 1
        self.fs = np.transpose(self.fs)
        # Delete bad elements from coordinate space
        self.fsc = np.array(np.delete(self.fsc, badelts, 1), dtype=np.int16)
        self.fsc = tuple(self.fsc)
        self.fsmask[self.fsc] = 1
        # NOTE: The above could easily be generalized to handle
        # different templates in the different images.
        # The feature space would be more complicated, i.e. would have
        # to AND different masks but what the heck...


    def clusfs(self, method="Kmeans", numclus=3, clusmax=20, cluscrit='BIC'):
        """
        method clusfs - clusters feature space

        With no arguments clusfs uses Kmeans (only clustering method
        currently implemented) to cluster the feature space points
        into 3 clusters. The user can specify a set of arguments that
        either specify a set number of clusters to use or asks clusfs
        to try and find the best number of clusters using a Gaussian
        likelihood and a penalty term the form of which can be specified
        by the user (currently AIC or BIC are the only choices available)

        optional arguments:

        method - clustering method, currently Kmeans is the only method
                 implemented

                 default = 'Kmeans'

        numclus - number of clusters to try; if this number is less than 2
                  clusfs will try to find the best number of clusters,
                  trying up to clusmax.

                  default = 3

        clusmax - the largest number of clusters that clusfs will try

                  default = 20

        cluscrit - the 'overfitting' criteria used as a penalty term in
                   conjuction with a Gaussian likelihood term that estimates
                   the fidelity of the clustering. See, e.g.
                   
                   Goutte C, Hansen LK, Liptrot MG, Rostrup E.
                   Feature-space clustering for fMRI meta-analysis.
                   Hum Brain Mapp. 2001 Jul;13(3):165-83.
        
        """
        self.numclus = numclus

        self.clusmax = clusmax

        self.cluscrit = cluscrit

        if method == "Kmeans":
            import scipy.cluster as sc
            # set up array of optimization values
            opto = []
            b = sc.vq.whiten(self.fs)
            if self.cluscrit == "ICL":
                print("Haven't implemented ICL yet, using BIC...")
            if numclus < 2:  # numclus < 2 means try to find "best" cluster size
                for i in range(2, min([self.clusmax + 1, self.fs.shape[0] + 1])):
                    z = sc.vq.kmeans(b, i)
                    t = sc.vq.kmeans2(b, z[0])
                    if i == self.fs.shape[0]:  # perfect explanation !
                        lh = 1.0
                    else:
                        # Not sure this works - Supposed to be Gaussian - see
                        # Gouette et al. mentioned above.
                        sig = (1. / b.shape[0]) * np.sum((np.abs(t[0][t[1]] - b)) ** 2)
                        lh = np.sum(np.log2(1. / (np.sqrt(2. * np.pi * sig * sig))) * np.exp(
                            -((1. / (2. * sig * sig)) * np.sum((t[0][t[1]] - b) ** 2, axis=1))))
                        # Could als try something like log2(1 -"distortion")
                        # lh = np.log2(1.0 - z[1])
                        if self.cluscrit == "AIC":
                            opto.append(lh - (i * self.fs.shape[1] + 1))
                        elif self.cluscrit == "ICL":
                            # later, man - stick BIC here for now
                            print("Warning: ICL not quite ready, using BIC")
                            opto.append(lh - ((i * self.fs.shape[1] + 1) / 2.) * np.log2(self.fs.shape[1]))
                        else:  # for now assume anything else means default, i.e. BIC
                            opto.append(lh - ((i * self.fs.shape[1] + 1) / 2.) * np.log2(self.fs.shape[1]))
                            # print i,lh,opto
                            # Find where max cluster size is in opto and generate clus size
                self.numclus = np.array(opto).argmax() + 2
                # urk, do it again
                z = sc.vq.kmeans(sc.vq.whiten(self.fs), self.numclus)
                t = sc.vq.kmeans2(sc.vq.whiten(self.fs), z[0])
                self.clusim[self.fsc] = t[1]
                print("Using", self.numclus, "clusters for feature space")
            else:  # just use self.numclus
                z = sc.vq.kmeans(sc.vq.whiten(self.fs), self.numclus)
                t = sc.vq.kmeans2(sc.vq.whiten(self.fs), z[0])
                self.clusim[self.fsc] = t[1]
        else:
            print("Sorry Kmeans only clustering method currently supported")
        
            
        
        
