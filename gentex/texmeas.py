"""  gentex.texmeas package

"""

import numpy as np


class Texmeas:
    """
    Class texmeas for generating texture measures from co-occurence
    matrix
    
    Class Methods
    --------------

    __init__(comat) - initializes the class; requires a cooccurence
                      matrix for construction and can be passed
                      any of the optional arguments listed below
                      re. 'available to constructor'

    calc_measure(measure) - passed one of the strings listed below
                            available for the class variable measure,
                            calculates the appropriate measure and
                            puts the value in the class variable val.
                            For info. on epsilon machine related
                            complexity/entropy measures see reference
                            list provided below in description of the
                            est_em() function. For a disucssion of
                            Haralick cooccurence style texture measures
                            see:
                            R. M. Haralick, 'Statistical and structural
                            approaches to texture'. Proceedings of the IEEE
                            May 1979, 67(5). 786-804 
                            


    est_em() - estimate an epsilon machine from a
               cooccurence matrix with #rows = #cols, done
               implicitly whenever one of the related
               complexity/entropy measures (EM Entropy,
               Statistical Complexity,Epsilon Machine Run Length )
               are calculated - for info. an epsilon machines and
               the related measures see:

               K. Young, Y. Chen, J. Kornak, G. B. Matson, N. Schuff,
               'Summarizing complexity in high dimensions',
               Phys Rev Lett. (2005) Mar 11;94(9):098701.

               C. R. Shalizi and J. P. Crutchfield, 'Computational
               Mechanics: Pattern and Prediction, Structure and Simplicity',
               Journal of Statistical Physics 104 (2001) 819--881.

               K. Young and J. P. Crutchfield, 'Fluctuation Spectroscopy',
               Chaos, Solitons, and Fractals 4 (1993) 5-39.

               J. P. Crutchfield and K. Young, 'Computation at the
               Onset of Chaos', in Entropy, Complexity, and Physics of
               Information, W. Zurek, editor, SFI Studies in the Sciences
               of Complexity, VIII, Addison-Wesley, Reading, Massachusetts
               (1990) 223-269. 
               
               C. R. Shalizi and J. P. Crutchfield, 'Computational
               Mechanics: Pattern and Prediction, Structure and Simplicity',
               Journal of Statistical Physics 104 (2001) 819--881. 
    

    Class Variables
    ----------------

    Class variables required by constructor:

    comat -    non-normalized cooccurence matrix - 
               chi-squared conditinal distribution
               comparisons require the actual number
               of counts so don't normalize this before
               sending in

    Class variables available to constructor:

    measure -  string
               texture meaure; choice of:
               'CM Entropy'
               'EM Entropy'
               'Statistical Complexity'
               'Energy Uniformity'
               'Maximum Probability'
               'Contrast'
               'Inverse Difference Moment'
               'Correlation'
               'Probability of Run Length'
               'Epsilon Machine Run Length'
               'Run Length Asymmetry'
               'Homogeneity'
               'Cluster Tendency'
               'Multifractal Spectrum Energy Range'
               'Multifractal Spectrum Entropy Range'
               
               default = 'Statistical Complexity'

    coordmom - int
               moment of coordinate differences in cooccurence matrix
               needed for calculating 'Contrast' and
               'Inverse Difference Moment'
               default = 0

    probmom -  int
               moment of individual cooccurence probabilities
               needed for calculating 'Contrast' and
               'Inverse Difference Moment'
               
               default = 0

    rllen -    int
               length of run length used for generating probability
               of a run length (the higher this probability the
               larger the constant patches on the scale used for generating
               the co-occurence matrix) or the epsilon machine run length
               
               default = 0

    clusmom -  int
               moment used for generating cooccurence cluster tendency
               
               default = 0
               
    samelev - boolean
              whether to treat the rows and columns in the cooccurence
              matrix as identical 'states' (the methods are very general
              so this needn't be the case, e.g. different template shapes
              from different images with different quantization levels
              could be used to generate the cooccurence matrix which could
              be of arbitrary shape)
              
              default - True (assumes the cooccurrence matrix is square
                              and the rows and columns correspond to the same
                              'state')
    betas -   array
              an array of 3 values, the lower limit, the upper limit and
              the number of steps to use as the 'inverse temperature' range
              for estimating the multifractal spectrum from an epsilon machine
              - getting the range right for an 'arbitrary' epsilon machine is
              tricky and is expected to be reset over a number of trials before
              getting a full spectrum estimate. For details on the rationale
              and algorithm see:
              
              K. Young and J. P. Crutchfield, 'Fluctuation Spectroscopy',
              Chaos, Solitons, and Fractals 4 (1993) 5-39.

    Internal class variables:

    emclus - number of clusters ('states') found when estimating an epsilon
             machine from the cooccurence matrix.

    emest - whether or not an epsilon machine has been estimated yet

    emmat - the estimated epsilon machine as a standard Markov process
            transition matrix.

    condo - cooccurence matrix renormailzed as a rowise matrix of conditional
            probabilites - built as part of epsilon machine estimation

    emclasses - list of which of the values in emclus each row in condo
                (and hence the cooccurence matrix) belongs to

    clusp - chisquared p value to use for clustering epsilon machine rows

    val -      float
               value of most recently calculated texture measure

    mfsspec - array
              array containing the multifractal spectral estimates obtained
              over the range of 'inverse temperatures' provided in betas

    currval - string
              one of the above listed values for measure specifying
              which of the meaures constitutes the current value in val
              (the most recently calculated value) and is equal to one of
              the values in the variables listed below (and which correspond
              to the appropriate measures)

    The following variables (Haralick measures and epsilon machine related
    quantities) are initialized to NaN so if that's what you get when
    asking for that variable that measure has not been estimated yet.

    cme -       CM Entropy
    eme -       EM Entropy
    stc -       Statistical Complexity
    enu -       Energy Uniformity
    map -       Maximum Probability
    con -       Contrast
    idm -       Inverse Difference Moment
    cor -       Correlation
    prl -       Probability of Run Length
    erl -       Epsilon Machine Run Length
    rla -       Run Length Asymmetry
    hom -       Homogeneity
    clt -       Cluster Tendency
    mfu -       Multifractal Spectrum Energy Range
    mfs -       Multifractal Spectrum Entropy Range
            
    """

    def __init__(self, comat, measure="Statistical Complexity", coordmom=0, probmom=0, rllen=0, clusmom=0, clusp=0.001,
                 samelev=True, betas=[-20, 20, 40]):

        self.comat = comat
        self.totcount = np.sum(comat)  # to get back histo after norm
        self.measure = measure
        self.coordmom = coordmom
        self.probmom = probmom
        self.rllen = rllen
        self.clusmom = clusmom
        self.clusp = clusp  # chisquared p value to use for conditional
        # distribution similarity

        self.emclus = 0  # record the actual number of clusters
        # found for the epsilon machine

        self.emest = False  # whether or not epsilon machine has been
        # estimated

        self.mfsest = False  # whether or not multifractal spectrum has
        # been estimated
        self.emmat = np.array([])  # epsilon machine pre-array

        self.condo = np.array([])  # raw em transition matrix (i..e
        # array of conditional distributions
        self.emclasses = np.array([])  # list of which class each row
        # of self.emmat belongs to
        self.samelev = samelev  # Boolean for whether pre and post
        # epsilon machine states should be
        # treated as the same
        if self.comat.shape[0] != self.comat.shape[1]:
            self.samelev = False  # - should automatically be set here
            # to false if # rows != #cols in
            # co-occurence matrix

        self.betas = betas  # "inverse temperature" range and
        # step for estimating multifractal
        # spectrum from epsilon machine

        self.val = 0.0
        self.currval = ""
        self.cme = np.nan  # CM Entropy
        self.eme = np.nan  # EM Entropy
        self.stc = np.nan  # Statistical Complexity
        self.enu = np.nan  # Energy Uniformity
        self.map = np.nan  # Maximum Probability
        self.con = np.nan  # Contrast
        self.idm = np.nan  # Inverse Difference Moment
        self.cor = np.nan  # Correlation
        self.prl = np.nan  # Probability of Run Length
        self.erl = np.nan  # Epsilon Machine Run Length
        self.rla = np.nan  # Run Length Asymmetry
        self.hom = np.nan  # Homogeneity
        self.clt = np.nan  # Cluster Tendency
        self.mfu = np.nan  # Multifractal max,min energy diff.
        self.mfs = np.nan  # Multifractal max,min entropy diff.

        # initial empty array for the multifractal spectrum
        # with size equla to the number of steps specified in self.betas
        self.mfsspec = np.array([])

        # Normalize cooccurence matrix in case it's not
        if np.sum(self.comat) != 1.0:
            self.comat = np.float_(self.comat) / np.sum(self.comat)

        # Actually normalize row vectors... -- NO !! --
        # if np.sum(self.comat) != self.comat.shape[0]:
        # self.comat = np.transpose(np.transpose(np.float_(self.comat))/np.float_(np.sum(self.comat,axis=1)))

        # Calculate an initial texture measure
        self.calc_measure(self.measure)

    def calc_measure(self, measure='Statistical Complexity', coordmom=0, probmom=0, rllen=0, clusmom=0, samelev=True):
        """
        Passed one of the strings:
        
        'CM Entropy'
        'EM Entropy'
        'Statistical Complexity'
        'Energy Uniformity'
        'Maximum Probability'
        'Contrast'
        'Inverse Difference Moment'
        'Correlation'
        'Probability of Run Length'
        'Epsilon Machine Run Length'
        'Run Length Asymmetry'
        'Homogeneity'
        'Cluster Tendency'
        'Multifractal Spectrum Energy Range'
        'Multifractal Spectrum Entropy Range'
        
        calculates the appropriate texture measure and
        puts the value in the class variable val and
        updates the class variable currval with the passed
        string
        """

        self.measure = measure

        # Allow for changed values of the following class variables
        # to be passed to calc measure
        if coordmom != 0:
            self.coordmom = coordmom
        if probmom != 0:
            self.probmom = probmom
        if rllen != 0:
            self.rllen = rllen
        if clusmom != 0:
            self.clusmom = clusmom
        if samelev == False:
            self.samelev = False

        if self.measure == "CM Entropy":
            if np.isnan(self.cme):
                self.cme = np.sum(
                    -np.where(self.comat > 0.0, self.comat, 1.0) * np.where(self.comat > 0.0, np.log2(self.comat), 0.0))

            self.val = self.cme
            self.currval = "CM Entropy"

        elif self.measure == "EM Entropy":
            if np.isnan(self.eme):
                import scipy.linalg as L

                if not self.emest:
                    self.est_em()
                # get left eigenvector associated with lambda = 1
                # (largest eignevalue)
                [e, v] = L.eig(np.nan_to_num(self.emmat), left=True, right=False)
                # Node probabilities are elements of normalized left eigenvector
                # associated with eigenvale 1 (assumes Scipy convention of
                # returning sorted eignevalues so eignevalue 1 in this case is
                # the first element of the returned eigenvalue array)
                # nodep = v[:,0]/sum(v[:,0])
                # ---- no longer make the above assumption
                # found it was wrong - now specifically ask for eigenvector
                # associated with eigenvalue 1 (greatest real part)
                maxind = np.where(np.real(e) == np.max(np.real(e)))[0][0]
                nodep = v[:, maxind] / sum(v[:, maxind])
                self.eme = -np.sum(
                    np.transpose(nodep * np.ones(self.emmat.shape)) * (self.emmat * np.nan_to_num(np.log2(self.emmat))))

            self.val = self.eme
            self.currval = "EM Entropy"

        elif self.measure == "Statistical Complexity":
            if np.isnan(self.stc):
                import scipy.linalg as L
                # estimate epsilon machine if it hasn't been made
                if not self.emest:
                    self.est_em()
                # get left eigenvector associated with lambda = 1
                # (largest eignevalue)
                [e, v] = L.eig(np.nan_to_num(self.emmat), left=True, right=False)
                # Node probabilities are elements of normalized left eigenvector                # associated with eigenvale 1 (assumes Scipy convention of
                # returning sorted eignevalues so eignevalue 1 in this case is
                # the first element of the returned eigenvalue array)
                # nodep = v[:,0]/sum(v[:,0])
                # ---- no longer make the above assumption
                # found it was wrong - now specifically ask for eigenvector
                # associated with eigenvalue 1 (greatest real part)
                maxind = np.where(np.real(e) == np.max(np.real(e)))[0][0]
                nodep = v[:, maxind] / sum(v[:, maxind])
                self.stc = -np.sum(nodep * np.log2(nodep))

            self.val = self.stc
            self.currval = "Statistical Complexity"

        elif self.measure == "Energy Uniformity":
            if np.isnan(self.enu):
                self.enu = np.sum(np.where(self.comat > 0.0, self.comat * self.comat, 0.0))
            self.val = self.enu
            self.currval = "Energy Uniformity"

        elif self.measure == "Maximum Probability":
            if self.map is np.nan:
                self.map = np.max(self.comat)

            self.val = self.map
            self.currval = "Maximum Probability"

        elif self.measure == "Contrast":
            if np.isnan(self.con):
                if self.coordmom == 0 or self.probmom == 0:
                    if self.coordmom == 0:
                        print("Nonzero coordinate moment is required for calculating Contrast")
                    if self.probmom == 0:
                        print("Nonzero probability moment is required for calculating Contrast")
                else:
                    crows = np.zeros(self.comat.shape)
                    ccols = np.zeros(self.comat.shape)
                    for i in range(self.comat.shape[0]):
                        crows[i, :] = i
                        ccols[:, i] = i

                    self.con = np.sum((np.abs(crows - ccols) ** self.coordmom) * (self.comat ** self.probmom))

            self.val = self.con
            self.currval = "Contrast"

        elif self.measure == "Inverse Difference Moment":
            if np.isnan(self.idm):
                if self.coordmom == 0 or self.probmom == 0:
                    if self.coordmom == 0:
                        print("Nonzero coordinate moment is required for calculating Inverse Difference Moment")
                    if self.probmom == 0:
                        print("Nonzero probability moment is required for calculating Inverse Difference Moment")
                else:
                    crows = np.zeros(self.comat.shape)
                    ccols = np.zeros(self.comat.shape)
                    for i in range(self.comat.shape[0]):
                        crows[i, :] = i
                        ccols[:, i] = i
                    codiffs = np.abs(crows - ccols) ** self.coordmom
                    # Set minimum coordinate difference for which you allow
                    # probability to be calculated
                    codiff_eps = 0.0000001
                    # Do following so test divides don't blow up and
                    # generte a warning
                    codiffs_ok = np.where(codiffs > codiff_eps, codiffs, 1.0)
                    self.idm = np.sum(np.where(codiffs > codiff_eps, (self.comat ** self.probmom) / codiffs_ok, 0.0))

            self.val = self.idm
            self.currval = "Inverse Difference Moment"

        elif self.measure == "Correlation":
            if np.isnan(self.cor):
                import scipy.stats as ss

                crows = np.zeros(self.comat.shape)
                ccols = np.zeros(self.comat.shape)
                for i in range(self.comat.shape[0]):
                    crows[i, :] = i + 1  # need to start at 1 for Correlation calcs.
                    ccols[:, i] = i + 1
                rowmom = np.sum(crows * self.comat)
                colmom = np.sum(ccols * self.comat)
                comatvar = np.var(np.ravel(self.comat * crows))
                self.cor = np.sum((crows - rowmom) * (ccols - colmom) * self.comat) / comatvar
            self.val = self.cor
            self.currval = "Correlation"

        elif self.measure == "Probability of Run Length":
            if np.isnan(self.prl):
                if self.rllen == 0:
                    print("Nonzero run length is required for calculating Probability of Run Length")
                else:
                    colprobs = np.zeros(self.comat.shape[0])
                    for i in range(self.comat.shape[0]):
                        colprobs[i] = np.sum(self.comat[i, :])
                    self.prl = 0.0
                    for i in range(self.comat.shape[0]):
                        if colprobs[i] != 0.0:
                            self.prl += ((colprobs[i] - self.comat[i, i]) ** 2 * (
                                self.comat[i, i] ** (self.rllen - 1))) / (colprobs[i] ** self.rllen)
            self.val = self.prl
            self.currval = "Probability of Run Length"

        elif self.measure == "Epsilon Machine Run Length":
            if np.isnan(self.erl):
                if self.rllen == 0:
                    print("Nonzero run length is required for calculating Epsilon Machine Run Length")
                else:
                    if not self.emest:
                        self.est_em()
                    self.erl = 0.0
                    colprobs = np.zeros(self.emmat.shape[0])
                    for i in range(self.emmat.shape[0]):
                        colprobs[i] = np.sum(self.emmat[i, :])
                    for i in range(self.emmat.shape[0]):
                        self.erl += ((colprobs[i] - self.emmat[i, i]) ** 2 * (self.emmat[i, i] ** (self.rllen - 1))) / (
                            colprobs[i] ** self.rllen)
            self.val = self.erl
            self.currval = "Epsilon Machine Run Length"

        elif self.measure == "Run Length Asymmetry":
            if np.isnan(self.rla):
                if self.rllen == 0:
                    print("Nonzero run length is required for calculating Run Length Asymmetry")
                else:
                    colprobs = np.zeros(self.comat.shape[0])
                    rowprobs = np.zeros(self.comat.shape[0])
                    for i in range(self.comat.shape[0]):
                        colprobs[i] = np.sum(self.comat[i, :])
                        rowprobs[i] = np.sum(self.comat[:, i])
                    colval = 0.0
                    rowval = 0.0
                    for i in range(self.comat.shape[0]):
                        if colprobs[i] != 0.0:
                            colval += ((colprobs[i] - self.comat[i, i]) ** 2 * (
                                self.comat[i, i] ** (self.rllen - 1))) / (colprobs[i] ** self.rllen)
                        if rowprobs[i] != 0.0:
                            rowval += ((rowprobs[i] - self.comat[i, i]) ** 2 * (
                                self.comat[i, i] ** (self.rllen - 1))) / (rowprobs[i] ** self.rllen)
                    self.rla = np.abs(colval - rowval)
            self.val = self.rla
            self.currval = "Run Length Asymmetry"

        elif self.measure == "Homogeneity":
            if np.isnan(self.hom):
                crows = np.zeros(self.comat.shape)
                ccols = np.zeros(self.comat.shape)
                for i in range(self.comat.shape[0]):
                    crows[i, :] = i
                    ccols[:, i] = i
                self.hom = np.sum((self.comat) / (1 + np.abs(crows - ccols)))
            self.val = self.hom
            self.currval = "Homogeneity"

        elif self.measure == "Cluster Tendency":
            if np.isnan(self.clt):
                if self.clusmom == 0:
                    print("Nonzero cluster moment is required for calculating Cluster Tendency")
                else:
                    crows = np.zeros(self.comat.shape)
                    ccols = np.zeros(self.comat.shape)
                    for i in range(self.comat.shape[0]):
                        crows[i, :] = i + 1  # need to start at 1 for Correlation calcs.
                        ccols[:, i] = i + 1
                    rowmom = np.sum(crows * self.comat)
                    colmom = np.sum(ccols * self.comat)
                    self.clt = np.sum(((crows + ccols - rowmom - colmom) ** self.clusmom) * self.comat)
            self.val = self.clt
            self.currval = "Cluster Tendency"

        elif self.measure == "Multifractal Spectrum Energy Range":
            if not self.emest:  # estimate epsilon machine
                self.est_em()
            if not self.mfsest:  # estimate multifractal spectrum
                self.est_multi_frac_spec()
            if self.mfsspec.size != 0:
                self.mfu = np.max(self.mfsspec[:, 0]) - np.min(self.mfsspec[:, 0])
            else:
                self.mfu = 0.0
            self.val = self.mfu
            self.currval = "Multifractal Spectrum Energy Range"

        elif self.measure == "Multifractal Spectrum Entropy Range":
            if not self.emest:  # estimate epsilon machine
                self.est_em()
            if not self.mfsest:  # estimate multifractal spectrum
                self.est_multi_frac_spec()
            if self.mfsspec.size != 0:
                self.mfs = np.max(self.mfsspec[:, 1]) - np.min(self.mfsspec[:, 1])
            else:
                self.mfs = 0.0
            self.val = self.mfs
            self.currval = "Multifractal Spectrum Entropy Range"

        else:
            "Sorry don't know about texture measure ", self.measure

    def est_multi_frac_spec(self):
        import scipy.linalg as L

        self.mfsspec = []
        if not self.emest:
            self.est_em()
            # print "Epsilon machine",self.emmat
        if self.betas[2] == 1:
            print(
                "Only 1 step asked for re. calculating multifractal spectrum, using lower limit specified, i.e. betas[0]")
            step = 0
        else:
            step = (np.float(self.betas[1]) - np.float(self.betas[0])) / (np.float(self.betas[2]) - 1)
        for i in range(self.betas[2]):
            if i == 0:  # in case self.betas[2] = 1 => step = 0
                cb = np.float(self.betas[0])
            else:
                cb = np.float(self.betas[0] + i * step)
            if cb == 1.0:
                # in this case just do standard metric entrop calc.
                # ( e.g. see above EM Entropy calculation for comments)
                # as both u and s(u) are equal to the metric entropy
                # in this case
                [e, v] = L.eig(np.nan_to_num(self.emmat), left=True, right=False)
                maxind = np.where(np.real(e) == np.max(np.real(e)))[0][0]
                nodep = v[:, maxind] / sum(v[:, maxind])
                su = -np.sum(
                    np.transpose(nodep * np.ones(self.emmat.shape)) * (self.emmat * np.nan_to_num(np.log2(self.emmat))))
                self.mfsspec.append([su, su])
                # print i,cb,su,su
            elif cb == 0.0:
                # skip it for now - need to re-figure out beta -> 0 limit
                # need placeholder though
                splat = 0
            else:  # cb != 0,1
                # get betafied epsilon machine
                a = np.where(self.emmat > 0.0, np.exp(cb * np.log(self.emmat)), 0.0)
                # get maximum eignvalue and take the log
                # ("inv. temp." times "free energy")
                [eb, vb] = L.eig(np.nan_to_num(a), left=False, right=True)
                maxind = np.where(np.real(eb) == np.max(np.real(eb)))[0][0]
                fe = np.log2(np.real(eb[maxind]))
                # stochastisize betafied epsilon machine
                b = np.dot((1 / eb[maxind]) * np.diag((1 / vb[:, maxind])), np.dot(a, (np.diag(vb[:, maxind]))))
                # get metric entropy of stochasticized machine
                # - same as "entropy" s(u) as func. of "energy" u
                # - i.e. multifractal spectrum is analogue of
                # - thermodynamic spectrum s(u) vs. u
                [e, v] = L.eig(np.nan_to_num(b), left=True, right=False)
                maxind = np.where(np.real(e) == np.max(np.real(e)))[0][0]
                nodep = v[:, maxind] / sum(v[:, maxind])
                # make sure they're real - sometimes linalg spits
                # out complex values with 0 imaginary part
                su = abs(-np.sum(np.transpose(nodep * np.ones(b.shape)) * (b * np.nan_to_num(np.log2(b)))))
                # then get energy - i.e. "temperature" normalized
                # difference between "entropy" and "free energy"
                u = abs((su - fe) / cb)
                self.mfsspec.append([u, su])
                # print i,cb,u,su

        self.mfsspec = np.array(np.real(self.mfsspec))
        # waste the nan's - e.g. when the range wasn't quite right
        self.mfsspec = np.delete(self.mfsspec, np.where(np.isnan(self.mfsspec))[0], 0)
        self.mfsest = True

    def est_em(self):
        """
        Estimates an epsilon machine

        No arguments, expects cooccurence matrix, with # rows =
        # columns to be in self.comat
        
        """
        import scipy.stats as ss

        # Make conditional distribution matrix, i.e. epsilon machine
        # (row probabilities)
        self.condo = np.transpose(np.transpose(self.comat) / np.sum(self.comat, axis=1))
        # the following is n^2 - need to figure a better way
        found = []
        self.emclasses = np.zeros(self.condo.shape[0], int)
        onclass = 0
        for i in range(self.condo.shape[0]):
            if i not in found:
                found.append(i)
                # if it's dinky just tack it on to class 0
                # code below will just combine it in
                if np.sum(self.condo[i, :]) < 0.00000001:
                    self.emclasses[i] = 0
                else:
                    # it's a new one
                    self.emclasses[i] = onclass
                    for j in range(i + 1, self.condo.shape[0]):
                        if j not in found:
                            # check if rows ("distributions") are "close"
                            # i.e. p value in chi squred test < self.clusp
                            tester = ss.chisquare(self.totcount * self.condo[i, :], self.totcount * self.condo[j, :])[1]
                            if tester < self.clusp:  # they're different
                                found.append(j)
                                onclass += 1
                                self.emclasses[j] = onclass
                            else:  # they're not
                                found.append(j)
                                self.emclasses[j] = onclass

        self.emclus = onclass + 1

        for i in range(self.emclus):
            rowinds = tuple(np.where(self.emclasses == i)[0])
            if i == 0:
                a = np.add.reduce(self.comat[rowinds, :], axis=0)
            else:
                a = np.vstack((a, np.add.reduce(self.comat[rowinds, :], axis=0)))
        # If initial/final states are the same need to also combine columns
        if self.samelev:
            if len(a.shape) > 1:
                for i in range(self.emclus):
                    colinds = tuple(np.where(self.emclasses == i)[0])
                    # seems like it has to be done rowise first...
                    if i == 0:
                        b = np.add.reduce(a[:, colinds], axis=1)
                    else:
                        b = np.vstack((b, np.add.reduce(a[:, colinds], axis=1)))
                        # ... then transposed
            else:
                for i in range(a.shape[0]):
                    if i == 0:
                        b = a
                    else:
                        b = np.vstack([b, a])
            self.emmat = np.transpose(b)
        else:  # do it all over again for columns
            found = []
            self.emclasses = np.zeros(self.condo.shape[1], int)
            onclass = 0
            for i in range(self.condo.shape[1]):
                if i not in found:
                    found.append(i)
                    # if it's dinky just tack it on to class 0
                    # code below will just combine it in
                    if np.sum(self.condo[:, i]) < 0.00000001:
                        self.emclasses[i] = 0
                    else:
                        # it's a new one
                        self.emclasses[i] = onclass
                        for j in range(self.condo.shape[1], i + 1):
                            if j not in found:
                                # check if rows ("distributions") are "close"
                                # i.e. p value in chi squred test < self.clusp
                                tester = \
                                    ss.chisquare(self.totcount * self.condo[:, i], self.totcount * self.condo[:, j])[1]
                                if tester < self.clusp:  # they're different
                                    found.append(j)
                                    onclass += 1
                                    self.emclasses[j] = onclass
                                else:  # they're not
                                    found.append(j)
                                    self.emclasses[j] = onclass

            self.emclus = onclass + 1

            for i in range(self.emclus):
                colinds = tuple(np.where(self.emclasses == i)[1])
                if i == 0:
                    a = np.add.reduce(self.comat[:, colinds], axis=1)
                else:
                    a = np.vstack((a, np.add.reduce(self.comat[:, colinds], axis=1)))
            self.emmat = np.transpose(a)
            # and finally turned into a Markov matrix...
        self.emmat = np.transpose(np.transpose(self.emmat) / np.sum(self.emmat, axis=1))
        self.emest = True
        
