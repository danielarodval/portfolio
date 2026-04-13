// Travis Meade
// Written in Jan 2018

// Illustrates Red-Black Tree Insertion and Deletion
// Outputs .pngs to clearly illustrate what occurs at each step
// in a random simulation of inserting (then deleting) 20 nodes.

import java.awt.image.BufferedImage;
import java.io.File;
import java.util.Arrays;

import javax.imageio.ImageIO;

public class TreePretty {

	public static final boolean DEBUG = false;

	public static void main(String[] Args) throws Exception {
		Node root = null;
		int SIZE = 20;

		// Initialize arrays
		int[] vs = new int[SIZE];
		boolean[] used = new boolean[SIZE];
		int[] vs2 = new int[SIZE];
		boolean[] used2 = new boolean[SIZE];

		// Choose a random order for insertion
		for (int i = 0; i < SIZE; i++) {
			int c = (int) (Math.random() * SIZE);
			while (used[c])
				c = (int) (Math.random() * SIZE);
			used[c] = true;
			vs[i] = c;
			
			c = (int) (Math.random() * SIZE);
			while (used2[c])
				c = (int) (Math.random() * SIZE);
			used2[c] = true;
			vs2[i] = c;
		}

		// Insert the values
		for (int i = 0; i < SIZE; i++) {
			Node n = new Node(vs[i]);
			System.out.println("Inserting " + n.getValue());
			root = insert(root, n);
			printViolations(root);
			drawTree("tree_" + (++count) + ".png", root);
			System.out.flush();
			System.err.flush();
		}
		
		// Delete nodes
		for (int i = 0; i < SIZE; i++) {
			System.out.println("Deleting " + vs2[i]);
			root = deleteNode(vs2[i], root);
			printViolations(root);
			drawTree("tree_" + (++count) + ".png", root);
			System.out.flush();
			System.err.flush();
		}
	}

	// Function that checks that there has been no condition violations of
	// the R-B tree
	public static void printViolations(Node n) throws Exception {

		if (n == null) {
			return;
		}
	
		// Check sorted order
		if (printCheckOrder(n, 0)) {
			System.out.println();
			System.out.flush();
			System.err.println("There was an order violation");
			System.err.flush();
		} else {
			System.out.println();
			System.out.flush();
		}

		// Check Condition 1 all nodes are black or red
		if (!condition1(n)) {
			System.err.println("Condition 1 violation: a node does not have a red or black color");
			System.err.flush();
		}

		// Check Condition 2 the root is black
		if (n != null && n.getColor() == RED) {
			System.err.println("Condition 2 violation: Root is red");
			System.err.flush();
		}

		// Condition 3 holds since we assume null is black

		// Check Condition 4
		if (!condition4(n)) {
			System.err.println("Condition 4 violation: a red node has a red child");
			System.err.flush();
		}

		// Check Condition 5
		int min = minPath(n);
		int max = maxPath(n);
		if (min != max) {
			System.err.println("Condition 5 violation: Differing lengths of black noded paths");
			System.err.flush();
		}
	}

	// Method for drawing the tree which contains the given node to a
	// specified file name
	public static void drawTree(String name, Node n) throws Exception {

		if (n == null)
			return;
	
		// Find the root of the tree
		while (n.getParent() != null)
			n = n.getParent();

		// Get the size of the tree
		int size = getSize(n);

		// Initialize the height of the tree
		int height = 0;

		// Initialize some stats of the tree
		depths = new int[size];
		vals = new int[size];
		colors = new int[size];
		parents = new int[size];
		Arrays.fill(parents, -1);

		// Get the depths of each node
		getDepth(n, 0, 0);

		// Use the depths to compute the heights
		for (int i = 0; i < size; i++)
			if (height < depths[i] + 1)
				height = depths[i] + 1;

		// Get the colors of the nodes
		getColors(n, 0);

		// Get the parents of the nodes
		getParents(n, 0);

		// Compute the width and height of the image
		int height2 = height * (buffer + diameter) + buffer;
		int width2 = (buffer + diameter) * size + buffer;

		// Make the image
		BufferedImage bi = new BufferedImage(width2, height2, BufferedImage.TYPE_INT_RGB);

		// Make the background white
		for (int i = 0; i < width2; i++)
			for (int j = 0; j < height2; j++)
				bi.setRGB(i, j, white);

		// Draw the lines for the nodes
		for (int i = 0; i < size; i++)
			if (parents[i] != -1)
				drawLine(bi, i, depths[i], parents[i], depths[parents[i]]);

		// Draw the nodes
		for (int i = 0; i < size; i++) {
			drawCircle(bi, i, depths[i], colors[i]);
			drawNumber(bi, i, depths[i], colors[i], vals[i]);
		}

		// Write the image to a file with the appropriate name
		ImageIO.write(bi, "PNG", new File(name));
	}

