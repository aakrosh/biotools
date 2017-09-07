#!/usr/bin/env python

class Node:
    def __init__ (self, key):
        self.id     = key
        self.parent = None
        self.left   = None
        self.right  = None
        self.lnum   = 0
        self.rnum   = 0

    def __str__ (self):
        string = "%s (%d, %d) :" % (str(self.id), self.lnum, self.rnum)
        if self.parent:
            string += " Parent %s:" % str(self.parent.id)
        if self.left:
            string += " Left %s:" % str(self.left.id)
        if self.right:
            string += " Right %s:" % str(self.right.id)
        return string

class IntervalTree:
    def __init__ (self):
        self.root = None

    def RotateRight (self, n):
#        print "in rotate right for %s" % str(n.id)
        is_root = False
        x = n.left

        x.parent = n.parent
        if n.parent: 
            if n.parent.left == n:
                n.parent.left = x
            else:
                n.parent.right = x
        else:
            # n is the root
            is_root = True

        # changes to n
        n.left = x.right
        if x.right:
            x.right.parent = n
        n.parent = x
        x.right = n
        n.lnum = x.rnum
        
        # changes to x
        x.right  = n
        x.rnum = n.lnum + n.rnum + 1

        if is_root:
            self.root = x

    def RotateLeft (self, n):
#        print "in rotate left for %s" % str(n.id)
        is_root = False
        y = n.right

        y.parent = n.parent
        if n.parent:
            if n.parent.left == n:
                n.parent.left = y
            else:
                n.parent.right = y
        else:
            # n is the root
            is_root = True

        # changes to n
        n.right = y.left
        if y.left:
            y.left.parent = n
        n.parent = y
        y.left = n
        n.rnum = y.lnum

        # changes to y
        y.left = n
        y.lnum = n.lnum + n.rnum + 1

        if is_root:
            self.root = y
   
    def Insert (self, k):
        prevNode = None
        currNode = self.root

        while currNode:
            prevNode = currNode
            if k < currNode.id:
                currNode.lnum += 1
                currNode = currNode.left
            else:
                currNode.rnum += 1
                currNode = currNode.right

        # Insert the node here
        if prevNode == None:
            # this is the first node, so we just Insert and quit 
            self.root = Node (k)       
#            print "Added root %s" % str(k)
        else:
            # Insert this as a child to this node
            node = Node (k)
            if k < prevNode.id:
                prevNode.left = node
#                print "Added %s to left of %s" % (str(k), str(prevNode.id))
            else:
                prevNode.right = node
#                print "Added %s to right of %s" % (str(k), str(prevNode.id))
            node.parent = prevNode

        # now make sure that all the ancestors are consistent with the rules
        # of an AVL tree
        node = prevNode
    
        while node:
            balanceFactor = node.lnum - node.rnum
            if balanceFactor == 2:
#                self.Print ()
#                print "-------------"
                p = node.left
                if p.lnum - p.rnum == -1:
                    self.RotateLeft (p)
#                    self.Print ()
#                    print "<<<<<<<<<<<<<<"
                self.RotateRight (node)
#                self.Print ()
#                print ">>>>>>>>>>>>>>"
                break
            elif balanceFactor == -2:
#                self.Print ()
#                print "-------------"
                p = node.right
                if p.lnum - p.rnum == 1:
                    self.RotateRight (p)
#                    self.Print ()
#                    print ">>>>>>>>>>>>>>"
                self.RotateLeft (node)
#                self.Print ()
#                print "<<<<<<<<<<<<<<"
                break
            else:
                node = node.parent

    def Print (self):
        queue = []
        indx  = 0
        queue.append ((indx, self.root))

        while queue:
            depth, node = queue.pop(0)
            #print node.id, depth, node.lnum, node.rnum
            print node
            if node.left: queue.append ((depth + 1,node.left))
            if node.right: queue.append ((depth + 1, node.right))

    def Search (self, k):
        node = self.root

        while node:
            if k < node.id:
                node = node.left
            elif k > node.id:
                node = node.right
            else:
                return node            

        return None   

    def Check (self):
        queue = []
        indx  = 0
        queue.append (self.root)

        while queue:
            node = queue.pop(0)
            if node.parent:
                assert node.parent.left == node or node.parent.right == node
            if node.left:
                assert node.left.parent == node
            if node.right:
                assert node.right.parent == node
            if node.left: queue.append (node.left)
            if node.right: queue.append (node.right)

           

if __name__ == "__main__":
    tree = IntervalTree ()

    tree.Insert (5)
    tree.Check ()
    tree.Insert (3)
    tree.Check ()
    tree.Insert (4)
    tree.Check ()
    tree.Insert (2)
    tree.Check ()
    tree.Insert (6)
    tree.Check ()
    tree.Insert (7)
    tree.Check ()
    tree.Insert (8)
    tree.Check ()
    tree.Insert (9)
    tree.Check ()

    tree.Print ()

    print tree.Search (1)
    print tree.Search (2)
