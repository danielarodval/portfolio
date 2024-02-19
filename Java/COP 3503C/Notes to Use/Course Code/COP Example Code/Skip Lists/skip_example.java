import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;

import javax.imageio.ImageIO;

public class skip_example {

	public static final int oo = 1000;
	public static SkipNode right_end = new SkipNode(oo);
	public static SkipNode head;
	public static SkipNode bottom = new SkipNode(oo);
	public static int height = 5;
	public static final int SMALL_SENT = 0;
	public static final int NUM_USES = 15;
	public static final int MAX_VALUE = 20;
	public static final double P_VALUE = 1.0 / 2.0;

	public static void main(String[] Args) throws IOException {
		bottom.below = bottom;
		bottom.right = bottom;
		right_end.right = right_end;
		right_end.below = bottom;

		// Make the left tower
		head = new SkipNode(SMALL_SENT);
		SkipNode prev = head;
		for (int i = 2; i <= height; i++) {
			SkipNode cur = new SkipNode(SMALL_SENT);

			// Set the previous below pointer to the current value
			prev.below = cur;

			// Update the previous value
			prev = cur;
		}

		SkipNode cur = head;
		while (cur != bottom) {
			System.out.println(cur);
			cur = cur.below;
		}

		for (int i = 0; i < NUM_USES; i++) {
			// Try to insert a random value
			int insertValue = 1 + (int) (Math.random() * MAX_VALUE);

			print("INSERTING " + insertValue);
			System.out.println("Trying to insert value " + insertValue);
			if (head.insert(insertValue)) {
				System.out.println("Successfully inserted value " + insertValue);
			} else {
				System.out.println("Failed to insert value " + insertValue);
			}

			// Check if a random value is contained
			int containsValue = 1 + (int) (Math.random() * MAX_VALUE);
			if (head.contains(containsValue)) {
				System.out.println("The value " + containsValue + " is within the skip list.");
			} else {
				System.out.println("The list does not contain the value " + containsValue);
			}

		}
		print("");
	}

	public static class SkipNode {
		SkipNode right;
		SkipNode below;
		int value;

		public SkipNode(int x) {
			right = right_end;
			below = bottom;
			value = x;
		}

		private boolean insert(int inVal) {
			if (contains(inVal))
				return false;
			ArrayList<SkipNode> separation = getSeparation(inVal);
			// System.out.println(separation);
			SkipNode prev = bottom;
			for (int i = 0; i < height; i++) {
				SkipNode newNode = new SkipNode(inVal);

				// Update the right pointer
				newNode.right = separation.get(i).right;
				separation.get(i).right = newNode;

				// Update the bottom pointer
				newNode.below = prev;
				prev = newNode;

				// Randomly decide to build an extra height
				if (Math.random() > P_VALUE)
					return true;
			}
			return true;
		}

		private ArrayList<SkipNode> getSeparation(int sepVal) {
			// We reach the end of the tower return an empty list
			if (this == bottom)
				return new ArrayList<SkipNode>();

			// Impossible case
			if (this == right_end)
				return null;

			// Check if this value is not great enough
			if (right.value < sepVal)
				return right.getSeparation(sepVal);

			// Build the array from the lower skip node
			ArrayList<SkipNode> ret = below.getSeparation(sepVal);
			if (ret == null)
				return null;

			// Add the current node to the list at the end
			ret.add(this);

			// Return the found set
			return ret;
		}

		public boolean contains(int conVal) {
			// System.out.println(this);
			if (this == bottom)
				return false;
			if (this == right_end)
				return false;
			if (right.value < conVal)
				return right.contains(conVal);
			if (right.value == conVal)
				return true;
			return below.contains(conVal);
		}

		public String toString() {
			return value + " r:" + right.value + " b:" + bottom.value;
		}

	}

	// Information for drawing seven segment numbers
	public static final int segment_length = 5;
	public static final int segment_width = 2;
	public static final int digit_buffer = 2;
	public static final int digit_height = 3 + segment_length * 2;
	public static final int digit_width = 2 + segment_length;
	public static final int digit_16_width = 3 + 6;
	public static final int digit_16_height = 3 + 8;
	public static final int digit_16_x_1 = 1 + 3;
	public static final int digit_16_x_2 = 2 + 6;
	public static final int digit_16_y_1 = 1 + 4;
	public static final int digit_16_y_2 = 2 + 8;