	// Some colors in RGB hex
	public static int white = 0xFFFFFF;
	public static int red = 0xFF0000;
	public static int black = 0x000000;
	public static int blue = 0x0000FF;

	// The number of times we step while drawing lines
	public static int times = 1000;

	// Method for drawing the lines
	public static void drawLine(BufferedImage bi, int x1, int y1, int x2, int y2) {
		int xx1 = (buffer + diameter) * x1 + buffer + diameter / 2;
		int yy1 = (buffer + diameter) * y1 + buffer + diameter / 2;
		int xx2 = (buffer + diameter) * x2 + buffer + diameter / 2;
		int yy2 = (buffer + diameter) * y2 + buffer + diameter / 2;
		for (int i = -1; i < 2; i++)
			for (int j = -1; j < 2; j++) {
				for (int k = 0; k < times; k++) {
					int xx = (k * xx1 + (times - k) * xx2) / times;
					int yy = (k * yy1 + (times - k) * yy2) / times;
					bi.setRGB(xx, yy, blue);
				}
			}

	}

	// Method for drawing circles
	public static void drawCircle(BufferedImage bi, int x, int y, int color) {
		int xx = (buffer + diameter) * x + buffer + diameter / 2;
		int yy = (buffer + diameter) * y + buffer + diameter / 2;
		for (int i = xx - diameter / 2; i < xx + diameter / 2; i++) {
			for (int j = yy - diameter / 2; j < yy + diameter / 2; j++) {
				int dx = xx - i;
				int dy = yy - j;
				if (dx * dx + dy * dy <= diameter * diameter / 4) {
					bi.setRGB(i, j, color == RED ? red : black);
				}
			}
		}
	}

	// Information for drawing seven segment numbers
	public static final int segment_length = 5;
	public static final int segment_width = 2;
	public static final int digit_buffer = 2;
	public static final int digit_height = 3 + segment_length * 2;
	public static final int digit_width = 2 + segment_length;

	// Method for drawing a value
	public static void drawNumber(BufferedImage bi, int x, int y, int color, int val) {
		int len = Integer.toString(val).length() * (digit_buffer + digit_width) + digit_buffer;
		int hei = digit_height + 2 * digit_buffer;
		int xx = (buffer + diameter) * x + buffer + diameter / 2 - len / 2;
		int yy = (buffer + diameter) * y + buffer + diameter / 2 - hei / 2;
		for (int i = 0; i < Integer.toString(val).length(); i++) {
			drawDigit(bi, xx + digit_buffer, yy + digit_buffer, color, Integer.toString(val).charAt(i) - '0');
			xx += digit_buffer + digit_width;
		}
	}

