# gentex.template package
#
# routines for generating a list of coordinate offsets
# for various template structures

import numpy as np


class Template:
    """
    Class template for generating lists of template voxels

    Class Parameters
    ----------------

    type - string
           (required by constructor) - the type of template
           currently available types are:

    'RectBox' - rectangular box (1,2,3,4 dimensions)
                template origin is center of box
    'RectShell' - shell of rectangular box (1,2,3,4 dimensions)
                template origin is center of shell
    'Ellipsoid' - ellispoid (1,2,3,4 dimensions)
                template origin is center of ellipsoid
    'EllipsoidShell' - ellipsoidal shell (1,2,3,4 dimensions)
                template origin is center of shell
    'Line' - linear template
                template origin is first point of line
    'Notch' - notch template
                template origin is point about which notch is built
    'Cone' - cone template
                template origin is start of half cone
                
    sizes - 1D int array (can be empty)
            array of sizes required for constructing template (required
            by constructor)

    dimension - int
                dimension of template (required by constructor)

    inculsion - bool
                whether or not to include anchor point (i.e. [0], [0,0],...)
                (required by constructor)
                
    handedness - if there are axial asymetries in the template (e.g. Notch)
                 can pass in a vector with +1 for 'right' and -1 for 'left'
                 (default is [1], or [1,1], or...)

    axbase - list of ints (each list of length = dimension)
           basis vector specifying axis, when appropriate, for direction
           of template (can be empty) - component lengths will be ignored;
           only whether the component is zero or nonzero, and the sign will be
           considered (i.e. only co-ordinate axes and '45 degree' lines
           will be considered as template axes), so e.g.
           
           [1,0] ~ [10,0] ~ x-axis in 2D
           [0,1,0] ~ [0,33,0] ~ y-axis in 3D
           [1,-1] ~ [30,-20] ~ [108,-1] ~ 135 degree axis in 2D
           
           if axbase is empty template will pick
           axes according to following conventions:

           - templates requiring single axis specification
             (e.g. line, notch, cone) will always use
             positive direction of first dimension
           - templates requiring multiple axis specification, e.g.
             rectangular parallelipipeds and ellipsoids will choose:
               - largest dimension (e.g. semi-major axis) in positive
                 direction of first dimension
               - next largest dimension (e.g. semi-minor axis) in
                 positive direction of second dimension
               - etc.

    anchoff  - 'dimension' dimensional list of ints
              offset of anchor point from template [0,0,0] in
              template (usually assume [0,0,0])


    shift -   'dimension' dimensional list of ints to use if you
              want to shift all points in offset array - useful, e.g.
              if you want to build cooccurence arrays from offset
              templates - build one template (set of offsets with no shift
              and another with an appropriate shift; those can each be passed
              to the feature space cluster algorithm, then those
              to the cooccurence matrix builder, and that to the texture  
              measure generator.

    offsets - list of int lists of appropriate size
              (based on dimension of template)
              list of of offsets from anchor comprising set of template points
    """

    def __init__(self, type, sizes, dimension, inclusion, handedness=[], axbase=[], anchoff=[], shift=[]):

        self.type = type
        self.sizes = sizes
        self.dim = dimension
        self.me = inclusion
        self.handedness = handedness
        self.offsets = []
        self.axbase = axbase
        self.anchoff = anchoff
        self.shift = shift

        # Set up default handedness
        if self.handedness == []:  # Nothing passed in to constructor
            if self.dim == 1:
                self.handedness = [1]
            if self.dim == 2:
                self.handedness = [1, 1]
            if self.dim == 3:
                self.handedness = [1, 1, 1]
            if self.dim == 4:
                self.handedness = [1, 1, 1, 1]

        # Set up default axis directions
        if self.axbase == []:  # Nothing passed in to constructor
            if self.dim == 1:
                # pick convention for 1 dimension of positve = 1
                # negative = -1
                self.axbase = [1]
            if self.dim == 2:
                self.axbase = [1, 0]
            if self.dim == 3:
                self.axbase = [1, 0, 0]
            if self.dim == 4:
                self.axbase = [1, 0, 0, 0]

        # Set up anchor point offset
        if self.anchoff == []:  # Nothing passed in to constructor
            if self.dim == 1:
                self.anchoff = [0]
            if self.dim == 2:
                self.anchoff = [0, 0]
            if self.dim == 3:
                self.anchoff = [0, 0, 0]
            if self.dim == 4:
                self.anchoff = [0, 0, 0, 0]

        # Set up shift
        if self.shift == []:  # Nothing passed in to constructor
            if self.dim == 1:
                self.shift = [0]
            if self.dim == 2:
                self.shift = [0, 0]
            if self.dim == 3:
                self.shift = [0, 0, 0]
            if self.dim == 4:
                self.shift = [0, 0, 0, 0]

        ################# RECTBOX  #######################
        if type == "RectBox":
            if len(self.sizes) != self.dim:
                print
                "sizes array is of length ", len(self.sizes), "but must be of length ", self.dim, " for type ", type
                # sys.exit(-1)
            # Calculate box limits
            lims = np.zeros((self.dim, 2), int)

            for i in range(self.dim):
                lims[i, 0] = -(self.sizes[0] / 2)
                if self.sizes[0] % 2 == 0:
                    lims[i, 1] = self.sizes[0] / 2
                else:
                    lims[i, 1] = (self.sizes[0] / 2) + 1

            if self.dim == 1:
                for i in range(lims[0, 0], lims[0, 1]):
                    self.offsets.append([i])
                if [0] in self.offsets:
                    self.offsets.remove([0])  # might put back later

            if self.dim == 2:
                for i in range(lims[0, 0], lims[0, 1]):
                    for j in range(lims[1, 0], lims[1, 1]):
                        self.offsets.append([i, j])
                if [0, 0] in self.offsets:
                    self.offsets.remove([0, 0])  # might put back later

            if self.dim == 3:
                for i in range(lims[0, 0], lims[0, 1]):
                    for j in range(lims[1, 0], lims[1, 1]):
                        for k in range(lims[2, 0], lims[2, 1]):
                            self.offsets.append([i, j, k])
                if [0, 0, 0] in self.offsets:
                    self.offsets.remove([0, 0, 0])  # might put back later
            if self.dim == 4:
                for i in range(lims[0, 0], lims[0, 1]):
                    for j in range(lims[1, 0], lims[1, 1]):
                        for k in range(lims[2, 0], lims[2, 1]):
                            for t in range(lims[3, 0], lims[3, 1]):
                                self.offsets.append([i, j, k, t])
                if [0, 0, 0, 0] in self.offsets:
                    self.offsets.remove([0, 0, 0, 0])  # might put back later

        ################# RECTSHELL  #######################
        elif type == "RectShell":

            if len(self.sizes) != self.dim:
                print
                "sizes array is of length ", len(self.sizes), "but must be of length ", self.dim, " for type ", type
                # sys.exit(-1)

            if self.dim == 1:
                sub = self.sizes[0] / 2
                for i in range(self.sizes[0]):
                    if (i == 0 or i == self.sizes[0] - 1):
                        self.offsets.append([i - sub])
            if self.dim == 2:
                sub0 = self.sizes[0] / 2
                sub1 = self.sizes[1] / 2
                for i in range(self.sizes[0]):
                    for j in range(self.sizes[1]):
                        if (i == 0 or i == self.sizes[0] - 1 or j == 0 or j == self.sizes[1] - 1):
                            self.offsets.append([i - sub0, j - sub1])

            if self.dim == 3:
                sub0 = self.sizes[0] / 2
                sub1 = self.sizes[1] / 2
                sub2 = self.sizes[2] / 2
                for i in range(self.sizes[0]):
                    for j in range(self.sizes[1]):
                        for k in range(self.sizes[2]):
                            if (i == 0 or i == self.sizes[0] - 1 or j == 0 or j == self.sizes[1] - 1 or k == 0 or k ==
                                    self.sizes[2] - 1):
                                self.offsets.append([i - sub0, j - sub1, k - sub2])

            if self.dim == 4:
                sub0 = self.sizes[0] / 2
                sub1 = self.sizes[1] / 2
                sub2 = self.sizes[2] / 2
                sub3 = self.sizes[3] / 2
                for i in range(self.sizes[0]):
                    for j in range(self.sizes[1]):
                        for k in range(self.sizes[2]):
                            for t in range(self.sizes[3]):
                                if (i == 0 or i == self.sizes[0] - 1 or j == 0 or j == self.sizes[
                                    1] - 1 or k == 0 or k == self.sizes[2] - 1 or t == 0 or t == self.sizes[3] - 1):
                                    self.offsets.append([i - sub0, j - sub1, k - sub2, t - sub3])
        ################# ELLIPSOID  #######################
        elif type == "Ellipsoid":

            if len(self.sizes) != self.dim:
                print
                "sizes array is of length ", len(self.sizes), "but must be of length ", self.dim, " for type ", type
                # sys.exit(-1)

            if self.dim == 1:  # same as 1D rectangular box
                sub = self.sizes[0] / 2
                for i in range(self.sizes[0]):
                    self.offsets.append([i - sub])
            if self.dim == 2:
                sub0 = self.sizes[0] / 2
                sub1 = self.sizes[1] / 2
                s02 = self.sizes[0] * self.sizes[0]
                s12 = self.sizes[1] * self.sizes[1]
                for i in range(self.sizes[0]):
                    for j in range(self.sizes[1]):
                        bounder = ((i - sub0) * (i - sub0)) / s02 + ((j - sub1) * (j - sub1)) / s12
                        if (bounder <= 1.0):
                            self.offsets.append([i - sub0, j - sub1])
            if self.dim == 3:
                sub0 = self.sizes[0] / 2
                sub1 = self.sizes[1] / 2
                sub2 = self.sizes[2] / 2
                s02 = self.sizes[0] * self.sizes[0]
                s12 = self.sizes[1] * self.sizes[1]
                s22 = self.sizes[2] * self.sizes[2]
                for i in range(self.sizes[0]):
                    for j in range(self.sizes[1]):
                        for k in range(self.sizes[2]):
                            bounder = ((i - sub0) * (i - sub0)) / s02 + ((j - sub1) * (j - sub1)) / s12 + (
                                                                                                          (k - sub2) * (
                                                                                                          k - sub2)) / s22
                            if (bounder <= 1.0):
                                self.offsets.append([i - sub0, j - sub1, k - sub2])

            if self.dim == 4:
                print
                "Sorry 4D ellipsoids not yet implemented"
                # sys.exit(-1)

        ################# ELLIPSOIDSHELL  #######################
        elif type == "EllipsoidShell":

            if len(self.sizes) != self.dim:
                print
                "sizes array is of length ", len(self.sizes), "but must be of length ", self.dim, " for type ", type
                # sys.exit(-1)

            if self.dim == 1:  # Same as 1D rectangular shell
                sub = self.sizes[0] / 2
                for i in range(self.sizes[0]):
                    if (i == 0 or i == self.sizes[0] - 1):
                        self.offsets.append([i - sub])

            # FIX ME !!! - Haven't used or tested 2,3 dim ellipsoidal shells
            if self.dim == 2:
                sub0 = self.sizes[0] / 2
                sub1 = self.sizes[1] / 2
                s02 = self.sizes[0] * self.sizes[0]
                s12 = self.sizes[1] * self.sizes[1]
                for i in range(self.sizes[0]):
                    for j in range(self.sizes[1]):
                        bounder = ((i - sub0) * (i - sub0)) / s02 + ((j - sub1) * (j - sub1)) / s12
                        if (bounder > 0.9 and bounder < 1.1):  # Need to figure
                            self.offsets.append([i - sub0, j - sub1])  # out these bounds
            if self.dim == 3:
                sub0 = self.sizes[0] / 2
                sub1 = self.sizes[1] / 2
                sub2 = self.sizes[2] / 2
                s02 = self.sizes[0] * self.sizes[0]
                s12 = self.sizes[1] * self.sizes[1]
                s22 = self.sizes[2] * self.sizes[2]
                for i in range(self.sizes[0]):
                    for j in range(self.sizes[1]):
                        for k in range(self.sizes[2]):
                            bounder = ((i - sub0) * (i - sub0)) / s02 + ((j - sub1) * (j - sub1)) / s12 + (
                                                                                                          (k - sub2) * (
                                                                                                          k - sub2)) / s22
                            if (bounder > 0.9 and bounder < 1.1):  # Need to figure
                                self.offsets.append([i - sub0, j - sub1, k - sub2])  # out these bounds

            if self.dim == 4:
                print
                "Sorry 4D ellipsoidal shells not yet implemented"
                # sys.exit(-1)

        #################  LINE  #######################
        elif type == "Line":

            if len(self.sizes) != 1:
                print
                "sizes array is of length ", len(self.sizes), "but must be of length 1 for type ", type
                # sys.exit(-1)

            proto = np.sign(self.axbase)  # Generate axis (rely on dimension
            # being correct re. above check)
            for i in range(1, self.sizes[0] + 1):
                self.offsets.append(list(i * proto))

        ################  NOTCH  #######################
        elif type == "Notch":

            if len(self.sizes) != 1:
                print
                "self.sizes array is of length ", len(self.sizes), "but must be of length 1 for type ", type
            # sys.exit(-1)
            proto = list(np.sign(self.axbase))
            if self.dim == 1:
                print
                "Sorry, no definition for 1 dimensional notches"
                # sys.exit(-1)

            if self.dim == 2:
                # proto must be one of [1,0],[-1,0],[0,1],[0,-1]
                # if not assume [1,0]
                protoset = [[1, 0], [-1, 0], [0, 1], [0, -1]]
                if proto not in protoset:
                    proto = [1, 0]
                if proto == [1, 0]:
                    for i in range(self.sizes[0] + 1):
                        for j in range(-self.sizes[0], self.sizes[0] + 1):
                            if (i > 0 or j <= 0):
                                self.offsets.append([i, j])
                if proto == [-1, 0]:
                    for i in range(-self.sizes[0], 1):
                        for j in range(-self.sizes[0], self.sizes[0] + 1):
                            if (i < 0 or j <= 0):
                                self.offsets.append([i, j])
                if proto == [0, 1]:
                    for i in range(-self.sizes[0], self.sizes[0] + 1):
                        for j in range(self.sizes[0] + 1):
                            if (j > 0 or i >= 0):
                                self.offsets.append([i, j])
                if proto == [0, -1]:
                    for i in range(-self.sizes[0], self.sizes[0] + 1):
                        for j in range(-self.sizes[0], 1):
                            if (j < 0 or i >= 0):
                                self.offsets.append([i, j])

            if self.dim == 3:
                protoset = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
                if proto not in protoset:
                    proto = [1, 0, 0]
                if proto == [1, 0, 0]:
                    for i in range(self.sizes[0] + 1):
                        for j in range(-self.sizes[0], self.sizes[0] + 1):
                            for k in range(-self.sizes[0], self.sizes[0] + 1):
                                if (i > 0 or (i >= 0 and j > 0) or (j >= 0 and k > 0)):
                                    self.offsets.append([i, j, k])

                if proto == [-1, 0, 0]:
                    for i in range(-self.sizes[0], self.sizes[0]):
                        for j in range(-self.sizes[0], self.sizes[0] + 1):
                            for k in range(-self.sizes[0], self.sizes[0] + 1):
                                if (i < 0 or (i <= 0 and j < 0) or (j <= 0 and k < 0)):
                                    self.offsets.append([i, j, k])

                if proto == [0, 1, 0]:
                    for j in range(self.sizes[0] + 1):
                        for k in range(-self.sizes[0], self.sizes[0] + 1):
                            for i in range(-self.sizes[0], self.sizes[0] + 1):
                                if (j > 0 or (j >= 0 and i > 0) or (i >= 0 and k < 0)):
                                    self.offsets.append([i, j, k])

                if proto == [0, -1, 0]:
                    for j in range(-self.sizes[0], self.sizes[0]):
                        for k in range(-self.sizes[0], self.sizes[0] + 1):
                            for i in range(-self.sizes[0], self.sizes[0] + 1):
                                if (j < 0 or (j <= 0 and i > 0) or (i >= 0 and k < 0)):
                                    self.offsets.append([i, j, k])

                if proto == [0, 0, 1]:
                    for k in range(self.sizes[0] + 1):
                        for i in range(-self.sizes[0], self.sizes[0] + 1):
                            for j in range(-self.sizes[0], self.sizes[0] + 1):
                                if (k > 0 or (k >= 0 and j < 0) or (j <= 0 and i > 0)):
                                    self.offsets.append([i, j, k])

                if proto == [0, 0, -1]:
                    for k in range(-self.sizes[0], self.sizes[0]):
                        for i in range(-self.sizes[0], self.sizes[0] + 1):
                            for j in range(-self.sizes[0], self.sizes[0] + 1):
                                if (k < 0 or (k <= 0 and j > 0) or (j >= 0 and i < 0)):
                                    self.offsets.append([i, j, k])

            if self.dim == 4:
                print
                "Sorry 4D notches not yet implemented"
                # sys.exit(-1)

        #################  CONE #######################
        elif type == "Cone":
            # currently only cones along coordinate axis are supported

            if len(self.sizes) != 1:
                print
                "sizes array is of length ", len(self.sizes), "but must be of length 1 for type ", type
                # sys.exit(-1)
            proto = list(np.sign(self.axbase))

            if self.dim == 1:
                for i in range(self.sizes[0]):
                    self.offsets.append([i])

            if self.dim == 2:
                protoset = [[1, 0], [-1, 0], [0, 1], [0, -1]]
                if proto not in protoset:
                    proto = [1, 0]
                if proto == [1, 0]:
                    for i in range(self.sizes[0]):
                        for j in range(-i, i + 1):
                            self.offsets.append([i, j])
                if proto == [-1, 0]:
                    for i in range(self.sizes[0]):
                        for j in range(-i, i + 1):
                            self.offsets.append([-i, j])
                if proto == [0, 1]:
                    for j in range(self.sizes[0]):
                        for i in range(-j, j + 1):
                            self.offsets.append([i, j])
                if proto == [0, -1]:
                    for j in range(self.sizes[0]):
                        for i in range(-j, j + 1):
                            self.offsets.append([i, -j])

            if self.dim == 3:
                protoset = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
                if proto not in protoset:
                    proto = [1, 0, 0]
                if proto == [1, 0, 0]:
                    for i in range(self.sizes[0]):
                        for j in range(-i, i + 1):
                            for k in range(-i, i + 1):
                                self.offsets.append([i, j, k])
                if proto == [-1, 0, 0]:
                    for i in range(self.sizes[0]):
                        for j in range(-i, i + 1):
                            for k in range(-i, i + 1):
                                self.offsets.append([-i, j, k])

                if proto == [0, 1, 0]:
                    for j in range(self.sizes[0]):
                        for k in range(-j, j + 1):
                            for i in range(-j, j + 1):
                                self.offsets.append([i, j, k])

                if proto == [0, -1, 0]:
                    for j in range(self.sizes[0]):
                        for k in range(-j, j + 1):
                            for i in range(-j, j + 1):
                                self.offsets.append([i, -j, k])

                if proto == [0, 0, 1]:
                    for k in range(self.sizes[0]):
                        for i in range(-k, k + 1):
                            for j in range(-k, k + 1):
                                self.offsets.append([i, j, k])

                if proto == [0, 0, -1]:
                    for k in range(self.sizes[0]):
                        for i in range(-k, k + 1):
                            for j in range(-k, k + 1):
                                self.offsets.append([i, j, -k])
            if self.dim == 4:
                # just do it in 4th dimension for now
                protoset = [[0, 0, 0, 1], [0, 0, 0, -1]]
                if proto not in protoset:
                    proto = [0, 0, 0, 1]
                if proto == [0, 0, 0, 1]:
                    for t in range(self.sizes[0]):
                        for i in range(-t, t + 1):
                            for j in range(-t, t + 1):
                                for k in range(-t, t + 1):
                                    self.offsets.append([i, j, k, t])

                if proto == [0, 0, 0, -1]:
                    for t in range(self.sizes[0]):
                        for i in range(-t, t + 1):
                            for j in range(-t, t + 1):
                                for k in range(-t, t + 1):
                                    self.offsets.append([i, j, k, -t])

        else:
            print
            "Type ", type, " unknown"
            # sys.exit(-1)

        for i in range(len(self.offsets)):
            self.offsets[i] = list(np.array(self.offsets[i]) + np.array(self.shift))

        # Add/Remove anchor point as requested
        if inclusion and (self.anchoff not in self.offsets):
            self.offsets.append(self.anchoff)
        if (not inclusion) and (self.anchoff in self.offsets):
            self.offsets.remove(self.anchoff)

        # Apply handedness
        tempoff = []
        for off in self.offsets:
            tempoff.append(list(np.array(off) * np.array(self.handedness)))
        self.offsets = tempoff