	// Method for drawing a value
	public static void drawNumber(BufferedImage bi, int x, int y, int color, int val) {

		int len = Integer.toString(val).length() * (digit_buffer + digit_width) + digit_buffer;
		int hei = digit_height + 2 * digit_buffer;
		int xx = BUFFER_LENGTH + (NODE_WIDTH + BUFFER_LENGTH) * x + VALUE_BOX_WIDTH / 2 - len / 2;
		int yy = BUFFER_LENGTH + (NODE_HEIGHT + BUFFER_LENGTH) * y + VALUE_BOX_HEIGHT / 2 - hei / 2 + BUFFER_LENGTH + digit_16_height;
		for (int i = 0; i < Integer.toString(val).length(); i++) {
			drawDigit(bi, xx + digit_buffer, yy + digit_buffer, color, Integer.toString(val).charAt(i) - '0');
			xx += digit_buffer + digit_width;
		}
	}

	public static void drawString(BufferedImage bi, int x, int y, int color, String s) {
		int len = s.length() * (digit_buffer + digit_16_width) + digit_buffer;
		int hei = digit_16_height + 2 * digit_buffer;
		int xx = x - len / 2;
		int yy = y - hei / 2;
		for (int i = 0; i < s.length(); i++) {
			if (s.charAt(i) >= 'A' && s.charAt(i) <= 'Z')
				drawLetter(bi, xx + digit_buffer, yy + digit_buffer, color, s.charAt(i) - 'A');
			if (s.charAt(i) >= '0' && s.charAt(i) <= '9')
				drawLetter(bi, xx + digit_buffer, yy + digit_buffer, color, s.charAt(i) - '0' + 26);
			xx += digit_buffer + digit_16_width;
		}
	}

	// Method for drawing digit
	public static void drawDigit(BufferedImage bi, int x, int y, int color, int c) {
		for (int i = 0; i < digit_height; i++) {
			for (int j = 0; j < digit_width; j++) {
				if (i < segment_width && (digitImage[c][0]))
					bi.setRGB(x + j, y + i, color);
				if ((i == (digit_height) / 2 || i == digit_height / 2 + 1) && (digitImage[c][3])) {
					bi.setRGB(x + j, y + i, color);
				}
				if (i >= digit_height - segment_width && (digitImage[c][6])) {
					bi.setRGB(x + j, y + i, color);
				}
				if (i >= (digit_height / 2) && j < segment_width && (digitImage[c][4])) {
					bi.setRGB(x + j, y + i, color);
				}
				if (i >= (digit_height / 2) && j >= digit_width - segment_width && (digitImage[c][5])) {
					bi.setRGB(x + j, y + i, color);
				}
				if (i <= (digit_height / 2) && j < segment_width && (digitImage[c][1])) {
					bi.setRGB(x + j, y + i, color);
				}
				if (i <= (digit_height / 2) && j >= digit_width - segment_width && (digitImage[c][2])) {
					bi.setRGB(x + j, y + i, color);
				}
			}
		}
	}