	// Method for drawing digit
	public static void drawDigit(BufferedImage bi, int x, int y, int color, int c) {
		for (int i = 0; i < digit_height; i++) {
			for (int j = 0; j < digit_width; j++) {
				if (i < segment_width && (digitImage[c][0]))
					bi.setRGB(x + j, y + i, (color == RED) ? black : white);
				if ((i == (digit_height) / 2 || i == digit_height / 2 + 1) && (digitImage[c][3])) {
					bi.setRGB(x + j, y + i, (color == RED) ? black : white);
				}
				if (i >= digit_height - segment_width && (digitImage[c][6])) {
					bi.setRGB(x + j, y + i, (color == RED) ? black : white);
				}
				if (i >= (digit_height / 2) && j < segment_width && (digitImage[c][4])) {
					bi.setRGB(x + j, y + i, (color == RED) ? black : white);
				}
				if (i >= (digit_height / 2) && j >= digit_width - segment_width && (digitImage[c][5])) {
					bi.setRGB(x + j, y + i, (color == RED) ? black : white);
				}
				if (i <= (digit_height / 2) && j < segment_width && (digitImage[c][1])) {
					bi.setRGB(x + j, y + i, (color == RED) ? black : white);
				}
				if (i <= (digit_height / 2) && j >= digit_width - segment_width && (digitImage[c][2])) {
					bi.setRGB(x + j, y + i, (color == RED) ? black : white);
				}
			}
		}
	}

	// More seven segment digit information
	// 1
	// 2 3
	// 4
	// 5 6
	// 7
	public static boolean[][] digitImage = { { true, true, true, false, true, true, true },
			{ false, false, true, false, false, true, false }, { true, false, true, true, true, false, true },
			{ true, false, true, true, false, true, true }, { false, true, true, true, false, true, false },
			{ true, true, false, true, false, true, true }, { true, true, false, true, true, true, true },
			{ true, false, true, false, false, true, false }, { true, true, true, true, true, true, true },
			{ true, true, true, true, false, true, true } };

	// Drawing parameters that should probably be closer to the top of
	// the file
	public static int buffer = 7;
	public static int diameter = 40;

	// Data structures for drawing the tree
	public static int[] depths;
	public static int[] vals;
	public static int[] colors;
	public static int[] parents;

	// Method for building depth in an array
	public static void getDepth(Node n, int curDepth, int index) {
		if (n == null)
			return;
		int loc = index + getSize(n.getLeft());
		depths[loc] = curDepth;
		vals[loc] = n.getValue();
		getDepth(n.getLeft(), curDepth + 1, index);
		getDepth(n.getRight(), curDepth + 1, loc + 1);
	}

	// Method for build the colors as an array
	public static void getColors(Node n, int index) {
		if (n == null)
			return;
		int loc = index + getSize(n.getLeft());
		colors[loc] = n.getColor();
		getColors(n.getLeft(), index);
		getColors(n.getRight(), loc + 1);
	}

	// Method for getting parent information
	public static void getParents(Node n, int index) {
		if (n == null)
			return;

		int loc = index + getSize(n.getLeft());

		if (n.getLeft() != null) {
			int nindex = index + getSize(n.getLeft().getLeft());
			parents[nindex] = loc;
		}

		if (n.getRight() != null) {
			int nindex = 1 + loc + getSize(n.getRight().getLeft());
			parents[nindex] = loc;
		}
		getParents(n.getLeft(), index);
		getParents(n.getRight(), loc + 1);
	}

	// Method for getting the size of a tree from some rooted node
	public static int getSize(Node n) {
		if (n == null)
			return 0;
		return 1 + getSize(n.getLeft()) + getSize(n.getRight());
	}

	// Method to check for condition 1 All nodes are either black or red
	public static boolean condition1(Node n) {
		if (n == null)
			return true;
		if (n.getColor() != RED && n.getColor() != BLACK)
			return false;
		return condition1(n.getLeft()) && condition1(n.getRight());
	}

	// Method for checking condition 4 all red nodes must have black children
	public static boolean condition4(Node n) {
		// Check if leaf
		if (n == null)
			return true;

		// Current node
		if (n.getColor() == RED && n.getRight() != null && n.getRight().getColor() == RED)
			return false;
		if (n.getColor() == RED && n.getLeft() != null && n.getLeft().getColor() == RED)
			return false;

		// Check the left and right tree recursively
		if (!condition4(n.getLeft()))
			return false;
		if (!condition4(n.getRight()))
			return false;

		// No violations found
		return true;
	}

