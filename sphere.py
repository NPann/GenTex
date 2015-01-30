# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 15:35:04 2014

@author: nicolaspannetier
"""


def circle_in(xm, ym, r):
    circ = []
    x = -r
    y = 0
    err = 2 - 2 * r
    # circ.append([xm,ym]) # not required for cooccurence matrix building
    while x < 0:  # do octants
        for i in range(-1, x - 1, -1):
            circ.append([xm - i, ym + y])
            circ.append([xm - y, ym - i])
            circ.append([xm + i, ym - y])
            circ.append([xm + y, ym + i])
        r = err
        if r > x:
            x += 1
            err += x * 2 + 1  # e_xy+e_x > 0
        if r <= y:
            y += 1
            err += y * 2 + 1  # e_xy+e_y < 0
    return circ


def bres_circle(xm, ym, r):
    # This is a version of Bresenhams circle algorithm via:
    # http://free.pages.at/easyfilter/bresenham.html

    circ = []
    x = -r
    y = 0
    err = 2 - 2 * r
    while x < 0:  # do octants
        circ.append([xm - x, ym + y])
        circ.append([xm - y, ym - x])
        circ.append([xm + x, ym - y])
        circ.append([xm + y, ym + x])
        r = err
        if r > x:
            x += 1
            err += x * 2 + 1  # e_xy+e_x > 0
        if r <= y:
            y += 1
            err += y * 2 + 1  # e_xy+e_y < 0
    return circ


def rem_dup(mylist):
    if mylist:
        mylist.sort()
        last = mylist[-1]
        for i in range(len(mylist) - 2, -1, -1):
            if last == mylist[i]:
                del mylist[i]
            else:
                last = mylist[i]
    return mylist


def get_radii(r):
    zero_circle = bres_circle(0, 0, r)
    radii = []
    if r > 1:
        for step in range(r + 1):
            for zc in zero_circle:
                if zc[0] == step and zc[1] > 0:
                    radii.append(zc[1])
    else:
        radii = [1, 0]
    return radii


def sphere_shell(xm, ym, zm, r):
    # This builds a sperical shell layer by layer using
    # the version of Bresenhams circle algorithm at:
    # http://free.pages.at/easyfilter/bresenham.html
    shell = []
    radii = get_radii(r)
    for z in range(len(radii) - 1):
        circ = bres_circle(xm, ym, radii[z])
        for ci in circ:
            withzp = ci + [z + zm]
            shell.append(withzp)
            if z > 0:
                withzm = ci + [zm - z]
                shell.append(withzm)
    for x in range(-radii[r], radii[r] + 1):  # do "caps"
        for y in range(-radii[r], radii[r] + 1):
            shell.append([x + xm, y + ym, r + zm])
            shell.append([x + xm, y + ym, zm - r])
    return shell


def sphere(xm, ym, zm, r):
    sphere = []
    r2 = r * r
    for x in range(r):
        for y in range(r):
            for z in range(r):
                if x > 0:
                    x2 = x * x
                else:
                    x2 = 0
                if y > 0:
                    y2 = y * y
                else:
                    y2 = 0
                if z > 0:
                    z2 = z * z
                else:
                    z2 = 0
                if x2 + y2 + z2 < r2:
                    sphere.append([x + xm, y + ym, z + zm])
                    if x > 0:
                        sphere.append([-x + xm, y + ym, z + zm])
                    if y > 0:
                        sphere.append([x + xm, -y + ym, z + zm])
                        if x > 0:
                            sphere.append([-x + xm, -y + ym, z + zm])
                    if z > 0:
                        sphere.append([x + xm, y + ym, -z + zm])
                        if x > 0:
                            sphere.append([-x + xm, y + ym, -z + zm])
                        if y > 0:
                            sphere.append([x + xm, -y + ym, -z + zm])
                            if x > 0:
                                sphere.append([-x + xm, -y + ym, -z + zm])
    return sphere

    ## circ = bres_circle(0,0,1)
    ## print circ
    ## shell = sphere_shell(0,0,0,1)
    ## print shell,len(shell)

    ## sph = sphere(0,0,0,2)
    ## print sph
    ## print len(sph)
    ## sph2 = rem_dup(sph)
    ## print sph2
    ## print len(sph2)