	public static void drawLetter(BufferedImage bi, int x, int y, int color, int c) {
		int mx = x + digit_16_x_1;
		int ex = x + digit_16_x_2;
		int my = y + digit_16_y_1;
		int ey = y + digit_16_y_2;
		if (letterImage[c].charAt(0) == '1')
			drawLine(bi, x, mx, y, y, c);
		if (letterImage[c].charAt(1) == '1')
			drawLine(bi, mx, ex, y, y, c);
		if (letterImage[c].charAt(2) == '1')
			drawLine(bi, x, x, y, my, c);
		if (letterImage[c].charAt(3) == '1')
			drawLine(bi, x, mx, y, my, c);
		if (letterImage[c].charAt(4) == '1')
			drawLine(bi, mx, mx, y, my, c);
		if (letterImage[c].charAt(5) == '1')
			drawLine(bi, ex, mx, y, my, c);
		if (letterImage[c].charAt(6) == '1')
			drawLine(bi, ex, ex, y, my, c);
		if (letterImage[c].charAt(7) == '1')
			drawLine(bi, x, mx, my, my, c);
		if (letterImage[c].charAt(8) == '1')
			drawLine(bi, mx, ex, my, my, c);
		if (letterImage[c].charAt(9) == '1')
			drawLine(bi, x, x, ey, my, c);
		if (letterImage[c].charAt(10) == '1')
			drawLine(bi, x, mx, ey, my, c);
		if (letterImage[c].charAt(11) == '1')
			drawLine(bi, mx, mx, ey, my, c);
		if (letterImage[c].charAt(12) == '1')
			drawLine(bi, ex, mx, ey, my, c);
		if (letterImage[c].charAt(13) == '1')
			drawLine(bi, ex, ex, ey, my, c);
		if (letterImage[c].charAt(14) == '1')
			drawLine(bi, x, mx, ey, ey, c);
		if (letterImage[c].charAt(15) == '1')
			drawLine(bi, mx, ex, ey, ey, c);
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

	// 1 2
	// 3 4 5 6 7
	// 8 9
	// 10 11 12 13 14
	// 15 16
	public static String[] letterImage = { "1110001111000100", // A
			"1100101010010111", // B
			"1110000001000011", // C
			"1100101000010111", // D
			"1110000101000011", // E
			"1110000101000000", // F
			"1110000011000111", // G
			"0010001111000100", // H
			"1100100000010011", // I
			"0000001001000111", // J
			"0010010101001000", // K
			"0010000001000011", // L
			"0011011001000100", // M
			"0011001001001100", // N
			"1110001001000111", // O
			"1110001111000000", // P
			"1110001001001111", // Q
			"1110001111001000", // R
			"1110000110000111", // S
			"1100100000010000", // T
			"0010001001000111", // U
			"0010010001100000", // V
			"0010001001101100", // W
			"0001010000101000", // X
			"0010001110000111", // Y
			"1100010000100011", // Z
			"1110011001100111", // 0
			"0000011000000100", // 1
			"1100001111000011", // 2
			"1100001110000111", // 3
			"0010001110000100", // 4
			"1110000100001011", // 5
			"1110000111000111", // 6
			"1100001000000100", // 7
			"1110001111000111", // 8
			"1110001110000111" // 9
	};

	// Some colors in RGB hex
	public static int white = 0xFFFFFF;
	public static int light_gray = 0xAAAAAA;
	public static int red = 0xFF0000;
	public static int black = 0x000000;
	public static int blue = 0x0000FF;

	public static void print(String message) throws IOException {
		HashMap<Integer, Integer> valToIndex = new HashMap<Integer, Integer>();
		SkipNode lastHead = head;
		while (lastHead.below != bottom) {
			lastHead = lastHead.below;
		}
		int c = 0;

		SkipNode curNode = lastHead;
		while (curNode != right_end) {
			valToIndex.put(curNode.value, c++);
			curNode = curNode.right;
		}
		valToIndex.put(curNode.value, c++);
		System.out.println(valToIndex);

		int[] vals = new int[c];
		for (Integer i : valToIndex.keySet()) {
			vals[valToIndex.get(i)] = i;
		}
		

		int pictureHeight = ((1 + height) * (NODE_HEIGHT + BUFFER_LENGTH)) + BUFFER_LENGTH + BUFFER_LENGTH + digit_16_height;
		int pictureWidth = (c * (NODE_WIDTH + BUFFER_LENGTH)) + BUFFER_LENGTH;
		int width2 = (digit_16_width + digit_buffer) * (message.length()) - digit_buffer + 2 * BUFFER_LENGTH;
		if (width2 > pictureWidth)
			pictureWidth = width2;
		BufferedImage bi = new BufferedImage(pictureWidth, pictureHeight, BufferedImage.TYPE_INT_RGB);
		
		for (int i = 0; i < pictureHeight; i++)
			for (int j = 0; j < pictureWidth; j++)
				bi.setRGB(j, i, white);
		drawString(bi, message.length() * (digit_buffer + digit_16_width) / 2 + BUFFER_LENGTH, BUFFER_LENGTH + digit_16_height / 2, black, message);
		
		SkipNode curHead = head;
		for (int i = 0; i < height; i++) {
			curNode = curHead;
			while (curNode != right_end) {
				drawNode(bi, valToIndex.get(curNode.value), i);
				drawNumber(bi, valToIndex.get(curNode.value), i, black, curNode.value);
				drawRightArrow(bi, valToIndex.get(curNode.value), valToIndex.get(curNode.right.value), i, black);
				drawDownArrow(bi, valToIndex.get(curNode.value), i, i + 1, black);
				curNode = curNode.right;
			}
			drawNode(bi, valToIndex.get(curNode.value), i);
			drawNumber(bi, valToIndex.get(curNode.value), i, black, curNode.value);
			drawDownArrow(bi, valToIndex.get(curNode.value), i, i + 1, black);
			curHead = curHead.below;
		}

		drawNull(bi, height, c);

		ImageIO.write(bi, "PNG", new File("skip_list_" + (imgCount++) + ".png"));
	}

	public static void drawNull(BufferedImage bi, int y_off, int width) {
		int x1 = BUFFER_LENGTH;
		int x2 = width * (BUFFER_LENGTH + NODE_WIDTH);
		int y1 = BUFFER_LENGTH + y_off * (BUFFER_LENGTH + NODE_HEIGHT) + digit_16_height + BUFFER_LENGTH;
		int y2 = y1 + NODE_HEIGHT;

		drawString(bi, (x1 + x2) / 2, (y1 + y2) / 2, black, "SENTINEL");
		drawLine(bi, x1, x2, y1, y1, black);
		drawLine(bi, x1, x2, y2, y2, black);
		drawLine(bi, x2, x2, y1, y2, black);
		drawLine(bi, x1, x1, y1, y2, black);
	}

	public static int imgCount = 0;

	public static int BUFFER_LENGTH = 10;
	public static int VALUE_BOX_HEIGHT = 20;
	public static int VALUE_BOX_WIDTH = 35;
	public static int NODE_HEIGHT = VALUE_BOX_HEIGHT + BUFFER_LENGTH;
	public static int NODE_WIDTH = VALUE_BOX_WIDTH + BUFFER_LENGTH;

	public static void drawNode(BufferedImage bi, int x, int y) {
		int xx = x * (NODE_WIDTH + BUFFER_LENGTH) + BUFFER_LENGTH;
		int yy = y * (NODE_HEIGHT + BUFFER_LENGTH) + BUFFER_LENGTH + digit_16_height + BUFFER_LENGTH;
		int xxe = xx + NODE_WIDTH;
		int yye = yy + NODE_HEIGHT;
		int xxe2 = xx + VALUE_BOX_WIDTH;
		int yye2 = yy + VALUE_BOX_HEIGHT;
		fillRect(bi, xxe2, xxe, yye2, yye, light_gray);
		drawLine(bi, xx, xx, yy, yye, black);
		drawLine(bi, xx, xxe, yy, yy, black);
		drawLine(bi, xxe, xxe, yy, yye, black);
		drawLine(bi, xx, xxe, yye, yye, black);
		drawLine(bi, xxe2, xxe2, yy, yye, black);
		drawLine(bi, xx, xxe, yye2, yye2, black);
	}

	public static void fillRect(BufferedImage bi, int x1, int x2, int y1, int y2, int color) {
		for (int x = x1; x <= x2; x++)
			for (int y = y1; y <= y2; y++)
				bi.setRGB(x, y, color);

	}

	public static double softness = 2;

	public static void drawLine(BufferedImage bi, int x1, int x2, int y1, int y2, int color) {
		double dx = (x1 - x2);
		double dy = (y1 - y2);
		double mag = dx * dx + dy * dy;
		mag = Math.sqrt(mag) * softness;
		dx /= mag;
		dy /= mag;

		// bi.setRGB(x1, y1, color);
		// bi.setRGB(x2, y2, color);

		double cx = x2 + dx;
		double cy = y2 + dy;
		for (int i = 0; i < mag; i++) {
			bi.setRGB((int) Math.round(cx), (int) Math.round(cy), color);
			cx += dx;
			cy += dy;
		}
	}

	public static int x_arrow_off = BUFFER_LENGTH / 2;
	public static int y_arrow_off = BUFFER_LENGTH / 3;

	public static void drawRightArrow(BufferedImage bi, int x1, int x2, int y, int color) {
		int xx = x1 * (NODE_WIDTH + BUFFER_LENGTH) + BUFFER_LENGTH;
		int yy = y * (NODE_HEIGHT + BUFFER_LENGTH) + BUFFER_LENGTH + BUFFER_LENGTH + digit_16_height;
		yy += VALUE_BOX_HEIGHT / 2;
		x1 = xx + VALUE_BOX_WIDTH + BUFFER_LENGTH / 2;
		x2 = x2 * (NODE_WIDTH + BUFFER_LENGTH) + BUFFER_LENGTH;
		drawLine(bi, x1, x2, yy, yy, color);
		drawLine(bi, x2, x2 - x_arrow_off, yy, yy - y_arrow_off, color);
		// drawLine(bi, x2, x2 - x_arrow_off, yy, yy + y_arrow_off, color);
	}

	public static void drawDownArrow(BufferedImage bi, int x, int y1, int y2, int color) {
		int xx = x * (NODE_WIDTH + BUFFER_LENGTH) + BUFFER_LENGTH;
		y1 = y1 * (NODE_HEIGHT + BUFFER_LENGTH) + BUFFER_LENGTH + BUFFER_LENGTH + digit_16_height;
		y2 = y2 * (NODE_HEIGHT + BUFFER_LENGTH) + BUFFER_LENGTH + BUFFER_LENGTH + digit_16_height;
		y1 += VALUE_BOX_HEIGHT + BUFFER_LENGTH / 2;
		xx = xx + VALUE_BOX_WIDTH / 2;
		drawLine(bi, xx, xx, y1, y2, color);
		drawLine(bi, xx, xx + y_arrow_off, y2, y2 - x_arrow_off, color);
		// drawLine(bi, x2, x2 - x_arrow_off, yy, yy + y_arrow_off, color);
	}
}