	// Method for computing the minimum black path in a sub-tree from a
	// given root
	public static int minPath(Node n) {
		if (n == null)
			return 1;
		int ret = minPath(n.getLeft());
		int tmp = minPath(n.getRight());
		if (ret > tmp)
			ret = tmp;
		if (n.getColor() == BLACK)
			ret++;
		return ret;
	}

	// Method for computing the maximum black node path in a sub-tree from a
	// given root
	public static int maxPath(Node n) {
		if (n == null)
			return 1;
		int ret = maxPath(n.getLeft());
		int tmp = maxPath(n.getRight());
		if (ret < tmp)
			ret = tmp;
		if (n.getColor() == BLACK)
			ret++;
		return ret;
	}

	// Method for verifying the Binary searchable property
	public static boolean printCheckOrder(Node n, int depth) {
		boolean ret = false;

		// Print left sub tree
		if (n.getLeft() != null) {
			printCheckOrder(n.getLeft(), depth + 1);
			if (n.getLeft().getValue() > n.getValue())
				ret = true;
		}

		// Print current value
		if (DEBUG)
			System.out.print(n.getValue() + " " + (n.getColor() == RED ? "RED" : "BLACK") + " " + depth + " :: ");

		// Print right subtree
		if (n.getRight() != null) {
			printCheckOrder(n.getRight(), depth + 1);
			if (n.getRight().getValue() < n.getValue())
				ret = true;
		}

		return ret;
	}

	public static int RED = 0;
	public static int BLACK = 1;

	public static int count = 0;
	public static int count2 = 0;

	public static Node insert(Node root, Node newNode) throws Exception {

		// Insert the new node
		insertRecursively(root, newNode);
		count2 = 0;
		// drawTree(newNode, "tree_" + count + "_" + (count2++) + ".png");

		// Fix the tree if the new node broke any properties
		insertRepairTree(newNode);

		// Find the root
		root = newNode;
		while (root.getParent() != null) {
			root = root.getParent();
		}

		// Return the "new" root of the tree
		return root;
	}

	public static void insertRecursively(Node root, Node newNode) {

		// check if the root is not null
		if (root != null) {
			if (root.value > newNode.value) {
				// In left tree
				if (root.left == null) {
					root.left = newNode;
				} else {
					insertRecursively(root.left, newNode);
					return;
				}
			} else {
				// In right tree
				if (root.right == null) {
					root.right = newNode;
				} else {
					insertRecursively(root.right, newNode);
					return;
				}
			}
		}

		// We found a spot in our tree so update the node's parameters
		newNode.parent = root;
		newNode.left = null;
		newNode.right = null;
		newNode.color = RED;
	}

	public static void insertRepairTree(Node newNode) throws Exception {
		drawTree("tree_" + count + "_" + (count2++) + ".png", newNode);

		if (newNode.getParent() == null) {
			// Node was the root
			insertRepairCase1(newNode);
		} else if (newNode.getParent().getColor() == BLACK) {
			// Node has a black parent so we can set our color does not matter
			insertRepairCase2(newNode);
		} else if (newNode.uncle() != null && newNode.uncle().getColor() == RED) {
			// Node has a red parent and the uncle is red
			insertRepairCase3(newNode);
		} else {
			// Node has a red parent and the uncle is black
			insertRepairCase4(newNode);
		}
	}

	public static void insertRepairCase1(Node newNode) {
		// Don't violate Condition 2
		if (newNode.getParent() == null)
			newNode.setColor(BLACK);
	}

	public static void insertRepairCase2(Node newNode) {
		// Do nothing
	}

	public static void insertRepairCase3(Node newNode) throws Exception {
		// Since uncle was red we can recolor and not violate anything
		newNode.getParent().setColor(BLACK);
		newNode.uncle().setColor(BLACK);
		newNode.grandparent().setColor(RED);

		// We might have broken grandparent (e.g. his parent was red)
		insertRepairTree(newNode.grandparent());
	}

	public static void insertRepairCase4(Node newNode) throws Exception {
		Node grand = newNode.grandparent();
		Node parent = newNode.getParent();

		// We don't have the nodes aligned
		if (newNode == grand.leftRight()) {
			parent.rotateLeft();
			insertRepairTree(parent);
			return;
		} else if (newNode == grand.rightLeft()) {
			parent.rotateRight();
			insertRepairTree(parent);
			return;
		}

		// Rotate the nodes and update the parents and grandparents color
		if (newNode == parent.getLeft()) {
			grand.rotateRight();
		} else {
			grand.rotateLeft();
		}
		parent.setColor(BLACK);
		grand.setColor(RED);
	}

	// Method for deleting a node with a given value from a tree with
	// a given root
	public static Node deleteNode(int value, Node root) throws Exception {
		// Find the node we actually want to delete
		Node delNode = findNode(value, root);

		// Check the node exists
		if (delNode == null) {
			return findRoot(root);
		}

		// Check if we are not in a simple case
		if (delNode.getRight() != null && delNode.getLeft() != null) {
			// Reduce the problem to a simpler problem by finding the least
			// valued node strictly greater than our node
			Node swapNode = delNode.upper();

			// Swap the nodes
			swapNode.swap(delNode);
		}

		// Find a child
		Node child = delNode.getRight();

		// Try to find a non-null child
		if (child == null) {
			child = delNode.getLeft();
		}

		// Check if both the current node and child have a red color
		if (child != null && child.getColor() == RED && delNode.getColor() == RED) {

			// This should not have happened
			System.err.println("ERROR: Red node with red child");

			// "That tree was garbage anyways"
			return null;
		}

		// Check if one of the nodes is red
		if (delNode.getColor() == RED || (child != null && child.getColor() == RED)) {
			// Find the parent
			Node parent = delNode.getParent();

			// Update the parents children
			if (parent != null)
				if (parent.getLeft() == delNode)
					parent.setLeft(child);
				else
					parent.setRight(child);

			// Update the childs parent
			if (child != null)
				child.setParent(parent);

			// Make the child black
			if (child != null)
				child.setColor(BLACK);

			// Find the root and return
			root = findRoot(child);

			// Child might have been null so check the parent as well
			if (root == null)
				root = findRoot(parent);

			// Return the root (potentially null if this was last node)
			return root;
		}

		// --------------------------------------------------------------------
		// We entered the double black case this is much more difficult to
		// handle. I will not test on this
		// --------------------------------------------------------------------
		// Find the parent
		Node parent = delNode.getParent();

		// Update the parents children
		if (parent != null)
			if (parent.getLeft() == delNode)
				parent.setLeft(child);
			else
				parent.setRight(child);

		// Update the childs parent
		if (child != null)
			child.setParent(parent);

		// Make the child black
		if (child != null)
			child.setColor(BLACK);
		handleDoubleBlack(child, parent);
		
		// Find the root and return
		root = findRoot(child);

		// Child might have been null so check the parent as well
		if (root == null)
			root = findRoot(parent);

		// Return the root (potentially null if this was last node)
		return root;
	}

	public static void handleDoubleBlack(Node child, Node parent) throws Exception {
		
		
		// Case 1 the child is the root (we don't need to do anything)
		if (parent == null){
			if (DEBUG)
				System.out.println("In Case 1 with parent \"null\""+" @ node " + ((child != null) ? child : "null"));
		
			return;
		}

		drawTree("tree_" + count + "_" + (count2++) + ".png", findRoot(parent));
		
		
		// Note since we have a parent and we were in double black node case
		// we have a non-leaf sibling as well
		
		// Get the sibling (We have a parent so I can access it)
		Node sib = parent.getLeft();
		if (sib == child) {
			// Oops I confused the child with its sibling... Parents do this
			// all the time
			sib = parent.getRight();
		}

		// Case 2 the sibling is red
		if (sib.getColor() == RED) {
			if (DEBUG)
				System.out.println("In Case 2 with parent " + parent+" @ node " + ((child != null) ? child : "null"));
			
			// Rotate parent accordingly
			if (sib == parent.getLeft()) {
				parent.rotateRight();
			} else {
				parent.rotateLeft();
			}
			
			// Adjust colors
			sib.setColor(BLACK);
			parent.setColor(RED);
			
			// Parent is still parent and child is still child...
			handleDoubleBlack(child, parent);
			return;
		}
		
		// Now we must have a black sibling.
		// Additionally our sibling should not be null, since we are still a
		// double black node
		
		// Case 3 sibling has two black children and parent is black
		if (parent.getColor() == BLACK && sib.getLeftColor() == BLACK && sib.getRightColor() == BLACK) {
			if (DEBUG)
				System.out.println("In Case 3 with parent " + parent + " @ node " + ((child != null) ? child : "null") + " : with sib " + ((sib != null) ? sib : "null"));
			
			// Make our sibling red and force the parent to be the double 
			// black node
			sib.setColor(RED);
			handleDoubleBlack(parent, parent.getParent());
			return;
		}
		
		// Case 4 parent is red and sibling has two black children
		if (parent.getColor() == RED && sib.getLeftColor() == BLACK && sib.getRightColor() == BLACK) {
			if (DEBUG)
				System.out.println("In Case 4 with parent " + parent+" @ node " + ((child != null) ? child : "null"));
		
			// Change the parents color to black this fixes the number of
			// paths in the current nodes path and does not change the paths
			// in the siblings paths
			parent.setColor(BLACK);
			sib.setColor(RED);
			return;
		}
		
		// Case 5 our sibling has a black child on the far side (e.g. our parents left.left or right.right)
		if ((sib == parent.getLeft() && sib.getLeftColor() == BLACK) || (sib == parent.getRight() && sib.getRightColor() == BLACK)) {
			
			if (DEBUG)
				System.out.println("In Case 5 with parent " + parent+" @ node " + ((child != null) ? child : "null"));
		
			
			// Rotate the sibling to the direction 
			if (sib == parent.getLeft())
				sib.rotateLeft();
			else
				sib.rotateRight();
			
			// Swap the colors after the rotation to prevent a new 
			// "double black node"
			sib.setColor(RED);
			sib.getParent().setColor(BLACK);
			
			// We should be able to do case 6 now, but as sanity check the
			// other cases
			handleDoubleBlack(child, parent);
			return;
		}
		
		if (DEBUG)
			System.out.println("In Case 6 with parent " + parent +" @ node " + ((child != null) ? child : "null"));
		
		// Well this is not as bad... we don't actually know the color of the
		// parent so store that for now along with the color of the inner 
		// nephew (niece?) child
		Node outerNephew = sib.getRight();
		int parentColor = parent.getColor();
		int nephewColor = sib.getLeftColor();
		
		// Check if we mixed up our nephews
		if (sib == parent.getLeft()){
			nephewColor = sib.getRightColor();
			outerNephew = sib.getLeft();
		}
		
		// Rotate parent the direction of ourselves
		if (sib == parent.getLeft()) {
			parent.rotateRight();
		} else {
			parent.rotateLeft();
		}
		
		// nephew keeps his color
		// Do nothing
		// parent becomes black
		parent.setColor(BLACK);
		// Sibling becomes old parent's color
		sib.setColor(parentColor);
		// Color the outer sibling left since his path count dropped
		outerNephew.setColor(BLACK);
	}

	public static Node findRoot(Node curNode) {
		// Check if we do not have a tree
		if (curNode == null)
			return null;

		// Check if we still have a parent
		while (curNode.getParent() != null)
			curNode = curNode.getParent();

		// Return the found node
		return curNode;
	}

	// Method for finding a node with a given value from a tree with
	// a given root
	public static Node findNode(int value, Node root) {
		// Check if there is no possible node
		if (root == null)
			return root;

		// Check if we are at the node
		if (root.value == value)
			return root;

		// Check if the root value is larger: go left!
		if (root.getValue() > value)
			return findNode(value, root.getLeft());

		// The root value is strictly smaller: go right!
		return findNode(value, root.getRight());
	}

	// The node class in all its glory
	public static class Node {
		private int value;
		private int color;
		private Node left, right, parent;

		Node(int i) {
			value = i;
			color = RED;
			left = null;
			right = null;
			parent = null;
		}

		// Some setter functions
		void setParent(Node n) {
			parent = n;
		}

		void setLeft(Node n) {
			left = n;
		}

		void setRight(Node n) {
			right = n;
		}

		void setColor(int c) {
			color = c;
		}

		// Some getter functions
		int getValue() {
			return value;
		}

		int getColor() {
			return color;
		}

		Node getLeft() {
			return left;
		}

		Node getRight() {
			return right;
		}

		Node getParent() {
			return parent;
		}
		
		int getLeftColor() {
			if (left == null)
				return BLACK;
			return left.color;
		}
		
		int getRightColor() {
			if (right == null)
				return BLACK;
			return right.color;
		}

		Node grandparent() {
			if (parent != null)
				return parent.getParent();
			return null;
		}

		Node sibling() {
			if (parent != null) {
				if (parent.left == this) {
					return parent.right;
				}
				return parent.left;
			}
			return null;
		}

		Node uncle() {
			if (parent != null) {
				return parent.sibling();
			}
			return null;
		}

		void rotateLeft() throws Exception {
			if (right == null) {
				System.err.println("Tried to rotate right into a null");
				throw new Exception("BLAH");
			}
			Node newNode = right;
			Node oldParent = parent;

			this.right = newNode.left;
			if (this.right != null) {
				this.right.parent = this;
			}

			newNode.left = this;
			this.parent = newNode;

			newNode.parent = oldParent;
			if (oldParent != null) {
				if (oldParent.left == this)
					oldParent.left = newNode;
				else
					oldParent.right = newNode;
			}
		}

		void rotateRight() throws Exception {
			if (left == null) {
				System.err.println("Tried to rotate left into a null");
				throw new Exception("BLAH");
			}
			Node newNode = left;
			Node oldParent = parent;

			// Connection 1
			this.left = newNode.right;
			if (this.left != null) {
				this.left.parent = this;
			}

			// Connection 2
			newNode.right = this;
			this.parent = newNode;

			// Connection 3
			newNode.parent = oldParent;
			if (oldParent != null) {
				if (oldParent.left == this)
					oldParent.left = newNode;
				else
					oldParent.right = newNode;
			}
		}

		public Node leftRight() {
			if (left != null)
				return left.right;
			return null;
		}

		public Node rightLeft() {
			if (right != null)
				return right.left;
			return null;
		}

		// Find the upper node of this node
		public Node upper() {
			Node ret = this.right;
			while (ret.left != null)
				ret = ret.left;
			return ret;
		}

		public void swap(Node o) {

			// Swap the parents
			Node oldParent = this.parent;
			Node newParent = o.parent;

			// Connect the other node to the old parent
			if (oldParent != null)
				if (oldParent.right == this)
					oldParent.right = o;
				else
					oldParent.left = o;
			o.parent = oldParent;

			// Connect the new parent to this node
			if (newParent != null)
				if (newParent.right == o)
					newParent.right = this;
				else
					newParent.left = this;
			parent = newParent;

			// Swap the right children
			Node oldRight = right;
			Node newRight = o.right;

			// Connect the other node to the old right child
			if (oldRight != null)
				oldRight.parent = o;
			o.right = oldRight;

			// Connect this node to the new right child
			if (newRight != null)
				newRight.parent = this;
			right = newRight;

			// Swap the left children
			Node oldLeft = left;
			Node newLeft = o.left;

			// Connect the other node to the old left child
			if (oldLeft != null)
				oldLeft.parent = o;
			o.left = oldLeft;

			// Connect tihs node to the new left child
			if (newLeft != null)
				newLeft.parent = this;
			left = newLeft;

			// Swap colors
			int oldColor = color;
			color = o.color;
			o.color = oldColor;
		}
		
		public String toString(){
			return "" +getValue();
		}
	}
}
